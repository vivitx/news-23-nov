"""Draw the 23 November 2026 world-news image (1024x1024) — v1.

Follows the v13 rank-3 formula (proven on 21 and 22 Nov): all-flat,
no AI photos; flat graphic + big number INSIDE the graphic + kicker +
headline + 1-line deck + sources per story. Masthead naming the day
and date. Region colour-coding consistent. Legible at ~300px.

Content: ~/workspace/makefun/news-20261123/content-2026-11-23.md
(triangulated from 8 mature Monday entries). Every story/number here
comes from that file; nothing invented.

Layout (mirrors 22 Nov): top strip + masthead + deck, UTC strip, stat
strip, region bar, 3 leads, 10 mediums (2 rows of 5), map + briefs
(32 briefs, 2 cols x 16), DATE CHECK box, no separate footer line
(the wires note lives in the DATE CHECK title line).

Number agreement (audited against the content file):
- Dymer: 11 killed + 14 missing everywhere (lead graphic, lead deck,
  stat strip, timeline 03:28 rescue).
- Cikande factory fire: 24 dead + ~30 missing everywhere (medium 6
  graphic/deck, UTC strip 00:00).
- COP31: 194 delegations; Hormuz: 2 tankers, 22 attacks in Nov,
  Brent $92.29; House: 258 seats; Nasdaq -10%, TAIEX -17.5%;
  Vanuatu M6.5, 601 km deep; EDITH 700,000 women; FIFA 48 teams,
  104 matches; Liverpool 4-0; NATO 3 Kh-101; Geneva 128 states.

Run: python3 draw_v1.py  ->  writes entry_v1.png + entry_v1-300.png.
Deterministic: fixed colours, fixed layout, no timestamps, no network.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "news-20261121", "bot"))

from PIL import Image, ImageDraw

from draw import (f, fs, text, headline, wrap, PAPER, INK, RED, GREEN,
                  BLUE, LIGHT, GOLD, flame, starburst, CONTINENTS,
                  quake_line, robot)
from draw_v11 import card_sq

W, H = 1024, 1024

ME, EU, AM, AF, SA, EA, SEA, OC, GL = ((190, 50, 45), (50, 90, 160),
                                       (50, 130, 80), (210, 130, 40),
                                       (140, 80, 170), (40, 150, 160),
                                       (180, 140, 30), (40, 60, 120),
                                       (110, 110, 110))
GREY = (120, 116, 104)


def kicker_bar_pill(d, x, y, w, num, label, col, pill, pill_col,
                    h=16, fsize=9):
    """v13 kicker bar, pill text/colour per-story."""
    d.rectangle([x, y, x + w, y + h], fill=col)
    text(d, x + 6, y + (h - 11) // 2 + 1, "%d %s" % (num, label),
         f(fsize, True), fill=LIGHT)
    pw = len(pill) * 5 + 10
    px = x + w - 6 - pw
    py = y + (h - 11) // 2
    d.rounded_rectangle([px, py, px + pw, py + 11], radius=2, fill=pill_col)
    text(d, px + pw / 2, py + 1, pill, f(7, True), fill=LIGHT, anchor="ma")


# ---------------------------------------------------------------- leads

def cop_v1(d, x, iy):
    """COP31 lead graphic (308x100): green COP31 block + big 194
    delegations, NO FOSSIL FUELS, 1.5C overshoot, collapse since 2009."""
    d.rectangle([x + 8, iy, x + 316, iy + 100], fill=(238, 244, 238))
    d.rectangle([x + 8, iy + 8, x + 118, iy + 52], fill=(0, 120, 80))
    text(d, x + 63, iy + 11, "COP31", fs(20), fill=LIGHT, anchor="ma")
    text(d, x + 63, iy + 37, "ANTALYA \u00b7 UN CLIMATE", f(7, True),
         fill=LIGHT, anchor="ma")
    d.rectangle([x + 128, iy + 8, x + 308, iy + 52], fill=(20, 33, 61))
    text(d, x + 136, iy + 10, "194", fs(26), fill=LIGHT)
    text(d, x + 136, iy + 38, "DELEGATIONS", f(9, True), fill=LIGHT)
    text(d, x + 8, iy + 60, "NO FOSSIL FUELS", fs(15), fill=RED)
    text(d, x + 8, iy + 80,
         "1.5\u00b0C overshoot confirmed \u00b7 first collapse since 2009",
         f(9))


def hormuz_v1(d, x, iy):
    """Hormuz lead graphic (308x100): flat Strait, two tankers ablaze,
    big 2 TANKERS HIT, 22 attacks in November, IRGC CLAIM chip."""
    x0, y0, x1, y1 = x + 8, iy, x + 316, iy + 100
    SEA = (58, 118, 170)
    LAND = (214, 196, 158)
    LANDTXT = (96, 84, 60)
    d.rectangle([x0, y0, x1, y1], fill=SEA)
    d.polygon([(x0, y0), (x1, y0), (x1, y0 + 30), (x0 + 265, y0 + 32),
               (x0 + 235, y0 + 36), (x0 + 180, y0 + 40), (x0 + 100, y0 + 42),
               (x0 + 40, y0 + 40), (x0, y0 + 36)], fill=LAND)
    d.polygon([(x0, y1), (x1, y1), (x1, y1 - 18), (x0 + 265, y1 - 38),
               (x0 + 235, y1 - 52), (x0 + 180, y1 - 36), (x0 + 100, y1 - 28),
               (x0 + 40, y1 - 22), (x0, y1 - 24)], fill=LAND)
    text(d, x0 + 14, y0 + 8, "IRAN", f(10, True), fill=LANDTXT)
    text(d, x0 + 14, y1 - 16, "ARABIA", f(9, True), fill=LANDTXT)
    # tanker 1 (upper) and tanker 2 (lower), both burning
    for (tx, ty) in [(x0 + 95, y0 + 52), (x0 + 175, y0 + 66)]:
        d.polygon([(tx - 26, ty), (tx + 26, ty), (tx + 20, ty + 9),
                   (tx - 20, ty + 9)], fill=(30, 48, 78))
        d.rectangle([tx - 14, ty - 7, tx + 2, ty], fill=(200, 60, 40))
        d.rectangle([tx + 6, ty - 7, tx + 18, ty], fill=(230, 230, 220))
        starburst(d, tx, ty - 4, 9, RED)
        flame(d, tx, ty - 4, 0.5)
    text(d, x0 + 8, y0 + 82, "STRAIT OF HORMUZ", f(8, True), fill=LIGHT)
    text(d, x0 + 235, y0 + 8, "2", fs(28), fill=LIGHT)
    text(d, x0 + 235, y0 + 42, "TANKERS HIT", f(9, True), fill=LIGHT)
    text(d, x0 + 235, y0 + 56, "22 ATTACKS", f(8, True), fill=LIGHT)
    text(d, x0 + 235, y0 + 68, "IN NOVEMBER", f(8, True), fill=LIGHT)
    chip = "IRGC CLAIM"
    cw = len(chip) * 5 + 12
    cx0 = x1 - cw - 8
    d.rectangle([cx0, y1 - 20, cx0 + cw, y1 - 6], fill=RED)
    text(d, cx0 + cw / 2, y1 - 18, chip, f(8, True), fill=LIGHT,
         anchor="ma")


def dymer_v1(d, x, iy):
    """Dymer lead graphic (308x100): night sky, big 11 KILLED and
    big 14 MISSING, rubble band, 03:28 rescue line, mourning chip."""
    d.rectangle([x + 8, iy, x + 316, iy + 100], fill=(14, 24, 48))
    for (sx, sy) in [(24, 10), (70, 14), (120, 8), (170, 12), (220, 8),
                     (280, 12), (300, 30), (40, 90), (300, 88),
                     (150, 92), (260, 92), (90, 88)]:
        d.ellipse([x + sx - 1, iy + sy - 1, x + sx + 1, iy + sy + 1],
                  fill=LIGHT)
    text(d, x + 12, iy + 6, "11", fs(30), fill=LIGHT)
    text(d, x + 12, iy + 42, "KILLED", f(9, True), fill=LIGHT)
    text(d, x + 170, iy + 6, "14", fs(30), fill=(240, 200, 60))
    text(d, x + 170, iy + 42, "MISSING", f(9, True), fill=LIGHT)
    # rubble band
    d.polygon([(x + 8, iy + 100), (x + 60, iy + 72), (x + 110, iy + 88),
               (x + 170, iy + 70), (x + 230, iy + 90), (x + 290, iy + 74),
               (x + 316, iy + 84), (x + 316, iy + 100)],
              fill=(60, 64, 78))
    d.rectangle([x + 96, iy + 62, x + 104, iy + 76], fill=(240, 200, 60))
    flame(d, x + 100, iy + 60, 0.35)
    text(d, x + 10, iy + 86,
         "03:28 \u2014 woman, 79, pulled alive",
         f(9), fill=LIGHT)
    chip = "DAY OF MOURNING"
    cw = len(chip) * 5 + 12
    cx0 = x + 316 - cw - 8
    d.rectangle([cx0, iy + 82, cx0 + cw, iy + 96], fill=(20, 33, 61),
                outline=LIGHT)
    text(d, cx0 + cw / 2, iy + 84, chip, f(8, True), fill=LIGHT,
         anchor="ma")


# -------------------------------------------------------------- mediums

def dems_v1(d, x, iy):
    """House 258 (176x62): Capitol dome + big 258, biggest since 1992."""
    d.rectangle([x + 8, iy, x + 184, iy + 62], fill=(240, 242, 248))
    d.ellipse([x + 22, iy + 12, x + 58, iy + 40], fill=(20, 33, 61))
    d.rectangle([x + 16, iy + 40, x + 64, iy + 46], fill=(20, 33, 61))
    for cx in (22, 32, 42, 52, 62):
        d.rectangle([x + cx - 2, iy + 46, x + cx + 2, iy + 58],
                    fill=(20, 33, 61))
    d.rectangle([x + 14, iy + 58, x + 66, iy + 62], fill=(20, 33, 61))
    text(d, x + 84, iy + 6, "258", fs(24), fill=BLUE)
    text(d, x + 84, iy + 38, "SEATS", f(9, True), fill=INK)
    text(d, x + 84, iy + 50, "BIGGEST SINCE 1992", f(8, True), fill=INK)


def merkury_v1(d, x, iy):
    """Merkury sunk (176x62): night sea, burning warship, 7 sea drones."""
    d.rectangle([x + 8, iy, x + 184, iy + 62], fill=(18, 38, 68))
    d.polygon([(x + 14, iy + 38), (x + 96, iy + 38), (x + 88, iy + 52),
               (x + 22, iy + 52)], fill=(10, 12, 16))
    d.rectangle([x + 60, iy + 28, x + 70, iy + 38], fill=LIGHT)
    flame(d, x + 44, iy + 34, 0.6)
    flame(d, x + 72, iy + 36, 0.5)
    for (dx, dy) in [(148, 16), (166, 26), (152, 34)]:
        d.ellipse([x + dx - 2, iy + dy - 2, x + dx + 2, iy + dy + 2],
                  fill=LIGHT)
    text(d, x + 112, iy + 8, "7", fs(28), fill=LIGHT)
    text(d, x + 112, iy + 40, "SEA DRONES", f(9, True), fill=LIGHT)
    text(d, x + 112, iy + 52, "WARSHIP SUNK", f(8, True), fill=LIGHT)


def cikande_v1(d, x, iy):
    """Cikande fire (176x62): factory + flames + big 24 DEAD, ~30 MISSING."""
    d.rectangle([x + 8, iy, x + 184, iy + 62], fill=(35, 28, 22))
    d.rectangle([x + 14, iy + 38, x + 70, iy + 62], fill=(20, 18, 16))
    d.rectangle([x + 58, iy + 24, x + 66, iy + 62], fill=(20, 18, 16))
    flame(d, x + 32, iy + 42, 0.8)
    flame(d, x + 52, iy + 38, 0.9)
    flame(d, x + 70, iy + 44, 0.7)
    text(d, x + 104, iy + 6, "24", fs(28), fill=(240, 120, 30))
    text(d, x + 104, iy + 40, "DEAD", f(9, True), fill=LIGHT)
    text(d, x + 104, iy + 52, "~30 MISSING", f(8, True), fill=LIGHT)


def rout_v1(d, x, iy):
    """AI rout (176x62): red falling chart + big -10%, TAIEX -17.5%."""
    d.rectangle([x + 8, iy, x + 184, iy + 62], fill=(255, 255, 255))
    pts = [(x + 14, iy + 16), (x + 44, iy + 24), (x + 74, iy + 22),
           (x + 104, iy + 40), (x + 134, iy + 36), (x + 168, iy + 56)]
    d.line(pts, fill=RED, width=4)
    for px, py in pts:
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=RED)
    d.polygon([(x + 168, iy + 56), (x + 156, iy + 56), (x + 168, iy + 46)],
              fill=RED)
    # white label chips so the chart line never strikes through the numbers
    d.rectangle([x + 10, iy + 4, x + 82, iy + 30], fill=LIGHT)
    text(d, x + 14, iy + 6, "-10%", fs(22), fill=RED)
    d.rectangle([x + 92, iy + 42, x + 180, iy + 58], fill=LIGHT)
    text(d, x + 96, iy + 44, "TAIEX -17.5%", f(9, True), fill=INK)


def vanuatu_v1(d, x, iy):
    """Vanuatu quake (176x62): seismograph line + big 6.5, 601 km deep."""
    d.rectangle([x + 8, iy, x + 184, iy + 62], fill=(245, 245, 240))
    quake_line(d, x + 12, iy + 6, 100, 22)
    text(d, x + 122, iy + 6, "6.5", fs(24), fill=RED)
    text(d, x + 122, iy + 38, "MAGNITUDE", f(8, True), fill=INK)
    text(d, x + 14, iy + 36, "02:40 UTC", f(9, True), fill=INK)
    text(d, x + 14, iy + 48, "601 KM DEEP \u00b7 NO TSUNAMI", f(8, True),
         fill=INK)


def delhi_v1(d, x, iy):
    """Nepal-India (176x62): two flags + big 24,000 crore deal, 8 MoUs."""
    d.rectangle([x + 8, iy, x + 184, iy + 62], fill=(240, 242, 248))
    # India flag
    d.rectangle([x + 14, iy + 10, x + 54, iy + 22], fill=(220, 120, 30))
    d.rectangle([x + 14, iy + 22, x + 54, iy + 34], fill=LIGHT)
    d.rectangle([x + 14, iy + 34, x + 54, iy + 46], fill=(40, 120, 60))
    d.ellipse([x + 30, iy + 24, x + 38, iy + 32], outline=BLUE, width=1)
    # Nepal flag (crimson double pennant)
    d.polygon([(x + 62, iy + 10), (x + 86, iy + 18), (x + 62, iy + 26),
               (x + 82, iy + 34), (x + 62, iy + 46)], fill=(200, 40, 60))
    text(d, x + 96, iy + 8, "24,000", fs(19), fill=INK)
    text(d, x + 96, iy + 34, "CRORE DEAL", f(9, True), fill=INK)
    text(d, x + 96, iy + 48, "8 MoUs SIGNED", f(8, True), fill=INK)


def fifa_v1(d, x, iy):
    """FIFA 2035 (176x62): green pitch + ball + big 48 teams, 104 matches."""
    d.rectangle([x + 8, iy, x + 184, iy + 62], fill=(45, 125, 65))
    d.ellipse([x + 22, iy + 18, x + 54, iy + 50], fill=LIGHT,
              outline=INK, width=1)
    d.polygon([(x + 38, iy + 26), (x + 44, iy + 30), (x + 42, iy + 38),
               (x + 34, iy + 38), (x + 32, iy + 30)], fill=INK)
    text(d, x + 66, iy + 8, "48", fs(26), fill=LIGHT)
    text(d, x + 66, iy + 40, "TEAMS", f(9, True), fill=LIGHT)
    text(d, x + 122, iy + 14, "104", fs(20), fill=LIGHT)
    text(d, x + 122, iy + 40, "MATCHES", f(9, True), fill=LIGHT)
    text(d, x + 122, iy + 52, "UK 2035", f(8, True), fill=LIGHT)


def liverpool_v1(d, x, iy):
    """Liverpool 4-0 (176x62): red scoreboard + big 4-0, ten-man United."""
    d.rectangle([x + 8, iy, x + 184, iy + 62], fill=(180, 30, 40))
    d.rectangle([x + 16, iy + 10, x + 96, iy + 52], fill=(20, 24, 34))
    text(d, x + 56, iy + 14, "4\u20130", fs(24), fill=LIGHT, anchor="ma")
    text(d, x + 56, iy + 42, "FULL TIME", f(8, True), fill=LIGHT,
         anchor="ma")
    text(d, x + 108, iy + 10, "LIVERPOOL", f(9, True), fill=LIGHT)
    text(d, x + 108, iy + 24, "THRASH", f(9, True), fill=LIGHT)
    text(d, x + 108, iy + 38, "TEN-MAN", f(9, True), fill=LIGHT)
    text(d, x + 108, iy + 50, "UNITED", f(9, True), fill=LIGHT)


def nato_v1(d, x, iy):
    """NATO Poland missiles (176x62): navy, compass star, big 3 Kh-101."""
    d.rectangle([x + 8, iy, x + 184, iy + 62], fill=(20, 33, 61))
    starburst(d, x + 38, iy + 31, 16, (120, 160, 220))
    d.ellipse([x + 32, iy + 25, x + 44, iy + 37], fill=LIGHT)
    text(d, x + 66, iy + 8, "3", fs(26), fill=LIGHT)
    text(d, x + 66, iy + 40, "KH-101 MISSILES", f(9, True), fill=LIGHT)
    text(d, x + 66, iy + 52, "CRASHED FRIDAY", f(8, True), fill=LIGHT)


def geneva_v1(d, x, iy):
    """Geneva killer robots (176x62): robot + big 128 states, rules by 2028."""
    d.rectangle([x + 8, iy, x + 184, iy + 62], fill=(240, 242, 248))
    robot(d, x + 38, iy + 36, 0.55)
    text(d, x + 72, iy + 8, "128", fs(24), fill=INK)
    text(d, x + 72, iy + 38, "STATES", f(9, True), fill=INK)
    text(d, x + 72, iy + 50, "RULES BY 2028", f(8, True), fill=INK)


# ------------------------------------------------------------------ map

# (number, lon, lat, region colour) — story numbers from the content file
PINS_23 = [
    (1, 30.7, 36.9, GL),    # Antalya — COP31
    (2, 56.5, 26.6, ME),    # Strait of Hormuz
    (3, 30.5, 50.4, EU),    # Kyiv / Dymer
    (4, -77.0, 38.9, AM),   # Washington
    (5, 20.1, 32.1, AF),    # Benghazi
    (6, 106.4, -6.2, SEA),  # Cikande
    (7, 121.6, 25.0, EA),   # Taipei
    (8, 167.9, -17.7, OC),  # Vanuatu
    (9, 77.2, 28.6, SA),    # New Delhi
    (10, 8.5, 47.4, EU),    # Zurich
    (11, -2.99, 53.4, EU),  # Liverpool
    (12, 4.35, 50.85, EU),  # Brussels
    (13, 6.1, 46.2, GL),    # Geneva
    (14, 25.0, 59.5, EU),   # Gulf of Finland
    (15, 39.0, 22.8, ME),   # Rabigh
    (16, 127.7, 26.2, EA),  # Okinawa
    (17, 121.0, 14.6, SEA), # Manila
    (18, 74.3, 31.5, SA),   # Lahore
    (19, 28.0, 7.9, AF),    # Warrap
    (20, 32.5, 15.6, AF),   # Khartoum
    (21, 35.2, 31.9, ME),   # Ramallah
    (22, 34.5, 31.5, ME),   # Gaza
]

PIN_OFFSETS = {
    1: (-14, 12), 2: (16, 10), 3: (14, -12), 5: (10, -10),
    10: (-18, -12), 11: (-18, 4), 12: (10, -14), 13: (-16, 10),
    15: (12, 12), 20: (8, 10), 21: (12, 8), 22: (-14, 10),
}


def world_map_v1(d, x0, y0, x1, y1):
    """Equirectangular world map with the 23 Nov pins."""
    d.rectangle([x0, y0, x1, y1], fill=(196, 221, 238))
    for lon in range(-150, 181, 30):
        gx = x0 + (lon + 180) / 360 * (x1 - x0)
        d.line([gx, y0, gx, y1], fill=(172, 202, 222), width=1)
    for lat in range(-60, 81, 30):
        gy = y0 + (80 - lat) / 140 * (y1 - y0)
        d.line([x0, gy, x1, gy], fill=(172, 202, 222), width=1)
    for poly in CONTINENTS:
        pts = [(x0 + (lon + 180) / 360 * (x1 - x0),
                y0 + (80 - lat) / 140 * (y1 - y0)) for lon, lat in poly]
        d.polygon(pts, fill=(188, 204, 168), outline=(140, 160, 120))
    text(d, x0 + (30 / 360) * (x1 - x0), y0 + (80 / 140) * (y1 - y0),
         "PACIFIC", f(7, True), fill=(120, 150, 175))
    text(d, x0 + (135 / 360) * (x1 - x0), y0 + (50 / 140) * (y1 - y0),
         "ATLANTIC", f(7, True), fill=(120, 150, 175))
    for num, lon, lat, col in PINS_23:
        cx = x0 + (lon + 180) / 360 * (x1 - x0)
        cy = y0 + (80 - lat) / 140 * (y1 - y0)
        px, py = cx, cy
        if num in PIN_OFFSETS:
            dx, dy = PIN_OFFSETS[num]
            px, py = cx + dx, cy + dy
            d.line([(cx, cy), (px, py)], fill=col, width=1)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=col,
                  outline=LIGHT, width=2)
        text(d, px, py - 6, str(num), f(8, True), fill=LIGHT, anchor="ma")


# ----------------------------------------------------------------- build

def build_v1():
    img = Image.new("RGB", (1024, 1024), PAPER)
    d = ImageDraw.Draw(img)

    # ---- top strip + masthead ----
    text(d, 12, 3, "THE WORLD IN ONE DAY", f(10, True))
    text(d, 512, 3, "DAY 327 OF 2026", f(10, True), fill=RED, anchor="ma")
    text(d, 1012, 3, "ALL TIMES UTC", f(10, True), anchor="ra")
    d.line([12, 16, 1012, 16], fill=INK, width=1)
    text(d, 12, 20, "Monday 23 November 2026", fs(58), fill=INK)
    d.line([12, 90, 1012, 90], fill=INK, width=2)
    text(d, 512, 94,
         "COP31 fallout in Antalya \u00b7 tankers ablaze in Hormuz \u00b7 Kyiv mourns Dymer \u00b7 Democrats take the House",
         fs(13), anchor="ma")

    # ---- UTC strip ----
    d.rectangle([12, 112, 104, 140], fill=INK)
    text(d, 58, 114, "THE DAY", f(10, True), fill=LIGHT, anchor="ma")
    text(d, 58, 126, "IN UTC", f(10, True), fill=LIGHT, anchor="ma")
    d.rectangle([112, 112, 1012, 140], fill=INK)
    text(d, 120, 115,
         "00:00 Cikande search resumes \u00b7 00:52 IRGC: tankers hit mines \u00b7 02:40 Vanuatu M6.5 quake \u00b7 03:28 Woman, 79, pulled alive in Dymer",
         f(9), fill=LIGHT)
    text(d, 120, 128,
         "10:13 NHS unveils EDITH trial \u00b7 MIDDAY Modi and Nepal's Shah meet \u00b7 AFTERNOON FIFA names UK as 2035 host \u00b7 EVENING COP31 backlash grows \u00b7 LATE US futures bounce",
         f(9), fill=LIGHT)

    # ---- stat strip ----
    stats = [("194", "delegations at\nCOP31 in Antalya"),
             ("2", "tankers hit in\nthe Strait of Hormuz"),
             ("11", "killed in Dymer;\n14 still missing"),
             ("258", "Democratic seats\nin the House"),
             ("-10%", "Nasdaq's worst week\nsince Covid"),
             ("700,000", "women in the NHS\nEDITH trial")]
    bounds = [12, 160, 300, 430, 580, 760, 1012]
    for i, (num, lab) in enumerate(stats):
        need = d.textlength(num, font=fs(24)) + 14 + max(
            d.textlength(ln, font=f(9)) for ln in lab.split("\n"))
        assert need <= bounds[i + 1] - bounds[i], \
            "stat %r needs %d px, column is %d" % (
                num, need, bounds[i + 1] - bounds[i])
    for i, (num, lab) in enumerate(stats):
        x = bounds[i]
        text(d, x + 4, 144, num, fs(24), fill=RED)
        nw = d.textlength(num, font=fs(24))
        lx = x + 14 + nw
        for j, ln in enumerate(lab.split("\n")):
            text(d, lx, 148 + j * 12, ln, f(9))
    for bx in bounds[1:-1]:
        d.line([bx, 142, bx, 180], fill=(200, 196, 180), width=1)
    # region bar (pictured stories 1-13 only)
    regions = [("Europe 4", EU), ("Global 3", GL), ("Middle East 1", ME),
               ("Americas 1", AM), ("Africa 1", AF), ("South Asia 1", SA),
               ("South-East Asia 1", SEA), ("Oceania 1", OC)]
    text(d, 12, 186, "STORIES BY REGION", f(9, True))
    rx = 132
    for name, col in regions:
        w = len(name) * 5 + 10
        d.rectangle([rx, 184, rx + w, 198], fill=col)
        text(d, rx + w / 2, 188, name, f(8, True), fill=LIGHT, anchor="ma")
        rx += w + 5

    # ---- leads (3) ----
    leads = [
        (1, "GLOBAL \u00b7 COP31, ANTALYA \u00b7 CLIMATE", "cop", "CONFIRMED",
         GREEN,
         "COP31 collapses without a deal \u2014 blame erupts",
         "Longest summit ever ends in failure; 194 delegations, no fossil-fuel mention, talks suspended.",
         "REUTERS \u00b7 LE MONDE", GL),
        (2, "MIDDLE EAST \u00b7 STRAIT OF HORMUZ \u00b7 GULF WAR", "hormuz",
         "CLAIM", RED,
         "Tankers ablaze in the Strait",
         "IRGC says two supertankers hit naval mines; 22 attacks in November. Brent near $92.29.",
         "MENAFN \u00b7 CNN \u00b7 UKMTO \u00b7 REUTERS", ME),
        (3, "EUROPE \u00b7 DYMER, UKRAINE \u00b7 WAR", "dymer", "CONFIRMED",
         GREEN,
         "Kyiv mourns as rescue ends in Dymer",
         "11 killed, 14 missing; woman, 79, and Davyd, 7, pulled alive after 14 hours.",
         "REUTERS \u00b7 BBC", EU),
    ]
    for i, (num, kick, kind, pill, pill_col, head, summ, src, col) in enumerate(leads):
        x = 12 + i * 338
        card_sq(d, [x, 214, x + 324, 442])
        kicker_bar_pill(d, x, 214, 324, num, kick, col, pill, pill_col,
                        h=24, fsize=10)
        if kind == "cop":
            cop_v1(d, x, 244)
        elif kind == "hormuz":
            hormuz_v1(d, x, 244)
        else:
            dymer_v1(d, x, 244)
        yy = headline(d, x + 8, 350, head, 20, 308, 2)
        yy = headline(d, x + 8, yy + 2, summ, 10, 308, 2)
        text(d, x + 8, yy + 2, src, f(8), fill=GREY)

    # ---- mediums (10), 2 rows of 5, pitch 150, card 144 tall ----
    mediums = [
        (4, "WASHINGTON", "dems", "CONFIRMED", GREEN,
         "Democrats take House with 258 seats",
         "Biggest majority since 1992.", "AP \u00b7 REUTERS", AM),
        (5, "BENGHAZI \u00b7 WAR", "merkury", "CONFIRMED", GREEN,
         "Ukraine sinks Russian warship off Libya",
         "Seven sea drones sank the Merkury.", "AP \u00b7 WSJ", AF),
        (6, "CIKANDE \u00b7 FIRE", "cikande", "CONFIRMED", GREEN,
         "Factory fire toll confirmed: 24 dead",
         "~30 still missing; DNA tests begin.", "REUTERS", SEA),
        (7, "MARKETS \u00b7 AI ROUT", "rout", "CONFIRMED", GREEN,
         "AI rout goes global as Nasdaq falls 10%",
         "Taiwan bans short selling.", "REUTERS \u00b7 CNBC",
         GL),
        (8, "VANUATU \u00b7 QUAKE", "vanuatu", "CONFIRMED", GREEN,
         "Vanuatu rocked by M6.5 quake",
         "601 km deep; no tsunami threat.", "USGS", OC),
        (9, "NEW DELHI", "delhi", "CONFIRMED", GREEN,
         "Nepal PM meets Modi in Delhi",
         "NPR 24,000-crore deal; 8 MoUs signed.", "REUTERS \u00b7 IANS",
         SA),
        (10, "ZURICH \u00b7 SPORT", "fifa", "REPORTED", (176, 132, 16),
         "FIFA names UK as 2035 World Cup host",
         "48 teams, 104 matches; vote pending.", "FIFA \u00b7 BBC \u00b7 REUTERS",
         EU),
        (11, "LIVERPOOL", "liverpool", "CONFIRMED", GREEN,
         "Liverpool 4\u20130 United: Pochettino's nightmare",
         "Yoro off in eight minutes.", "REUTERS", EU),
        (12, "BRUSSELS \u00b7 NATO", "nato", "CONFIRMED", GREEN,
         "NATO meets today on Poland missiles",
         "Tusk calls it a provocation.", "REUTERS", EU),
        (13, "GENEVA", "geneva", "CONFIRMED", GREEN,
         "128 states to draft killer-robot rules",
         "No binding treaty; rules due by 2028.", "UN \u00b7 CCW", GL),
    ]
    gfx = {"dems": dems_v1, "merkury": merkury_v1, "cikande": cikande_v1,
           "rout": rout_v1, "vanuatu": vanuatu_v1, "delhi": delhi_v1,
           "fifa": fifa_v1, "liverpool": liverpool_v1, "nato": nato_v1,
           "geneva": geneva_v1}
    for i, (num, kick, kind, pill, pill_col, head, deck, src, col) in enumerate(mediums):
        x = 12 + (i % 5) * 200
        y = 448 + (i // 5) * 150
        card_sq(d, [x, y, x + 192, y + 144])
        gfx[kind](d, x, y + 4)
        kicker_bar_pill(d, x, y + 70, 192, num, kick, col, pill, pill_col)
        hl = wrap(d, head, fs(13), 176)
        assert len(hl) <= 2, "medium %d headline wraps to %d lines: %r" % (num, len(hl), hl)
        assert d.textlength(deck, font=f(9)) <= 176, \
            "medium %d deck too wide: %r" % (num, deck)
        headline(d, x + 8, y + 90, head, 13, 176, 2)
        text(d, x + 8, y + 126, deck, f(9))
        text(d, x + 192 - 8, y + 137, src, f(8), fill=GREY, anchor="ra")

    # ---- map + briefs ----
    card_sq(d, [12, 748, 460, 948])
    text(d, 20, 752, "WHERE IT HAPPENED", f(11, True))
    text(d, 20, 766, "pin numbers match the stories; pin colour is the region",
         f(9), fill=GREY)
    world_map_v1(d, 20, 778, 452, 944)
    text(d, 468, 752, "ALSO ON MONDAY 23 NOVEMBER 2026", f(11, True))
    text(d, 468, 766, "32 more stories, in order of consequence",
         f(9), fill=GREY)
    briefs = [
        (14, "FINLAND", "Sparta II still burning; Russia tows it.", EU),
        (15, "RABIGH", "Houthis claim strike on Saudi refinery.", ME),
        (16, "GULF", "Saudi downs Houthi missiles; Brent $92.", ME),
        (17, "OKINAWA", "Shuri Castle reopens after seven years.", EA),
        (18, "MANILA", "8,320 drug-war dead named by Truth panel.", SEA),
        (19, "LAHORE", "World's most polluted city, AQI 538.", SA),
        (20, "WARRAP", "24 civilians, 7 children, killed in raid.", AF),
        (21, "KHARTOUM", "Drones hit UN building; 4 dead.", AF),
        (22, "RAMALLAH", "Settlers burn 12 Palestinian vehicles.", ME),
        (23, "GAZA", "3 more killed; ceasefire toll hits 1,675.", ME),
        (24, "BRUSSELS", "France, Germany reject \u20ac1.781bn budget.", EU),
        (25, "BEIJING", "China cuts margin ratios to slow slide.", EA),
        (26, "WELLINGTON", "Nicholls' unbeaten 175 saves NZ draw.", OC),
        (27, "NAPLES", "Thitikul's $4m three-peat tops record.", AM),
        (28, "CINEMA", "'Sunrise on the Reaping' opens with $120m.", GL),
        (29, "VIRGINIA", "First child measles death in Virginia.", AM),
        (30, "WASHINGTON", "The penny ends after 232 years.", AM),
        (31, "JERUSALEM", "Eisenkot denounces 'Jewish terrorism'.", ME),
        (32, "SYRIA", "Burns 400 million Captagon pills.", ME),
        (33, "HORMUZ", "Ships collide as Iran holds talks.", ME),
        (34, "SUVA", "India\u2013Fiji defence pact signed.", OC),
        (35, "SEATTLE", "ICE detain father and daughter.", AM),
        (36, "CONGO", "Fighting threatens Ebola response.", AF),
        (37, "ISTANBUL", "Thousands protest media closure.", EU),
        (38, "PYONGYANG", "North Korea expands uranium plant.", EA),
        (39, "OTTAWA", "Pentagon memo curbs US\u2013Canada ties.", AM),
        (40, "LONDON", "NHS EDITH trial to enrol 700,000 women.", EU),
        (41, "DHAKA", "Bangladesh vows to jail ex-PM Hasina.", SA),
        (42, "CANBERRA", "Australia nears Solomon Islands treaty.", OC),
        (43, "BRATISLAVA", "Slovakia refuses \u20ac45bn loan share.", EU),
        (44, "MANAMA", "Bahrain takes Iran to the UN.", ME),
        (45, "WASHINGTON", "Trump blames Democrats for $6tn fall.", AM),
    ]
    for i, (num, region, s, col) in enumerate(briefs):
        col_i = i // 16
        row = i % 16
        bx = 468 + col_i * 272
        by = 780 + row * 10.5
        by = int(by)
        d.rectangle([bx, by, bx + 14, by + 13], fill=col)
        text(d, bx + 7, by + 1, str(num), f(8, True), fill=LIGHT,
             anchor="ma")
        text(d, bx + 18, by, region + ": ", f(9, True))
        rw = d.textlength(region + ": ", font=f(9, True))
        text(d, bx + 18 + rw, by, s, f(9))
        total = d.textlength(region + ": " + s, font=f(9, True)) + \
            d.textlength(region + ": ", font=f(9, True)) * 0  # measured below
        w = 18 + d.textlength(region + ": ", font=f(9, True)) + \
            d.textlength(s, font=f(9))
        assert w <= 272, "brief %d too wide (%d px): %s" % (num, w, s)

    # ---- bottom: DATE CHECK (exact excluded set from the content file) ----
    dc = ("Left out on purpose \u2014 first reported Fri\u2013Sun, not Monday's news: "
          "COP31 collapse itself (Sun 22 Nov \u2014 Monday's news is the fallout) \u00b7 "
          "Dymer strike itself (Sun 22 Nov \u2014 Monday's news is the toll) \u00b7 "
          "Banten fire itself (Sat 21 Nov \u2014 Monday's news is the confirmed toll) \u00b7 "
          "Lisbon living-cost march (Sat 21 Nov) \u00b7 Nvidia probe (22 Nov) \u00b7 "
          "Myanmar\u2013ASEAN (21 Nov) \u00b7 al-Khuwair taken (13 Nov) \u00b7 "
          "El Obeid strike (19 Nov) \u00b7 Verstappen's Las Vegas GP win (Sun) \u00b7 "
          "'El Chapo Isidro' captured (Fri 20 Nov) \u00b7 Alcaraz's ATP Finals win (Sun final) \u00b7 "
          "BepiColombo's Mercury orbit (Sat) \u00b7 Seoul's education minister quits (22 Nov) \u00b7 "
          "Bolsonaro's ICU admission (22 Nov) \u00b7 Denmark expels Russian attach\u00e9 (22 Nov) \u00b7 "
          "Hong Kong election turnout 98.79% (Sun) \u00b7 186-drone barrage (Sun overnight) \u00b7 "
          "Russia's 400-drone barrage (19\u201320 Nov) \u00b7 Peru quake (20 Nov) \u00b7 "
          "Gaza food-aid vehicle strike (22 Nov). Wires read to ~14:15 UTC, Mon 23 Nov 2026; "
          "every story here was reported, or was still developing, on 23 Nov in at least one "
          "time zone. Claims labelled CLAIM; unconfirmed items REPORTED.")
    d.rectangle([12, 952, 1012, 1020], fill=(255, 250, 235), outline=RED,
                width=1)
    text(d, 20, 955, "DATE CHECK \u2014 LEFT OUT ON PURPOSE", f(9, True),
         fill=RED)
    dc_lines = wrap(d, dc, f(8), 984)
    assert len(dc_lines) <= 5, "DATE CHECK wrapped to %d lines" % len(dc_lines)
    for j, ln in enumerate(dc_lines):
        text(d, 20, 966 + j * 10, ln, f(8))
    return img


if __name__ == "__main__":
    im = build_v1()
    im.save("entry_v1.png")
    im.resize((300, 300), Image.LANCZOS).save("entry_v1-300.png")
    print("saved entry_v1.png", im.size)
