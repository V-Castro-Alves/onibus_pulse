# 🚌 Onibus Pulse

> Bringing the heartbeat of the city to your pocket.

**Onibus Pulse** is a high-performance, cross-platform transit tracker built to eliminate *bus stop anxiety*. It transforms raw data from [onibus.info](https://onibus.info) into a sleek, real-time dashboard — so you can answer the only question that matters: *should I run, or grab a coffee?*

---

## ✨ Features

| Feature | Description |
|---|---|
| ⚡ **Live ETA Engine** | Countdown timers merging scheduled arrivals with real-time scraped delays |
| ⭐ **One-Tap Favorites** | Instantly surface your most-used lines on launch |
| 📍 **Proximity Discovery** | Finds nearby stops and active lines within walking distance |
| 🗺️ **Visual Route Mapping** | Track buses live on an interactive map with shape-accurate paths |

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | React + Vite (TypeScript), Capacitor *(planned)* |
| **Backend** | FastAPI (Python) |
| **Scraping** | Selenium + Requests + BeautifulSoup |
| **Persistence** | Local caching for offline mode *(planned)* |

---

## 🏗️ Project Structure

```
onibus-pulse/
├── onibus_pulse_backend/
│   ├── main.py          # FastAPI entrypoint (routes, Pydantic models)
│   ├── scraper.py       # OnibusScraper class (scraping + transformation)
│   └── examples/        # Sample data and HAR traces
└── onibus_pulse_frontend/
    ├── src/             # React components, screens, assets
    └── public/          # Static assets
```

---

## 📲 App Flow

```
GET /routes/list
  → user picks a route
GET /routes/{route_id}
  → user picks a direction/trip
GET /stops/{shape_id}
  → user picks a stop
GET /eta/{route_id}/{shape_id}/{stop_id}
  → live ETA shown, auto-refreshes every 5 min
```

---

## ▶️ Quick Start

### 🐳 Using Docker (Recommended)

```bash
docker-compose up --build
```

- **Backend:** [http://localhost:8000](http://localhost:8000)
- **Frontend:** [http://localhost:80](http://localhost:80)

