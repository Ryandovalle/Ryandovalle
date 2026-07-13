#!/usr/bin/env python3
"""Render GitHub profile SVG — Synthwave theme for Ryandovalle."""
import json, random, os, math

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "assets", "data.json")
OUTP = os.path.join(ROOT, "assets", "profile.svg")

NEON_PINK = "#ff007f"
NEON_CYAN = "#00f0ff"
NEON_YELLOW = "#ffd700"
NEON_ORANGE = "#ff6b35"
PURPLE = "#b000ff"
SNOW = "#e8ecff"
MUTED = "#7a7aa0"
INK = "#c7c7ee"
EMPTY = "#12122e"
BG_DEEP = "#0b021a"
BG_MID = "#1a0533"
BG_TOP = "#0f0224"

MONO = "ui-monospace,SFMono-Regular,Menlo,Consolas,monospace"

FONT = {
    "R": ["11110","10001","10001","11110","10100","10010","10001"],
    "Y": ["10001","10001","01010","00100","00100","00100","00100"],
    "A": ["01110","10001","10001","11111","10001","10001","10001"],
    "N": ["10001","11001","10101","10011","10001","10001","10001"],
    "D": ["11110","10001","10001","10001","10001","10001","11110"],
    "O": ["01110","10001","10001","10001","10001","10001","01110"],
    "V": ["10001","10001","10001","10001","10001","01010","00100"],
    "L": ["10000","10000","10000","10000","10000","10000","11111"],
    "E": ["11111","10000","11110","10000","10000","10000","11111"],
    " ": ["00000"]*7,
}

W, H = 820, 1052
Y_HERO, Y_STACK, Y_STATS, Y_NOW, Y_FOOT = 0, 258, 516, 792, 982

s = []
def add(x): s.append(x)
def esc(t): return t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

def load():
    d = json.load(open(DATA))["data"]["user"]
    cal = d["contributionsCollection"]["contributionCalendar"]
    weeks = cal["weeks"]
    days = [dd for w in weeks for dd in w["contributionDays"]]
    lon = c = 0
    for dd in days:
        if dd["contributionCount"] > 0: c += 1; lon = max(lon, c)
        else: c = 0
    return {"total": cal["totalContributions"], "repos": d["repositories"]["totalCount"],
            "followers": d["followers"]["totalCount"], "longest": lon, "weeks": weeks}

def heading(x, y, prompt, label):
    add(f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="15" font-weight="700">'
        f'<tspan fill="{NEON_YELLOW}">&gt; {esc(prompt)}</tspan><tspan fill="{NEON_CYAN}"> {esc(label)}</tspan></text>')
    add(f'<line x1="{x+(len(prompt)+len(label))*9+30}" y1="{y-5}" x2="{W-40}" y2="{y-5}" '
        f'stroke="{NEON_PINK}" stroke-opacity="0.25" stroke-width="1" stroke-dasharray="4 4"/>')

def glyphs(text, p, x0, y0, face, shadow=None, hi=None):
    ox = x0
    for ch in text:
        g = FONT.get(ch, FONT[" "])
        for r in range(7):
            for c in range(5):
                if g[r][c] == "1":
                    px, py = ox + c*p, y0 + r*p
                    if shadow:
                        sh = round(p*0.34)
                        add(f'<rect x="{px+sh}" y="{py+sh}" width="{p}" height="{p}" fill="{shadow}"/>')
                    add(f'<rect x="{px}" y="{py}" width="{p}" height="{p}" fill="{face}"/>')
                    if hi:
                        add(f'<rect x="{px}" y="{py}" width="{max(1,round(p*0.4))}" height="{max(1,round(p*0.4))}" fill="{hi}"/>')
        ox += 6*p

def chip(x, y, text, bg, fg, star=False):
    label = text + ("  *" if star else "")
    w = 18 + len(label)*7.3
    add(f'<rect x="{x+2}" y="{y+2}" width="{w:.0f}" height="23" rx="3" fill="#000" opacity="0.5"/>')
    add(f'<rect x="{x}" y="{y}" width="{w:.0f}" height="23" rx="3" fill="{bg}" stroke="{NEON_PINK}" stroke-opacity="0.5" stroke-width="1.5"/>')
    add(f'<text x="{x+w/2:.0f}" y="{y+16}" text-anchor="middle" font-family="{MONO}" font-size="12" font-weight="700" fill="{fg}">{esc(label)}</text>')
    return x + w + 9

