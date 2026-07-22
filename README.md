# Ciclovia del Navile — bike navigation

A GPS-ready version of the [Ciclovia del Navile](https://www.bolognawelcome.com/it/blog/percorso-ciclabile-lungo-il-canale-navile)
cycle route, door to door: **Casalecchio di Reno (Via Don Filippo Ercolani) → Bologna → Malalbergo**,
following the historic Navile canal. Mostly flat, mixed surface (paved + gravel — MTB, gravel or a
sturdy city bike). Starting from Casalecchio adds the crossing of Bologna before the canal proper.

Along the way the map shows **attraction pins** (★) for stops worth a short detour — the Chiusa di
Casalecchio, Parco della Montagnola, the Castello di Bentivoglio and more — each with a pop-up.

## Two ways to use it

### 1. The map app (phone-friendly)
Open **`index.html`** — hosted on GitHub Pages it becomes a live map you can use in the field:

- The full route drawn along the canal
- All 15 points of interest as tappable markers (locks, museums, parks, villages)
- A **live GPS "blue dot"** with **follow mode** (starts automatically; tap ⊚ to recenter)
- **Turn-by-turn navigation** with **named-street instructions** (via the OSRM cycling router,
  e.g. *"Turn left onto Via della Beverara"*): a nav card shows the next maneuver and the distance
  to it, plus live **km remaining, ETA, and the next stop** — with an off-route warning
- **Voice guidance** — tap the 🔈 button to hear each turn announced (~150 m ahead and at the turn)
- **Auto-zoom** that tightens as you approach a turn, **keep-screen-awake** while navigating, and an
  **elevation profile** (⛰ button) with total ascent/descent, fetched in-browser from Open-Meteo
- A **↓ GPX** button and per-point "Directions to here" links

The site lives in **`docs/`**. To publish it: go to **Settings → Pages**, set
**Source: Deploy from a branch**, **Branch: `main` / `docs`**, and Save. Your app goes live at
**https://khakpour27.github.io/test/** within a minute or two.
(GPS requires HTTPS, which GitHub Pages provides automatically.)

### 2. The GPX file (any navigation app)
**`navile.gpx`** works in every major free app — import it and navigate offline:

- **OsmAnd** / **Organic Maps** — import the GPX, download the offline map of Emilia-Romagna, and get turn-by-turn along real paths.
- **Komoot** — import as a Tour to get bike routing snapped to trails.
- **Strava**, **Garmin Connect**, **Locus Map**, **Cabo**, **Ride with GPS** — all read GPX.

The file contains named **waypoints** for each point of interest plus a **track** of the route line.

## Points of interest (in order)

1. Porta Galliera (start) — by Bologna Centrale station
2. Sostegno della Bova — where the canal was born (1221)
3. Parco di Villa Angeletti
4. Sostegno del Battiferro — best-preserved lock
5. Museo del Patrimonio Industriale
6. Sostegno del Torreggiani
7. Sostegno del Landi
8. Sostegno del Grassi (rebuilt by Vignola)
9. Ponte della Bionda / Corticella — Bologna's first river port
10. Ponte di Corticella — bridge dating to 1289
11. Castel Maggiore — end of the urban stretch
12. San Marino di Bentivoglio — Villa Smeraldi & Museum of Rural Life
13. Bentivoglio
14. Oasi La Rizza — nature reserve, birdwatching
15. Malalbergo (end)

## How positions are made accurate

Nothing critical relies on my hand-typed coordinates. When `index.html` loads in your browser it
resolves everything against **live OpenStreetMap data**:

- **The route line** is traced from the real **Canale Navile** geometry (fetched via the
  [Overpass API](https://overpass-api.de)), then snapped to actual cycleways/towpaths with the
  [BRouter](https://brouter.de) cycling engine — so it follows the canal path, not a straight guess.
- **Every stop and attraction** is geocoded to its real OSM location
  ([Nominatim](https://nominatim.openstreetmap.org)) and cached in your browser, so it only looks up
  once per device.
- The in-app **↓ GPX** button exports whatever the app is currently showing (the snapped track +
  resolved waypoints).

Each step falls back gracefully (and the banner tells you which path it took) if a service is
unreachable. The hardcoded values in `gen.py` / `docs/navile.gpx` are only fallbacks and a coarse
offline overview — for exact turn-by-turn use the app's GPX export or import any GPX into
OsmAnd/Komoot.

The official route is not signposted — carry a map/GPS, watch for limited water sources,
and check the weather before you go.

## Editing the route

Both files are generated from one source of truth. Edit the `POIS` / `TRACK` lists in
`gen.py` and regenerate:

```bash
python3 gen.py    # rewrites docs/navile.gpx and docs/data.js
```
