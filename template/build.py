"""Builds one static artist site per entry in artists.json.
Usage: python3 build.py  -> writes ../<slug>/index.html"""
import json, html, os, re
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
 "stencil": {"preload": "black-ops-one-latin-400-normal.woff2", "css": """
@font-face{font-family:"Black Ops One";font-style:normal;font-weight:400;font-display:swap;src:url("../assets/fonts/black-ops-one-latin-400-normal.woff2") format("woff2")}
:root{--display:"Black Ops One",Impact,sans-serif;--bg:#0d0a08;--panel:#17110d;--ink:#f6eee2;--mute:#b8a894}
.hero h1 span{-webkit-text-stroke:0;color:var(--ink)}
.h2{font-size:clamp(34px,4.6vw,66px);line-height:1}
.btn,.rel .shops a,.lang button{border-radius:3px}
.marquee{background:linear-gradient(90deg,#d42a20,#f08a1c,#f6c21a)}.marquee div{color:#0d0a08}
"""},
 "retro": {"preload": "righteous-latin-400-normal.woff2", "css": """
@font-face{font-family:"Righteous";font-style:normal;font-weight:400;font-display:swap;src:url("../assets/fonts/righteous-latin-400-normal.woff2") format("woff2")}
:root{--display:"Righteous","Arial Rounded MT Bold",sans-serif;--bg:#0b0d0a;--panel:#131711;--ink:#f5f0de;--mute:#aeb3a2}
.hero h1 span{-webkit-text-stroke:0;color:var(--ink)}
.h2{font-size:clamp(38px,5.2vw,76px);line-height:1}
.btn{border-radius:99px}.rel .shops a,.lang button{border-radius:8px}
.marquee{background:#f6c21a}.marquee div{color:#0b0d0a}
"""},
}

# Hero layouts: position and line breaks of the artist name (independent of the font theme)
LAYOUTS = {
 "stack": "",
 "center": """
.hero{align-items:center;text-align:center}
.hero .wrap{padding-top:120px;padding-bottom:90px;display:flex;flex-direction:column;align-items:center}
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
.hero .wrap{padding-top:120px;padding-bottom:80px}
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
.hero .wrap{padding-top:120px;padding-bottom:90px}
.hero h1{display:table;font-size:clamp(50px,7.6vw,118px);line-height:1.02;border:3px solid var(--acc);padding:.22em .34em .16em;margin:28px 0 26px;background:rgba(16,12,20,.45);backdrop-filter:blur(3px)}
.hero h1 span{display:block}
.hero p.lead{border-left:2px solid var(--acc);padding-left:18px}
""",
 "vertical": """
@media(min-width:900px){
.hero .wrap{display:grid;grid-template-columns:auto 1fr;grid-template-rows:1fr auto auto auto auto;column-gap:56px;align-items:end;min-height:72vh}
.hero h1{grid-column:1;grid-row:1/6;writing-mode:vertical-rl;transform:rotate(180deg);font-size:clamp(90px,15vh,170px);line-height:.86;margin:0;white-space:nowrap}
.hero h1 span{display:inline}
.hero .wrap>*:not(h1){grid-column:2;justify-self:start}
.hero .chip{grid-row:2}.hero p.lead{grid-row:3}.hero .cta{grid-row:4}.hero .soc{grid-row:5}
}
""",
 "fire": """
.hero{align-items:stretch}
.hero .wrap{display:flex;flex-direction:column;justify-content:flex-end;min-height:100vh;padding-top:130px;padding-bottom:70px}
.hero .wrap>*:not(h1){align-self:flex-start}
.hero h1{order:9;font-size:clamp(56px,11vw,176px);line-height:.9;margin:34px 0 0;white-space:nowrap;background:linear-gradient(90deg,#f6c21a 0%,#f08a1c 45%,#d42a20 100%);-webkit-background-clip:text;background-clip:text;color:transparent}
.hero h1 i,.hero h1 span{display:inline;color:transparent;-webkit-text-stroke:0}
.hero h1:after{content:"";display:block;height:8px;margin-top:14px;background:linear-gradient(90deg,#d42a20 0 33.3%,#f6c21a 33.3% 66.6%,#1f8a3b 66.6%)}
.hero:after{background:linear-gradient(0deg,rgba(13,10,8,.96) 0%,rgba(13,10,8,.62) 45%,rgba(13,10,8,.25) 100%)}
@media(max-width:700px){.hero h1{white-space:normal}.hero h1 span{display:block}}
""",
 "sticker": """
.hero{align-items:center}
.hero .wrap{padding-top:130px;padding-bottom:90px}
.hero h1{display:inline-block;font-size:clamp(56px,11.5vw,180px);line-height:1;margin:30px 0 34px -6px;padding:.08em .28em .12em;background:var(--acc);color:#0b0d0a;transform:rotate(-3deg);box-shadow:12px 12px 0 #d42a20,24px 24px 0 #1f8a3b}
.hero h1 i,.hero h1 span{display:inline;color:#0b0d0a;-webkit-text-stroke:0}
""",
}

