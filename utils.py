import sys
import argparse
import logging
import urllib.request
import json
from datetime import datetime, timedelta

# Set up logging with best practices (you might later drive logs into files, etc.)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
from enum import Enum


class WallpaperPath(Enum):
    """Enum containing paths to wallpaper images in media directory"""

    NIGHT = "media/night.png"
    SUNRISE = "media/sunrise.png"
    MORNING = "media/morning.png"
    NOON = "media/noon.png"
    EVENING = "media/evening.png"
    SUNSET = "media/sunset.png"


def get_sun_times(lat: float, lng: float) -> tuple:
    """
    Fetches sunrise and sunset times from the Sunrise–Sunset API.
    The API returns ISO8601 datetime strings in UTC.

    Args:
        lat (float): Latitude.
        lng (float): Longitude.

    Returns:
        tuple: (sunrise_utc, sunset_utc) as timezone-aware datetime objects in UTC.

    Raises:
        Exception: If the API call fails or the response is invalid.
    """
    url = f"https://api.sunrise-sunset.org/json?lat={lat}&lng={lng}&date=today&formatted=0"
    logging.info("Fetching sun times from API: %s", url)

    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            if response.status != 200:
                raise Exception(f"Non-200 response received: {response.status}")
            api_response = json.loads(response.read().decode())
    except Exception as e:
        logging.error("Error calling the sun times API: %s", e)
        raise

    results = api_response.get("results", {})
    if not results:
        raise Exception("Invalid API response: missing 'results'")

    try:
        # Parse the returned ISO8601 times. They are already in UTC.
        sunrise_utc = datetime.fromisoformat(results["sunrise"])
        sunset_utc = datetime.fromisoformat(results["sunset"])
    except Exception as e:
        logging.error("Error parsing sun times: %s", e)
        raise

    logging.info("Sunrise (UTC): %s, Sunset (UTC): %s", sunrise_utc, sunset_utc)
    return sunrise_utc, sunset_utc


def choose_wallpaper(now: datetime, sunrise: datetime, sunset: datetime) -> str:
    """
    Determines the appropriate wallpaper filename based on the current UTC time relative
    to sunrise, solar noon, and sunset.

    Conditions:
      - Before sunrise or after sunset: "night.png"
      - Within 15 minutes of sunrise: "sunrise.png"
      - Within 15 minutes of solar noon (midpoint between sunrise and sunset): "noon.png"
      - Within 15 minutes of sunset: "sunset.png"
      - If between sunrise (outside its window) and solar noon: "morning.png"
      - If between solar noon (outside its window) and sunset: "evening.png"

    Args:
        now (datetime): The current time in UTC.
        sunrise (datetime): Today's sunrise time in UTC.
        sunset (datetime): Today's sunset time in UTC.

    Returns:
        str: The selected wallpaper file name.
    """
    if now < sunrise or now > sunset:
        logging.info("The current UTC time is outside daytime. It's night time.")
        return WallpaperPath.NIGHT.value

    time_window = timedelta(minutes=15)

    # Check if current time is near sunrise
    if abs(now - sunrise) <= time_window:
        logging.info("Current time is within 15 minutes of sunrise.")
        return WallpaperPath.SUNRISE.value

    # Calculate solar noon (midpoint) in UTC.
    solar_noon = sunrise + (sunset - sunrise) / 2
    if abs(now - solar_noon) <= time_window:
        logging.info("Current time is within 15 minutes of solar noon.")
        return WallpaperPath.NOON.value

    # Check if current time is near sunset.
    if abs(now - sunset) <= time_window:
        logging.info("Current time is within 15 minutes of sunset.")
        return WallpaperPath.SUNSET.value

    # Otherwise, decide between morning and evening.
    if now < solar_noon:
        logging.info("Current time is in the morning period.")
        return WallpaperPath.MORNING.value
    else:
        logging.info("Current time is in the evening period.")
        return WallpaperPath.EVENING.value
