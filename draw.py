#!/usr/bin/env python3
"""news-image-20261126 v4 — "one-page pictorial" front page (1024x1024 PNG).

Hand-written in this session from the Antigravity v2 spec
(~/workspace/makefun-news-image-20261126/v2-spec.md), then revised by hand
through three review rounds plus a fresh-AI full review (2026-11-27).
v4 changes: Gaza 10 (was 8), Kuwait 2 dead 2 injured, FedEx timezone,
13:30 parade removed from the timeline, chess Game 3 drawn 1.5-1.5,
map pins re-seated, ISS ground track redrawn across the equator,
DATE CHECK back to a red frame, illustration small-text removed.
Layout is entirely new (giant date masthead, 3 hero illustrations +
10 small cards, numbers band, UTC timeline, numbered-pin map,
one-line list, DATE CHECK box); nothing is copied from the rejected
v1 draw.py except the rough continent-outline polygon data used for
the map.

Deterministic: no random/time/datetime, fixed font files, PNG saved with
optimize=True, compress_level=9 and no metadata. Run:
    python3 draw.py            # writes entry.png next to this file
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- constants
W, H = 1024, 1024
MX = 24                        # side margin
CW = 976                       # content width (24..1000)
MAX_BYTES = 1_048_576

PAPER = (247, 242, 231)        # #F7F2E7 warm paper
CARD = (255, 253, 248)         # #FFFDF8 card
SAND = (239, 233, 220)         # #EFE9DC timeline strip
BORDER = (214, 207, 194)       # #D6CFC2 borders
RULE = (203, 213, 225)         # #CBD5E1 kicker rule
INK = (15, 23, 42)             # #0F172A main text
INK2 = (51, 65, 85)            # #334155 secondary text
GRAY = (100, 116, 139)         # #64748B source gray
RED = (200, 30, 30)            # #C81E1E signal red
NAVY = (16, 42, 67)            # #102A43 numbers band
GOLD = (217, 119, 6)           # #D97706 warm gold
OCEAN = (219, 231, 240)        # #DBE7F0 map ocean
LAND = (231, 222, 200)         # #E7DEC8 map land
LAND_EDGE = (201, 191, 169)    # map land outline
DC_BG = (245, 245, 244)        # #F5F5F4 DATE CHECK background (muted stone)

TAG_COLOR = {
    "OFFICIAL": (21, 128, 61),    # #15803D
    "CONFIRMED": (29, 78, 216),   # #1D4ED8
    "REPORTED": (180, 83, 9),     # #B45309
    "CLAIM": (185, 28, 28),       # #B91C1C
}

FONT_DIR = "/usr/share/fonts/truetype/liberation/"
SERIF_B = FONT_DIR + "LiberationSerif-Bold.ttf"
SERIF_I = FONT_DIR + "LiberationSerif-Italic.ttf"
SANS_B = FONT_DIR + "LiberationSans-Bold.ttf"
SANS_R = FONT_DIR + "LiberationSans-Regular.ttf"
for _p in (SERIF_B, SERIF_I, SANS_B, SANS_R):
    assert Path(_p).exists(), f"missing font: {_p}"

# ------------------------------------------------------------------- data
# Self-contained; the program never reads v2-spec.md at runtime.
EDITION_DATE = "Thursday, 26 November 2026"
KICKER_LEFT = "THE WORLD IN ONE DAY · THURSDAY EDITION"
KICKER_RIGHT = "36 STORIES · 9 REGIONS · 20+ SOURCES"
DECK = ("Macy's 100th parade postponed for storm; India honors 26/11 "
        "victims; Gukesh–Sindarov draw Game 3, tied 1.5–1.5.")

REGIONS = [
    ("Europe", "EUR", 8, "#3B5B8C"),
    ("North America", "NAM", 5, "#C2594B"),
    ("East Asia", "EAS", 5, "#D49A3A"),
    ("Africa", "AFR", 4, "#4A7C59"),
    ("Middle East", "MEA", 3, "#9E5A82"),
    ("Southeast Asia", "SEA", 3, "#3D8B8B"),
    ("Latin America", "LAT", 3, "#7A8B3C"),
    ("Oceania & Global", "GLB", 3, "#5B6D82"),
    ("South Asia", "SAS", 2, "#B86B35"),
]

BY_THE_NUMBERS = [
    ("100th", "MACY'S PARADE DELAYED"),
    ("166", "26/11 VICTIMS HONORED"),
    ("€45B", "EU UKRAINE LOAN TALK"),
    ("3.25%", "BOK RATE AFTER HIKE"),
    ("12,021", "DRC EBOLA CONFIRMED"),
]

UTC_TIMELINE = [
    ("00:50", "BOK hikes to 3.25%"),
    ("01:40", "#19 FedEx overrun"),
    ("07:45", "Bangkok refinery fire"),
    ("12:08", "Progress 97 at ISS"),
    ("14:00", "Chess Game 3 starts"),
]

DATE_CHECK = [
    "COP31 Antalya summit closed — 22 Nov",
    "Nvidia reinstated Jensen Huang — 23 Nov",
    "China probed Shanghai chief Chen — 24 Nov",
    "Cairo Ring Road tanker fire (31 dead) — 25 Nov",
    "U.S. USTR 14-partner tariff unveil — 25 Nov",
    "Houthi Ras Tanura refinery claim — 25 Nov",
    "FCC approved SpaceX Starmind — 25 Nov",
    "SA court Phala Phala ruling — 25 Nov",
]
UPCOMING_LINE = "Upcoming: Macy's Parade Sat 28 Nov · Spain Election Sun 29 Nov"

# 36 stories, transcribed from spec section 7 JSON.
# Deviation from spec, measured: story #19's line_text is reworded
# ("FedEx 910 overruns in Miami (01:40 UTC)", 291px) so the UTC timezone
# fits the 302px sub-column; the review's fuller wording
# ("Miami recovers after FedEx 910 overrun (01:40 UTC)", 345px) does not
# fit. Every other row fits unchanged.
STORIES = [
    {"id": 1, "tier": "hero", "title": "Macy's 100th Parade Postponed to Saturday",
     "summary": "New York moved Thursday's parade to Saturday over 45–65 mph gusts; NBC aired the 2025 encore.",
     "region": "North America", "source": "NYC Mayor / Macy's", "tag": "OFFICIAL",
     "lon": -74.0, "lat": 40.7, "dx": 0, "dy": 0},
    {"id": 2, "tier": "hero", "title": "India Marks 18 Years Since the 26/11 Attacks",
     "summary": "U.S. Ambassador Sergio Gor honored 166 Mumbai terror victims as India marked Constitution Day.",
     "region": "South Asia", "source": "U.S. Embassy / PIB", "tag": "OFFICIAL",
     "lon": 72.9, "lat": 19.1, "dx": 0, "dy": 0},
    {"id": 3, "tier": "hero", "title": "Gukesh, Sindarov Draw Game 3 to Stay Tied 1.5–1.5",
     "summary": "World Chess Championship Game 3 ended in a 60-move draw in Geneva; the match is tied 1.5–1.5.",
     "region": "Europe", "source": "FIDE", "tag": "OFFICIAL",
     "lon": 6.1, "lat": 46.2, "dx": -5, "dy": 2},
    {"id": 4, "tier": "card", "title": "EU Summit Clashes Over Budget, Ukraine Loan",
     "summary": "Brussels talks stalled on next long-term budget and a proposed €45B loan for Kyiv.",
     "region": "Europe", "source": "EU Council / Guardian", "tag": "CONFIRMED",
     "lon": 4.4, "lat": 50.8, "dx": 5, "dy": -4},
    {"id": 5, "tier": "card", "title": "Russian Missiles Strike Kyiv, Odesa Grain Ships",
     "summary": "Barrage injured seven in Kyiv and hit two foreign vessels carrying 100,000t of grain.",
     "region": "Europe", "source": "Ukraine / NV", "tag": "CONFIRMED",
     "lon": 30.5, "lat": 50.5, "dx": 0, "dy": 0},
    {"id": 6, "tier": "card", "title": "Blast and Fire Hit Bangkok Oil Refinery",
     "summary": "Bangchak hydrocracker explosion injured nine workers, halted output, and sparked brief local evacuations.",
     "region": "Southeast Asia", "source": "Thai Min. / CNA", "tag": "CONFIRMED",
     "lon": 100.5, "lat": 13.8, "dx": 0, "dy": -3},
    {"id": 7, "tier": "card", "title": "Bank of Korea Raises Key Rate to 3.25%",
     "summary": "Central bank raised rates 25 bps on AI-boom inflation while KOSPI stocks rebounded.",
     "region": "East Asia", "source": "Bank of Korea", "tag": "OFFICIAL",
     "lon": 127.0, "lat": 37.6, "dx": -3, "dy": 4},
    {"id": 8, "tier": "card", "title": "Kim Urges Wider Tactical Nuclear Deployment",
     "summary": "KCNA reported Thursday that Kim inspected nuclear facilities Wednesday and refused denuclearization.",
     "region": "East Asia", "source": "KCNA / CNN", "tag": "CLAIM",
     "lon": 125.8, "lat": 39.0, "dx": 2, "dy": -4},
    {"id": 9, "tier": "card", "title": "Israeli Strikes Kill 10 in Gaza",
     "summary": "Israeli strikes killed at least 10 Palestinians, including Hamas official Khaled Abu Nada.",
     "region": "Middle East", "source": "Gaza Health / AP / Reuters", "tag": "CONFIRMED",
     "lon": 34.5, "lat": 31.5, "dx": 0, "dy": 0},
    {"id": 10, "tier": "card", "title": "Congo Ebola Reaches 12,021 Confirmed Cases",
     "summary": "DRC outbreak hit 5,904 deaths as Canada, Bahamas, and Bahrain imposed traveler restrictions.",
     "region": "Africa", "source": "DRC MoH / WHO", "tag": "OFFICIAL",
     "lon": 29.5, "lat": 1.5, "dx": 0, "dy": 0},
    {"id": 11, "tier": "card", "title": "Historic King Tides Flood Coastal California",
     "summary": "El Niño–boosted surges broke pier structures and kept Thanksgiving coastal flood warnings active.",
     "region": "North America", "source": "NOAA / NWS", "tag": "OFFICIAL",
     "lon": -121.0, "lat": 36.0, "dx": 0, "dy": 0},
    {"id": 12, "tier": "card", "title": "Brazil Condemns U.S. Excess-Capacity Tariffs",
     "summary": "Brasília rejected Washington's newly unveiled tariffs and left reciprocal trade measures open.",
     "region": "Latin America", "source": "Brazil Gov.", "tag": "OFFICIAL",
     "lon": -47.9, "lat": -15.8, "dx": 0, "dy": 0},
    {"id": 13, "tier": "card", "title": "Progress 97 Cargo Craft Docks at ISS",
     "summary": "Unpiloted Russian ship delivered three tons of food and fuel at 12:08 UTC.",
     "region": "Oceania & Global", "source": "NASA / Roscosmos", "tag": "OFFICIAL",
     "lon": -125.0, "lat": -30.0, "inset": "ORBIT #13 (ISS)"},
    {"id": 14, "tier": "list", "title": "Ukraine Claims Neptune Strike on Russian Airbase",
     "line_text": "Ukraine claims Neptune hit Marinovka airbase",
     "short_source": "UA Staff", "tag": "CLAIM", "region": "Europe"},
    {"id": 15, "tier": "list", "title": "UK Contacts 100,000 Veterans for Reserve Readiness",
     "line_text": "UK contacts 100,000 veterans for reserves",
     "short_source": "UK MoD", "tag": "OFFICIAL", "region": "Europe"},
    {"id": 16, "tier": "list", "title": "European Commission Proposes New EU Quantum Act",
     "line_text": "EU Commission proposes new Quantum Act",
     "short_source": "EC", "tag": "OFFICIAL", "region": "Europe"},
    {"id": 17, "tier": "list", "title": "EU Sanctions 15 More Russian Defense Entities",
     "line_text": "EU sanctions 15 Russian defense entities",
     "short_source": "EU Council", "tag": "OFFICIAL", "region": "Europe"},
    {"id": 18, "tier": "list", "title": "Merz Clashes With AfD Over Ukraine Aid",
     "line_text": "Merz clashes with AfD over Ukraine aid",
     "short_source": "Bundestag", "tag": "CONFIRMED", "region": "Europe"},
    {"id": 19, "tier": "list", "title": "Miami Airport Recovers After FedEx Runway Overrun",
     "line_text": "FedEx 910 overruns in Miami (01:40 UTC)",
     "short_source": "FAA/FedEx", "tag": "CONFIRMED", "region": "North America"},
    {"id": 20, "tier": "list", "title": "NFL Thanksgiving Tripleheader Headlines Week 12 Slate",
     "line_text": "NFL Thanksgiving tripleheader kicks off Thu",
     "short_source": "NFL", "tag": "OFFICIAL", "region": "North America"},
    {"id": 21, "tier": "list", "title": "Microsoft: Salt Typhoon Uses AI Tool ARTEX",
     "line_text": "Microsoft: Salt Typhoon uses AI tool ARTEX",
     "short_source": "Microsoft", "tag": "CONFIRMED", "region": "North America"},
    {"id": 22, "tier": "list", "title": "Taiwan Expects to Keep 15% Tariff Cap",
     "line_text": "Taiwan expects to keep 15% U.S. tariff cap",
     "short_source": "Exec Yuan", "tag": "OFFICIAL", "region": "East Asia"},
    {"id": 23, "tier": "list", "title": "Memory Chip Crunch Triples RAM Prices",
     "line_text": "AI memory crunch triples DRAM prices",
     "short_source": "TrendForce", "tag": "CONFIRMED", "region": "East Asia"},
    {"id": 24, "tier": "list", "title": "WHO Names Nanjing Institute Leprosy Collaborating Centre",
     "line_text": "WHO names Nanjing leprosy research centre",
     "short_source": "WHO", "tag": "OFFICIAL", "region": "East Asia"},
    {"id": 25, "tier": "list", "title": "Ethiopia Launches $1 Billion Defaulted Bond Exchange",
     "line_text": "Ethiopia launches $1B defaulted bond swap",
     "short_source": "Eth. Fin.", "tag": "OFFICIAL", "region": "Africa"},
    {"id": 26, "tier": "list", "title": "Ethiopia Launches Inclusive Sudan Peace Dialogue Bid",
     "line_text": "Sudan peace bid launched by Ethiopia",
     "short_source": "Sudan Trib.", "tag": "OFFICIAL", "region": "Africa"},
    {"id": 27, "tier": "list", "title": "South Africa Factory Inflation Jumps to 8.1%",
     "line_text": "South Africa Oct PPI jumps to 8.1%",
     "short_source": "Stats SA", "tag": "OFFICIAL", "region": "Africa"},
    {"id": 28, "tier": "list", "title": "Kuwait Says Drone Debris Killed Two, Injured Two",
     "line_text": "Kuwait: drone shrapnel kills two, injures two",
     "short_source": "KW MoD", "tag": "OFFICIAL", "region": "Middle East"},
    {"id": 29, "tier": "list", "title": "Explosion Reported Near Tanker West of Dubai",
     "line_text": "Blast logged near tanker west of Dubai",
     "short_source": "UKMTO", "tag": "REPORTED", "region": "Middle East"},
    {"id": 30, "tier": "list", "title": "Manila Counts 48 Chinese Ships in Sea",
     "line_text": "Manila logs 48 Chinese ships in S. China Sea",
     "short_source": "PH AFP", "tag": "REPORTED", "region": "Southeast Asia"},
    {"id": 31, "tier": "list", "title": "Malaysia Plans Talks With Myanmar on Nationals",
     "line_text": "Malaysia plans Myanmar talks: 200k refugees",
     "short_source": "MY Gov", "tag": "OFFICIAL", "region": "Southeast Asia"},
    {"id": 32, "tier": "list", "title": "Brazil Mid-November Inflation Slows to 0.22%",
     "line_text": "Brazil mid-Nov inflation slows to 0.22%",
     "short_source": "IBGE", "tag": "OFFICIAL", "region": "Latin America"},
    {"id": 33, "tier": "list", "title": "Seven Killed in Michoacán–Jalisco Cartel Shootout",
     "line_text": "Seven killed in Mexican cartel clash",
     "short_source": "Reuters", "tag": "REPORTED", "region": "Latin America"},
    {"id": 34, "tier": "list", "title": "India Presents 2036 Olympic Bid to IOC",
     "line_text": "India pitches 2036 Olympic bid to IOC",
     "short_source": "IOA", "tag": "OFFICIAL", "region": "South Asia"},
    {"id": 35, "tier": "list", "title": "Australian Senate Blasts Aged-Care Assessment Algorithm",
     "line_text": "AU Senate blasts aged-care wait times",
     "short_source": "AU Senate", "tag": "OFFICIAL", "region": "Oceania & Global"},
    {"id": 36, "tier": "list", "title": "Top Banks Lag 6:1 Clean-Energy Ratio",
     "line_text": "Top 65 banks give 72¢ clean per $1 fossil",
     "short_source": "Reclaim", "tag": "REPORTED", "region": "Oceania & Global"},
]

# ------------------------------------------------------------ map polygons
# Rough equirectangular continent outlines as (lon, lat) points.
EURASIA = [(-10, 36), (-9, 43), (-2, 48), (-1, 50), (2, 51), (5, 53), (8, 57),
           (10, 59), (18, 56), (21, 55), (24, 59), (28, 60), (30, 62), (30, 70),
           (40, 68), (50, 69), (60, 69), (68, 73), (75, 73), (85, 75), (95, 76),
           (105, 77), (113, 73), (120, 73), (130, 72), (140, 72), (150, 70),
           (158, 66), (162, 60), (158, 52), (156, 51), (150, 59), (142, 54),
           (141, 45), (138, 43), (132, 43), (129, 38), (127, 35), (126, 33),
           (122, 31), (121, 28), (118, 25), (112, 22), (109, 18), (106, 10),
           (104, 9), (101, 7), (99, 10), (97, 15), (94, 17), (91, 22), (88, 22),
           (86, 20), (83, 17), (80, 13), (77, 8), (75, 11), (73, 16), (70, 20),
           (67, 24), (64, 25), (61, 25), (58, 26), (56, 26), (52, 26), (50, 29),
           (48, 30), (45, 29), (42, 29), (39, 29), (36, 36), (33, 36), (30, 36),
           (27, 37), (23, 36), (21, 38), (19, 42), (16, 44), (13, 45), (9, 44),
           (5, 43), (3, 42), (0, 39), (-2, 37), (-6, 36), (-9, 38), (-10, 36)]
N_AMERICA = [(-168, 66), (-140, 70), (-125, 71), (-110, 68), (-95, 69), (-85, 66),
             (-78, 62), (-70, 62), (-65, 60), (-60, 55), (-55, 52), (-60, 47),
             (-65, 44), (-70, 42), (-74, 39), (-76, 35), (-80, 32), (-81, 26),
             (-84, 30), (-90, 21), (-97, 16), (-92, 15), (-87, 13), (-83, 9),
             (-79, 9), (-83, 12), (-87, 14), (-90, 14), (-94, 17), (-97, 19),
             (-97, 22), (-105, 20), (-110, 23), (-114, 28), (-117, 33), (-122, 37),
             (-124, 42), (-124, 48), (-130, 54), (-140, 60), (-150, 58),
             (-158, 58), (-165, 60), (-168, 66)]
S_AMERICA = [(-79, 9), (-77, 7), (-75, 10), (-72, 12), (-68, 11), (-64, 10),
             (-61, 9), (-59, 8), (-54, 6), (-52, 5), (-50, 0), (-44, -3),
             (-38, -5), (-35, -8), (-38, -15), (-40, -20), (-41, -23), (-48, -27),
             (-52, -32), (-58, -35), (-62, -39), (-65, -41), (-68, -47),
             (-70, -52), (-73, -54), (-74, -50), (-73, -44), (-73, -37),
             (-72, -30), (-70, -20), (-70, -18), (-75, -15), (-79, -9),
             (-81, -5), (-80, 1), (-80, 5), (-79, 9)]
AFRICA = [(-6, 35), (-9, 32), (-13, 27), (-16, 20), (-17, 15), (-16, 11),
          (-13, 8), (-8, 4), (6, 4), (9, 4), (9, 0), (12, -5), (13, -10),
          (12, -17), (14, -23), (16, -28), (19, -34), (25, -34), (28, -33),
          (32, -29), (35, -24), (36, -18), (40, -15), (40, -10), (41, -5),
          (44, -1), (48, 0), (51, 2), (51, 11), (48, 11), (44, 11), (40, 15),
          (38, 18), (37, 22), (35, 28), (33, 31), (30, 31), (25, 32), (20, 32),
          (15, 33), (11, 34), (10, 37), (6, 37), (0, 36), (-6, 35)]
AUSTRALIA = [(113, -22), (114, -30), (115, -35), (118, -35), (122, -34),
             (124, -33), (129, -32), (132, -32), (134, -33), (136, -35),
             (138, -35), (140, -38), (143, -39), (146, -39), (150, -37),
             (153, -32), (153, -27), (151, -24), (149, -20), (146, -19),
             (144, -15), (142, -11), (141, -13), (138, -15), (136, -15),
             (135, -12), (132, -11), (130, -13), (127, -14), (125, -15),
             (122, -17), (119, -20), (116, -21), (113, -22)]
GREENLAND = [(-45, 60), (-40, 64), (-32, 68), (-22, 70), (-20, 74), (-25, 76),
             (-35, 76), (-50, 75), (-58, 74), (-55, 70), (-52, 66), (-48, 62),
             (-45, 60)]
UK = [(-5, 50), (-3, 53), (-5, 56), (-3, 58), (-1, 57), (0, 53), (1, 51),
      (-3, 50), (-5, 50)]
JAPAN = [(130, 31), (132, 33), (134, 34), (136, 35), (138, 35), (139, 37),
         (140, 39), (141, 41), (142, 43), (143, 44), (145, 44), (144, 42),
         (142, 40), (141, 38), (140, 36), (139, 34), (137, 34), (135, 33),
         (133, 34), (131, 33), (130, 31)]
MADAGASCAR = [(44, -16), (47, -15), (50, -16), (49, -20), (47, -24), (45, -25),
              (43, -22), (43, -18), (44, -16)]
NEW_ZEALAND = [(167, -45), (169, -43), (172, -41), (174, -39), (176, -38),
               (178, -37), (175, -40), (173, -42), (170, -44), (168, -46),
               (167, -45)]
ANTARCTICA = [(-180, -70), (-120, -72), (-60, -68), (-30, -70), (0, -66),
              (30, -70), (60, -66), (90, -70), (120, -68), (150, -72),
              (180, -70), (180, -90), (-180, -90)]
CONTINENTS = [EURASIA, N_AMERICA, S_AMERICA, AFRICA, AUSTRALIA, GREENLAND,
              UK, JAPAN, MADAGASCAR, NEW_ZEALAND, ANTARCTICA]

# ------------------------------------------------------------------ helpers
def _hex(s):
    s = s.lstrip("#")
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))


def _font(path, size):
    return ImageFont.truetype(path, size)


def fit_font(d, text, path, size, max_w, min_size=8):
    """Largest font size <= `size` that fits `max_w`; never below min_size."""
    while size > min_size:
        f = _font(path, size)
        if d.textlength(text, font=f) <= max_w:
            return f, size
        size -= 1
    f = _font(path, min_size)
    if d.textlength(text, font=f) > max_w:
        raise ValueError(f"text does not fit even at {min_size}px: {text!r}")
    return f, min_size


def wrap_lines(d, text, font, max_w, max_lines, strict=True):
    """Greedy word wrap. Raises on overflow when strict (never truncate)."""
    words = text.split(" ")
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if d.textlength(trial, font=font) <= max_w:
            cur = trial
        else:
            if not cur:
                raise ValueError(f"single word too wide: {w!r}")
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    if strict and len(lines) > max_lines:
        raise ValueError(f"wrap overflow ({len(lines)} > {max_lines}): {text!r}")
    return lines


def _draw_centered(d, cx, y, text, font, fill):
    w = d.textlength(text, font=font)
    d.text((cx - w / 2, y), text, font=font, fill=fill)


def _badge(d, cx, cy, r, number, fill=RED):
    """Red numbered circle badge (drawn at 1x on the main canvas)."""
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=fill,
              outline=(255, 255, 255), width=1)
    f = _font(SANS_B, 11 if r >= 10 else 9)
    _draw_centered(d, cx, cy - (5 if r >= 10 else 4), str(number), f,
                   (255, 255, 255))


def _ss(w, h):
    """2x supersampled canvas + draw context for one illustration."""
    img = Image.new("RGB", (w * 2, h * 2))
    return img, ImageDraw.Draw(img)


def _finish(img2x, w, h):
    return img2x.resize((w, h), Image.Resampling.LANCZOS)


def _star(d, cx, cy, r_out, r_in, color, points=5):
    import math
    pts = []
    for i in range(points * 2):
        r = r_out if i % 2 == 0 else r_in
        a = -math.pi / 2 + i * math.pi / points
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    d.polygon(pts, fill=color)


def _banner(d, w2, y2, h2, text, size2, fill=RED):
    """Bottom banner strip inside an illustration (2x coordinates)."""
    d.rectangle([0, y2, w2, y2 + h2], fill=fill)
    f = _font(SANS_B, size2)
    _draw_centered(d, w2 / 2, y2 + (h2 - size2) / 2 - 2, text, f,
                   (255, 255, 255))


# ------------------------------------------------------- hero illustrations
def ill_1_macys():
    """#1 Macy's parade postponed — night skyline + tilted red balloon."""
    w, h = 309, 108
    img, d = _ss(w, h)
    d.rectangle([0, 0, 618, 216], fill=(22, 36, 71))          # #162447
    # skyline silhouettes with lit windows
    import math
    buildings = [(0, 150, 70, 216), (60, 128, 130, 216), (120, 158, 185, 216),
                 (175, 120, 250, 216), (240, 150, 310, 216),
                 (300, 132, 372, 216), (362, 160, 430, 216),
                 (420, 140, 500, 216), (490, 156, 560, 216),
                 (550, 146, 618, 216)]
    for x0, y0, x1, y1 in buildings:
        d.rectangle([x0, y0, x1, y1], fill=(36, 59, 103))     # #243B67
        for wy in range(y0 + 12, y1 - 8, 18):
            for wx in range(x0 + 8, x1 - 8, 16):
                if (wx * 7 + wy * 13) % 5 < 2:
                    d.rectangle([wx, wy, wx + 5, wy + 7], fill=(250, 204, 21))
    # red balloon on its own layer so it can tilt 18 degrees
    layer = Image.new("RGBA", (618, 216), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.ellipse([345, 24, 545, 144], fill=(217, 45, 32, 255))   # #D92D20
    ld.ellipse([397, 18, 419, 38], fill=(217, 45, 32, 255))    # left ear
    ld.ellipse([473, 18, 495, 38], fill=(217, 45, 32, 255))    # right ear
    ld.arc([372, 34, 472, 124], 200, 320, fill=(255, 255, 255, 220), width=6)
    layer = layer.rotate(18, resample=Image.BICUBIC, center=(445, 84))
    img.paste(layer, (0, 0), layer)
    # 4 thin strings from balloon bottom
    for sx in (420, 440, 460, 480):
        d.line([(sx, 150), (sx + 14, 176)], fill=(226, 232, 240), width=2)
    # 3 white wind arcs, left side
    for i, (ax, ay) in enumerate(((24, 34), (44, 58), (18, 84))):
        d.arc([ax, ay, ax + 46, ay + 26], 300, 60, fill=(255, 255, 255),
              width=4)
    # gold "100" medallion, top-left inside the sky
    d.ellipse([88, 10, 140, 62], fill=GOLD, outline=(255, 255, 255), width=3)
    f = _font(SANS_B, 26)
    _draw_centered(d, 114, 24, "100", f, (255, 255, 255))
    _banner(d, 618, 176, 40, "POSTPONED TO SAT", 26)
    return _finish(img, w, h)


def ill_2_mumbai():
    """#2 Mumbai 26/11 — India Gate arch at dusk + memorial candles."""
    w, h = 309, 108
    img, d = _ss(w, h)
    d.rectangle([0, 0, 618, 120], fill=(30, 41, 59))           # #1E293B
    d.rectangle([0, 120, 618, 216], fill=(71, 59, 48))         # #473B30
    # India Gate: dark arch body with a warm glowing opening
    d.polygon([(219, 176), (219, 84), (256, 52), (362, 52), (399, 84),
               (399, 176)], fill=(11, 18, 32))
    d.polygon([(283, 176), (283, 100), (309, 78), (335, 100), (335, 176)],
              fill=(232, 217, 176))
    d.rectangle([204, 170, 414, 180], fill=(11, 18, 32))
    # 5 memorial candles with gold flames
    for i, cx in enumerate((180, 246, 309, 372, 438)):
        d.rectangle([cx - 8, 150, cx + 8, 196], fill=(245, 240, 220))
        d.polygon([(cx, 122), (cx + 7, 140), (cx, 148), (cx - 7, 140)],
                  fill=(245, 158, 11))
        d.polygon([(cx, 130), (cx + 3, 140), (cx, 146), (cx - 3, 140)],
                  fill=(254, 240, 138))
    _banner(d, 618, 176, 40, "18 YEARS · 26/11", 26)
    return _finish(img, w, h)


def ill_3_chess():
    """#3 Chess Game 3 — 6x4 board with two kings + digital clock 1–1."""
    w, h = 309, 108
    img, d = _ss(w, h)
    d.rectangle([0, 0, 618, 216], fill=(241, 235, 222))
    # board 6x4, 44px squares at (16, 16)
    sq = 44
    for r in range(4):
        for c in range(6):
            col = (237, 228, 208) if (r + c) % 2 == 0 else (74, 55, 40)
            d.rectangle([16 + c * sq, 16 + r * sq,
                         16 + (c + 1) * sq, 16 + (r + 1) * sq], fill=col)
    # white king on c2, black king on e3 (geometric: base + crown + cross)
    def king(cx, cy, body, cross):
        d.ellipse([cx - 15, cy + 2, cx + 15, cy + 16], fill=body)
        d.rectangle([cx - 9, cy - 12, cx + 9, cy + 6], fill=body)
        d.line([cx, cy - 22, cx, cy - 8], fill=cross, width=5)
        d.line([cx - 7, cy - 16, cx + 7, cy - 16], fill=cross, width=5)
    king(16 + 1 * sq + sq // 2, 16 + 1 * sq + sq // 2, (250, 250, 248),
         (15, 23, 42))
    king(16 + 4 * sq + sq // 2, 16 + 2 * sq + sq // 2, (31, 41, 55),
         (250, 250, 248))
    # digital clock: dark slate box, two digit panels "1.5" and "1.5"
    d.rounded_rectangle([300, 28, 600, 164], radius=10, fill=(31, 41, 55))
    for i, x0 in enumerate((318, 456)):
        d.rounded_rectangle([x0, 48, x0 + 66, 144], radius=6,
                            fill=(241, 245, 249))
        f = _font(SANS_B, 36)
        _draw_centered(d, x0 + 33, 78, "1.5", f, (15, 23, 42))
    d.ellipse([432, 76, 444, 88], fill=(241, 245, 249))
    d.ellipse([432, 108, 444, 120], fill=(241, 245, 249))
    _banner(d, 618, 176, 40, "TIED 1.5–1.5 · GENEVA", 26)
    return _finish(img, w, h)


# ------------------------------------------------------- small illustrations
def ill_4_eu():
    """#4 EU summit — blue field, 12-star ring, crack, €45B plaque."""
    w, h = 180, 58
    img, d = _ss(w, h)
    d.rectangle([0, 0, 360, 116], fill=(29, 60, 120))          # #1D3C78
    import math
    for k in range(12):
        a = -math.pi / 2 + k * math.pi / 6
        _star(d, 128 + 42 * math.cos(a), 58 + 42 * math.sin(a), 9, 4,
              (250, 204, 21))
    d.line([(86, 8), (118, 58), (96, 108)], fill=(255, 255, 255), width=5)
    d.rectangle([238, 30, 348, 86], fill=(255, 255, 255))
    f = _font(SANS_B, 26)
    _draw_centered(d, 293, 48, "€45B", f, (15, 23, 42))
    return _finish(img, w, h)


def ill_5_kyiv():
    """#5 Kyiv/Odesa — night sky, red missile, city, grain ship on waves."""
    w, h = 180, 58
    img, d = _ss(w, h)
    d.rectangle([0, 0, 360, 116], fill=(58, 72, 95))           # lighter slate
    # city rectangles bottom-right with lit windows
    for x0, y0, x1 in ((210, 62, 244), (248, 48, 282), (286, 66, 316),
                       (320, 56, 352)):
        d.rectangle([x0, y0, x1, 96], fill=(15, 23, 42))
        for wy in range(y0 + 8, 90, 12):
            for wx in range(x0 + 6, x1 - 6, 12):
                if (wx * 3 + wy * 5) % 4 < 2:
                    d.rectangle([wx, wy, wx + 4, wy + 5], fill=(250, 204, 21))
    # red missile flying down-right from top-left, orange tail flame
    d.polygon([(30, 8), (96, 34), (88, 48), (22, 24)], fill=(200, 30, 30))
    d.polygon([(22, 24), (30, 8), (38, 14)], fill=(255, 255, 255))
    d.polygon([(18, 18), (2, 8), (10, 30)], fill=(234, 88, 12))
    # waves + grain ship at the bottom
    d.line([(0, 100), (60, 94), (120, 100), (180, 94), (240, 100),
            (300, 94), (360, 100)], fill=(59, 130, 246), width=4)
    d.line([(0, 110), (60, 104), (120, 110), (180, 104), (240, 110),
            (300, 104), (360, 110)], fill=(30, 64, 175), width=4)
    d.polygon([(96, 92), (180, 92), (172, 104), (104, 104)], fill=(154, 82, 26))
    d.rectangle([128, 80, 150, 92], fill=(154, 82, 26))
    return _finish(img, w, h)


def ill_6_bangkok():
    """#6 Bangkok refinery — towers left, fireball + smoke right."""
    w, h = 180, 58
    img, d = _ss(w, h)
    d.rectangle([0, 0, 360, 116], fill=(226, 232, 240))        # #E2E8F0
    # 3 distillation towers + horizontal pipe
    for x0 in (24, 62, 100):
        d.rectangle([x0, 34, x0 + 26, 116], fill=(71, 85, 105))
        d.polygon([(x0, 34), (x0 + 13, 18), (x0 + 26, 34)], fill=(71, 85, 105))
        d.line([(x0 + 4, 50), (x0 + 22, 50)], fill=(226, 232, 240), width=2)
        d.line([(x0 + 4, 74), (x0 + 22, 74)], fill=(226, 232, 240), width=2)
    d.rectangle([20, 84, 150, 92], fill=(71, 85, 105))
    # jagged fireball with yellow core
    d.polygon([(250, 108), (236, 84), (258, 78), (248, 58), (272, 66),
               (272, 44), (292, 60), (306, 42), (312, 66), (332, 58),
               (322, 82), (340, 88), (318, 100), (322, 112), (292, 104),
               (276, 116)], fill=(234, 88, 12))
    d.polygon([(272, 100), (266, 84), (280, 80), (278, 66), (292, 76),
               (302, 64), (306, 82), (316, 78), (306, 94), (310, 104),
               (292, 100), (284, 108)], fill=(250, 204, 21))
    # 3 smoke ellipses
    for cx, cy, rx, ry in ((262, 30, 22, 12), (300, 22, 26, 13),
                           (330, 34, 20, 11)):
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(100, 116, 139))
    return _finish(img, w, h)


