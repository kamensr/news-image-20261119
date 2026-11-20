#!/usr/bin/env python3
"""Generate entry.png for the make.fun news-image-20261119 competition (v2).

A dense winner-format news poster summing up Thursday 19 November 2026:
49 verified stories across 7 regions -- 4 feature stories, 12 mini stories,
33 one-liners, a UTC timeline, a world map with numbered pins, and a date
check box listing big stories deliberately left out because they broke
before the 19th.

All drawing is PIL (flat shapes + real text, no AI photos).
Run: python3 generate.py  ->  writes entry.png (1024x1024) next to this file.

NOTE: the grader runs main.py in python:3.13-slim with the standard library
only, so main.py is a plain copy of the entry.png this script produces.
"""

import math

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024

# --- palette (broadsheet: cream paper, black ink, red + navy accents) -------
PAPER = (250, 245, 235)
INK = (26, 26, 26)
MUTED = (90, 86, 76)
RED = (176, 42, 42)
NAVY = (27, 42, 77)
TEAL = (23, 107, 101)
GOLD = (176, 132, 26)
PANEL = (238, 231, 214)
PANEL2 = (243, 236, 222)
LINE = (200, 190, 168)
SEA = (208, 226, 231)
LAND = (188, 210, 172)
LAND2 = (172, 198, 158)
WHITE = (255, 255, 255)
SKY = (196, 214, 226)

DJ = "/usr/share/fonts/truetype/dejavu/"
LB = "/usr/share/fonts/truetype/liberation/"


def _font(path, size):
    return ImageFont.truetype(path, size)


def f_serif(s):
    return _font(DJ + "DejaVuSerif-Bold.ttf", s)


def f_bold(s):
    return _font(DJ + "DejaVuSans-Bold.ttf", s)


def f_reg(s):
    return _font(DJ + "DejaVuSans.ttf", s)


def f_lbold(s):
    return _font(LB + "LiberationSans-Bold.ttf", s)


def f_lreg(s):
    return _font(LB + "LiberationSans-Regular.ttf", s)


