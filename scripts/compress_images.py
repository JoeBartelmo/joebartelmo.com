#!/usr/bin/env python3
"""Compress raster images under assets/images to a mobile-friendly size.

This script walks the project image tree, optimizes each image for the web,
and keeps every file at or below a target size (default: 1 MB). It is safe to
reuse on a project without changing the folder layout.

Examples:
    python scripts/compress_images.py
    python scripts/compress_images.py --root assets/images --max-size 1048576 --dry-run
    python scripts/compress_images.py --root assets/images --max-width 1600 --quality 72
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Iterable

try:
    from PIL import Image, ImageOps
except ImportError as exc:  # pragma: no cover - CLI guidance
    raise SystemExit(
        "Pillow is required. Install it with: python -m pip install pillow"
    ) from exc

DEFAULT_MAX_SIZE = 512 * 1024
DEFAULT_MAX_WIDTH = 1300
DEFAULT_MAX_HEIGHT = 1300
DEFAULT_QUALITY = 60
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".gif"}


def iter_images(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if path.is_file() and path.suffix.lower() in SUPPORTED_EXTENSIONS:
            yield path


def get_target_format(path: Path, has_alpha: bool) -> str:
    """Choose a modern, mobile-friendly output format.

    JPEG for photos and general images, WEBP for alpha/transparency-heavy files.
    """
    suffix = path.suffix.lower()

    if suffix in {".webp"} and not has_alpha:
        return "JPEG"
    if has_alpha:
        return "WEBP"
    if suffix in {".jpg", ".jpeg"}:
        return "JPEG"
    return "JPEG"


def normalize_size(width: int, height: int, max_width: int, max_height: int) -> tuple[int, int]:
    scale = min(max_width / width, max_height / height, 1.0)
    if scale >= 1.0:
        return width, height
    return max(1, int(round(width * scale))), max(1, int(round(height * scale)))


def process_image(path: Path, max_size: int, max_width: int, max_height: int, quality: int, dry_run: bool) -> tuple[bool, str]:
    """Return (changed, message)."""
    original_size = path.stat().st_size

    if original_size <= max_size:
        return False, f"skipped {path} (already under {max_size / (1024 * 1024):.1f} MB)"

    with Image.open(path) as img:
        img = ImageOps.exif_transpose(img)
        has_alpha = img.mode in {"RGBA", "LA", "PA", "P"} and "transparency" in img.info

        working = img.copy()
        working = working.convert("RGBA" if has_alpha else "RGB")

        target_format = get_target_format(path, has_alpha)
        output_ext = ".webp" if target_format == "WEBP" else ".jpg"
        target_path = path.with_suffix(output_ext)

        if target_path == path:
            temp_path = path.with_suffix(path.suffix + ".tmp")
        else:
            temp_path = path.with_suffix(path.suffix + ".tmp")

        width, height = working.size
        width, height = normalize_size(width, height, max_width, max_height)

        current_quality = quality
        last_size = original_size

        for _ in range(16):
            resized = working.resize((width, height), Image.Resampling.LANCZOS)

            save_kwargs: dict[str, object] = {"optimize": True}
            if target_format == "WEBP":
                save_kwargs.update({"quality": current_quality, "method": 6})
                if has_alpha:
                    save_kwargs["lossless"] = False
            else:
                save_kwargs.update({"quality": current_quality, "progressive": True, "subsampling": 0})

            resized.save(temp_path, format=target_format, **save_kwargs)
            last_size = temp_path.stat().st_size

            if last_size <= max_size:
                if dry_run:
                    temp_path.unlink(missing_ok=True)
                    return False, f"would compress {path} to {last_size / 1024:.1f} KB ({target_format})"

                if target_path.exists() and target_path != path:
                    target_path.unlink()

                temp_path.replace(target_path)

                if target_path != path:
                    path.unlink(missing_ok=True)

                return True, f"compressed {path} to {last_size / 1024:.1f} KB ({target_format})"

            current_quality = max(25, current_quality - 10)
            width = max(1, int(width * 0.9))
            height = max(1, int(height * 0.9))

        temp_path.unlink(missing_ok=True)
        return False, f"could not reduce {path} below {max_size / (1024 * 1024):.1f} MB; final size was {last_size / (1024 * 1024):.2f} MB"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compress images under assets/images to a mobile-friendly maximum size."
    )
    parser.add_argument(
        "--root",
        type=Path,
        default=Path("assets/images"),
        help="Root folder to scan recursively (default: assets/images)",
    )
    parser.add_argument(
        "--max-size",
        type=int,
        default=DEFAULT_MAX_SIZE,
        help="Maximum file size in bytes (default: 1048576 = 1MB)",
    )
    parser.add_argument(
        "--max-width",
        type=int,
        default=DEFAULT_MAX_WIDTH,
        help="Maximum width to retain while resizing (default: 1800)",
    )
    parser.add_argument(
        "--max-height",
        type=int,
        default=DEFAULT_MAX_HEIGHT,
        help="Maximum height to retain while resizing (default: 1800)",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=DEFAULT_QUALITY,
        help="Starting JPEG/WebP quality (default: 78)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Identify files that would be changed without writing to disk",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()

    if not root.exists():
        print(f"Image root does not exist: {root}", file=sys.stderr)
        return 1

    image_files = list(iter_images(root))
    if not image_files:
        print(f"No supported image files found under {root}")
        return 0

    total_changed = 0
    total_bytes_saved = 0

    for path in image_files:
        before = path.stat().st_size
        changed, message = process_image(
            path=path,
            max_size=args.max_size,
            max_width=args.max_width,
            max_height=args.max_height,
            quality=args.quality,
            dry_run=args.dry_run,
        )

        after = path.stat().st_size if path.exists() else before
        if changed:
            total_changed += 1
            total_bytes_saved += max(0, before - after)

        print(message)

    print(f"\nSummary: {len(image_files)} files scanned, {total_changed} files changed.")
    if total_bytes_saved:
        print(f"Estimated savings: {total_bytes_saved / (1024 * 1024):.2f} MB")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
