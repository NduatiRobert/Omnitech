"""
Hero illustrations (inline SVG, brand colours) for the home page and each service page.

To use a real photo instead, put it in site/assets/img/hero/<page>.jpg (or .webp / .png),
e.g. site/assets/img/hero/cctv-installation.jpg or site/assets/img/hero/home.jpg.
The build uses the photo automatically when it exists. Recommended size: 1280 x 960 px.
"""
from icons import P as ICON_PATHS

VIOLET, BLUE, CYAN, INK = "#7038e0", "#4e79e8", "#22c7f4", "#0c0b17"
ZOHO_LOGOS = {}  # filled in by build.py: {"crm": "assets/img/zoho/crm.svg", ...}
W, H = 640, 480


# ------------------------------------------------------------------ primitives
def defs(p):
    return f'''<defs>
<linearGradient id="{p}-brand" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{VIOLET}"/><stop offset=".55" stop-color="{BLUE}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
<linearGradient id="{p}-brandh" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{VIOLET}"/><stop offset="1" stop-color="{CYAN}"/></linearGradient>
<linearGradient id="{p}-bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f3efff"/><stop offset=".55" stop-color="#eef3ff"/><stop offset="1" stop-color="#e3f6fd"/></linearGradient>
<linearGradient id="{p}-wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff" stop-opacity=".9"/><stop offset="1" stop-color="#e8eaf6" stop-opacity=".9"/></linearGradient>
<linearGradient id="{p}-body" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#dfe3f0"/></linearGradient>
<linearGradient id="{p}-dark" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1b1840"/><stop offset="1" stop-color="{INK}"/></linearGradient>
<linearGradient id="{p}-screen" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#211d4d"/><stop offset="1" stop-color="#0e1a33"/></linearGradient>
<radialGradient id="{p}-lens" cx=".35" cy=".35" r=".7"><stop offset="0" stop-color="#5b6bd8"/><stop offset=".45" stop-color="#1b1840"/><stop offset="1" stop-color="#05040c"/></radialGradient>
<radialGradient id="{p}-glowv" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{VIOLET}" stop-opacity=".35"/><stop offset="1" stop-color="{VIOLET}" stop-opacity="0"/></radialGradient>
<radialGradient id="{p}-glowc" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{CYAN}" stop-opacity=".35"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
<filter id="{p}-sh" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#1b1840" flood-opacity=".18"/></filter>
<filter id="{p}-shs" x="-30%" y="-30%" width="160%" height="170%"><feDropShadow dx="0" dy="4" stdDeviation="5" flood-color="#1b1840" flood-opacity=".18"/></filter>
<pattern id="{p}-dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.2" fill="#6d3bdf" opacity=".12"/></pattern>
</defs>'''


def background(p, floor=True):
    s = (f'<rect width="{W}" height="{H}" fill="url(#{p}-bg)"/>'
         f'<rect width="{W}" height="{H}" fill="url(#{p}-dots)"/>'
         f'<circle cx="560" cy="60" r="200" fill="url(#{p}-glowv)"/>'
         f'<circle cx="60" cy="440" r="220" fill="url(#{p}-glowc)"/>')
    if floor:
        s += f'<rect y="390" width="{W}" height="90" fill="#ffffff" opacity=".55"/><rect y="389" width="{W}" height="1.5" fill="#c9cde6"/>'
    return s


def ic(name, x, y, size=24, color="#fff", sw=2):
    return (f'<svg x="{x}" y="{y}" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" stroke="{color}" '
            f'stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{ICON_PATHS[name]}</svg>')


def card(p, x, y, w, h, r=14, fill="#fff", shadow=True):
    f = f' filter="url(#{p}-sh)"' if shadow else ""
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"{f}/>'


def shadow_floor(x, y, w, op=.16):
    return f'<ellipse cx="{x}" cy="{y}" rx="{w/2}" ry="{w/14}" fill="#1b1840" opacity="{op}"/>'


def text(x, y, t, size=12, fill=INK, weight=700, anchor="start", op=1):
    return (f'<text x="{x}" y="{y}" font-family="Plus Jakarta Sans, Segoe UI, Arial, sans-serif" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" opacity="{op}">{t}</text>')


def bar(x, y, w, h=7, fill="#dfe3f0", r=3.5):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}"/>'


def wifi(cx, cy, r, color, sw=6, op=1):
    out = ""
    for i, k in enumerate((1, .68, .36)):
        rr = r * k
        out += (f'<path d="M{cx-rr*.87} {cy-rr*.5} A{rr} {rr} 0 0 1 {cx+rr*.87} {cy-rr*.5}" fill="none" stroke="{color}" '
                f'stroke-width="{sw}" stroke-linecap="round" opacity="{op*(1-i*.15)}"/>')
    return out + f'<circle cx="{cx}" cy="{cy}" r="{sw*.9}" fill="{color}" opacity="{op}"/>'


def phone(p, x, y, w, h, inner="", dark=False):
    scr = f"url(#{p}-screen)" if dark else "#ffffff"
    return (f'<g filter="url(#{p}-sh)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{w*.16}" fill="{INK}"/></g>'
            f'<rect x="{x+5}" y="{y+5}" width="{w-10}" height="{h-10}" rx="{w*.12}" fill="{scr}"/>'
            f'<rect x="{x+w/2-14}" y="{y+9}" width="28" height="6" rx="3" fill="{INK}"/>'
            f'<svg x="{x+5}" y="{y+5}" width="{w-10}" height="{h-10}" viewBox="0 0 {w-10} {h-10}">{inner}</svg>')