def tile(x, y, w, num, label, fire=False):
    add(f'<rect x="{x}" y="{y}" width="{w}" height="72" rx="4" fill="#13042a" stroke="{NEON_CYAN}" stroke-opacity="0.3" stroke-width="1.5"/>')
    add(f'<text x="{x+w/2:.0f}" y="{y+38}" text-anchor="middle" font-family="{MONO}" font-size="26" font-weight="800" fill="{NEON_PINK if fire else NEON_CYAN}">{esc(str(num))}</text>')
    add(f'<text x="{x+w/2:.0f}" y="{y+58}" text-anchor="middle" font-family="{MONO}" font-size="10" letter-spacing="1" fill="{MUTED}">{esc(label)}</text>')

data = load()
DUR = 50.0

add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
    f'role="img" aria-label="Ryan do Valle — Fullstack Developer profile">')

add('<style>'
    '@keyframes tw{0%,100%{opacity:.25}50%{opacity:.9}}'
    '@keyframes shoot{0%{opacity:0;transform:translate(0,0)}12%{opacity:.95}42%{opacity:0}100%{opacity:0;transform:translate(var(--dx),var(--dy))}}'
    '@keyframes pulse{0%,100%{opacity:.6}50%{opacity:1}}'
    '@keyframes scanlines{0%{transform:translateY(0)}100%{transform:translateY(4px)}}'
    '@keyframes sunGlow{0%,100%{opacity:.7}50%{opacity:1}}'
    '@keyframes flicker{0%,100%{opacity:.5}50%{opacity:1}}'
    '@keyframes steam{0%{opacity:0;transform:translateY(0)}30%{opacity:.7}100%{opacity:0;transform:translateY(-9px)}}'
    '@media(prefers-reduced-motion:reduce){*{animation:none!important}}'
    '</style>')

add('<defs>'
    f'<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{BG_TOP}"/><stop offset="0.4" stop-color="{BG_MID}"/>'
    f'<stop offset="0.75" stop-color="#2a0845"/>'
    f'<stop offset="1" stop-color="{NEON_PINK}" stop-opacity="0.25"/></linearGradient>'
    f'<linearGradient id="sun" x1="0" y1="0" x2="0" y2="1">'
    f'<stop offset="0" stop-color="{NEON_YELLOW}"/>'
    f'<stop offset="0.4" stop-color="{NEON_ORANGE}"/>'
    f'<stop offset="0.7" stop-color="{NEON_PINK}"/>'
    f'<stop offset="1" stop-color="{PURPLE}"/></linearGradient>'
    f'<radialGradient id="sunGlowGrad" cx="50%" cy="50%" r="50%">'
    f'<stop offset="0" stop-color="{NEON_YELLOW}" stop-opacity="0.25"/>'
    f'<stop offset="1" stop-color="{NEON_PINK}" stop-opacity="0"/></radialGradient>'
    '<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">'
    f'<rect width="40" height="40" fill="none"/><rect width="1" height="40" fill="{NEON_PINK}" opacity="0.06"/>'
    f'<rect width="40" height="1" fill="{NEON_PINK}" opacity="0.06"/></pattern>'
    '<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="#000" opacity="0.1"/></pattern>'
    '</defs>')

add(f'<rect width="{W}" height="{H}" fill="url(#sky)"/>')
add(f'<rect x="60" y="20" width="{W-120}" height="{H-40}" fill="url(#grid)"/>')

# Synthwave sun at the bottom
sun_cx, sun_cy, sun_r = W//2, H-80, 260
add(f'<circle cx="{sun_cx}" cy="{sun_cy}" r="{sun_r+80}" fill="url(#sunGlowGrad)" style="animation:sunGlow 3s ease-in-out infinite"/>')
add(f'<clipPath id="sunClip"><rect x="0" y="{sun_cy-sun_r+80}" width="{W}" height="{sun_r*2}"/></clipPath>')
add(f'<circle cx="{sun_cx}" cy="{sun_cy}" r="{sun_r}" fill="url(#sun)" clip-path="url(#sunClip)"/>')