def ill_7_bok():
    """#7 Bank of Korea — navy field, bars, red staircase arrow, 3.25%."""
    w, h = 180, 58
    img, d = _ss(w, h)
    d.rectangle([0, 0, 360, 116], fill=NAVY)
    # bars: red down bar, then two green rebound bars
    d.rectangle([30, 58, 66, 96], fill=(200, 30, 30))
    d.rectangle([82, 70, 118, 96], fill=(34, 197, 94))
    d.rectangle([134, 46, 170, 96], fill=(34, 197, 94))
    # red staircase arrow up-right
    d.line([(30, 96), (66, 96), (66, 70), (100, 70), (100, 46),
            (134, 46), (134, 22), (196, 22)], fill=(239, 68, 68), width=6)
    d.polygon([(196, 22), (168, 12), (168, 34)], fill=(239, 68, 68))
    f = _font(SANS_B, 30)
    d.text((212, 66), "3.25%", font=f, fill=(255, 255, 255))
    return _finish(img, w, h)


def ill_8_nk():
    """#8 North Korea — gray field, white missile, radiation trefoil, KCNA."""
    w, h = 180, 58
    img, d = _ss(w, h)
    d.rectangle([0, 0, 360, 116], fill=(51, 65, 85))           # #334155
    # white missile with red nose, tilted ~30 degrees up-right
    layer = Image.new("RGBA", (360, 116), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    ld.polygon([(20, 70), (150, 70), (176, 58), (150, 46)], fill=(255, 255, 255, 255))
    ld.polygon([(150, 46), (176, 58), (150, 70)], fill=(200, 30, 30, 255))
    ld.rectangle([28, 54, 44, 70], fill=(200, 30, 30, 255))
    layer = layer.rotate(-28, resample=Image.BICUBIC, center=(98, 58))
    img.paste(layer, (0, 0), layer)
    # radiation trefoil: yellow disc, 3 black sectors, black centre
    import math
    cx, cy, r = 296, 52, 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(250, 204, 21))
    for a0 in (90, 210, 330):
        d.pieslice([cx - r + 6, cy - r + 6, cx + r - 6, cy + r - 6],
                   a0 - 26, a0 + 26, fill=(15, 23, 42))
    d.ellipse([cx - 9, cy - 9, cx + 9, cy + 9], fill=(15, 23, 42))
    return _finish(img, w, h)


