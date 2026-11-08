#!/usr/bin/env python3
"""
Builds the static Omnitech Systems website into ./site

    python3 build.py

Edit copy in src/content.py and business details in src/config.py.
"""
import glob
import html
import json
import math
import os
import re
import shutil
import sys
from datetime import date
from urllib.parse import quote

ROOT = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT, "src"))

import config as C  # noqa: E402
from content import SERVICES, SERVICE_BY_SLUG, PROCESS, WHY, HOME_FAQS, ZOHO_APPS, ZOHO_OFFER_LOGOS  # noqa: E402
from icons import icon  # noqa: E402
import markdown_lite as md  # noqa: E402
import illustrations  # noqa: E402
from illustrations import illustration  # noqa: E402
import portfolio as pf  # noqa: E402
import gallery as gal  # noqa: E402

OUT = os.path.join(ROOT, "site")
esc = html.escape


def fill(text):
    return text.replace("{LOCATION}", C.LOCATION)


def wa_link(msg="Hello Omnitech Systems, I'd like to enquire about your services."):
    return f"https://wa.me/{C.WHATSAPP}?text={quote(msg)}"


TODAY = date.today()
POSTS_PER_PAGE = 9

# Main Google keyword for each service page (used in the <title> with your city)
SEO_KW = {
    "cctv-installation": "CCTV Installation",
    "internet-installation": "Internet & Wi-Fi Installation",
    "hotspot-business": "Wi-Fi Hotspot Billing Systems",
    "website-development": "Website Design & Development",
    "software-development": "Custom Software Development",
    "digital-marketing": "Digital Marketing & SEO",
    "business-automation": "Business Automation",
    "zoho-consulting": "Zoho Consulting & Implementation",
}

CATEGORY_ICON = {
    "CCTV & Security": "camera", "Internet & Networking": "wifi", "Hotspot Business": "hotspot",
    "Websites": "globe", "Software": "code", "Digital Marketing": "megaphone",
    "Automation": "zap", "Zoho": "grid", "Business Tips": "chart",
}


def asset_version(rel):
    """Short content hash so browsers and Cloudflare fetch a fresh copy whenever the file changes."""
    import hashlib
    try:
        return hashlib.md5(open(os.path.join(OUT, rel), "rb").read()).hexdigest()[:10]
    except OSError:
        return "1"


def abs_url(path=""):
    return f"{C.SITE_URL}/{path}"


def fill_vars(text):
    return (text.replace("{COMPANY}", C.COMPANY).replace("{EMAIL}", C.EMAIL)
            .replace("{PHONE}", C.PHONE_DISPLAY).replace("{LOCATION}", C.LOCATION))


def nice_date(d):
    return f"{d.day} {d.strftime('%B %Y')}"


def load_posts():
    posts = []
    for path in sorted(glob.glob(os.path.join(ROOT, "blog", "*.md"))):
        name = os.path.basename(path)
        if name.startswith("_"):
            continue
        meta, body = md.parse_front_matter(open(path, encoding="utf-8").read())
        if meta.get("draft", "").lower() in ("true", "yes", "1"):
            continue
        try:
            d = date.fromisoformat(meta.get("date", "")[:10])
        except ValueError:
            m = re.match(r"(\d{4}-\d{2}-\d{2})", name)
            d = date.fromisoformat(m.group(1)) if m else TODAY
        if d > TODAY:  # scheduled for a future date
            continue
        slug = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", name[:-3])
        body_html, toc = md.to_html(body)
        words = len(md.plain_text(body).split())
        img = meta.get("image", "").strip()
        posts.append({
            "slug": slug, "file": f"blog/{slug}.html",
            "title": meta.get("title", slug.replace("-", " ").title()),
            "description": meta.get("description", md.plain_text(body)[:155]),
            "category": meta.get("category", "Business Tips"), "service": meta.get("service", ""),
            "author": meta.get("author", f"{C.COMPANY} Team"), "date": d,
            "updated": date.fromisoformat(meta["updated"][:10]) if meta.get("updated") else d,
            "image": img, "html": body_html, "toc": toc,
            "minutes": max(1, math.ceil(words / 220)), "words": words,
        })
    posts.sort(key=lambda p: (p["date"], p["title"]), reverse=True)
    return posts


POSTS = []
PROJECTS = []
ALBUMS = []


# ---------------------------------------------------------------- PIECES
def logo(light=False, pre=""):
    f = C.LOGO_FILE_LIGHT if (light and C.LOGO_FILE_LIGHT) else C.LOGO_FILE
    if f:
        return f'<img src="{pre}{f}" alt="{esc(C.COMPANY)} logo" class="logo-img" width="394" height="132">'
    return ('<span class="logo-mark" aria-hidden="true">'
            '<svg viewBox="0 0 32 32"><circle cx="16" cy="16" r="11" fill="none" stroke="currentColor" stroke-width="3.2"/>'
            '<circle cx="16" cy="16" r="4.2" fill="currentColor"/></svg></span>'
            '<span class="logo-text">Omnitech<small>Systems</small></span>')


def header(active, pre=""):
    groups = {}
    for s in SERVICES:
        groups.setdefault(s["group"], []).append(s)
    cols = ""
    for g, items in groups.items():
        links = "".join(
            f'<a href="{pre}{s["slug"]}.html" class="dd-item{" is-active" if active == s["slug"] else ""}">'
            f'<span class="dd-ic">{icon(s["icon"])}</span><span><strong>{esc(s["nav"])}</strong>'
            f'<small>{esc(s["short"])}</small></span></a>'
            for s in items)
        cols += f'<div class="dd-col"><p class="dd-label">{esc(g)}</p>{links}</div>'

    def nl(href, label, key):
        cur = ' aria-current="page"' if active == key else ""
        return f'<a href="{href}" class="nav-link"{cur}>{label}</a>'

    svc_active = " is-active" if active in SERVICE_BY_SLUG or active == "services" else ""
    return f'''
<header class="site-header" id="top">
  <div class="container header-inner">
    <a href="{pre}index.html" class="logo" aria-label="{esc(C.COMPANY)} home">{logo(pre=pre)}</a>
    <nav class="main-nav" id="main-nav" aria-label="Main">
      {nl(pre + "index.html", "Home", "home")}
      <div class="nav-dd">
        <button class="nav-link dd-toggle{svc_active}" aria-expanded="false" aria-controls="dd-services">Services {icon("chevron", "ic ic-sm")}</button>
        <div class="dd-panel" id="dd-services">{cols}
          <a href="{pre}services.html" class="dd-all">View all services {icon("arrow", "ic ic-sm")}</a>
        </div>
      </div>
      {nl(pre + "index.html#about", "About", "about")}
      {nl(pre + "portfolio.html", "Portfolio", "portfolio")}
      {nl(pre + "gallery.html", "Gallery", "gallery")}
      {nl(pre + "blog.html", "Blog", "blog")}
      {nl(pre + "contact.html", "Contact", "contact")}
      <a href="{pre}contact.html" class="btn btn-primary nav-cta-mobile">Get a Free Quote {icon("arrow", "ic ic-sm")}</a>
    </nav>
    <div class="header-actions">
      <a href="{wa_link()}" class="btn btn-ghost btn-sm hide-sm" target="_blank" rel="noopener">{icon("whatsapp", "ic ic-sm")} WhatsApp</a>
      <a href="{pre}contact.html" class="btn btn-primary btn-sm hide-sm">Get a Free Quote</a>
      <button class="menu-btn" aria-label="Open menu" aria-expanded="false" aria-controls="main-nav">{icon("menu")}</button>
    </div>
  </div>
</header>'''


def socials():
    labels = {"facebook": "Facebook", "instagram": "Instagram", "linkedin": "LinkedIn", "tiktok": "TikTok", "x": "X"}
    links = "".join(f'<a href="{u}" target="_blank" rel="noopener">{labels.get(k, k.title())}</a>'
                    for k, u in C.SOCIAL_LINKS.items() if u)
    return f'<p class="socials">{links}</p>' if links else ""


