import requests
import threading
from app.config import GOOGLE_MAPS_API_KEY
from google_maps import fetch_directions_async

def get_nearby_places(lat, lon, place_type="restaurant", radius=500):
    url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    params = {
        "location": f"{lat},{lon}",
        "radius": radius,
        "type": place_type,
        "key": GOOGLE_MAPS_API_KEY
    }
    try:
        r = requests.get(url, params=params, timeout=5)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        print(f"Error fetching nearby places: {e}")
        return {}

def get_directions(origin, destination, mode="walking"):
    url = "https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "mode": mode,
        "key": GOOGLE_MAPS_API_KEY
    }
    try:
        r = requests.get(url, params=params, timeout=5)
        r.raise_for_status()
        return r.json()
    except requests.RequestException as e:
        print(f"Error fetching directions: {e}")
        return {}

def fetch_directions_async(origin, destination, tts_callback=None):
    """
    אפשר להריץ את הקריאה ל-Directions בלי לחסום את הלולאה הראשית.
    tts_callback: פונקציה שתקבל את ההוראות ותקריא למשתמש.
    """
    def task():
        directions = get_directions(origin, destination)
        steps = directions.get("routes", [{}])[0].get("legs", [{}])[0].get("steps", [])
        instructions = [step.get("html_instructions", "") for step in steps]
        if tts_callback:
            for instr in instructions:
                tts_callback(instr)
        else:
            for instr in instructions:
                print(instr)
    threading.Thread(target=task).start()
