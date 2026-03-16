# Onibus Pulse - Backend (FastAPI)

This repository contains the backend for the **Onibus Pulse** project. It is responsible for scraping real-time bus data from `onibus.info` and providing a clean REST API for the Flutter frontend.

## 🚀 Project Overview

- **Technology Stack:** FastAPI (Python 3.10+), Requests, Selenium (for cookie bypass).
- **Core Functionality:** 
  - Route discovery.
  - Stop listing.
  - Real-time ETA calculation.
- **Frontend:** A separate Flutter repository (planned).

## 🛠 Guidelines for Development

- **Maintain Scraper Integrity:** The `OnibusScraper` in `scraper.py` is the heart of the project. Be careful when modifying it to avoid triggering anti-bot protections.
- **FastAPI Standards:** Use Pydantic models for request/response validation.
- **Error Handling:** Ensure the API returns meaningful HTTP status codes and error messages, especially when the upstream scraper fails.
- **Concurrency:** FastAPI's `async` capabilities should be leveraged where appropriate, although the current scraper is synchronous (Requests-based).

## 📂 Key Files

- `scraper.py`: Core logic for interacting with `onibus.info`.
- `main.py`: FastAPI application entry point.
- `requirements.txt`: Project dependencies.
- `onibus.info.har`: Reference for API calls (for debugging).
