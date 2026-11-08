"""
Portfolio / projects. Each project is a Markdown file in portfolio/ (see portfolio/_TEMPLATE.md).
Photos go in portfolio/images/. They are resized automatically for fast loading.
"""
import glob
import os
import re
from datetime import date

import markdown_lite as md

IMG_MAX = 1600   # px, longest side for full-size photos
THUMB_MAX = 800  # px, card thumbnails


def _parse_date(value, fallback):
    value = (value or "").strip()
    for fmt_len in (10, 7, 4):
        try:
            v = value[:fmt_len]
            if fmt_len == 10:
                return date.fromisoformat(v)
            if fmt_len == 7:
                y, m = v.split("-")
                return date(int(y), int(m), 1)
            return date(int(v), 1, 1)
        except (ValueError, TypeError):
            continue
    return fallback


def _list(value):
    return [x.strip() for x in (value or "").split(",") if x.strip()]


def load_projects(root, today, services_by_slug):
    projects = []
    for path in sorted(glob.glob(os.path.join(root, "portfolio", "*.md"))):
        name = os.path.basename(path)
        if name.startswith("_"):
            continue
        meta, body = md.parse_front_matter(open(path, encoding="utf-8").read())
        if meta.get("draft", "").lower() in ("true", "yes", "1"):
            continue
        d = _parse_date(meta.get("date"), today)
        slug = re.sub(r"^\d{4}(-\d{2}){0,2}-", "", name[:-3])
        services = [s for s in _list(meta.get("service")) if s in services_by_slug]
        body_html, _ = md.to_html(body)
        projects.append({
            "slug": slug, "file": f"portfolio/{slug}.html",
            "title": meta.get("title", slug.replace("-", " ").title()),
            "client": meta.get("client", ""), "location": meta.get("location", ""),
            "date": d, "date_label": meta.get("date", "")[:7] and d.strftime("%B %Y") or str(d.year),
            "services": services, "summary": meta.get("summary", md.plain_text(body)[:155]),
            "highlights": _list(meta.get("highlights")),
            "cover": meta.get("cover", "").strip(), "gallery": _list(meta.get("gallery")),
            "featured": meta.get("featured", "").lower() in ("true", "yes", "1"),
            "sample": meta.get("sample", "").lower() in ("true", "yes", "1"),
            "html": body_html,
        })
    projects.sort(key=lambda p: (p["featured"], p["date"], p["title"]), reverse=True)
    return projects


def copy_images(root, out):
    """Copies portfolio/images to site/portfolio/images, resizing large photos and making thumbnails."""
    src = os.path.join(root, "portfolio", "images")
    if not os.path.isdir(src):
        return
    dst = os.path.join(out, "portfolio", "images")
    os.makedirs(os.path.join(dst, "thumbs"), exist_ok=True)
    try:
        from PIL import Image, ImageOps
    except ImportError:
        Image = None
    for name in os.listdir(src):
        sp = os.path.join(src, name)
        if not os.path.isfile(sp) or name.startswith("."):
            continue
        ext = name.rsplit(".", 1)[-1].lower()
        if Image is None or ext not in ("jpg", "jpeg", "png", "webp"):
            import shutil
            shutil.copy2(sp, os.path.join(dst, name))
            shutil.copy2(sp, os.path.join(dst, "thumbs", name))
            continue
        im = ImageOps.exif_transpose(Image.open(sp))
        save_kw = {"quality": 82, "optimize": True} if ext in ("jpg", "jpeg", "webp") else {"optimize": True}
        if ext in ("jpg", "jpeg") and im.mode != "RGB":
            im = im.convert("RGB")
        for folder, size in (("", IMG_MAX), ("thumbs", THUMB_MAX)):
            copy = im.copy()
            copy.thumbnail((size, size))
            copy.save(os.path.join(dst, folder, name), **save_kw)