def ill_9_gaza():
    """#9 Gaza — dark violet-gray field, broken buildings, smoke, GAZA tag."""
    w, h = 180, 58
    img, d = _ss(w, h)
    d.rectangle([0, 0, 360, 116], fill=(72, 72, 80))           # lighter gray
    # 4 damaged buildings with jagged tops
    for pts in ([(16, 116), (16, 56), (34, 44), (52, 58), (70, 48),
                 (86, 116)],
                [(96, 116), (96, 72), (112, 60), (128, 74), (146, 64),
                 (160, 116)],
                [(170, 116), (170, 50), (190, 38), (206, 52), (224, 44),
                 (238, 116)],
                [(248, 116), (248, 66), (264, 54), (282, 68), (300, 60),
                 (316, 116)]):
        d.polygon(pts, fill=(125, 125, 135))
    # smoke ellipses
    for cx, cy, rx, ry in ((60, 34, 26, 12), (200, 26, 30, 13),
                           (290, 40, 22, 11)):
        d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(150, 150, 160))
    return _finish(img, w, h)


def ill_10_ebola():
    """#10 Ebola — pale alert field, red cross, 12,021, virus ring."""
    w, h = 180, 58
    img, d = _ss(w, h)
    d.rectangle([0, 0, 360, 116], fill=(254, 242, 242))        # #FEF2F2
    # red circle, white cross
    d.ellipse([14, 22, 94, 102], fill=(200, 30, 30))
    d.rectangle([46, 34, 62, 90], fill=(255, 255, 255))
    d.rectangle([26, 54, 82, 70], fill=(255, 255, 255))
    # big dark-red case count
    f = _font(SANS_B, 40)
    d.text((112, 30), "12,021", font=f, fill=(153, 27, 27))
    # green virus ring with spikes
    import math
    cx, cy, r = 306, 62, 26
    for k in range(8):
        a = k * math.pi / 4
        d.line([(cx + (r - 4) * math.cos(a), cy + (r - 4) * math.sin(a)),
                (cx + (r + 10) * math.cos(a), cy + (r + 10) * math.sin(a))],
               fill=(21, 128, 61), width=4)
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=(21, 128, 61), width=5)
    d.ellipse([cx - 8, cy - 8, cx + 8, cy + 8], fill=(21, 128, 61))
    return _finish(img, w, h)