# Sun horizontal bands
for i in range(6):
    y = sun_cy - sun_r + 30 + i * (sun_r*2 - 60)/6
    op = 0.08 + i * 0.02
    add(f'<rect x="0" y="{y:.0f}" width="{W}" height="2" fill="{NEON_CYAN}" opacity="{op:.2f}" clip-path="url(#sunClip)"/>')

# Mountains silhouette
add(f'<polygon points="0,{H} 0,{H-180} 80,{H-280} 180,{H-220} 280,{H-300} 380,{H-240} 480,{H-290} 580,{H-210} 680,{H-260} 780,{H-180} 820,{H-190} 820,{H}" '
    f'fill="{BG_DEEP}" opacity="0.9"/>')

# Perspective grid floor
add(f'<g opacity="0.3">')
for i in range(18):
    y = H - i*12
    op = max(0.02, 0.25 - i*0.014)
    add(f'<line x1="0" y1="{y}" x2="{W}" y2="{y}" stroke="{NEON_PINK}" stroke-opacity="{op:.2f}" stroke-width="0.5"/>')
add('</g>')

# Stars (twinkling)
random.seed(42)
for _ in range(140):
    x, y = random.randint(0, W-2), random.randint(0, H-340)
    sz = 2 if random.random() < 0.1 else 1
    col = NEON_YELLOW if (random.random() < 0.25) else SNOW
    dur = round(random.uniform(1.8, 4.2), 2)
    delay = round(random.uniform(0, 4), 2)
    add(f'<rect x="{x}" y="{y}" width="{sz}" height="{sz}" fill="{col}" '
        f'style="animation:tw {dur}s ease-in-out infinite;animation-delay:-{delay}s"/>')

# Shooting stars
for sx, sy, dx, dy, dur, delay in [(120,60,100,45,7,0),(500,100,-140,55,9,3.2),(260,130,130,-60,8,5.6)]:
    add(f'<line x1="{sx}" y1="{sy}" x2="{sx-dx*0.22:.0f}" y2="{sy-dy*0.22:.0f}" stroke="{SNOW}" stroke-width="1.5" '
        f'style="--dx:{dx}px;--dy:{dy}px;opacity:0;animation:shoot {dur}s linear infinite;animation-delay:-{delay}s"/>')

# Section dividers
for yy in (Y_STACK, Y_STATS, Y_NOW, Y_FOOT):
    add(f'<line x1="0" y1="{yy}" x2="{W}" y2="{yy}" stroke="{NEON_PINK}" stroke-opacity="0.12" stroke-width="1"/>')

# ========== HERO ==========
title = "RYAN DO VALLE"
p = 8; tw = (len(title)*6-1)*p; x0 = (W-tw)//2
glyphs(title, p, x0, 74, NEON_PINK, shadow=PURPLE, hi=NEON_YELLOW)

sy = 74 + 7*p + 26
add(f'<rect x="{x0}" y="{sy-14}" width="{tw}" height="2" fill="{NEON_CYAN}" opacity="0.6"'
    f' style="animation:pulse 2s ease-in-out infinite"/>')
add(f'<text x="{W//2}" y="{sy+2}" text-anchor="middle" font-family="{MONO}" font-size="13" letter-spacing="4" fill="{NEON_CYAN}">F U L L S T A C K&#160;&#160;D E V E L O P E R</text>')
add(f'<text x="{W//2}" y="{sy+22}" text-anchor="middle" font-family="{MONO}" font-size="10" letter-spacing="2" fill="{MUTED}">// vue &#183; node &#183; python &#183; php &#183; typescript&#160;&#160;&#9889;</text>')

# Synthwave sun smaller accent at top of hero
add(f'<circle cx="{W-70}" cy="90" r="50" fill="#ff007f" opacity="0.08"/>')
add(f'<rect x="{W-120}" y="80" width="100" height="3" fill="{NEON_PINK}" opacity="0.4"/>')
add(f'<rect x="{W-120}" y="117" width="100" height="3" fill="{NEON_CYAN}" opacity="0.4"/>')

