"""Builds one static artist site per entry in artists.json.
Usage: python3 build.py  -> writes ../<slug>/index.html"""
import json, html, os
HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(HERE, "artists.json")))
tpl = open(os.path.join(HERE, "template.html")).read()
UI = json.load(open(os.path.join(HERE, "ui.json")))
AFF = json.load(open(os.path.join(HERE, "affiliate.json")))
HERO_YT_JS = open(os.path.join(HERE, "hero-youtube.js")).read()
e = html.escape
PLAY = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 4v16l13-8z"/></svg>'
CART = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M3 4h2l2.4 11.2a2 2 0 0 0 2 1.6h7.7a2 2 0 0 0 2-1.5L21 8H6"/><circle cx="10" cy="20" r="1.3"/><circle cx="17" cy="20" r="1.3"/></svg>'

from urllib.parse import quote_plus, quote

THEMES = {
 "poster": {"preload": "anton-latin-400-normal.woff2", "css": ""},
 "slab": {"preload": "alfa-slab-one-latin-400-normal.woff2", "css": """
@font-face{font-family:"Alfa Slab One";font-style:normal;font-weight:400;font-display:swap;src:url("../assets/fonts/alfa-slab-one-latin-400-normal.woff2") format("woff2")}
:root{--display:"Alfa Slab One",Rockwell,"Courier New",serif;--bg:#0a0d0a;--panel:#111611;--ink:#f3f0e4}
.hero h1{font-size:clamp(60px,10.5vw,164px);line-height:.92;letter-spacing:-.01em}
.hero h1 span{color:var(--acc);-webkit-text-stroke:0}
.h2{font-size:clamp(38px,5vw,70px);line-height:1}
.btn,.rel .shops a,.lang button{border-radius:6px}
.eyebrow{letter-spacing:.2em}
.marquee{background:var(--acc)}.marquee div{color:#0a0d0a}
"""},
 "serif": {"preload": "playfair-display-latin-700-normal.woff2", "css": """
@font-face{font-family:"Playfair Display";font-style:normal;font-weight:700;font-display:swap;src:url("../assets/fonts/playfair-display-latin-700-normal.woff2") format("woff2")}
@font-face{font-family:"Playfair Display";font-style:italic;font-weight:700;font-display:swap;src:url("../assets/fonts/playfair-display-latin-700-italic.woff2") format("woff2")}
:root{--display:"Playfair Display",Georgia,"Times New Roman",serif;--bg:#110d0a;--panel:#1a1410;--ink:#f7efe2;--mute:#b3a38c}
.hero h1,.h2,.logo,.marquee div,.consent h3,.merch h3,.extra .h3,.rel h3{text-transform:none;font-weight:700;letter-spacing:-.01em}
.hero h1{font-size:clamp(70px,11.5vw,176px);line-height:.9}
.hero h1 span{color:var(--acc);-webkit-text-stroke:0;font-style:italic}
.h2{font-size:clamp(42px,5.6vw,80px);line-height:1}
.marquee div{font-style:italic;color:#7d6a52}
.btn{border-radius:4px;letter-spacing:.02em}
.eyebrow{font-weight:500;letter-spacing:.32em}
"""},
 "mono": {"preload": "archivo-black-latin-400-normal.woff2", "css": """
@font-face{font-family:"Archivo Black";font-style:normal;font-weight:400;font-display:swap;src:url("../assets/fonts/archivo-black-latin-400-normal.woff2") format("woff2")}
:root{--display:"Archivo Black","Arial Black",sans-serif;--bg:#0b0b0b;--panel:#151515;--ink:#f5f5f2;--mute:#a8a8a2}
.hero .slides,.hero .vid{filter:grayscale(1) contrast(1.08)}
.hero h1,.h2{letter-spacing:-.035em}
.h2{font-size:clamp(36px,4.8vw,68px);line-height:.98}
.btn,.rel .shops a,.lang button{border-radius:0}
.marquee{background:#f5f5f2}.marquee div{color:#0b0b0b}
"""},
 "royal": {"preload": "cinzel-latin-900-normal.woff2", "css": """
@font-face{font-family:"Cinzel";font-style:normal;font-weight:700;font-display:swap;src:url("../assets/fonts/cinzel-latin-700-normal.woff2") format("woff2")}
@font-face{font-family:"Cinzel";font-style:normal;font-weight:900;font-display:swap;src:url("../assets/fonts/cinzel-latin-900-normal.woff2") format("woff2")}
:root{--display:"Cinzel",Georgia,serif;--bg:#100c14;--panel:#19131f;--ink:#f4ecdc;--mute:#b4a690}
.hero h1,.h2,.logo{font-weight:900;letter-spacing:.02em}
.hero h1 span{color:var(--acc);-webkit-text-stroke:0}
.h2{font-size:clamp(34px,4.4vw,64px);line-height:1.05}
.btn,.rel .shops a,.lang button{border-radius:2px}
.marquee div{color:var(--acc)}
"""},
 "loud": {"preload": "bungee-latin-400-normal.woff2", "css": """
@font-face{font-family:"Bungee";font-style:normal;font-weight:400;font-display:swap;src:url("../assets/fonts/bungee-latin-400-normal.woff2") format("woff2")}
:root{--display:"Bungee",Impact,sans-serif;--bg:#0b0b0e;--panel:#141419;--ink:#f4f4ef;--mute:#a9a9b3}
.hero h1 span{color:var(--acc);-webkit-text-stroke:0}
.h2{font-size:clamp(32px,4.4vw,62px);line-height:1.02}
.btn{border-radius:99px}
.marquee{background:var(--acc)}.marquee div{color:#0b0b0e}
"""},
 "tall": {"preload": "bebas-neue-latin-400-normal.woff2", "css": """
@font-face{font-family:"Bebas Neue";font-style:normal;font-weight:400;font-display:swap;src:url("../assets/fonts/bebas-neue-latin-400-normal.woff2") format("woff2")}
:root{--display:"Bebas Neue",Impact,sans-serif;--bg:#0c0f0b;--panel:#141a13;--ink:#f3efe0;--mute:#aab0a0}
.hero h1{letter-spacing:.01em}
.hero h1 span{color:var(--acc);-webkit-text-stroke:0}
.h2{font-size:clamp(48px,6.4vw,96px);line-height:.92;letter-spacing:.01em}
.marquee{background:linear-gradient(90deg,#3fae5a,#f2c230,#d2402f)}.marquee div{color:#0c0f0b}
"""},
}

