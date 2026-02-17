"""
weather_service.py
Fetches weather data using the free Open-Meteo API (no API key needed).
Uses only Python standard library modules.
"""

import urllib.request
import urllib.parse
import json


# WMO Weather interpretation codes -> human-readable descriptions
WMO_CODES = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Light freezing drizzle",
    57: "Dense freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Light freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snowfall",
    73: "Moderate snowfall",
    75: "Heavy snowfall",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail",
}


def _geocode(city_name):
    """
    Convert a city name to latitude/longitude using the Open-Meteo geocoding API.
    Returns (location_dict, None) on success or (None, error_string) on failure.
    """
    params = urllib.parse.urlencode({
        "name": city_name,
        "count": 1,
        "language": "en",
        "format": "json",
    })
    url = f"https://geocoding-api.open-meteo.com/v1/search?{params}"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            raw = response.read().decode("utf-8")
            data = json.loads(raw)
    except urllib.error.URLError as e:
        return None, f"Network error: {e.reason}"
    except Exception as e:
        return None, f"Geocoding failed: {e}"

    results = data.get("results")
    if not results or len(results) == 0:
        return None, f"City '{city_name}' not found. Please check the spelling."

    loc = results[0]
    return {
        "name": loc.get("name", city_name),
        "country": loc.get("country", "Unknown"),
        "lat": loc["latitude"],
        "lon": loc["longitude"],
    }, None


def get_weather(city_name):
    """
    Fetch current weather for the given city name.

    Returns a dict with keys:
        city, country, temperature, windspeed, condition
    On error, returns a dict with a single 'error' key.

    No API key is required (uses the free Open-Meteo API).
    """
    # Step 1: Resolve city name to coordinates
    location, error = _geocode(city_name)
    if error:
        return {"error": error}

    # Step 2: Fetch current weather from Open-Meteo
    params = urllib.parse.urlencode({
        "latitude": location["lat"],
        "longitude": location["lon"],
        "current_weather": "true",
    })
    url = f"https://api.open-meteo.com/v1/forecast?{params}"

    try:
        req = urllib.request.Request(url)
        with urllib.request.urlopen(req, timeout=10) as response:
            raw = response.read().decode("utf-8")
            data = json.loads(raw)
    except urllib.error.URLError as e:
        return {"error": f"Network error: {e.reason}"}
    except Exception as e:
        return {"error": f"Could not fetch weather: {e}"}

    # Step 3: Parse the response
    current = data.get("current_weather")
    if current is None:
        return {"error": "Unexpected API response — no weather data found."}

    weather_code = current.get("weathercode", -1)
    condition = WMO_CODES.get(weather_code, "Unknown")

    return {
        "city": location["name"],
        "country": location["country"],
        "temperature": current.get("temperature", "N/A"),
        "windspeed": current.get("windspeed", "N/A"),
        "condition": condition,
    }