# ========== STACK ==========
heading(40, Y_STACK+42, "const", "stack = [")
rows = [
    ("// frontend", [("Vue","#42b883","#fff",False),("JavaScript","#f7df1e","#000",False),("TypeScript","#3178c6","#fff",True)]),
    ("// backend", [("Node.js","#339933","#fff",False),("Python","#3776ab","#fff",False),("PHP","#777bb4","#fff",False)]),
    ("// infra & more", [("Docker","#2496ed","#fff",False),("PostgreSQL","#4169e1","#fff",False),("Git","#f05032","#fff",False)]),
]
yy2 = Y_STACK + 66
for cat, chips in rows:
    add(f'<text x="40" y="{yy2+16}" font-family="{MONO}" font-size="11.5" fill="{NEON_CYAN}">{esc(cat)}</text>')
    xx = 178
    for txt, bg, fg, st in chips:
        xx = chip(xx, yy2, txt, bg, fg, st)
    yy2 += 40
add(f'<text x="40" y="{yy2+14}" font-family="{MONO}" font-size="15" font-weight="700" fill="{NEON_PINK}">]</text>')

# ========== STATS ==========
heading(40, Y_STATS+42, "git", "--stats")
tw2 = (W-80-3*16)/4; tx = 40
for num, lbl, fire in [(f"{data['total']:,}".replace(",", " "), "CONTRIBUTIONS", True),
                       (data["longest"], "LONGEST STREAK", True),
                       (data["repos"], "REPOSITORIES", False),
                       (data["followers"], "FOLLOWERS", False)]:
    tile(tx, Y_STATS+58, int(tw2), num, lbl, fire)
    tx += tw2 + 16

# Contribution grid + snake
gx, gy = 40, Y_STATS + 150
cell, gap = 11, 3; step = cell + gap
NW = len(data["weeks"])
def level(n):
    if n == 0: return EMPTY
    if n <= 3: return "#2d0b4e"
    if n <= 9: return "#7a1a7a"
    if n <= 20: return "#cc3388"
    return NEON_PINK
def center(wi, di): return (gx + wi*step + cell/2, gy + di*step + cell/2)

filled = []
for wi, wk in enumerate(data["weeks"]):
    for di, dd in enumerate(wk["contributionDays"]):
        col = level(dd["contributionCount"])
        px, py = gx + wi*step, gy + di*step
        add(f'<rect x="{px}" y="{py}" width="{cell}" height="{cell}" rx="2" fill="{EMPTY}"/>')
        if col != EMPTY:
            cx, cy = center(wi, di)
            filled.append((wi, di, col, cx, cy, px, py))

