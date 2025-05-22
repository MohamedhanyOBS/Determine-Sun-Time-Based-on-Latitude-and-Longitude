# Wallpaper Selector

This is a simple Python executable program that selects a desktop wallpaper based on the sun's position at a given location (specified by latitude and longitude). It is designed with best practices in mind, including clear logging, error handling, and a maintainable project structure.

## How It Works

1. **Sun Times Retrieval:**  
   The program calls the [Sunrise–Sunset API](https://sunrise-sunset.org/api) to fetch today’s sunrise and sunset times for the specified location. The API returns the times in UTC.

2. **UTC Uniformity:**  
   Instead of using the system’s local timezone, the program uses UTC for all calculations. The current time is obtained using `datetime.now(timezone.utc)`, so whether you run this from Cairo, Riyadh, Washington DC, or anywhere else, the correct period is determined based solely on UTC.

3. **Wallpaper Selection Logic:**  
   - **Night:** If the current UTC time is before sunrise or after sunset.
   - **Sunrise:** If the current UTC time is within 15 minutes of sunrise.
   - **Morning:** If the time is after sunrise (and not near sunrise) and before solar noon.
   - **Noon:** If the time is within 15 minutes of the solar noon (computed as the midpoint between sunrise and sunset).
   - **Sunset:** If the time is within 15 minutes of sunset.
   - **Evening:** If the time is after solar noon (and not near sunset) but before sunset.

## Prerequisites

- Python 3.7 or later.
- Internet access (for API calls).

_No external libraries are required; the solution uses only Python’s standard library._

## How to Run

In a Linux Bash environment, navigate to the project directory and run:

```bash
python main.py <latitude> <longitude>