# Hero layouts: position and line breaks of the artist name (independent of the font theme)
LAYOUTS = {
 "stack": "",
 "center": """
.hero{align-items:center;text-align:center}
.hero .wrap{padding:120px 0 90px;display:flex;flex-direction:column;align-items:center}
.hero h1{font-size:clamp(58px,9.5vw,150px);line-height:.95}
.hero h1 span{display:inline}
.hero p.lead{margin:0 auto}
.hero .cta{justify-content:center}
.hero:after{background:radial-gradient(ellipse at center,rgba(8,8,8,.5) 0%,rgba(8,8,8,.86) 75%),linear-gradient(0deg,var(--bg) 0%,transparent 35%)}
""",
 "right": """
.hero .wrap{display:flex;flex-direction:column;align-items:flex-end;text-align:right}
.hero p.lead{margin-left:auto}
.hero .cta{justify-content:flex-end}
.hero:after{background:linear-gradient(270deg,rgba(12,11,10,.92) 0%,rgba(12,11,10,.55) 45%,rgba(12,11,10,.1) 100%),linear-gradient(0deg,var(--bg) 0%,transparent 40%)}
.hero .watch{right:auto;left:28px}.scroll{right:auto;left:28px}
""",
 "split": """
.hero{align-items:center}
.hero .wrap{padding:120px 0 80px}
.hero h1{font-size:clamp(96px,20vw,320px);line-height:.8;margin:30px 0 26px}
.hero h1 i{display:block;font-size:.2em;letter-spacing:.62em;line-height:1;margin:0 0 .25em .06em;color:var(--acc2)}
.hero h1 span{display:block;color:var(--ink);-webkit-text-stroke:0}
""",
 "masthead": """
.hero{align-items:stretch}
.hero .wrap{display:flex;flex-direction:column;min-height:100vh;padding-top:96px}
.hero h1{order:-1;font-size:clamp(90px,24vw,400px);line-height:.82;margin:0;letter-spacing:-.02em}
.hero h1 span{display:inline}
.hero .chip{margin-top:auto;align-self:flex-start}
.hero:after{background:linear-gradient(180deg,rgba(11,11,14,.82) 0%,rgba(11,11,14,.15) 45%,rgba(11,11,14,.6) 75%,var(--bg) 100%)}
""",
 "framed": """
.hero{align-items:center}
.hero .wrap{padding:120px 0 90px}
.hero h1{display:table;font-size:clamp(50px,7.6vw,118px);line-height:1.02;border:3px solid var(--acc);padding:.22em .34em .16em;margin:28px 0 26px;background:rgba(16,12,20,.45);backdrop-filter:blur(3px)}
.hero h1 span{display:block}
.hero p.lead{border-left:2px solid var(--acc);padding-left:18px}
""",
 "vertical": """
@media(min-width:900px){
.hero .wrap{display:grid;grid-template-columns:auto 1fr;grid-template-rows:1fr auto auto auto;column-gap:56px;align-items:end;min-height:72vh}
.hero h1{grid-column:1;grid-row:1/5;writing-mode:vertical-rl;transform:rotate(180deg);font-size:clamp(90px,15vh,170px);line-height:.86;margin:0;white-space:nowrap}
.hero h1 span{display:inline}
.hero .wrap>*:not(h1){grid-column:2;justify-self:start}
.hero .chip{grid-row:2}.hero p.lead{grid-row:3}.hero .cta{grid-row:4}
}
""",
}

