import time
import sys
from datetime import datetime, timedelta
from scraper import OnibusScraper

def list_route_trips(scraper, route_id):
    print(f"\nFetching directions for route {route_id}...")
    trips = scraper.get_route_trips(route_id)
    if not trips:
        print("No directions found for this route.")
        return None

    print("\nAvailable Directions:")
    for i, trip in enumerate(trips):
        print(f"[{i}] {trip['trip_headsign']} (Shape: {trip['shape_id']})")
    
    while True:
        choice = input("\nSelect a direction index (or 'b' to go back, 'q' to quit): ").strip().lower()
        if choice == 'b':
            return None
        if choice == 'q':
            sys.exit(0)
        try:
            idx = int(choice)
            if 0 <= idx < len(trips):
                return trips[idx]
            else:
                print(f"Invalid index. Please choose between 0 and {len(trips)-1}.")
        except ValueError:
            print("Invalid input. Please enter a number, 'b', or 'q'.")

def list_shape_stops(scraper, shape_id):
    print(f"\nFetching stops for shape {shape_id}...")
    stops = scraper.get_shape_stops(shape_id)
    if not stops:
        print("No stops found for this shape.")
        return None

    print("\nAvailable Stops:")
    for i, stop in enumerate(stops):
        print(f"[{i}] {stop['stop_id']}: {stop['stop_name']} (Order: {stop['stop_order']})")
    
    while True:
        choice = input("\nSelect a stop index (or 'b' to go back, 'q' to quit): ").strip().lower()
        if choice == 'b':
            return None
        if choice == 'q':
            sys.exit(0)
        try:
            idx = int(choice)
            if 0 <= idx < len(stops):
                return stops[idx]
            else:
                print(f"Invalid index. Please choose between 0 and {len(stops)-1}.")
        except ValueError:
            print("Invalid input. Please enter a number, 'b', or 'q'.")

def track_eta(scraper, route_id, shape_id, stop_id, stop_name):
    print(f"\nTarget Stop: {stop_name}")
    
    # Get scheduled stop times
    print("Fetching scheduled stop times...")
    stop_times = scraper.get_stop_times(shape_id)
    if not stop_times:
        print("Could not fetch scheduled stop times.")
        return
    
    target_stop_times = next((s for s in stop_times if s['stop_id'] == stop_id), None)
    if not target_stop_times:
        print(f"No schedule found for stop {stop_id}.")
        return

    print("\nStarting real-time tracking (Ctrl+C to stop and return to menu)...")
    try:
        while True:
            realtime_data = scraper.get_realtime_trips(route_id)
            if not realtime_data:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] Could not fetch real-time data. Retrying in 10s...")
                time.sleep(10)
                continue
            
            # Filter vehicles for this shape
            vehicles = [v for v in realtime_data if v.get('shape_id') == shape_id and v.get('trip_status') == 'LIVE']
            
            if not vehicles:
                print(f"[{datetime.now().strftime('%H:%M:%S')}] No live vehicles found for this shape.")
            else:
                print(f"\n--- Update at {datetime.now().strftime('%H:%M:%S')} ---")
                found_eta = False
                for v in vehicles:
                    trip_id = v['trip_id']
                    delay = v['trip_delay']  # in seconds
                    
                    # Find scheduled time for this specific trip
                    sched_time_str = next((t['arrival_time'] for t in target_stop_times['times'] if t['trip_id'] == trip_id), None)
                    
                    if sched_time_str:
                        found_eta = True
                        # Parse scheduled time
                        sched_time = datetime.strptime(sched_time_str, "%H:%M:%S")
                        now = datetime.now()
                        sched_dt = now.replace(hour=sched_time.hour, minute=sched_time.minute, second=sched_time.second)
                        
                        # Handle midnight crossing
                        if sched_dt < now - timedelta(hours=12):
                            sched_dt += timedelta(days=1)
                        
                        eta_dt = sched_dt + timedelta(seconds=delay)
                        remaining = (eta_dt - now).total_seconds()
                        
                        status = "Arrived" if remaining < 0 else f"{int(remaining // 60)}m {int(remaining % 60)}s"
                        
                        print(f"Vehicle {v['vehicle_prefix']}:")
                        print(f"  Scheduled: {sched_time_str}")
                        print(f"  Delay: {delay}s ({delay//60}m {delay%60}s)")
                        print(f"  ETA: {eta_dt.strftime('%H:%M:%S')} ({status} remaining)")
                
                if not found_eta:
                    print("No vehicle's current trip matches the schedule for this stop.")
            
            time.sleep(15)
    except KeyboardInterrupt:
        print("\nTracking stopped. Returning to menu...")

def main_loop():
    print("Welcome to Onibus Pulse - Real-time Bus Tracking")
    scraper = OnibusScraper()

    while True:
        route_id = input("\nEnter Route ID (e.g., 0800) or 'q' to quit: ").strip().lower()
        if route_id == 'q':
            break
        if not route_id:
            continue
        
        # Step 1: Select Direction
        selected_trip = list_route_trips(scraper, route_id)
        if not selected_trip:
            continue
        
        shape_id = selected_trip['shape_id']
        
        # Step 2: Select Stop
        selected_stop = list_shape_stops(scraper, shape_id)
        if not selected_stop:
            continue
        
        stop_id = selected_stop['stop_id']
        stop_name = selected_stop['stop_name']
        
        # Step 3: Track
        track_eta(scraper, route_id, shape_id, stop_id, stop_name)

if __name__ == "__main__":
    try:
        main_loop()
    except EOFError:
        print("\nExiting...")
    except Exception as e:
        print(f"An error occurred: {e}")