def ill_11_tides():
    """#11 California king tides — gray sky, waves, broken pier, gauge."""
    w, h = 180, 58
    img, d = _ss(w, h)
    d.rectangle([0, 0, 360, 116], fill=(203, 213, 225))        # #CBD5E1
    # broken pier: tilted planks half-submerged
    d.polygon([(30, 66), (150, 58), (160, 66), (120, 74), (60, 80),
               (34, 76)], fill=(120, 113, 108))
    for x in range(40, 150, 18):
        d.line([(x, 64), (x + 4, 78)], fill=(87, 83, 78), width=2)
    d.line([(150, 58), (170, 40)], fill=(120, 113, 108), width=6)
    # 3 wave lines
    for y0, col in ((82, (2, 132, 199)), (96, (15, 76, 129)),
                    (108, (2, 132, 199))):
        pts = []
        for x in range(0, 361, 20):
            pts.append((x, y0 + (6 if (x // 20) % 2 == 0 else -6)))
        d.line(pts, fill=col, width=5)
    # gauge pill with water height (no invented numbers: ticks + HIGH only)
    d.rounded_rectangle([300, 22, 352, 96], radius=8, fill=(15, 23, 42))
    d.rectangle([310, 52, 342, 86], fill=(2, 132, 199))
    for ty in (34, 48, 62, 76, 90):
        d.line([(304, ty), (312, ty)], fill=(255, 255, 255), width=2)
    return _finish(img, w, h)


def ill_12_brazil():
    """#12 Brazil tariffs — stacked containers + red TARIFFS stamp."""
    w, h = 180, 58
    img, d = _ss(w, h)
    d.rectangle([0, 0, 360, 116], fill=(241, 245, 249))        # #F1F5F9
    # two stacked containers, bottom-left
    for y0, col in ((66, (22, 163, 74)), (30, (37, 99, 235))):
        d.rectangle([16, y0, 156, y0 + 34], fill=col)
        for x in range(28, 150, 14):
            d.line([(x, y0 + 3), (x, y0 + 31)], fill=(255, 255, 255), width=2)
    # downward arrow
    d.line([(250, 20), (250, 52)], fill=(200, 30, 30), width=5)
    d.polygon([(250, 60), (238, 46), (262, 46)], fill=(200, 30, 30))
    # red TARIFFS stamp, rotated -12 degrees, on the light right side
    # (clear of the green/blue containers so the red does not clash)
    layer = Image.new("RGBA", (360, 116), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    f = _font(SANS_B, 30)
    tw = ld.textlength("TARIFFS", font=f)
    ld.rectangle([260 - tw / 2 - 8, 62, 260 + tw / 2 + 8, 100],
                 outline=(200, 30, 30, 255), width=4)
    ld.text((260 - tw / 2, 68), "TARIFFS", font=f, fill=(200, 30, 30, 255))
    layer = layer.rotate(-12, resample=Image.BICUBIC, center=(260, 81))
    img.paste(layer, (0, 0), layer)
    return _finish(img, w, h)


def ill_13_iss():
    """#13 Progress 97 docks at ISS — starfield, truss + solar wings, ship."""
    w, h = 180, 58
    img, d = _ss(w, h)
    d.rectangle([0, 0, 360, 116], fill=(11, 19, 43))           # #0B132B
    # 8 stars
    for sx, sy, r in ((20, 16, 3), (70, 10, 2), (120, 22, 3), (180, 12, 2),
                      (240, 18, 3), (300, 10, 2), (340, 26, 3), (30, 96, 2)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(255, 255, 255))
    # gold truss + blue solar wings
    d.rectangle([120, 40, 240, 52], fill=GOLD)
    for x in range(126, 236, 12):
        d.line([(x, 40), (x + 8, 52)], fill=(146, 64, 14), width=2)
    for x0 in (30, 252):
        d.rectangle([x0, 34, x0 + 78, 58], fill=(29, 78, 216))
        for gx in range(x0 + 10, x0 + 78, 13):
            d.line([(gx, 34), (gx, 58)], fill=(147, 197, 253), width=2)
    # silver cargo cylinder docking from below
    d.rounded_rectangle([160, 62, 200, 104], radius=8, fill=(203, 213, 225))
    d.rectangle([168, 70, 192, 76], fill=(100, 116, 139))
    d.rectangle([168, 84, 192, 90], fill=(100, 116, 139))
    d.line([(180, 52), (180, 62)], fill=(203, 213, 225), width=4)
    return _finish(img, w, h)


ILLUSTRATIONS = {1: ill_1_macys, 2: ill_2_mumbai, 3: ill_3_chess,
                 4: ill_4_eu, 5: ill_5_kyiv, 6: ill_6_bangkok,
                 7: ill_7_bok, 8: ill_8_nk, 9: ill_9_gaza,
                 10: ill_10_ebola, 11: ill_11_tides, 12: ill_12_brazil,
                 13: ill_13_iss}

# --------------------------------------------------------------------- map
def draw_map():
    """World map 348x186 at 1x, drawn 2x and downscaled (equirectangular)."""
    w, h = 348, 186
    img, d = _ss(w, h)
    d.rectangle([0, 0, 696, 372], fill=OCEAN)

    def proj(lon, lat):
        return ((lon + 180) / 360 * 696, (90 - lat) / 180 * 372)

    for poly in CONTINENTS:
        d.polygon([proj(lon, lat) for lon, lat in poly],
                  fill=LAND, outline=LAND_EDGE)
    return _finish(img, w, h)


def draw_pins(d, map_x, map_y, map_w, map_h):
    """Numbered red pins 1-12 + ORBIT #13 box, at 1x on the main canvas."""
    def proj(lon, lat):
        return (map_x + (lon + 180) / 360 * map_w,
                map_y + (90 - lat) / 180 * map_h)

    # dashed ISS ground-track: centred on the equator, amplitude ~50px so
    # the wave reaches about +/-51.6 deg latitude (the real ISS inclination)
    import math
    prev = None
    for x in range(map_x + 8, map_x + map_w - 8, 4):
        t = (x - map_x) / map_w
        y = map_y + map_h * 0.5 + 50 * math.sin(t * math.pi * 2.2 - 0.6)
        if prev is not None and (x // 12) % 2 == 0:
            d.line([prev, (x, y)], fill=RED, width=2)
        prev = (x, y)

    for s in STORIES:
        if s["tier"] == "list":
            continue
        sid = s["id"]
        if sid == 13:
            # ORBIT box centred on the projected ISS point (South Pacific)
            cx, cy = proj(s["lon"], s["lat"])
            f = _font(SANS_B, 8)
            label = "ORBIT #13 (ISS)"
            tw = d.textlength(label, font=f)
            bw, bh = tw + 12, 18
            x0, y0 = cx - bw / 2, cy - bh / 2
            d.rounded_rectangle([x0, y0, x0 + bw, y0 + bh], radius=3,
                                fill=(255, 255, 255), outline=RED, width=1)
            _draw_centered(d, cx, y0 + 5, label, f, RED)
            continue
        x, y = proj(s["lon"], s["lat"])
        dx, dy = s.get("dx", 0), s.get("dy", 0)
        if dx or dy:
            d.line([(x, y), (x + dx, y + dy)], fill=RED, width=1)
            x, y = x + dx, y + dy
        _badge(d, x, y, 8, sid)


# -------------------------------------------------------------------- main
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    heroes = [s for s in STORIES if s["tier"] == "hero"]
    cards = [s for s in STORIES if s["tier"] == "card"]
    listed = [s for s in STORIES if s["tier"] == "list"]
    assert len(STORIES) == 36 and len(heroes) == 3 and len(cards) == 10
    assert len(listed) == 23

    # ------------------------------------------------- 1. kicker (12..34)
    f_kick = _font(SANS_B, 11)
    d.text((MX, 14), KICKER_LEFT, font=f_kick, fill=INK)
    rw = d.textlength(KICKER_RIGHT, font=f_kick)
    d.text((MX + CW - rw, 14), KICKER_RIGHT, font=f_kick, fill=INK2)
    d.rectangle([MX, 35, MX + CW, 35], fill=RULE)

    # --------------------------------------- 2. date masthead (36..114)
    # "Thursday, " + red "26 November" + " 2026", 62px serif bold, centred.
    f_date, date_size = fit_font(d, EDITION_DATE, SERIF_B, 62, CW)
    parts = [("Thursday, ", INK), ("26 November", RED), (" 2026", INK)]
    total = sum(d.textlength(t, font=f_date) for t, _ in parts)
    x = MX + (CW - total) / 2
    for text, color in parts:
        d.text((x, 34), text, font=f_date, fill=color)
        x += d.textlength(text, font=f_date)
    f_deck, _ = fit_font(d, DECK, SERIF_I, 14, CW, min_size=12)
    _draw_centered(d, MX + CW / 2, 100, DECK, f_deck, INK2)

    # --------------------------------- 3. region bar + numbers (116..182)
    f_reg = _font(SANS_B, 10)
    rx = MX
    for name, short, count, color in REGIONS:
        seg_w = CW * count / 36
        fill = _hex(color)
        d.rectangle([rx, 116, rx + seg_w, 136], fill=fill)
        label = f"{short} {count}"
        lw = d.textlength(label, font=f_reg)
        txt_color = INK if color == "#D49A3A" else (255, 255, 255)
        d.text((rx + (seg_w - lw) / 2, 120), label, font=f_reg,
               fill=txt_color)
        rx += seg_w
    d.rectangle([MX, 140, MX + CW, 182], fill=NAVY)
    col_w = CW / 5
    f_val = _font(SANS_B, 24)
    f_lab = _font(SANS_B, 9)
    for i, (value, label) in enumerate(BY_THE_NUMBERS):
        cx = MX + col_w * (i + 0.5)
        _draw_centered(d, cx, 144, value, f_val, (255, 255, 255))
        _draw_centered(d, cx, 170, label, f_lab, (203, 213, 225))
        if i:
            d.line([MX + col_w * i, 146, MX + col_w * i, 176],
                   fill=(51, 65, 85), width=1)

    # --------------------------------------- 4. hero stories (188..376)
    f_htitle = _font(SANS_B, 21)
    f_hsum = _font(SANS_R, 12)
    f_hbot = _font(SANS_R, 10)
    f_hbot_b = _font(SANS_B, 10)
    for i, s in enumerate(heroes):
        x0 = MX + i * (317 + 12)
        ill = ILLUSTRATIONS[s["id"]]()
        img.paste(ill, (x0 + 4, 188))
        _badge(d, x0 + 4 + 14, 188 + 14, 10, s["id"])
        title_lines = wrap_lines(d, s["title"], f_htitle, 317, 2)
        y = 296
        for line in title_lines:
            d.text((x0, y), line, font=f_htitle, fill=INK)
            y += 22
        sum_lines = wrap_lines(d, s["summary"], f_hsum, 317, 2)
        y = 341
        for line in sum_lines:
            d.text((x0, y), line, font=f_hsum, fill=INK2)
            y += 13
        by = 368
        d.text((x0, by), s["source"], font=f_hbot, fill=GRAY)
        sw = d.textlength(s["source"], font=f_hbot)
        d.text((x0 + sw + 6, by), s["tag"], font=f_hbot_b,
               fill=TAG_COLOR[s["tag"]])

    # ---------------------------------------- 5. cards 5x2 (382..630)
    f_ctitle = _font(SANS_B, 13)
    f_cbot = _font(SANS_R, 9)
    f_cbot_b = _font(SANS_B, 9)
    for i, s in enumerate(cards):
        col, row = i % 5, i // 5
        x0 = 26 + col * (188 + 8)
        y0 = 382 + row * (120 + 8)
        d.rounded_rectangle([x0, y0, x0 + 188, y0 + 120], radius=4,
                            fill=CARD, outline=BORDER, width=1)
        ill = ILLUSTRATIONS[s["id"]]()
        img.paste(ill, (x0 + 4, y0 + 5))
        _badge(d, x0 + 4 + 12, y0 + 5 + 12, 8, s["id"])
        title_lines = wrap_lines(d, s["title"], f_ctitle, 180, 2)
        y = y0 + 67
        for line in title_lines:
            d.text((x0 + 4, y), line, font=f_ctitle, fill=INK)
            y += 15
        by = y0 + 103
        d.text((x0 + 4, by), s["source"], font=f_cbot, fill=GRAY)
        sw = d.textlength(s["source"], font=f_cbot)
        d.text((x0 + 4 + sw + 4, by), s["tag"], font=f_cbot_b,
               fill=TAG_COLOR[s["tag"]])

    # --------------------------------------- 6. UTC timeline (636..668)
    d.rectangle([MX, 636, MX + CW, 668], fill=SAND)
    d.rounded_rectangle([MX + 6, 641, MX + 128, 663], radius=9, fill=NAVY)
    f_tl_cap = _font(SANS_B, 10)
    _draw_centered(d, MX + 67, 646, "THE DAY IN UTC", f_tl_cap,
                   (255, 255, 255))
    f_tl_t = _font(SANS_B, 11)
    f_tl_l = _font(SANS_R, 11)
    slot_x, slot_w = MX + 140, (MX + CW - (MX + 140)) / len(UTC_TIMELINE)
    for i, (time, label) in enumerate(UTC_TIMELINE):
        cx = slot_x + slot_w * i
        d.ellipse([cx, 648, cx + 7, 655], fill=RED)
        tx = cx + 11
        d.text((tx, 645), time, font=f_tl_t, fill=RED)
        tw = d.textlength(time, font=f_tl_t)
        d.text((tx + tw + 4, 645), label, font=f_tl_l, fill=INK2)

    # --------------------------------- 7. map, left bottom (674..898)
    f_map_t = _font(SANS_B, 18)
    d.text((MX, 674), "WHERE IT HAPPENED", font=f_map_t, fill=INK)
    map_img = draw_map()
    img.paste(map_img, (MX, 698))
    d.rectangle([MX, 698, MX + 348, 698 + 186], outline=BORDER, width=1)
    draw_pins(d, MX, 698, 348, 186)
    f_map_f = _font(SANS_R, 9)
    d.text((MX, 888), "PINS 1–12 MARK STORY LOCATIONS · #13 SHOWS THE ISS ORBIT",
           font=f_map_f, fill=GRAY)

    # --------------------------------- 8. one-line list, right (674..898)
    f_list_h = _font(SANS_B, 11)
    d.text((384, 674), "AND ALSO — STORIES 14–36", font=f_list_h, fill=INK)
    f_num = _font(SANS_B, 11)
    f_line = _font(SANS_R, 11)
    row_y0, row_h = 690, 16.8
    for j, s in enumerate(listed):
        col, row = j // 12, j % 12
        x0 = 384 + col * (302 + 12)
        y = row_y0 + row * row_h
        tag_color = TAG_COLOR[s["tag"]]
        d.text((x0, y), str(s["id"]), font=f_num, fill=tag_color)
        nw = d.textlength(str(s["id"]) + "  ", font=f_num)
        tx = x0 + nw
        d.text((tx, y), s["line_text"], font=f_line, fill=INK)
        lw = d.textlength(s["line_text"], font=f_line)
        d.text((tx + lw + 4, y), "· " + s["short_source"], font=f_line,
               fill=GRAY)
        total_w = (nw + lw + 4
                   + d.textlength("· " + s["short_source"], font=f_line))
        if total_w > 302:
            raise ValueError(f"list row #{s['id']} is {total_w:.0f}px > 302px")

    # --------------------------------------- 9. DATE CHECK (904..968)
    d.rounded_rectangle([MX, 904, MX + CW, 968], radius=4,
                        fill=DC_BG, outline=RED, width=2)
    f_dc_t = _font(SANS_B, 11)
    d.text((MX + 10, 909), "DATE CHECK — EXCLUDED NEAR-MISSES",
           font=f_dc_t, fill=RED)
    f_dc = _font(SANS_R, 10)
    for i, item in enumerate(DATE_CHECK):
        col, row = i // 4, i % 4
        x0 = MX + 10 + col * 478
        y = 924 + row * 10
        d.text((x0, y), "× ", font=_font(SANS_B, 10), fill=RED)
        d.text((x0 + 11, y), item, font=f_dc, fill=INK2)

    # ----------------------------------------- 10. footer (972..1012)
    f_f1 = _font(SANS_R, 10)
    d.text((MX, 972),
           "Every story here happened or was first reported on Thursday "
           "26 November 2026. " + UPCOMING_LINE, font=f_f1, fill=INK2)
    f_f2 = _font(SANS_R, 9)
    fx = MX
    fy = 984
    for tag, expl in (("OFFICIAL", "official sources"),
                      ("CONFIRMED", "2+ independent sources"),
                      ("REPORTED", "single source"),
                      ("CLAIM", "one-sided assertion")):
        d.rectangle([fx, fy + 1, fx + 8, fy + 9], fill=TAG_COLOR[tag])
        fx += 12
        seg = f"{tag} = {expl}    "
        d.text((fx, fy), seg, font=f_f2, fill=INK2)
        fx += d.textlength(seg, font=f_f2)
    d.text((MX, 995),
           "Sources: NYC Mayor, Macy's, U.S. Embassy, FIDE, EU Council, "
           "Bank of Korea, KCNA, NASA, WHO, IBGE + 20 more · All scenes "
           "are original flat-vector drawings, not photographs.",
           font=f_f2, fill=GRAY)

    out = Path(__file__).resolve().parent / "entry.png"
    img.save(out, format="PNG", optimize=True, compress_level=9)
    size = out.stat().st_size
    assert size <= MAX_BYTES, f"entry.png is {size} bytes > 1 MiB"
    preview = img.resize((300, 300), Image.Resampling.LANCZOS)
    preview.save("/tmp/preview_300.png", format="PNG", optimize=True,
                 compress_level=9)
    print(f"saved {out} ({size} bytes)")
    print(f"date font size: {date_size}px, deck font size: 14px (fit)")
    print("preview: /tmp/preview_300.png")


if __name__ == "__main__":
    main()