DISCO_ALL = json.load(open(os.path.join(HERE, "discography.json")))
DISCOGS_IDS = {"chuck-fenda": 81766, "turbulence": 306321, "jah-mason": 154711, "glen-washington": 166268, "lutan-fyah": 413695, "natural-black": 187305, "ras-shiloh": 215529, "bugle": 828489, "natty-king": 232740}
def disco_html(slug):
    items = DISCO_ALL.get(slug, [])
    out = []
    for n, d in enumerate(items):
        cls = ' class="x"' if n >= 12 else ""
        if d.get("i"):
            href = "https://music.apple.com/album/" + d["u"]
            img = "https://is1-ssl.mzstatic.com/image/thumb/" + d["i"] + "/300x300bb.jpg"
            pic = f'<img src="{e(img)}" alt="{e(d["t"])} cover" loading="lazy" width="300" height="300">'
        else:
            href = d["url"]
            pic = f'<span class="tile"><span>{e(d["t"])}</span><small>{e(d["y"])}</small></span>'
        out.append(f'<a{cls} href="{e(href)}" target="_blank" rel="noopener">{pic}<b>{e(d["t"])}</b><small>{e(d["y"])}</small></a>')
    more = (f'<div class="more"><button class="btn g" type="button" onclick="this.closest(\'.disco\').classList.add(\'all\')"><span data-i18n="show_all">Show all</span> ({len(items)})</button></div>' if len(items) > 12 else "")
    return "".join(out), more, str(len(items))