def aff(url, slug=""):
    """Append partner tracking where an ID is configured (affiliate.json)."""
    if AFF.get("apple_token") and "music.apple.com" in url:
        sep = "&" if "?" in url else "?"
        return f"{url}{sep}at={AFF['apple_token']}&ct={slug or 'rootspages'}"
    return url

def aff_active():
    return bool(AFF.get("apple_token") or AFF.get("juno_active"))

def links_for(a):
    """Stream and shop links. Official profile URLs from artists.json win; otherwise a search link (replace before go-live)."""
    q, n = quote_plus(a["name"]), quote(a["name"])
    o = a.get("links", {})
    stream = [("Apple Music", a["apple"]),
              ("Spotify", o.get("spotify", f"https://open.spotify.com/search/{n}/artists")),
              ("YouTube", o.get("youtube", f"https://www.youtube.com/results?search_query={q}")),
              ("Deezer", o.get("deezer", f"https://www.deezer.com/search/{n}/artist")),
              ("Tidal", o.get("tidal", f"https://listen.tidal.com/search/artists?q={q}"))]
    shop = [("Buyreggae", a["buyreggae"]),
            ("Discogs", o.get("discogs", f"https://www.discogs.com/search/?q={q}&type=artist")),
            ("Juno Records", o.get("juno", f"https://www.juno.co.uk/search/?q%5Ball%5D%5B%5D={q}")),
            ("Bandcamp", o.get("bandcamp", f"https://bandcamp.com/search?q={q}&item_type=b")),
            ("Beatport / Traxsource", o.get("downloads", f"https://www.traxsource.com/search?term={q}"))]
    fmt = lambda xs: "".join(f'<a href="{e(aff(u, a.get("_slug", "")))}" target="_blank" rel="noopener">{e(l)}</a>' for l, u in xs)
    return fmt(stream), fmt(shop), [u for _, u in stream + shop if "search" not in u] + list(a.get("social", {}).values())

def favicon(a):
    ini = "".join(w[0] for w in a["name"].split()[:2]).upper()
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><rect width='64' height='64' rx='14' fill='#0c0b0a'/>"
           f"<text x='32' y='44' font-family='Impact,Arial Narrow,sans-serif' font-size='30' text-anchor='middle' fill='{a['accent']}'>{ini}</text></svg>")
    return "data:image/svg+xml," + quote(svg)

