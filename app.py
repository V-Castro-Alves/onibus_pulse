from flask import Flask, render_template, request, jsonify, session
import requests
from flask_caching import Cache
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# Initialize cache
app.config['CACHE_TYPE'] = 'simple'  # Use simple in-memory cache for demo
cache = Cache(app)

# Function to fetch cookies using Selenium
def get_cookies_via_selenium(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        driver.get(url)
        time.sleep(5)  # Wait for page to load
        cookies = driver.get_cookies()
        driver.quit()
        
        cookie_string = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
        return cookie_string
    except Exception as e:
        driver.quit()
        return None

# Helper function to make a request to the API
def make_request(url, headers):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"error": f"An error occurred: {e}"}

# Get the headers required for requests
def get_headers(cookie, trip_id):
    return {
        "accept": "application/json, text/plain, */*",
        "cookie": cookie,
        "referer": f"https://onibus.info/linhas/{trip_id}",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }

@app.route('/')
def index():
    # Fetch cookie if not in session
    if 'cookie' not in session:
        cookie = get_cookies_via_selenium("https://onibus.info")
        if not cookie:
            return jsonify({"error": "Failed to retrieve cookies"}), 500
        session['cookie'] = cookie

    # Render the initial template with any session data
    trip_id = session.get('trip_id')
    direction_id = session.get('direction_id')
    stop_id = session.get('stop_id')

    return render_template('index.html', trip_id=trip_id, direction_id=direction_id, stop_id=stop_id)

@app.route('/get_trip', methods=['POST'])
def get_trip():
    trip_id = request.form.get('trip_id')
    cookie = session.get('cookie')

    if not trip_id:
        return jsonify({"error": "Trip ID is required"}), 400

    session['trip_id'] = trip_id  # Update session with new trip_id

    url = f"https://onibus.info/api/routetrips/{trip_id}"
    headers = get_headers(cookie, trip_id)
    route_data = make_request(url, headers)

    if route_data and isinstance(route_data, list) and len(route_data) > 0:
        return jsonify({"route_data": route_data})

    return jsonify({"error": "No route data found"}), 500

@app.route('/get_shape_stops', methods=['POST'])
def get_shape_stops():
    direction_id = request.form.get('direction_id')
    trip_id = request.form.get('trip_id')
    cookie = session.get('cookie')

    if not direction_id or not trip_id:
        return jsonify({"error": "Invalid trip or direction ID"}), 400

    session['direction_id'] = direction_id  # Update session with new direction_id

    shape_id = f"{trip_id}-{direction_id}"
    url = f"https://onibus.info/api/shapestops/{shape_id}"
    headers = get_headers(cookie, trip_id)

    shape_stops_data = make_request(url, headers)
    
    if isinstance(shape_stops_data, list) and shape_stops_data:
        return jsonify({"shape_stops": shape_stops_data})

    return jsonify({"error": "No shape stops found"}), 500

@app.route('/get_stop_times', methods=['POST'])
def get_stop_times():
    stop_id = request.form.get('stop_id')
    trip_id = request.form.get('trip_id')
    direction_id = request.form.get('direction_id')

    if not stop_id or not trip_id or not direction_id:
        return jsonify({"error": "Stop ID, Trip ID, and Direction ID are required"}), 400

    session['stop_id'] = stop_id  # Update session with new stop_id

    cookie = session.get('cookie')

    url = f"https://onibus.info/api/stoptimes/shape/{trip_id}-{direction_id}"
    headers = get_headers(cookie, trip_id)

    stop_times_data = make_request(url, headers)

    for stop in stop_times_data:
        if stop["stop_id"] == stop_id:
            first_arrival_time = stop["times"][0]["arrival_time"]
            return jsonify({"first_arrival_time": first_arrival_time})

    return jsonify({"error": "No matching stop found"}), 400

if __name__ == "__main__":
    app.run(debug=True)