SOCIAL_ICONS = {
 "Instagram": '<path d="M12 7.2A4.8 4.8 0 1 0 12 16.8 4.8 4.8 0 0 0 12 7.2zm0 7.9a3.1 3.1 0 1 1 0-6.2 3.1 3.1 0 0 1 0 6.2zM17 5.8a1.1 1.1 0 1 0 0 2.2 1.1 1.1 0 0 0 0-2.2zM12 2c-2.7 0-3 0-4.1.1C4.3 2.2 2.2 4.3 2.1 7.9 2 9 2 9.3 2 12s0 3 .1 4.1c.1 3.6 2.2 5.7 5.8 5.8 1.1.1 1.4.1 4.1.1s3 0 4.1-.1c3.6-.1 5.7-2.2 5.8-5.8.1-1.1.1-1.4.1-4.1s0-3-.1-4.1c-.1-3.6-2.2-5.7-5.8-5.8C15 2 14.7 2 12 2zm0 1.8c2.7 0 3 0 4 .1 2.6.1 3.9 1.4 4 4 .1 1 .1 1.3.1 4s0 3-.1 4c-.1 2.6-1.4 3.9-4 4-1 .1-1.3.1-4 .1s-3 0-4-.1c-2.6-.1-3.9-1.4-4-4-.1-1-.1-1.3-.1-4s0-3 .1-4c.1-2.6 1.4-3.9 4-4 1-.1 1.3-.1 4-.1z"/>',
 "Facebook": '<path d="M14 8.5V6.8c0-.8.2-1.3 1.4-1.3H17V2.3c-.3 0-1.3-.1-2.5-.1-2.5 0-4.2 1.5-4.2 4.3v2H7.5v3.6h2.8V22H14v-9.9h2.8l.4-3.6H14z"/>',
 "YouTube": '<path d="M23 7.2a3 3 0 0 0-2.1-2.1C19 4.6 12 4.6 12 4.6s-7 0-8.9.5A3 3 0 0 0 1 7.2 31 31 0 0 0 .5 12a31 31 0 0 0 .5 4.8 3 3 0 0 0 2.1 2.1c1.9.5 8.9.5 8.9.5s7 0 8.9-.5a3 3 0 0 0 2.1-2.1 31 31 0 0 0 .5-4.8 31 31 0 0 0-.5-4.8zM9.8 15V9l5.8 3-5.8 3z"/>',
 "X / Twitter": '<path d="M17.8 3h3.1l-6.8 7.7L22 21h-6.2l-4.9-6.4L5.3 21H2.2l7.2-8.3L1.8 3h6.4l4.4 5.8L17.8 3zm-1.1 16.2h1.7L7.4 4.7H5.6l11.1 14.5z"/>',
 "SoundCloud": '<path d="M1 14.5c0 1.4.8 2.5 1.8 2.5V12c-1 0-1.8 1.1-1.8 2.5zm2.7-3.4v6h1.1v-6.3l-1.1.3zm2-.6v6.6h1.1v-7l-1.1.4zm2-.3v6.9h1.1V9.6c-.4.1-.8.1-1.1.1zm2-.9v7.8h1.1V8.1c-.4.2-.8.4-1.1.7zM19.6 11c-.3 0-.6 0-.9.1A5.3 5.3 0 0 0 13.4 6c-.6 0-1.2.1-1.7.3v10.8h7.9a3.1 3.1 0 0 0 0-6.1z"/>',
 "Spotify": '<path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm4.6 14.4a.6.6 0 0 1-.9.2c-2.4-1.5-5.4-1.8-8.9-1a.6.6 0 1 1-.3-1.2c3.9-.9 7.2-.5 9.9 1.1.3.2.4.6.2.9zm1.2-2.7a.8.8 0 0 1-1.1.3c-2.7-1.7-6.9-2.2-10.1-1.2a.8.8 0 1 1-.5-1.5c3.7-1.1 8.3-.6 11.4 1.3.4.2.5.7.3 1.1zm.1-2.8C14.7 9 9.4 8.8 6.3 9.7a1 1 0 1 1-.6-1.8c3.5-1.1 9.4-.9 13.2 1.4a1 1 0 0 1-1 1.6z"/>',
 "TikTok": '<path d="M16.6 2h-3.3v13.4a2.9 2.9 0 1 1-2-2.8V9.2a6.3 6.3 0 1 0 5.3 6.2V8.6a8 8 0 0 0 4.7 1.5V6.8a4.7 4.7 0 0 1-4.7-4.8z"/>',
}
def social_icons(a):
    items = []
    if a.get("spotify_id"):
        items.append(("Spotify", "https://open.spotify.com/artist/" + a["spotify_id"]))
    order = ["Instagram", "Facebook", "YouTube", "TikTok", "X / Twitter", "SoundCloud"]
    soc = a.get("social", {})
    for n in order:
        if soc.get(n): items.append((n, soc[n]))
    return "".join(f'<a href="{e(u)}" target="_blank" rel="noopener" aria-label="{e(n)}" title="{e(n)}"><svg viewBox="0 0 24 24" fill="currentColor">{SOCIAL_ICONS[n]}</svg></a>' for n, u in items)

PREFIX_KEYS = {"Watch live at": "lbl_watch_live", "Watch": "lbl_watch", "Latest album": "lbl_album", "New single": "lbl_single", 'New 7"': "lbl_7inch", "Classic": "lbl_classic"}
def lbl(s):
    """translate a known English prefix of a hero label, keep the title as is"""
    for p, k in PREFIX_KEYS.items():
        if s.startswith(p + ": ") or s.startswith(p + " "):
            sep = ": " if s.startswith(p + ": ") else " "
            return f'<em class="lb"><em data-i18n="{k}">{e(p)}</em>{e(sep)}{e(s[len(p) + len(sep):])}</em>'
    return e(s)

def aff(url, slug=""):
    """Append partner tracking where an ID is configured (affiliate.json)."""
    if AFF.get("apple_token") and "music.apple.com" in url:
        sep = "&" if "?" in url else "?"
        return f"{url}{sep}at={AFF['apple_token']}&ct={slug or 'rootspages'}"
    return url

