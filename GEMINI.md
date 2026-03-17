# Onibus Pulse - Monorepo

This repository is a monorepo for the **Onibus Pulse** project, containing both the backend and frontend.

## 🚀 Project Overview

- **Backend (`/backend`):** FastAPI (Python 3.10+), Requests, Selenium (for cookie bypass).
- **Frontend (`/frontend`):** Flutter (planned/in-progress).
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

### Frontend (Flutter)
- **State Management:** Use a consistent state management pattern (e.g., Provider, Riverpod, or Bloc).
- **UI/UX:** Focus on a clean, responsive interface for mobile users.
- **API Integration:** Ensure robust handling of API responses and errors.

## 📂 Key Files

- `backend/scraper.py`: Core logic for interacting with `onibus.info`.
- `backend/main.py`: FastAPI application entry point.
- `docker-compose.yml`: Root configuration for running services.
- `backend/har-files/`: Reference for API calls (for debugging).