def footer(pre=""):
    sec = "".join(f'<li><a href="{pre}{s["slug"]}.html">{esc(s["nav"])}</a></li>' for s in SERVICES)
    return f'''
<section class="cta-wrap">
  <div class="container">
    <div class="cta-band">
      <div class="cta-glow g1"></div><div class="cta-glow g2"></div>
      <p class="eyebrow eyebrow-light">Let's talk</p>
      <h2>Ready to secure, connect and grow your business?</h2>
      <p>Tell us what you need. We'll recommend the right solution and send you a clear quotation.</p>
      <div class="btn-row">
        <a href="{pre}contact.html" class="btn btn-primary">Get a Free Quote {icon("arrow", "ic ic-sm")}</a>
        <a href="{wa_link()}" class="btn btn-outline-light" target="_blank" rel="noopener">{icon("whatsapp", "ic ic-sm")} Chat on WhatsApp</a>
      </div>
    </div>
  </div>
</section>
<footer class="site-footer">
  <div class="container footer-grid">
    <div class="footer-brand">
      <a href="{pre}index.html" class="logo logo-light">{logo(light=True, pre=pre)}</a>
      <p>{esc(C.TAGLINE)}</p>
      <img src="{pre}assets/img/zoho-authorized-partner.png" alt="Zoho Authorized Partner" class="partner-badge" width="200" height="74" loading="lazy">
      {socials()}
    </div>
    <div><h3>Services</h3><ul>{sec}</ul></div>
    <div><h3>Company</h3><ul>
      <li><a href="{pre}index.html#about">About us</a></li>
      <li><a href="{pre}services.html">All services</a></li>
      <li><a href="{pre}portfolio.html">Portfolio</a></li>
      <li><a href="{pre}gallery.html">Gallery</a></li>
      <li><a href="{pre}blog.html">Blog</a></li>
      <li><a href="{pre}index.html#faq">FAQs</a></li>
      <li><a href="{pre}contact.html">Contact</a></li>
      <li><a href="{pre}privacy-policy.html">Privacy Policy</a></li>
      <li><a href="{pre}terms-and-conditions.html">Terms & Conditions</a></li>
    </ul></div>
    <div><h3>Get in touch</h3><ul class="contact-list">
      <li>{icon("call", "ic ic-sm")}<a href="tel:{C.PHONE_LINK}">{esc(C.PHONE_DISPLAY)}</a></li>
      <li>{icon("whatsapp", "ic ic-sm")}<a href="{wa_link()}" target="_blank" rel="noopener">Chat on WhatsApp</a></li>
      <li>{icon("mail", "ic ic-sm")}<a href="mailto:{C.EMAIL}">{esc(C.EMAIL)}</a></li>
      <li>{icon("pin", "ic ic-sm")}<a href="{C.MAPS_URL}" target="_blank" rel="noopener">{esc(C.LOCATION)}</a></li>
      <li>{icon("globe", "ic ic-sm")}<span>Serving all of Kenya, and clients across East Africa and the UAE</span></li>
      <li>{icon("clock", "ic ic-sm")}<span>{esc(C.HOURS)}</span></li>
    </ul></div>
  </div>
  <div class="container footer-bottom">
    <p>&copy; <span data-year>{TODAY.year}</span> {esc(C.COMPANY)}. All rights reserved. Zoho and related product names are trademarks of Zoho Corporation.</p>
    <p class="footer-legal"><a href="{pre}privacy-policy.html">Privacy Policy</a><a href="{pre}terms-and-conditions.html">Terms & Conditions</a><a href="{pre}sitemap.xml">Sitemap</a></p>
  </div>
</footer>
<a href="{wa_link()}" class="wa-float" target="_blank" rel="noopener" aria-label="Chat with us on WhatsApp">{icon("whatsapp")}</a>'''


def faq_block(faqs, title="Frequently asked questions", sub="Straight answers to the questions we hear most."):
    items = "".join(
        f'<details class="faq-item"{" open" if i == 0 else ""}><summary>{esc(fill(q))}'
        f'<span class="faq-ic">{icon("chevron", "ic ic-sm")}</span></summary>'
        f'<div class="faq-a"><p>{esc(fill(a))}</p></div></details>'
        for i, (q, a) in enumerate(faqs))
    return f'''
<section class="section" id="faq">
  <div class="container faq-grid">
    <div class="faq-intro">
      <p class="eyebrow">FAQ</p>
      <h2>{title}</h2>
      <p class="lead-sm">{sub}</p>
      <a href="contact.html" class="btn btn-ghost">Ask us a question {icon("arrow", "ic ic-sm")}</a>
    </div>
    <div class="faq-list">{items}</div>
  </div>
</section>'''


def process_block(title="Simple. Structured. Practical.", sub="A clear four-step approach from first conversation to ongoing support."):
    steps = "".join(
        f'<div class="card step"><span class="step-n">{n}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></div>'
        for n, t, d in PROCESS)
    return f'''
<section class="section">
  <div class="container">
    <p class="eyebrow">Our process</p>
    <h2>{title}</h2>
    <p class="lead-sm">{sub}</p>
    <div class="grid-4 mt-lg">{steps}</div>
  </div>
</section>'''


def why_block():
    items = "".join(
        f'<div class="why-item"><span class="why-ic">{icon(i)}</span><h3>{esc(t)}</h3><p>{esc(d)}</p></div>'
        for i, t, d in WHY)
    return f'''
<section class="section section-tint" id="about">
  <div class="container">
    <p class="eyebrow">Why {esc(C.COMPANY)}</p>
    <h2>Technical skill, grounded in<br class="hide-sm-br"> how businesses run</h2>
    <p class="lead-sm">{esc(C.COMPANY)} brings physical security, connectivity and digital solutions under one roof — so you have one trusted partner for the technology your business depends on.</p>
    <div class="grid-4 mt-lg">{items}</div>
  </div>
</section>'''


def service_card(s):
    return (f'<a href="{s["slug"]}.html" class="card svc-card">'
            f'<span class="svc-ic">{icon(s["icon"])}</span>'
            f'<h3>{esc(s["name"])}</h3><p>{esc(s["short"])}</p>'
            f'<span class="link-arrow">Explore service {icon("arrow", "ic ic-sm")}</span></a>')


def faq_schema(faqs):
    data = {"@context": "https://schema.org", "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": fill(q),
                            "acceptedAnswer": {"@type": "Answer", "text": fill(a)}} for q, a in faqs]}
    return ld(data)


def ld(data):
    return f'<script type="application/ld+json">{json.dumps(data, ensure_ascii=False)}</script>'


def org_data():
    addr = {"@type": "PostalAddress", "addressLocality": C.CITY, "addressRegion": "Nairobi County", "addressCountry": "KE"}
    if C.STREET:
        addr["streetAddress"] = C.STREET
    data = {
        "@context": "https://schema.org", "@type": ["LocalBusiness", "ProfessionalService"],
        "@id": abs_url("#business"), "name": C.COMPANY, "url": abs_url(),
        "logo": abs_url(C.LOGO_FILE), "image": abs_url("assets/img/og-image.png"),
        "telephone": C.PHONE_LINK, "email": C.EMAIL, "description": C.TAGLINE,
        "address": addr, "openingHours": C.OPENING_HOURS,
        "areaServed": [{"@type": "Country", "name": a} for a in C.AREA_SERVED],
        "contactPoint": {"@type": "ContactPoint", "telephone": C.PHONE_LINK, "contactType": "customer service",
                         "areaServed": "KE", "availableLanguage": ["English", "Swahili"]},
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": "IT & Security Services", "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": s["name"], "url": abs_url(s["slug"] + ".html")}}
            for s in SERVICES]},
    }
    same = [u for u in C.SOCIAL_LINKS.values() if u]
    if same:
        data["sameAs"] = same
    return data


def website_data():
    return {"@context": "https://schema.org", "@type": "WebSite", "@id": abs_url("#website"),
            "name": C.COMPANY, "url": abs_url(), "publisher": {"@id": abs_url("#business")}}


def crumbs_schema(items):
    """items: list of (name, path) — path relative to the site root ('' = home)."""
    return ld({"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": abs_url(p)} for i, (n, p) in enumerate(items)]})


def org_schema():
    return ld(org_data()) + ld(website_data())


