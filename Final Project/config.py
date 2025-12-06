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
    'A28': {'name': 'W 4 St-Washington Sq', 'lines': ['A', 'C', 'E', 'B', 'D', 'F', 'M']},
    'D16': {'name': '34 St-Herald Sq', 'lines': ['B', 'D', 'F', 'M', 'N', 'Q', 'R', 'W']},
    'A38': {'name': 'Fulton St', 'lines': ['A', 'C', 'J', 'Z', '2', '3', '4', '5']},
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

# NYC Ferry API
FERRY_API_URL = "https://data.cityofnewyork.us/resource/sqhz-wtqh.json"

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

# MTA Official Line Colors (for display purposes)
MTA_LINE_COLORS = {
    # IRT Broadway-Seventh Avenue Line (Red)
    '1': '#EE352E', '2': '#EE352E', '3': '#EE352E',
    # IRT Lexington Avenue Line (Green)
    '4': '#00933C', '5': '#00933C', '6': '#00933C',
    # IRT Flushing Line (Purple)
    '7': '#B933AD',
    # BMT Canarsie Line (Gray)
    'L': '#A7A9AC',
    # IND Eighth Avenue Line (Blue)
    'A': '#0039A6', 'C': '#0039A6', 'E': '#0039A6',
    # IND Sixth Avenue Line (Orange)
    'B': '#FF6319', 'D': '#FF6319', 'F': '#FF6319', 'M': '#FF6319',
    # IND Crosstown Line (Light Green)
    'G': '#6CBE45',
    # BMT Broadway Line (Yellow)
    'N': '#FCCC0A', 'Q': '#FCCC0A', 'R': '#FCCC0A', 'W': '#FCCC0A',
    # BMT Nassau Street Line (Brown)
    'J': '#996633', 'Z': '#996633',
    # Shuttles (Gray)
    'S': '#808183'
}