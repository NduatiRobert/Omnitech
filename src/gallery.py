"""
Photo gallery. Each album is a folder inside gallery/, e.g.

    gallery/2026-11-08-montana-mall-site-visit/
        album.md        (optional: title, date, category, location, description)
        captions.txt    (optional: one line per photo ->  photo-1.jpg: Caption text)
        photo-1.jpg
        photo-2.jpg

Photos are resized for the web automatically (full size + thumbnail).
"""
import os
import re
from datetime import date

import markdown_lite as md

IMG_EXT = ("jpg", "jpeg", "png", "webp")
FULL_MAX, THUMB_MAX = 1800, 640


def _date_from(value, folder, fallback):
    for src in (value or "", folder):
        m = re.match(r"(\d{4})-(\d{2})(?:-(\d{2}))?", src.strip())
        if m:
            try:
                return date(int(m.group(1)), int(m.group(2)), int(m.group(3) or 1)), bool(m.group(3))
            except ValueError:
                pass
    return fallback, False


def load_albums(root, today):
    base = os.path.join(root, "gallery")
    albums = []
    if not os.path.isdir(base):
        return albums
    for folder in sorted(os.listdir(base)):
        path = os.path.join(base, folder)
        if not os.path.isdir(path) or folder.startswith(("_", ".")):
            continue
        meta, body = {}, ""
        if os.path.exists(os.path.join(path, "album.md")):
            meta, body = md.parse_front_matter(open(os.path.join(path, "album.md"), encoding="utf-8").read())
        if meta.get("draft", "").lower() in ("true", "yes", "1"):
            continue
        captions = {}
        cap_file = os.path.join(path, "captions.txt")
        if os.path.exists(cap_file):
            for line in open(cap_file, encoding="utf-8"):
                if ":" in line:
                    k, v = line.split(":", 1)
                    captions[k.strip()] = v.strip()
        photos = [f for f in sorted(os.listdir(path)) if f.rsplit(".", 1)[-1].lower() in IMG_EXT and not f.startswith(".")]
        if not photos:
            continue
        d, has_day = _date_from(meta.get("date"), folder, today)
        slug = re.sub(r"^\d{4}-\d{2}(-\d{2})?-", "", folder).lower()
        slug = re.sub(r"[^a-z0-9-]+", "-", slug).strip("-") or folder
        cover = meta.get("cover", "").strip()
        if cover not in photos:
            cover = photos[0]
        albums.append({
            "folder": folder, "slug": slug, "file": f"gallery/{slug}.html",
            "title": meta.get("title") or slug.replace("-", " ").capitalize(),
            "category": meta.get("category", "Projects").strip() or "Projects",
            "location": meta.get("location", ""), "date": d,
            "date_label": f"{d.day} {d.strftime('%B %Y')}" if has_day else d.strftime("%B %Y"),
            "description": md.to_html(body)[0] if body.strip() else "",
            "summary": meta.get("description", "") or md.plain_text(body)[:160],
            "photos": [{"file": f, "caption": captions.get(f, "")} for f in photos],
            "cover": cover, "sample": meta.get("sample", "").lower() in ("true", "yes", "1"),
        })
    albums.sort(key=lambda a: (a["date"], a["title"]), reverse=True)
    return albums


def copy_images(root, out, albums):
    try:
        from PIL import Image, ImageOps
    except ImportError:
        Image = None
    import shutil
    for a in albums:
        src = os.path.join(root, "gallery", a["folder"])
        dst = os.path.join(out, "gallery", "photos", a["slug"])
        os.makedirs(os.path.join(dst, "thumbs"), exist_ok=True)
        for ph in a["photos"]:
            sp = os.path.join(src, ph["file"])
            ext = ph["file"].rsplit(".", 1)[-1].lower()
            if Image is None:
                shutil.copy2(sp, os.path.join(dst, ph["file"]))
                shutil.copy2(sp, os.path.join(dst, "thumbs", ph["file"]))
                continue
            im = ImageOps.exif_transpose(Image.open(sp))
            if ext in ("jpg", "jpeg") and im.mode != "RGB":
                im = im.convert("RGB")
            kw = {"quality": 82, "optimize": True} if ext in ("jpg", "jpeg", "webp") else {"optimize": True}
            for folder, size in (("", FULL_MAX), ("thumbs", THUMB_MAX)):
                c = im.copy()
                c.thumbnail((size, size))
                c.save(os.path.join(dst, folder, ph["file"]), **kw)