def page(filename, title, desc, active, body, extra_head="", full_title=None, og_type="website",
         image=None, noindex=False, pre=""):
    full_title = full_title or f"{title} | {C.COMPANY}"
    canonical = abs_url("" if filename == "index.html" else filename)
    img = image if (image or "").startswith("http") else abs_url(image or "assets/img/og-image.png")
    verify = (f'<meta name="google-site-verification" content="{esc(C.GOOGLE_SITE_VERIFICATION)}">\n'
              if C.GOOGLE_SITE_VERIFICATION else "")
    ga = ""
    if C.GA_MEASUREMENT_ID:
        ga = (f'<script async src="https://www.googletagmanager.com/gtag/js?id={C.GA_MEASUREMENT_ID}"></script>\n'
              f"<script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}"
              f"gtag('js',new Date());gtag('config','{C.GA_MEASUREMENT_ID}');</script>\n")
    robots = "noindex, follow" if noindex else "index, follow, max-image-preview:large, max-snippet:-1"
    doc = f'''<!doctype html>
<html lang="en-KE">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(full_title)}</title>
<meta name="description" content="{esc(desc)}">
<meta name="robots" content="{robots}">
<link rel="canonical" href="{canonical}">
<meta property="og:site_name" content="{esc(C.COMPANY)}">
<meta property="og:locale" content="en_KE">
<meta property="og:type" content="{og_type}">
<meta property="og:title" content="{esc(full_title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{img}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(full_title)}">
<meta name="twitter:description" content="{esc(desc)}">
<meta name="twitter:image" content="{img}">
<meta name="geo.region" content="KE">
<meta name="geo.placename" content="{esc(C.CITY)}">
{verify}<meta name="theme-color" content="#0c0b17">
<link rel="icon" href="{pre}assets/img/favicon.png" type="image/png">
<link rel="apple-touch-icon" href="{pre}assets/img/apple-touch-icon.png">
<link rel="alternate" type="application/rss+xml" title="{esc(C.COMPANY)} Blog" href="{abs_url('feed.xml')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<link rel="stylesheet" href="{pre}assets/css/styles.css?v={asset_version('assets/css/styles.css')}">
{ga}{extra_head}
</head>
<body>
<a href="#main" class="skip-link">Skip to content</a>
{header(active, pre)}
<main id="main">
{body}
</main>
{footer(pre)}
<script src="{pre}assets/js/main.js?v={asset_version('assets/js/main.js')}" defer></script>
</body>
</html>
'''
    path = os.path.join(OUT, filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(doc)
    print("built", filename)


# ---------------------------------------------------------------- ZOHO LOGOS
def zoho_logo_path(key):
    """Official Zoho product icon, if it has been added to site/assets/img/zoho/."""
    for ext in ("svg", "png", "webp"):
        rel = f"assets/img/zoho/{key}.{ext}"
        if os.path.exists(os.path.join(OUT, rel)):
            return rel
    return None


def zoho_apps_block():
    tiles = ""
    for key, name, desc, fallback in ZOHO_APPS:
        path = zoho_logo_path(key)
        logo = (f'<img src="{path}" alt="{esc(name)} logo" width="48" height="48" loading="lazy">' if path
                else f'<span class="svc-ic">{icon(fallback)}</span>')
        tiles += f'<div class="card zapp">{logo}<div><h3>{esc(name)}</h3><p>{esc(desc)}</p></div></div>'
    return f'''
<section class="section section-tint">
  <div class="container">
    <p class="eyebrow">Zoho apps we implement</p>
    <h2>One ecosystem, set up around your business</h2>
    <p class="lead-sm">We help you choose the right Zoho apps, connect them and train your team to use them every day.</p>
    <div class="zapps mt-lg">{tiles}</div>
  </div>
</section>'''


# ---------------------------------------------------------------- PARTNER LOGOS
def load_partners():
    """Logos in site/assets/img/partners/. Optional partners.txt: file | Name | https://link (one per line)."""
    folder = os.path.join(OUT, "assets/img/partners")
    if not os.path.isdir(folder):
        return []
    extra = {}
    txt = os.path.join(folder, "partners.txt")
    if os.path.exists(txt):
        for line in open(txt, encoding="utf-8"):
            parts = [x.strip() for x in line.split("|")]
            if parts and parts[0] and not parts[0].startswith("#"):
                extra[parts[0]] = parts[1:]
    logos = []
    for f in sorted(os.listdir(folder)):
        if f.rsplit(".", 1)[-1].lower() not in ("svg", "png", "webp", "jpg", "jpeg"):
            continue
        info = extra.get(f, [])
        base = re.sub(r"^\d+[-_ ]*", "", f.rsplit(".", 1)[0])
        name = info[0] if info and info[0] else base.replace("-", " ").replace("_", " ").title()
        url = info[1] if len(info) > 1 else ""
        logos.append({"file": f"assets/img/partners/{f}", "name": name, "url": url})
    return logos


def partners_block():
    logos = load_partners()
    if not logos:
        return ""
    def item(l, hidden=False):
        img = f'<img src="{l["file"]}" alt="{"" if hidden else esc(l["name"])}" loading="lazy" height="44">'
        attrs = ' aria-hidden="true"' if hidden else ""
        if l["url"] and not hidden:
            return f'<li><a href="{esc(l["url"])}" target="_blank" rel="noopener" title="{esc(l["name"])}">{img}</a></li>'
        return f'<li{attrs}>{img}</li>'
    # Repeat short lists so each half of the loop is wider than a large screen (no gap)
    reps = max(1, math.ceil(12 / len(logos)))
    track = "".join(item(l) for l in logos) + "".join(item(l, hidden=True) for l in logos * (reps - 1))
    clone = "".join(item(l, hidden=True) for l in logos * reps)  # second half makes the loop seamless
    dur = max(24, len(logos) * reps * 3)
    return f'''
<section class="partners" aria-label="{esc(C.PARTNERS_TITLE)}">
  <div class="container">
    <p class="partners-title">{esc(C.PARTNERS_TITLE)}</p>
  </div>
  <div class="marquee" style="--dur:{dur}s">
    <ul class="marquee-track">{track}{clone}</ul>
  </div>
</section>'''


# ---------------------------------------------------------------- HERO MEDIA
def hero_media(key, label):
    """Uses a real photo from site/assets/img/hero/<key>.(webp|jpg|jpeg|png) when present, otherwise the illustration."""
    for ext in ("webp", "jpg", "jpeg", "png"):
        rel = f"assets/img/hero/{key}.{ext}"
        if os.path.exists(os.path.join(OUT, rel)):
            try:
                from PIL import Image
                w, h = Image.open(os.path.join(OUT, rel)).size
            except Exception:
                w, h = 1280, 960
            return (f'<img src="{rel}" alt="{esc(label)}" width="{w}" height="{h}" fetchpriority="high" decoding="async">')
    return illustration(key, label)


# ---------------------------------------------------------------- BLOG PIECES
def post_cover(p, pre="", big=False):
    """Uses the article photo if set, otherwise a branded graphic with the category icon."""
    if p["image"]:
        src = p["image"] if p["image"].startswith("http") else pre + "blog/" + p["image"]
        return (f'<div class="post-cover has-img"><img src="{src}" alt="{esc(p["title"])}" loading="lazy" '
                f'width="1200" height="675"></div>')
    ic = CATEGORY_ICON.get(p["category"], "chart")
    return (f'<div class="post-cover{" big" if big else ""}" aria-hidden="true"><span class="pc-ic">{icon(ic)}</span>'
            f'<span class="pc-cat">{esc(p["category"])}</span></div>')


def post_meta(p):
    return (f'<p class="post-meta"><time datetime="{p["date"].isoformat()}">{nice_date(p["date"])}</time>'
            f'<span>·</span><span>{p["minutes"]} min read</span></p>')


def post_card(p, pre=""):
    return (f'<a href="{pre}{p["file"]}" class="card post-card" data-cat="{esc(p["category"])}">'
            f'{post_cover(p, pre)}<div class="post-body"><span class="post-cat">{esc(p["category"])}</span>'
            f'<h3>{esc(p["title"])}</h3><p>{esc(p["description"])}</p>{post_meta(p)}</div></a>')


def latest_posts_block():
    if not POSTS:
        return ""
    cards = "".join(post_card(p) for p in POSTS[:3])
    return f'''
<section class="section">
  <div class="container">
    <div class="section-head">
      <div><p class="eyebrow">From the blog</p><h2>Tips, guides and insights</h2>
      <p class="lead-sm">Practical advice on security, connectivity and technology for Kenyan businesses.</p></div>
      <a href="blog.html" class="btn btn-ghost">View all articles {icon("arrow", "ic ic-sm")}</a>
    </div>
    <div class="grid-3 mt-lg">{cards}</div>
  </div>
</section>'''


def service_posts_block(s):
    posts = [p for p in POSTS if p["service"] == s["slug"]][:3]
    if not posts:
        return ""
    return f'''
<section class="section pt-0">
  <div class="container">
    <p class="eyebrow">Helpful reading</p>
    <h2>{esc(s["nav"])} guides</h2>
    <div class="grid-3 mt-lg">{"".join(post_card(p) for p in posts)}</div>
  </div>
</section>'''


# ---------------------------------------------------------------- PAGES
def build_home():
    sec_cc = [s for s in SERVICES if s["group"] == "Security & Connectivity"]
    dig = [s for s in SERVICES if s["group"] == "Digital & Software"]
    body = f'''
<section class="hero hero-dark">
  <div class="hero-glow g-a"></div><div class="hero-glow g-b"></div>
  <div class="container hero-grid">
    <div class="hero-copy">
      <p class="hero-badge">Security · Connectivity · IT Solutions</p>
      <h1>Secure your premises.<br><span class="accent">Connect and grow your business.</span></h1>
      <p class="lead">{esc(C.COMPANY)} installs CCTV, internet and Wi-Fi hotspot systems, and builds the websites, software, automations and Zoho solutions that help businesses run smarter.</p>
      <div class="btn-row">
        <a href="contact.html" class="btn btn-primary">Get a Free Quote {icon("arrow", "ic ic-sm")}</a>
        <a href="{wa_link()}" class="btn btn-outline-light" target="_blank" rel="noopener">{icon("whatsapp", "ic ic-sm")} Chat on WhatsApp</a>
      </div>
      <ul class="hero-points">
        <li>{icon("check", "ic ic-sm")} Free site surveys</li>
        <li>{icon("check", "ic ic-sm")} Itemised quotations</li>
        <li>{icon("check", "ic ic-sm")} After-sales support</li>
      </ul>
    </div>
    <div class="hero-media">{hero_media("home", "Outdoor Wi-Fi security camera installed on a building wall by Omnitech Systems")}</div>
  </div>
</section>

{partners_block()}

<section class="section" id="services">
  <div class="container">
    <p class="eyebrow">Our services</p>
    <h2>End-to-end technology solutions<br class="hide-sm-br"> under one roof</h2>
    <p class="lead-sm">From the cameras on your walls to the software on your screens — practical solutions, properly installed and supported.</p>
    <div class="grid-4 mt-lg">{"".join(service_card(s) for s in SERVICES)}</div>
  </div>
</section>

<section class="section section-tint">
  <div class="container split">
    <div class="card split-card">
      <p class="eyebrow">Security & Connectivity</p>
      <h2 class="h3">Protect and connect your premises</h2>
      <p>Physical installations done neatly and to standard — with clear documentation and support afterwards.</p>
      <ul class="check-list">
        {"".join(f'<li>{icon("check", "ic ic-sm")}<a href="{s["slug"]}.html">{esc(s["name"])}</a></li>' for s in sec_cc)}
        <li>{icon("check", "ic ic-sm")}<span>Access control, alarms & structured cabling</span></li>
        <li>{icon("check", "ic ic-sm")}<span>Maintenance & support contracts</span></li>
      </ul>
      <a href="cctv-installation.html" class="btn btn-ghost">Explore security & networking {icon("arrow", "ic ic-sm")}</a>
    </div>
    <div class="card split-card dark">
      <p class="eyebrow eyebrow-light">Digital & Software</p>
      <h2 class="h3">Go further with smart IT solutions</h2>
      <p>We build the digital tools that win customers, cut manual work and keep your business information connected.</p>
      <div class="tags">
        {"".join(f'<a class="tag" href="{s["slug"]}.html">{esc(s["nav"])}</a>' for s in dig)}
        <span class="tag">M-Pesa integration</span><span class="tag">KRA eTIMS</span>
      </div>
      <a href="software-development.html" class="btn btn-primary">Discuss your project {icon("arrow", "ic ic-sm")}</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <p class="eyebrow">Who we serve</p>
    <h2>Built for businesses, homes and institutions</h2>
    <p class="lead-sm">From our office at {esc(C.LOCATION)}, we serve clients in every city and town in Kenya, and work remotely with businesses in Uganda, Tanzania, Rwanda, the UAE and beyond.</p>
    <div class="sector-row mt-lg">
      {"".join(f'<span class="sector">{icon(i, "ic ic-sm")} {t}</span>' for i, t in [("box","Retail & shops"),("monitor","Offices & SMEs"),("book","Schools & colleges"),("layers","Estates & apartments"),("users","Hotels & restaurants"),("lifebuoy","Clinics & hospitals"),("server","Warehouses"),("globe","NGOs & churches")])}
    </div>
  </div>
</section>

{process_block()}
{why_block()}
{projects_block(PROJECTS[:3], "Recent projects", "A look at some of the work we've delivered for our clients.")}
{latest_posts_block()}
{faq_block(HOME_FAQS, sub="Straight answers about how we work. Each service page has its own detailed FAQs.")}
'''
    page("index.html", C.COMPANY,
         f"CCTV installation, internet & Wi-Fi, hotspot billing, websites, software, digital marketing "
         f"and Zoho consulting in {C.CITY}. Call {C.PHONE_DISPLAY}.",
         "home", body, org_schema() + faq_schema(HOME_FAQS),
         full_title=f"CCTV, Internet & IT Solutions in {C.CITY}, {C.COUNTRY} | {C.COMPANY}")


def build_services_index():
    groups = {}
    for s in SERVICES:
        groups.setdefault(s["group"], []).append(s)
    blocks = ""
    for g, items in groups.items():
        blocks += (f'<div class="svc-group"><p class="eyebrow">{esc(g)}</p>'
                   f'<div class="grid-4 mt-md">{"".join(service_card(s) for s in items)}</div></div>')
    body = f'''
<section class="page-hero">
  <div class="container">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>Services</span></nav>
    <p class="eyebrow">Our services</p>
    <h1>Everything your business needs,<br class="hide-sm-br"> <span class="accent">from one partner.</span></h1>
    <p class="lead">Choose a service to see what's included, how we work and answers to common questions.</p>
  </div>
</section>
<section class="section pt-0"><div class="container">{blocks}</div></section>
{process_block()}
'''
    page("services.html", "Our Services",
         "Explore Omnitech Systems services: CCTV, internet installation, hotspot business, websites, software, digital marketing, automation and Zoho.",
         "services", body, crumbs_schema([("Home", ""), ("Services", "services.html")]),
         full_title=f"IT, Security & Networking Services in {C.CITY} | {C.COMPANY}")


def build_service(s):
    def offer_icon(i, t):
        paths = [zoho_logo_path(k) for k in ZOHO_OFFER_LOGOS.get(t, [])] if s["slug"] == "zoho-consulting" else []
        paths = [x for x in paths if x]
        if paths:
            return '<span class="offer-logos">' + "".join(
                f'<img src="{x}" alt="" width="46" height="46" loading="lazy">' for x in paths) + '</span>'
        return f'<span class="svc-ic">{icon(i)}</span>'
    offers = "".join(
        f'<div class="card offer">{offer_icon(i, t)}<h3>{esc(t)}</h3><p>{esc(d)}</p></div>'
        for i, t, d in s["offer"])
    inc = "".join(f'<li>{icon("check", "ic ic-sm")} {esc(x)}</li>' for x in s["includes"])
    f = s["feature"]
    tags = "".join(f'<span class="tag">{esc(t)}</span>' for t in f["tags"])
    sectors = "".join(f'<span class="sector">{icon("check", "ic ic-sm")} {esc(x)}</span>' for x in s["sectors"])
    related = "".join(service_card(SERVICE_BY_SLUG[r]) for r in s["related"])
    msg = f"Hello Omnitech Systems, I'd like a quote for {s['name']}."
    body = f'''
<section class="hero hero-dark hero-service">
  <div class="hero-glow g-a"></div><div class="hero-glow g-b"></div>
  <div class="container hero-grid">
    <div class="hero-copy">
      <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><a href="services.html">Services</a><span>/</span><span>{esc(s["nav"])}</span></nav>
      <p class="hero-badge">{esc(s["eyebrow"])}</p>
      <h1>{esc(s["h1"])}<br><span class="accent">{esc(s["h1_accent"])}</span></h1>
      <p class="lead">{esc(s["lead"])}</p>
      <div class="btn-row">
        <a href="contact.html?service={s["slug"]}" class="btn btn-primary">Request a Quote {icon("arrow", "ic ic-sm")}</a>
        <a href="{wa_link(msg)}" class="btn btn-outline-light" target="_blank" rel="noopener">{icon("whatsapp", "ic ic-sm")} Chat on WhatsApp</a>
      </div>
    </div>
    <div class="hero-media">{hero_media(s["slug"], s["name"])}</div>
  </div>
</section>

<section class="includes-band">
  <div class="container includes-inner">
    <p class="fc-label">What's included</p>
    <ul>{inc}</ul>
    <a href="#faq" class="link-arrow">Read the FAQs {icon("arrow", "ic ic-sm")}</a>
  </div>
</section>

<section class="section">
  <div class="container">
    <p class="eyebrow">What we offer</p>
    <h2>{esc(s["offer_title"])}</h2>
    <p class="lead-sm">{esc(s["offer_lead"])}</p>
    <div class="grid-3 mt-lg">{offers}</div>
  </div>
</section>

<section class="section pt-0">
  <div class="container split">
    <div class="card split-card dark">
      <p class="eyebrow eyebrow-light">{esc(f["eyebrow"])}</p>
      <h2 class="h3">{esc(f["title"])}</h2>
      <p>{esc(f["text"])}</p>
      <div class="tags">{tags}</div>
      <a href="contact.html?service={s["slug"]}" class="btn btn-primary">Talk to an expert {icon("arrow", "ic ic-sm")}</a>
    </div>
    <div class="card split-card">
      <p class="eyebrow">Who it's for</p>
      <h2 class="h3">Trusted across sectors</h2>
      <p>We tailor every project to the environment, the budget and the people who will use it.</p>
      <div class="sector-row">{sectors}</div>
    </div>
  </div>
</section>

{zoho_apps_block() if s["slug"] == "zoho-consulting" else ""}
{process_block()}
{faq_block(s["faqs"], title=esc(s["nav"]) + " FAQs")}
{projects_block([p for p in PROJECTS if s["slug"] in p["services"]][:3], "Recent " + esc(s["nav"]) + " projects", "Examples of similar work we've delivered.", "Portfolio")}
{service_posts_block(s)}

<section class="section section-tint">
  <div class="container">
    <p class="eyebrow">Related services</p>
    <h2>You might also need</h2>
    <div class="grid-3 mt-lg">{related}</div>
  </div>
</section>
'''
    kw = SEO_KW.get(s["slug"], s["name"])
    desc = f'{s["short"]} Based in {C.CITY}, serving all of {C.COUNTRY}. Free quote: {C.PHONE_DISPLAY}.'
    service_ld = ld({
        "@context": "https://schema.org", "@type": "Service", "name": s["name"], "serviceType": kw,
        "description": s["lead"], "url": abs_url(s["slug"] + ".html"),
        "provider": {"@id": abs_url("#business")},
        "areaServed": [{"@type": "Country", "name": a} for a in C.AREA_SERVED],
        "hasOfferCatalog": {"@type": "OfferCatalog", "name": s["name"], "itemListElement": [
            {"@type": "Offer", "itemOffered": {"@type": "Service", "name": t, "description": d}} for _, t, d in s["offer"]]},
    })
    page(f'{s["slug"]}.html', s["name"], desc, s["slug"], body,
         service_ld + faq_schema(s["faqs"]) + crumbs_schema([("Home", ""), ("Services", "services.html"), (s["nav"], s["slug"] + ".html")]),
         full_title=f"{kw} in {C.CITY}, {C.COUNTRY} | {C.COMPANY}")


def build_contact():
    opts = "".join(f'<option value="{s["slug"]}">{esc(s["name"])}</option>' for s in SERVICES)
    body = f'''
<section class="page-hero">
  <div class="container">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>Contact</span></nav>
    <p class="eyebrow">Contact us</p>
    <h1>Let's talk about <span class="accent">your project.</span></h1>
    <p class="lead">Tell us what you need and we'll get back to you with recommendations and a clear quotation.</p>
  </div>
</section>
<section class="section pt-0">
  <div class="container contact-grid">
    <form class="card contact-form" id="quote-form" data-wa="{C.WHATSAPP}" novalidate>
      <h2 class="h3">Request a free quote</h2>
      <p class="muted">Your message opens in WhatsApp, ready to send.</p>
      <div class="form-row">
        <label>Full name<input name="name" required autocomplete="name"></label>
        <label>Phone number<input name="phone" type="tel" required autocomplete="tel"></label>
      </div>
      <div class="form-row">
        <label>Email (optional)<input name="email" type="email" autocomplete="email"></label>
        <label>Location / town<input name="location"></label>
      </div>
      <label>Service needed
        <select name="service" required><option value="">Select a service</option>{opts}<option value="other">Something else</option></select>
      </label>
      <label>Tell us about your project<textarea name="message" rows="5" placeholder="e.g. 8 cameras for a 2-storey shop, with phone viewing"></textarea></label>
      <p class="form-error" role="alert" hidden>Please fill in your name, phone number and the service you need.</p>
      <button class="btn btn-primary btn-block" type="submit">{icon("whatsapp", "ic ic-sm")} Send via WhatsApp</button>
    </form>
    <aside class="contact-side">
      <div class="card contact-card">
        <h2 class="h3">Reach us directly</h2>
        <ul class="contact-list">
          <li><span class="svc-ic">{icon("call")}</span><div><small>Call us</small><a href="tel:{C.PHONE_LINK}">{esc(C.PHONE_DISPLAY)}</a></div></li>
          <li><span class="svc-ic">{icon("whatsapp")}</span><div><small>WhatsApp</small><a href="{wa_link()}" target="_blank" rel="noopener">Start a chat</a></div></li>
          <li><span class="svc-ic">{icon("mail")}</span><div><small>Email</small><a href="mailto:{C.EMAIL}">{esc(C.EMAIL)}</a></div></li>
          <li><span class="svc-ic">{icon("pin")}</span><div><small>Office</small><a href="{C.MAPS_URL}" target="_blank" rel="noopener">{esc(C.LOCATION)}</a></div></li>
          <li><span class="svc-ic">{icon("globe")}</span><div><small>Areas we serve</small><span>All of Kenya · Remote projects in Uganda, Tanzania, Rwanda, the UAE and beyond</span></div></li>
          <li><span class="svc-ic">{icon("clock")}</span><div><small>Working hours</small><span>{esc(C.HOURS)}</span></div></li>
        </ul>
      </div>
      <div class="card split-card dark">
        <p class="eyebrow eyebrow-light">Free site survey</p>
        <h2 class="h3">Not sure what you need?</h2>
        <p>For CCTV, networking and hotspot projects we'll assess your premises and recommend the right setup before you commit.</p>
      </div>
    </aside>
  </div>
</section>
'''
    page("contact.html", "Contact Us & Get a Quote",
         "Contact Omnitech Systems for a free quote on CCTV, internet, hotspot, website, software, marketing, automation and Zoho services.",
         "contact", body, crumbs_schema([("Home", ""), ("Contact", "contact.html")]),
         full_title=f"Contact {C.COMPANY} | Free Quote in {C.CITY}")


def build_blog_index():
    cats = sorted({p["category"] for p in POSTS})
    pages = max(1, math.ceil(len(POSTS) / POSTS_PER_PAGE))
    for n in range(1, pages + 1):
        chunk = POSTS[(n - 1) * POSTS_PER_PAGE: n * POSTS_PER_PAGE]
        fname = "blog.html" if n == 1 else f"blog-page-{n}.html"
        featured = ""
        rest = chunk
        if n == 1 and chunk:
            fp, rest = chunk[0], chunk[1:]
            featured = f'''
    <a href="{fp["file"]}" class="card featured-post" data-cat="{esc(fp["category"])}">
      {post_cover(fp, big=True)}
      <div class="post-body">
        <span class="post-cat">Latest · {esc(fp["category"])}</span>
        <h2>{esc(fp["title"])}</h2>
        <p>{esc(fp["description"])}</p>
        {post_meta(fp)}
        <span class="link-arrow">Read article {icon("arrow", "ic ic-sm")}</span>
      </div>
    </a>'''
        chips = ""
        if n == 1 and len(cats) > 1:
            chips = ('<div class="chips" role="group" aria-label="Filter by category">'
                     '<button class="chip is-active" data-filter="all">All</button>'
                     + "".join(f'<button class="chip" data-filter="{esc(c)}">{esc(c)}</button>' for c in cats) + '</div>')
        pager = ""
        if pages > 1:
            links = []
            if n > 1:
                links.append(f'<a href="{"blog.html" if n == 2 else f"blog-page-{n-1}.html"}" rel="prev">← Newer</a>')
            for k in range(1, pages + 1):
                href = "blog.html" if k == 1 else f"blog-page-{k}.html"
                links.append(f'<a href="{href}"{" aria-current=\"page\"" if k == n else ""}>{k}</a>')
            if n < pages:
                links.append(f'<a href="blog-page-{n+1}.html" rel="next">Older →</a>')
            pager = f'<nav class="pager" aria-label="Blog pages">{"".join(links)}</nav>'
        empty = '<p class="muted">New articles are coming soon.</p>' if not POSTS else ""
        body = f'''
<section class="page-hero">
  <div class="container">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>Blog</span></nav>
    <p class="eyebrow">Blog</p>
    <h1>Insights for <span class="accent">smarter businesses.</span></h1>
    <p class="lead">Guides and tips on CCTV, internet, hotspots, websites, software, marketing and automation, written for businesses in {esc(C.COUNTRY)}.</p>
  </div>
</section>
<section class="section pt-0">
  <div class="container">
    {featured}
    {chips}
    {empty}
    <div class="grid-3 mt-lg post-grid">{"".join(post_card(p) for p in rest)}</div>
    {pager}
  </div>
</section>'''
        blog_ld = ld({"@context": "https://schema.org", "@type": "Blog", "name": f"{C.COMPANY} Blog",
                      "url": abs_url("blog.html"), "publisher": {"@id": abs_url("#business")},
                      "blogPost": [{"@type": "BlogPosting", "headline": p["title"], "url": abs_url(p["file"]),
                                    "datePublished": p["date"].isoformat()} for p in chunk]})
        suffix = "" if n == 1 else f" (Page {n})"
        page(fname, "Blog", f"Tips and guides on CCTV, internet, hotspot business, websites, software and digital marketing in {C.COUNTRY} from {C.COMPANY}.",
             "blog", body, blog_ld + crumbs_schema([("Home", ""), ("Blog", "blog.html")]),
             full_title=f"Blog: Tech Tips for {C.COUNTRY}n Businesses{suffix} | {C.COMPANY}")


def build_posts():
    pre = "../"
    for p in POSTS:
        svc = SERVICE_BY_SLUG.get(p["service"])
        toc = ""
        if len(p["toc"]) >= 3:
            toc = ('<nav class="card toc" aria-label="In this article"><p class="fc-label">In this article</p><ol>'
                   + "".join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in p["toc"]) + "</ol></nav>")
        url = abs_url(p["file"])
        share = (f'<div class="share"><span class="fc-label">Share</span>'
                 f'<a href="https://wa.me/?text={quote(p["title"] + " " + url)}" target="_blank" rel="noopener">WhatsApp</a>'
                 f'<a href="https://www.facebook.com/sharer/sharer.php?u={quote(url)}" target="_blank" rel="noopener">Facebook</a>'
                 f'<a href="https://www.linkedin.com/sharing/share-offsite/?url={quote(url)}" target="_blank" rel="noopener">LinkedIn</a>'
                 f'<a href="https://x.com/intent/post?url={quote(url)}&text={quote(p["title"])}" target="_blank" rel="noopener">X</a></div>')
        cta = ""
        if svc:
            cta = f'''<div class="card split-card dark side-cta">
          <span class="svc-ic">{icon(svc["icon"])}</span>
          <p class="eyebrow eyebrow-light">Our service</p>
          <h2 class="h3">{esc(svc["name"])}</h2>
          <p>{esc(svc["short"])}</p>
          <a href="{pre}{svc["slug"]}.html" class="btn btn-primary">Learn more {icon("arrow", "ic ic-sm")}</a>
        </div>'''
        else:
            cta = f'''<div class="card split-card dark side-cta">
          <p class="eyebrow eyebrow-light">Need help?</p>
          <h2 class="h3">Talk to our team</h2>
          <p>Get practical advice and a clear quotation for your project.</p>
          <a href="{pre}contact.html" class="btn btn-primary">Get a free quote {icon("arrow", "ic ic-sm")}</a>
        </div>'''
        related = [q for q in POSTS if q is not p and q["category"] == p["category"]]
        related += [q for q in POSTS if q is not p and q not in related]
        rel_html = ""
        if related:
            rel_html = f'''
<section class="section section-tint">
  <div class="container">
    <p class="eyebrow">Keep reading</p>
    <h2>More articles</h2>
    <div class="grid-3 mt-lg">{"".join(post_card(q, pre) for q in related[:3])}</div>
  </div>
</section>'''
        updated = ""
        if p["updated"] != p["date"]:
            updated = f' <span>·</span> <span>Updated <time datetime="{p["updated"].isoformat()}">{nice_date(p["updated"])}</time></span>'
        cover = post_cover(p, pre, big=True) if p["image"] else ""
        body = f'''
<article>
<header class="page-hero post-hero">
  <div class="container">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="{pre}index.html">Home</a><span>/</span><a href="{pre}blog.html">Blog</a><span>/</span><span>{esc(p["category"])}</span></nav>
    <span class="post-cat">{esc(p["category"])}</span>
    <h1>{esc(p["title"])}</h1>
    <p class="lead">{esc(p["description"])}</p>
    <p class="post-meta big"><span>By {esc(p["author"])}</span><span>·</span><time datetime="{p["date"].isoformat()}">{nice_date(p["date"])}</time><span>·</span><span>{p["minutes"]} min read</span>{updated}</p>
  </div>
</header>
<section class="section pt-0">
  <div class="container post-layout">
    <div class="post-main">
      {cover}
      <div class="prose">{p["html"]}</div>
      {share}
    </div>
    <aside class="post-side">
      {toc}
      {cta}
    </aside>
  </div>
</section>
</article>
{rel_html}'''
        art = {"@context": "https://schema.org", "@type": "BlogPosting", "headline": p["title"],
               "description": p["description"], "datePublished": p["date"].isoformat(),
               "dateModified": p["updated"].isoformat(), "wordCount": p["words"],
               "mainEntityOfPage": {"@type": "WebPage", "@id": url}, "url": url,
               "author": {"@type": "Organization", "name": p["author"], "url": abs_url()},
               "publisher": {"@type": "Organization", "name": C.COMPANY,
                             "logo": {"@type": "ImageObject", "url": abs_url(C.LOGO_FILE)}},
               "image": abs_url("blog/" + p["image"]) if p["image"] and not p["image"].startswith("http") else (p["image"] or abs_url("assets/img/og-image.png")),
               "articleSection": p["category"], "inLanguage": "en-KE"}
        head = (ld(art) + crumbs_schema([("Home", ""), ("Blog", "blog.html"), (p["title"], p["file"])])
                + f'<meta property="article:published_time" content="{p["date"].isoformat()}">'
                + f'<meta property="article:modified_time" content="{p["updated"].isoformat()}">'
                + f'<meta property="article:section" content="{esc(p["category"])}">')
        img = ("blog/" + p["image"]) if p["image"] and not p["image"].startswith("http") else (p["image"] or None)
        page(p["file"], p["title"], p["description"], "blog", body, head, og_type="article", image=img, pre=pre)


