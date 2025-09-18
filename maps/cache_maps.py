import json
import os
from app.config import GOOGLE_MAPS_API_KEY
import requests
import threading
from bs4 import BeautifulSoup

CACHE_FILE = "directions_cache.json"

#load cache if exists
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, "r", encoding="utf-8") as f:
        directions_cache = json.load(f)
else:
    directions_cache = {}

def save_cache():
    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(directions_cache, f, ensure_ascii=False, indent=2)

def get_directions(origin, destination, mode="walking"):
    key = f"{origin}_{destination}_{mode}"
    
    #test if having cache 
    if key in directions_cache:
        return directions_cache[key]
    
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
        result = r.json()
        # save to cache
        directions_cache[key] = result
        save_cache()
        return result
    except requests.RequestException as e:
        print(f"Error fetching directions: {e}")
        return {}

def fetch_directions_async(origin, destination, tts_callback=None):
    def task():
        directions = get_directions(origin, destination)
        steps = directions.get("routes", [{}])[0].get("legs", [{}])[0].get("steps", [])
        seen = set()
        for step in steps:
            html_instr = step.get("html_instructions", "")
            instr = BeautifulSoup(html_instr, "html.parser").get_text()
            if instr not in seen:
                seen.add(instr)
                if tts_callback:
                    tts_callback(instr)
                else:
                    print(f"Step: {instr}")
    threading.Thread(target=task).start()
