# Ciclovia del Navile — bike navigation

A GPS-ready version of the [Ciclovia del Navile](https://www.bolognawelcome.com/it/blog/percorso-ciclabile-lungo-il-canale-navile)
cycle route: **Bologna (Porta Galliera) → Malalbergo**, following the historic Navile canal.
~30 km, mostly flat, mixed surface (paved + gravel — MTB, gravel or a sturdy city bike).

## Two ways to use it

### 1. The map app (phone-friendly)
Open **`index.html`** — hosted on GitHub Pages it becomes a live map you can use in the field:

- The full route drawn along the canal
- All 15 points of interest as tappable markers (locks, museums, parks, villages)
- A **live GPS "blue dot"** — tap the ⊚ button to show your position; tap again for **follow mode**
- A readout of the nearest point of interest and how far away it is
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

## A note on accuracy

The **waypoints** are placed on the real locations. The **track line** follows the canal's
course and is precise through the Bologna urban section; the rural
Bentivoglio → Malalbergo stretch is *indicative*. For exact turn-by-turn, import the GPX into
OsmAnd/Komoot and let it snap the route to mapped paths, or re-trace it in
[BRouter](https://brouter.de/brouter-web/) with the "trekking" bike profile.

The official route is not signposted — carry a map/GPS, watch for limited water sources,
and check the weather before you go.

## Editing the route

Both files are generated from one source of truth. Edit the `POIS` / `TRACK` lists in
`gen.py` and regenerate:

```bash
python3 gen.py    # rewrites docs/navile.gpx and docs/data.js
```
