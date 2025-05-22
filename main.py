#!/usr/bin/env python3
"""
wallpaper_selector - Select a wallpaper based on sun position.

Usage (in a Linux Bash environment):
    python main.py <latitude> <longitude>

The program calls a public API to get today's sunrise and sunset times based on the
provided geographic coordinates. It then compares the current local time to these times.
• If the sun is below the horizon, it prints "night.png" to stdout.
• If the current time is within 15 minutes of sunrise, it prints "sunrise.png".
• Otherwise, it prints "morning.png".

Author: Mohamed Hany
"""

import sys
import argparse
import logging
from datetime import datetime, timezone

from utils import get_sun_times, choose_wallpaper

# Set up logging with best practices (you might later drive logs into files, etc.)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)


def main():
    parser = argparse.ArgumentParser(
        description="Select an appropriate wallpaper based on the sun's position (using UTC) for a given location."
    )
    parser.add_argument("latitude", type=float, help="Latitude of the location")
    parser.add_argument("longitude", type=float, help="Longitude of the location")
    args = parser.parse_args()

    # Use UTC for the current time to avoid relying on the system's local timezone.
    now = datetime.now(timezone.utc)
    logging.info("Current UTC time: %s", now)

    try:
        sunrise, sunset = get_sun_times(args.latitude, args.longitude)
    except Exception as e:
        logging.error("Failed to retrieve sun times: %s", e)
        sys.exit(1)

    wallpaper = choose_wallpaper(now, sunrise, sunset)
    # Output the image file name (e.g., morning.png, noon.png, etc.)
    print(wallpaper)


if __name__ == "__main__":
    main()
