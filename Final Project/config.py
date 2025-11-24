# config.py
"""
Configuration file for Roosevelt Transit Lens
Store API keys, update intervals, and GPIO pin assignments
"""

# API Configuration
# Load secrets from environment. If you keep a `.env` file in the same
# directory as this config, python-dotenv will be used to load it.
import os
from pathlib import Path

try:
    # optional dependency: python-dotenv
    from dotenv import load_dotenv
    _env_path = Path(__file__).parent / '.env'
    if _env_path.exists():
        load_dotenv(dotenv_path=_env_path)
except Exception:
    # If python-dotenv isn't installed, we'll still try to read from the
    # real environment variables via os.environ.
    pass

# Environment values may be quoted in the `.env` file; strip quotes if present.
def _clean(v: str | None) -> str:
    if not v:
        return ''
    v = v.strip()
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        return v[1:-1]
    return v

MTA_API_KEY = _clean(os.getenv('MTA_API_KEY'))
OPENWEATHER_API_KEY = _clean(os.getenv('OPENWEATHER_API_KEY'))

# NYC Ferry API
FERRY_API_URL = _clean(os.getenv('FERRY_API_URL'))

# MTA GTFS-Realtime Feed URLs
MTA_FEEDS = {
    'f_train': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm',
    'ace': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace'
}

# Roosevelt Island Station ID (F line)
ROOSEVELT_STATION_ID = 'F09'  # Northbound and southbound

# Roosevelt Island Tram (manual schedule - no real-time API available)
TRAM_SCHEDULE = {
    'frequency_minutes': 7.5,  # Every 7.5 minutes during peak
    'operating_hours': {'start': '06:00', 'end': '02:00'}
}

# Weather API Configuration
WEATHER_LOCATION = {
    'lat': 40.7614,  # Roosevelt Island coordinates
    'lon': -73.9509
}

# Update Intervals (in seconds)
UPDATE_INTERVALS = {
    'transit': 30,      # Update transit data every 30 seconds
    'weather': 300,     # Update weather every 5 minutes
    'ferry': 60         # Update ferry every minute
}

# GPIO Pin Assignments (for Raspberry Pi)
GPIO_PINS = {
    'neopixel': 18,     # GPIO 18 (PWM capable)
    'pir_sensor': 23,   # GPIO 23 (optional motion sensor)
}

# LED Configuration
LED_CONFIG = {
    'num_pixels': 24,   # 24 LED NeoPixel ring
    'brightness': 0.7,  # 70% brightness (0.0 to 1.0)
    'colors': {
        'normal': (0, 255, 0),      # Green
        'delays': (255, 215, 0),     # Yellow/Gold
        'problems': (255, 0, 0),     # Red
        'offline': (128, 128, 128)   # Gray
    }
}

# Flask Configuration
FLASK_CONFIG = {
    'host': '0.0.0.0',  # Listen on all interfaces
    'port': 5000,
    'debug': True
}

# Status Thresholds
DELAY_THRESHOLDS = {
    'minor': 5,   # 5+ minutes = yellow
    'major': 10   # 10+ minutes = red
}