def write_press(slug, a):
    """Printable one-page press kit (EPK) at ../<slug>/press/index.html"""
    photos = [a["hero"], a["about_img"]] + a["gallery"]
    seen, pics = set(), []
    for u in photos:
        if u not in seen:
            seen.add(u); pics.append(u)
    rel = "".join(f"<tr><td>{y}</td><td>{e(ti)}</td><td>{e(r or '')}</td><td>{e(l)}</td></tr>" for _, ti, r, l, y, _ in a["releases"])
    facts = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in a["facts"])
    bio = "".join(f"<p>{e(p)}</p>" for p in a["bio"])
    imgs = "".join(f'<figure><img src="{u}" alt="{e(a["name"])}"><figcaption><a href="{u.replace("/960px-", "/1920px-")}" target="_blank" rel="noopener">High-res</a></figcaption></figure>' for u in pics)
    html_ = f"""<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(a["name"])} · Press kit</title><meta name="robots" content="noindex"><link rel="icon" href="{favicon(a)}">
<style>@font-face{{font-family:Anton;src:url(../../assets/fonts/anton-latin-400-normal.woff2) format("woff2")}}@font-face{{font-family:Inter;font-weight:400;src:url(../../assets/fonts/inter-latin-400-normal.woff2) format("woff2")}}@font-face{{font-family:Inter;font-weight:600;src:url(../../assets/fonts/inter-latin-600-normal.woff2) format("woff2")}}
body{{font:15px/1.6 Inter,Arial,sans-serif;color:#151311;background:#fff;margin:0}}main{{max-width:880px;margin:0 auto;padding:48px 28px}}
h1{{font:400 64px/1 Anton,Impact,sans-serif;text-transform:uppercase;margin:6px 0 4px}}h2{{font:400 26px/1 Anton,Impact,sans-serif;text-transform:uppercase;margin:36px 0 12px;border-bottom:3px solid {a["accent"]};padding-bottom:6px}}
.k{{font-size:12px;letter-spacing:.2em;text-transform:uppercase;color:#7a7266}}.lead{{font-size:18px}}
dl{{display:grid;grid-template-columns:1fr 1fr;gap:10px 24px}}dt{{font-size:11px;letter-spacing:.15em;text-transform:uppercase;color:#7a7266}}dd{{margin:0;font-weight:600}}
table{{width:100%;border-collapse:collapse;font-size:14px}}td{{padding:6px 8px;border-bottom:1px solid #e5e0d8}}
.ph{{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}}figure{{margin:0}}figure img{{width:100%;aspect-ratio:4/5;object-fit:cover;border-radius:4px}}figcaption{{font-size:12px;margin-top:4px}}
.bar{{display:flex;gap:10px;margin:20px 0}}.bar a,.bar button{{background:#151311;color:#fff;border:0;border-radius:99px;padding:10px 18px;font:600 13px Inter,sans-serif;cursor:pointer;text-decoration:none}}
.small{{font-size:12px;color:#7a7266}}@media print{{.bar{{display:none}}main{{padding:0}}h2{{break-after:avoid}}.ph{{break-inside:avoid}}}}</style></head><body><main>
<div class="k">Electronic press kit</div><h1>{e(a["name"])}</h1><p class="lead">{e(a["tagline"])}</p>
<div class="bar"><button onclick="print()">Print / save as PDF</button><a href="../">Back to website</a></div>
<h2>Biography</h2>{bio}<h2>Facts</h2><dl>{facts}</dl>
<h2>Selected vinyl releases</h2><table>{rel}</table>
<h2>Press photos</h2><div class="ph">{imgs}</div><p class="small">{e(a["credits"])}. Please credit the photographer when publishing.</p>
<h2>Booking &amp; contact</h2><p>Booking and management: <a href="{a["booking"]}">{a["booking"]}</a><br>Technical rider and hospitality rider on request.</p>
<p class="small">Design preview by Roots Pages, not an official press kit.</p></main></body></html>"""
    d = os.path.join(HERE, "..", slug, "press"); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(html_)

def more_shops(artist, title):
    """Extra record stores per release (search links, so they work for any shop stock)."""
    clean = title.split(" (")[0]
    q = quote_plus(f"{artist} {clean}")
    return [("Discogs", f"https://www.discogs.com/sell/list?q={q}&format=Vinyl"),
            ("Juno", f"https://www.juno.co.uk/search/?q%5Ball%5D%5B%5D={q}"),
            ("eBay", f"https://www.ebay.de/sch/i.html?_nkw={q}+vinyl")]

import re as _re
RASTA = ("#2f8f3a", "#f2b632", "#d9452b")

def _facts(a):
    f = dict(a["facts"])
    origin = f.get("From", "Jamaica")
    return origin, str(a.get("est", ""))

def _txt(x, y, s, size, fill, extra="", anchor="middle"):
    return f'<text x="{x}" y="{y}" text-anchor="{anchor}" font-size="{size}" fill="{fill}" style="font-family:var(--display)" {extra}>{e(s)}</text>'