def browser(p, x, y, w, h, inner="", url="omnitechsystems.co.ke"):
    return (f'<g filter="url(#{p}-sh)"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#fff"/></g>'
            f'<path d="M{x} {y+12} a12 12 0 0 1 12 -12 h{w-24} a12 12 0 0 1 12 12 v18 h-{w} z" fill="#f1f2f8"/>'
            f'<circle cx="{x+16}" cy="{y+15}" r="4" fill="#ff6b6b"/><circle cx="{x+29}" cy="{y+15}" r="4" fill="#ffc94d"/>'
            f'<circle cx="{x+42}" cy="{y+15}" r="4" fill="#3ddc97"/>'
            f'<rect x="{x+58}" y="{y+8}" width="{min(w-80, 220)}" height="14" rx="7" fill="#fff"/>'
            f'{text(x+68, y+18.5, url, 8, "#8a88a3", 600)}'
            f'<svg x="{x}" y="{y+30}" width="{w}" height="{h-30}" viewBox="0 0 {w} {h-30}">{inner}</svg>')


def chip(p, x, y, label, icon_name, w=None, color=VIOLET):
    w = w or (len(label) * 7.2 + 46)
    return (f'<g filter="url(#{p}-shs)"><rect x="{x}" y="{y}" width="{w}" height="34" rx="17" fill="#fff"/></g>'
            f'<circle cx="{x+17}" cy="{y+17}" r="11" fill="{color}" opacity=".12"/>'
            f'{ic(icon_name, x+10, y+10, 14, color, 2.4)}{text(x+34, y+21.5, label, 11.5, INK, 700)}')


# ------------------------------------------------------------------ devices
def bullet_cam(p, x, y, s=1, flip=False):
    """Bullet CCTV camera on a wall mount; (x, y) = mount point."""
    t = f'translate({x} {y}) scale({-s if flip else s} {s})'
    return f'''<g transform="{t}">
<rect x="-10" y="-18" width="20" height="36" rx="5" fill="url(#{p}-body)" stroke="#cfd4e6"/>
<path d="M0 0 L22 10" stroke="#c4c9de" stroke-width="7" stroke-linecap="round"/>
<g transform="translate(22 10) rotate(14)" filter="url(#{p}-shs)">
<rect x="0" y="-15" width="96" height="30" rx="13" fill="url(#{p}-body)" stroke="#d3d8ea"/>
<path d="M-2 -17 H92 a8 8 0 0 1 8 8 v0 H-2 z" fill="#ffffff" stroke="#d3d8ea"/>
<rect x="84" y="-12" width="14" height="24" rx="5" fill="{INK}"/>
<circle cx="93" cy="0" r="8.5" fill="url(#{p}-lens)"/><circle cx="90" cy="-3" r="2.2" fill="{CYAN}" opacity=".9"/>
<rect x="12" y="-3" width="40" height="5" rx="2.5" fill="url(#{p}-brandh)" opacity=".85"/>
</g></g>'''


def dome_cam(p, x, y, s=1):
    return f'''<g transform="translate({x} {y}) scale({s})" filter="url(#{p}-shs)">
<ellipse cx="0" cy="0" rx="40" ry="10" fill="url(#{p}-body)" stroke="#d3d8ea"/>
<path d="M-32 0 a32 30 0 0 0 64 0 z" fill="#2a2752"/>
<path d="M-32 0 a32 30 0 0 0 64 0 z" fill="url(#{p}-lens)" opacity=".7"/>
<circle cx="0" cy="12" r="9" fill="url(#{p}-lens)" stroke="#3b3770"/><circle cx="-3" cy="9" r="2.4" fill="{CYAN}"/>
<path d="M-24 4 a26 20 0 0 0 14 18" stroke="#fff" stroke-opacity=".35" stroke-width="3" fill="none" stroke-linecap="round"/>
</g>'''


def ptz_cam(p, x, y, s=1):
    return f'''<g transform="translate({x} {y}) scale({s})">
<rect x="-6" y="-70" width="12" height="40" rx="4" fill="#cfd4e6"/>
<path d="M-26 -34 h52 v8 a26 6 0 0 1 -52 0 z" fill="url(#{p}-body)" stroke="#d3d8ea"/>
<g filter="url(#{p}-shs)"><path d="M-36 -26 h72 v22 a36 36 0 0 1 -72 0 z" fill="url(#{p}-body)" stroke="#d3d8ea"/></g>
<path d="M-30 -4 a30 30 0 0 0 60 0 z" fill="url(#{p}-lens)"/>
<circle cx="0" cy="12" r="10" fill="#0d0b20" stroke="#4a46a0" stroke-width="2"/><circle cx="-3" cy="9" r="3" fill="{CYAN}"/>
<rect x="-30" y="-20" width="60" height="4" rx="2" fill="url(#{p}-brandh)"/>
</g>'''


def nvr(p, x, y, w=170):
    leds = "".join(f'<circle cx="{x+18+i*12}" cy="{y+17}" r="2.6" fill="{c}"/>' for i, c in enumerate((CYAN, CYAN, "#3ddc97", VIOLET)))
    vents = "".join(f'<rect x="{x+w-70+i*8}" y="{y+10}" width="4" height="14" rx="2" fill="#2d2a55"/>' for i in range(7))
    return (f'<g filter="url(#{p}-sh)"><rect x="{x}" y="{y}" width="{w}" height="34" rx="6" fill="url(#{p}-dark)"/></g>'
            f'<rect x="{x}" y="{y}" width="{w}" height="3" rx="1.5" fill="url(#{p}-brandh)"/>{leds}{vents}')


