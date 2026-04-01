from fastapi.testclient import TestClient
from unittest.mock import patch
from main import app

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "Welcome to Onibus Pulse API",
        "docs": "/docs",
        "status": "active",
    }


@patch("main.onibus_scraper")
def test_get_all_grouped_routes(mock_scraper):
    mock_scraper.get_all_routes.return_value = [
        {
            "station_name": "Station A",
            "routes": [
                {
                    "route_id": "1",
                    "route_long_name": "Route 1",
                    "station_name": "Station A",
                    "service_id": ["S1"],
                }
            ],
        }
    ]
    response = client.get("/routes")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["station_name"] == "Station A"


@patch("main.onibus_scraper")
def test_get_flat_routes(mock_scraper):
    mock_scraper.get_all_routes.return_value = [
        {
            "station_name": "Station A",
            "routes": [
                {
                    "route_id": "1",
                    "route_long_name": "Route 1",
                    "station_name": "Station A",
                    "service_id": ["S1"],
                }
            ],
        },
        {
            "station_name": "Station B",
            "routes": [
                {
                    "route_id": "1",
                    "route_long_name": "Route 1",
                    "station_name": "Station B",
                    "service_id": ["S1"],
                }
            ],
        },
    ]
    response = client.get("/routes/list")
    assert response.status_code == 200
    # Should deduplicate by route_id
    assert len(response.json()) == 1


@patch("main.onibus_scraper")
def test_get_routes(mock_scraper):
    mock_scraper.get_route_trips.return_value = [
        {"trip_headsign": "Downtown", "shape_id": "SH1", "direction_id": 0}
    ]
    response = client.get("/routes/1")
    assert response.status_code == 200
    assert response.json() == [
        {"trip_headsign": "Downtown", "shape_id": "SH1", "direction_id": 0}
    ]


@patch("main.onibus_scraper")
def test_get_stops(mock_scraper):
    mock_scraper.get_shape_stops.return_value = [
        {
            "stop_id": "ST1",
            "stop_name": "Main St",
            "stop_order": 1,
            "stop_lat": 10.0,
            "stop_lon": 20.0,
        }
    ]
    response = client.get("/stops/SH1")
    assert response.status_code == 200
    assert response.json() == [
        {
            "stop_id": "ST1",
            "stop_name": "Main St",
            "stop_order": 1,
            "lat": 10.0,
            "lon": 20.0,
        }
    ]


@patch("main.onibus_scraper")
def test_get_eta(mock_scraper):
    mock_scraper.get_stop_times.return_value = [
        {"stop_id": "ST1", "times": [{"trip_id": "TR1", "arrival_time": "12:00:00"}]}
    ]
    mock_scraper.get_realtime_trips.return_value = [
        {
            "shape_id": "SH1",
            "trip_status": "LIVE",
            "trip_id": "TR1",
            "trip_delay": 60,
            "vehicle_prefix": "BUS1",
        }
    ]
    response = client.get("/eta/1/SH1/ST1")
    assert response.status_code == 200
    # We just want to ensure it completes and returns a list.
    assert isinstance(response.json(), list)
