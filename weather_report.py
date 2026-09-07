"""
Software Weather Satellite
---------------------------
Fetches current weather data from Open-Meteo (no API key required)
and pushes a plain-text report to your phone via ntfy.sh (no API key required).

Configure via environment variables (set these as GitHub Actions secrets,
or export them locally before running):

    LATITUDE       - e.g. "22.5726"   (Kolkata)
    LONGITUDE      - e.g. "88.3639"   (Kolkata)
    NTFY_TOPIC     - your unique, private topic name, e.g. "sumit-weather-report-47"
    LOCATION_NAME  - optional friendly label, e.g. "Kolkata"
"""

import os
import sys
from datetime import datetime

import requests

OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"
NTFY_BASE_URL = "https://ntfy.sh"


def get_config():
    lat = os.environ.get("LATITUDE", "22.5726")
    lon = os.environ.get("LONGITUDE", "88.3639")
    topic = os.environ.get("NTFY_TOPIC")
    location_name = os.environ.get("LOCATION_NAME", "Your Location")

    if not topic:
        print("ERROR: NTFY_TOPIC environment variable is not set.", file=sys.stderr)
        sys.exit(1)

    return lat, lon, topic, location_name


def fetch_weather(lat, lon):
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "apparent_temperature",
            "precipitation",
            "weather_code",
            "wind_speed_10m",
            "wind_direction_10m",
            "cloud_cover",
        ],
        "daily": [
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_probability_max",
        ],
        "timezone": "auto",
        "forecast_days": 1,
    }
    response = requests.get(OPEN_METEO_URL, params=params, timeout=15)
    response.raise_for_status()
    return response.json()


WEATHER_CODES = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Fog", 48: "Freezing fog",
    51: "Light drizzle", 53: "Moderate drizzle", 55: "Dense drizzle",
    61: "Slight rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Slight snow", 73: "Moderate snow", 75: "Heavy snow",
    80: "Slight rain showers", 81: "Moderate rain showers", 82: "Violent rain showers",
    95: "Thunderstorm", 96: "Thunderstorm with hail", 99: "Thunderstorm with heavy hail",
}


def build_report(data, location_name):
    current = data["current"]
    daily = data["daily"]

    condition = WEATHER_CODES.get(current["weather_code"], "Unknown")
    now = datetime.now().strftime("%Y-%m-%d %H:%M")

    report_lines = [
        f"Weather Report - {location_name}",
        f"Time: {now}",
        "",
        f"Condition: {condition}",
        f"Temperature: {current['temperature_2m']}°C (feels like {current['apparent_temperature']}°C)",
        f"Humidity: {current['relative_humidity_2m']}%",
        f"Cloud cover: {current['cloud_cover']}%",
        f"Precipitation: {current['precipitation']} mm",
        f"Wind: {current['wind_speed_10m']} km/h, direction {current['wind_direction_10m']}°",
        "",
        f"Today's high/low: {daily['temperature_2m_max'][0]}°C / {daily['temperature_2m_min'][0]}°C",
        f"Chance of rain today: {daily['precipitation_probability_max'][0]}%",
    ]
    return "\n".join(report_lines)


def send_ntfy(topic, message, title="Weather Satellite Report"):
    url = f"{NTFY_BASE_URL}/{topic}"
    response = requests.post(
        url,
        data=message.encode("utf-8"),
        headers={
            "Title": title,
            "Priority": "default",
            "Tags": "cloud",
        },
        timeout=15,
    )
    response.raise_for_status()


def main():
    lat, lon, topic, location_name = get_config()
    data = fetch_weather(lat, lon)
    report = build_report(data, location_name)
    print(report)  # Also visible in GitHub Actions logs
    send_ntfy(topic, report)
    print("\nReport sent to ntfy topic:", topic)


if __name__ == "__main__":
    main()
