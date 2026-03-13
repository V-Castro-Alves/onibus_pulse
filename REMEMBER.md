# Onibus Pulse - System Documentation

Onibus Pulse is a real-time bus tracking system that scrapes data from `onibus.info`. It provides information about bus routes, stop locations, schedules, and real-time Estimated Time of Arrival (ETA).

## System Architecture

The system consists of two main components:
1.  **Scraper (`scraper.py`)**: Handles communication with the `onibus.info` API. It includes a cookie refresh mechanism using Selenium to bypass anti-bot protections (like Cloudflare).
2.  **CLI App (`main.py`)**: Provides a user interface to interact with the scraper, allowing users to search for routes, list stops, and track bus ETAs in real-time.

## API Endpoints

All API calls are made to `https://onibus.info/api/`.

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `search` | POST | Searches for routes based on a term. |
| `routetrips/{route_id}` | GET | Returns available shapes and directions for a specific route. |
| `shapestops/{shape_id}` | GET | Lists all stops associated with a specific shape ID. |
| `stoptimes/shape/{shape_id}` | GET | Returns the scheduled arrival times for all stops in a shape. |
| `stoptrips/-{route_id}` | GET | Returns real-time trip data, including vehicle positions and delays. |

### Parameters
- `route_id`: The identifier for a bus route (e.g., `0800`, `0290`).
- `shape_id`: The identifier for a specific direction/variation of a route (e.g., `0800-0`, `0290-1`).

## Real-time ETA Calculation

The system calculates the real-time ETA for a specific stop using the following formula:

**ETA = Scheduled Arrival Time + Trip Delay**

1.  **Scheduled Arrival Time**: Obtained from the `stoptimes/shape/{shape_id}` endpoint.
2.  **Trip Delay**: Obtained from the `stoptrips/-{route_id}` endpoint. It represents the current delay of the vehicle in seconds (can be positive for delays or negative for early arrivals).

## Cookie & Header Management

The `onibus.info` API requires valid session cookies and specific headers to function:
- **Cookies**: Obtained by visiting the base website (`https://onibus.info`) using a headless browser (Selenium).
- **User-Agent**: A standard browser User-Agent must be used.
- **Referer**: Many API endpoints check the `Referer` header. Usually, it should point to the specific route page (e.g., `https://onibus.info/linhas/{route_id}`).

## Dependencies

The project relies on:
- `requests`: For making HTTP calls to the API.
- `selenium` & `webdriver-manager`: For automating cookie retrieval.
- `Interactive Menu`: The `main.py` script now uses a loop-based interactive menu for user input and selection.
