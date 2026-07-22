#!/usr/bin/env python3
"""Generate navile.gpx and route data (data.js) from a single source of truth."""
import json, html, os

OUT = os.environ.get("OUT_DIR", "docs")

# --- Start point (resolved to the exact address in-browser; these are fallback coords) ---
# name, geocode query, fallback lat, fallback lon, description
START = ("Start · Via Don Filippo Ercolani",
         "Via Don Filippo Ercolani, Casalecchio di Reno, Italy",
         44.4775, 11.2860,
         "Ride start in Casalecchio di Reno. From here the route crosses to Bologna and picks up the Navile canal.")

# --- Route waypoints along the canal (accurate anchors) ---
# name, lat, lon, description
POIS = [
    ("Porta Galliera", 44.5045, 11.3478,
     "Gateway to the Ciclovia del Navile, by the Montagnola park near Bologna Centrale station."),
    ("Sostegno della Bova", 44.5090, 11.3388,
     "Historic canal lock just outside Porta Lame, where the Navile canal was born (1221)."),
    ("Parco di Villa Angeletti", 44.5160, 11.3460,
     "Large green park along the right bank of the canal - a good first rest stop."),
    ("Sostegno del Battiferro", 44.5230, 11.3432,
     "The best-preserved lock on the whole canal."),
    ("Museo del Patrimonio Industriale", 44.5242, 11.3437,
     "Industrial Heritage Museum, via della Beverara 123. Bologna's economy from the Modern age onward."),
    ("Sostegno del Torreggiani", 44.5300, 11.3470,
     "One of the 15th-16th century canal locks along the urban stretch."),
    ("Sostegno del Landi", 44.5360, 11.3500,
     "15th-16th century canal lock."),
    ("Sostegno del Grassi (Vignola)", 44.5420, 11.3530,
     "Lock rebuilt by the architect Vignola."),
    ("Ponte della Bionda / Corticella", 44.5488, 11.3552,
     "Cross the Ponte della Bionda to reach Corticella, site of Bologna's first river port."),
    ("Ponte di Corticella", 44.5512, 11.3585,
     "Bridge documented since the 13th century, dating to 1289."),
    ("Castel Maggiore", 44.5760, 11.3625,
     "End of the urban stretch; the landscape opens into farmland."),
    ("San Marino di Bentivoglio - Villa Smeraldi", 44.6265, 11.3480,
     "Museo della Civilta Contadina (Museum of Rural Life) inside the majestic Villa Smeraldi."),
    ("Bentivoglio", 44.6360, 11.3520,
     "Village on the plain; small detours reach museums and nature areas."),
    ("Oasi La Rizza", 44.6480, 11.3720,
     "Protected natural area, ideal for birdwatching."),
    ("Malalbergo (end)", 44.7157, 11.5343,
     "End of the route on the plain, along natural paths and short road sections - ride with care."),
]

# --- Attractions worth a stop or short detour (shown as distinct pins, refined in-browser) ---
# name, geocode query, fallback lat, fallback lon, description
ATTRACTIONS = [
    ("Chiusa di Casalecchio",
     "Chiusa di Casalecchio, Casalecchio di Reno, Italy", 44.4886, 11.2846,
     "Medieval sluice-dam on the River Reno (rebuilt 14th c.), a National Monument that still feeds Bologna's canals."),
    ("Parco della Chiusa (Parco Talon)",
     "Parco della Chiusa, Casalecchio di Reno, Italy", 44.4930, 11.2840,
     "Large riverside park of woods, meadows and old villa grounds, just above the Chiusa."),
    ("Parco della Montagnola",
     "Parco della Montagnola, Bologna, Italy", 44.4998, 11.3452,
     "Bologna's oldest public park, with a monumental stair down toward the old Navile port quarter."),
    ("Museo del Patrimonio Industriale",
     "Museo del Patrimonio Industriale, Bologna, Italy", 44.5242, 11.3437,
     "Working models and machines telling the story of Bologna's water-powered industry (via della Beverara 123)."),
    ("Castello di Bentivoglio (Ponte Poledrano)",
     "Castello di Bentivoglio, Bentivoglio, Italy", 44.6372, 11.3520,
     "15th-century castle of Giovanni II Bentivoglio, with the frescoed 'Sala del Vaso'."),
    ("Oasi La Rizza",
     "Oasi La Rizza, Bentivoglio, Italy", 44.6480, 11.3720,
     "Protected wetland reserve in the Bentivoglio woods - hides, trails and great birdwatching."),
]

