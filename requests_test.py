import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time
import logging
from webdriver_manager.chrome import ChromeDriverManager

# Set up logging
logging.basicConfig(level=logging.INFO)

def get_cookies_via_selenium(url):
    """
    Use Selenium to retrieve fresh cookies from the website.
    """
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Use webdriver-manager to automatically download the correct ChromeDriver
    service = Service(ChromeDriverManager().install())  # Automatically installs and sets up ChromeDriver

    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # Navigate to the website
        driver.get(url)
        
        # Wait for a few seconds for the page to load
        time.sleep(5)  # Adjust as necessary, but it's better to wait for specific elements if needed
        
        # Retrieve cookies
        cookies = driver.get_cookies()
        
        # Ensure the browser quits
        driver.quit()
        
        # Format cookies for use in requests
        cookie_string = "; ".join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
        logging.info("Cookies retrieved successfully.")
        return cookie_string
    except Exception as e:
        driver.quit()
        logging.error(f"Error retrieving cookies: {e}")
        return None


def make_request(url, headers, output_file):
    """
    Make a GET request to the given URL with the provided headers,
    and save the JSON response to the specified output file.
    """
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        
        # Parse JSON response
        data = response.json()
        
        # Save to JSON file
        with open(output_file, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        
        logging.info(f"Response saved to {output_file}")
    except requests.exceptions.RequestException as e:
        logging.error(f"An error occurred while making the request: {e}")


def get_headers(cookie, trip_id):
    """
    Generate headers dynamically based on trip_id and cookies.
    """
    return {
        "accept": "application/json, text/plain, */*",
        "accept-encoding": "gzip, deflate, br, zstd",
        "accept-language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7,es;q=0.6",
        "cache-control": "no-cache",
        "cookie": cookie,
        "pragma": "no-cache",
        "referer": f"https://onibus.info/linhas/{trip_id}",
        "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
    }


def get_route_trips(trip_id, cookie):
    url = f"https://onibus.info/api/routetrips/{trip_id}"
    headers = get_headers(cookie, trip_id)
    output_file = f"route_trips_{trip_id}.json"
    make_request(url, headers, output_file)


def get_shape_stops(trip_id, trip_direction, cookie):
    url = f"https://onibus.info/api/shapestops/{trip_id}-{trip_direction}"
    headers = get_headers(cookie, trip_id)
    output_file = f"shape_stops_{trip_id}-{trip_direction}.json"
    make_request(url, headers, output_file)


def get_shape(trip_id, trip_direction, cookie):
    url = f"https://onibus.info/api/stoptimes/shape/{trip_id}-{trip_direction}"
    headers = get_headers(cookie, trip_id)
    output_file = f"stoptimes_{trip_id}-{trip_direction}.json"
    make_request(url, headers, output_file)

# Example usage
if __name__ == "__main__":
    site_url = "https://onibus.info"
    cookie = get_cookies_via_selenium(site_url)

    if cookie:
        # Example calls to the functions using the retrieved cookies
        get_route_trips("0800", cookie)
        get_shape_stops("0800", "0", cookie)
        get_shape("0800", "0", cookie)
    else:
        logging.error("Failed to retrieve cookies. Cannot make further requests.")
