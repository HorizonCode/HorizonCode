#!/usr/bin/env python3
"""Rework assets/profile.svg"""
import random
import math
import re
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

SVG_FILE = Path("assets/profile.svg")
src = SVG_FILE.read_text(encoding="utf-8")

def grab(pattern, name):
    m = re.search(pattern, src, re.S)
    if not m:
        raise ValueError(f"failed to extract: {name}")
    return m.group(0) if m.lastindex is None else m.group(1)

font_style = grab(r"<style>@font-face.*?</style>", "font style")
text_style = grab(r"<style>text\{.*?</style>", "text style")
banner_raw = grab(r'(<g clip-path="url\(#wipe\)" font-size="16" font-weight="700">.*?</g></g>)', "banner")
moon_raw   = grab(r'(<g opacity="\.22" font-size="14" fill="#e9e0f8">.*?</g></g>)', "moon starfield")
art        = grab(r'(<g clip-path="url\(#logoclip\)" font-size="5\.98">.*?\n</g>)', "ascii art")
shine_def  = grab(r'(<linearGradient id="shine".*?</linearGradient>)', "shine gradient")

# ---------------------------------------------------------------- matrix char-by-char reveal clips
rng_matrix = random.Random(20261015)

# Title Matrix Wipe Clip (Quetzalcoatl banner) - 88 discrete columns, 7 rows (step 16px)
title_rects = []
vals_title = ';'.join(str(h) for h in [0, 24, 40, 56, 72, 88, 104, 120, 150])
for c in range(88):
    x = 104.0 + c * 9.0
    wave_delay = 0.3 + (c / 88.0) * 1.5
    jitter = rng_matrix.uniform(-0.12, 0.12)
    start_t = max(0.2, wave_delay + jitter)
    dur = rng_matrix.uniform(0.32, 0.52)
    title_rects.append(
        f'<rect x="{x:.1f}" y="80" width="9.2" height="0">'
        f'<animate attributeName="height" values="{vals_title}" calcMode="discrete" '
        f'dur="{dur:.2f}s" begin="{start_t:.2f}s" fill="freeze"/>'
        f'</rect>'
    )
wipe_clip = '<clipPath id="wipe">\n' + '\n'.join(title_rects) + '\n</clipPath>'

# Lucoa Matrix Logo Clip - 114 discrete columns, step 3.5px, 87 rows (step 7px, total ~630px)
# 45 discrete steps snapping 2 character rows at a time
lucoa_rects = []
vals_lucoa = ';'.join(str(h) for h in range(0, 630, 14)) + ';640'
for c in range(114):
    x = 48.0 + c * 3.5
    cluster = (c * 7) % 23
    base_t = 1.6 + (cluster / 23.0) * 1.5 + rng_matrix.uniform(-0.08, 0.08)
    dur = rng_matrix.uniform(0.7, 1.15)
    lucoa_rects.append(
        f'<rect x="{x:.1f}" y="450" width="3.6" height="0">'
        f'<animate attributeName="height" values="{vals_lucoa}" calcMode="discrete" '
        f'dur="{dur:.2f}s" begin="{base_t:.2f}s" fill="freeze"/>'
        f'</rect>'
    )
logo_clip = '<clipPath id="logoclip">\n' + '\n'.join(lucoa_rects) + '\n</clipPath>'

W, H = 1600, 1000

# ---------------------------------------------------------------- fastfetch info lines
BIRTH_DATE = date(1999, 1, 6)
today = date.today()
age = today.year - BIRTH_DATE.year - ((today.month, today.day) < (BIRTH_DATE.month, BIRTH_DATE.day))

INFO_DATA = [
    ("4.00s", "Alias", "Quetzalcoatl (HorizonCode, Horizon)", "#fbcfe8"),
    ("4.20s", "Species", "feathered dragon, sun-kissed", "#f472b6"),
    ("4.40s", "Role", "Full-stack developer", "#e2e8f0"),
    ("4.60s", "Uptime", f"{age} years (since 1999)", "#e2e8f0"),
    ("4.80s", "Den", "Germany", "#e2e8f0"),
    ("5.00s", "Stack", "TypeScript, Svelte, SvelteKit", "#e2e8f0"),
    ("5.20s", "Running", "EZPPFarm, osu.direct", "#e2e8f0"),
    ("5.40s", "Comfy with", "SvelteKit", "#e2e8f0"),
    ("5.60s", "Scene", "osu! tooling", "#e2e8f0"),
    ("5.80s", "Hobbies", "sunbathing, side quests", "#c084fc"),
    ("6.00s", "Mood", "chill dragon energy", "#c084fc"),
    ("6.20s", "Known bug", "starts > finishes", "#fb7185"),
    ("6.40s", "Web", "horizonco.de", "#e2e8f0"),
]