def design(a, kind, pid):
    """Print artwork in a 200x200 box. kind: seal | type | vinyl"""
    th = a.get("theme", "poster"); acc, acc2 = a["accent"], a["accent2"]
    name = a["name"]; words = name.split(); origin, yr = _facts(a)
    up = (lambda s: s) if th == "serif" else str.upper
    ink = "#f4efe4"
    if kind == "seal":
        ring = f"{up(name)} ★ {up(origin)} ★ "
        g = (f'<defs><path id="{pid}c" d="M100,100 m-74,0 a74,74 0 1,1 148,0 a74,74 0 1,1 -148,0"/></defs>'
             f'<circle cx="100" cy="100" r="96" fill="none" stroke="{acc}" stroke-width="3"/>'
             f'<circle cx="100" cy="100" r="60" fill="none" stroke="{acc}" stroke-width="1.5" stroke-dasharray="2 4"/>'
             f'<text font-size="15" fill="{ink}" letter-spacing="3" style="font-family:var(--body);font-weight:700">'
             f'<textPath href="#{pid}c" startOffset="0" textLength="458" lengthAdjust="spacing">{e(ring)}</textPath></text>')
        mid = words[0] if len(words) > 1 else name
        g += _txt(100, 104, up(mid), 30 if len(mid) < 6 else 24, acc)
        g += _txt(100, 130, up(" ".join(words[1:])), 20 if len(" ".join(words[1:])) < 9 else 16, ink)
        if yr: g += _txt(100, 76, f"EST. {yr}", 10, ink, 'letter-spacing="3" style="font-family:var(--body);font-weight:700"')
        return g
    if kind == "type":
        if th == "slab":
            g = "".join(f'<rect x="20" y="{18 + i*9}" width="160" height="6" fill="{c}"/>' for i, c in enumerate(RASTA))
            g += "".join(_txt(100, 92 + i*46, up(w), 44, acc if i else ink) for i, w in enumerate(words[:2]))
            g += _txt(100, 178, "ROOTS · CULTURE · REALITY", 10, ink, 'letter-spacing="2" style="font-family:var(--body);font-weight:700"')
            g += "".join(f'<rect x="20" y="{184 + i*0}" width="0" height="0"/>' for i in range(0))
            return g
        if th == "serif":
            g = _txt(100, 78, words[0], 46, ink, 'font-weight="700"')
            g += _txt(100, 128, " ".join(words[1:]), 40, acc, 'font-weight="700" font-style="italic"')
            g += f'<path d="M40 142 Q100 160 160 142" fill="none" stroke="{acc}" stroke-width="2"/>'
            g += _txt(100, 176, "LOVERS ROCK · ROOTS", 10, ink, 'letter-spacing="4" style="font-family:var(--body);font-weight:600"')
            return g
        # poster: echo outline effect
        g = ""
        for i, w in enumerate(words[:2]):
            y = 88 + i*62
            g += _txt(104, y + 4, up(w), 64, acc2)
            g += _txt(100, y, up(w), 64, ink if i == 0 else acc)
        return g
    if kind == "vinyl":
        g = f'<circle cx="100" cy="100" r="92" fill="#0b0b0b" stroke="#333" stroke-width="1"/>'
        g += "".join(f'<circle cx="100" cy="100" r="{r}" fill="none" stroke="#262626" stroke-width=".8"/>' for r in range(48, 90, 5))
        g += f'<path d="M40 60 A70 70 0 0 1 100 30" fill="none" stroke="rgba(255,255,255,.18)" stroke-width="4"/>'
        g += f'<circle cx="100" cy="100" r="40" fill="{acc}"/><circle cx="100" cy="100" r="4" fill="#0b0b0b"/>'
        g += _txt(100, 92, up(words[0]), 13, "#111")
        g += _txt(100, 118, up(" ".join(words[1:])), 11, "#111")
        return g
    return ""

GARMENT = {
 "tee": ('M95 22 Q150 50 205 22 L262 44 L292 114 L250 130 L238 104 L238 300 Q150 308 62 300 L62 104 L50 130 L8 114 L38 44 Z',
         'M95 22 Q150 62 205 22', (80, 72, .7)),
 "hoodie": ('M70 66 L40 80 L10 258 L48 268 L68 146 L68 306 Q150 314 232 306 L232 146 L252 268 L290 258 L260 80 L230 66 Q150 40 70 66 Z',
            'M108 64 Q150 96 192 64', (95, 104, .55)),
}