def aff_active():
    return bool(AFF.get("apple_token") or AFF.get("juno_active"))

def pic(u, alt):
    """Gallery/bio image. URL suffix #lb crops letterbox bars burned into a 16:9 frame, #x=NN sets the horizontal focus in %.
    YouTube sd* stills are 4:3 with black bars and are wrapped automatically."""
    u, _, frag = u.partition("#")
    opts = dict(p.split("=") if "=" in p else (p, "1") for p in frag.split("&") if p)
    st = f' style="object-position:{opts["x"]}% 22%"' if "x" in opts else ""
    img = f'<img src="{e(u)}" alt="{e(alt)}" loading="lazy"{st}>'
    if "lb" in opts: return f'<span class="lbx lbw">{img}</span>'
    return f'<span class="lbx">{img}</span>' if re.search(r"ytimg\.com/vi/[^/]+/sd", u) else img

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
            ("Beatport", o.get("downloads", f"https://www.beatport.com/search?q={q}"))]
    fmt = lambda xs: "".join(f'<a href="{e(aff(u, a.get("_slug", "")))}" target="_blank" rel="noopener">{e(l)}</a>' for l, u in xs)
    return fmt(stream), fmt(shop), [u for _, u in stream + shop if "search" not in u] + list(a.get("social", {}).values())

def favicon(a):
    ini = "".join(w[0] for w in a["name"].split()[:2]).upper()
    svg = (f"<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'><rect width='64' height='64' rx='14' fill='#0c0b0a'/>"
           f"<text x='32' y='44' font-family='Impact,Arial Narrow,sans-serif' font-size='30' text-anchor='middle' fill='{a['accent']}'>{ini}</text></svg>")
    return "data:image/svg+xml," + quote(svg)

def write_press(slug, a):
    """Printable one-page press kit (EPK) at ../<slug>/press/index.html"""
    photos = [u.split("#")[0] for u in [a["hero"], a["about_img"]] + a["gallery"]]
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
<h2>Booking &amp; contact</h2><p>{(f'Booking and management: <a href="{a["booking"]}">{a["booking"]}</a>' if a["booking"] else "Booking and management: via the booking form on the website.")}<br>Technical rider and hospitality rider on request.</p>
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

R, Y, G, INK, CREAM = "#d42a20", "#f6c21a", "#1f8a3b", "#121212", "#f3ead6"

def _duo(pid, dark, light, contrast=1.9):
    """Black-and-white high-contrast portrait mapped onto two print colours (screen-print look)."""
    def ch(i):
        a, b = int(dark[1+2*i:3+2*i], 16)/255, int(light[1+2*i:3+2*i], 16)/255
        return f"{a:.3f} {b:.3f}"
    k = -(contrast - 1) / 2
    return (f'<filter id="{pid}" color-interpolation-filters="sRGB"><feColorMatrix type="saturate" values="0"/>'
            f'<feComponentTransfer><feFuncR type="gamma" exponent=".62"/><feFuncG type="gamma" exponent=".62"/><feFuncB type="gamma" exponent=".62"/></feComponentTransfer>'
            f'<feComponentTransfer><feFuncR type="linear" slope="{contrast}" intercept="{k}"/><feFuncG type="linear" slope="{contrast}" intercept="{k}"/><feFuncB type="linear" slope="{contrast}" intercept="{k}"/></feComponentTransfer>'
            f'<feComponentTransfer><feFuncR type="table" tableValues="{ch(0)}"/><feFuncG type="table" tableValues="{ch(1)}"/><feFuncB type="table" tableValues="{ch(2)}"/></feComponentTransfer></filter>')