def build_legal(slug):
    meta, raw = md.parse_front_matter(open(os.path.join(ROOT, "src", "pages", slug + ".md"), encoding="utf-8").read())
    body_html, toc = md.to_html(fill_vars(raw))
    upd = date.fromisoformat(meta.get("updated", TODAY.isoformat()))
    title = meta.get("title", slug.replace("-", " ").title())
    toc_html = ('<nav class="card toc" aria-label="Contents"><p class="fc-label">Contents</p><ol>'
                + "".join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in toc) + "</ol></nav>")
    body = f'''
<section class="page-hero">
  <div class="container">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>{esc(title)}</span></nav>
    <p class="eyebrow">Legal</p>
    <h1>{esc(title)}</h1>
    <p class="post-meta big">Last updated <time datetime="{upd.isoformat()}">{nice_date(upd)}</time></p>
  </div>
</section>
<section class="section pt-0">
  <div class="container post-layout">
    <div class="post-main"><div class="prose">{body_html}</div></div>
    <aside class="post-side">{toc_html}</aside>
  </div>
</section>'''
    page(slug + ".html", title, fill_vars(meta.get("description", title)), slug, body,
         crumbs_schema([("Home", ""), (title, slug + ".html")]))


def build_404():
    body = f'''
<section class="page-hero">
  <div class="container narrow center">
    <p class="eyebrow">Error 404</p>
    <h1>We couldn't find <span class="accent">that page.</span></h1>
    <p class="lead">The page may have moved. Try one of these instead:</p>
    <div class="btn-row center">
      <a href="/index.html" class="btn btn-primary">Go to home page</a>
      <a href="/services.html" class="btn btn-ghost">Our services</a>
      <a href="/blog.html" class="btn btn-ghost">Read the blog</a>
    </div>
  </div>
</section>'''
    page("404.html", "Page not found", "This page could not be found.", "", body, noindex=True, pre="/")


