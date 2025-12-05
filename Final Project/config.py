# config.py
"""
Configuration file for Roosevelt Transit Lens
Store API keys, update intervals, and GPIO pin assignments
"""

# API Configuration
MTA_API_KEY = "YOUR_MTA_API_KEY_HERE"  # Get from https://api.mta.info/
OPENWEATHER_API_KEY = "YOUR_OPENWEATHER_API_KEY_HERE"  # Get from https://openweathermap.org/api

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
    'F15': {'name': '57 St-7 Av', 'lines': ['F']},
    'G08': {'name': 'Queens Plaza', 'lines': ['E', 'M', 'R']},
    'G06': {'name': 'Court Sq-23 St', 'lines': ['E', 'M', 'G']},
    'E12': {'name': '5 Av/53 St', 'lines': ['E', 'M']},
    '631': {'name': 'Grand Central-42 St', 'lines': ['4', '5', '6', '7', 'S']},
    'R09': {'name': 'Queensboro Plaza', 'lines': ['N', 'W', '7']},
    'E13': {'name': 'Lexington Av/53 St', 'lines': ['E', 'M']},
    '635': {'name': 'Union Sq-14 St', 'lines': ['4', '5', '6', 'L', 'N', 'Q', 'R', 'W']},
    '902': {'name': 'Times Sq-42 St', 'lines': ['1', '2', '3', '7', 'N', 'Q', 'R', 'W', 'S']},
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
    'weather': 300      # Update weather every 5 minutes
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