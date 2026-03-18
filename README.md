# 🚏 Onibus Pulse

A monorepo for the **Onibus Pulse** project, featuring a FastAPI-based backend that scrapes `onibus.info` and a Flutter-based mobile application.

---

## 🏗 Architecture

- **Backend (`/onibus_pulse_backend`):** FastAPI (Python) - The data engine that provides a clean REST API.
- **Frontend (`/onibus_pulse_frontend`):** Flutter (Mobile/Web/Desktop) - The user interface for real-time bus tracking.
- **Data Source:** Scraped from `onibus.info` (with Cloudflare bypass via Selenium).

---

## ✨ Features (MVP)

- **Route Discovery:** Search for bus routes by ID or name.
- **Stop Listing:** Get all stops for a specific route and direction (shape).
- **Real-time ETA:** Calculate accurate bus arrival times by combining scheduled times with live trip delays.
- **Cross-Platform:** Mobile application built with Flutter.

---

## 🛠 Tech Stack

### Backend
- **FastAPI:** Modern, high-performance web framework.
- **Requests:** For standard API communication.
- **Selenium:** To handle Cloudflare challenges and refresh session cookies.
- **Uvicorn:** ASGI server for development and production.

### Frontend
- **Flutter:** UI toolkit for building natively compiled applications.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Flutter SDK
- Docker & Docker Compose (optional, for containerized execution)

### Installation & Development

#### Backend
1. Navigate to the backend directory:
   ```bash
   cd onibus_pulse_backend
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

#### Frontend
1. Navigate to the frontend directory:
   ```bash
   cd onibus_pulse_frontend
   ```
2. Install dependencies:
   ```bash
   flutter pub get
   ```
3. Run the app:
   ```bash
   flutter run
   ```

### Running with Docker

From the root directory:
```bash
docker-compose up --build
```

---

## ⚠ Disclaimer

This project is an independent wrapper built around publicly accessible data from https://onibus.info. It is not affiliated with or endorsed by the original service.

---

## 📜 License

MIT License
