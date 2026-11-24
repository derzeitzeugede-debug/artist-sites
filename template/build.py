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

MERCH_SHAPES = {
 "tee": '<path d="M70 30 L40 42 L14 78 L40 92 L52 74 L52 190 L148 190 L148 74 L160 92 L186 78 L160 42 L130 30 Q100 52 70 30Z" fill="{bg}" stroke="rgba(255,255,255,.15)"/>',
 "hoodie": '<path d="M72 34 Q100 14 128 34 L162 46 L188 150 L164 158 L150 92 L150 192 L50 192 L50 92 L36 158 L12 150 L38 46Z" fill="{bg}" stroke="rgba(255,255,255,.15)"/><path d="M78 36 Q100 66 122 36" fill="none" stroke="rgba(255,255,255,.25)" stroke-width="2"/><rect x="74" y="150" width="52" height="26" rx="4" fill="none" stroke="rgba(255,255,255,.18)"/>',
 "tote": '<path d="M74 60 Q74 18 100 18 Q126 18 126 60" fill="none" stroke="#d8cdb8" stroke-width="6"/><rect x="40" y="58" width="120" height="136" rx="4" fill="#e9dfcc"/>',
 "poster": '<rect x="42" y="14" width="116" height="174" fill="{bg}" stroke="rgba(255,255,255,.2)"/><circle cx="100" cy="74" r="38" fill="none" stroke="{acc2}" stroke-width="3"/><circle cx="100" cy="74" r="12" fill="{acc2}"/>',
}
MERCH_DEFAULT = [("tee", "T-Shirt"), ("hoodie", "Hoodie"), ("tote", "Tote Bag"), ("poster", "Tour Poster")]

def merch_svg(kind, a):
    words = a["name"].upper().split()
    bg = "#1b1916"; acc = a["accent"]; acc2 = a["accent2"]
    ink = "#1b1916" if kind == "tote" else acc
    y0 = {"tee": 112, "hoodie": 108, "tote": 118, "poster": 140}[kind]
    fs = 24 if max(len(w) for w in words) <= 6 else 19
    txt = "".join(f'<text x="100" y="{y0 + i*fs}" text-anchor="middle" font-family="Anton,Impact,sans-serif" font-size="{fs}" fill="{ink}">{e(w)}</text>' for i, w in enumerate(words))
    return (f'<svg viewBox="0 0 200 206" aria-hidden="true">' + MERCH_SHAPES[kind].format(bg=bg, acc2=acc2) + txt + '</svg>')

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
    h1 = e(words[0]) + "".join(f"<span>{e(w)}</span>" for w in words[1:])
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
           "THEME_CSS": THEMES[a.get("theme", "poster")]["css"], "FONT_PRELOAD": THEMES[a.get("theme", "poster")]["preload"],
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
