#!/usr/bin/env python3
"""Playsaku static site builder. Reads games.json, writes index.html, game/<slug>/index.html, sitemap.xml, robots.txt."""
import json, os, html, shutil
ROOT = os.path.dirname(os.path.abspath(__file__))
SITE = "https://game.toolsak.online"
NAME = "Playsaku"
OUT = os.path.join(ROOT, "dist")
games = json.load(open(os.path.join(ROOT, "games.json"), encoding="utf-8"))
e = html.escape

if os.path.isdir(OUT): shutil.rmtree(OUT)
os.makedirs(OUT)
shutil.copytree(os.path.join(ROOT, "assets"), os.path.join(OUT, "assets"))

def head(title, desc, path, extra=""):
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<link rel="canonical" href="{SITE}{path}"><meta name="theme-color" content="#0b0820">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website">
<link rel="icon" href="/assets/logo.svg" type="image/svg+xml">
<link rel="stylesheet" href="/assets/style.css">{extra}
</head><body>
<header class="top"><a class="brand" href="/"><img src="/assets/logo.svg" alt="" width="34" height="34"><span>Play<b>saku</b></span></a>
<label class="search"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg><input id="q" type="search" placeholder="Search games" aria-label="Search games"></label></header>
"""

FOOT = f"""<footer class="foot"><p><b>{NAME}</b> · free browser games, no download, no sign-up.</p>
<p><a href="https://toolsak.online/">Toolsaku tools</a> · <a href="https://toolsak.online/privacy/">Privacy</a> · <a href="https://toolsak.online/about/">About</a></p></footer>
<script src="/assets/app.js" defer></script></body></html>"""

def card(g, big=False):
    return (f'<a class="card{" card--big" if big else ""}" href="/game/{g["slug"]}/" data-cat="{e(g["cat"])}" data-t="{e(g["title"].lower())}">'
            f'<img src="{e(g["thumb"])}" alt="{e(g["title"])}" loading="lazy" width="512" height="384">'
            f'<span class="card__t">{e(g["title"])}</span><span class="card__c">{e(g["cat"])}</span></a>')

cats = []
for g in games:
    if g["cat"] not in cats: cats.append(g["cat"])
ICON = {"Obby": "🧱", "Brainrot": "🧠", "Puzzle": "🧩", "Racing": "🏎️", "Action": "💥", "Arcade": "🕹️", "Sports": "⚽", "Shooting": "🎯", "Multiplayer": "👥",
        "Hypercasual": "⚡", "3D": "🧊", "Stickman": "🥷", "Adventure": "🗺️"}

# ---- home
feat = games[:3]
h = head(f"{NAME} – Play Free Online Games in Your Browser", "Play free online games on your phone or computer. Racing, puzzle, action and sports games. No download, no sign-up.", "/")
h += '<main class="wrap">\n<section class="hero">'
h += '<div class="hero__txt"><p class="kick">🎮 Free · No download · Phone &amp; PC</p><h1>Tap. Play. <span>Win.</span></h1><p>Hand-picked browser games that load fast and play right here.</p></div>'
h += '<div class="hero__row">' + "".join(card(g, True) for g in feat) + "</div></section>\n"
h += '<nav class="chips" aria-label="Categories"><button class="chip is-on" data-c="">🔥 All</button>' + "".join(f'<button class="chip" data-c="{e(c)}">{ICON.get(c, "🎲")} {e(c)}</button>' for c in cats) + "</nav>\n"
h += '<h2 class="sec">Popular games</h2><div class="grid" id="grid">' + "".join(card(g) for g in games) + '</div><p class="empty" id="empty" hidden>No games found. Try another word.</p>\n'
h += "</main>" + FOOT
open(os.path.join(OUT, "index.html"), "w", encoding="utf-8").write(h)

# ---- game pages
for g in games:
    more = [x for x in games if x["cat"] == g["cat"] and x is not g] + [x for x in games if x["cat"] != g["cat"]]
    ratio = f'{g["w"]} / {g["h"]}'
    ld = json.dumps({"@context": "https://schema.org", "@type": "VideoGame", "name": g["title"], "url": f'{SITE}/game/{g["slug"]}/',
                     "image": g["thumb"], "description": g["desc"][:300], "genre": g["cat"], "gamePlatform": ["Web browser", "Android", "iOS"],
                     "applicationCategory": "Game", "operatingSystem": "Any"}, ensure_ascii=False)
    p = head(f'{g["title"]} – Play Free Online | {NAME}', (g["desc"][:150].rsplit(" ", 1)[0] + "…") if len(g["desc"]) > 150 else g["desc"],
             f'/game/{g["slug"]}/', f'<script type="application/ld+json">{ld}</script>')
    p += '<main class="wrap">\n'
    p += f'<nav class="crumb"><a href="/">Home</a> › <span>{e(g["cat"])}</span></nav>'
    p += f'<section class="play{" play--tall" if g["h"] > g["w"] else ""}" style="--ar:{ratio}"><div class="stage" id="stage" data-src="{e(g["url"])}">'
    p += f'<img class="stage__bg" src="{e(g["thumb"])}" alt=""><div class="stage__go"><img src="{e(g["thumb"])}" alt="{e(g["title"])}" width="160" height="120"><h1>{e(g["title"])}</h1><button class="btn-play" id="playBtn">▶ Play now</button></div></div>'
    p += '<div class="bar"><span class="bar__t">' + e(g["title"]) + '</span><button class="ic" id="fsBtn" aria-label="Full screen">⛶</button></div></section>\n'
    p += f'<section class="info"><h2>About {e(g["title"])}</h2><p>{e(g["desc"])}</p>'
    if g["how"]: p += f'<h2>How to play</h2><p>{e(g["how"])}</p>'
    p += f'<p class="tags">' + "".join(f"<span>{e(t.strip())}</span>" for t in g["tags"].split(",") if t.strip()) + "</p></section>\n"
    p += '<h2 class="sec">More games</h2><div class="grid">' + "".join(card(x) for x in more[:8]) + "</div>\n</main>" + FOOT
    d = os.path.join(OUT, "game", g["slug"]); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, "index.html"), "w", encoding="utf-8").write(p)

urls = ["/"] + [f'/game/{g["slug"]}/' for g in games]
open(os.path.join(OUT, "sitemap.xml"), "w").write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + "".join(f"<url><loc>{SITE}{u}</loc></url>\n" for u in urls) + "</urlset>\n")
open(os.path.join(OUT, "robots.txt"), "w").write(f"User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n")
print("built", len(games), "games")