new_info = []
for i, (begin, label, val, val_color) in enumerate(INFO_DATA):
    y = 406 + i * 29
    line = (
        f'<g opacity="0">'
        f'<animate attributeName="opacity" from="0" to="1" begin="{begin}" dur=".4s" fill="freeze"/>'
        f'<text x="690" y="{y}" font-size="14">'
        f'<tspan fill="#f43f5e" opacity=".9">♥ </tspan>'
        f'<tspan fill="#c084fc" font-weight="700">{label}</tspan>'
        f'<tspan fill="#8b949e">: </tspan>'
        f'<tspan fill="{val_color}">{val}</tspan>'
        f'</text></g>'
    )
    new_info.append(line)
info_block = "\n".join(new_info)

# ---------------------------------------------------------------- gothic falling rose petals
rng = random.Random(20261015)
petals = []
petal_colors = ["#4c0519", "#881337", "#9f1239", "#be185d", "#e11d48", "#581c87", "#7c3aed"]
for i in range(18):
    px = rng.uniform(60, 1540)
    py = rng.uniform(-100, 200)
    scale = rng.uniform(0.6, 1.2)
    dur = rng.uniform(10.0, 18.0)
    delay = rng.uniform(0.0, 8.0)
    dx = rng.uniform(-60, 60)
    rot = rng.uniform(120, 360)
    color = rng.choice(petal_colors)
    opacity = rng.uniform(0.35, 0.75)
    
    petals.append(
        f'<g transform="translate({px:.0f} {py:.0f})">'
        f'<animateTransform attributeName="transform" type="translate" '
        f'values="{px:.0f} -40; {px + dx * 0.5:.0f} 480; {px + dx:.0f} 1040" '
        f'dur="{dur:.1f}s" begin="{delay:.1f}s" repeatCount="indefinite"/>'
        f'<path d="M0,0 C3,-5 9,-7 13,-3 C15,2 11,8 6,10 C1,11 -2,7 0,0 Z" '
        f'fill="{color}" opacity="{opacity:.2f}" transform="scale({scale:.2f})">'
        f'<animateTransform attributeName="transform" type="rotate" values="0; {rot:.0f}" dur="{dur * 0.7:.1f}s" repeatCount="indefinite"/>'
        f'</path></g>'
    )
petal_block = "\n".join(petals)

# ---------------------------------------------------------------- gothic sparkles & twilight runes
twinkles = []
runes = ["✦", "✧", "⋆", "₊", "⊹", "·", "†", "⛤"]
for _ in range(24):
    tx = rng.uniform(50, 1550)
    ty = rng.uniform(40, 960)
    dur = rng.uniform(3.0, 6.5)
    delay = rng.uniform(0.0, 4.0)
    rune = rng.choice(runes)
    color = rng.choice(["#e9d5ff", "#c084fc", "#f472b6", "#a855f7", "#fda4af"])
    twinkles.append(
        f'<text x="{tx:.0f}" y="{ty:.0f}" font-size="{rng.uniform(10, 15):.0f}" fill="{color}" opacity=".6">'
        f'{rune}<animate attributeName="opacity" values=".15;.85;.15" dur="{dur:.1f}s" begin="{delay:.1f}s" repeatCount="indefinite"/>'
        f'</text>'
    )
twinkle_block = "\n".join(twinkles)

# ---------------------------------------------------------------- corner gothic roses with thorn filigree
def corner_gothic_rose(x, y, flip_x=1, flip_y=1):
    return (
        f'<g transform="translate({x} {y}) scale({flip_x * 1.6} {flip_y * 1.6})">'
        # Dark thorn bramble branches
        f'<path d="M-10,-5 C-25,-2 0,-30 -8,-45 C-12,-38 -20,-32 -28,-36" fill="none" stroke="#251a2d" stroke-width="2" stroke-linecap="round"/>'
        f'<path d="M-14,-22 L-19,-26 L-15,-20 Z" fill="#3b1d44"/>' # thorn
        f'<path d="M-6,-35 L-2,-40 L-4,-34 Z" fill="#3b1d44"/>'  # thorn
        # Emerald leaves
        f'<use href="#leaf" transform="translate(-16 10) rotate(145)"/>'
        f'<use href="#leaf" transform="translate(15 12) rotate(35)"/>'
        f'<use href="#leaf" transform="translate(-8 -18) rotate(220) scale(0.8)"/>'
        # Layered Black Baccara Rose
        f'<use href="#gothicRose"/>'
        f'<circle cx="0" cy="-18" r="2.2" fill="#c084fc">'
        f'<animate attributeName="opacity" values=".4;.95;.4" dur="3.2s" repeatCount="indefinite"/></circle>'
        f'</g>'
    )

