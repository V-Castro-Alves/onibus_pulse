# Onibus Pulse - System Documentation (Backend)

The **Onibus Pulse Backend** is a FastAPI-based service designed to provide real-time bus tracking data for the **Onibus Pulse** Flutter application.

## System Architecture

The backend consists of:
1.  **FastAPI Application (`main.py`)**: Exposes REST endpoints for the Flutter frontend.
2.  **Scraper (`scraper.py`)**: Handles communication with `onibus.info`. Uses Selenium for session cookie acquisition to bypass Cloudflare protection.
3.  **Real-time ETA Logic**: Dynamically calculates the Estimated Time of Arrival (ETA) by merging scheduled arrival data with real-time trip delays.

## API Endpoints (Current Implementation)

| Endpoint | Method | Parameters | Description |
| :--- | :--- | :--- | :--- |
| `/routes/{route_id}` | GET | `route_id` (e.g., `0800`) | Returns all directions (shapes) available for a specific route. |
| `/stops/{shape_id}` | GET | `shape_id` (e.g., `0800-0`) | Lists all stops associated with a specific shape (direction). |
| `/eta/{route_id}/{shape_id}/{stop_id}` | GET | `route_id`, `shape_id`, `stop_id` | Returns real-time ETA information for a specific stop on a given route. |

## Scraper Details

- **Base URL:** `https://onibus.info`
- **Cookie & User-Agent Management:** Managed by the `OnibusScraper` class in `scraper.py`. If a request returns a 403 or 401 error, the scraper automatically uses Selenium in headless mode to refresh the session cookies.
- **Data Fetching:** Primarily relies on the `requests` library for performance, only falling back to Selenium for session management.

## Real-time ETA Calculation

The backend calculates the real-time ETA for a specific stop:
- **Scheduled Arrival Time:** Fetched from `stoptimes/shape/{shape_id}`.
- **Trip Delay:** Fetched from `stoptrips/-{route_id}`.
- **Formula:** `ETA = Scheduled Time + Current Delay`.

## Dependencies

- `fastapi` & `uvicorn`: Web framework and server.
- `requests`: HTTP client for data scraping.
- `selenium` & `webdriver-manager`: Automated session management for cookie retrieval.
- `pydantic`: Data validation and serialization for API responses.
