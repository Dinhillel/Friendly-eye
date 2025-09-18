import requests
import threading
import time
import re
from app.config import GOOGLE_MAPS_API_KEY

# --------------------------
# פונקציות עיקריות
# --------------------------

def get_nearby_places(lat, lon, place_type="restaurant", radius=500):
    """ מחזירה מקומות סמוכים """
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
    """ מחזירה הוראות מסלול רגיל """
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
    """ מחזירה הוראות אסינכרוניות ב-thread נפרד """
    def task():
        directions = get_directions(origin, destination)
        steps = directions.get("routes", [{}])[0].get("legs", [{}])[0].get("steps", [])
        if not steps:
            print("No steps found for directions.")
            return
        for step in steps:
            instr = step.get("html_instructions", "")
            instr = re.sub('<[^<]+?>', '', instr)  # מסיר HTML
            if tts_callback:
                tts_callback(instr)
            else:
                print(instr)
    thread = threading.Thread(target=task)
    thread.start()
    return thread  # מחזיר את ה-thread כדי שנוכל להצטרף אליו אם רוצים

# --------------------------
# סקריפט בדיקה
# --------------------------

if __name__ == "__main__":
    print("API Key:", GOOGLE_MAPS_API_KEY)

    # בדיקת Nearby Places
    print("\n--- Nearby Places ---")
    places = get_nearby_places(48.8584, 2.2945)  # מגדל אייפל
    results = places.get("results", [])
    if not results:
        print("No nearby places found.")
    else:
        for place in results[:3]:  # מציג 3 מקומות ראשונים
            print("Nearby place:", place.get("name"))

    # בדיקת Directions רגיל
    print("\n--- Directions (regular) ---")
    directions = get_directions("Eiffel Tower, Paris", "Louvre Museum, Paris")
    steps = directions.get("routes", [{}])[0].get("legs", [{}])[0].get("steps", [])
    if not steps:
        print("No directions found.")
    else:
        for step in steps[:5]:  # מציג 5 הוראות ראשונות
            instr = step.get("html_instructions", "")
            instr = re.sub('<[^<]+?>', '', instr)
            print("Step:", instr)

    # בדיקת Directions אסינכרוני
    print("\n--- Directions (async) ---")
    def tts_callback(instr):
        print("Async Step:", instr)

    thread = fetch_directions_async("Eiffel Tower, Paris", "Louvre Museum, Paris", tts_callback)
    
    # מחכה ל-thread להסתיים
    thread.join()
    print("\nAll async directions fetched.")
