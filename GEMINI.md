# Onibus Pulse - Monorepo

This repository is a monorepo for the **Onibus Pulse** project, containing both the backend and frontend.

## 🚀 Project Overview

- **Backend (`/backend`):** FastAPI (Python 3.10+), Requests, Selenium (for cookie bypass).
- **Frontend (`/frontend`):** Planned/in-progress.
- **Core Functionality:** 
  - Route discovery.
  - Stop listing.
  - Real-time ETA calculation.

## 🛠 Guidelines for Development

### Backend (FastAPI)
- **Maintain Scraper Integrity:** The `OnibusScraper` in `backend/scraper.py` is the heart of the project. Be careful when modifying it to avoid triggering anti-bot protections.
- **FastAPI Standards:** Use Pydantic models for request/response validation.
- **Error Handling:** Ensure the API returns meaningful HTTP status codes and error messages.
- **Concurrency:** Leverage FastAPI's `async` capabilities where appropriate.

### Frontend
- **Status:** Implemented
- **UI/UX:** Implemented a Transit Heartbeat-inspired design with top app bar, search input, grouped route list tiles, cards for trips/stops/ETA, and loading/error states.
- **API Integration:** Implemented robust API service with endpoints:
  - `GET /routes/list`
  - `GET /routes/{route_id}`
  - `GET /stops/{shape_id}`
  - `GET /eta/{route_id}/{shape_id}/{stop_id}`
  - Includes retry, pull-to-refresh, and 5-minute periodic refresh on ETA screen.

## 🏗 Architecture & Directory Layout

- `/onibus_pulse_backend`
  - `main.py`: FastAPI app with routes and Pydantic models.
  - `scraper.py`: `OnibusScraper` performs website calls and transformations.
  - `examples/`: sample JSON responses and HAR files.
- `/onibus_pulse_frontend`
  - `lib/`: contains frontend source code.
  - `test/`: contains frontend tests.

## 🔄 Data/API flow

1. `RoutesScreen` loads route list from `GET /routes/list`.
2. User selects route => `RouteDetailScreen` loads `GET /routes/{route_id}`.
3. User selects trip/direction => `StopsScreen` loads `GET /stops/{shape_id}`.
4. User selects stop => `EtaScreen` loads `GET /eta/{route_id}/{shape_id}/{stop_id}`.
5. `EtaScreen` auto-refreshes every 5 minutes, plus manual pull-to-refresh and button refresh.

## 🧰 Frontend implementation details

- Data mapping and error handling covered in API service.
- UI style:
  - Color palette modeled from reference site: blue/teal app bar, white cards, light background.
  - Search + route grouping for rapid discovery.
  - Status chips (on-time/delay) and card information.
  - Loading states.
  - Error states with retry buttons.

## 🧪 Running locally

Backend
- `cd onibus_pulse_backend`
- `pip install -r requirements.txt`
- `uvicorn main:app --reload --host 0.0.0.0 --port 8000`

Frontend
- `cd onibus_pulse_frontend`

API host configuration
- Android emulator: `http://10.0.2.2:8000`
- iOS simulator/desktop: `http://localhost:8000`

## 📌 Notes

- First implementation is complete; extension points include route favorites, offline caching, and map integration.
- Keep backend scrape logic stable and avoid frequent layout assumptions on source website.

