from fastapi import FastAPI, HTTPException
from typing import List
from pydantic import BaseModel
from datetime import datetime, timedelta
from scraper import OnibusScraper

app = FastAPI(title="Onibus Pulse API")
onibus_scraper = OnibusScraper()


@app.get("/")
def read_root():
    return {
        "message": "Welcome to Onibus Pulse API",
        "docs": "/docs",
        "status": "active",
    }


# --- Pydantic Models ---


class RouteTrip(BaseModel):
    trip_headsign: str
    shape_id: str
    direction_id: int


class RouteListItem(BaseModel):
    route_id: str
    route_long_name: str
    station_name: str
    service_id: List[str]


class StationRoutes(BaseModel):
    station_name: str
    routes: List[RouteListItem]


class Stop(BaseModel):
    stop_id: str
    stop_name: str
    stop_order: int
    lat: float
    lon: float


class ETAInfo(BaseModel):
    vehicle_prefix: str
    scheduled_arrival: str
    delay_seconds: int
    eta_time: str
    remaining_minutes: int
    status: str


# --- API Endpoints ---


@app.get("/routes", response_model=List[StationRoutes])
def get_all_grouped_routes():
    """Get all routes grouped by station."""
    data = onibus_scraper.get_all_routes()
    if not data:
        raise HTTPException(status_code=500, detail="Failed to fetch routes")
    return data


@app.get("/routes/list", response_model=List[RouteListItem])
def get_flat_routes():
    """Get a flat, deduplicated list of all routes."""
    data = onibus_scraper.get_all_routes()
    if not data:
        raise HTTPException(status_code=500, detail="Failed to fetch routes")

    flat_list = []
    seen_routes = set()

    for station in data:
        for route in station["routes"]:
            if route["route_id"] not in seen_routes:
                flat_list.append(route)
                seen_routes.add(route["route_id"])

    return sorted(flat_list, key=lambda x: x["route_id"])


@app.get("/routes/{route_id}", response_model=List[RouteTrip])
def get_routes(route_id: str):
    """Get available directions (shapes) for a specific route."""
    data = onibus_scraper.get_route_trips(route_id)
    if not data:
        raise HTTPException(status_code=404, detail="Route not found")

    return [
        RouteTrip(
            trip_headsign=t["trip_headsign"],
            shape_id=t["shape_id"],
            direction_id=t["direction_id"],
        )
        for t in data
    ]


@app.get("/stops/{shape_id}", response_model=List[Stop])
def get_stops(shape_id: str):
    """List all stops for a specific direction (shape)."""
    data = onibus_scraper.get_shape_stops(shape_id)
    if not data:
        raise HTTPException(status_code=404, detail="Shape not found")

    return [
        Stop(
            stop_id=s["stop_id"],
            stop_name=s["stop_name"],
            stop_order=s["stop_order"],
            lat=s["stop_lat"],
            lon=s["stop_lon"],
        )
        for s in data
    ]


@app.get("/eta/{route_id}/{shape_id}/{stop_id}", response_model=List[ETAInfo])
def get_eta(route_id: str, shape_id: str, stop_id: str):
    """Get real-time ETA for a specific stop."""
    # 1. Get scheduled times for this stop
    stop_times_data = onibus_scraper.get_stop_times(shape_id)
    if not stop_times_data:
        raise HTTPException(
            status_code=404, detail="Scheduled times not found for this shape"
        )

    target_stop = next((s for s in stop_times_data if s["stop_id"] == stop_id), None)
    if not target_stop:
        raise HTTPException(status_code=404, detail="Stop not found in this shape")

    # 2. Get real-time trip data
    realtime_data = onibus_scraper.get_realtime_trips(route_id)
    if not realtime_data:
        # If no real-time data, we can't calculate ETA (upstream might be down or no buses)
        return []

    # 3. Filter vehicles for this shape
    vehicles = [
        v
        for v in realtime_data
        if v.get("shape_id") == shape_id and v.get("trip_status") == "LIVE"
    ]

    results = []
    now = datetime.now()

    for v in vehicles:
        trip_id = v["trip_id"]
        delay = v["trip_delay"]  # in seconds

        # Find scheduled time for this specific trip
        sched_time_str = next(
            (
                t["arrival_time"]
                for t in target_stop["times"]
                if t["trip_id"] == trip_id
            ),
            None,
        )

        if sched_time_str:
            # Parse scheduled time
            try:
                sched_time = datetime.strptime(sched_time_str, "%H:%M:%S")
                sched_dt = now.replace(
                    hour=sched_time.hour,
                    minute=sched_time.minute,
                    second=sched_time.second,
                )

                # Handle midnight crossing
                if sched_dt < now - timedelta(hours=12):
                    sched_dt += timedelta(days=1)
                elif sched_dt > now + timedelta(hours=12):
                    sched_dt -= timedelta(days=1)

                eta_dt = sched_dt + timedelta(seconds=delay)
                remaining_seconds = (eta_dt - now).total_seconds()

                status = (
                    "Arrived"
                    if remaining_seconds < 0
                    else f"{int(remaining_seconds // 60)}m"
                )

                results.append(
                    ETAInfo(
                        vehicle_prefix=v["vehicle_prefix"],
                        scheduled_arrival=sched_time_str,
                        delay_seconds=delay,
                        eta_time=eta_dt.strftime("%H:%M:%S"),
                        remaining_minutes=int(max(0, remaining_seconds // 60)),
                        status=status,
                    )
                )
            except Exception as e:
                print(f"Error parsing time: {e}")
                continue

    return results


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)  # nosec B104
