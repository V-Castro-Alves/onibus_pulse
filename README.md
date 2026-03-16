# 🚏 Onibus Pulse - Backend

A FastAPI-based backend that scrapes `onibus.info` to provide a clean REST API for real-time bus tracking.

This project serves as the data engine for the **Onibus Pulse** ecosystem, with a separate Flutter frontend in another repository.

---

## 🏗 Architecture

- **Backend:** FastAPI (Python) - *This Repository*
- **Frontend:** Flutter (Mobile/Web/Desktop) - *Separate Repository*
- **Data Source:** Scraped from `onibus.info` (with Cloudflare bypass via Selenium).

---

## ✨ Features (MVP)

- **Route Discovery:** Search for bus routes by ID or name.
- **Stop Listing:** Get all stops for a specific route and direction (shape).
- **Real-time ETA:** Calculate accurate bus arrival times by combining scheduled times with live trip delays.
- **Cookie Bypass:** Automatic session/cookie refresh using Selenium when needed.

---

## 🛠 Tech Stack

- **FastAPI:** Modern, high-performance web framework.
- **Requests:** For standard API communication.
- **Selenium:** To handle Cloudflare challenges and refresh session cookies.
- **Uvicorn:** ASGI server for development and production.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Google Chrome (for Selenium cookie refresh)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/vitor/onibus_pulse.git
   cd onibus_pulse
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # or venv\Scripts\activate on Windows
   pip install -r requirements.txt
   ```

3. Run the API:
   ```bash
   uvicorn main:app --reload
   ```

### API Endpoints (Planned/Current)

- `GET /routes/{route_id}`: Get available directions for a route.
- `GET /stops/{shape_id}`: List all stops for a specific direction.
- `GET /eta/{route_id}/{shape_id}/{stop_id}`: Get real-time ETA for a specific stop.

---

## ⚠ Disclaimer

This project is an independent wrapper built around publicly accessible data from https://onibus.info. It is not affiliated with or endorsed by the original service.

---

## 📜 License

MIT License