def wrap_text(d, text, font, width):
    """Greedy word wrap; returns lines that each fit `width` px."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(d, x, y, text, font, width, fill, leading, max_lines=None):
    """Draw wrapped text; returns y just below the last drawn line."""
    lines = wrap_text(d, text, font, width)
    if max_lines:
        lines = lines[:max_lines]
    for line in lines:
        d.text((x, y), line, font=font, fill=fill)
        y += leading
    return y


def pill(d, x, y, text, font, bg, fg=WHITE, pad_x=5, pad_y=2):
    """Draw a small filled pill tag; returns the x just past it."""
    w = int(d.textlength(text, font=font)) + 2 * pad_x
    h = font.size + 2 * pad_y + 2
    d.rounded_rectangle([x, y, x + w, y + h], radius=3, fill=bg)
    d.text((x + pad_x, y + pad_y), text, font=font, fill=fg)
    return x + w


def hrule(d, y, x0=16, x1=1008, color=INK, width=2):
    d.line([(x0, y), (x1, y)], fill=color, width=width)


# --- canvas -----------------------------------------------------------------
img = Image.new("RGB", (W, H), PAPER)
d = ImageDraw.Draw(img)

# --- header -----------------------------------------------------------------
hrule(d, 8, width=3)
d.text((512, 16), "ONE DAY OF WORLD NEWS, ONE PICTURE",
       font=f_bold(15), fill=RED, anchor="ma")
d.text((512, 34), "Thursday 19 November 2026",
       font=f_serif(36), fill=INK, anchor="ma")
d.text((512, 74), "49 STORIES  \u00b7  7 REGIONS  \u00b7  EVERY ONE FROM THIS THURSDAY",
       font=f_bold(14), fill=NAVY, anchor="ma")
hrule(d, 92, width=1, color=LINE)

# --- UTC timeline strip -----------------------------------------------------
TL_Y = 96
d.text((16, TL_Y), "THE DAY IN UTC", font=f_bold(11), fill=RED)
timeline = [
    ("00:13", "Anthropic pricing\nconfirmed: $83"),
    ("04:43", "Trump meets Putin\n(~40 min)"),
    ("~08:00", "Kerch Bridge hit\nagain; rail halted"),
    ("08:16", "Trilateral begins\nat Kylin Villa"),
    ("10:01", "Summit ends (~90 min);\nTrump flies home"),
    ("10:55", "Peace declaration\npublished (Xinhua)"),
    ("11:28", "ICJ: Myanmar guilty\nof genocide"),
    ("14:30", "ANT first trade\non Nasdaq"),
    ("Day*", "Bangladesh unrest\nspreads, 4 killed"),
    ("21:00", "Wall St closes:\nDow \u22121,101"),
]
tl_x0, tl_w = 16, 992
col_w = tl_w / len(timeline)
d.line([(tl_x0 + 4, TL_Y + 30), (tl_x0 + tl_w - 4, TL_Y + 30)],
       fill=NAVY, width=2)
for i, (t, label) in enumerate(timeline):
    cx = tl_x0 + col_w * i + col_w / 2
    d.ellipse([cx - 4, TL_Y + 26, cx + 4, TL_Y + 34], fill=RED)
    d.text((cx, TL_Y + 11), t, font=f_bold(11), fill=NAVY, anchor="ma")
    for j, ln in enumerate(label.split("\n")):
        d.text((cx, TL_Y + 38 + j * 11), ln, font=f_lreg(10), fill=INK,
               anchor="ma")
hrule(d, 156, width=1, color=LINE)


# --- feature illustrations (flat shapes, drawn per story) -------------------
def ill_summit(d, x, y, w, h):
    """Three flags above a conference table at Kylin Villa."""
    d.rectangle([x, y, x + w, y + h], fill=(250, 226, 170))
    d.rectangle([x, y + h - 24, x + w, y + h], fill=(120, 84, 52))
    # back wall panel
    d.rectangle([x + 10, y + 8, x + w - 10, y + h - 30], fill=(255, 244, 214),
                outline=(200, 170, 110))
    # three flags on poles
    flag_cols = [(178, 34, 52), (222, 41, 16), (255, 255, 255)]
    flag_cols2 = [(60, 59, 110), (255, 222, 0), (0, 57, 166)]
    for i in range(3):
        fx = x + 22 + i * 38
        d.line([(fx, y + 12), (fx, y + h - 40)], fill=(80, 60, 40), width=2)
        d.rectangle([fx, y + 12, fx + 24, y + 30], fill=flag_cols[i])
        d.rectangle([fx, y + 21, fx + 24, y + 30], fill=flag_cols2[i])
    # table with three name cards
    d.rectangle([x + 14, y + h - 40, x + w - 14, y + h - 30], fill=(150, 100, 60))
    for i in range(3):
        cx = x + 24 + i * 38
        d.rectangle([cx, y + h - 38, cx + 16, y + h - 31], fill=WHITE)
    # handshake: two arms meeting over the table
    d.line([(x + 34, y + h - 40), (x + 66, y + h - 52)], fill=(40, 40, 40),
           width=4)
    d.line([(x + 98, y + h - 40), (x + 66, y + h - 52)], fill=(40, 40, 40),
           width=4)
    d.ellipse([x + 60, y + h - 58, x + 72, y + h - 46], fill=(230, 190, 150))


def ill_ipo(d, x, y, w, h):
    """A Nasdaq board: ANT opens high, fades, closes green."""
    d.rectangle([x, y, x + w, y + h], fill=(16, 30, 54))
    d.text((x + 8, y + 4), "ANT", font=f_bold(16), fill=(255, 220, 90))
    d.text((x + 8, y + 24), "$97.17  +17%", font=f_bold(13),
           fill=(120, 220, 140))
    d.text((x + 8, y + 42), "OPEN $111.50", font=f_bold(10),
           fill=(180, 190, 205))
    # chart area
    cx0, cy0, cx1, cy1 = x + 8, y + 58, x + w - 8, y + h - 6
    d.rectangle([cx0, cy0, cx1, cy1], fill=(24, 44, 74))
    # grid
    for gy in range(cy0 + 6, cy1, 7):
        d.line([(cx0, gy), (cx1, gy)], fill=(40, 60, 95), width=1)
    # line: jumps up, fades down, ends above the open level
    pts = [(cx0 + 2, cy1 - 4), (cx0 + 18, cy0 + 8), (cx0 + 38, cy0 + 12),
           (cx0 + 58, cy0 + 16), (cx0 + 78, cy0 + 20), (cx0 + 98, cy0 + 22),
           (cx1 - 2, cy0 + 24)]
    d.line(pts, fill=(120, 220, 140), width=3, joint="curve")
    d.ellipse([cx0 + 14, cy0 + 4, cx0 + 22, cy0 + 12], fill=(255, 220, 90))


def ill_icj(d, x, y, w, h):
    """The Peace Palace: columns, pediment, scales of justice."""
    d.rectangle([x, y, x + w, y + h], fill=(214, 226, 240))
    # pediment
    d.polygon([(x + 12, y + 30), (x + w // 2, y + 10), (x + w - 12, y + 30)],
              fill=(150, 160, 175))
    # columns
    for i in range(5):
        cx = x + 18 + i * 24
        d.rectangle([cx, y + 32, cx + 10, y + h - 18], fill=(240, 238, 230))
        d.rectangle([cx - 2, y + 30, cx + 12, y + 34], fill=(200, 195, 185))
    # base
    d.rectangle([x + 8, y + h - 18, x + w - 8, y + h - 12], fill=(150, 160, 175))
    d.rectangle([x + 4, y + h - 12, x + w - 4, y + h - 6], fill=(120, 130, 148))
    # scales of justice in the pediment
    sx, sy = x + w // 2, y + 16
    d.line([(sx, sy - 4), (sx, sy + 10)], fill=NAVY, width=2)
    d.line([(sx - 10, sy - 2), (sx + 10, sy - 2)], fill=NAVY, width=2)
    d.line([(sx - 10, sy - 2), (sx - 14, sy + 8)], fill=NAVY, width=1)
    d.line([(sx - 10, sy - 2), (sx - 6, sy + 8)], fill=NAVY, width=1)
    d.line([(sx + 10, sy - 2), (sx + 6, sy + 8)], fill=NAVY, width=1)
    d.line([(sx + 10, sy - 2), (sx + 14, sy + 8)], fill=NAVY, width=1)
    d.arc([sx - 16, sy + 4, sx - 4, sy + 14], 0, 180, fill=NAVY, width=2)
    d.arc([sx + 4, sy + 4, sx + 16, sy + 14], 0, 180, fill=NAVY, width=2)
    # "9-6" verdict chip
    d.rounded_rectangle([x + w - 40, y + h - 34, x + w - 6, y + h - 20],
                        radius=3, fill=RED)
    d.text((x + w - 23, y + h - 33), "9\u20136", font=f_bold(10), fill=WHITE,
           anchor="ma")


def ill_gaza(d, x, y, w, h):
    """Tanks withdrawing at dusk after a 24-hour operation."""
    d.rectangle([x, y, x + w, y + h], fill=(240, 214, 160))
    # low sun
    d.ellipse([x + w - 36, y + 8, x + w - 14, y + 30], fill=(240, 150, 60))
    # road
    d.rectangle([x, y + h - 26, x + w, y + h], fill=(140, 130, 115))
    for dx in range(0, w, 22):
        d.rectangle([x + dx, y + h - 14, x + dx + 12, y + h - 11],
                    fill=(240, 235, 220))
    # checkpoint barrier, raised
    d.line([(x + 12, y + h - 26), (x + 12, y + h - 56)], fill=(60, 60, 60),
           width=3)
    d.line([(x + 12, y + h - 56), (x + 46, y + h - 70)], fill=(220, 40, 40),
           width=4)
    # tank heading away (small, rear view)
    d.rounded_rectangle([x + 62, y + h - 52, x + 104, y + h - 34], radius=4,
                        fill=(90, 100, 70))
    d.rectangle([x + 72, y + h - 62, x + 94, y + h - 50], fill=(90, 100, 70))
    for wx in range(x + 68, x + 100, 10):
        d.ellipse([wx, y + h - 36, wx + 7, y + h - 29], fill=(60, 68, 48))
    # dust trail
    for sx, sy, r in [(x + 56, y + h - 40, 5), (x + 48, y + h - 34, 7),
                      (x + 38, y + h - 30, 5)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(210, 190, 150))
    # "24h" chip, sized to the measured text so nothing spills out
    chip_font = f_bold(9)
    chip_w = int(d.textlength("24 HOURS", font=chip_font)) + 12
    d.rounded_rectangle([x + 6, y + 6, x + 6 + chip_w, y + 20], radius=3,
                        fill=NAVY)
    d.text((x + 6 + chip_w // 2, y + 7), "24 HOURS", font=chip_font,
           fill=WHITE, anchor="ma")


# --- feature boxes ----------------------------------------------------------
FEATURES = [
    dict(num=1, region="ASIA-PACIFIC", beat="DIPLOMACY", status="CONFIRMED",
         claim=False,
         headline="Three-way summit ends with a peace declaration \u2014 but no deals",
         body=("Trump, Xi and Putin met ~90 min at Kylin Villa and issued a "
               "four-point 'Declaration Towards Peace'. No deal on Ukraine, "
               "Iran or a new nuclear treaty."),
         source="USA TODAY \u00b7 THE TIMES \u00b7 XINHUA \u00b7 CNN \u00b7 WSJ",
         ill=ill_summit),
    dict(num=2, region="GLOBAL", beat="MARKETS", status="CONFIRMED",
         claim=False,
         headline="Anthropic's ANT debuts on Nasdaq in the biggest IPO ever",
         body=("Priced $83, upsized to 980m shares, $81.34bn raised \u2014 the "
               "largest IPO ever. Opened $111.50 (+34%), faded all day, "
               "closed $97.17 (+17%), ~$1.8tn valuation."),
         source="SEC 424(b)(4) \u00b7 INVESTOPEDIA \u00b7 WSJ \u00b7 BARRON'S",
         ill=ill_ipo),
    dict(num=3, region="ASIA-PACIFIC", beat="JUSTICE", status="CONFIRMED",
         claim=False,
         headline="World court: Myanmar committed genocide against the Rohingya",
         body=("The ICJ ruled 9\u20136 that Myanmar committed genocide in "
               "2016\u201317: ~10,000 killed, widespread sexual violence. "
               "Final and binding; Myanmar must allow safe return."),
         source="AP \u00b7 GUARDIAN \u00b7 AL JAZEERA", ill=ill_icj),
    dict(num=4, region="MIDDLE EAST", beat="WAR", status="CONFIRMED",
         claim=True,
         headline="Israeli ground operation in Gaza ends after ~24 hours",
         body=("The IDF ground operation beyond the 'Yellow Line' near "
               "Nuseirat ended after ~24h; COGAT says Palestinians can move "
               "freely again. IDF says it hit a 'terror tunnel' \u2014 CLAIM."),
         source="REUTERS \u00b7 HORIZON \u00b7 OPEN CHRONICLE", ill=ill_gaza),
]

FEAT_Y, FEAT_H, FEAT_GAP = 162, 122, 6
FEAT_W = (992 - FEAT_GAP) // 2


def draw_feature(f, bx, by):
    d.rectangle([bx, by, bx + FEAT_W, by + FEAT_H], fill=PANEL2,
                outline=LINE, width=1)
    # number chip
    d.ellipse([bx + 6, by + 6, bx + 24, by + 24], fill=RED)
    d.text((bx + 15, by + 8), str(f["num"]), font=f_bold(11), fill=WHITE,
           anchor="ma")
    # illustration panel
    ix, iy, iw, ih = bx + 8, by + 28, 132, FEAT_H - 36
    f["ill"](d, ix, iy, iw, ih)
    d.rectangle([ix, iy, ix + iw, iy + ih], outline=LINE, width=1)
    # text column
    tx = bx + 148
    tw = FEAT_W - 156
    ty = by + 8
    nx = pill(d, tx, ty, f["region"], f_bold(10), NAVY)
    nx = pill(d, nx + 4, ty, f["beat"], f_bold(10), GOLD)
    nx = pill(d, nx + 4, ty, f["status"], f_bold(10), TEAL)
    if f["claim"]:
        pill(d, nx + 4, ty, "INCLUDES A CLAIM", f_bold(10), RED)
    hy = ty + 22
    draw_wrapped(d, tx, hy, f["headline"], f_bold(15), tw, INK, 18,
                 max_lines=2)
    draw_wrapped(d, tx, hy + 38, f["body"], f_lreg(11), tw, INK, 13,
                 max_lines=3)
    d.text((tx, by + FEAT_H - 15), f["source"], font=f_lbold(9), fill=MUTED)


for i, f in enumerate(FEATURES):
    bx = 16 + (i % 2) * (FEAT_W + FEAT_GAP)
    by = FEAT_Y + (i // 2) * (FEAT_H + FEAT_GAP)
    draw_feature(f, bx, by)


# --- mini-story icons (tiny flat drawings, 40x40 box) -----------------------
def ic_bridge(d, x, y, s):
    d.rectangle([x + 4, y + s - 12, x + s - 4, y + s - 4], fill=(70, 120, 150))
    d.rectangle([x + 8, y + 22, x + s - 8, y + 26], fill=(60, 60, 65))
    d.rectangle([x + s // 2 - 5, y + 22, x + s // 2 + 5, y + 30],
                fill=(255, 255, 255))
    d.rectangle([x + 10, y + 8, x + 14, y + 24], fill=(90, 90, 95))
    d.rectangle([x + s - 14, y + 8, x + s - 10, y + 24], fill=(90, 90, 95))
    d.line([(x + 12, y + 10), (x + s // 2 - 6, y + 22)], fill=(120, 120, 125),
           width=2)
    d.line([(x + s - 12, y + 10), (x + s // 2 + 6, y + 22)],
           fill=(120, 120, 125), width=2)
    for sx, sy, r in [(x + 20, y + 12, 4), (x + 24, y + 7, 3)]:
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(140, 140, 140))


def ic_flame(d, x, y, s):
    d.polygon([(x + 20, y + 4), (x + 30, y + 20), (x + 26, y + 32),
               (x + 14, y + 32), (x + 10, y + 20)], fill=(240, 140, 30))
    d.polygon([(x + 20, y + 14), (x + 26, y + 24), (x + 24, y + 30),
               (x + 16, y + 30), (x + 14, y + 24)], fill=(250, 210, 60))
    d.rectangle([x + 8, y + 33, x + s - 8, y + 36], fill=(90, 70, 50))


def ic_shield(d, x, y, s):
    d.polygon([(x + 8, y + 6), (x + s - 8, y + 6), (x + s - 8, y + 20),
               (x + 20, y + s - 4), (x + 8, y + 20)], fill=NAVY)
    d.polygon([(x + 13, y + 18), (x + 18, y + 24), (x + 28, y + 12)],
              fill=WHITE)


def ic_euro(d, x, y, s):
    d.ellipse([x + 8, y + 8, x + s - 8, y + s - 8], fill=GOLD,
              outline=(140, 100, 10), width=2)
    d.text((x + 20, y + 9), "\u20ac", font=f_bold(20), fill=NAVY, anchor="ma")


def ic_atom(d, x, y, s):
    cx, cy = x + 20, y + 20
    d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=RED)
    for ang in (0, 60, 120):
        a = math.radians(ang)
        rx, ry = 15, 6
        pts = []
        for t in range(0, 360, 12):
            tr = math.radians(t)
            px = rx * math.cos(tr)
            py = ry * math.sin(tr)
            qx = px * math.cos(a) - py * math.sin(a)
            qy = px * math.sin(a) + py * math.cos(a)
            pts.append((cx + qx, cy + qy))
        d.line(pts + [pts[0]], fill=NAVY, width=1)


def ic_oil(d, x, y, s):
    d.ellipse([x + 10, y + 14, x + s - 10, y + s - 6], fill=(40, 40, 40))
    d.polygon([(x + 20, y + 4), (x + 30, y + 20), (x + 10, y + 20)],
              fill=(40, 40, 40))
    d.ellipse([x + 14, y + 18, x + 20, y + 28], fill=(120, 120, 120))


def ic_fall(d, x, y, s):
    d.line([(x + 6, y + s - 6), (x + s - 6, y + s - 6)], fill=INK, width=2)
    d.line([(x + 6, y + s - 6), (x + 6, y + 6)], fill=INK, width=2)
    d.line([(x + 9, y + 10), (x + 17, y + 16), (x + 25, y + 20),
            (x + 33, y + 29)], fill=RED, width=3)
    d.polygon([(x + 33, y + 29), (x + 28, y + 27), (x + 33, y + 22)],
              fill=RED)


def ic_gavel(d, x, y, s):
    d.line([(x + 8, y + 28), (x + 28, y + 8)], fill=(120, 84, 52), width=4)
    d.rectangle([x + 22, y + 4, x + 34, y + 14], fill=(150, 100, 60))
    d.rectangle([x + 6, y + 30, x + 22, y + 35], fill=(90, 70, 50))
    d.rectangle([x + 4, y + 35, x + 24, y + 37], fill=(60, 45, 30))


def ic_ship(d, x, y, s):
    d.rectangle([x + 4, y + 28, x + s - 4, y + s - 4], fill=(70, 120, 150))
    d.polygon([(x + 8, y + 28), (x + 32, y + 28), (x + 28, y + 20),
               (x + 12, y + 20)], fill=RED)
    d.rectangle([x + 10, y + 12, x + 16, y + 20], fill=GOLD)
    d.rectangle([x + 18, y + 12, x + 24, y + 20], fill=TEAL)
    d.rectangle([x + 26, y + 12, x + 30, y + 20], fill=NAVY)
    d.line([(x + 20, y + 4), (x + 20, y + 12)], fill=INK, width=2)


def ic_debt(d, x, y, s):
    d.rectangle([x + 6, y + 6, x + s - 6, y + s - 6], fill=WHITE,
                outline=RED, width=2)
    d.text((x + 20, y + 7), "100%", font=f_bold(11), fill=RED, anchor="ma")
    d.rectangle([x + 10, y + 24, x + s - 10, y + 29], fill=(220, 220, 220))
    d.rectangle([x + 10, y + 24, x + s - 12, y + 29], fill=RED)


def ic_leaf(d, x, y, s):
    d.ellipse([x + 8, y + 6, x + s - 8, y + s - 10], fill=(80, 160, 80))
    d.line([(x + 20, y + 8), (x + 20, y + s - 6)], fill=(40, 100, 40),
           width=2)
    d.line([(x + 20, y + 16), (x + 28, y + 12)], fill=(40, 100, 40), width=1)
    d.line([(x + 20, y + 22), (x + 12, y + 18)], fill=(40, 100, 40), width=1)


def ic_child(d, x, y, s):
    d.ellipse([x + 16, y + 5, x + 24, y + 13], fill=(230, 190, 150))
    d.polygon([(x + 20, y + 14), (x + 12, y + 30), (x + 28, y + 30)],
              fill=TEAL)
    d.ellipse([x + 8, y + 10, x + 14, y + 16], fill=(200, 170, 130))
    d.polygon([(x + 11, y + 17), (x + 5, y + 30), (x + 17, y + 30)],
              fill=(180, 140, 90))
    d.ellipse([x + 26, y + 10, x + 32, y + 16], fill=(160, 130, 100))
    d.polygon([(x + 29, y + 17), (x + 23, y + 30), (x + 35, y + 30)],
              fill=(140, 110, 70))


MINIS = [
    dict(num=5, region="EUROPE", icon=ic_bridge,
         headline="Kerch Bridge hit a third time this week",
         body="Neptune missiles, Ukraine confirms; rail traffic halted, no injuries reported.",
         source="BBC \u00b7 KIMKJ"),
    dict(num=6, region="ASIA-PACIFIC", icon=ic_flame,
         headline="Bangladesh: 4 killed as violence spreads",
         body="Yunus ancestral home torched; unrest in 28 districts, paramilitary deployed.",
         source="HORIZON \u00b7 EGAZETTE"),
    dict(num=7, region="MIDDLE EAST", icon=ic_shield,
         headline="Kuwait repels Iranian attack",
         body="First in two months; Bahrain also targeted after the Qeshm strike.",
         source="HORIZON"),
    dict(num=8, region="EUROPE", icon=ic_euro,
         headline="EU proposes \u20ac45bn loan for Ukraine",
         body="Joint-debt loan tabled; leaders meet in Berlin on Thursday.",
         source="EC \u00b7 HORIZON"),
    dict(num=9, region="ASIA-PACIFIC", icon=ic_atom,
         headline="North Korea expands Yongbyon enrichment",
         body="IAEA: uranium enrichment extension completed in late October.",
         source="IAEA \u00b7 STRAITS TIMES"),
    dict(num=10, region="GLOBAL", icon=ic_oil,
         headline="Hormuz crisis 'greatest threat' to energy",
         body="IEA annual report warns on energy security amid the strait crisis.",
         source="IEA"),
    dict(num=11, region="GLOBAL", icon=ic_fall,
         headline="Wall Street sell-off: Dow \u22121,101",
         body="S&P \u22122.02%, 6th straight loss; Nasdaq \u22122.25% after +2% intraday; VIX +15%.",
         source="AP \u00b7 INVESTOPEDIA"),
    dict(num=12, region="AMERICAS", icon=ic_gavel,
         headline="Jeffries to be first Black House Speaker",
         body="Democrats designate Hakeem Jeffries to lead the chamber.",
         source="NDTV \u00b7 COURRIER INT'L"),
    dict(num=13, region="ASIA-PACIFIC", icon=ic_ship,
         headline="South Korea exports pass $1tn",
         body="First time ever, chip-driven; a record year for exporters.",
         source="HORIZON"),
    dict(num=14, region="GLOBAL", icon=ic_debt,
         headline="IMF: public debt nears 100% of GDP",
         body="Highest since WWII, Georgieva warns; fiscal risks rising.",
         source="IMF \u00b7 GEORGIEVA"),
    dict(num=15, region="GLOBAL", icon=ic_leaf,
         headline="COP31 ministers meet to unblock talks",
         body="Antalya push on finance; Vanuatu urges reform of negotiations.",
         source="HORIZON"),
    dict(num=16, region="GLOBAL", icon=ic_child,
         headline="Record 589m children in conflict zones",
         body="UN: humanitarian access blocked for millions of children.",
         source="UN"),
]

MINI_Y, MINI_H, MINI_GAP = 420, 96, 6
MINI_W = (992 - 3 * MINI_GAP) // 4


def draw_mini(m, bx, by):
    d.rectangle([bx, by, bx + MINI_W, by + MINI_H], fill=PANEL2,
                outline=LINE, width=1)
    # number chip + region tag + source (one row)
    d.ellipse([bx + 6, by + 6, bx + 22, by + 22], fill=NAVY)
    d.text((bx + 14, by + 8), str(m["num"]), font=f_bold(10), fill=WHITE,
           anchor="ma")
    nx = pill(d, bx + 26, by + 7, m["region"], f_bold(9), NAVY)
    d.text((nx + 5, by + 8), m["source"], font=f_lbold(9), fill=MUTED)
    # icon box
    ix, iy = bx + 6, by + 28
    d.rectangle([ix, iy, ix + 38, iy + 38], fill=WHITE, outline=LINE, width=1)
    m["icon"](d, ix - 1, iy - 1, 40)
    # headline beside icon
    draw_wrapped(d, ix + 44, iy + 1, m["headline"], f_bold(12), MINI_W - 56,
                 INK, 14, max_lines=2)
    # body below icon row
    draw_wrapped(d, bx + 6, by + 70, m["body"], f_lreg(10), MINI_W - 12,
                 INK, 12, max_lines=2)


hrule(d, 416, width=1, color=LINE)
for i, m in enumerate(MINIS):
    bx = 16 + (i % 4) * (MINI_W + MINI_GAP)
    by = MINI_Y + (i // 4) * (MINI_H + MINI_GAP)
    draw_mini(m, bx, by)


# --- map + "ALSO ON" list band ----------------------------------------------
hrule(d, 724, width=1, color=LINE)
BAND_Y, BAND_H = 728, 220

# --- world map (stylised continents, lon/lat polygons) ----------------------
MAP_X, MAP_Y, MAP_W, MAP_H = 16, BAND_Y, 320, BAND_H
d.rectangle([MAP_X, MAP_Y, MAP_X + MAP_W, MAP_Y + MAP_H], fill=SEA,
            outline=LINE, width=1)
d.text((MAP_X + 8, MAP_Y + 5), "WHERE IT HAPPENED", font=f_bold(12),
       fill=NAVY)
d.text((MAP_X + 8, MAP_Y + MAP_H - 16), "Pins match story numbers.",
       font=f_lreg(10), fill=MUTED)

mx, my, mw, mh = MAP_X + 6, MAP_Y + 26, MAP_W - 12, MAP_H - 46


def ll(lon, lat):
    return (mx + (lon + 170) / 360.0 * mw,
            my + (75 - lat) / 130.0 * mh)


def continent(pts, fill=LAND):
    d.polygon([ll(lon, lat) for lon, lat in pts], fill=fill,
              outline=(140, 165, 130))


# North America
continent([(-165, 65), (-140, 70), (-110, 68), (-90, 66), (-75, 62),
           (-60, 52), (-70, 42), (-80, 32), (-90, 21), (-97, 16),
           (-105, 22), (-115, 30), (-125, 42), (-130, 55), (-150, 60)])
# Greenland
continent([(-45, 60), (-30, 68), (-25, 76), (-55, 78), (-60, 70)], LAND2)
# South America
continent([(-79, 9), (-70, 11), (-55, 5), (-40, -5), (-35, -10), (-40, -22),
           (-50, -32), (-60, -40), (-65, -50), (-70, -54), (-73, -40),
           (-72, -25), (-77, -12), (-80, -3)])
# Europe
continent([(-10, 36), (-5, 43), (0, 50), (5, 58), (10, 60), (18, 56),
           (25, 60), (30, 70), (40, 68), (30, 55), (28, 45), (20, 40),
           (12, 44), (8, 38), (3, 36)])
# Africa
continent([(-17, 15), (-10, 30), (0, 36), (10, 37), (20, 32), (32, 31),
           (35, 27), (40, 12), (48, 10), (51, -2), (40, -10), (35, -20),
           (32, -28), (25, -34), (18, -34), (14, -22), (12, -10), (9, 4),
           (0, 6), (-8, 5), (-13, 8)])
# Asia
continent([(30, 70), (60, 70), (90, 75), (120, 73), (150, 70), (178, 66),
           (170, 60), (160, 55), (140, 45), (130, 40), (122, 30), (110, 20),
           (105, 10), (100, 8), (95, 16), (90, 22), (85, 20), (80, 8),
           (75, 12), (70, 22), (60, 25), (55, 27), (48, 30), (44, 29),
           (40, 36), (35, 36), (30, 45), (28, 55), (30, 60)])
# Australia
continent([(113, -22), (122, -14), (132, -12), (142, -11), (150, -22),
           (153, -28), (150, -37), (140, -38), (132, -32), (124, -33),
           (115, -32)])
# New Zealand, Britain, Japan
continent([(167, -35), (174, -37), (178, -42), (172, -47), (167, -42)], LAND2)
continent([(-5, 50), (-2, 53), (-3, 58), (-6, 57)], LAND2)
continent([(130, 31), (135, 34), (140, 38), (142, 43), (145, 44), (141, 39),
           (136, 33)], LAND2)
# Indonesia: a few island blobs
for ilon, ilat, ir in [(100, 0, 4), (110, -6, 5), (120, -9, 4), (132, -3, 5),
                       (141, -4, 4)]:
    px, py = ll(ilon, ilat)
    d.ellipse([px - ir, py - ir // 2, px + ir, py + ir // 2], fill=LAND)

# Pins 9 (Yongbyon) and 13 (Seoul) are ~2 degrees apart in reality, which
# is ~3 px on this map, so they are nudged apart for legibility; the other
# pins sit on their real locations.
PINS = [(1, 114, 22.5), (2, -74, 40.7), (3, 4.3, 52.1), (4, 34.5, 31.5),
        (5, 36.5, 45.3), (6, 90.4, 23.8), (7, 47.5, 29.4), (9, 122, 42),
        (13, 129, 36.5), (17, 101.7, 3.1), (18, 106.8, -6.2),
        (27, -80.2, 25.8)]
# Draw every circle first, then every number, so a later pin never covers
# an earlier pin's number where two circles touch.
for num, lon, lat in PINS:
    px, py = ll(lon, lat)
    r = 7
    d.ellipse([px - r, py - r, px + r, py + r], fill=RED,
              outline=WHITE, width=1)
for num, lon, lat in PINS:
    px, py = ll(lon, lat)
    d.text((px, py - 5), str(num), font=f_bold(9), fill=WHITE, anchor="ma")

# --- "ALSO ON" numbered list -------------------------------------------------
LIST_X, LIST_W = 344, 664
d.text((LIST_X, BAND_Y + 2), "ALSO ON THURSDAY 19 NOVEMBER",
       font=f_bold(13), fill=RED)
ALSO = [
    (17, "Malaysia to end visa-free entry for Indians in Jan 2027"),
    (18, "Indonesia passes asset-forfeiture law after 18-year wait"),
    (19, "Refinery explosion in Indonesia kills one worker"),
    (20, "Fires ravage ~3m hectares in Indonesia this season"),
    (21, "UN: 1 in 4 women globally cannot refuse sex in marriage"),
    (22, "Trump raised Huang claims with Xi; APEC appears to nod"),
    (23, "Russian arrested for spying on Palantir over Ukraine"),
    (24, "Pakistan military: \u226522 militants killed in KP raids"),
    (25, "Taiz water crisis: output nearly halved, 800,000+ cut off"),
    (26, "Haitian police in 'heavy fighting' with gangs in Martissant"),
    (27, "Miami court convicts pastor over 2021 Mo\u00efse murder"),
    (28, "El Salvador reportedly sends ~2,500 troops to Haiti"),
    (29, "EU moves to delay methane rules after US pressure"),
    (30, "Settler driver rams Palestinians in central Israel, \u22658 hurt"),
    (31, "Prince Harry: he'd return to service to fight Russia"),
    (32, "Homo erectus teeth in Guangxi challenge evolution theory"),
    (33, "Epstein autopsy expert doubts suicide theory \u2014 CLAIM"),
    (34, "Pakistan suffers nationwide internet outage"),
    (35, "Hong Kong drops case against Newnew Polar Bear captain"),
    (36, "NZ court: pay-equity reform violated women's rights"),
    (37, "Mossad chief pushed joint US\u2013Israel strikes on Iran"),
    (38, "Argentine Senate to vote on scrapping 2027 primaries"),
    (39, "French senators refuse pension freeze, eye retiree taxes"),
    (40, "Palo Alto Networks raises outlook after solid results"),
    (41, "Houthi missile toward Riyadh, PIF Tower damaged"),
    (42, "Copper falls, threatening the AI infrastructure build"),
    (43, "NASA sets coverage for Northrop Grumman CRS-25 launch"),
    (44, "MEPs accuse Chinese officials of intimidation over Taiwan"),
    (45, "Myanmar re-examines its ASEAN relations, junta says"),
    (46, "Australia, China's Landbridge at odds over Darwin port"),
    (47, "Kenya hit by milk shortage as drought cuts output"),
    (48, "107 ransomware claims recorded worldwide in 48h"),
    (49, "Lebanon charges 5 Hezbollah members; US sanctions networks"),
]
COL_W = LIST_W // 2
ROW_Y0, ROW_LEAD = BAND_Y + 22, 11.5
for i, (num, text) in enumerate(ALSO):
    col = 0 if i < 17 else 1
    row = i if col == 0 else i - 17
    x = LIST_X + col * COL_W
    y = ROW_Y0 + row * ROW_LEAD
    d.text((x, y), f"{num}.", font=f_lbold(11), fill=RED)
    d.text((x + 22, y), text, font=f_lreg(11), fill=INK)

# --- DATE CHECK band --------------------------------------------------------
DC_Y, DC_H = 952, 38
d.rectangle([16, DC_Y, 1008, DC_Y + DC_H], fill=NAVY)
d.text((24, DC_Y + 3),
       "DATE CHECK \u2014 LEFT OUT ON PURPOSE (they broke before today):",
       font=f_bold(10), fill=(255, 220, 120))
d.text((24, DC_Y + 15),
       "Van Gogh sells for $190.4m (18 Nov)  \u00b7  US loses measles elimination status (17 Nov)  \u00b7  Fiji drought disaster (18 Nov)  \u00b7  Hegseth's Caracas deal (18 Nov)",
       font=f_lreg(10), fill=WHITE)
d.text((24, DC_Y + 26),
       "OpenAI launches GPT-6.2 (18 Nov)  \u00b7  Voyager 1 passes one light-day (18 Nov)  \u00b7  Peltola wins Alaska Senate seat (18 Nov)  \u00b7  Senegal's Pastef split (18 Nov)",
       font=f_lreg(10), fill=WHITE)

# --- footer -----------------------------------------------------------------
hrule(d, 994, width=1, color=LINE)
d.text((512, 998),
       "Every story here happened or was first reported on Thursday 19 November 2026.  CLAIM = one side's account, not independently confirmed.",
       font=f_lreg(10), fill=MUTED, anchor="ma")
d.text((512, 1010),
       "Sources: Reuters \u00b7 AP \u00b7 AFP \u00b7 Al Jazeera \u00b7 BBC \u00b7 USA Today \u00b7 The Times \u00b7 Xinhua \u00b7 CNN \u00b7 WSJ \u00b7 Investopedia \u00b7 SEC \u00b7 IAEA \u00b7 IEA \u00b7 IMF \u00b7 UN \u00b7 Straits Times \u00b7 SCMP \u00b7 Le Monde \u00b7 NDTV \u00b7 ABC",
       font=f_lreg(10), fill=MUTED, anchor="ma")

img.save("entry.png")
print("saved entry.png")