def feed(x, y, w, h, kind, label):
    """A stylised camera feed tile."""
    base = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="5" fill="#1c2a4a"/>'
    if kind == "gate":
        sc = (f'<rect x="{x}" y="{y+h*.62}" width="{w}" height="{h*.38}" fill="#24395e"/>'
              + "".join(f'<rect x="{x+w*.15+i*w*.09}" y="{y+h*.22}" width="3" height="{h*.42}" fill="#7a8bb8"/>' for i in range(8))
              + f'<rect x="{x+w*.12}" y="{y+h*.2}" width="{w*.72}" height="3" fill="#7a8bb8"/>')
    elif kind == "shop":
        sc = (f'<rect x="{x+w*.08}" y="{y+h*.18}" width="{w*.84}" height="{h*.16}" fill="#2f4a78"/>'
              f'<rect x="{x+w*.08}" y="{y+h*.42}" width="{w*.84}" height="{h*.16}" fill="#2f4a78"/>'
              f'<rect x="{x+w*.55}" y="{y+h*.66}" width="{w*.3}" height="{h*.22}" fill="#3b5d94"/>'
              f'<circle cx="{x+w*.3}" cy="{y+h*.66}" r="{h*.07}" fill="#9fb3e0"/><rect x="{x+w*.26}" y="{y+h*.72}" width="{w*.08}" height="{h*.2}" rx="3" fill="#9fb3e0"/>')
    elif kind == "parking":
        sc = (f'<rect x="{x}" y="{y+h*.5}" width="{w}" height="{h*.5}" fill="#24395e"/>'
              + "".join(f'<rect x="{x+w*.1+i*w*.28}" y="{y+h*.5}" width="2" height="{h*.5}" fill="#7a8bb8"/>' for i in range(4))
              + f'<rect x="{x+w*.16}" y="{y+h*.6}" width="{w*.2}" height="{h*.16}" rx="4" fill="{CYAN}" opacity=".8"/>'
              f'<rect x="{x+w*.46}" y="{y+h*.62}" width="{w*.2}" height="{h*.16}" rx="4" fill="#a78bfa" opacity=".8"/>')
    else:  # office
        sc = (f'<rect x="{x+w*.1}" y="{y+h*.55}" width="{w*.8}" height="{h*.08}" fill="#3b5d94"/>'
              f'<rect x="{x+w*.2}" y="{y+h*.3}" width="{w*.22}" height="{h*.22}" rx="2" fill="#2f4a78"/>'
              f'<rect x="{x+w*.56}" y="{y+h*.3}" width="{w*.22}" height="{h*.22}" rx="2" fill="#2f4a78"/>'
              f'<circle cx="{x+w*.67}" cy="{y+h*.75}" r="{h*.07}" fill="#9fb3e0"/>')
    return (base + sc + f'<circle cx="{x+9}" cy="{y+9}" r="3" fill="#ff5d5d"/>'
            + text(x+16, y+12, label, 7, "#ffffff", 700, op=.85))


# ------------------------------------------------------------------ scenes
def scene_cctv(p):
    mon_x, mon_y, mw, mh = 228, 92, 300, 192
    feeds = (feed(mon_x+12, mon_y+12, 134, 78, "gate", "CAM 01 · GATE") + feed(mon_x+154, mon_y+12, 134, 78, "shop", "CAM 02 · SHOP")
             + feed(mon_x+12, mon_y+98, 134, 78, "parking", "CAM 03 · PARKING") + feed(mon_x+154, mon_y+98, 134, 78, "office", "CAM 04 · OFFICE"))
    phone_inner = (f'<rect width="70" height="130" fill="url(#{p}-screen)"/>' + feed(6, 26, 58, 40, "gate", "LIVE")
                   + feed(6, 72, 58, 40, "shop", "") + bar(8, 14, 30, 5, "#ffffff40"))
    return f'''{background(p)}
<rect x="22" y="40" width="182" height="340" rx="14" fill="url(#{p}-wall)" stroke="#dfe2f2"/>
{text(40, 68, "SECURITY", 10, VIOLET, 800)}{bar(40, 76, 60, 3, f"url(#{p}-brandh)")}
{bullet_cam(p, 46, 118, .95)}{bullet_cam(p, 46, 196, .95)}
{dome_cam(p, 112, 278, .85)}
<rect x="40" y="318" width="146" height="44" rx="10" fill="#fff" stroke="#e3e6f3"/>
{ic("shield", 52, 328, 22, VIOLET)}{text(82, 337, "Night vision", 10.5, INK, 700)}{text(82, 352, "Motion alerts", 9.5, "#6b6984", 600)}
{shadow_floor(378, 386, 260)}
<rect x="{mon_x+mw/2-10}" y="{mon_y+mh}" width="20" height="54" fill="#cfd4e6"/>
<rect x="{mon_x+mw/2-60}" y="{mon_y+mh+50}" width="120" height="10" rx="5" fill="#cfd4e6"/>
<g filter="url(#{p}-sh)"><rect x="{mon_x-8}" y="{mon_y-8}" width="{mw+16}" height="{mh+16}" rx="14" fill="{INK}"/></g>
<rect x="{mon_x}" y="{mon_y}" width="{mw}" height="{mh}" rx="8" fill="#0b1426"/>{feeds}
<rect x="{mon_x+mw-62}" y="{mon_y-30}" width="62" height="20" rx="10" fill="#ff5d5d"/>{text(mon_x+mw-31, mon_y-16, "● LIVE", 9.5, "#fff", 800, "middle")}
{nvr(p, 266, 348, 190)}
{ptz_cam(p, 580, 140, .9)}
{phone(p, 548, 236, 76, 140, phone_inner, dark=True)}
{chip(p, 238, 34, "Remote viewing", "phone")}'''