corner_decorations = (
    corner_gothic_rose(48, 48, 1, 1) +
    corner_gothic_rose(1552, 48, -1, 1) +
    corner_gothic_rose(48, 952, 1, -1) +
    corner_gothic_rose(1552, 952, -1, -1)
)

# ---------------------------------------------------------------- climbing rose vine (removed per user request)
vine = ""

# ---------------------------------------------------------------- bats with glowing crimson eyes
def flying_gothic_bat(x, y, s, dur, phase):
    return (
        f'<g><animateTransform attributeName="transform" type="translate" '
        f'values="{x} {y}; {x + 24} {y - 14}; {x + 6} {y - 4}; {x - 20} {y - 12}; {x} {y}" '
        f'dur="{dur}s" begin="{phase}s" repeatCount="indefinite"/>'
        f'<g transform="translate({x} {y}) scale({s})"><use href="#bat"/>'
        f'<animateTransform attributeName="transform" type="rotate" '
        f'values="-8 0 0;8 0 0;-8 0 0" dur="{dur / 2:.1f}s" begin="{phase}s" repeatCount="indefinite"/>'
        f'</g></g>'
    )

bats = flying_gothic_bat(1180, 110, 1.15, 11, 0) + flying_gothic_bat(230, 140, .9, 13, 1.8)

# ---------------------------------------------------------------- flying dragon with Lucoa hair gradient
stops_dragon = [
    (0.00, '#58a6ff'), # sky blue tail tip
    (0.22, '#22d3ee'), # turquoise / cyan
    (0.50, '#34d399'), # mint / green
    (0.78, '#a3e635'), # lime / chartreuse
    (1.00, '#ffe66d'), # golden blonde head
]

def hex_to_rgb(h):
    h = h.lstrip('#')
    return [int(h[i:i+2], 16) for i in (0, 2, 4)]

def rgb_to_hex(rgb):
    return '#' + ''.join(f'{int(round(c)):02x}' for c in rgb)

def get_dragon_color(t):
    for i in range(len(stops_dragon) - 1):
        t0, c0 = stops_dragon[i]
        t1, c1 = stops_dragon[i+1]
        if t0 <= t <= t1:
            local_t = (t - t0) / (t1 - t0)
            rgb0 = hex_to_rgb(c0)
            rgb1 = hex_to_rgb(c1)
            rgb = [rgb0[j] + local_t * (rgb1[j] - rgb0[j]) for j in range(3)]
            return rgb_to_hex(rgb)
    return stops_dragon[-1][1]

dragon_chars = '.' * 5 + ':' * 5 + '-' * 4 + '=' * 5 + '+' * 5 + '*' * 4 + '#' * 5 + '%' * 5
trail_parts = []
for i, c in enumerate(dragon_chars):
    t = i / (len(dragon_chars) - 1)
    sz = 8.0 + 9.0 * t
    col = get_dragon_color(t)
    trail_parts.append(f'<tspan font-size="{sz:.1f}" fill="{col}">{c}</tspan>')

trail = "".join(trail_parts)

# ---------------------------------------------------------------- gothic studs along borders
studs = []
stud_coords  = [(x, 14) for x in (80, 240, 420, 600, 1000, 1180, 1360, 1520)]
stud_coords += [(x, 986) for x in (80, 240, 420, 600, 780, 960, 1140, 1320, 1520)]
stud_coords += [(14, y) for y in (160, 320, 480, 640, 800)]
stud_coords += [(1586, y) for y in (160, 320, 480, 640, 800)]
for i, (x, y) in enumerate(stud_coords):
    color = "#881337" if i % 2 == 0 else "#4c1d95"
    glow = "#f43f5e" if i % 2 == 0 else "#c084fc"
    anim = f'<animate attributeName="fill" values="{color};{glow};{color}" dur="{3.0 + (i % 4) * 0.8:.1f}s" begin="{i * 0.15:.1f}s" repeatCount="indefinite"/>'
    studs.append(
        f'<g transform="translate({x} {y}) scale(1.1)">'
        f'<use href="#heart" fill="{color}" opacity=".85">{anim}</use>'
        f'</g>'
    )
stud_block = "\n".join(studs)

