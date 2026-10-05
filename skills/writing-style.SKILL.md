---
name: Writing Style and Project Post Template
version: 1.1
description: |
  Use this skill to turn a provided project image folder into a concise project post.
  Favor short, direct writing, high-value details, and a compact task table instead of long narrative paragraphs.
author: automated-assistant
---

Purpose
-
Write project posts that feel like a quick, honest recap of a build or upgrade. The goal is to sound practical, useful, and clear without over-explaining.

Core writing direction
-
- Keep it short and direct.
- Favor tight paragraphs and clean section headers.
- Cut fluff. Start with the point.
- Use a table for the project checklist or summary.
- Prefer practical detail over storytelling filler.
- Write in first person, conversationally, but keep the structure readable.

Voice
-
- "This project was..."
- "I wanted..."
- "The main issue was..."
- "The final result is..."
- "Here’s what I changed and what I’d do differently."

Preferred structure
-
1. Short intro: what the project was and why it mattered.
2. One sentence on the design or goal.
3. "The List" table with status, category, task, time, difficulty, notes.
4. A couple of short sections for key decisions or challenges.
5. After Photos gallery.

Table format
-
Use a table for the project summary instead of a long prose checklist. A good default is:

| Status | Category | Task | Time | Difficulty | Notes |
| --- | --- | --- | --- | --- | --- |
| ✅ | Design | ... | ... | ... | ... |
| ✅ | Build | ... | ... | ... | ... |
| ⚠️ | Problem | ... | ... | ... | ... |

Keep the notes column high-signal: what changed, what mattered, what was frustrating, what was worth it.

Image-driven workflow
-
When the user provides a folder of images, do this first:
- Compress the image set before writing. Reduce each file to a practical web/mobile size, with a hard cap of 1MB per image.
- Keep aspect ratio and crop only as needed to preserve composition, but avoid oversized originals that do not need full-resolution detail.
- Use a reduced-size preview set for review and article drafting; do not rewrite from raw 20MB-60MB files when the site only needs mobile-friendly imagery.
- Inspect the compressed folder and choose the clearest representative image for the header.
- Prefer `after/` images for the main gallery when available.
- Use the image set to infer the story: before/after, key materials, layout changes, problem solved, or finish quality.
- Ask for missing details only when needed.

Prompting for input
-
Before writing, ask for the minimum needed information to produce a good post. Good defaults:
- project title
- category
- relevant tags
- folder path or image set
- what the project was for
- what changed or was improved
- any rough time/cost/difficulty notes
- any notable mistakes, constraints, or decisions

If the image folder is clear enough, do not over-question. If it is not, ask only the missing high-value inputs.

Front matter
-
Use front matter like this:

---
title: "{{title}}"
categories:
  - {{category}}
tags:
  - {{tag1}}
  - {{tag2}}
toc: true
toc_label: "Table of Contents"
toc_icon: "cog"
header:
  og_image: /assets/images/{{image_folder}}/{{representative_image}}
---

Content rules
-
- Write short, concrete paragraphs.
- Keep sections focused: overview, list, key notes, after photos.
- Use markdown headings and a clean hierarchy.
- Use image syntax like:
  `![Alt Text](/assets/images/<folder>/after/image.jpg){:class="img-responsive"}`
- If there are paired before/after images, call that out plainly.
- Avoid long setup, author intros, or generic background.
- Prefer direct language like: "This was a straightforward fix," "The big issue was...," "I’d do this differently next time."

Output preference
-
The final article should read like a practical recap, not a blog essay. It should give the reader a fast understanding of the project, the work done, and the result without excess prose.

Canonical structure
-
## Overview
Short intro; what it was; why it mattered.

## The List
Markdown table summarizing the work.

## Key Notes
Short bullets or brief sections on design choices, problems, and materials.

## After Photos
Image gallery and representative figures.

Generator expectation
-
Create a new post in `_posts/` using the date and slug pattern. If image folders exist, first compress the assets to a web-safe size and use the optimized set for the gallery. Use the most useful images, not necessarily all of them. Keep the article compact and direct.

If you want a more opinionated version, tell the generator to favor even shorter writeups and tighter tables with fewer words per cell.

Compression requirement
-
- No image should exceed 1MB.
- Prefer a long-edge target in the 1200-1600px range for web display.
- Keep a practical mobile-friendly balance between clarity and file size.
- Use the optimized images as the source for the post, and use the existing site assets as the reference for visual review when needed.