def scene_internet(p):
    patch = "".join(f'<rect x="{62+i*13}" y="{150+r*36}" width="9" height="8" rx="1.5" fill="#2d2a55"/>'
                    for r in range(2) for i in range(8))
    cables = ""
    cols = (VIOLET, BLUE, CYAN, "#a78bfa", CYAN, BLUE)
    for i, c in enumerate(cols):
        cables += f'<path d="M{66+i*18} {166} C {66+i*18} 210, {150+i*6} 220, {242} {300+i*4}" stroke="{c}" stroke-width="3" fill="none" opacity=".85"/>'
    lap_inner = (f'<rect width="230" height="140" fill="#fff"/>{text(16, 24, "Network status", 11, INK, 800)}'
                 f'<circle cx="62" cy="80" r="38" fill="none" stroke="#e7e5f0" stroke-width="10"/>'
                 f'<path d="M24 80 A38 38 0 1 1 92 101" fill="none" stroke="url(#{p}-brandh)" stroke-width="10" stroke-linecap="round"/>'
                 f'{text(62, 84, "Online", 10, INK, 800, "middle")}'
                 + "".join(f'<circle cx="122" cy="{50+i*24}" r="4" fill="{c}"/>{bar(132, 46+i*24, w, 7)}' for i, (c, w) in enumerate(((CYAN, 70), (VIOLET, 54), ("#3ddc97", 80), (BLUE, 46)))))
    return f'''{background(p)}
<path d="M0 32 H640" stroke="#dfe2f2" stroke-width="2"/>
<g filter="url(#{p}-sh)"><ellipse cx="420" cy="58" rx="56" ry="13" fill="url(#{p}-body)"/></g>
<rect x="414" y="32" width="12" height="16" fill="#cfd4e6"/><circle cx="420" cy="58" r="4" fill="{CYAN}"/>
{wifi(420, 150, 80, f"url(#{p}-brandh)", 7, .9)}
<g filter="url(#{p}-sh)"><rect x="44" y="110" width="140" height="270" rx="10" fill="url(#{p}-dark)"/></g>
<rect x="54" y="122" width="120" height="76" rx="4" fill="#211d4d"/>{patch}
{text(60, 140, "PATCH PANEL", 7, "#a9a6d6", 800)}
<rect x="54" y="210" width="120" height="30" rx="4" fill="#211d4d"/>
{"".join(f'<rect x="{62+i*14}" y="219" width="10" height="12" rx="2" fill="#3a3672"/><circle cx="{67+i*14}" cy="225" r="1.6" fill="{CYAN}"/>' for i in range(8))}
<rect x="54" y="250" width="120" height="30" rx="4" fill="#211d4d"/>{text(62, 269, "CORE SWITCH", 7, "#a9a6d6", 800)}
{"".join(f'<circle cx="{140+i*9}" cy="265" r="2.4" fill="{c}"/>' for i, c in enumerate((CYAN, "#3ddc97", VIOLET)))}
{cables}
{shadow_floor(388, 386, 300)}
<g filter="url(#{p}-sh)"><path d="M236 360 h236 l24 22 h-284 z" fill="#d4d8ea"/></g>
<rect x="242" y="214" width="224" height="148" rx="10" fill="{INK}"/>
<svg x="250" y="222" width="208" height="128" viewBox="0 0 230 140">{lap_inner}</svg>
<g filter="url(#{p}-sh)"><rect x="482" y="340" width="140" height="40" rx="10" fill="url(#{p}-dark)"/></g>
<rect x="498" y="300" width="5" height="42" rx="2.5" fill="{INK}"/><rect x="600" y="300" width="5" height="42" rx="2.5" fill="{INK}"/>
{"".join(f'<circle cx="{502+i*12}" cy="360" r="2.6" fill="{c}"/>' for i, c in enumerate((CYAN, CYAN, "#3ddc97", VIOLET, CYAN)))}
<rect x="482" y="340" width="140" height="3" rx="1.5" fill="url(#{p}-brandh)"/>
{text(552, 334, "Wi-Fi router", 9, "#6b6984", 700, "middle")}
{chip(p, 456, 78, "Full coverage", "wifi")}
{chip(p, 30, 60, "Cat6 cabling", "cable", color=BLUE)}'''