# ---------------------------------------------------------------- typing clip values
typed_vals = ";".join(str(i * 8.8) for i in range(11)) + ";200"

# ---------------------------------------------------------------- full assembled SVG
svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="HorizonCode profile: a cute dragon girl inside an ornate gothic rose terminal window">
{font_style}
<defs>
  <!-- Base Heart Marker -->
  <path id="heart" d="M0,-3.2C-0.9,-5.4 -3.2,-5.9 -4.6,-4.5C-6.2,-2.9 -6.2,-0.9 -4.8,0.5L0,5L4.8,0.5C6.2,-0.9 6.2,-2.9 4.6,-4.5C3.2,-5.9 0.9,-5.4 0,-3.2Z"/>

  <!-- Ornate Multi-Petal Gothic Rose -->
  <g id="gothicRose">
    <!-- Outer Deep Velvet Petals -->
    <g fill="#2e021f" stroke="#170110" stroke-width=".5">
      <ellipse cx="0" cy="-12" rx="7.2" ry="9.4"/>
      <ellipse cx="11.4" cy="-3.7" rx="7.2" ry="9.4" transform="rotate(72)"/>
      <ellipse cx="7.1" cy="9.8" rx="7.2" ry="9.4" transform="rotate(144)"/>
      <ellipse cx="-7.1" cy="9.8" rx="7.2" ry="9.4" transform="rotate(216)"/>
      <ellipse cx="-11.4" cy="-3.7" rx="7.2" ry="9.4" transform="rotate(288)"/>
    </g>
    <!-- Mid Wine-Crimson Petals -->
    <g fill="#831843" stroke="#4c0519" stroke-width=".4">
      <ellipse cx="0" cy="-7.5" rx="5.2" ry="6.8" transform="rotate(36)"/>
      <ellipse cx="0" cy="-7.5" rx="5.2" ry="6.8" transform="rotate(108)"/>
      <ellipse cx="0" cy="-7.5" rx="5.2" ry="6.8" transform="rotate(180)"/>
      <ellipse cx="0" cy="-7.5" rx="5.2" ry="6.8" transform="rotate(252)"/>
      <ellipse cx="0" cy="-7.5" rx="5.2" ry="6.8" transform="rotate(324)"/>
    </g>
    <!-- Inner Radiant Crimson Core -->
    <g fill="#be185d">
      <ellipse cx="0" cy="-4" rx="3.4" ry="4.4" transform="rotate(18)"/>
      <ellipse cx="0" cy="-4" rx="3.4" ry="4.4" transform="rotate(90)"/>
      <ellipse cx="0" cy="-4" rx="3.4" ry="4.4" transform="rotate(162)"/>
      <ellipse cx="0" cy="-4" rx="3.4" ry="4.4" transform="rotate(234)"/>
      <ellipse cx="0" cy="-4" rx="3.4" ry="4.4" transform="rotate(306)"/>
    </g>
    <circle cx="0" cy="0" r="3.2" fill="#f43f5e"/>
    <path d="M 2.6,0.5 A 2.6,2.6 0 1 1 -1.5,-1.8 A 1.6,1.6 0 1 0 1.2,1.3 A 0.8,0.8 0 1 1 -0.3,-0.3"
          fill="none" stroke="#ffe4e6" stroke-width=".7" stroke-linecap="round"/>
    <circle cx="-0.9" cy="-0.9" r=".6" fill="#fff" opacity=".9"/>
  </g>

  <!-- Emerald Thorn Leaf -->
  <g id="leaf">
    <path d="M0,0 C3.5,-5.2 10.5,-6.8 15,-2.8 C11.8,3.2 4.5,5.1 0,0 Z" fill="#2d3a28" stroke="#182215" stroke-width=".7"/>
    <path d="M1.5,-.3 C5.5,-1.8 10.5,-2.6 14,-2.4" fill="none" stroke="#465c3e" stroke-width=".7"/>
  </g>

  <!-- Gothic Bat with Ruby Eyes -->
  <g id="bat">
    <path d="M0,-3 C-3.6,-9 -10,-10.5 -14,-6.5 C-11.4,-6.2 -9.4,-4.4 -8.4,-1.4 C-6.6,-5.4 -3.2,-6 0,-3.6 Z" fill="#140a20" stroke="#7c3aed" stroke-width=".6" stroke-opacity=".55"/>
    <path d="M0,-3 C3.6,-9 10,-10.5 14,-6.5 C11.4,-6.2 9.4,-4.4 8.4,-1.4 C6.6,-5.4 3.2,-6 0,-3.6 Z" fill="#140a20" stroke="#7c3aed" stroke-width=".6" stroke-opacity=".55"/>
    <ellipse cx="0" cy="-1.6" rx="2.3" ry="3.1" fill="#140a20" stroke="#7c3aed" stroke-width=".6" stroke-opacity=".55"/>
    <path d="M-1.8,-4.4 L-2.4,-7 L-0.5,-5 Z M1.8,-4.4 L2.4,-7 L0.5,-5 Z" fill="#140a20"/>
    <circle cx="-.9" cy="-2.4" r=".5" fill="#f43f5e"/>
    <circle cx=".9" cy="-2.4" r=".5" fill="#f43f5e"/>
  </g>

  <!-- Background Gradients -->
  <linearGradient id="page" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="0" y2="{H}">
    <stop offset="0" stop-color="#040207"/>
    <stop offset=".22" stop-color="#0c0517"/>
    <stop offset=".45" stop-color="#160829"/>
    <stop offset=".62" stop-color="#1e0938"/>
    <stop offset=".85" stop-color="#100520"/>
    <stop offset="1" stop-color="#06020a"/>
  </linearGradient>

  <!-- Ornate Gothic Metallic Frame -->
  <linearGradient id="frame" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="{H}">
    <stop offset="0" stop-color="#c084fc"/>
    <stop offset=".25" stop-color="#7c3aed"/>
    <stop offset=".5" stop-color="#9f1239"/>
    <stop offset=".75" stop-color="#4c1d95"/>
    <stop offset="1" stop-color="#e879f9"/>
  </linearGradient>

  <!-- Quetzalcoatl Halftone Banner (Lucoa Hair Gradient) -->
  <linearGradient id="tg" gradientUnits="userSpaceOnUse" x1="104" y1="0" x2="896" y2="0">
    <stop offset="0" stop-color="#ffe66d"/>
    <stop offset=".28" stop-color="#a3e635"/>
    <stop offset=".65" stop-color="#22d3ee"/>
    <stop offset="1" stop-color="#58a6ff"/>
  </linearGradient>

  {shine_def}

  <!-- Mist Horizontal Gradient -->
  <linearGradient id="hz" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="{W}" y2="0">
    <stop offset="0" stop-color="#7c3aed" stop-opacity="0"/>
    <stop offset=".35" stop-color="#c084fc" stop-opacity=".7"/>
    <stop offset=".5" stop-color="#f43f5e" stop-opacity=".8"/>
    <stop offset=".65" stop-color="#a855f7" stop-opacity=".7"/>
    <stop offset="1" stop-color="#7c3aed" stop-opacity="0"/>
  </linearGradient>

  <!-- Gothic Rose Moon Glows -->
  <radialGradient id="moonGlow">
    <stop offset="0" stop-color="#e9d5ff" stop-opacity=".18"/>
    <stop offset=".4" stop-color="#c084fc" stop-opacity=".08"/>
    <stop offset="1" stop-color="#7c3aed" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="bloodCorona">
    <stop offset="0" stop-color="#f43f5e" stop-opacity=".14"/>
    <stop offset=".5" stop-color="#9f1239" stop-opacity=".05"/>
    <stop offset="1" stop-color="#9f1239" stop-opacity="0"/>
  </radialGradient>
  <radialGradient id="wineGlow">
    <stop offset="0" stop-color="#7c3aed" stop-opacity=".25"/>
    <stop offset=".5" stop-color="#4c1d95" stop-opacity=".12"/>
    <stop offset="1" stop-color="#4c1d95" stop-opacity="0"/>
  </radialGradient>

  <!-- Clips & Paths -->
  <clipPath id="card"><rect width="{W}" height="{H}" rx="24"/></clipPath>
  {wipe_clip}
  {logo_clip}
  <clipPath id="typed"><rect x="724" y="362" width="0" height="24"><animate attributeName="width" values="{typed_vals}" dur="0.8s" calcMode="discrete" fill="freeze" begin="2.0s"/></rect></clipPath>
  <path id="glide" d="M -60,202 C 140,180 340,224 560,202 S 940,180 1160,202 S 1480,224 1720,200"/>
