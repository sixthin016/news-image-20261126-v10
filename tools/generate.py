#!/usr/bin/env python3
"""v10 renderer - news-image-20261126 (copy of v9, re-slatted).

v10 changes (dissection v10: top-1 migasmin 99.1692%, #2 yossapr 99.1559%,
v9 live rank 778 / 98.4958% - REGRESSED from v8 rank 16 / 98.7076%):
1. DATE FENCING FLIPPED to the top-1/top-2 camp. v8/v9 led with TWO
   25-Nov events as 26-Nov news: the Cairo tanker fire (Wed 25 Nov
   19:08 EGY, 31 dead - verified: Wikipedia/CNN/AP/Al Jazeera) and the
   Shenzhou-24 docking (25 Nov). Top-1 migasmin and #2 yossapr BOTH
   exclude Cairo + Shenzhou + the Solomons treaty signing (Wed 25 Nov)
   + the Ras Tanura claim + the Dhaka wage announcement as 25 Nov.
   v10 moves all five into DATE CHECK and leads with three
   unambiguous 26-Nov stories: Trump tariffs (OFFICIAL), Macy's
   postponement (CONFIRMED), Kyiv overnight missiles (CONFIRMED).
2. DENSITY 35 -> 48 stories (13 pictured + 35 also, like migasmin),
   stat strip 4 -> 6 numbers, also-list 2 cols -> 3 cols.
3. PANELS all hard news: Gaza, Hormuz, Ebola 12,021, EU budget,
   Korea 3.25%, Dhaka factories SHUT (the 26-Nov angle - the wage
   announcement itself was 25 Nov), KL Google, Constitution Day,
   Guinea-Bissau vote->2028 (Africa in panels), Nvidia halt.
   War 3, Health 1, Politics 3, Economy 1, Labour 1, Tech/AI 2.
4. NEW ART, multi-element: tariff bars, Kyiv night skyline +
   missile trails, enriched Macy's (rain), Ebola clinic, EU stars,
   rate chart, shuttered factory, ballot box, Nvidia chip.
5. WHY IT MATTERS line under each lead (migasmin pattern).
6. REGION BAR rebalanced: NA 8, SA 4, EU 8, ME 4, SAsia 11, EA 5,
   OC 2, AF 4, Global 2 (v9: EU 8, OC 1, AF 1, Global 2).
7. VERIFICATION FIX (27 Nov, sesi verifikasi): ALSO #43 Bangladesh
   "BNP clash: 1 dead" diganti BOGOR "Mine flood kills 16"
   (Disaster, AP, SAsia) - angka strip "16 BOGOR DEAD" sebelumnya
   tidak punya cerita di halaman (migasmin mempicturenya sebagai
   panel 11); kini ke-6 angka strip didukung cerita di halaman.
   Region counts tidak berubah (SAsia->SAsia); Politics tetap ada;
   Daily Star keluar dari sumber (21 -> 20 sumber).
New facts verified by web 27 Nov: Guinea-Bissau delay to Nov 2028
(Reuters/AP, Thu 26 Nov); Ebola 12,021 cases / 5,904 dead (Reuters,
Thu 26 Nov, 2nd-largest outbreak); BOK 3.25%, 5-2 vote, 2027 outlook
4.1% (Reuters/WSJ, Thu 26 Nov); Bogor 16 dead, 10 missing (West Java
police via AP, Thu 26 Nov); Nvidia halt to MY/SG/TH/ID (FT via
Reuters, Thu 26 Nov). Stdlib + PIL only. Deterministic: no random
(unseeded), no wall clock, no network.
"""
import hashlib
import os
import sys
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (247, 243, 232)
INK = (26, 26, 26)
NAVY = (27, 42, 74)
RED = (176, 30, 36)
GOLD = (201, 162, 39)
SEA = (191, 212, 222)
LAND = (227, 211, 168)
GREY = (90, 90, 86)
LGREY = (230, 226, 216)

FD = "/usr/share/fonts/truetype/dejavu"
FD_NOTO = "/usr/share/fonts/truetype/noto"
def F(size, bold=False, serif=True, italic=False):
    if serif and italic:
        return ImageFont.truetype(os.path.join(FD_NOTO, "NotoSerif-Italic.ttf"), size)
    if serif:
        name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
    else:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FD, name), size)

def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def fit(draw, text, font, maxw, maxlines):
    """Wrap text; return lines, asserting it fits in maxlines."""
    lines = wrap(draw, text, font, maxw)
    assert len(lines) <= maxlines, "OVERFLOW %r -> %d lines (max %d)" % (
        text[:40], len(lines), maxlines)
    return lines

def tw(draw, text, font):
    return draw.textlength(text, font=font)

# ---------------------------------------------------------------- slate
# num, place, region, field, kicker, headline, body, why, source, badge, art
LEADS = [
    dict(num=1, place="WASHINGTON, USA", region="NA", field="Trade",
         badge="OFFICIAL",
         head="TRUMP UNVEILS TARIFFS ON 14 PARTNERS",
         body=("Section 301 cases: China up to 20%, Vietnam 35%, "
               "India 25%."),
         why="Rewrites US trade terms at once.",
         src="Reuters \u00b7 AP", art="tariffs"),
    dict(num=2, place="NEW YORK, USA", region="NA", field="Holiday",
         badge="CONFIRMED",
         head="MACY'S 100TH PARADE POSTPONED TO SATURDAY",
         body=("A nor'easter brings 50\u201360 mph gusts, grounding the "
               "balloons. The 100th parade steps off Saturday at 08:30 ET "
               "instead \u2014 the first postponement in its 100-year history."),
         why="A first in the parade's 100 years.",
         src="AP \u00b7 Reuters", art="balloon"),
    dict(num=3, place="KYIV, UKRAINE", region="EU", field="War",
         badge="CONFIRMED",
         head="RUSSIA'S MISSILES POUND KYIV OVERNIGHT",
         body=("Missiles and drones hit the capital overnight; seven "
               "wounded, grain ships hit near Odesa."),
         why="Moscow vows more strikes in reply.",
         src="Reuters", art="kyiv"),
]

