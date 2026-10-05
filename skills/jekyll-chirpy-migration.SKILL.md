---
name: Jekyll Site Editing and Chirpy Migration
version: 1.0
description: |
  Use this skill when editing the code, content structure, and theme behavior of this Jekyll site.
  This project originally started as a Minimal Mistakes site and is being converted to the Chirpy theme.
author: automated-assistant
---

Purpose
-
This repository is a Jekyll-powered personal site that originally used the Minimal Mistakes theme and is now in transition to the Chirpy theme. Use this skill when making content, layout, config, or site-structure changes.

Project context
-
- The site was originally based on Minimal Mistakes: https://mmistakes.github.io/minimal-mistakes/docs/quick-start-guide/
- The current configuration is moving toward the Chirpy theme: https://chirpy.cotes.page/posts/write-a-new-post/
- The project is not intended to be maintained as a local Ruby-only Jekyll setup.
- The supported build path is the Dockerfile at the repository root.

Migration guidance
-
- Treat this as a migration from Minimal Mistakes conventions to Chirpy conventions.
- Do not assume old Minimal Mistakes layouts, front matter, or theme conventions are still the source of truth.
- Prefer Chirpy-style front matter, page layouts, post structure, and category/tag handling.
- Preserve the site’s own content and customizations, but update the site structure to match modern Chirpy expectations.
- Review existing data in `_config.yml`, `_posts/`, `_pages/`, `_includes/`, and `assets/` before making structural changes.

Important build rule
-
This project does not build correctly with local Ruby/Jekyll commands in a host environment. The canonical build path is the Dockerfile in the root directory.

Do not do this locally:
- `bundle install`
- `bundle exec jekyll serve`
- any direct Ruby/Jekyll install workflow on the host machine

Use this instead:
- `docker build -t joebartelmo-site .`
- `docker run --rm -p 4000:4000 -v "$PWD":/srv/jekyll joebartelmo-site`

If a site preview is needed, use the Dockerized Jekyll workflow defined by the root Dockerfile. The container is the supported development environment.

Site architecture
-
This project contains these key areas:
- `_config.yml` — site settings, theme config, defaults, plugins, and Chirpy-specific metadata
- `_posts/` — blog posts
- `_pages/` — standalone pages
- `assets/images/` — image sources; optimize and compress before use
- `_includes/` — page partials and reusable HTML
- `_data/` — data files for navigation and similar content
- `resume.html` — standalone resume output

When editing the site, keep the structure clean and predictable:
- Prefer the existing top-level Jekyll conventions already in use
- Keep pages modular and easy to maintain
- Do not introduce new custom build scripts unless the site clearly requires them
- Preserve compatibility with the Docker-based build environment

Theme migration rules
-
- Minimal Mistakes was the original starting point, but the active configuration and intent now follow Chirpy.
- Update layouts and metadata to fit Chirpy naming and defaults where needed.
- Keep page content usable in a mobile-friendly, responsive theme environment.
- When converting older content, prefer Chirpy-compatible front matter and structure over legacy Minimal Mistakes metadata.
- Do not rely on Minimal Mistakes-only features or settings unless you are intentionally preserving them for a specific compatibility reason.

Content and post conventions
-
When creating or editing posts, follow the Chirpy writing pattern described in the project docs:
- Use clear front matter with title, categories, tags, and relevant metadata
- Keep posts concise, readable, and mobile friendly
- Favor short sections, clear headings, and useful images
- Ensure visual assets are compressed and lightweight

Recommended post structure:
- intro paragraph
- relevant sections or key notes
- bullet list or table for project details when useful
- hero or supporting images
- concise conclusion

Image handling rules
-
Images in `assets/images/` must stay web-optimized and mobile-compatible.

Constraints:
- No image should exceed 1MB.
- Prefer a long-edge target in the 1200-1600px range for web display.
- Reduce oversized originals before using them in posts or pages.
- Maintain good clarity at mobile sizes without wasting bandwidth.
- Keep aspect ratio intact and crop only when needed.

When adding screenshots or galleries:
- compress the originals before committing
- prefer clear, representative images over full-size raw files
- choose the most legible mobile-friendly assets for the page

Editing expectations
-
When making project changes, prefer the following workflow:
1. Review the current site structure and relevant theme config.
2. Check whether the change belongs in front matter, layout, include, content, or assets.
3. Ensure the change works with the Dockerized Jekyll environment rather than host Ruby.
4. Keep the site mobile-friendly and performance-aware.
5. Preserve clean Jekyll conventions and avoid broad refactors unless necessary.

Do not
-
- assume the project can be built with a local Ruby/Jekyll install
- add theme code that depends on Minimal Mistakes-only behavior without a clear reason
- introduce large raw image files into the repo
- change broad site structure without checking the existing Chirpy configuration and Docker workflow

Summary
-
This site is best treated as a Chirpy migration project that retains older content and custom assets, but is no longer a stock Minimal Mistakes site. Build and preview it through the root Dockerfile, not by running Ruby locally.
