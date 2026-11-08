"""
A small Markdown converter (no external libraries needed).

Supports: front matter (--- key: value ---), ## / ### / #### headings, paragraphs,
- bullet and 1. numbered lists, > quotes, ![alt](image.jpg), [links](url),
**bold**, *italic*, `code`, --- horizontal rules, and simple | tables |.
"""
import html
import re


def slugify(text):
    text = re.sub(r"<[^>]+>", "", text).lower()
    text = re.sub(r"[^a-z0-9\s-]", "", text)
    return re.sub(r"[\s-]+", "-", text).strip("-")


def parse_front_matter(raw):
    meta = {}
    if raw.startswith("---"):
        end = raw.find("\n---", 3)
        if end != -1:
            for line in raw[3:end].strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    meta[k.strip().lower()] = v.strip().strip('"').strip("'")
            raw = raw[end + 4:]
    return meta, raw.strip()


def inline(text):
    text = html.escape(text, quote=False)
    codes = []
    text = re.sub(r"`([^`]+)`", lambda m: codes.append(m.group(1)) or f"\x00{len(codes)-1}\x00", text)
    text = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)",
                  lambda m: f'<img src="{m.group(2)}" alt="{html.escape(m.group(1))}" loading="lazy">', text)

    def link(m):
        label, url = m.group(1), m.group(2)
        ext = url.startswith("http") and "omnitech" not in url
        rel = ' target="_blank" rel="noopener"' if ext else ""
        return f'<a href="{url}"{rel}>{label}</a>'
    text = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", link, text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<![*\w])\*([^*\n]+)\*(?!\w)", r"<em>\1</em>", text)
    text = re.sub(r"\x00(\d+)\x00", lambda m: f"<code>{codes[int(m.group(1))]}</code>", text)
    return text


def to_html(md):
    """Returns (html, toc) where toc is a list of (id, title) for ## headings."""
    lines = md.replace("\r\n", "\n").split("\n")
    out, toc, para, i = [], [], [], 0

    def flush():
        if para:
            out.append(f"<p>{inline(' '.join(para))}</p>")
            para.clear()

    while i < len(lines):
        line = lines[i].rstrip()
        s = line.strip()
        if not s:
            flush(); i += 1; continue
        m = re.match(r"^(#{2,4})\s+(.*)$", s)
        if m:
            flush()
            lvl, title = len(m.group(1)), m.group(2).strip()
            hid = slugify(title)
            if lvl == 2:
                toc.append((hid, re.sub(r"[*`]", "", title)))
            out.append(f'<h{lvl} id="{hid}">{inline(title)}</h{lvl}>')
            i += 1; continue
        if re.match(r"^(-{3,}|\*{3,})$", s):
            flush(); out.append("<hr>"); i += 1; continue
        if s.startswith(">"):
            flush(); buf = []
            while i < len(lines) and lines[i].strip().startswith(">"):
                buf.append(lines[i].strip()[1:].strip()); i += 1
            out.append(f"<blockquote><p>{inline(' '.join(buf))}</p></blockquote>")
            continue
        if re.match(r"^[-*]\s+", s) or re.match(r"^\d+[.)]\s+", s):
            flush()
            ordered = bool(re.match(r"^\d+[.)]\s+", s))
            pat = r"^\d+[.)]\s+" if ordered else r"^[-*]\s+"
            items = []
            while i < len(lines) and re.match(pat, lines[i].strip()):
                items.append(re.sub(pat, "", lines[i].strip()))
                i += 1
                while i < len(lines) and lines[i].startswith(("  ", "\t")) and lines[i].strip():
                    items[-1] += " " + lines[i].strip(); i += 1
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{inline(x)}</li>" for x in items) + f"</{tag}>")
            continue
        if s.startswith("|"):
            flush(); rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")]); i += 1
            if len(rows) > 1 and all(re.match(r"^:?-+:?$", c) for c in rows[1]):
                head, body = rows[0], rows[2:]
            else:
                head, body = None, rows
            t = '<div class="table-wrap"><table>'
            if head:
                t += "<thead><tr>" + "".join(f"<th>{inline(c)}</th>" for c in head) + "</tr></thead>"
            t += "<tbody>" + "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in body) + "</tbody></table></div>"
            out.append(t)
            continue
        if re.match(r"^!\[[^\]]*\]\([^)]+\)$", s):
            flush(); out.append(f"<figure>{inline(s)}</figure>"); i += 1; continue
        para.append(s); i += 1
    flush()
    return "\n".join(out), toc


def plain_text(md):
    t = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", md)
    t = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", t)
    t = re.sub(r"[#>*`|_-]", " ", t)
    return re.sub(r"\s+", " ", t).strip()
