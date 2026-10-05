#!/usr/bin/env python3
"""Generate a new Jekyll project post from an images folder.

Usage:
  python scripts/generate_project_post.py <image-folder-name> "Post Title" --category diy --tags tag1,tag2

The script looks under `assets/images/<image-folder-name>` for images and optional
`before/` and `after/` subfolders to build galleries. It creates a file under `_posts/`.
"""
import os
import sys
import datetime

def slugify(s):
    s = s.strip().lower()
    keep = []
    for ch in s:
        if ch.isalnum() or ch in [' ', '-']:
            keep.append(ch)
    return '-'.join(''.join(keep).split())

def gather_images(images_root):
    images = {'after': [], 'before': [], 'root': []}
    if not os.path.isdir(images_root):
        return images
    for entry in sorted(os.listdir(images_root)):
        path = os.path.join(images_root, entry)
        if os.path.isdir(path):
            if entry.lower() == 'after':
                images['after'] = sorted([f for f in os.listdir(path) if not f.startswith('.')])
            elif entry.lower() == 'before':
                images['before'] = sorted([f for f in os.listdir(path) if not f.startswith('.')])
        else:
            if entry.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.webp')):
                images['root'].append(entry)
    return images

def build_front_matter(title, category, tags, og_image_path):
    tags_yaml = '\n'.join([f"  - {t.strip()}" for t in tags if t.strip()])
    fm = ["---"]
    fm.append(f'title: "{title}"')
    fm.append('categories:')
    fm.append(f'  - {category}')
    fm.append('tags:')
    fm.append(tags_yaml if tags_yaml else '  - diy')
    fm.append('toc: true')
    fm.append('toc_label: "Table of Contents"')
    fm.append('toc_icon: "cog"')
    fm.append('header:')
    fm.append(f'  og_image: {og_image_path}')
    fm.append('')
    fm.append('---\n')
    return '\n'.join(fm)

def build_body(title, image_folder, images):
    intro = [
        f"I may do a mini-series of posts on this at some point. This project, {title}, was a focused effort and worth documenting.",
        '',
        '## Project Overview',
        '',
        'Write a short overview here describing goals, constraints, and motivation.',
        '',
        '## The List',
        '',
        '| Status | Category | TODO Item | Time taken | Difficulty | Notes |',
        '|--|--|--|--|--|--|',
        '| - | 🧰 General | Placeholder task | - | Medium | Fill this in |',
        '',
    ]

    # After photos
    gallery = []
    gallery.append('## After Photos\n')
    if images.get('after'):
        gallery.append('<figure class="half">')
        for img in images['after'][:6]:
            gallery.append(f'  <a href="/assets/images/{image_folder}/after/{img}"><img src="/assets/images/{image_folder}/after/{img}"></a>')
        gallery.append('</figure>\n')
    elif images.get('root'):
        gallery.append('<figure class="half">')
        for img in images['root'][:6]:
            gallery.append(f'  <a href="/assets/images/{image_folder}/{img}"><img src="/assets/images/{image_folder}/{img}"></a>')
        gallery.append('</figure>\n')
    else:
        gallery.append('_No images found in the specified folder._\n')

    return '\n'.join(intro + gallery)

def main():
    if len(sys.argv) < 3:
        print('Usage: python scripts/generate_project_post.py <image-folder-name> "Post Title" [--category cat] [--tags t1,t2]')
        sys.exit(1)

    image_folder = sys.argv[1]
    title = sys.argv[2]
    category = 'diy'
    tags = []
    for arg in sys.argv[3:]:
        if arg.startswith('--category'):
            category = arg.split('=',1)[1] if '=' in arg else sys.argv[sys.argv.index(arg)+1]
        if arg.startswith('--tags'):
            parts = arg.split('=',1)
            if len(parts) == 2:
                tags = parts[1].split(',')

    images_root = os.path.join('assets', 'images', image_folder)
    images = gather_images(images_root)

    # choose og_image
    og = None
    if images.get('after'):
        og = f'/assets/images/{image_folder}/after/{images["after"][0]}'
    elif images.get('root'):
        og = f'/assets/images/{image_folder}/{images["root"][0]}'
    else:
        og = '/assets/images/favicon/site.webmanifest'

    slug = slugify(title)
    today = datetime.date.today().isoformat()
    filename = f"{today}-{slug}.md"
    post_path = os.path.join('_posts', filename)

    front = build_front_matter(title, category, tags or ['diy'], og)
    body = build_body(title, image_folder, images)

    content = front + body

    with open(post_path, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'Created post: {post_path}')

if __name__ == '__main__':
    main()