</defs>
{text_style}

<!-- Card Canvas -->
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="24" fill="url(#page)" stroke="url(#frame)" stroke-width="2.2"/>

<g clip-path="url(#card)">
  <!-- Ethereal Moon Aura & Glow Spheres -->
  <ellipse cx="290" cy="530" rx="390" ry="390" fill="url(#moonGlow)"/>
  <ellipse cx="290" cy="530" rx="440" ry="440" fill="url(#bloodCorona)"/>
  <ellipse cx="1150" cy="1010" rx="640" ry="340" fill="url(#wineGlow)"/>

  <!-- Ornate Inner Tracery Border -->
  <rect x="10" y="10" width="{W - 20}" height="{H - 20}" rx="18" fill="none" stroke="#7c3aed" stroke-opacity=".35" stroke-width="1.8"/>
  <rect x="15" y="15" width="{W - 30}" height="{H - 30}" rx="15" fill="none" stroke="#c084fc" stroke-opacity=".18" stroke-width="1" stroke-dasharray="2 10" stroke-linecap="round"/>

  <!-- Falling Gothic Rose Petals & Atmospheric Twinkles -->
{twinkle_block}
{petal_block}

  <!-- Moon Starfield Sphere -->
  <g transform="translate(-200 202)">
{moon_raw}
  </g>

  <!-- Floating Ambient Hearts -->
  <g opacity="0.65">
    <text x="326" y="820" font-size="13" fill="#f472b6">&#9825;<animate attributeName="opacity" values=".15;.85;.15" dur="6.2s" repeatCount="indefinite"/></text>
    <text x="182" y="615" font-size="13" fill="#c084fc">&#9825;<animate attributeName="opacity" values=".15;.85;.15" dur="6.4s" repeatCount="indefinite"/></text>
    <text x="442" y="753" font-size="13" fill="#fb7185">&#9825;<animate attributeName="opacity" values=".15;.85;.15" dur="5.1s" repeatCount="indefinite"/></text>
    <text x="290" y="585" font-size="13" fill="#d8b4fe">&#9825;<animate attributeName="opacity" values=".15;.85;.15" dur="6.2s" repeatCount="indefinite"/></text>
    <text x="417" y="430" font-size="13" fill="#c084fc">&#9825;<animate attributeName="opacity" values=".15;.85;.15" dur="4.4s" repeatCount="indefinite"/></text>
    <text x="293" y="551" font-size="13" fill="#f43f5e">&#9825;<animate attributeName="opacity" values=".15;.85;.15" dur="5.4s" repeatCount="indefinite"/></text>
    <text x="340" y="675" font-size="13" fill="#e879f9">&#9825;<animate attributeName="opacity" values=".15;.85;.15" dur="6.6s" repeatCount="indefinite"/></text>
    <text x="222" y="426" font-size="13" fill="#e9d5ff">&#9825;<animate attributeName="opacity" values=".15;.85;.15" dur="5.2s" repeatCount="indefinite"/></text>
  </g>

  <!-- Complete, Non-Seethrough Lucoa ASCII Art -->
  <g transform="translate(34.4 -204.7) scale(1.02)">
{art}
  </g>

  <!-- Halftone Quetzalcoatl Banner (Lucoa Hair Gradient) -->
  <g transform="translate(304.5 -36)">
{banner_raw}
  </g>

  <!-- Flying Feathered Dragon (Lucoa Hair Gradient) below Quetzalcoatl Banner -->
  <text font-weight="700"><textPath href="#glide" startOffset="520">{trail}<tspan font-size="22" fill="#ffe66d">@</tspan><tspan font-size="14" fill="#ef476f">&gt;</tspan><animate attributeName="startOffset" from="-520" to="1780" dur="15s" repeatCount="indefinite"/></textPath></text>

  <!-- Gothic Subtitle -->
  <text x="800" y="250" text-anchor="middle" font-size="14.5" fill="#e9d5ff" letter-spacing="1.8" opacity="0">
    <animate attributeName="opacity" from="0" to="1" begin="1.8s" dur=".9s" fill="freeze"/>
    ~ a cute dragon girl <tspan fill="#f43f5e">♥</tspan> // HorizonCode // full-stack since 2014 ~<tspan fill="#c084fc">_<animate attributeName="fill-opacity" values="1;0;1" dur="1.1s" repeatCount="indefinite"/></tspan>
  </text>

  <!-- ==================== GOTHIC TERMINAL FASTFETCH WINDOW ==================== -->
  <g transform="translate(0 0)">
    <!-- Terminal Window Glass Pane -->
    <rect x="662" y="292" width="876" height="620" rx="14" fill="#090412" fill-opacity="0.75" stroke="#7c3aed" stroke-opacity="0.38" stroke-width="1.4"/>
    <rect x="662" y="292" width="876" height="32" rx="14" fill="#140622" fill-opacity="0.9"/>
    <rect x="662" y="316" width="876" height="8" fill="#140622" fill-opacity="0.9"/>
    
    <!-- Gothic Terminal Window Buttons (Jeweled Roses) -->
    <circle cx="682" cy="308" r="5.5" fill="#f43f5e" stroke="#9f1239" stroke-width="1"><animate attributeName="opacity" values=".75;1;.75" dur="3s" repeatCount="indefinite"/></circle>
    <circle cx="680.5" cy="306.5" r="1.5" fill="#fff" opacity=".8"/>
    <circle cx="700" cy="308" r="5.5" fill="#f59e0b" stroke="#b45309" stroke-width="1"/>
    <circle cx="698.5" cy="306.5" r="1.5" fill="#fff" opacity=".8"/>
    <circle cx="718" cy="308" r="5.5" fill="#c084fc" stroke="#7c3aed" stroke-width="1"><animate attributeName="opacity" values=".75;1;.75" dur="3s" begin="1.5s" repeatCount="indefinite"/></circle>
    <circle cx="716.5" cy="306.5" r="1.5" fill="#fff" opacity=".8"/>

    <!-- Kitty Tab Bar -->
    <rect x="736" y="296" width="162" height="24" rx="5" fill="#1e0a33" stroke="#7c3aed" stroke-width="1"/>
    <text x="746" y="312" font-size="12" fill="#e9d5ff" font-weight="700">🐱 1: fish <tspan fill="#f43f5e">♥</tspan></text>
    <text x="884" y="312" font-size="12" fill="#71717a">×</text>
    <rect x="906" y="296" width="24" height="24" rx="5" fill="#120422" stroke="#4c1d95" stroke-width="0.8"/>
    <text x="918" y="312" text-anchor="middle" font-size="13" fill="#a78bfa">+</text>
    <text x="1512" y="312" text-anchor="end" font-size="11.5" fill="#a78bfa" letter-spacing="1"><tspan fill="#c084fc">horizon@dragon-den:~</tspan></text>

    <!-- Starship Prompt (fastfetch execution) -->
    <text x="690" y="352" font-size="14"><tspan fill="#7c3aed">╭─ </tspan><tspan fill="#4ade80" font-weight="700">🐱 horizon</tspan><tspan fill="#8b949e"> at </tspan><tspan fill="#c084fc">dragon-den</tspan><tspan fill="#8b949e"> in </tspan><tspan fill="#38bdf8" font-weight="700">📁 ~</tspan><tspan fill="#8b949e"> on git:(</tspan><tspan fill="#f472b6" font-weight="700">main</tspan><tspan fill="#8b949e">)</tspan><tspan fill="#22c55e"> [⇡]</tspan><tspan fill="#8b949e"> via </tspan><tspan fill="#fb923c" font-weight="700">🐟 fish</tspan></text>
    <text x="690" y="376" font-size="14.5"><tspan fill="#7c3aed">╰─</tspan><tspan fill="#4ade80" font-weight="700">❯ </tspan><tspan fill="#f1f5f9" clip-path="url(#typed)">fastfetch</tspan></text>

    <!-- Fastfetch Info Lines -->
{info_block}

    <!-- Gothic Heart Palette Blocks -->
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="7.0s" dur=".5s" fill="freeze"/>
      <g transform="translate(696 788) scale(1.25)">
        <g transform="translate(0 0)"><use href="#heart" fill="#4c0519"><animateTransform attributeName="transform" type="scale" values="1.15;1.3;1.15" dur="2.2s" begin="0.00s" repeatCount="indefinite"/></use></g>
        <g transform="translate(38 0)"><use href="#heart" fill="#881337"><animateTransform attributeName="transform" type="scale" values="1.15;1.3;1.15" dur="2.2s" begin="0.18s" repeatCount="indefinite"/></use></g>
        <g transform="translate(76 0)"><use href="#heart" fill="#be185d"><animateTransform attributeName="transform" type="scale" values="1.15;1.3;1.15" dur="2.2s" begin="0.36s" repeatCount="indefinite"/></use></g>
        <g transform="translate(114 0)"><use href="#heart" fill="#f43f5e"><animateTransform attributeName="transform" type="scale" values="1.15;1.3;1.15" dur="2.2s" begin="0.54s" repeatCount="indefinite"/></use></g>
        <g transform="translate(152 0)"><use href="#heart" fill="#581c87"><animateTransform attributeName="transform" type="scale" values="1.15;1.3;1.15" dur="2.2s" begin="0.72s" repeatCount="indefinite"/></use></g>
        <g transform="translate(190 0)"><use href="#heart" fill="#7c3aed"><animateTransform attributeName="transform" type="scale" values="1.15;1.3;1.15" dur="2.2s" begin="0.90s" repeatCount="indefinite"/></use></g>
        <g transform="translate(228 0)"><use href="#heart" fill="#c084fc"><animateTransform attributeName="transform" type="scale" values="1.15;1.3;1.15" dur="2.2s" begin="1.08s" repeatCount="indefinite"/></use></g>
        <g transform="translate(266 0)"><use href="#heart" fill="#e9d5ff"><animateTransform attributeName="transform" type="scale" values="1.15;1.3;1.15" dur="2.2s" begin="1.26s" repeatCount="indefinite"/></use></g>
      </g>
    </g>

    <!-- Waves line -->
    <g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="7.4s" dur=".5s" fill="freeze"/>
      <text x="690" y="822" font-size="13.5" fill="#d8b4fe" letter-spacing="1">*waves at you* <tspan fill="#f43f5e">♥</tspan></text>
    </g>

    <!-- Active Starship Return Prompt with Blinking Cursor and Right Status -->
    <g opacity="0"><set attributeName="opacity" to="1" begin="7.9s"/>
      <text x="690" y="852" font-size="14"><tspan fill="#7c3aed">╭─ </tspan><tspan fill="#4ade80" font-weight="700">🐱 horizon</tspan><tspan fill="#8b949e"> at </tspan><tspan fill="#c084fc">dragon-den</tspan><tspan fill="#8b949e"> in </tspan><tspan fill="#38bdf8" font-weight="700">📁 ~</tspan><tspan fill="#8b949e"> on git:(</tspan><tspan fill="#f472b6" font-weight="700">main</tspan><tspan fill="#8b949e">)</tspan><tspan fill="#22c55e"> [⇡]</tspan><tspan fill="#8b949e"> via </tspan><tspan fill="#fb923c" font-weight="700">🐟 fish</tspan></text>
      <text x="1512" y="852" font-size="13" text-anchor="end" fill="#fb7185">⏱ 18ms</text>
      <text x="690" y="878" font-size="14.5"><tspan fill="#7c3aed">╰─</tspan><tspan fill="#4ade80" font-weight="700">❯ </tspan></text>
      <rect x="726" y="864" width="8.5" height="15" fill="#f1f5f9"><animate attributeName="opacity" values="1;0" calcMode="discrete" dur="1.1s" repeatCount="indefinite"/></rect>
      <text x="1512" y="878" font-size="13" text-anchor="end" letter-spacing="1"><tspan fill="#c084fc">~ a dragon girl, haunting the horizon </tspan><tspan fill="#f43f5e">♥</tspan><tspan fill="#c084fc"> ~</tspan></text>
    </g>
  </g>

  <!-- Ground Mist & Fog Runes -->
  <g font-size="12" fill="url(#hz)" opacity=".55">
    <text x="0" y="924">{"· " * 160}</text>
  </g>
  <g font-size="12" fill="url(#hz)" opacity=".3">
    <text x="5" y="938">{"· " * 160}</text>
  </g>

  <!-- Fluttering Gothic Bats -->
{bats}

  <!-- Border Heart Studs & Corner Gothic Roses -->
{stud_block}
{corner_decorations}

  <!-- ==================== GOTHIC WINDOW HEADER CREST ==================== -->
  <g opacity="0"><animate attributeName="opacity" from="0" to="1" begin="1.2s" dur=".8s" fill="freeze"/>
    <!-- Gothic Titleplate Arch -->
    <path d="M600,6 L1000,6 C1000,6 990,38 970,38 L630,38 C610,38 600,6 600,6 Z" fill="#0d0418" stroke="url(#frame)" stroke-width="1.6"/>
    <!-- Jeweled Filigree Accents -->
    <circle cx="616" cy="22" r="3" fill="#f43f5e"/>
    <circle cx="984" cy="22" r="3" fill="#f43f5e"/>
    <text x="800" y="27" text-anchor="middle" font-size="13" letter-spacing="2.2" fill="#f1f5f9">
      <tspan fill="#f43f5e">♰</tspan> <tspan fill="#c084fc">DRAGON'S DEN</tspan> <tspan fill="#8b7ba0">::</tspan> <tspan fill="#e9d5ff">kitty</tspan> <tspan fill="#f43f5e">♰</tspan>
    </text>
  </g>
</g>
</svg>
"""

SVG_FILE.write_text(svg, encoding="utf-8")
ET.fromstring(svg)
print(f"Successfully generated gothic card: {SVG_FILE} ({len(svg)} bytes), XML valid!")