PANELS = [
    dict(num=4, place="GAZA CITY", region="ME", field="War",
         badge="CONFIRMED",
         head="Israeli strike kills Hamas security chief in Gaza",
         body="Abuelouf dies with his wife and two daughters; second chief in 24 hours.",
         src="AP", art="burst"),
    dict(num=5, place="STRAIT OF HORMUZ", region="ME", field="War",
         badge="REPORTED",
         head="Two tankers hit naval mines in Strait of Hormuz",
         body="Iran says the tankers exploded and caught fire on an unauthorised route.",
         src="Reuters", art="mine"),
    dict(num=6, place="DR CONGO", region="AF", field="Health",
         badge="OFFICIAL",
         head="Congo's Ebola outbreak passes 12,000 cases",
         body="12,021 confirmed, 5,904 dead; the second-largest outbreak on record.",
         src="Reuters", art="ebola"),
    dict(num=7, place="BRUSSELS", region="EU", field="Politics",
         badge="CONFIRMED",
         head="EU haggling over \u20ac1.7tn budget",
         body="Leaders meet for two days; \u20ac45bn more for Ukraine is on the table.",
         src="Euronews", art="budget"),
    dict(num=8, place="SEOUL", region="EA", field="Economy",
         badge="OFFICIAL",
         head="Bank of Korea raises rates to 3.25%",
         body="A 25-point hike on a 5\u20132 vote; 2027 outlook lifted to 4.1%.",
         src="Reuters \u00b7 Yonhap", art="rate"),
    dict(num=9, place="DHAKA, BANGLADESH", region="SAsia", field="Labour",
         badge="REPORTED",
         head="400 Bangladesh garment factories stay shut",
         body="Workers reject the new 17,000-taka wage; police fire tear gas.",
         src="AFP", art="shut"),
    dict(num=10, place="KUALA LUMPUR", region="SAsia", field="Tech/AI",
         badge="CONFIRMED",
         head="Malaysia sues Google for $146m over YouTube",
         body="Harmful content \u2014 gambling, scams, fraud \u2014 was left up.",
         src="Reuters", art="gavel"),
    dict(num=11, place="NEW DELHI, INDIA", region="SAsia", field="Politics",
         badge="CONFIRMED",
         head="India marks 77 years of its Constitution",
         body="The charter adopted in 1949 turns 77; events mark the day nationwide.",
         src="PTI", art="charter"),
    dict(num=12, place="BISSAU", region="AF", field="Politics",
         badge="OFFICIAL",
         head="Guinea-Bissau junta delays vote to 2028",
         body="Junta scraps December vote a year after its coup; new date: Nov 2028.",
         src="Reuters", art="guinea"),
    dict(num=13, place="SOUTHEAST ASIA", region="SAsia", field="Tech/AI",
         badge="REPORTED",
         head="Nvidia halts AI servers to 4 nations",
         body="Dell and Supermicro told to halt orders, FT reports.",
         src="Reuters", art="nvidia"),
]

# num, place, field, text, source, region - terse, one line each.
ALSO = [
    (14, "ODESA", "War", "Power cut in five regions", "Reuters", "EU"),
    (15, "RUSSIA", "War", "War dead put at 490,334", "BBC", "EU"),
    (16, "COLOMBIA", "Crime", "25 hostages freed", "France24", "SA"),
    (17, "CANARIES", "Migration", "Record 2,121 arrive", "AP", "EU"),
    (18, "MUMBAI", "Crime", "18 years since 26/11", "PTI", "SAsia"),
    (19, "CANADA", "Economy", "Confidence 2-year high", "CBC", "NA"),
    (20, "US", "Tech/AI", "Nasdaq slides on AI fears", "Reuters", "NA"),
    (21, "US", "Politics", "AG dodges Nvidia probe", "AP", "NA"),
    (22, "COLOMBIA", "Politics", "Peace deal at 10", "UN", "SA"),
    (23, "VENEZUELA", "Economy", "Debt put at $237.5bn", "Reuters", "SA"),
    (24, "GENEVA", "Sport", "Gukesh\u2013Sindarov, Game 3", "FIDE", "Global"),
    (25, "INDIA", "Diplomacy", "\u20b915,000cr aid for Nepal", "PTI", "SAsia"),
    (26, "N. KOREA", "Diplomacy", "Swiss office shut", "AP", "EA"),
    (27, "SUDAN", "War", "Drone strikes kill 19", "Reuters", "AF"),
    (28, "GENEVA", "Health", "WHO: HIV fight strained", "WHO", "Global"),
    (29, "IOWA", "Defence", "Army blows up 5t explosives", "Al Jazeera", "NA"),
    (30, "UZHHOROD", "Politics", "Meets Magyar", "AP", "EU"),
    (31, "INDIA", "Sport", "Sooryavanshi 204 off 53", "Cricinfo", "SAsia"),
    (32, "INDIA", "Sport", "1,220 in IPL auction", "IPL", "SAsia"),
    (33, "HONG KONG", "Disaster", "Wang Fuk: a year on", "Euronews", "EA"),
    (34, "BEIJING", "Politics", "18 golf courses shut", "AFP", "EA"),
    (35, "N. KOREA", "Politics", "Kim tours nuclear sites", "Euronews", "EA"),
    (36, "UKRAINE", "War", "Kyiv: laser downed jet drone", "Euromaidan", "EU"),
    (37, "POLAND", "Defence", "NATO sends AWACS planes", "Euronews", "EU"),
    (38, "NIGER", "Crime", "Saudi kidnapped by 15 men", "Reuters", "AF"),
    (39, "HODEIDAH", "War", "Coalition strikes back", "Reuters", "ME"),
    (40, "PALM BEACH", "Labour", "Ferries on strike", "NSW Govt", "OC"),
    (41, "BEIRUT", "Crime", "Minibus shootout kills 2", "L'Orient", "ME"),
    (42, "PAKISTAN", "Diplomacy", "Pact talks set", "Reuters", "SAsia"),
    (43, "BOGOR", "Disaster", "Mine flood kills 16", "AP", "SAsia"),
    (44, "N. ZEALAND", "Politics", "Luxon loses majority", "RNZ", "OC"),
    (45, "ARGENTINA", "Economy", "Technical recession", "Euronews", "SA"),
    (46, "MEXICO", "Diplomacy", "US talks, SpaceX debris", "Al Jazeera", "NA"),
    (47, "PHILADELPHIA", "Weather", "Parade cancelled", "WHYY", "NA"),
    (48, "BANGKOK", "Disaster", "Oil-plant blast, 9 hurt", "AP", "SAsia"),
]
TIMELINE = [
    ("OVERNIGHT", "KYIV \u2014 Biggest air attack on the capital"),
    ("c. 01:00 UTC", "HONG KONG \u2014 Families return to Wang Fuk"),
    ("06:00 UTC", "DELHI \u2014 India wakes to Constitution Day"),
    ("09:00 UTC", "BRUSSELS \u2014 Euro Summit opens; Ukraine aid"),
    ("13:30 UTC", "NEW YORK \u2014 Macy's parade due; postponed"),
    ("14:00 UTC", "GENEVA \u2014 Gukesh\u2013Sindarov, Game 3"),
]