def scene_hotspot(p):
    pkgs = (("1 Hour", "Buy ›"), ("1 Day", "Buy ›"), ("1 Week", "Buy ›"))
    rows = "".join(
        f'<rect x="12" y="{118+i*44}" width="146" height="36" rx="9" fill="{"#f3efff" if i == 1 else "#f6f7fb"}" stroke="{VIOLET if i == 1 else "#e7e5f0"}"/>'
        f'{text(24, 140+i*44, a, 11, INK, 800)}{text(146, 140+i*44, b, 10, VIOLET, 800, "end")}' for i, (a, b) in enumerate(pkgs))
    phone_inner = (f'<rect width="170" height="330" fill="#fff"/>'
                   f'<rect width="170" height="96" fill="url(#{p}-brand)"/>'
                   f'{wifi(85, 58, 26, "#fff", 4)}{text(85, 84, "Omnitech Wi-Fi", 12, "#fff", 800, "middle")}'
                   f'{text(14, 112, "Choose a package", 9.5, "#6b6984", 700)}{rows}'
                   f'<rect x="12" y="254" width="146" height="38" rx="10" fill="#22a95b"/>'
                   f'{text(85, 277, "Pay with M-Pesa", 11.5, "#fff", 800, "middle")}'
                   f'{text(85, 312, "Connected instantly after payment", 7.5, "#8a88a3", 600, "middle")}')
    chart = "".join(f'<rect x="{458+i*18}" y="{352-h}" width="11" height="{h}" rx="3" fill="url(#{p}-brand)" opacity="{.55+i*.06}"/>'
                    for i, h in enumerate((24, 36, 30, 48, 42, 60, 54)))
    return f'''{background(p)}
<rect x="64" y="96" width="10" height="290" rx="5" fill="#c9cde6"/>
<g filter="url(#{p}-sh)"><rect x="40" y="70" width="58" height="96" rx="14" fill="url(#{p}-body)" stroke="#d3d8ea"/></g>
<rect x="52" y="86" width="34" height="5" rx="2.5" fill="url(#{p}-brandh)"/>
{"".join(f'<circle cx="69" cy="{108+i*14}" r="2.6" fill="{CYAN}"/>' for i in range(3))}
{wifi(69, 62, 58, f"url(#{p}-brandh)", 7, .6)}
{shadow_floor(268, 388, 190)}
{phone(p, 178, 50, 180, 340, phone_inner)}
<g filter="url(#{p}-sh)"><rect x="410" y="244" width="190" height="126" rx="16" fill="#fff"/></g>
{text(430, 272, "Today's sales", 11, INK, 800)}{text(430, 290, "Active users online", 9, "#6b6984", 600)}{chart}
<rect x="440" y="352" width="140" height="1.5" fill="#e7e5f0"/>
{chip(p, 404, 92, "M-Pesa auto-payments", "wallet", color="#22a95b")}
{chip(p, 430, 150, "Vouchers & packages", "ticket")}
{chip(p, 404, 196, "Speed limits", "sliders", color=BLUE)}'''


def scene_web(p):
    cards = "".join(f'<rect x="{24+i*118}" y="168" width="104" height="70" rx="8" fill="#f6f7fb" stroke="#ebeaf3"/>'
                    f'<rect x="{34+i*118}" y="178" width="22" height="22" rx="6" fill="{c}" opacity=".18"/>'
                    f'{bar(34+i*118, 210, 70, 6)}{bar(34+i*118, 222, 50, 6)}' for i, c in enumerate((VIOLET, BLUE, CYAN)))
    site = (f'<rect width="380" height="270" fill="#fff"/>'
            f'<rect x="20" y="14" width="24" height="16" rx="5" fill="url(#{p}-brand)"/>{bar(52, 19, 46, 7, "#2a2752")}'
            + "".join(bar(200 + i*36, 19, 26, 6) for i in range(3))
            + f'<rect x="306" y="12" width="56" height="20" rx="7" fill="url(#{p}-brandh)"/>'
            f'<rect x="0" y="44" width="380" height="110" fill="url(#{p}-bg)"/>'
            f'{bar(24, 66, 170, 13, INK, 6)}{bar(24, 86, 130, 13, f"url(#{p}-brandh)", 6)}{bar(24, 110, 150, 6)}{bar(24, 121, 120, 6)}'
            f'<rect x="24" y="134" width="64" height="14" rx="7" fill="{VIOLET}"/>'
            f'<rect x="232" y="56" width="128" height="86" rx="10" fill="url(#{p}-dark)"/>'
            f'<circle cx="296" cy="99" r="26" fill="url(#{p}-brand)" opacity=".85"/>{ic("globe", 284, 87, 24, "#fff")}'
            + cards)
    mob = (f'<rect width="96" height="190" fill="#fff"/><rect width="96" height="80" fill="url(#{p}-bg)"/>'
           f'<rect x="10" y="12" width="16" height="11" rx="3" fill="url(#{p}-brand)"/>'
           f'{bar(10, 34, 70, 8, INK, 4)}{bar(10, 47, 56, 8, f"url(#{p}-brandh)", 4)}<rect x="10" y="62" width="40" height="10" rx="5" fill="{VIOLET}"/>'
           + "".join(f'<rect x="10" y="{90+i*32}" width="76" height="26" rx="6" fill="#f6f7fb" stroke="#ebeaf3"/>{bar(18, 99+i*32, 44, 5)}' for i in range(3)))
    return f'''{background(p)}
{shadow_floor(300, 392, 360)}
{browser(p, 40, 70, 380, 300, site)}
{phone(p, 446, 160, 106, 210, mob)}
<path d="M392 300 l0 26 l7 -7 l8 14 l5 -3 l-8 -13 l10 -1 z" fill="{INK}" stroke="#fff" stroke-width="1.5"/>
{chip(p, 452, 74, "Mobile-friendly", "phone")}
{chip(p, 486, 112, "SEO ready", "search", color=BLUE)}
{chip(p, 30, 26, "M-Pesa checkout", "cart", color="#22a95b")}'''


