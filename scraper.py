import requests
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class OnibusScraper:
    BASE_URL = "https://onibus.info"
    API_URL = f"{BASE_URL}/api"

    def __init__(self):
        self.session = requests.Session()
        self.cookie_string = None
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"

    def refresh_cookies(self):
        print("Refreshing cookies via Selenium...")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        try:
            driver.get(self.BASE_URL)
            time.sleep(5)  # Wait for page to load/CF challenge
            cookies = driver.get_cookies()
            driver.quit()
            
            self.cookie_string = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
            self.session.headers.update({
                "cookie": self.cookie_string,
                "user-agent": self.user_agent,
                "accept": "application/json, text/plain, */*"
            })
            return True
        except Exception as e:
            print(f"Error refreshing cookies: {e}")
            if 'driver' in locals():
                driver.quit()
            return False

    def _get_headers(self, referer=None):
        headers = {
            "accept": "application/json, text/plain, */*",
            "user-agent": self.user_agent
        }
        if self.cookie_string:
            headers["cookie"] = self.cookie_string
        if referer:
            headers["referer"] = referer
        else:
            headers["referer"] = self.BASE_URL
        return headers

    def make_request(self, endpoint, referer=None):
        url = f"{self.API_URL}/{endpoint}"
        headers = self._get_headers(referer)
        try:
            response = self.session.get(url, headers=headers)
            if response.status_code == 403 or response.status_code == 401:
                print("Access denied. Refreshing cookies...")
                if self.refresh_cookies():
                    headers = self._get_headers(referer)
                    response = self.session.get(url, headers=headers)
            
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
            return None

    def get_route_trips(self, route_id):
        return self.make_request(f"routetrips/{route_id}", referer=f"{self.BASE_URL}/linhas/{route_id}")

    def get_shape_stops(self, shape_id):
        return self.make_request(f"shapestops/{shape_id}")

    def get_stop_times(self, shape_id):
        # The endpoint in app.py for stoptimes is /api/stoptimes/shape/{trip_id}-{direction_id}
        # But looking at the files, it seems it's /api/stoptimes/shape/{shape_id}
        return self.make_request(f"stoptimes/shape/{shape_id}")

    def get_realtime_trips(self, route_id):
        # The endpoint is /api/stoptrips/-{route_id}
        return self.make_request(f"stoptrips/-{route_id}", referer=f"{self.BASE_URL}/linhas/{route_id}")

    def get_all_routes(self):
        """Fetch all routes grouped by station."""
        return self.make_request("routes/group", referer=f"{self.BASE_URL}/linhas")