def _face(a, pid, x, y, w, h, filt, clip):
    """Artist photo cropped on the face. merch_crop = [focus x, focus y (0..1 of the photo), zoom, photo width/height]."""
    fx, fy, z, ar = a.get("merch_crop", [.5, .4, 1, 16 / 9])
    ih = h * z; iw = ih * ar
    if iw < w * z: iw = w * z; ih = iw / ar
    ix = min(x, max(x + w - iw, x + w / 2 - iw * fx)); iy = min(y, max(y + h - ih, y + h / 2 - ih * fy))
    return (f'<g clip-path="url(#{clip})"><image href="{e(a.get("merch_img") or a["about_img"])}" x="{ix:.1f}" y="{iy:.1f}" width="{iw:.1f}" height="{ih:.1f}" '
            f'preserveAspectRatio="none" filter="url(#{filt})"/></g>')

def _name(x, y, s, size, fill, maxw, extra=""):
    fit = f' textLength="{maxw}" lengthAdjust="spacingAndGlyphs"' if len(s) * size * .78 > maxw else ""
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{fill}" style="font-family:var(--display);font-weight:700"{fit} {extra}>{e(s)}</text>'

def _small(x, y, s, size, fill, ls=3):
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-size="{size}" fill="{fill}" letter-spacing="{ls}" style="font-family:var(--body);font-weight:800">{e(s)}</text>'

def art_badge(a, pid):
    """Tee: portrait in red/gold/green rings with a name banner, classic band-tee layout."""
    origin, _ = _facts(a)
    g = f'<defs>{_duo(pid+"f", INK, Y)}<clipPath id="{pid}c"><circle cx="100" cy="88" r="62"/></clipPath></defs>'
    g += "".join(f'<circle cx="100" cy="88" r="{r}" fill="{c}"/>' for r, c in ((84, R), (77, Y), (70, G), (64, INK)))
    g += _face(a, pid, 38, 26, 124, 124, pid+"f", pid+"c")
    g += f'<path d="M14 150 L186 150 L180 166 L186 182 L14 182 L20 166 Z" fill="{R}"/>'
    g += _name(100, 175, a["name"].upper(), 24, CREAM, 150)
    g += _small(100, 198, origin.upper(), 9, Y)
    return g

def art_stripes(a, pid):
    """Hoodie: name over the three flag stripes, no photo."""
    origin, yr = _facts(a)
    w = a["name"].upper().split()
    g = ""
    if len(w) > 1:
        g += _name(100, 62, w[0], 40, Y, 170) + _name(100, 104, " ".join(w[1:]), 40, CREAM, 170)
        y0 = 118
    else:
        g += _name(100, 96, w[0], 54, Y, 170); y0 = 112
    g += "".join(f'<rect x="20" y="{y0 + i*13}" width="160" height="10" fill="{c}"/>' for i, c in enumerate((R, Y, G)))
    g += _small(100, y0 + 56, (origin + (f" · {yr}" if yr else "")).upper(), 10, CREAM)
    return g

def art_tote(a, pid):
    """Tote: one-colour black portrait print on canvas, flag stripe underneath."""
    g = f'<defs>{_duo(pid+"f", INK, "#e6dac2", 2.2)}<clipPath id="{pid}c"><rect x="30" y="0" width="140" height="140"/></clipPath></defs>'
    g += _face(a, pid, 30, 0, 140, 140, pid+"f", pid+"c")
    g += "".join(f'<rect x="{30 + i*47}" y="146" width="46" height="8" fill="{c}"/>' for i, c in enumerate((R, Y, G)))
    g += _name(100, 184, a["name"].upper(), 26, INK, 140)
    return g