def build_og_image():
    """Creates the image shown when the site is shared on WhatsApp, Facebook, LinkedIn etc."""
    try:
        from PIL import Image, ImageDraw, ImageFilter, ImageFont
    except ImportError:
        return
    out = os.path.join(OUT, "assets/img/og-image.png")
    W, H = 1200, 630
    im = Image.new("RGB", (W, H), (12, 11, 23))
    glow = Image.new("RGB", (W, H), (0, 0, 0))
    g = ImageDraw.Draw(glow)
    g.ellipse((780, -260, 1380, 340), fill=(112, 56, 224))
    g.ellipse((-200, 380, 360, 900), fill=(34, 199, 244))
    glow = glow.filter(ImageFilter.GaussianBlur(140))
    im = Image.blend(im, glow, 0.55)
    d = ImageDraw.Draw(im)
    for x in range(W):  # brand gradient bar
        t = x / W
        c = tuple(int(a + (b - a) * t) for a, b in zip((112, 56, 224), (34, 199, 244)))
        d.line([(x, 0), (x, 8)], fill=c)
    logo_path = os.path.join(OUT, C.LOGO_FILE_LIGHT or C.LOGO_FILE)
    if os.path.exists(logo_path):
        lg = Image.open(logo_path).convert("RGBA")
        lw = 470
        lg = lg.resize((lw, round(lg.height * lw / lg.width)), Image.LANCZOS)
        im.paste(lg, (80, 90), lg)
    try:
        f1 = ImageFont.truetype("DejaVuSans-Bold.ttf", 52)
        f2 = ImageFont.truetype("DejaVuSans.ttf", 30)
    except OSError:
        return  # no suitable font on this machine: keep the existing og-image.png
    d.text((80, 330), "CCTV · Internet · Hotspots", font=f1, fill=(255, 255, 255))
    d.text((80, 398), "Websites · Software · Zoho", font=f1, fill=(255, 255, 255))
    d.text((80, 500), f"{C.CITY}, {C.COUNTRY}   |   {C.PHONE_DISPLAY}", font=f2, fill=(160, 220, 245))
    im.save(out, optimize=True)


