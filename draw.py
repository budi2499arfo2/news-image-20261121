#!/usr/bin/env python3
"""Draw the 21 Nov 2026 world-news briefing board (1024x1024).

Design: a dark "briefing board" — one large lead story on top, four
colour-coded story cards below. Flat vector illustrations drawn with
Pillow; every headline on a solid card so text stays crisp.

Run: python3 draw.py  -> writes entry.png next to this file.
"""
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(name, size):
    return ImageFont.truetype(f"{FONT_DIR}/{name}", size)


F_TITLE = font("DejaVuSans-Bold.ttf", 50)
F_SUB = font("DejaVuSans-Bold.ttf", 20)
F_DATE = font("DejaVuSans-Bold.ttf", 28)
F_LEAD_LABEL = font("DejaVuSans-Bold.ttf", 22)
F_LEAD_HEAD = font("DejaVuSans-Bold.ttf", 48)
F_LEAD_DETAIL = font("DejaVuSans.ttf", 26)
F_LABEL = font("DejaVuSans-Bold.ttf", 20)
F_HEAD = font("DejaVuSans-Bold.ttf", 32)
F_DETAIL = font("DejaVuSans.ttf", 23)

BG = (31, 41, 55)          # dark slate board
MASTHEAD = (11, 18, 32)    # near-black navy
RED = (212, 42, 42)
WHITE = (255, 255, 255)
INK = (17, 24, 39)         # headline ink
GREY = (55, 65, 81)        # detail text
MUTED = (159, 179, 200)    # masthead subtitle

img = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(img)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_block(draw, x, y, lines, fnt, fill, leading):
    for i, line in enumerate(lines):
        draw.text((x, y + i * leading), line, font=fnt, fill=fill)


# ---------------------------------------------------------------- masthead
d.rectangle([0, 0, W, 104], fill=MASTHEAD)
d.rectangle([0, 104, W, 110], fill=RED)
d.text((28, 18), "WORLD BRIEFING", font=F_TITLE, fill=WHITE)
d.text((30, 76), "SATURDAY  \u00b7  FIVE STORIES", font=F_SUB, fill=MUTED)
# date chip, right side
chip = "21 NOV 2026"
cw = d.textlength(chip, font=F_DATE) + 36
d.rounded_rectangle([W - 28 - cw, 26, W - 28, 78], radius=12, fill=RED)
d.text((W - 28 - cw + 18, 33), chip, font=F_DATE, fill=WHITE)

# ---------------------------------------------------------------- lead card
LX, LY, LW, LH = 24, 126, 976, 330
d.rounded_rectangle([LX, LY, LX + LW, LY + LH], radius=14, fill=WHITE)

# lead illustration: summit scene on navy
IX, IY, IW, IH = LX + 12, LY + 12, 336, LH - 24
d.rounded_rectangle([IX, IY, IX + IW, IY + IH], radius=10, fill=(20, 50, 79))
# round table
d.ellipse([IX + 78, IY + 218, IX + 258, IY + 268], fill=(194, 154, 74))
# three flags on poles (US / China / Russia, simplified)
flags = [
    (IX + 52, [(212, 42, 42), (255, 255, 255), (212, 42, 42),
               (255, 255, 255), (212, 42, 42)]),   # US stripes
    (IX + 142, [(222, 41, 16)]),                    # China red
    (IX + 232, [(255, 255, 255), (0, 57, 166), (213, 0, 50)]),  # Russia
]
for fx, bands in flags:
    d.rectangle([fx, IY + 44, fx + 6, IY + 218], fill=(210, 210, 210))
    bh = 54 // len(bands)
    for i, col in enumerate(bands):
        d.rectangle([fx + 6, IY + 44 + i * bh, fx + 62,
                     IY + 44 + (i + 1) * bh], fill=col)
# US canton + China stars (tiny, simple)
d.rectangle([IX + 58, IY + 44, IX + 82, IY + 66], fill=(0, 40, 104))
for sx, sy in [(IX + 158, IY + 56), (IX + 172, IY + 52), (IX + 182, IY + 62),
               (IX + 176, IY + 72), (IX + 162, IY + 70)]:
    d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=(255, 222, 0))
d.text((IX + 18, IY + IH - 34), "SHENZHEN SUMMIT", font=F_SUB,
       fill=(200, 220, 240))

# lead text
TX = IX + IW + 28
d.text((TX, LY + 40), "LEAD STORY  \u00b7  DIPLOMACY", font=F_LEAD_LABEL,
       fill=(138, 109, 27))
head_lines = wrap(d, "Trump, Xi, Putin agree nuclear talks", F_LEAD_HEAD, 560)
text_block(d, TX, LY + 78, head_lines, F_LEAD_HEAD, INK, 58)
detail_lines = wrap(d, "Three leaders meet at Shenzhen summit",
                    F_LEAD_DETAIL, 560)
text_block(d, TX, LY + 78 + len(head_lines) * 58 + 20, detail_lines,
           F_LEAD_DETAIL, GREY, 32)
d.line([TX, LY + LH - 56, LX + LW - 28, LY + LH - 56], fill=(220, 224, 230),
       width=2)
d.text((TX, LY + LH - 42), "The summit leads a crowded day",
       font=F_LEAD_DETAIL, fill=GREY)

