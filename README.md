# Onibus Pulse

Bringing the heartbeat of the city to your pocket.

Onibus Pulse is a high-performance, cross-platform transit tracker designed to eliminate "bus stop anxiety." By transforming raw data from onibus.info into a sleek, real-time dashboard, it helps commuters make informed decisions: Should I run for the bus, or grab a coffee?

## 🎯 User-First Features

### ⚡ Pulse Dashboard (MVP)

- One-Tap Favorites: Instantly view your most-used lines and their proximity on app launch.
- Live ETA Engine: A smart countdown timer that merges scheduled arrival times with real-time scraped delays.
- Proximity Discovery: Uses device location to find nearby stops and active lines within walking distance.
- Visual Route Mapping: Track the live "Pulse" of buses on an interactive map with shape-accurate paths.

## 🛠 Tech Stack

- **Frontend**: (Planned/In-progress)
- **Backend**: FastAPI (Python)
- **Scraping/Engine**: Selenium + requests + BeautifulSoup (for Cloudflare bypass and parsing)
- **Persistence**: Optional local caching (offline mode intent)

## 🏗 Monorepo System Architecture

- `onibus_pulse_backend/`
  - `main.py`: FastAPI entrypoint with Pydantic models and endpoints.
  - `scraper.py`: `OnibusScraper` class for web scraping and transformation.
  - `examples/`: sample data and HAR traces.
- `onibus_pulse_frontend/`
  - `lib/`: contains frontend source code.

## 📲 Runtime app flow

1. Frontend calls `GET /routes/list` to load available routes.
2. User selects a route to see `GET /routes/{route_id}` data (direction/trips).
3. Selects trip shape to load stops from `GET /stops/{shape_id}`.
4. Select stop, then load ETA with `GET /eta/{route_id}/{shape_id}/{stop_id}`.
5. Refresh mechanism every 5 minutes and supports pull-to-refresh.

## ▶️ Quick Start (Local)

### Prerequisites

- Python 3.10+
- Chrome + chromedriver (for scraper path)

### Backend

```bash
cd onibus_pulse_backend
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend

```bash
cd onibus_pulse_frontend
```

### API Host Notes

- Android emulator: `http://10.0.2.2:8000`
- iOS simulator / desktop: `http://localhost:8000`

## 🧩 Planned Enhancements

- Crowdsourced accuracy feedback buttons
- Multi-route watch mode
- Low-data text mode with minimal UI
- Favorites and offline caches
- Map and geofencing trip alerts

## 📜 License & DISCLAIMER

- MIT License
- Not affiliated with or endorsed by onibus.info. Data is provided "as-is".
