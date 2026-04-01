# Onibus Pulse

This repository is a monorepo for the **Onibus Pulse** project, containing both the backend and frontend for a real-time bus tracking application.

## 🚀 Project Overview

- **Backend (`/onibus_pulse_backend`):** A FastAPI (Python) API that scrapes and serves data from the `onibus.info` website.
  - **Key Libraries:** FastAPI, Requests, Selenium.
- **Frontend (`/onibus_pulse_frontend`):** A responsive web application built with React and Vite.
  - **Key Libraries:** React (TypeScript), Vite, React Router, Lucide Icons.
- **Core Functionality:** 
  - **Route Discovery:** Search and browse all available bus lines.
  - **Direction & Stop Listing:** View the specific path (directions) for a route and all associated stops.
  - **Real-time ETA Calculation:** Get live arrival time predictions for a specific bus at a specific stop.

## 🏗️ Architecture & Directory Layout

- **`/onibus_pulse_backend`**
  - `main.py`: The core FastAPI application, defining all API endpoints and Pydantic data models.
  - `scraper.py`: Contains the `OnibusScraper` class, responsible for all web scraping and data extraction from `onibus.info`.
  - `requirements.txt`: Lists all Python dependencies.
  - `Dockerfile`: Container definition for the backend service.

- **`/onibus_pulse_frontend`**
  - `src/`: Main React application source code.
    - `screens/`: Contains the main page components (`HomeScreen`, `RouteDetailScreen`, etc.).
    - `components/`: Reusable UI components like `Layout` and `RouteCard`.
    - `App.tsx`: Defines the application's routing structure using `react-router-dom`.
  - `package.json`: Lists all Node.js dependencies and project scripts.
  - `vite.config.ts`: Vite build tool configuration.
  - `Dockerfile`: Container definition for the frontend service.

## 🔄 Data & API Flow

The application follows a logical flow, with each user interaction triggering a specific API call:

1.  **App Start (`HomeScreen.tsx`):** The frontend calls `GET /routes/list` to fetch a flat list of all bus routes, which are then displayed to the user.
2.  **Select a Route (`RouteDetailScreen.tsx`):** When the user selects a route, the app calls `GET /routes/{route_id}` to retrieve the available directions (e.g., "to Downtown", "to Suburb").
3.  **Select a Direction (`StopListScreen.tsx`):** After a direction is chosen, the app calls `GET /stops/{shape_id}` to get an ordered list of all bus stops along that path.
4.  **Select a Stop (`EtaScreen.tsx`):** Finally, selecting a stop triggers a call to `GET /eta/{route_id}/{shape_id}/{stop_id}` to fetch live arrival time data for that stop.
5.  **Live Updates (`EtaScreen.tsx`):** The ETA screen automatically polls the API every **30 seconds** for fresh data. It also provides a manual refresh button.

## 🛠️ Development Guidelines & Implementation Details

### Backend (FastAPI)

-   **Scraper Integrity:** The `OnibusScraper` in `scraper.py` is the project's most critical and fragile component. It uses **Selenium with a headless Chromium** to visit the target site and solve anti-bot challenges (like Cloudflare), saving the resulting cookies. All subsequent API calls made with the `requests` library use these cookies to appear legitimate. Modifications here risk breaking the entire data pipeline.
-   **API Standards:** The API adheres to FastAPI best practices, using Pydantic models for robust request/response validation and automatically generating OpenAPI documentation (`/docs`).
-   **Endpoints:** The primary endpoints are clearly defined in `main.py` and cover routes, stops, and ETAs.

### Frontend (React + Vite)

-   **UI/UX:** The interface is designed for simplicity and speed, inspired by modern transit apps.
    - **Icons:** `lucide-react` is used for a clean and consistent icon set.
    - **State Management:** The UI includes clear loading, error, and empty states to provide user feedback during API calls.
    - **Components:** The code is structured into reusable components (`RouteCard`, `Layout`) and screen-specific views.
-   **API Integration:**
    -   API calls are made using the browser's `fetch` API.
    -   The backend URL is currently **hardcoded** to `http://localhost:8000` in each screen component. For production, this should be moved to an environment variable.
    -   The `EtaScreen` implements a robust refresh mechanism (auto and manual) to provide live data.

## 🧪 Running Locally

The simplest way to run the full stack is using Docker.

### 🐳 Using Docker (Recommended)
```bash
docker-compose up --build
```
-   **Backend API:** `http://localhost:8000`
-   **Frontend App:** `http://localhost:80`