def build_feed():
    items = "".join(
        f"<item><title>{esc(p['title'])}</title><link>{abs_url(p['file'])}</link><guid>{abs_url(p['file'])}</guid>"
        f"<pubDate>{p['date'].strftime('%a, %d %b %Y')} 08:00:00 +0300</pubDate><category>{esc(p['category'])}</category>"
        f"<description>{esc(p['description'])}</description></item>" for p in POSTS[:20])
    rss = (f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>{esc(C.COMPANY)} Blog</title>'
           f'<link>{abs_url("blog.html")}</link><description>{esc(C.TAGLINE)}</description><language>en-ke</language>{items}</channel></rss>')
    with open(os.path.join(OUT, "feed.xml"), "w", encoding="utf-8") as f:
        f.write(rss)


def build_sitemap():
    entries = [("", TODAY, "1.0"), ("services.html", TODAY, "0.9"), ("contact.html", TODAY, "0.8"),
               ("blog.html", POSTS[0]["date"] if POSTS else TODAY, "0.8"), ("portfolio.html", TODAY, "0.8"),
               ("gallery.html", ALBUMS[0]["date"] if ALBUMS else TODAY, "0.7")]
    entries += [(a["file"], min(a["date"], TODAY), "0.5") for a in ALBUMS if not a["sample"]]
    entries += [(pr["file"], pr["date"] if pr["date"] <= TODAY else TODAY, "0.7") for pr in PROJECTS if not pr["sample"]]
    entries += [(f'{s["slug"]}.html', TODAY, "0.9") for s in SERVICES]
    entries += [(p["file"], p["updated"], "0.7") for p in POSTS]
    entries += [("privacy-policy.html", TODAY, "0.3"), ("terms-and-conditions.html", TODAY, "0.3")]
    n_pages = max(1, math.ceil(len(POSTS) / POSTS_PER_PAGE))
    entries += [(f"blog-page-{k}.html", TODAY, "0.5") for k in range(2, n_pages + 1)]
    urls = "".join(f"<url><loc>{abs_url(u)}</loc><lastmod>{d.isoformat()}</lastmod><priority>{pr}</priority></url>"
                   for u, d, pr in entries)
    with open(os.path.join(OUT, "sitemap.xml"), "w") as f:
        f.write(f'<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>')
    with open(os.path.join(OUT, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\nDisallow: /404.html\n\nSitemap: {abs_url('sitemap.xml')}\n")


def copy_blog_images():
    src = os.path.join(ROOT, "blog", "images")
    dst = os.path.join(OUT, "blog", "images")
    if os.path.isdir(src):
        shutil.copytree(src, dst, dirs_exist_ok=True)


# ---------------------------------------------------------------- PORTFOLIO
def project_img(pr, path, pre="", thumb=False):
    if path.startswith("http"):
        return path
    name = path.split("/", 1)[1] if path.startswith("images/") else path
    return f'{pre}portfolio/images/{"thumbs/" if thumb else ""}{name}'


def project_cover(pr, pre="", big=False):
    if pr["cover"]:
        return (f'<div class="post-cover has-img{" big" if big else ""}"><img src="{project_img(pr, pr["cover"], pre, thumb=not big)}" '
                f'alt="{esc(pr["title"])}" loading="{"eager" if big else "lazy"}" width="1200" height="675"></div>')
    s = SERVICE_BY_SLUG.get(pr["services"][0]) if pr["services"] else None
    ic_name = s["icon"] if s else "layers"
    label = s["nav"] if s else "Project"
    return (f'<div class="post-cover{" big" if big else ""}" aria-hidden="true"><span class="pc-ic">{icon(ic_name)}</span>'
            f'<span class="pc-cat">{esc(label)}</span></div>')


def project_card(pr, pre=""):
    svc = " ".join(pr["services"])
    labels = " · ".join(SERVICE_BY_SLUG[x]["nav"] for x in pr["services"][:2]) or "Project"
    where = " · ".join(x for x in (pr["location"], str(pr["date"].year)) if x)
    tags = "".join(f'<span class="mini-tag">{esc(h)}</span>' for h in pr["highlights"][:3])
    return (f'<a href="{pre}{pr["file"]}" class="card post-card project-card" data-svc="{esc(svc)}">'
            f'{project_cover(pr, pre)}{"<span class=sample-badge>Sample project</span>" if pr["sample"] else ""}<div class="post-body"><span class="post-cat">{esc(labels)}</span>'
            f'<h3>{esc(pr["title"])}</h3><p>{esc(pr["summary"])}</p>'
            f'{f"<div class=mini-tags>{tags}</div>" if tags else ""}'
            f'<p class="post-meta">{icon("pin", "ic ic-sm")}<span>{esc(where)}</span></p></div></a>')


def projects_block(projects, title, sub, eyebrow="Our work", show_all=True):
    if not projects:
        return ""
    btn = f'<a href="portfolio.html" class="btn btn-ghost">View all projects {icon("arrow", "ic ic-sm")}</a>' if show_all else ""
    return f'''
<section class="section">
  <div class="container">
    <div class="section-head">
      <div><p class="eyebrow">{eyebrow}</p><h2>{title}</h2><p class="lead-sm">{sub}</p></div>
      {btn}
    </div>
    <div class="grid-3 mt-lg">{"".join(project_card(p) for p in projects)}</div>
  </div>
</section>'''


def build_portfolio_index():
    used = [s for s in SERVICES if any(s["slug"] in p["services"] for p in PROJECTS)]
    chips = ""
    if len(used) > 1:
        chips = ('<div class="chips" role="group" aria-label="Filter by service">'
                 '<button class="chip is-active" data-pf="all">All projects</button>'
                 + "".join(f'<button class="chip" data-pf="{s["slug"]}">{esc(s["nav"])}</button>' for s in used) + '</div>')
    if PROJECTS:
        grid = f'<div class="grid-3 mt-lg project-grid">{"".join(project_card(p) for p in PROJECTS)}</div>'
    else:
        grid = f'''<div class="card empty-state">
      <span class="svc-ic svc-ic-lg">{icon("layers")}</span>
      <h2 class="h3">Case studies are on the way</h2>
      <p>We're documenting recent CCTV, networking, hotspot, web and software projects. In the meantime, we're happy to share references and examples of similar work.</p>
      <div class="btn-row center">
        <a href="contact.html" class="btn btn-primary">Ask for references {icon("arrow", "ic ic-sm")}</a>
        <a href="{wa_link("Hello Omnitech Systems, could you share examples of your previous work?")}" class="btn btn-ghost" target="_blank" rel="noopener">{icon("whatsapp", "ic ic-sm")} WhatsApp us</a>
      </div>
    </div>'''
    body = f'''
<section class="page-hero">
  <div class="container">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>Portfolio</span></nav>
    <p class="eyebrow">Portfolio</p>
    <h1>Projects we're <span class="accent">proud of.</span></h1>
    <p class="lead">A selection of security, connectivity and digital projects we've delivered for businesses, homes and institutions.</p>
  </div>
</section>
<section class="section pt-0">
  <div class="container">
    {chips}
    {grid}
  </div>
</section>'''
    items = ld({"@context": "https://schema.org", "@type": "CollectionPage", "name": f"{C.COMPANY} Portfolio",
                "url": abs_url("portfolio.html"), "about": {"@id": abs_url("#business")},
                "hasPart": [{"@type": "CreativeWork", "name": p["title"], "url": abs_url(p["file"])} for p in PROJECTS]})
    page("portfolio.html", "Portfolio", f"Recent CCTV, networking, hotspot, website, software and Zoho projects by {C.COMPANY} in {C.COUNTRY}.",
         "portfolio", body, items + crumbs_schema([("Home", ""), ("Portfolio", "portfolio.html")]),
         full_title=f"Portfolio: Our Projects in {C.COUNTRY} | {C.COMPANY}")


def build_projects():
    pre = "../"
    for pr in PROJECTS:
        svcs = [SERVICE_BY_SLUG[x] for x in pr["services"]]
        facts = [("Client", pr["client"]), ("Location", pr["location"]), ("Completed", pr["date_label"]),
                 ("Services", ", ".join(s["nav"] for s in svcs))]
        facts_html = "".join(f'<div><dt>{k}</dt><dd>{esc(v)}</dd></div>' for k, v in facts if v)
        hl = "".join(f'<li>{icon("check", "ic ic-sm")} {esc(h)}</li>' for h in pr["highlights"])
        gallery = ""
        if pr["gallery"]:
            gallery = ('<div class="gallery">' + "".join(
                f'<a href="{project_img(pr, g, pre)}" class="gallery-item" data-lightbox>'
                f'<img src="{project_img(pr, g, pre, thumb=True)}" alt="{esc(pr["title"])}, photo {i+1}" loading="lazy" width="800" height="600"></a>'
                for i, g in enumerate(pr["gallery"])) + '</div>')
        svc_links = "".join(f'<a href="{pre}{s["slug"]}.html" class="btn btn-primary btn-block">{esc(s["nav"])} {icon("arrow", "ic ic-sm")}</a>' for s in svcs[:2])
        others = [q for q in PROJECTS if q is not pr and set(q["services"]) & set(pr["services"])]
        others += [q for q in PROJECTS if q is not pr and q not in others]
        more = ""
        if others:
            more = f'''
<section class="section section-tint">
  <div class="container">
    <p class="eyebrow">More work</p><h2>Other projects</h2>
    <div class="grid-3 mt-lg">{"".join(project_card(q, pre) for q in others[:3])}</div>
  </div>
</section>'''
        msg = f"Hello Omnitech Systems, I saw the \"{pr['title']}\" project on your website and I'd like something similar."
        body = f'''
<article>
<header class="page-hero post-hero">
  <div class="container">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="{pre}index.html">Home</a><span>/</span><a href="{pre}portfolio.html">Portfolio</a><span>/</span><span>{esc(pr["title"])}</span></nav>
    <span class="post-cat">{esc(" · ".join(s["nav"] for s in svcs) or "Project")}</span>
    <h1>{esc(pr["title"])}</h1>
    <p class="lead">{esc(pr["summary"])}</p>
    <dl class="facts">{facts_html}</dl>
    {'<p class="sample-note">' + icon("layers", "ic ic-sm") + ' This is a sample project showing how our case studies are presented. The images are illustrations, not photos of a real installation.</p>' if pr["sample"] else ""}
  </div>
</header>
<section class="section pt-0">
  <div class="container">
    <div class="project-cover">{project_cover(pr, pre, big=True)}</div>
    <div class="post-layout mt-lg">
      <div class="post-main">
        <div class="prose">{pr["html"]}</div>
        {gallery}
      </div>
      <aside class="post-side">
        {f'<div class="card toc"><p class="fc-label">Project highlights</p><ul class="check-list">{hl}</ul></div>' if hl else ""}
        <div class="card split-card dark side-cta">
          <p class="eyebrow eyebrow-light">Want something similar?</p>
          <h2 class="h3">Let's plan your project</h2>
          <p>Tell us about your premises or business and we'll recommend the right solution.</p>
          <a href="{wa_link(msg)}" class="btn btn-primary" target="_blank" rel="noopener">{icon("whatsapp", "ic ic-sm")} Chat on WhatsApp</a>
        </div>
        {f'<div class="card toc"><p class="fc-label">Services used</p><div class="svc-links">{svc_links}</div></div>' if svc_links else ""}
      </aside>
    </div>
  </div>
</section>
</article>
{more}'''
        work = {"@context": "https://schema.org", "@type": "CreativeWork", "name": pr["title"], "about": pr["summary"],
                "url": abs_url(pr["file"]), "dateCreated": pr["date"].isoformat(),
                "creator": {"@id": abs_url("#business")}, "keywords": ", ".join(pr["highlights"])}
        if pr["location"]:
            work["locationCreated"] = {"@type": "Place", "name": pr["location"]}
        img = None
        if pr["cover"]:
            img = project_img(pr, pr["cover"])
            work["image"] = abs_url(img) if not img.startswith("http") else img
        page(pr["file"], pr["title"], pr["summary"], "portfolio", body,
             ld(work) + crumbs_schema([("Home", ""), ("Portfolio", "portfolio.html"), (pr["title"], pr["file"])]),
             image=img, pre=pre, noindex=pr["sample"])


# ---------------------------------------------------------------- GALLERY
def gal_src(a, ph, pre="", thumb=False):
    return f'{pre}gallery/photos/{a["slug"]}/{"thumbs/" if thumb else ""}{ph["file"]}'


def gal_grid(a, pre="", limit=None):
    photos = a["photos"][:limit] if limit else a["photos"]
    items = ""
    for i, ph in enumerate(photos):
        alt = ph["caption"] or f'{a["title"]}, photo {i + 1}'
        cap = f' data-caption="{esc(ph["caption"])}"' if ph["caption"] else ""
        items += (f'<a href="{gal_src(a, ph, pre)}" class="gallery-item" data-lightbox="{a["slug"]}"{cap}>'
                  f'<img src="{gal_src(a, ph, pre, thumb=True)}" alt="{esc(alt)}" loading="lazy" width="640" height="480"></a>')
    return items


def album_meta(a):
    bits = [f'{icon("clock", "ic ic-sm")}<span>{esc(a["date_label"])}</span>']
    if a["location"]:
        bits.append(f'{icon("pin", "ic ic-sm")}<span>{esc(a["location"])}</span>')
    bits.append(f'{icon("layers", "ic ic-sm")}<span>{len(a["photos"])} photo{"s" if len(a["photos"]) != 1 else ""}</span>')
    return '<p class="album-meta">' + "".join(f'<span class="am">{b}</span>' for b in bits) + '</p>'


def build_gallery_index():
    cats = []
    for a in ALBUMS:
        if a["category"] not in cats:
            cats.append(a["category"])
    chips = ""
    if len(cats) > 1:
        chips = ('<div class="chips" role="group" aria-label="Filter albums">'
                 '<button class="chip is-active" data-gal="all">All</button>'
                 + "".join(f'<button class="chip" data-gal="{esc(c)}">{esc(c)}</button>' for c in cats) + '</div>')
    if ALBUMS:
        sections = ""
        for a in ALBUMS:
            more = len(a["photos"]) - 8
            more_link = (f'<a href="{a["file"]}" class="link-arrow">View all {len(a["photos"])} photos {icon("arrow", "ic ic-sm")}</a>'
                         if more > 0 else f'<a href="{a["file"]}" class="link-arrow">Open album {icon("arrow", "ic ic-sm")}</a>')
            badge = '<span class="mini-tag">Sample album</span>' if a["sample"] else ""
            sections += f'''
    <section class="album" data-cat="{esc(a["category"])}">
      <div class="album-head">
        <div>
          <span class="post-cat">{esc(a["category"])}</span> {badge}
          <h2 class="h3"><a href="{a["file"]}">{esc(a["title"])}</a></h2>
          {album_meta(a)}
        </div>
        {more_link}
      </div>
      <div class="gallery gallery-wall">{gal_grid(a, limit=8)}</div>
    </section>'''
        content = f'{chips}<div class="albums">{sections}</div>'
    else:
        content = f'''<div class="card empty-state">
      <span class="svc-ic svc-ic-lg">{icon("camera")}</span>
      <h2 class="h3">Photos are on the way</h2>
      <p>We're adding photos from recent installations and site visits. Follow along, or ask us for examples of similar work.</p>
      <div class="btn-row center"><a href="portfolio.html" class="btn btn-primary">See our portfolio {icon("arrow", "ic ic-sm")}</a>
      <a href="contact.html" class="btn btn-ghost">Contact us</a></div>
    </div>'''
    body = f'''
<section class="page-hero">
  <div class="container">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="index.html">Home</a><span>/</span><span>Gallery</span></nav>
    <p class="eyebrow">Gallery</p>
    <h1>Our work, <span class="accent">on the ground.</span></h1>
    <p class="lead">Photos from our installations, projects and site visits across {esc(C.COUNTRY)}.</p>
  </div>
</section>
<section class="section pt-0">
  <div class="container">{content}</div>
</section>'''
    gal_ld = ld({"@context": "https://schema.org", "@type": "ImageGallery", "name": f"{C.COMPANY} Gallery",
                 "url": abs_url("gallery.html"), "about": {"@id": abs_url("#business")},
                 "hasPart": [{"@type": "ImageGallery", "name": a["title"], "url": abs_url(a["file"])} for a in ALBUMS if not a["sample"]]})
    page("gallery.html", "Gallery", f"Photos of CCTV installations, network setups, projects and site visits by {C.COMPANY} in {C.COUNTRY}.",
         "gallery", body, gal_ld + crumbs_schema([("Home", ""), ("Gallery", "gallery.html")]),
         full_title=f"Gallery: Installations & Site Visits | {C.COMPANY}")


def build_albums():
    pre = "../"
    for idx, a in enumerate(ALBUMS):
        nav = ""
        newer = ALBUMS[idx - 1] if idx > 0 else None
        older = ALBUMS[idx + 1] if idx + 1 < len(ALBUMS) else None
        if newer or older:
            nav = '<nav class="album-nav">' + (
                f'<a href="{pre}{newer["file"]}" class="btn btn-ghost">← {esc(newer["title"])}</a>' if newer else '<span></span>') + (
                f'<a href="{pre}{older["file"]}" class="btn btn-ghost">{esc(older["title"])} →</a>' if older else '') + '</nav>'
        sample = ('<p class="sample-note">' + icon("layers", "ic ic-sm") + ' This is a sample album showing how the gallery works. '
                  'The images are illustrations, not real photos.</p>') if a["sample"] else ""
        body = f'''
<section class="page-hero">
  <div class="container">
    <nav class="crumbs" aria-label="Breadcrumb"><a href="{pre}index.html">Home</a><span>/</span><a href="{pre}gallery.html">Gallery</a><span>/</span><span>{esc(a["title"])}</span></nav>
    <span class="post-cat">{esc(a["category"])}</span>
    <h1 class="album-title">{esc(a["title"])}</h1>
    {album_meta(a)}
    {f'<div class="prose album-desc">{a["description"]}</div>' if a["description"] else ""}
    {sample}
  </div>
</section>
<section class="section pt-0">
  <div class="container">
    <div class="gallery gallery-wall">{gal_grid(a, pre)}</div>
    {nav}
  </div>
</section>'''
        imgs = [{"@type": "ImageObject", "contentUrl": abs_url(gal_src(a, ph)), "caption": ph["caption"] or a["title"]}
                for ph in a["photos"]]
        data = {"@context": "https://schema.org", "@type": "ImageGallery", "name": a["title"], "url": abs_url(a["file"]),
                "datePublished": a["date"].isoformat(), "image": imgs, "author": {"@id": abs_url("#business")}}
        if a["location"]:
            data["contentLocation"] = {"@type": "Place", "name": a["location"]}
        cover = next(ph for ph in a["photos"] if ph["file"] == a["cover"])
        page(a["file"], a["title"], a["summary"] or f'{a["category"]} photos by {C.COMPANY}: {a["title"]}.', "gallery", body,
             ld(data) + crumbs_schema([("Home", ""), ("Gallery", "gallery.html"), (a["title"], a["file"])]),
             image=gal_src(a, cover), pre=pre, noindex=a["sample"])


if __name__ == "__main__":
    os.makedirs(os.path.join(OUT, "assets/img"), exist_ok=True)
    # remove old generated blog pages so deleted / unpublished articles disappear
    shutil.rmtree(os.path.join(OUT, "blog"), ignore_errors=True)
    shutil.rmtree(os.path.join(OUT, "portfolio"), ignore_errors=True)
    shutil.rmtree(os.path.join(OUT, "gallery"), ignore_errors=True)
    for old in glob.glob(os.path.join(OUT, "blog-page-*.html")):
        os.remove(old)
    illustrations.ZOHO_LOGOS.update({k: zoho_logo_path(k) for k, *_ in ZOHO_APPS if zoho_logo_path(k)})
    POSTS[:] = load_posts()
    PROJECTS[:] = pf.load_projects(ROOT, TODAY, SERVICE_BY_SLUG)
    ALBUMS[:] = gal.load_albums(ROOT, TODAY)
    build_home()
    build_services_index()
    for s in SERVICES:
        build_service(s)
    build_contact()
    build_blog_index()
    build_posts()
    copy_blog_images()
    build_portfolio_index()
    build_projects()
    pf.copy_images(ROOT, OUT)
    build_gallery_index()
    build_albums()
    gal.copy_images(ROOT, OUT, ALBUMS)
    build_legal("privacy-policy")
    build_legal("terms-and-conditions")
    build_404()
    build_og_image()
    build_feed()
    build_sitemap()
    print(f"Done -> {OUT}  ({len(POSTS)} published articles, {len(PROJECTS)} portfolio projects, {len(ALBUMS)} gallery albums)")