def scene_software(p):
    side = "".join(f'<rect x="12" y="{56+i*26}" width="68" height="16" rx="5" fill="{"#ffffff22" if i == 0 else "none"}"/>'
                   f'<circle cx="22" cy="{64+i*26}" r="3.5" fill="{CYAN if i == 0 else "#ffffff55"}"/>{bar(31, 61+i*26, 40, 5, "#ffffff55", 2.5)}' for i in range(6))
    kpis = "".join(f'<rect x="{104+i*92}" y="44" width="82" height="58" rx="9" fill="#fff" stroke="#ebeaf3"/>'
                   f'{bar(114+i*92, 56, 40, 5)}{bar(114+i*92, 70, 54, 11, c, 4)}{bar(114+i*92, 88, 30, 5)}'
                   for i, c in enumerate((INK, VIOLET, BLUE, CYAN)))
    bars = "".join(f'<rect x="{120+i*24}" y="{226-h}" width="13" height="{h}" rx="3" fill="url(#{p}-brand)" opacity="{.6+i*.04}"/>'
                   for i, h in enumerate((40, 62, 50, 78, 66, 92, 84, 104)))
    table = "".join(f'<rect x="318" y="{126+i*24}" width="138" height="18" rx="5" fill="#f6f7fb"/>{bar(326, 132+i*24, 50, 6, "#cfd2e6")}'
                    f'<rect x="420" y="{130+i*24}" width="28" height="10" rx="5" fill="{c}" opacity=".25"/>' for i, c in enumerate((CYAN, "#3ddc97", VIOLET, "#3ddc97")))
    app = (f'<rect width="470" height="250" fill="#f6f7fb"/><rect width="92" height="250" fill="url(#{p}-dark)"/>'
           f'<rect x="12" y="14" width="20" height="20" rx="6" fill="url(#{p}-brand)"/>{bar(38, 21, 40, 7, "#ffffffcc")}{side}'
           f'{text(104, 30, "Business dashboard", 12, INK, 800)}{kpis}'
           f'<rect x="104" y="112" width="204" height="128" rx="9" fill="#fff" stroke="#ebeaf3"/>{text(116, 132, "Monthly sales", 9.5, INK, 800)}{bars}'
           f'<rect x="312" y="112" width="150" height="128" rx="9" fill="#fff" stroke="#ebeaf3"/>{table}')
    mob = (f'<rect width="84" height="160" fill="#fff"/><rect width="84" height="34" fill="url(#{p}-brand)"/>{bar(10, 14, 40, 6, "#fff")}'
           + "".join(f'<rect x="8" y="{44+i*28}" width="68" height="22" rx="6" fill="#f6f7fb"/><circle cx="18" cy="{55+i*28}" r="5" fill="{c}" opacity=".5"/>{bar(28, 52+i*28, 38, 5)}'
                     for i, c in enumerate((VIOLET, CYAN, BLUE, "#3ddc97"))))
    return f'''{background(p)}
{shadow_floor(300, 392, 400)}
<g filter="url(#{p}-sh)"><rect x="34" y="60" width="486" height="300" rx="14" fill="{INK}"/></g>
<rect x="42" y="68" width="470" height="250" rx="6" fill="#fff"/>
<svg x="42" y="68" width="470" height="250" viewBox="0 0 470 250">{app}</svg>
<rect x="42" y="326" width="470" height="26" rx="6" fill="#1b1840"/><circle cx="277" cy="339" r="4" fill="#3a3672"/>
{phone(p, 520, 196, 94, 180, mob)}
{chip(p, 456, 98, "M-Pesa & KRA eTIMS", "plug", w=170)}
{chip(p, 40, 18, "Custom-built for you", "code", color=BLUE)}'''


def scene_marketing(p):
    post = (f'<rect width="200" height="270" fill="#fff"/>'
            f'<circle cx="22" cy="22" r="11" fill="url(#{p}-brand)"/>{bar(40, 15, 70, 6, INK)}{bar(40, 25, 46, 5)}'
            f'<rect x="0" y="42" width="200" height="150" fill="url(#{p}-dark)"/>'
            f'<circle cx="150" cy="80" r="70" fill="url(#{p}-glowv)"/><circle cx="40" cy="170" r="60" fill="url(#{p}-glowc)"/>'
            f'{text(18, 108, "Grow your", 18, "#fff", 800)}{text(18, 132, "business", 18, CYAN, 800)}'
            f'<rect x="18" y="148" width="74" height="22" rx="11" fill="url(#{p}-brandh)"/>{text(55, 163, "Learn more", 9, "#fff", 800, "middle")}'
            f'{ic("bell", 14, 202, 18, "#ff5d8a")}{ic("message", 42, 202, 18, INK)}{ic("share", 70, 202, 18, INK)}'
            f'{bar(14, 232, 120, 6)}{bar(14, 244, 90, 6)}')
    line = "M0 92 C 30 86, 50 70, 80 74 S 130 48, 160 40 S 210 14, 236 8"
    chart = (f'<rect width="250" height="150" fill="#fff"/>{text(16, 24, "Campaign results", 11, INK, 800)}'
             f'{text(16, 40, "Enquiries this month", 8.5, "#6b6984", 600)}'
             f'<svg x="8" y="48" width="236" height="96" viewBox="0 0 236 96">'
             f'<path d="{line} V96 H0 Z" fill="url(#{p}-brand)" opacity=".14"/>'
             f'<path d="{line}" fill="none" stroke="url(#{p}-brandh)" stroke-width="4" stroke-linecap="round"/>'
             f'<circle cx="236" cy="8" r="5" fill="{CYAN}" stroke="#fff" stroke-width="2"/></svg>')
    return f'''{background(p)}
{shadow_floor(330, 392, 420)}
<g filter="url(#{p}-sh)"><rect x="60" y="70" width="200" height="270" rx="16" fill="#fff"/></g>
<svg x="60" y="70" width="200" height="270" viewBox="0 0 200 270"><clipPath id="{p}-pc"><rect width="200" height="270" rx="16"/></clipPath><g clip-path="url(#{p}-pc)">{post}</g></svg>
<g filter="url(#{p}-sh)"><rect x="300" y="150" width="250" height="150" rx="16" fill="#fff"/></g>
<svg x="300" y="150" width="250" height="150" viewBox="0 0 250 150"><clipPath id="{p}-cc"><rect width="250" height="150" rx="16"/></clipPath><g clip-path="url(#{p}-cc)">{chart}</g></svg>
<g transform="translate(470 66) rotate(-12)" filter="url(#{p}-sh)">
<path d="M0 26 L58 6 V70 L0 50 Z" fill="url(#{p}-brand)"/><rect x="-16" y="24" width="20" height="28" rx="6" fill="url(#{p}-dark)"/>
<path d="M4 50 L12 76 h12 l-6 -22" fill="#1b1840"/><path d="M70 22 l14 -8 M72 38 h16 M70 54 l14 8" stroke="{CYAN}" stroke-width="4" stroke-linecap="round"/></g>
<g filter="url(#{p}-shs)"><rect x="300" y="318" width="120" height="44" rx="12" fill="#fff"/></g>
{ic("target", 312, 328, 24, VIOLET)}{text(344, 337, "Google Ads", 10, INK, 800)}{text(344, 351, "Targeted reach", 8.5, "#6b6984", 600)}
<g filter="url(#{p}-shs)"><rect x="432" y="318" width="130" height="44" rx="12" fill="#fff"/></g>
{ic("search", 444, 328, 24, BLUE)}{text(476, 337, "SEO", 10, INK, 800)}{text(476, 351, "Rank on Google", 8.5, "#6b6984", 600)}
{chip(p, 300, 96, "Social media", "share")}'''


