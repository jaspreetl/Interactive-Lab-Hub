# config.py
"""
Configuration file for Roosevelt Transit Lens
Store API keys, update intervals, and GPIO pin assignments
"""
from dotenv import load_dotenv
import os
from pathlib import Path

# Load .env from the same directory as this file (if present)
_env_path = Path(__file__).parent / '.env'
if _env_path.exists():
    load_dotenv(dotenv_path=_env_path)
else:
    # fallback to default loader which looks at current working dir
    load_dotenv()

def _clean(v: str | None) -> str:
    if not v:
        return ''
    v = v.strip()
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        return v[1:-1]
    return v

# API Configuration
MTA_API_KEY = _clean(os.getenv("MTA_API_KEY"))
OPENWEATHER_API_KEY = _clean(os.getenv("OPENWEATHER_API_KEY"))
if not MTA_API_KEY:
    raise ValueError("Missing MTA_API_KEY in .env")
if not OPENWEATHER_API_KEY:
    raise ValueError("Missing OPENWEATHER_API_KEY in .env")

# MTA GTFS-Realtime Feed URLs
# These feeds cover all the lines we need
MTA_FEEDS = {
    'bdfm': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm',  # B, D, F, M lines
    'ace': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace',    # A, C, E lines
    'nqrw': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-nqrw',  # N, Q, R, W lines
    '123456s': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs',    # 1, 2, 3, 4, 5, 6, S lines
    'jz': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-jz',      # J, Z lines
    'g': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-g',        # G line
    'l': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-l',        # L line
}

# Station IDs for the 12 key stations
STATION_IDS = {
    'F09': {'name': 'Roosevelt Island', 'lines': ['F']},
    'F11': {'name': 'Lexington Av/63 St', 'lines': ['F', 'Q']},
    'F08': {'name': '21 St-Queensbridge', 'lines': ['F']},
    'R20': {'name': 'Lexington Av/59 St', 'lines': ['N', 'R', 'W', '4', '5', '6']},
    'G08': {'name': 'Queens Plaza', 'lines': ['E', 'M', 'R']},
    'G06': {'name': 'Court Sq-23 St', 'lines': ['E', 'M', 'G']},
    '902': {'name': 'Times Sq-42 St', 'lines': ['1', '2', '3', '7', 'N', 'Q', 'R', 'W', 'S']},
    'D16': {'name': '34 St-Herald Sq', 'lines': ['B', 'D', 'F', 'M', 'N', 'Q', 'R', 'W']},
    '631': {'name': 'Grand Central-42 St', 'lines': ['4', '5', '6', '7', 'S']},
    '635': {'name': 'Union Sq-14 St', 'lines': ['4', '5', '6', 'L', 'N', 'Q', 'R', 'W']},
    'M22': {'name': 'Canal St', 'lines': ['J', 'Z', 'N', 'Q', 'R', 'W', '6']},
    'A38': {'name': 'WTC/Fulton St', 'lines': ['A', 'C', 'E', '2', '3', '4', '5', 'J', 'Z', 'R', 'W']},
}

# Map lines to feed URLs
LINE_TO_FEED = {
    'F': 'bdfm', 'B': 'bdfm', 'D': 'bdfm', 'M': 'bdfm',
    'A': 'ace', 'C': 'ace', 'E': 'ace',
    'N': 'nqrw', 'Q': 'nqrw', 'R': 'nqrw', 'W': 'nqrw',
    '1': '123456s', '2': '123456s', '3': '123456s', 
    '4': '123456s', '5': '123456s', '6': '123456s', 'S': '123456s', '7': '123456s',
    'J': 'jz', 'Z': 'jz',
    'G': 'g',
    'L': 'l',
}

# NYC Ferry API
FERRY_API_URL = 'https://data.cityofnewyork.us/resource/7jtt-s6ch.json'

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
    'num_pixels': 12,   # 12 LED NeoPixel ring
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

# # config.py for version 1
# """
# Configuration file for Roosevelt Transit Lens
# Store API keys, update intervals, and GPIO pin assignments
# """

# # API Configuration
# MTA_API_KEY = 
# OPENWEATHER_API_KEY = 
# # MTA GTFS-Realtime Feed URLs
# MTA_FEEDS = {
#     'f_train': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-bdfm',
#     'ace': 'https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace'
# }

# # Roosevelt Island Station ID (F line)
# ROOSEVELT_STATION_ID = 'F09'  # Northbound and southbound

# # NYC Ferry API
# FERRY_API_URL = 'https://data.cityofnewyork.us/resource/7jtt-s6ch.json'

# # Roosevelt Island Tram (manual schedule - no real-time API available)
# TRAM_SCHEDULE = {
#     'frequency_minutes': 7.5,  # Every 7.5 minutes during peak
#     'operating_hours': {'start': '06:00', 'end': '02:00'}
# }

# # Weather API Configuration
# WEATHER_LOCATION = {
#     'lat': 40.7614,  # Roosevelt Island coordinates
#     'lon': -73.9509
# }

# # Update Intervals (in seconds)
# UPDATE_INTERVALS = {
#     'transit': 30,      # Update transit data every 30 seconds
#     'weather': 300,     # Update weather every 5 minutes
#     'ferry': 60         # Update ferry every minute
# }

# # GPIO Pin Assignments (for Raspberry Pi)
# GPIO_PINS = {
#     'neopixel': 18,     # GPIO 18 (PWM capable)
#     'pir_sensor': 23,   # GPIO 23 (optional motion sensor)
# }

# # LED Configuration
# LED_CONFIG = {
#     'num_pixels': 12,   # 12 LED NeoPixel ring
#     'brightness': 0.7,  # 70% brightness (0.0 to 1.0)
#     'colors': {
#         'normal': (0, 255, 0),      # Green
#         'delays': (255, 215, 0),     # Yellow/Gold
#         'problems': (255, 0, 0),     # Red
#         'offline': (128, 128, 128)   # Gray
#     }
# }

# # Flask Configuration
# FLASK_CONFIG = {
#     'host': '0.0.0.0',  # Listen on all interfaces
#     'port': 5000,
#     'debug': False
# }

# # Status Thresholds
# DELAY_THRESHOLDS = {
#     'minor': 5,   # 5+ minutes = yellow
#     'major': 10   # 10+ minutes = red
# }