def garment_svg(a, kind, art, pid, col):
    body, collar, (tx, ty, sc) = GARMENT[kind]
    g = (f'<svg viewBox="0 0 300 330" aria-hidden="true"><defs>'
         f'<linearGradient id="{pid}s" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".35"/><stop offset=".3" stop-color="#fff" stop-opacity=".06"/>'
         f'<stop offset=".55" stop-color="#fff" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".4"/></linearGradient>'
         f'<radialGradient id="{pid}g" cx=".5" cy=".95" r=".5"><stop offset="0" stop-color="#000" stop-opacity=".55"/><stop offset="1" stop-color="#000" stop-opacity="0"/></radialGradient></defs>'
         f'<ellipse cx="150" cy="316" rx="120" ry="10" fill="url(#{pid}g)"/>')
    if kind == "hoodie":
        g += f'<path d="M96 70 Q98 12 150 10 Q202 12 204 70 Q150 98 96 70 Z" fill="{col}"/><path d="M96 70 Q98 12 150 10 Q202 12 204 70 Q150 98 96 70 Z" fill="url(#{pid}s)"/>'
    g += f'<path d="{body}" fill="{col}"/>'
    if kind == "hoodie":
        g += '<path d="M112 66 Q150 30 188 66 Q150 88 112 66 Z" fill="#000" opacity=".45"/>'
        g += '<path d="M138 80 L134 136 M162 80 L166 136" stroke="#ddd" stroke-width="2.4" stroke-linecap="round" opacity=".8"/>'
        g += '<path d="M92 232 L208 232 L222 292 L78 292 Z" fill="none" stroke="#000" stroke-opacity=".35" stroke-width="2"/>'
        g += '<rect x="68" y="294" width="164" height="12" fill="#000" opacity=".18"/>'
    g += f'<path d="{collar}" fill="none" stroke="#000" stroke-opacity=".45" stroke-width="7" stroke-linecap="round"/>'
    g += f'<g transform="translate({tx} {ty}) scale({sc})">{art}</g>'
    g += f'<path d="{body}" fill="url(#{pid}s)"/>'
    g += ('<path d="M90 140 Q110 200 96 280 M210 150 Q190 210 206 286 M140 250 Q150 270 160 300" fill="none" stroke="#000" stroke-opacity=".12" stroke-width="3"/>')
    return g + '</svg>'

def tote_svg(a, art, pid):
    return (f'<svg viewBox="0 0 300 330" aria-hidden="true"><defs><linearGradient id="{pid}t" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".18"/>'
            f'<stop offset=".5" stop-color="#fff" stop-opacity=".05"/><stop offset="1" stop-color="#000" stop-opacity=".22"/></linearGradient></defs>'
            f'<ellipse cx="150" cy="318" rx="110" ry="8" fill="#000" opacity=".4"/>'
            f'<path d="M105 96 Q105 22 150 22 Q195 22 195 96" fill="none" stroke="#cbbd9f" stroke-width="10"/>'
            f'<path d="M52 92 L248 92 L256 312 L44 312 Z" fill="#e6dac2"/><g transform="translate(60 118) scale(.9)">'
            + art.replace('fill="#f4efe4"', 'fill="#1b1814"').replace(f'fill="{ "#f4efe4" }"', 'fill="#1b1814"') +
            f'</g><path d="M52 92 L248 92 L256 312 L44 312 Z" fill="url(#{pid}t)"/></svg>')

def poster_svg(a, pid):
    words = a["name"].upper().split() if a.get("theme") != "serif" else a["name"].split()
    acc = a["accent"]
    return (f'<svg viewBox="0 0 300 330" aria-hidden="true"><defs><filter id="{pid}f"><feColorMatrix type="saturate" values="0"/></filter>'
            f'<clipPath id="{pid}c"><rect x="52" y="14" width="196" height="290"/></clipPath></defs>'
            f'<rect x="58" y="20" width="196" height="290" fill="#000" opacity=".45"/>'
            f'<g clip-path="url(#{pid}c)"><rect x="52" y="14" width="196" height="290" fill="#111"/>'
            f'<image href="{e(a["about_img"])}" x="52" y="14" width="196" height="230" preserveAspectRatio="xMidYMid slice" filter="url(#{pid}f)" opacity=".85"/>'
            f'<rect x="52" y="14" width="196" height="230" fill="{acc}" style="mix-blend-mode:multiply"/>'
            f'<rect x="52" y="200" width="196" height="104" fill="#111"/></g>'
            + "".join(_txt(150, 236 + i*30, w, 30, "#f4efe4" if i == 0 else acc) for i, w in enumerate(words[:2]))
            + _txt(150, 292, (a.get("new_label", "").split(": ")[-1] or "ROOTS REGGAE").upper(), 9, "#f4efe4", 'letter-spacing="3" style="font-family:var(--body);font-weight:700"')
            + '</svg>')