DATECHECK_OUT = [
    ("Cairo fuel-tanker fire", "Wed 25 Nov"),
    ("Shenzhou-24 docks at Tiangong", "25 Nov"),
    ("Australia\u2013Solomons treaty signed", "25 Nov"),
    ("Houthi strike on Ras Tanura", "25 Nov"),
    ("Dhaka wage announcement", "25 Nov"),
    ("COP31 ends without a pact", "22 Nov"),
]

REGIONS = [("NA", "North America", (27, 42, 74)),
           ("SA", "South America", (120, 90, 40)),
           ("EU", "Europe", (90, 60, 140)),
           ("ME", "Middle East", (176, 30, 36)),
           ("SAsia", "South Asia", (200, 120, 30)),
           ("EA", "East Asia", (40, 120, 90)),
           ("OC", "Oceania", (60, 140, 160)),
           ("AF", "Africa", (150, 100, 40)),
           ("Global", "Global", (110, 110, 110))]
REGION_ORDER = ["NA", "SA", "EU", "ME", "SAsia", "EA", "OC", "AF", "Global"]
# region per story 1..48 (verified against slate; counts NA 8, SA 4, EU 8,
# ME 4, SAsia 11, EA 5, OC 2, AF 4, Global 2)
FULL_REGIONS = ["NA", "NA", "EU", "ME", "ME", "AF", "EU", "EA",
                "SAsia", "SAsia", "SAsia", "AF", "SAsia",
                "EU", "EU", "SA", "EU", "SAsia", "NA", "NA", "NA",
                "SA", "SA", "Global", "SAsia", "EA", "AF", "Global",
                "NA", "EU", "SAsia", "SAsia", "EA", "EA", "EA",
                "EU", "EU", "AF", "ME", "OC", "ME", "SAsia", "SAsia",
                "OC", "SA", "NA", "NA", "SAsia"]

# lat/lon pins 1-13 (leads + panels; v10: 1 DC, 2 NY, 3 Kyiv, 4 Gaza,
# 5 Hormuz, 6 Ituri, 7 Brussels, 8 Seoul, 9 Dhaka, 10 KL, 11 Delhi,
# 12 Bissau, 13 Singapore)
PINS = [(38.9, -77.0), (40.7, -74.0), (50.4, 30.5), (31.5, 34.4),
        (26.5, 56.5), (1.6, 30.2), (50.85, 4.35), (37.57, 126.98),
        (23.8, 90.4), (3.1, 101.7), (28.6, 77.2), (11.86, -15.58),
        (1.35, 103.8)]
# manual pixel nudges for colliding pins (index: dx, dy)
PIN_NUDGE = {0: (8, -6), 1: (-12, 8), 2: (-2, -8), 3: (10, 8),
             4: (20, 2), 5: (-10, 8), 6: (-10, 8), 8: (12, 0),
             9: (-10, 10), 10: (-16, -12), 12: (14, 4)}