n = len(filled)
if n > 0:
    cx0 = [f[3] for f in filled]; cy0 = [f[4] for f in filled]
    used = [False]*n
    cur = min(range(n), key=lambda j: cx0[j] + cy0[j])
    tour = [cur]; used[cur] = True
    for _ in range(n-1):
        bx, by = cx0[cur], cy0[cur]
        best, bd = -1, 1e18
        for j in range(n):
            if used[j]: continue
            d = (bx-cx0[j])**2 + (by-cy0[j])**2
            if d < bd: bd, best = d, j
        tour.append(best); used[best] = True; cur = best

    N_SEG = 6
    stepp = 100.0 / max(n-1, 1)
    snake_stops, kf, cellrects = [], [], []
    for order_pos, j in enumerate(tour):
        wi, di, col, cx, cy, px, py = filled[j]
        pct = round(order_pos * stepp, 3)
        snake_stops.append(f'{pct}%{{transform:translate({cx:.0f}px,{cy:.0f}px)}}')
        p1 = round(min(max(pct, 0.3), 99.7), 3)
        p2 = round(min(p1 + 0.15, 99.85), 3)
        kf.append(f'@keyframes e{order_pos}{{0%,{p1}%{{opacity:1}}{p2}%,100%{{opacity:0}}}}')
        cellrects.append(f'<rect x="{px}" y="{py}" width="{cell}" height="{cell}" rx="2" fill="{col}" '
                         f'style="animation:e{order_pos} {DUR}s linear infinite"/>')
    kf.append('@keyframes snake{' + ''.join(snake_stops) + '}')
    add('<style>' + ''.join(kf) + '</style>')
    for r in cellrects:
        add(r)

    seg_dt = DUR / max(n-1, 1)
    for i in range(N_SEG):
        d = i * seg_dt
        anim = f'animation:snake {DUR}s linear infinite backwards;animation-delay:{d:.3f}s'
        if i == 0:
            add(f'<g style="{anim}">'
                f'<rect x="{-cell/2-2:.0f}" y="{-cell/2-2:.0f}" width="{cell+4}" height="{cell+4}" rx="4" fill="{NEON_CYAN}" opacity="0.35"/>'
                f'<rect x="{-cell/2:.0f}" y="{-cell/2:.0f}" width="{cell}" height="{cell}" rx="3" fill="{NEON_YELLOW}"/></g>')
        else:
            add(f'<g style="{anim}">'
                f'<rect x="{-cell/2:.0f}" y="{-cell/2:.0f}" width="{cell}" height="{cell}" rx="3" fill="{NEON_PINK}" opacity="{round(1-i*0.13,2)}"/></g>')

# ========== NOW ==========
heading(40, Y_NOW+42, "whoami", "--now")
lines = [
    ("\U0001F4BB", "Building fullstack apps with Vue, Node & Python"),
    ("\U0001F9EA", "Learning & experimenting with new tech daily"),
    ("\U0001F3A7", "Coding to synthwave beats"),
    ("\U0001F4E1", "Open to collabs — find me on GitHub!"),
]
yy3 = Y_NOW + 78
for ic, txt in lines:
    add(f'<text x="44" y="{yy3}" font-size="16">{ic}</text>')
    add(f'<text x="76" y="{yy3}" font-family="{MONO}" font-size="13.5" fill="{INK}">{esc(txt)}</text>')
    yy3 += 30

# ========== FOOTER ==========
bx, by, bw = 220, Y_FOOT+34, 260
seg = bw/10; filledn = int(0.82*10)
for i in range(10):
    if i < filledn:
        add(f'<rect x="{bx+i*seg+1:.0f}" y="{by}" width="{seg-3:.0f}" height="14" fill="{NEON_PINK}" '
            f'style="animation:flicker 1.5s ease-in-out infinite;animation-delay:-{i*0.12:.2f}s"/>')
    else:
        add(f'<rect x="{bx+i*seg+1:.0f}" y="{by}" width="{seg-3:.0f}" height="14" fill="#1a0a2e"/>')
add(f'<text x="{bx}" y="{by-6}" font-family="{MONO}" font-size="10" letter-spacing="2" fill="{MUTED}">POWER LEVEL: CODING</text>')
add(f'<text x="{bx+bw+10}" y="{by+12}" font-family="{MONO}" font-size="11" fill="{NEON_PINK}">82%</text>')
add(f'<text x="{bx+bw+48}" y="{by+12}" font-family="{MONO}" font-size="11" fill="{MUTED}">— ready</text>')

# Synthwave sun accent at footer
add(f'<circle cx="640" cy="{by+7}" r="20" fill="{NEON_YELLOW}" opacity="0.15"/>')
add(f'<rect x="625" y="{by+2}" width="30" height="2" fill="{NEON_PINK}" opacity="0.5"/>')
add(f'<rect x="625" y="{by+14}" width="30" height="2" fill="{NEON_CYAN}" opacity="0.5"/>')

add(f'<rect width="{W}" height="{H}" fill="url(#scan)"/>')
add(f'<rect x="1" y="1" width="{W-2}" height="{H-2}" fill="none" stroke="{NEON_PINK}" stroke-opacity="0.3" stroke-width="2" rx="4"/>')
add('</svg>')

open(OUTP, "w").write("\n".join(s))
print(f"wrote {OUTP} ({len(chr(10).join(s))} bytes) — {n} filled cells, {data['total']} contributions")
