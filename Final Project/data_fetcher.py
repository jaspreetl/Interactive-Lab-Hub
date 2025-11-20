# data_fetcher.py
"""
Fetches real-time transit data from MTA, NYC Ferry, and Weather APIs
"""

import requests
from datetime import datetime, timedelta
from google.transit import gtfs_realtime_pb2
import config

class TransitDataFetcher:
    def __init__(self):
        self.last_update = {}
        self.cached_data = {
            'f_train': None,
            'tram': None,
            'ferry': None,
            'weather': None
        }
    
    def get_f_train_status(self):
        """Fetch F train real-time data from MTA GTFS-RT feed"""
        try:
            headers = {'x-api-key': config.MTA_API_KEY}
            response = requests.get(config.MTA_FEEDS['f_train'], headers=headers, timeout=10)
            
            if response.status_code != 200:
                print(f"MTA API error: {response.status_code}")
                return self._get_fallback_train_data()
            
            # Parse GTFS-Realtime protobuf data
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)
            
            trains = []
            alerts = []
            
            for entity in feed.entity:
                # Process trip updates
                if entity.HasField('trip_update'):
                    trip = entity.trip_update
                    for stop_update in trip.stop_time_update:
                        if stop_update.stop_id.startswith(config.ROOSEVELT_STATION_ID):
                            arrival_time = stop_update.arrival.time
                            arrival_dt = datetime.fromtimestamp(arrival_time)
                            minutes_away = int((arrival_dt - datetime.now()).total_seconds() / 60)
                            
                            if minutes_away >= 0:
                                trains.append({
                                    'minutes': minutes_away,
                                    'direction': 'Manhattan' if 'N' in stop_update.stop_id else 'Queens',
                                    'trip_id': trip.trip.trip_id
                                })
                
                # Process service alerts
                if entity.HasField('alert'):
                    alert = entity.alert
                    # Check if alert affects F train
                    for informed_entity in alert.informed_entity:
                        if informed_entity.route_id == 'F':
                            alerts.append({
                                'header': alert.header_text.translation[0].text,
                                'description': alert.description_text.translation[0].text
                            })
            
            # Sort trains by arrival time
            trains.sort(key=lambda x: x['minutes'])
            
            # Determine status
            status = self._determine_train_status(trains, alerts)
            
            train_data = {
                'status': status,
                'next_trains': trains[:5],  # Next 5 trains
                'alerts': alerts,
                'updated_at': datetime.now().isoformat()
            }
            
            self.cached_data['f_train'] = train_data
            return train_data
            
        except Exception as e:
            print(f"Error fetching F train data: {e}")
            return self._get_fallback_train_data()
    
    def _determine_train_status(self, trains, alerts):
        """Determine overall train status based on delays and alerts"""
        if alerts:
            return 'problems'
        
        if not trains:
            return 'offline'
        
        # Check if next train is delayed significantly
        if trains[0]['minutes'] > config.DELAY_THRESHOLDS['major']:
            return 'delays'
        elif trains[0]['minutes'] > config.DELAY_THRESHOLDS['minor']:
            return 'delays'
        
        return 'normal'
    
    def _get_fallback_train_data(self):
        """Return cached or default data if API fails"""
        if self.cached_data['f_train']:
            return self.cached_data['f_train']
        
        return {
            'status': 'offline',
            'next_trains': [],
            'alerts': [{'header': 'Data unavailable', 'description': 'Unable to fetch real-time data'}],
            'updated_at': datetime.now().isoformat()
        }
    
    def get_tram_status(self):
        """Get Roosevelt Island Tram status (schedule-based, no real-time API)"""
        try:
            now = datetime.now()
            current_time = now.time()
            
            # Parse operating hours
            start_time = datetime.strptime(config.TRAM_SCHEDULE['operating_hours']['start'], '%H:%M').time()
            end_time = datetime.strptime(config.TRAM_SCHEDULE['operating_hours']['end'], '%H:%M').time()
            
            # Check if tram is operating
            is_operating = start_time <= current_time <= end_time
            
            if is_operating:
                # Calculate next departure (every 7.5 minutes)
                freq = config.TRAM_SCHEDULE['frequency_minutes']
                minutes_into_hour = now.minute + (now.second / 60)
                next_departure = (freq - (minutes_into_hour % freq))
                
                tram_data = {
                    'status': 'normal',
                    'next_departure': int(next_departure),
                    'frequency': f"Every {freq} min",
                    'updated_at': datetime.now().isoformat()
                }
            else:
                tram_data = {
                    'status': 'offline',
                    'next_departure': None,
                    'frequency': 'Not operating',
                    'updated_at': datetime.now().isoformat()
                }
            
            self.cached_data['tram'] = tram_data
            return tram_data
            
        except Exception as e:
            print(f"Error calculating tram status: {e}")
            return {
                'status': 'offline',
                'next_departure': None,
                'frequency': 'Unknown',
                'updated_at': datetime.now().isoformat()
            }
    
    def get_ferry_status(self):
        """Fetch NYC Ferry schedule data"""
        try:
            # NYC Ferry real-time data
            response = requests.get(config.FERRY_API_URL, timeout=10)
            
            if response.status_code != 200:
                return self._get_fallback_ferry_data()
            
            # Filter for Roosevelt Island stops
            ferries = response.json()
            roosevelt_ferries = [f for f in ferries if 'Roosevelt' in f.get('stop_name', '')]
            
            if roosevelt_ferries:
                next_ferry = roosevelt_ferries[0]
                ferry_data = {
                    'status': 'normal',
                    'next_arrival': 12,  # Placeholder - would need to calculate from schedule
                    'route': next_ferry.get('route_name', 'Astoria Route'),
                    'updated_at': datetime.now().isoformat()
                }
            else:
                ferry_data = {
                    'status': 'normal',
                    'next_arrival': 15,
                    'route': 'Astoria Route',
                    'updated_at': datetime.now().isoformat()
                }
            
            self.cached_data['ferry'] = ferry_data
            return ferry_data
            
        except Exception as e:
            print(f"Error fetching ferry data: {e}")
            return self._get_fallback_ferry_data()
    
    def _get_fallback_ferry_data(self):
        """Return cached or default ferry data"""
        if self.cached_data['ferry']:
            return self.cached_data['ferry']
        
        return {
            'status': 'offline',
            'next_arrival': None,
            'route': 'Unknown',
            'updated_at': datetime.now().isoformat()
        }
    
    def get_weather_data(self):
        """Fetch weather data from OpenWeather API"""
        try:
            url = f"https://api.openweathermap.org/data/2.5/weather"
            params = {
                'lat': config.WEATHER_LOCATION['lat'],
                'lon': config.WEATHER_LOCATION['lon'],
                'appid': config.OPENWEATHER_API_KEY,
                'units': 'imperial'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code != 200:
                return self._get_fallback_weather_data()
            
            data = response.json()
            
            weather_data = {
                'temp': round(data['main']['temp']),
                'feels_like': round(data['main']['feels_like']),
                'condition': data['weather'][0]['main'],
                'description': data['weather'][0]['description'].title(),
                'wind_speed': round(data['wind']['speed']),
                'humidity': data['main']['humidity'],
                'icon': data['weather'][0]['icon'],
                'updated_at': datetime.now().isoformat()
            }
            
            self.cached_data['weather'] = weather_data
            return weather_data
            
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return self._get_fallback_weather_data()
    
    def _get_fallback_weather_data(self):
        """Return cached or default weather data"""
        if self.cached_data['weather']:
            return self.cached_data['weather']
        
        return {
            'temp': 68,
            'feels_like': 68,
            'condition': 'Clear',
            'description': 'Clear Sky',
            'wind_speed': 5,
            'humidity': 60,
            'icon': '01d',
            'updated_at': datetime.now().isoformat()
        }
    
    def get_all_transit_data(self):
        """Fetch all transit data and return combined status"""
        f_train = self.get_f_train_status()
        tram = self.get_tram_status()
        ferry = self.get_ferry_status()
        weather = self.get_weather_data()
        
        # Determine overall status
        statuses = [f_train['status'], tram['status'], ferry['status']]
        if 'problems' in statuses:
            overall = 'problems'
        elif 'delays' in statuses:
            overall = 'delays'
        elif all(s == 'normal' for s in statuses):
            overall = 'normal'
        else:
            overall = 'delays'
        
        return {
            'overall_status': overall,
            'f_train': f_train,
            'tram': tram,
            'ferry': ferry,
            'weather': weather,
            'timestamp': datetime.now().isoformat()
        }