# rough continent outlines (lon, lat) - drawn from scratch
CONTINENTS = [
    [(-168, 66), (-140, 70), (-125, 72), (-110, 73), (-95, 80), (-85, 80),
     (-80, 73), (-75, 72), (-70, 62), (-65, 60), (-55, 52), (-60, 47),
     (-70, 42), (-75, 35), (-80, 26), (-85, 30), (-90, 21), (-95, 19),
     (-100, 16), (-105, 20), (-110, 23), (-115, 30), (-125, 40),
     (-125, 48), (-140, 60), (-155, 58), (-165, 60)],
    [(-80, 10), (-75, 11), (-70, 12), (-62, 10), (-55, 6), (-50, 0),
     (-45, -5), (-35, -8), (-40, -20), (-48, -28), (-55, -35), (-65, -40),
     (-70, -50), (-70, -55), (-75, -45), (-75, -30), (-80, -18), (-80, -5)],
    [(-17, 15), (-10, 30), (0, 35), (10, 37), (20, 32), (30, 31),
     (35, 28), (40, 15), (48, 11), (51, 10), (45, 0), (40, -10),
     (35, -20), (30, -30), (20, -35), (15, -30), (12, -18), (13, -10),
     (10, 0), (5, 5), (-5, 5), (-12, 8)],
    [(-10, 36), (-9, 43), (-2, 48), (0, 50), (5, 53), (8, 57), (10, 59),
     (18, 56), (21, 55), (24, 58), (28, 60), (30, 60), (28, 55), (25, 50),
     (23, 45), (20, 40), (15, 38), (12, 44), (8, 44), (3, 42), (-2, 37)],
    [(30, 60), (40, 68), (50, 70), (60, 70), (70, 72), (80, 73), (90, 75),
     (100, 77), (110, 76), (120, 73), (130, 72), (140, 72), (150, 70),
     (160, 66), (162, 60), (158, 52), (150, 60), (142, 55), (140, 45),
     (135, 43), (130, 38), (127, 35), (122, 32), (120, 25), (115, 22),
     (110, 20), (105, 10), (100, 8), (98, 15), (95, 20), (92, 22),
     (88, 22), (85, 18), (80, 15), (77, 8), (75, 12), (70, 20), (65, 25),
     (60, 25), (55, 26), (50, 29), (48, 30), (45, 28), (42, 25), (40, 30),
     (38, 36), (35, 36), (33, 40), (30, 42), (28, 45), (30, 50), (30, 55)],
    [(113, -22), (114, -30), (115, -35), (120, -34), (125, -32), (130, -32),
     (135, -35), (140, -38), (145, -38), (150, -37), (153, -32), (153, -27),
     (150, -22), (146, -19), (142, -11), (137, -12), (135, -15), (132, -12),
     (130, -13), (126, -14), (122, -17), (118, -20)],
]

# ---------------------------------------------------------------- art
def badge(draw, x, y, text, size=9):
    f = F(size, bold=True, serif=False)
    w = draw.textlength(text, font=f) + 8
    draw.rounded_rectangle([x, y, x + w, y + size + 5], radius=2,
                           outline=RED, width=1)
    draw.text((x + 4, y + 2), text, font=f, fill=RED)
    return w

def star(draw, cx, cy, r, fill):
    pts = []
    import math
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)

def lead_art(draw, kind, x, y, w, h):
    """Flat illustration inside (x, y, w, h). h = 84."""
    if kind == "balloon":
        draw.rectangle([x, y, x + w, y + h], fill=(220, 233, 242))
        # v10: rain streaks over the skyline (seeded, deterministic)
        import random
        rnd = random.Random(26)
        for _ in range(16):
            rx = x + rnd.randint(6, w - 6)
            ry = y + rnd.randint(2, 44)
            draw.line([rx, ry, rx - 4, ry + 9], fill=(140, 175, 205), width=1)
        for i, bh in enumerate([20, 32, 24, 36, 28, 18]):
            bx = x + 8 + i * 52
            draw.rectangle([bx, y + h - 6 - bh, bx + 40, y + h - 6],
                           fill=(27, 42, 74))
            for wy in range(2):
                draw.rectangle([bx + 8, y + h - 6 - bh + 5 + wy * 9,
                                bx + 14, y + h - 6 - bh + 10 + wy * 9],
                               fill=(245, 220, 120))
        cx, cy = x + w // 2, y + 36
        draw.ellipse([cx - 46, cy - 28, cx + 46, cy + 28], fill=(192, 57, 43))
        draw.ellipse([cx - 46, cy - 28, cx - 6, cy + 28], fill=(214, 80, 62))
        draw.line([cx - 26, cy + 28, cx - 16, cy + 38], fill=(90, 60, 40), width=2)
        draw.line([cx + 26, cy + 28, cx + 16, cy + 38], fill=(90, 60, 40), width=2)
        draw.rectangle([cx - 16, cy + 38, cx + 16, cy + 46], fill=(120, 80, 50))
        draw.text((x + w - 44, y + 4), "100",
                  font=F(18, bold=True, serif=False), fill=(255, 255, 255))
    elif kind == "tariffs":
        # v10: tariff-rate bars - CHINA 20, INDIA 25, EU 15, JAPAN 15
        draw.rectangle([x, y, x + w, y + h], fill=(232, 228, 216))
        draw.rectangle([x, y, x + 118, y + 16], fill=RED)
        draw.text((x + 8, y + 2), "14 PARTNERS",
                  font=F(10, bold=True, serif=False), fill=(255, 255, 255))
        vals = [("CHINA", 20), ("INDIA", 25), ("EU", 15), ("JAPAN", 15)]
        base = y + h - 14
        for i, (name, v) in enumerate(vals):
            bx = x + 26 + i * 74
            bh = int(v * 1.6)
            draw.rectangle([bx, base - bh, bx + 36, base], fill=NAVY)
            draw.text((bx + 18 - tw(draw, "%d%%" % v, F(10, bold=True, serif=False)) / 2,
                       base - bh - 13), "%d%%" % v,
                      font=F(10, bold=True, serif=False), fill=RED)
            draw.text((bx + 18 - tw(draw, name, F(8, bold=True, serif=False)) / 2,
                       base + 2), name,
                      font=F(8, bold=True, serif=False), fill=INK)
        draw.line([x + 14, base, x + w - 14, base], fill=(150, 145, 130), width=1)
    elif kind == "kyiv":
        # v10: night skyline + missile trails
        draw.rectangle([x, y, x + w, y + h], fill=(18, 30, 44))
        import random
        rnd = random.Random(26)
        for _ in range(22):
            sx, sy = x + rnd.randint(4, w - 4), y + rnd.randint(4, h - 34)
            draw.ellipse([sx, sy, sx + 2, sy + 2], fill=(255, 255, 255))
        for i, bh in enumerate([18, 30, 22, 34, 26, 16, 24]):
            bx = x + 6 + i * 46
            draw.rectangle([bx, y + h - 6 - bh, bx + 36, y + h - 6],
                           fill=(10, 16, 28))
            for wy in range(2):
                draw.rectangle([bx + 7, y + h - 6 - bh + 5 + wy * 9,
                                bx + 12, y + h - 6 - bh + 10 + wy * 9],
                               fill=(245, 200, 90))
        # three missile trails, heads glowing, tails fading up-right
        for (hx, hy) in ((x + 120, y + 26), (x + 190, y + 16), (x + 255, y + 30)):
            draw.line([hx + 52, hy - 22, hx, hy], fill=(230, 120, 40), width=3)
            draw.line([hx + 52, hy - 22, hx, hy], fill=(245, 200, 90), width=1)
            draw.ellipse([hx - 5, hy - 5, hx + 5, hy + 5], fill=(245, 200, 90))
            star(draw, hx, hy, 5, (255, 220, 120))
        draw.rectangle([x, y + h - 18, x + 108, y + h], fill=RED)
        draw.text((x + 8, y + h - 14), "7 WOUNDED",
                  font=F(10, bold=True, serif=False), fill=(255, 255, 255))