# --- Track: Casalecchio -> Bologna prefix, then the canal course. Fallback line only;
# the app snaps this to real bike paths in the browser. ---
PREFIX = [
    (44.4775, 11.2860), (44.4810, 11.2950), (44.4850, 11.3060), (44.4890, 11.3170),
    (44.4935, 11.3280), (44.4985, 11.3390), (44.5045, 11.3478),
]
CANAL = [
    (44.5062, 11.3470), (44.5080, 11.3430), (44.5090, 11.3388),
    (44.5105, 11.3388), (44.5130, 11.3420), (44.5160, 11.3460), (44.5195, 11.3450),
    (44.5230, 11.3432), (44.5242, 11.3437), (44.5275, 11.3452), (44.5300, 11.3470),
    (44.5335, 11.3488), (44.5360, 11.3500), (44.5400, 11.3520), (44.5420, 11.3530),
    (44.5460, 11.3545), (44.5488, 11.3552), (44.5512, 11.3585), (44.5560, 11.3600),
    (44.5620, 11.3615), (44.5690, 11.3620), (44.5760, 11.3625), (44.5820, 11.3600),
    (44.5900, 11.3560), (44.5980, 11.3520), (44.6060, 11.3500), (44.6140, 11.3490),
    (44.6210, 11.3485), (44.6265, 11.3480), (44.6320, 11.3500), (44.6360, 11.3520),
    (44.6410, 11.3600), (44.6480, 11.3720), (44.6560, 11.3900), (44.6650, 11.4150),
    (44.6780, 11.4450), (44.6900, 11.4800), (44.7000, 11.5050), (44.7080, 11.5220),
    (44.7157, 11.5343),
]
TRACK = PREFIX + CANAL

# --- Write GPX ---
def esc(s): return html.escape(s, quote=True)

def wpt(name, lat, lon, desc, sym):
    return [f'  <wpt lat="{lat}" lon="{lon}">',
            f'    <name>{esc(name)}</name>',
            f'    <desc>{esc(desc)}</desc>',
            f'    <sym>{sym}</sym>',
            '  </wpt>']

gpx = ['<?xml version="1.0" encoding="UTF-8"?>']
gpx.append('<gpx version="1.1" creator="Ciclovia del Navile" '
           'xmlns="http://www.topografix.com/GPX/1/1" '
           'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
           'xsi:schemaLocation="http://www.topografix.com/GPX/1/1 '
           'http://www.topografix.com/GPX/1/1/gpx.xsd">')
gpx += ['  <metadata>',
        '    <name>Ciclovia del Navile</name>',
        '    <desc>Casalecchio di Reno to Malalbergo via Bologna and the Navile canal.</desc>',
        '  </metadata>']
gpx += wpt(START[0], START[2], START[3], START[4], "Flag")
for name, lat, lon, desc in POIS:
    gpx += wpt(name, lat, lon, desc, "Waypoint")
for name, q, lat, lon, desc in ATTRACTIONS:
    gpx += wpt(name, lat, lon, desc, "Tourist Info")
gpx += ['  <trk>', '    <name>Ciclovia del Navile</name>', '    <trkseg>']
for lat, lon in TRACK:
    gpx.append(f'      <trkpt lat="{lat}" lon="{lon}"></trkpt>')
gpx += ['    </trkseg>', '  </trk>', '</gpx>']
with open(os.path.join(OUT, "navile.gpx"), "w") as f:
    f.write("\n".join(gpx) + "\n")

# --- Write data.js for the web app ---
data = {
    "start": {"name": START[0], "query": START[1], "lat": START[2], "lon": START[3], "desc": START[4]},
    "pois": [{"name": n, "lat": la, "lon": lo, "desc": d} for (n, la, lo, d) in POIS],
    "attractions": [{"name": n, "query": q, "lat": la, "lon": lo, "desc": d}
                    for (n, q, la, lo, d) in ATTRACTIONS],
    "track": [[la, lo] for (la, lo) in TRACK],
}
with open(os.path.join(OUT, "data.js"), "w") as f:
    f.write("window.NAVILE = " + json.dumps(data, ensure_ascii=False, indent=2) + ";\n")

print("Wrote navile.gpx and data.js:", 1 + len(POIS), "waypoints,",
      len(ATTRACTIONS), "attractions,", len(TRACK), "track points")