def scene_automation(p):
    def node(x, y, w, title, sub, icon_name, color, dark=False):
        bg = f"url(#{p}-dark)" if dark else "#fff"
        tc, sc = ("#fff", "#b9b6dc") if dark else (INK, "#6b6984")
        return (f'<g filter="url(#{p}-sh)"><rect x="{x}" y="{y}" width="{w}" height="58" rx="14" fill="{bg}"/></g>'
                f'<rect x="{x+12}" y="{y+13}" width="32" height="32" rx="9" fill="{color}" opacity="{.25 if dark else .14}"/>'
                f'{ic(icon_name, x+19, y+20, 18, color if not dark else CYAN)}'
                f'{text(x+54, y+27, title, 11.5, tc, 800)}{text(x+54, y+43, sub, 9, sc, 600)}')
    flow = f'url(#{p}-brandh)'
    paths = (f'<path d="M206 130 C 250 130, 240 222, 282 222" stroke="{flow}" stroke-width="3.5" fill="none" stroke-dasharray="2 7" stroke-linecap="round"/>'
             f'<path d="M462 222 C 500 222, 480 120, 520 108" stroke="{flow}" stroke-width="3.5" fill="none" stroke-dasharray="2 7" stroke-linecap="round"/>'
             f'<path d="M462 222 C 500 222, 490 222, 520 222" stroke="{flow}" stroke-width="3.5" fill="none" stroke-dasharray="2 7" stroke-linecap="round"/>'
             f'<path d="M462 222 C 500 222, 480 330, 520 338" stroke="{flow}" stroke-width="3.5" fill="none" stroke-dasharray="2 7" stroke-linecap="round"/>')
    return f'''{background(p, floor=False)}
<circle cx="372" cy="222" r="120" fill="url(#{p}-glowv)"/>
{paths}
{node(30, 100, 176, "New order", "Trigger", "cart", VIOLET)}
<g filter="url(#{p}-sh)"><rect x="282" y="176" width="180" height="92" rx="18" fill="url(#{p}-dark)"/></g>
<circle cx="318" cy="222" r="22" fill="url(#{p}-brand)"/>{ic("zap", 306, 210, 24, "#fff")}
{text(350, 216, "Automation", 13, "#fff", 800)}{text(350, 234, "Runs 24/7", 9.5, "#b9b6dc", 600)}
<rect x="282" y="176" width="180" height="4" rx="2" fill="url(#{p}-brandh)"/>
{node(452, 78, 176, "Send invoice", "Email · PDF", "file", BLUE)}
{node(452, 193, 176, "Notify client", "WhatsApp · SMS", "message", "#22a95b")}
{node(452, 308, 176, "Update CRM", "Sync records", "users", VIOLET)}
{node(30, 300, 200, "Daily report", "Sent at 8:00am", "chart", CYAN)}
<path d="M130 300 C 130 270, 200 250, 282 236" stroke="{flow}" stroke-width="3" fill="none" stroke-dasharray="2 7" stroke-linecap="round" opacity=".6"/>
<g transform="translate(120 230)" opacity=".9">{ic("refresh", -18, -18, 36, VIOLET, 2)}</g>
{chip(p, 30, 30, "Less manual work", "workflow")}'''