def panel_art(draw, kind, x, y, w, h):
    """Small flat motif band for numbered panels. h = 46."""
    if kind == "mine":
        draw.rectangle([x, y, x + w, y + h], fill=(30, 60, 90))
        draw.rectangle([x, y + h - 12, x + w, y + h], fill=(20, 45, 70))
        draw.rectangle([x + 18, y + 18, x + 120, y + h - 12], fill=(40, 40, 42))
        draw.rectangle([x + 122, y + 24, x + 152, y + h - 12], fill=(60, 60, 62))
        star(draw, x + 168, y + 16, 10, (240, 200, 60))
        draw.polygon([(x + 52, y + 18), (x + 60, y + 4), (x + 68, y + 18)],
                     fill=(230, 90, 30))
    elif kind == "burst":
        draw.rectangle([x, y, x + w, y + h], fill=(52, 48, 44))
        for i, bh in enumerate([14, 24, 18, 28]):
            bx = x + 14 + i * 38
            draw.rectangle([bx, y + h - 4 - bh, bx + 28, y + h - 4], fill=(30, 30, 32))
        star(draw, x + w - 30, y + 18, 14, (220, 60, 50))
    elif kind == "gavel":
        draw.rectangle([x, y, x + w, y + h], fill=(232, 228, 216))
        draw.rectangle([x + 40, y + 12, x + 110, y + 24], fill=(120, 80, 40))
        draw.rectangle([x + 66, y + 24, x + 78, y + 40], fill=(90, 60, 30))
        draw.rectangle([x + 120, y + 16, x + 150, y + 22], fill=(120, 80, 40))
        draw.text((x + w - 86, y + 10), "$146M", font=F(15, bold=True, serif=False),
                  fill=RED)
    elif kind == "charter":
        # Constitution Day - saffron / white / green + navy wheel + 77
        draw.rectangle([x, y, x + w, y + h // 3], fill=(255, 153, 51))
        draw.rectangle([x, y + h // 3, x + w, y + 2 * h // 3], fill=(245, 245, 240))
        draw.rectangle([x, y + 2 * h // 3, x + w, y + h], fill=(19, 136, 8))
        cx, cy = x + 60, y + h // 2
        draw.ellipse([cx - 11, cy - 11, cx + 11, cy + 11],
                     outline=(27, 42, 74), width=2)
        draw.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=(27, 42, 74))
        draw.text((x + w - 52, y + 8), "77", font=F(20, bold=True, serif=False),
                  fill=(27, 42, 74))
    elif kind == "ebola":
        # v10: clinic tent + red cross + case count
        draw.rectangle([x, y, x + w, y + h], fill=(210, 232, 214))
        draw.polygon([(x + 30, y + 12), (x + 78, y + 12), (x + 96, y + h - 4),
                      (x + 12, y + h - 4)], fill=(255, 255, 255),
                     outline=(150, 150, 150))
        draw.rectangle([x + 48, y + 20, x + 60, y + 36], fill=RED)
        draw.rectangle([x + 42, y + 26, x + 66, y + 30], fill=RED)
        draw.text((x + w - 84, y + 10), "12,021",
                  font=F(14, bold=True, serif=False), fill=RED)
        draw.text((x + w - 84, y + 28), "CASES",
                  font=F(9, bold=True, serif=False), fill=INK)
    elif kind == "budget":
        # v10: EU blue + circle of 12 gold stars + amount
        draw.rectangle([x, y, x + w, y + h], fill=(0, 51, 153))
        import math
        cx, cy = x + 58, y + h // 2
        for i in range(12):
            ang = -math.pi / 2 + i * math.pi / 6
            sx = cx + 15 * math.cos(ang)
            sy = cy + 15 * math.sin(ang)
            draw.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(255, 204, 0))
        draw.text((x + w - 86, y + 10), "\u20ac45BN",
                  font=F(14, bold=True, serif=False), fill=(255, 255, 255))
    elif kind == "rate":
        # v10: rising bars + green arrow + new rate
        draw.rectangle([x, y, x + w, y + h], fill=(232, 228, 216))
        for i, bh in enumerate([12, 20, 30]):
            bx = x + 22 + i * 30
            draw.rectangle([bx, y + h - 6 - bh, bx + 22, y + h - 6], fill=NAVY)
        draw.line([x + 24, y + h - 12, x + 108, y + 8],
                  fill=(19, 136, 8), width=3)
        draw.polygon([(x + 108, y + 8), (x + 96, y + 8), (x + 108, y + 18)],
                     fill=(19, 136, 8))
        draw.text((x + w - 76, y + 10), "3.25%",
                  font=F(14, bold=True, serif=False), fill=RED)
    elif kind == "shut":
        # v10: shuttered garment factory + CLOSED
        draw.rectangle([x, y, x + w, y + h], fill=(206, 226, 222))
        draw.rectangle([x + 16, y + 22, x + 110, y + h - 4], fill=(90, 100, 105))
        draw.rectangle([x + 116, y + 10, x + 128, y + h - 4], fill=(90, 100, 105))
        for yy in (26, 32, 38):
            draw.line([x + 22, y + yy, x + 104, y + yy], fill=(60, 68, 72), width=2)
        draw.text((x + w - 92, y + 10), "CLOSED",
                  font=F(12, bold=True, serif=False), fill=RED)
    elif kind == "guinea":
        # v10: ballot box + 2028
        draw.rectangle([x, y, x + w, y + h], fill=(240, 230, 200))
        draw.rectangle([x + 34, y + 14, x + 96, y + h - 6], fill=(255, 255, 255),
                       outline=(27, 42, 74), width=2)
        draw.rectangle([x + 52, y + 14, x + 78, y + 18], fill=(27, 42, 74))
        draw.polygon([(x + 46, y + 4), (x + 58, y + 4), (x + 66, y + 12),
                      (x + 54, y + 12)], fill=(19, 136, 8))
        draw.text((x + w - 72, y + 10), "2028",
                  font=F(16, bold=True, serif=False), fill=NAVY)
    elif kind == "nvidia":
        # v10: AI chip + 4 nations
        draw.rectangle([x, y, x + w, y + h], fill=(20, 30, 26))
        draw.rectangle([x + 30, y + 10, x + 66, y + h - 10], fill=(34, 139, 34))
        for px in (30, 40, 50, 60):
            draw.rectangle([x + px, y + 4, x + px + 3, y + 10], fill=(120, 200, 120))
            draw.rectangle([x + px, y + h - 10, x + px + 3, y + h - 4],
                           fill=(120, 200, 120))
        draw.ellipse([x + 42, y + 18, x + 54, y + 28], fill=(255, 255, 255))
        draw.text((x + w - 96, y + 12), "4 NATIONS",
                  font=F(11, bold=True, serif=False), fill=(255, 255, 255))
# ---------------------------------------------------------------- render
def render():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    import random
    rnd = random.Random(20261126)
    for _ in range(900):
        px, py = rnd.randint(0, W - 1), rnd.randint(0, H - 1)
        img.putpixel((px, py), (238, 233, 220))
    MX = 14
    CW = W - 2 * MX

    # --- top strip
    d.rectangle([0, 0, W, 32], fill=NAVY)
    d.text((MX, 8), "THE WORLD IN ONE DAY", font=F(15, bold=True, serif=False),
           fill=(255, 255, 255))
    d.text((MX + 268, 9), "No. 331", font=F(12, serif=False), fill=(200, 210, 225))
    r = "PRICE: ONE DAY"
    d.text((W - MX - tw(d, r, F(12, serif=False)), 9), r,
           font=F(12, serif=False), fill=(200, 210, 225))

    # --- masthead + one-line subhead
    d.text((W // 2 - tw(d, "Thursday 26 November 2026", F(50, bold=True)) // 2, 34),
           "Thursday 26 November 2026", font=F(50, bold=True), fill=INK)
    d.line([MX, 90, W - MX, 90], fill=INK, width=2)
    sub = ("Trump unveils tariffs on 14 partners, a nor'easter grounds "
           "the 100th Macy's parade, and Russia's missiles hit Kyiv overnight.")
    sl = fit(d, sub, F(14, italic=True), CW, 1)
    d.text((W // 2 - tw(d, sl[0], F(14, italic=True)) // 2, 94), sl[0],
           font=F(14, italic=True), fill=(60, 60, 60))
    d.line([MX, 112, W - MX, 112], fill=INK, width=1)

    # --- stat boxes + region bar
    stories = LEADS + PANELS
    # Sources actually used, in first-appearance order (v8: the footer
    # prints this same list, so the two can never disagree again).
    srcs_ordered = []
    for s in stories:
        for part in s["src"].split(" \u00b7 "):
            if part not in srcs_ordered:
                srcs_ordered.append(part)
    for a in ALSO:
        if a[4] not in srcs_ordered:
            srcs_ordered.append(a[4])
    nsrc = len(srcs_ordered)
    # Distinct fields across ALL 48 stories (asserted, as v1-v4 did).
    nfields = len({s["field"] for s in stories} | {a[2] for a in ALSO})
    boxes = [("48", "STORIES"), ("9", "REGIONS"),
             ("%d" % nsrc, "SOURCES \u00b7 %d FIELDS" % nfields)]
    bw = CW // 3
    for i, (num, lab) in enumerate(boxes):
        x0 = MX + i * bw
        d.rectangle([x0 + 2, 116, x0 + bw - 2, 142], outline=(150, 145, 130))
        f1, f2 = F(16, bold=True, serif=False), F(11, bold=True, serif=False)
        wtot = tw(d, num + "  ", f1) + tw(d, lab, f2)
        xx = x0 + (bw - wtot) // 2
        d.text((xx, 121), num, font=f1, fill=RED)
        d.text((xx + tw(d, num + "  ", f1), 124), lab, font=f2, fill=INK)
    assert len(FULL_REGIONS) == 48
    rc = {}
    for r in FULL_REGIONS:
        rc[r] = rc.get(r, 0) + 1
    assert sorted(rc) == sorted(REGION_ORDER) and len(rc) == 9
    x = MX
    cmap = {k: c for k, _, c in REGIONS}
    for r in REGION_ORDER:
        wseg = CW * rc[r] // 48
        d.rectangle([x, 146, x + wseg - 1, 154], fill=cmap[r][2])
        x += wseg
    rname = dict((k, v) for k, v, _ in REGIONS)
    cline = " \u00b7 ".join("%s %d" % (rname[r], rc[r]) for r in REGION_ORDER)
    d.text((W // 2 - tw(d, cline, F(10, serif=False)) // 2, 156), cline,
           font=F(10, serif=False), fill=(70, 70, 70))

    # --- leads
    ly = 174
    lw, lgap = 324, 12
    lead_bottom = ly
    for i, s in enumerate(LEADS):
        x0 = MX + i * (lw + lgap)
        lead_art(d, s["art"], x0, ly, lw, 84)
        if s["art"] == "balloon":
            # banner at TOP: the basket hangs at the art bottom, so a
            # bottom banner would cover it (and the old bottom banner
            # overlapped the kicker once the art shrank to 78).
            d.rectangle([x0, ly, x0 + 186, ly + 16], fill=RED)
            d.text((x0 + 8, ly + 2), "POSTPONED TO SATURDAY",
                   font=F(10, bold=True, serif=False), fill=(255, 255, 255))
        yy = ly + 90
        # v8: kicker generated from the data, one system for every story:
        # "N . PLACE - Field" (Title Case field, place for every story).
        kick = "%d \u00b7 %s \u2014 %s" % (s["num"], s.get("kplace", s["place"]),
                                 s["field"])
        assert tw(d, kick, F(10, bold=True, serif=False)) <= lw, \
            "lead kicker overflow: %r" % kick
        d.text((x0, yy), kick, font=F(10, bold=True, serif=False), fill=NAVY)
        badge(d, x0 + lw - 76, yy - 1, s["badge"], 8)
        yy += 16
        hl = fit(d, s["head"], F(22, bold=True), lw, 3)
        for ln in hl:
            d.text((x0, yy), ln, font=F(22, bold=True), fill=INK)
            yy += 24
        yy += 2
        bl = fit(d, s["body"], F(12), lw, 4)
        for ln in bl:
            d.text((x0, yy), ln, font=F(12), fill=(40, 40, 40))
            yy += 14
        if "stat" in s:
            d.text((x0, yy), s["stat"],
                   font=F(12, bold=True, serif=False), fill=RED)
            yy += 14
        # v10: WHY IT MATTERS (migasmin pattern), one line, asserted.
        wl = "WHY IT MATTERS \u2014 "
        fit(d, wl + s["why"], F(9, bold=True, serif=False), lw, 1)
        d.text((x0, yy), wl, font=F(9, bold=True, serif=False), fill=RED)
        d.text((x0 + tw(d, wl, F(9, bold=True, serif=False)), yy), s["why"],
               font=F(9, bold=True, serif=False), fill=INK)
        yy += 12
        yy += 2
        d.text((x0, yy), "SOURCE: " + s["src"], font=F(9, serif=False),
               fill=GREY)
        lead_bottom = max(lead_bottom, yy + 12)

    # --- numbered panels 2 rows x 5
    py = lead_bottom + 10
    d.line([MX, py - 5, W - MX, py - 5], fill=INK, width=1)
    pw, pgap = 191, 9
    ph = 126
    for row in range(2):
        for col in range(5):
            s = PANELS[row * 5 + col]
            x0 = MX + col * (pw + pgap)
            y0 = py + row * (ph + 6)
            panel_art(d, s["art"], x0, y0, pw, 46)
            d.rectangle([x0, y0, x0 + pw, y0 + 46], outline=(180, 175, 160))
            yy = y0 + 52
            # v8: same kicker system as the leads ("N . PLACE - Field").
            kick = "%d \u00b7 %s \u2014 %s" % (s["num"], s.get("kplace", s["place"]),
                                     s["field"])
            assert tw(d, kick, F(9, bold=True, serif=False)) <= pw, \
                "panel kicker overflow: %r" % kick
            d.text((x0, yy), kick, font=F(9, bold=True, serif=False), fill=NAVY)
            yy += 12
            hl = fit(d, s["head"], F(13, bold=True), pw, 2)
            for ln in hl:
                d.text((x0, yy), ln, font=F(13, bold=True), fill=INK)
                yy += 15
            bl = fit(d, s["body"], F(10), pw, 2)
            for ln in bl:
                d.text((x0, yy), ln, font=F(10), fill=(50, 50, 50))
                yy += 12
            d.text((x0, yy + 1), s["src"], font=F(8, bold=True, serif=False),
                   fill=GREY)
            badge(d, x0 + pw - 62, yy, s["badge"], 8)
    panels_bottom = py + 2 * ph + 6

    # --- BY THE NUMBERS strip (v10: 6 numbers, like migasmin)
    ny = panels_bottom + 2
    d.rectangle([0, ny, W, ny + 34], fill=NAVY)
    d.text((MX, ny + 9), "BY THE NUMBERS", font=F(12, bold=True, serif=False),
           fill=(245, 220, 120))
    nums = [("14", "TARIFF PARTNERS"), ("\u20ac45bn", "EU AID FOR UKRAINE"),
            ("12,021", "EBOLA CASES"), ("3.25%", "KOREA RATE"),
            ("16", "BOGOR DEAD"), ("$237.5bn", "VENEZUELA DEBT")]
    xx = MX + 150
    for num, lab in nums:
        d.text((xx, ny + 4), num, font=F(20, bold=True, serif=False),
               fill=(255, 255, 255))
        d.text((xx, ny + 25), lab, font=F(8, bold=True, serif=False),
               fill=(200, 210, 225))
        xx += 138

    # --- timeline (2 rows x 3)
    ty = ny + 34 + 4
    d.text((MX, ty), "THE DAY IN UTC", font=F(11, bold=True, serif=False), fill=NAVY)
    d.line([MX + 118, ty + 7, W - MX, ty + 7], fill=(150, 145, 130), width=1)
    ty += 14
    tw3 = CW // 3
    for i, (tm, txt) in enumerate(TIMELINE):
        col, row = i % 3, i // 3
        x0 = MX + col * tw3
        y0 = ty + row * 13
        d.text((x0, y0), tm, font=F(10, bold=True, serif=False), fill=RED)
        t2 = fit(d, txt, F(10, serif=False), tw3 - 88, 1)[0]
        d.text((x0 + 86, y0), t2, font=F(10, serif=False), fill=INK)

    # --- map + also list (v10: map 300x132, also 3 cols x 12 rows)
    my = ty + 2 * 13 + 8
    d.text((MX, my), "WHERE IT HAPPENED \u2014 PINS 1\u201313",
           font=F(11, bold=True, serif=False), fill=NAVY)
    ax = MX + 318
    d.text((ax, my), "AND ALSO \u2014 STORIES 14\u201348",
           font=F(11, bold=True, serif=False), fill=NAVY)
    my += 15
    mapx, mapy, mapw, maph = MX, my, 300, 132
    d.rectangle([mapx, mapy, mapx + mapw, mapy + maph], fill=SEA,
                outline=(150, 145, 130))
    def proj(lon, lat):
        return (mapx + (lon + 180) / 360.0 * mapw,
                mapy + (90 - lat) / 180.0 * maph)
    for poly in CONTINENTS:
        pts = [proj(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=LAND, outline=(170, 150, 110))
    for idx, (lat, lon) in enumerate(PINS, start=1):
        px, py = proj(lon, lat)
        dx, dy = PIN_NUDGE.get(idx - 1, (0, 0))
        px, py = px + dx, py + dy
        assert mapx <= px <= mapx + mapw and mapy <= py <= mapy + maph, \
            "pin %d off map" % idx
        d.ellipse([px - 8, py - 8, px + 8, py + 8], fill=RED,
                  outline=(255, 255, 255))
        t = str(idx)
        d.text((px - tw(d, t, F(9, bold=True, serif=False)) / 2, py - 6), t,
               font=F(9, bold=True, serif=False), fill=(255, 255, 255))
    # also list, 3 columns x 12 rows - each row carries its field, the same
    # "number . place . field" system as the leads and panels above.
    colw = (W - MX - ax - 8) // 3
    for i, (num, place, field, txt, src, region) in enumerate(ALSO):
        col, row = i // 12, i % 12
        x0 = ax + col * (colw + 4)
        y0 = my + row * 11
        d.text((x0, y0), str(num), font=F(9, bold=True, serif=False), fill=RED)
        line = "%s \u00b7 %s \u2014 %s" % (place, field, txt)
        ll = fit(d, line, F(8, serif=False), colw - 18, 1)
        d.text((x0 + 18, y0), ll[0], font=F(8, serif=False), fill=INK)
    map_bottom = my + maph

    # --- DATE CHECK (3 cols x 2 rows)
    dy = map_bottom + 2
    d.rectangle([MX, dy, W - MX, dy + 44], outline=RED, width=2)
    d.text((MX + 8, dy + 3),
           "\u2715  DATE CHECK \u2014 THESE ARE NOT 26 NOVEMBER   \u00b7   Not yet: NFL results \u00b7 Black Friday",
           font=F(10, bold=True, serif=False), fill=RED)
    for i, (txt, when) in enumerate(DATECHECK_OUT):
        col, row = i // 2, i % 2
        x0 = MX + 8 + col * 332
        y0 = dy + 18 + row * 12
        d.text((x0, y0), "\u2715  %s \u2014 %s" % (txt, when), font=F(10, serif=False),
               fill=INK)
    date_bottom = dy + 44

    # --- footer (3 lines)
    fy = date_bottom + 2
    d.text((MX, fy), "CONFIRMED 2+ outlets \u00b7 OFFICIAL on the record \u00b7 "
           "REPORTED one outlet \u00b7 CLAIM one side's word",
           font=F(9, serif=False), fill=GREY)
    fy += 11
    d.text((MX, fy), "Every story above happened or was first reported on "
           "Thursday 26 November 2026, in some time zone. Times UTC; "
           "'c.' = approximate \u00b7 pictures and map drawn in code, not photos.",
           font=F(9, serif=False), fill=GREY)
    fy += 11
    # v8: footer source list is built from the slate itself (first
    # appearance order).
    src_line = ("Sources: " + " \u00b7 ".join(srcs_ordered) +
                " \u2014 as reported 25\u201326 Nov 2026.")
    assert tw(d, src_line, F(9, serif=False)) <= CW, \
        "footer sources overflow"
    d.text((MX, fy), src_line, font=F(9, serif=False), fill=GREY)
    assert fy + 10 <= H, "layout overflow: footer ends %d" % fy
    return img

def main():
    out = os.path.join(os.path.dirname(__file__), "..", "assets", "entry.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    img = render()
    img.save(out, optimize=True)
    data = open(out, "rb").read()
    assert len(data) <= 1048576, "PNG too big: %d" % len(data)
    assert img.size == (1024, 1024)
    assert len(LEADS) + len(PANELS) + len(ALSO) == 48
    nums = [s["num"] for s in LEADS + PANELS] + [a[0] for a in ALSO]
    assert sorted(nums) == list(range(1, 49)), "story numbers not 1..48"
    fields = {s["field"] for s in LEADS + PANELS} | {a[2] for a in ALSO}
    assert len(fields) == 15, "distinct fields %d != 15: %s" % (
        len(fields), sorted(fields))
    assert len({a[5] for a in ALSO} | {s["region"] for s in LEADS + PANELS}) == 9
    print("v10 entry.png: %d bytes sha256 %s" %
          (len(data), hashlib.sha256(data).hexdigest()))

if __name__ == "__main__":
    main()