MERCH_COL = {"poster": ("#141414", "#1d2a40"), "slab": ("#151515", "#2e3b24"), "serif": ("#1a1512", "#4a2f25")}
MERCH_DEFAULT = [("tee", "T-Shirt"), ("hoodie", "Hoodie"), ("tote", "Tote Bag"), ("poster", "Tour Poster")]

def merch_svg(kind, a):
    th = a.get("theme", "poster"); tee_c, hood_c = MERCH_COL.get(th, MERCH_COL["poster"])
    pid = f"m{kind}"
    if kind == "tee": return garment_svg(a, "tee", design(a, "type", pid + "d"), pid, tee_c)
    if kind == "hoodie": return garment_svg(a, "hoodie", design(a, "seal", pid + "d"), pid, hood_c)
    if kind == "tote": return tote_svg(a, design(a, "vinyl" if th == "poster" else "seal", pid + "d"), pid)
    return poster_svg(a, pid)

def merch_html(a):
    items = a.get("merch") or []
    url = a.get("merch_url", "")
    if items:  # real products from management: [{"name","price","img","url"}]
        cards = [f'<a class="mi" href="{e(m.get("url") or url)}" target="_blank" rel="noopener"><div class="mp"><img src="{e(m["img"])}" alt="{e(m["name"])}" loading="lazy"></div>'
                 f'<h3>{e(m["name"])}</h3><p>{e(m.get("price",""))}</p></a>' for m in items]
    else:      # design concepts until a store exists
        cards = [f'<div class="mi"><div class="mp">{merch_svg(k, a)}<span class="cn" data-i18n="merch_concept">Design concept</span></div><h3>{n}</h3></div>' for k, n in MERCH_DEFAULT]
    btn = (f'<a class="btn p" href="{e(url)}" target="_blank" rel="noopener" data-i18n="merch_shop">Shop merch</a>' if url
           else '<a class="btn g" href="#press" data-i18n="merch_notify">Get notified at launch</a>')
    return "".join(cards), btn

def sample(pid):  # buyreggae preview pattern: /sounds/<id//10000>/<id>A.mp3
    return f"https://www.buyreggae.com/sounds/{pid // 10000}/{pid}A.mp3"