GARMENT = {
 "tee": ('M95 22 Q150 50 205 22 L262 44 L292 114 L250 130 L238 104 L238 300 Q150 308 62 300 L62 104 L50 130 L8 114 L38 44 Z',
         'M95 22 Q150 62 205 22', (80, 70, .7)),
 "hoodie": ('M70 66 L40 80 L10 258 L48 268 L68 146 L68 306 Q150 314 232 306 L232 146 L252 268 L290 258 L260 80 L230 66 Q150 40 70 66 Z',
            'M108 64 Q150 96 192 64', (95, 96, .55)),
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
        g += '<path d="M138 80 L134 136 M162 80 L166 136" stroke="#e9dfc8" stroke-width="2.4" stroke-linecap="round" opacity=".8"/>'
        g += '<path d="M92 232 L208 232 L222 292 L78 292 Z" fill="none" stroke="#000" stroke-opacity=".35" stroke-width="2"/>'
        g += '<rect x="68" y="294" width="164" height="12" fill="#000" opacity=".18"/>'
    g += f'<path d="{collar}" fill="none" stroke="#000" stroke-opacity=".45" stroke-width="7" stroke-linecap="round"/>'
    g += f'<g transform="translate({tx} {ty}) scale({sc})" opacity=".96">{art}</g>'
    g += f'<path d="{body}" fill="url(#{pid}s)"/>'
    g += ('<path d="M90 140 Q110 200 96 280 M210 150 Q190 210 206 286 M140 250 Q150 270 160 300" fill="none" stroke="#000" stroke-opacity=".12" stroke-width="3"/>')
    return g + '</svg>'

def tote_svg(a, art, pid):
    return (f'<svg viewBox="0 0 300 330" aria-hidden="true"><defs><linearGradient id="{pid}t" x1="0" x2="1"><stop offset="0" stop-color="#000" stop-opacity=".18"/>'
            f'<stop offset=".5" stop-color="#fff" stop-opacity=".05"/><stop offset="1" stop-color="#000" stop-opacity=".22"/></linearGradient></defs>'
            f'<ellipse cx="150" cy="318" rx="110" ry="8" fill="#000" opacity=".4"/>'
            f'<path d="M105 96 Q105 22 150 22 Q195 22 195 96" fill="none" stroke="#cbbd9f" stroke-width="10"/>'
            f'<path d="M52 92 L248 92 L256 312 L44 312 Z" fill="#e6dac2"/><g transform="translate(62 108) scale(.88)">{art}</g>'
            f'<path d="M52 92 L248 92 L256 312 L44 312 Z" fill="url(#{pid}t)"/></svg>')

def poster_svg(a, pid):
    """Gig poster: green-to-gold duotone portrait, red header, flag stripes, name block."""
    origin, _ = _facts(a)
    x0, y0, W, H = 52, 14, 196, 290
    g = (f'<svg viewBox="0 0 300 330" aria-hidden="true"><defs>{_duo(pid+"f", "#0f2a17", Y, 1.8)}'
         f'<clipPath id="{pid}c"><rect x="{x0}" y="{y0+26}" width="{W}" height="176"/></clipPath></defs>'
         f'<rect x="{x0+6}" y="{y0+6}" width="{W}" height="{H}" fill="#000" opacity=".45"/>'
         f'<rect x="{x0}" y="{y0}" width="{W}" height="{H}" fill="{INK}"/>'
         f'<rect x="{x0}" y="{y0}" width="{W}" height="26" fill="{R}"/>'
         + _small(150, y0 + 17, "LIVE · ROOTS REGGAE", 10, CREAM, 3)
         + _face(a, pid, x0, y0 + 26, W, 176, pid+"f", pid+"c")
         + "".join(f'<rect x="{x0}" y="{y0 + 202 + i*7}" width="{W}" height="7" fill="{c}"/>' for i, c in enumerate((R, Y, G)))
         + _name(150, y0 + 256, a["name"].upper(), 30, Y, 176)
         + _small(150, y0 + 278, f"{origin.upper()} · TOUR 2027", 8, CREAM, 1)
         + '</svg>')
    return g

MERCH_DEFAULT = [("tee", "T-Shirt"), ("hoodie", "Hoodie"), ("tote", "Tote Bag"), ("poster", "Tour Poster")]

def merch_svg(kind, a):
    pid = f"m{kind}"
    if kind == "tee": return garment_svg(a, "tee", art_badge(a, pid + "d"), pid, "#151515")
    if kind == "hoodie": return garment_svg(a, "hoodie", art_stripes(a, pid + "d"), pid, "#1d3a25")
    if kind == "tote": return tote_svg(a, art_tote(a, pid + "d"), pid)
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
                    f'<a class="b" href="{url}" target="_blank" rel="noopener" onclick="event.stopPropagation()" data-i18n="buy">Buy</a></li>')
        cards.append(f'<article class="rel rv"><div class="cv"><img src="{img}" alt="{e(title)}" loading="lazy"><span class="yr">{year}</span>'
                     f'<div class="ov"><button onclick="playId({pid})" aria-label="Preview">{PLAY}</button><a href="{url}" target="_blank" rel="noopener" aria-label="Buy">{CART}</a></div></div>'
                     f'<h3>{e(title)}</h3><p>{e(meta)}</p><div class="shops"><a class="buy" href="{url}" target="_blank" rel="noopener">Buyreggae</a>'
                     + "".join(f'<a href="{e(u)}" target="_blank" rel="noopener">{n}</a>' for n, u in more_shops(a["name"], title))
                     + '</div></article>')
    words = a["name"].split()
    h1 = f"<i>{e(words[0])}</i>" + "".join(f" <span>{e(w)}</span>" for w in words[1:])
    marquee = "".join(f"<span>{e(l)}</span><i>✦</i>" for l in a["labels"])
    gallery = "".join(pic(u, a["name"] + " live") for u in a["gallery"])
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
           "SPOTIFY_ID": a.get("spotify_id", ""), "NAME_Q": quote_plus(a["name"]), "BIT_URL": a.get("bandsintown", "https://www.bandsintown.com/search?query=" + quote_plus(a["name"])),
           "NEWSLETTER_ENDPOINT": e(a.get("newsletter_endpoint", "")),
           "AFF_NOTE": ('<p class="aff" data-i18n="aff_note">Some shop links are affiliate links: if you buy through them, the shop pays a small commission. The price stays the same for you.</p>' if aff_active() else ""),
           "SOCIAL": ('<div><h3 data-i18n="follow">Follow</h3><div class="links">' + "".join(f'<a href="{e(u)}" target="_blank" rel="noopener">{e(n)}</a>' for n, u in a.get("social", {}).items()) + '</div></div>') if a.get("social") else "",
           "THEME_CSS": THEMES[a.get("theme", "poster")]["css"] + LAYOUTS[a.get("layout", "stack")], "FONT_PRELOAD": THEMES[a.get("theme", "poster")]["preload"],
           "MERCH": merch_cards, "MERCH_BTN": merch_btn,
           "NAME_H1": h1, "STREAM_LINKS": stream_html, "SHOP_LINKS": shop_html, "FAVICON": favicon(a),
           "JSONLD": json.dumps(ld, ensure_ascii=False).replace("</", "<\\/"), "FORM_ENDPOINT": e(a.get("form_endpoint", "")), "NAME": e(a["name"]), "TAGLINE": e(a["tagline"]), "ACCENT2": a["accent2"], "ACCENT": a["accent"],
           "HERO_POS": a["hero_pos"], "HERO": a["hero"], "BAND": a["band_img"], "ABOUT_IMG": a["about_img"].split("#")[0], "ABOUT_PIC": pic(a["about_img"], a["name"] + " live"),
           "MARQUEE": marquee, "TRACKS_JSON": json.dumps(tracks, ensure_ascii=False), "TRACKS": "\n".join(rows),
           "RELEASES": "\n".join(cards), "GALLERY": gallery, "FACTS": facts, "BIO": bio, "SHOP": a["buyreggae"],
           "APPLE": a["apple"], "BOOKING": a["booking"], "MGMT_BTN": (f'<a class="btn g" href="{e(a["booking"])}" target="_blank" rel="noopener" data-i18n="mgmt">Management page</a>' if a["booking"] else ""), "COUNT": str(len(cards)), "CREDITS": e(a["credits"]),
           "NEW_LABEL": lbl(a["new_label"]), "DISCO": disco_html(slug)[0], "DISCO_MORE": disco_html(slug)[1], "DISCO_COUNT": disco_html(slug)[2], "DISCOGS_ID": str(DISCOGS_IDS.get(slug, "")), "SOCIAL_ICONS": social_icons(a),
           "SLIDES": "".join(f'<div style="background-image:url(\'{u}\');background-position:{p}"></div>' for u, p in a["slides"]),
           "VIDEO": a["video"], "VIDEO_START": str(a["video_start"]), "VIDEO_LABEL": lbl(a["video_label"])}
    out = tpl
    for k, v in rep.items():
        out = out.replace("{{" + k + "}}", v)
    assert "{{" not in out, [l for l in out.splitlines() if "{{" in l][:3]
    d = os.path.join(HERE, "..", slug); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w").write(out)
    print("built", slug, len(out))
