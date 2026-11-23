"""Builds one static artist site per entry in artists.json.
Usage: python3 build.py  -> writes ../<slug>/index.html"""
import json, html, os
HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(HERE, "artists.json")))
tpl = open(os.path.join(HERE, "template.html")).read()
e = html.escape
PLAY = '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M7 4v16l13-8z"/></svg>'
CART = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2"><path d="M3 4h2l2.4 11.2a2 2 0 0 0 2 1.6h7.7a2 2 0 0 0 2-1.5L21 8H6"/><circle cx="10" cy="20" r="1.3"/><circle cx="17" cy="20" r="1.3"/></svg>'

def sample(pid):  # buyreggae preview pattern: /sounds/<id//10000>/<id>A.mp3
    return f"https://www.buyreggae.com/sounds/{pid // 10000}/{pid}A.mp3"

for slug, a in data.items():
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
                     f'<h3>{e(title)}</h3><p>{e(meta)}</p><a class="buy" href="{url}" target="_blank" rel="noopener">Buy vinyl</a></article>')
    words = a["name"].split()
    h1 = e(words[0]) + "".join(f"<span>{e(w)}</span>" for w in words[1:])
    marquee = "".join(f"<span>{e(l)}</span><i>✦</i>" for l in a["labels"])
    gallery = "".join(f'<img src="{u}" alt="{e(a["name"])} live">' for u in a["gallery"])
    facts = "".join(f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in a["facts"])
    bio = "".join(f"<p>{e(p)}</p>" for p in a["bio"])
    rep = {"NAME_H1": h1, "NAME": e(a["name"]), "TAGLINE": e(a["tagline"]), "ACCENT2": a["accent2"], "ACCENT": a["accent"],
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