for slug, a in data.items():
    a["_slug"] = slug
    tracks, rows, cards = [], [], []
    for pid, title, riddim, label, year, _ in a["releases"]:
        url = f"https://www.buyreggae.com/products/{pid}"
        img = f"https://www.buyreggae.com/images/product/P{pid}.jpg"
        meta = " · ".join(x for x in [riddim, label] if x)
        tracks.append({"id": pid, "title": title, "sub": f"{meta} · {year}", "mp3": sample(pid), "img": img, "url": url})
        i = len(tracks) - 1
        rows.append(f'<li onclick="playIdx({i})"><span class="pb"><span class="ic">{PLAY}</span><span class="eq"><i></i><i></i><i></i></span></span>'
                    f'<span class="t">{e(title)}<span class="s">{e(meta)}</span></span><span class="y">{year}</span>'
                    f'<a class="b" href="{url}" target="_blank" rel="noopener" onclick="event.stopPropagation()">Buy</a></li>')
        cards.append(f'<article class="rel rv"><div class="cv"><img src="{img}" alt="{e(title)}" loading="lazy"><span class="yr">{year}</span>'
                     f'<div class="ov"><button onclick="playId({pid})" aria-label="Preview">{PLAY}</button><a href="{url}" target="_blank" rel="noopener" aria-label="Buy">{CART}</a></div></div>'
                     f'<h3>{e(title)}</h3><p>{e(meta)}</p><div class="shops"><a class="buy" href="{url}" target="_blank" rel="noopener">Buyreggae</a>'
                     + "".join(f'<a href="{e(u)}" target="_blank" rel="noopener">{n}</a>' for n, u in more_shops(a["name"], title))
                     + '</div></article>')
    words = a["name"].split()
    h1 = f"<i>{e(words[0])}</i>" + "".join(f" <span>{e(w)}</span>" for w in words[1:])
    marquee = "".join(f"<span>{e(l)}</span><i>✦</i>" for l in a["labels"])
    gallery = "".join(f'<img src="{u}" alt="{e(a["name"])} live">' for u in a["gallery"])
    facts = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in a["facts"])
    bio = "".join(f"<p>{e(p)}</p>" for p in a["bio"])
    stream_html, shop_html, same_as = links_for(a)
    ld = {"@context": "https://schema.org", "@type": "MusicGroup", "name": a["name"], "genre": "Reggae",
          "description": a["tagline"], "image": a["hero"], "sameAs": same_as,
          "track": [{"@type": "MusicRecording", "name": t["title"], "url": t["url"]} for t in tracks[:6]]}
    if a.get("video_file"):  # self-hosted loop: no third-party request, no consent needed
        hero_video = f'<video class="loop" src="{e(a["video_file"])}" poster="{a["hero"]}" autoplay muted loop playsinline preload="auto"></video>'
        hero_js = ""
    else:
        hero_video = '<div class="vid" id="vid"><div id="yt"></div></div>'
        hero_js = HERO_YT_JS
    loc = {"en": {"tagline": a["tagline"], "bio": a["bio"], "facts": a["facts"]}}
    loc.update(a.get("i18n", {}))
    write_press(slug, a)
    merch_cards, merch_btn = merch_html(a)
    rep = {"HERO_VIDEO_JS": hero_js, "HERO_VIDEO": hero_video,
           "UI_JSON": json.dumps(UI, ensure_ascii=False).replace("</", "<\\/"),
           "LOC_JSON": json.dumps(loc, ensure_ascii=False).replace("</", "<\\/"),
           "SPOTIFY_ID": a.get("spotify_id", ""), "NAME_Q": quote_plus(a["name"]),
           "NEWSLETTER_ENDPOINT": e(a.get("newsletter_endpoint", "")),
           "AFF_NOTE": ('<p class="aff" data-i18n="aff_note">Some shop links are affiliate links: if you buy through them, the shop pays a small commission. The price stays the same for you.</p>' if aff_active() else ""),
           "SOCIAL": ('<div><h3>Follow</h3><div class="links">' + "".join(f'<a href="{e(u)}" target="_blank" rel="noopener">{e(n)}</a>' for n, u in a.get("social", {}).items()) + '</div></div>') if a.get("social") else "",
           "THEME_CSS": THEMES[a.get("theme", "poster")]["css"] + LAYOUTS[a.get("layout", "stack")], "FONT_PRELOAD": THEMES[a.get("theme", "poster")]["preload"],
           "MERCH": merch_cards, "MERCH_BTN": merch_btn,
           "NAME_H1": h1, "STREAM_LINKS": stream_html, "SHOP_LINKS": shop_html, "FAVICON": favicon(a),
           "JSONLD": json.dumps(ld, ensure_ascii=False).replace("</", "<\\/"), "FORM_ENDPOINT": e(a.get("form_endpoint", "")), "NAME": e(a["name"]), "TAGLINE": e(a["tagline"]), "ACCENT2": a["accent2"], "ACCENT": a["accent"],
           "HERO_POS": a["hero_pos"], "HERO": a["hero"], "BAND": a["band_img"], "ABOUT_IMG": a["about_img"],
           "MARQUEE": marquee, "TRACKS_JSON": json.dumps(tracks, ensure_ascii=False), "TRACKS": "\n".join(rows),
           "RELEASES": "\n".join(cards), "GALLERY": gallery, "FACTS": facts, "BIO": bio, "SHOP": a["buyreggae"],
           "APPLE": a["apple"], "BOOKING": a["booking"], "COUNT": str(len(cards)), "CREDITS": e(a["credits"]),
           "NEW_LABEL": e(a["new_label"]),
           "SLIDES": "".join(f'<div style="background-image:url(\'{u}\');background-position:{p}"></div>' for u, p in a["slides"]),
           "VIDEO": a["video"], "VIDEO_START": str(a["video_start"]), "VIDEO_LABEL": e(a["video_label"])}
    out = tpl
    for k, v in rep.items():
        out = out.replace("{{" + k + "}}", v)
    assert "{{" not in out, [l for l in out.splitlines() if "{{" in l][:3]
    d = os.path.join(HERE, "..", slug); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(out)
    print("built", slug, len(out))
