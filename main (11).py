#!/usr/bin/env python3
"""Sum up 22 November 2026's world news in one image.

Builds a newspaper-style front page (entry.png) from the day's real,
dated stories: 3 illustrated lead panels, 10 illustrated mini panels,
a numbered world map, and a dense 'Also on Sunday' column.
All artwork is original and drawn in code with PIL.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 2240, 3160
PAPER = (247, 243, 233)
INK = (24, 24, 28)
ACCENT = (154, 32, 28)
RULE = (90, 86, 78)
PANEL_BG = (255, 253, 247)
SHADE = (236, 230, 216)

# ---------------------------------------------------------------- stories
# (continent, headline, body, source) -- all first reported Sun 22 Nov 2026
LEADS = [
    ("GLOBAL",
     "COP31 TALKS SLIP INTO OVERTIME, FOSSIL FUELS STILL OUT OF THE DRAFT",
     "Negotiators in Antalya worked past the deadline on Sunday with the "
     "latest draft deal still silent on fossil fuels, raising fears the "
     "summit could end without a pact.",
     "AFP"),
    ("MIDDLE EAST",
     "TRUMP FAVOURS ECONOMIC SQUEEZE ON IRAN OVER NEW STRIKES",
     "Washington weighed four options and leans toward tightening the oil "
     "blockade, now at 130 straight days. CENTCOM says the blockade has "
     "stopped more than $25bn of Iranian crude exports.",
     "Israel Hayom reports"),
    ("ASIA",
     "39 MISSING AFTER FACTORY FIRE WEST OF JAKARTA",
     "Rescuers searched on Sunday for 39 people missing after fire tore "
     "through the Fonusa Agung Mulia confectionery factory in Serang, "
     "about 50 km from the capital, on Saturday afternoon.",
     "AFP"),
]

MINIS = [
    ("AMERICAS", "M6.9 QUAKE HITS PERU'S JUNIN REGION",
     "152 homes left uninhabitable in the revised official count.", "AFP"),
    ("MIDDLE EAST", "HERZOG ASKS EISENKOT TO FORM ISRAEL'S GOVERNMENT",
     "The president bypasses Netanyahu after the Oct 27 election left no "
     "bloc a majority.", "reports"),
    ("AMERICAS", "FBI TOP-10 CARTEL CHIEF 'CHAPO ISIDRO' CAPTURED",
     "Mexican special forces, with US help; violence in Sinaloa kills 11.",
     "reports"),
    ("EUROPE", "MISSILES HIT ZELENSKYY'S HOMETOWN KRYVYI RIH",
     "Two dead and 58 injured, six of them children, officials say.",
     "officials"),
    ("AMERICAS", "BITCOIN BACK ABOVE $60,000",
     "Rebound from $55,300, the lowest since Sep 2024; fear index at 12.",
     "markets"),
    ("MIDDLE EAST", "TWO TANKERS STRUCK NEAR OMAN",
     "Projectiles hit a stern and an engine room east of Khasab; no "
     "casualties.", "UKMTO"),
    ("GLOBAL", "VOYAGER 1 NOW ONE LIGHT-DAY FROM EARTH",
     "NASA's 1977 probe reaches a distance no spacecraft has reached "
     "before.", "NASA"),
    ("AFRICA", "NIGERIA BOAT CAPSIZE TOLL RISES TO 24",
     "NEMA confirms 24 bodies recovered after the vessel capsized.", "AFP"),
    ("AFRICA", "EBOLA DEATH TOLL PASSES 5,700",
     "Containment still in doubt as the outbreak's toll keeps climbing.",
     "reports"),
    ("ASIA", "INDIA PILE UP 720/9 IN NEW ZEALAND",
     "Centuries by KL Rahul and Rishabh Pant set a record Test total "
     "on NZ soil.", "scorecard"),
]

ALSO = [
    ("ASIA", "EU and Indonesia sign CEPA trade and investment pacts, "
     "Brussels confirms.", "European Commission"),
    ("ASIA", "South Korea's president repeats a $75,000 reward for "
     "reporting exam cheating.", "reports"),
    ("EUROPE", "Finland probes a suspected Russian helicopter incursion "
     "up to 4.1 km into its airspace.", "ministry"),
    ("EUROPE", "Denmark expels Russia's military attache, named as a GRU "
     "officer, over a plot to kill a Ukrainian rapper.", "The Insider"),
    ("EUROPE", "Spain will extend its bank tax to fund housing, "
     "PM Sanchez says.", "reports"),
    ("EUROPE", "Thousands march in Lisbon against inflation and the "
     "cost of living.", "reports"),
    ("EUROPE", "France sees a fourth straight weekend of nationwide "
     "protests over living costs.", "reports"),
    ("EUROPE", "Crowds rally in Zagreb demanding answers over a "
     "psychiatric hospital death.", "reports"),
    ("EUROPE", "Costa Concordia captain Schettino walks free after "
     "serving nine years.", "reports"),
    ("EUROPE", "A Russian cargo ship catches fire and drifts into "
     "Finnish waters in the Gulf of Finland.", "Border Guard"),
    ("EUROPE", "Turkey's government takes control of the last big "
     "independent news outlet amid a fraud case.", "reports"),
    ("EUROPE", "Zelenskyy brands Putin a 'killer' after Trump calls "
     "the Russian leader his 'friend'.", "reports"),
    ("MIDDLE EAST", "Four Palestinians killed and 14 hurt in Gaza "
     "ceasefire breaches; Australia, Canada, Italy and the UK demand "
     "unrestricted aid access after floods.", "reports"),
    ("MIDDLE EAST", "Fire at Basra's Hartha power station kills 4 "
     "and injures 35.", "reports"),
    ("AFRICA", "Sudan's Tasis alliance says it has taken the "
     "strategic Bau area in Blue Nile.", "reports"),
    ("AMERICAS", "A man is convicted of arson over the deadly Pacific "
     "Palisades blaze after a retrial.", "court"),
    ("AMERICAS", "Virginia records its first child measles death "
     "since 1978.", "reports"),
    ("AMERICAS", "'We lost everything': Tupancireta, Brazil, clears "
     "rubble after a deadly storm.", "AFP"),
    ("AMERICAS", "Brazil's Jair Bolsonaro is in intensive care with "
     "gastrointestinal problems.", "reports"),
    ("AMERICAS", "US State Department details $12bn in Venezuelan "
     "oil and mineral revenue.", "State Dept"),
    ("GLOBAL", "UN talks agree to keep negotiating toward a 2028 "
     "pact on autonomous weapons.", "UN"),
    ("GLOBAL", "US lawmakers push to ban Chinese-made AI models "
     "from federal systems.", "reports"),
]

LEFT_OUT = ("Left out as other days' news: Nov 20 - Wall Street's "
            "correction and reports of an SEC probe into Nvidia; "
            "Nov 19 - the Shenzhen summit; Nov 18 - the US-Venezuela "
            "military pact announced in Caracas.")

CONTINENTS = ["ASIA", "MIDDLE EAST", "EUROPE", "AFRICA", "AMERICAS",
              "GLOBAL"]
CONT_STAT = {
    "ASIA": "39 missing in Serang fire",
    "MIDDLE EAST": "blockade day 130",
    "EUROPE": "4.1 km incursion probed",
    "AFRICA": "Ebola toll 5,700+",
    "AMERICAS": "Bitcoin back at $60k",
    "GLOBAL": "Voyager 1 light-day",
}

# ------------------------------------------------------------------ fonts
def font(size, bold=False, serif=False):
    names = []
    if serif:
        names = ["/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf",
                 "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"]
    elif bold:
        names = ["/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"]
    else:
        names = ["/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"]
    for n in names:
        try:
            return ImageFont.truetype(n, size)
        except OSError:
            continue
    return ImageFont.load_default()


def wrap(d, text, fnt, maxw):
    words, lines, cur = text.split(), [], ""
    for w_ in words:
        t = (cur + " " + w_).strip()
        if d.textlength(t, font=fnt) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w_
    if cur:
        lines.append(cur)
    return lines


def text_block(d, x, y, text, fnt, maxw, fill=INK, leading=1.18,
               max_lines=None):
    lines = wrap(d, text, fnt, maxw)
    if max_lines:
        lines = lines[:max_lines]
    step = int(fnt.size * leading)
    for ln in lines:
        d.text((x, y), ln, font=fnt, fill=fill)
        y += step
    return y


def num_badge(d, x, y, n, r=17):
    d.ellipse([x, y, x + 2 * r, y + 2 * r], fill=ACCENT)
    t = str(n)
    f = font(21, bold=True)
    tw = d.textlength(t, font=f)
    d.text((x + r - tw / 2, y + r - 12), t, font=f, fill=(255, 255, 255))


# ------------------------------------------------------------------ icons
def icon_globe(d, x, y, s):
    d.ellipse([x, y, x + s, y + s], outline=INK, width=4,
              fill=(168, 205, 225))
    d.arc([x + s * 0.22, y, x + s * 0.78, y + s], 90, 270, fill=INK, width=2)
    d.arc([x + s * 0.22, y, x + s * 0.78, y + s], 270, 90, fill=INK, width=2)
    d.line([x, y + s * 0.5, x + s, y + s * 0.5], fill=INK, width=2)
    tx = x + s * 0.78
    d.rectangle([tx, y + s * 0.42, tx + 10, y + s * 0.86], outline=ACCENT,
                width=4)
    d.ellipse([tx - 7, y + s * 0.8, tx + 17, y + s * 1.04], fill=ACCENT)


def icon_tanker(d, x, y, s):
    hull = [(x, y + s * 0.55), (x + s, y + s * 0.55), (x + s * 0.88,
            y + s * 0.8), (x + s * 0.1, y + s * 0.8)]
    d.polygon(hull, fill=(70, 74, 84))
    d.rectangle([x + s * 0.14, y + s * 0.34, x + s * 0.8, y + s * 0.55],
                fill=(196, 120, 60))
    d.rectangle([x + s * 0.8, y + s * 0.16, x + s * 0.9, y + s * 0.55],
                fill=(90, 94, 104))
    for i in range(5):
        cx = x + s * (0.2 + i * 0.16)
        d.line([cx, y + s * 0.88, cx + 12, y + s * 0.97], fill=(60, 110,
               170), width=4)
    d.line([x + s * 0.3, y + s * 0.2, x + s * 0.3, y + s * 0.34],
           fill=INK, width=3)
    d.polygon([(x + s * 0.3, y + s * 0.2), (x + s * 0.46, y + s * 0.26),
               (x + s * 0.3, y + s * 0.32)], fill=ACCENT)


def icon_factory(d, x, y, s):
    d.rectangle([x + s * 0.06, y + s * 0.45, x + s * 0.94, y + s * 0.92],
                fill=(110, 104, 96))
    d.polygon([(x + s * 0.06, y + s * 0.45), (x + s * 0.32, y + s * 0.28),
               (x + s * 0.58, y + s * 0.45)], fill=(80, 76, 70))
    d.rectangle([x + s * 0.68, y + s * 0.12, x + s * 0.8, y + s * 0.45],
                fill=(80, 76, 70))
    for r_ in range(2):
        for c_ in range(4):
            wx = x + s * (0.14 + c_ * 0.18)
            wy = y + s * (0.56 + r_ * 0.18)
            d.rectangle([wx, wy, wx + s * 0.1, wy + s * 0.1],
                        fill=(250, 214, 120))
    fx, fy = x + s * 0.42, y + s * 0.3
    d.polygon([(fx, fy), (fx + s * 0.1, fy - s * 0.2), (fx + s * 0.16,
              fy + s * 0.02), (fx + s * 0.24, fy - s * 0.12),
               (fx + s * 0.26, fy + s * 0.12), (fx + s * 0.02,
              fy + s * 0.12)], fill=(232, 110, 40))
    d.polygon([(fx + s * 0.07, fy + s * 0.1), (fx + s * 0.13, fy - s * 0.06),
               (fx + s * 0.2, fy + s * 0.1)], fill=(250, 190, 60))


def icon_quake(d, x, y, s):
    d.rectangle([x, y + s * 0.78, x + s, y + s * 0.84], fill=(120, 96, 70))
    pts = [(x + s * 0.08, y + s * 0.8), (x + s * 0.3, y + s * 0.62),
           (x + s * 0.42, y + s * 0.8), (x + s * 0.55, y + s * 0.55),
           (x + s * 0.68, y + s * 0.8), (x + s * 0.9, y + s * 0.66)]
    d.line(pts, fill=ACCENT, width=6)
    d.rectangle([x + s * 0.62, y + s * 0.18, x + s * 0.92, y + s * 0.52],
                outline=INK, width=4, fill=(210, 200, 180))
    d.line([x + s * 0.7, y + s * 0.52, x + s * 0.78, y + s * 0.36,
            x + s * 0.86, y + s * 0.52], fill=ACCENT, width=3)


def icon_flag_il(d, x, y, s):
    d.line([x + s * 0.14, y + s * 0.06, x + s * 0.14, y + s * 0.95],
           fill=INK, width=5)
    d.rectangle([x + s * 0.14, y + s * 0.08, x + s * 0.92, y + s * 0.52],
                fill=(245, 245, 245), outline=INK, width=2)
    d.rectangle([x + s * 0.14, y + s * 0.15, x + s * 0.92, y + s * 0.21],
                fill=(40, 80, 170))
    d.rectangle([x + s * 0.14, y + s * 0.39, x + s * 0.92, y + s * 0.45],
                fill=(40, 80, 170))
    cx, cy, r = x + s * 0.53, y + s * 0.3, s * 0.09
    for a in range(0, 360, 60):
        import math
        x1 = cx + r * math.cos(math.radians(a))
        y1 = cy + r * math.sin(math.radians(a))
        x2 = cx + r * math.cos(math.radians(a + 180))
        y2 = cy + r * math.sin(math.radians(a + 180))
        d.line([x1, y1, x2, y2], fill=(40, 80, 170), width=3)


def icon_badge(d, x, y, s):
    pts = []
    import math
    for i in range(10):
        a = math.radians(i * 36 - 90)
        r = s * 0.42 if i % 2 == 0 else s * 0.2
        pts.append((x + s / 2 + r * math.cos(a), y + s / 2 +
                    r * math.sin(a)))
    d.polygon(pts, fill=(232, 180, 60), outline=INK)
    d.text((x + s * 0.3, y + s * 0.36), "FBI", font=font(30, bold=True),
           fill=INK)


def icon_missile(d, x, y, s):
    d.polygon([(x + s * 0.62, y + s * 0.08), (x + s * 0.86, y + s * 0.3),
               (x + s * 0.5, y + s * 0.44), (x + s * 0.38, y + s * 0.32)],
              fill=(120, 124, 134))
    d.polygon([(x + s * 0.38, y + s * 0.32), (x + s * 0.2, y + s * 0.52),
               (x + s * 0.44, y + s * 0.5)], fill=ACCENT)
    d.polygon([(x + s * 0.14, y + s * 0.6), (x + s * 0.3, y + s * 0.52),
               (x + s * 0.26, y + s * 0.72), (x + s * 0.06, y + s * 0.78)],
              fill=(240, 150, 50))
    d.rectangle([x + s * 0.55, y + s * 0.78, x + s * 0.95, y + s * 0.92],
                fill=(110, 104, 96))
    d.rectangle([x + s * 0.62, y + s * 0.62, x + s * 0.74, y + s * 0.78],
                fill=(110, 104, 96))


def icon_chart(d, x, y, s):
    d.line([x + s * 0.08, y + s * 0.1, x + s * 0.08, y + s * 0.88],
           fill=INK, width=3)
    d.line([x + s * 0.08, y + s * 0.88, x + s * 0.95, y + s * 0.88],
           fill=INK, width=3)
    pts = [(x + s * 0.12, y + s * 0.66), (x + s * 0.34, y + s * 0.74),
           (x + s * 0.52, y + s * 0.5), (x + s * 0.7, y + s * 0.56),
           (x + s * 0.9, y + s * 0.22)]
    d.line(pts, fill=(30, 130, 60), width=6)
    d.polygon([(x + s * 0.9, y + s * 0.22), (x + s * 0.78, y + s * 0.24),
               (x + s * 0.88, y + s * 0.36)], fill=(30, 130, 60))
    d.text((x + s * 0.3, y + s * 0.06), "$60k", font=font(34, bold=True),
           fill=(30, 130, 60))


def icon_probe(d, x, y, s):
    d.rectangle([x + s * 0.36, y + s * 0.4, x + s * 0.62, y + s * 0.62],
                fill=(200, 170, 90), outline=INK, width=3)
    d.polygon([(x + s * 0.36, y + s * 0.5), (x + s * 0.06, y + s * 0.3),
               (x + s * 0.06, y + s * 0.62)], fill=(90, 120, 190))
    d.polygon([(x + s * 0.62, y + s * 0.5), (x + s * 0.94, y + s * 0.3),
               (x + s * 0.94, y + s * 0.62)], fill=(90, 120, 190))
    d.line([x + s * 0.49, y + s * 0.4, x + s * 0.49, y + s * 0.16],
           fill=INK, width=3)
    d.ellipse([x + s * 0.4, y + s * 0.04, x + s * 0.58, y + s * 0.18],
              outline=INK, width=3)
    for sx, sy in [(0.12, 0.14), (0.85, 0.12), (0.7, 0.82), (0.2, 0.85)]:
        d.text((x + s * sx, y + s * sy), "*", font=font(30, bold=True),
               fill=(120, 120, 160))


def icon_boat(d, x, y, s):
    d.polygon([(x + s * 0.3, y + s * 0.3), (x + s * 0.62, y + s * 0.52),
               (x + s * 0.2, y + s * 0.56)], fill=(150, 90, 50))
    d.line([x + s * 0.3, y + s * 0.3, x + s * 0.28, y + s * 0.62],
           fill=INK, width=4)
    for i in range(4):
        wy = y + s * (0.72 + i * 0.07)
        d.arc([x + s * (0.06 + i * 0.05), wy, x + s * (0.5 + i * 0.05),
               wy + s * 0.12], 0, 180, fill=(60, 110, 170), width=4)
        d.arc([x + s * (0.45 + i * 0.05), wy, x + s * (0.9 + i * 0.03),
               wy + s * 0.12], 0, 180, fill=(60, 110, 170), width=4)


def icon_virus(d, x, y, s):
    import math
    cx, cy, r = x + s / 2, y + s / 2, s * 0.26
    for a in range(0, 360, 36):
        x1 = cx + r * math.cos(math.radians(a))
        y1 = cy + r * math.sin(math.radians(a))
        x2 = cx + (r + s * 0.16) * math.cos(math.radians(a))
        y2 = cy + (r + s * 0.16) * math.sin(math.radians(a))
        d.line([x1, y1, x2, y2], fill=ACCENT, width=5)
        d.ellipse([x2 - 7, y2 - 7, x2 + 7, y2 + 7], fill=ACCENT)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(196, 90, 80),
              outline=ACCENT, width=3)


def icon_cricket(d, x, y, s):
    d.polygon([(x + s * 0.2, y + s * 0.85), (x + s * 0.34, y + s * 0.78),
               (x + s * 0.78, y + s * 0.2), (x + s * 0.66, y + s * 0.1)],
              fill=(190, 150, 90))
    d.ellipse([x + s * 0.62, y + s * 0.58, x + s * 0.88, y + s * 0.84],
              fill=ACCENT)
    d.arc([x + s * 0.66, y + s * 0.62, x + s * 0.84, y + s * 0.8], 300,
          120, fill=(255, 255, 255), width=3)

# -------------------------------------------------------------------- map
def lonlat(bx, by, bw, bh, lon, lat):
    return (bx + (lon + 180) / 360 * bw, by + (90 - lat) / 180 * bh)


CONTINENT_POLYS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 80), (-85, 70),
     (-80, 73), (-75, 62), (-65, 60), (-55, 52), (-65, 45), (-70, 42),
     (-75, 35), (-80, 26), (-84, 20), (-90, 15), (-97, 16), (-105, 20),
     (-110, 23), (-114, 29), (-120, 34), (-124, 40), (-124, 48),
     (-132, 55), (-152, 60), (-165, 60)],
    [(-77, 7), (-70, 11), (-62, 10), (-52, 5), (-50, 0), (-44, -3),
     (-35, -8), (-39, -13), (-40, -22), (-48, -27), (-52, -33),
     (-57, -38), (-62, -41), (-65, -45), (-67, -50), (-68, -54),
     (-71, -54), (-73, -50), (-73, -44), (-72, -37), (-70, -30),
     (-70, -20), (-75, -15), (-79, -8), (-81, -4), (-80, 1)],
    [(-17, 15), (-10, 29), (0, 35), (10, 37), (11, 34), (20, 32),
     (30, 31), (32, 31), (35, 28), (38, 22), (43, 12), (48, 11),
     (51, 12), (46, 5), (42, -2), (40, -10), (38, -18), (36, -22),
     (33, -26), (28, -33), (20, -35), (17, -32), (14, -22), (12, -15),
     (13, -5), (9, -1), (9, 4), (-8, 4), (-13, 8), (-17, 12)],
    [(-10, 36), (-9, 43), (-2, 44), (0, 46), (3, 43), (8, 44),
     (12, 46), (16, 45), (20, 42), (24, 40), (28, 41), (30, 46),
     (26, 48), (28, 50), (24, 54), (21, 59), (24, 65), (31, 70),
     (45, 68), (55, 66), (48, 60), (40, 55), (32, 52), (24, 50),
     (18, 56), (12, 54), (8, 55), (5, 58), (10, 59), (18, 59),
     (21, 55), (14, 50), (6, 50), (0, 48), (-5, 48), (-2, 44)],
    [(30, 41), (36, 36), (42, 35), (44, 29), (48, 30), (50, 29),
     (55, 26), (60, 25), (66, 25), (72, 20), (77, 8), (80, 15),
     (86, 20), (90, 20), (92, 15), (97, 16), (100, 12), (103, 8),
     (105, 5), (108, 8), (110, 15), (115, 20), (120, 25), (122, 31),
     (129, 33), (135, 35), (140, 40), (142, 45), (150, 50), (158, 55),
     (162, 60), (178, 66), (178, 62), (162, 68), (150, 70), (135, 70),
     (120, 68), (110, 66), (100, 64), (90, 62), (80, 60), (70, 58),
     (60, 55), (50, 52), (40, 50), (32, 46)],
    [(113, -22), (114, -30), (115, -34), (118, -35), (124, -33),
     (129, -32), (132, -32), (135, -35), (138, -36), (140, -38),
     (145, -38), (147, -38), (150, -37), (153, -32), (153, -27),
     (151, -24), (146, -19), (142, -15), (142, -11), (146, -11),
     (143, -14), (141, -17), (140, -18), (136, -15), (135, -12),
     (132, -11), (130, -12), (126, -14), (122, -17), (118, -20)],
    [(167, -45), (170, -44), (172, -43), (174, -41), (176, -38),
     (174, -37), (172, -40), (169, -43), (167, -46)],
]

PINS = [  # (number, lon, lat) for the 13 illustrated stories
    (1, 30.7, 36.9), (2, 53.0, 32.0), (3, 106.2, -6.1), (4, -75.2, -9.2),
    (5, 34.9, 31.9), (6, -107.5, 25.0), (7, 33.4, 47.9), (8, -74.0, 40.7),
    (9, 58.5, 23.6), (11, 7.5, 9.0), (12, 15.0, -1.0), (13, 174.8, -41.3),
]


def draw_map(d, bx, by, bw, bh):
    d.rectangle([bx, by, bx + bw, by + bh], fill=(222, 233, 240),
                outline=RULE, width=3)
    for poly in CONTINENT_POLYS:
        pts = [lonlat(bx, by, bw, bh, lo, la) for lo, la in poly]
        d.polygon(pts, fill=(196, 208, 172), outline=(110, 120, 96))
    for n, lo, la in PINS:
        px, py = lonlat(bx, by, bw, bh, lo, la)
        d.ellipse([px - 15, py - 15, px + 15, py + 15], fill=ACCENT)
        t = str(n)
        f = font(19, bold=True)
        d.text((px - d.textlength(t, font=f) / 2, py - 11), t, font=f,
               fill=(255, 255, 255))
    # story 10 (Voyager) lives in deep space: a star at the box corner
    sx, sy = bx + bw - 46, by + 26
    d.text((sx, sy), "*", font=font(44, bold=True), fill=ACCENT)
    d.ellipse([sx + 26, sy - 6, sx + 56, sy + 24], fill=ACCENT)
    f = font(19, bold=True)
    d.text((sx + 33, sy - 3), "10", font=f, fill=(255, 255, 255))


# ----------------------------------------------------------------- panels
def panel_frame(d, x, y, w, h, n, cont):
    d.rectangle([x, y, x + w, y + h], fill=PANEL_BG, outline=RULE, width=3)
    num_badge(d, x + 12, y + 12, n)
    d.text((x + 58, y + 16), cont, font=font(20, bold=True), fill=ACCENT)


def lead_panel(d, x, y, w, h, n, story, icon):
    cont, head, body, src = story
    panel_frame(d, x, y, w, h, n, cont)
    icon(d, x + w / 2 - 110, y + 58, 220)
    yy = text_block(d, x + 24, y + 300, head, font(37, bold=True), w - 48,
                    leading=1.12)
    yy = text_block(d, x + 24, yy + 10, body, font(27), w - 48,
                    leading=1.22)
    d.text((x + 24, y + h - 40), "(" + src + ")", font=font(21),
           fill=RULE)


def mini_panel(d, x, y, w, h, n, story, icon):
    cont, head, body, src = story
    panel_frame(d, x, y, w, h, n, cont)
    icon(d, x + w - 138, y + 52, 112)
    yy = text_block(d, x + 16, y + 56, head, font(26, bold=True), w - 176,
                    leading=1.12, max_lines=5)
    text_block(d, x + 16, max(yy + 6, y + 268), body, font(23), w - 32,
               leading=1.18, max_lines=4)


LEAD_ICONS = [icon_globe, icon_tanker, icon_factory]
MINI_ICONS = [icon_quake, icon_flag_il, icon_badge, icon_missile,
              icon_chart, icon_tanker, icon_probe, icon_boat, icon_virus,
              icon_cricket]


# ------------------------------------------------------------------- main
def build(path):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    M = 48

    # masthead
    title = "THE WORLD IN ONE PAGE"
    f_title = font(96, bold=True, serif=True)
    d.text(((W - d.textlength(title, font=f_title)) / 2, 30), title,
           font=f_title, fill=INK)
    d.line([M, 152, W - M, 152], fill=INK, width=5)
    d.line([M, 162, W - M, 162], fill=INK, width=2)
    f_date = font(30, bold=True)
    d.text((M, 176), "SUNDAY, NOVEMBER 22, 2026", font=f_date, fill=INK)
    note = "Every story first reported today · No. 22"
    d.text((W - M - d.textlength(note, font=f_date), 176), note,
           font=f_date, fill=RULE)

    # continent stat bar
    counts = {c: 0 for c in CONTINENTS}
    for s_ in LEADS + MINIS + ALSO:
        counts[s_[0]] += 1
    by0, bh = 224, 108
    cw = (W - 2 * M) / 6
    d.rectangle([M, by0, W - M, by0 + bh], fill=SHADE, outline=RULE,
                width=2)
    for i, c in enumerate(CONTINENTS):
        cx = M + i * cw
        if i:
            d.line([cx, by0, cx, by0 + bh], fill=RULE, width=2)
        d.text((cx + 14, by0 + 8), c, font=font(19, bold=True), fill=INK)
        d.text((cx + 14, by0 + 30), str(counts[c]), font=font(40, bold=True),
               fill=ACCENT)
        d.text((cx + 80, by0 + 62), CONT_STAT[c], font=font(19), fill=INK)

    # lead row
    ly, lh, gap = 356, 660, 24
    lw = (W - 2 * M - 2 * gap) / 3
    for i, story in enumerate(LEADS):
        lead_panel(d, M + i * (lw + gap), ly, lw, lh, i + 1, story,
                   LEAD_ICONS[i])

    # mini rows (5 + 5)
    my, mh, mgap = 1040, 430, 20
    mw = (W - 2 * M - 4 * mgap) / 5
    for i, story in enumerate(MINIS):
        row, col = divmod(i, 5)
        mini_panel(d, M + col * (mw + mgap), my + row * (mh + mgap), mw,
                   mh, 4 + i, story, MINI_ICONS[i])

    # bottom: map (left) + ALSO column (right)
    byy, bhh = 1950, 916
    d.text((M, byy), "WHERE IT HAPPENED", font=font(30, bold=True),
           fill=INK)
    draw_map(d, M, byy + 44, 880, bhh - 44)
    ax = M + 880 + 24
    aw = W - M - ax
    d.text((ax, byy), "ALSO ON SUNDAY", font=font(30, bold=True), fill=INK)
    colw = (aw - 24) / 2
    f_also = font(24)
    for j, (cont, txt, src) in enumerate(ALSO):
        col, row = divmod(j, 11)
        cx = ax + col * (colw + 24)
        cy = byy + 52 + row * 79
        n = 14 + j
        d.text((cx, cy), str(n) + ".", font=font(24, bold=True),
               fill=ACCENT)
        text_block(d, cx + 44, cy, txt + " (" + src + ")", f_also,
                   colw - 44, leading=1.14, max_lines=3)

    # footer
    fy = 2900
    d.line([M, fy, W - M, fy], fill=INK, width=3)
    d.text((M, fy + 14), "DATE CHECK \u2713  All 35 stories happened or "
           "were first reported on Sunday, November 22, 2026.",
           font=font(26, bold=True), fill=INK)
    text_block(d, M, fy + 58, LEFT_OUT, font(23), W - 2 * M, fill=RULE,
               leading=1.2)
    d.text((M, fy + 128), "Claims are attributed, not stated as fact · "
           "Pictures and map: original, drawn in code",
           font=font(23), fill=RULE)

    img.save(path)
    return path


if __name__ == "__main__":
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    print(build(out))