# ---------------------------------------------------------------- story cards
def card(x, y, w, h, color, label, headline, detail, art):
    d.rounded_rectangle([x, y, x + w, y + h], radius=12, fill=WHITE)
    # colour tab
    d.rounded_rectangle([x + 18, y + 18, x + 30, y + 30], radius=3, fill=color)
    d.text((x + 40, y + 14), label, font=F_LABEL, fill=color)
    tw = w - 190
    hl = wrap(d, headline, F_HEAD, tw)
    text_block(d, x + 20, y + 48, hl, F_HEAD, INK, 38)
    dl = wrap(d, detail, F_DETAIL, tw)
    text_block(d, x + 20, y + 48 + len(hl) * 38 + 10, dl, F_DETAIL, GREY, 28)
    # illustration tile, right side
    ax, ay, aw, ah = x + w - 158, y + 52, 138, 150
    d.rounded_rectangle([ax, ay, ax + aw, ay + ah], radius=10,
                        fill=(235, 238, 242))
    art(ax, ay, aw, ah)


def art_cop31(ax, ay, aw, ah):
    d.ellipse([ax + 16, ay + 14, ax + 122, ay + 120], fill=(30, 122, 70))
    d.ellipse([ax + 36, ay + 32, ax + 76, ay + 62], fill=(120, 200, 140))
    d.ellipse([ax + 72, ay + 66, ax + 102, ay + 94], fill=(120, 200, 140))
    d.arc([ax + 16, ay + 14, ax + 122, ay + 120], 0, 360, fill=(255, 255, 255),
          width=3)


def art_hormuz(ax, ay, aw, ah):
    d.rectangle([ax, ay, ax + aw, ay + ah], fill=(255, 255, 255))
    d.rounded_rectangle([ax, ay, ax + aw, ay + ah], radius=10,
                        fill=(58, 28, 24))
    # ship silhouette
    d.polygon([(ax + 24, ay + 96), (ax + 114, ay + 96), (ax + 100, ay + 116),
               (ax + 38, ay + 116)], fill=(230, 230, 230))
    d.rectangle([ax + 56, ay + 72, ax + 84, ay + 96], fill=(230, 230, 230))
    d.rectangle([ax + 86, ay + 62, ax + 94, ay + 96], fill=(230, 230, 230))
    # drone above
    d.ellipse([ax + 62, ay + 26, ax + 76, ay + 40], fill=(255, 200, 60))
    for dx, dy in [(54, 18), (84, 18), (54, 48), (84, 48)]:
        d.ellipse([ax + dx - 5, ay + dy - 5, ax + dx + 5, ay + dy + 5],
                  fill=(255, 200, 60))
    d.line([ax + 59, ay + 23, ax + 79, ay + 43], fill=(255, 200, 60), width=3)
    d.line([ax + 79, ay + 23, ax + 59, ay + 43], fill=(255, 200, 60), width=3)
    # waves
    for wy in (124, 136):
        for wx in range(12, 120, 24):
            d.arc([ax + wx, ay + wy, ax + wx + 22, ay + wy + 12], 180, 360,
                  fill=(120, 180, 220), width=3)


def art_denmark(ax, ay, aw, ah):
    d.rounded_rectangle([ax, ay, ax + aw, ay + ah], radius=10, fill=(200, 16, 46))
    d.rectangle([ax + 44, ay, ax + 62, ay + ah], fill=WHITE)
    d.rectangle([ax, ay + 58, ax + aw, ay + 76], fill=WHITE)
    # re-round the corners over the cross bars
    d.rounded_rectangle([ax, ay, ax + aw, ay + ah], radius=10, outline=WHITE,
                        width=2)


def art_space(ax, ay, aw, ah):
    d.rounded_rectangle([ax, ay, ax + aw, ay + ah], radius=10,
                        fill=(10, 40, 70))
    for sx, sy in [(20, 20), (48, 34), (96, 18), (118, 44), (30, 60),
                   (108, 66)]:
        d.ellipse([ax + sx - 2, ay + sy - 2, ax + sx + 2, ay + sy + 2],
                  fill=WHITE)
    # parachute + capsule
    d.pieslice([ax + 34, ay + 26, ax + 104, ay + 78], 180, 360,
               fill=(255, 120, 40))
    d.line([ax + 40, ay + 54, ax + 58, ay + 96], fill=WHITE, width=2)
    d.line([ax + 98, ay + 54, ax + 80, ay + 96], fill=WHITE, width=2)
    d.polygon([(ax + 56, ay + 94), (ax + 82, ay + 94), (ax + 76, ay + 120),
               (ax + 62, ay + 120)], fill=(220, 225, 230))
    # sea
    for wx in range(10, 120, 24):
        d.arc([ax + wx, ay + 128, ax + wx + 22, ay + 140], 180, 360,
              fill=(120, 180, 220), width=3)


cards = [
    (24, 472, 472, 258, (30, 122, 70), "CLIMATE",
     "COP31 talks run overtime",
     "Fossil fuel phase-out splits nations", art_cop31),
    (528, 472, 472, 258, (179, 64, 42), "CONFLICT",
     "US drone downed over Hormuz",
     "Six vessels attacked, tensions surge", art_hormuz),
    (24, 746, 472, 254, (200, 16, 46), "EUROPE",
     "Denmark expels Russian attach\u00e9",
     "Expelled for alleged spying", art_denmark),
    (528, 746, 472, 254, (14, 116, 144), "SPACE",
     "Dragon splashes down from ISS",
     "Crew home after six months in orbit", art_space),
]
for c in cards:
    card(*c)

img.save("entry.png", optimize=True)
print("wrote entry.png")