def scene_zoho(p):
    apps = (("CRM", "users", VIOLET, "crm"), ("Books", "book", BLUE, "books"), ("Inventory", "box", CYAN, "inventory"),
            ("Mail", "mail", "#e2557a", "mail"), ("Creator", "code", "#f2a33a", "creator"), ("People", "users", "#22a95b", "people"))
    cx, cy = 330, 226
    pos = [(cx + 190 * __import__("math").cos(a), cy + 140 * __import__("math").sin(a))
           for a in [(-90 + i * 60) * 3.14159 / 180 for i in range(6)]]
    lines = "".join(f'<line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="url(#{p}-brandh)" stroke-width="3" stroke-dasharray="2 7" stroke-linecap="round"/>' for x, y in pos)
    tiles = ""
    for (name, icn, col, key), (x, y) in zip(apps, pos):
        tiles += f'<g filter="url(#{p}-sh)"><rect x="{x-62:.1f}" y="{y-34:.1f}" width="134" height="68" rx="16" fill="#fff"/></g>'
        if key in ZOHO_LOGOS:
            tiles += f'<image href="{ZOHO_LOGOS[key]}" x="{x-50:.1f}" y="{y-20:.1f}" width="40" height="40" preserveAspectRatio="xMidYMid meet"/>'
        else:
            tiles += (f'<rect x="{x-50:.1f}" y="{y-20:.1f}" width="40" height="40" rx="11" fill="{col}"/>'
                      f'{ic(icn, x-41, y-11, 22, "#fff")}')
        tiles += text(x-2, y+5, name, 12, INK, 800)
    return f'''{background(p)}
<circle cx="{cx}" cy="{cy}" r="150" fill="url(#{p}-glowc)"/>
{lines}{tiles}
<g filter="url(#{p}-sh)"><circle cx="{cx}" cy="{cy}" r="62" fill="url(#{p}-dark)"/></g>
<circle cx="{cx}" cy="{cy}" r="62" fill="none" stroke="url(#{p}-brandh)" stroke-width="4"/>
{ic("grid", cx-16, cy-30, 32, CYAN)}{text(cx, cy+16, "One suite", 12, "#fff", 800, "middle")}{text(cx, cy+31, "fully connected", 9, "#b9b6dc", 600, "middle")}'''


def scene_home(p):
    # storefront building with CCTV + Wi-Fi, laptop with website and phone with dashboard
    win = "".join(f'<rect x="{150+c*58}" y="{96+r*52}" width="40" height="34" rx="4" fill="#cfe0ff" opacity=".9"/>'
                  f'<rect x="{150+c*58}" y="{96+r*52}" width="40" height="10" fill="#ffffff" opacity=".6"/>' for r in range(2) for c in range(4))
    site = (f'<rect width="210" height="124" fill="#fff"/><rect width="210" height="58" fill="url(#{p}-bg)"/>'
            f'<rect x="10" y="8" width="14" height="10" rx="3" fill="url(#{p}-brand)"/>{bar(14, 26, 100, 8, INK, 4)}{bar(14, 38, 70, 8, f"url(#{p}-brandh)", 4)}'
            + "".join(f'<rect x="{10+i*66}" y="70" width="58" height="44" rx="6" fill="#f6f7fb" stroke="#ebeaf3"/><rect x="{17+i*66}" y="77" width="14" height="14" rx="4" fill="{c}" opacity=".25"/>'
                      for i, c in enumerate((VIOLET, BLUE, CYAN))))
    mob = (f'<rect width="74" height="136" fill="#fff"/><rect width="74" height="30" fill="url(#{p}-brand)"/>{bar(8, 12, 34, 6, "#fff")}'
           + "".join(f'<rect x="{9+i*14}" y="{98-h}" width="9" height="{h}" rx="2" fill="url(#{p}-brand)"/>' for i, h in enumerate((22, 34, 28, 44)))
           + f'{bar(8, 108, 58, 6)}{bar(8, 118, 40, 6)}')
    return f'''{background(p)}
{shadow_floor(330, 390, 470)}
<g filter="url(#{p}-sh)"><rect x="128" y="70" width="270" height="318" rx="8" fill="#fff"/></g>
<rect x="128" y="70" width="270" height="12" rx="6" fill="url(#{p}-brandh)"/>
{win}
<rect x="150" y="210" width="226" height="30" rx="6" fill="url(#{p}-dark)"/>{text(263, 230, "OMNITECH CLIENT", 10, "#fff", 800, "middle")}
<rect x="168" y="256" width="78" height="132" rx="4" fill="#d9e6ff"/><rect x="206" y="256" width="2" height="132" fill="#fff"/>
<rect x="268" y="256" width="94" height="70" rx="4" fill="#d9e6ff"/>
{bullet_cam(p, 128, 120, .62, flip=True)}
{wifi(263, 58, 42, f"url(#{p}-brandh)", 5, .95)}
<g filter="url(#{p}-sh)"><path d="M388 372 h236 l18 16 h-272 z" fill="#d4d8ea"/></g>
<rect x="396" y="246" width="224" height="128" rx="9" fill="{INK}"/>
<svg x="403" y="253" width="210" height="114" viewBox="0 0 210 124" preserveAspectRatio="none">{site}</svg>
{phone(p, 46, 236, 84, 146, mob)}
{chip(p, 420, 70, "CCTV & security", "camera")}
{chip(p, 452, 112, "Internet & Wi-Fi", "wifi", color=BLUE)}
{chip(p, 420, 154, "Websites & software", "code", color=CYAN)}
{chip(p, 452, 196, "Automation & Zoho", "zap")}'''


SCENES = {
    "home": scene_home,
    "cctv-installation": scene_cctv,
    "internet-installation": scene_internet,
    "hotspot-business": scene_hotspot,
    "website-development": scene_web,
    "software-development": scene_software,
    "digital-marketing": scene_marketing,
    "business-automation": scene_automation,
    "zoho-consulting": scene_zoho,
}


def illustration(key, label):
    p = "il" + "".join(ch for ch in key if ch.isalnum())[:10]
    body = SCENES[key](p)
    return (f'<svg class="hero-illus" viewBox="0 0 {W} {H}" role="img" aria-label="{label}" '
            f'xmlns="http://www.w3.org/2000/svg" preserveAspectRatio="xMidYMid slice">{defs(p)}{body}</svg>')
