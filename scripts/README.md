# generate_project_post.py

Quick usage

```bash
python scripts/generate_project_post.py <image-folder-name> "Post Title" --category=development --tags=tag1,tag2
```

Examples

```bash
python scripts/generate_project_post.py basement "Finishing 1000sqft Basement" --category=diy --tags=basement,remodel
```

What it does
- Scans `assets/images/<image-folder-name>` for `before/`, `after/`, and top-level images.
- Generates `_posts/YYYY-MM-DD-title-slug.md` with front-matter and a basic template.

Notes
- The script intentionally creates a simple, editable markdown file — refine the generated
  content manually after generation to match exact phrasing or add more TODO table rows.
