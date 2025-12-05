# data_fetcher.py
"""
Fetches real-time transit data from MTA, NYC Ferry, and Weather APIs
Includes mock data mode for development/testing
"""

import requests
from datetime import datetime, timedelta
from google.transit import gtfs_realtime_pb2
import config

# Set to True to use mock data (for testing without API keys)
USE_MOCK_DATA = True

class TransitDataFetcher:
    def __init__(self):
        self.last_update = {}
        self.cached_data = {
            'f_train': None,
            'tram': None,
            'ferry': None,
            'weather': None
        }
    
    def get_station_data(self, stop_id, line):
        """Fetch data for any station by stop_id and line"""
        
        # Handle special cases
        if stop_id == 'TRAM':
            return self.get_tram_status()
        elif stop_id == 'FERRY':
            return self.get_ferry_status()
        
        # For mock mode, generate realistic data
        if USE_MOCK_DATA:
            print(f"Using mock data for {stop_id} ({line} line)")
            return self._get_mock_station_data(stop_id, line)
        
        try:
            # Determine which feed to use
            feed_key = config.LINE_TO_FEED.get(line, 'bdfm')
            feed_url = config.MTA_FEEDS.get(feed_key)
            
            if not feed_url:
                return self._get_mock_station_data(stop_id, line)
            
            headers = {'x-api-key': config.MTA_API_KEY}
            response = requests.get(feed_url, headers=headers, timeout=10)
            
            if response.status_code != 200:
                print(f"MTA API error for {line}: {response.status_code}")
                return self._get_mock_station_data(stop_id, line)
            
            # Parse GTFS-Realtime data
            feed = gtfs_realtime_pb2.FeedMessage()
            feed.ParseFromString(response.content)
            
            trains = []
            alerts = []
            
            for entity in feed.entity:
                # Process trip updates for this station
                if entity.HasField('trip_update'):
                    trip = entity.trip_update
                    
                    # Check if trip is for our line
                    if trip.trip.route_id != line:
                        continue
                    
                    for stop_update in trip.stop_time_update:
                        # Match station (stop_id may have N/S suffix)
                        if stop_update.stop_id.startswith(stop_id):
                            arrival_time = stop_update.arrival.time
                            arrival_dt = datetime.fromtimestamp(arrival_time)
                            minutes_away = int((arrival_dt - datetime.now()).total_seconds() / 60)
                            
                            if minutes_away >= 0:
                                # Determine direction
                                direction = 'Manhattan' if 'N' in stop_update.stop_id else 'Queens'
                                if stop_id in ['631', '635', 'D16', 'A38', 'M22']:
                                    direction = 'Downtown' if 'S' in stop_update.stop_id else 'Uptown'
                                
                                trains.append({
                                    'minutes': minutes_away,
                                    'direction': direction,
                                    'route': line
                                })
                
                # Process service alerts
                if entity.HasField('alert'):
                    alert = entity.alert
                    for informed_entity in alert.informed_entity:
                        if informed_entity.route_id == line:
                            alerts.append({
                                'header': alert.header_text.translation[0].text,
                                'description': alert.description_text.translation[0].text
                            })
            
            # Sort trains by arrival time
            trains.sort(key=lambda x: x['minutes'])
            
            # Determine status
            status = self._determine_train_status(trains, alerts)
            
            station_info = config.STATION_IDS.get(stop_id, {})
            
            return {
                'name': station_info.get('name', 'Unknown'),
                'line': line,
                'stop_id': stop_id,
                'status': status,
                'next_trains': trains[:5],
                'alerts': alerts,
                'updated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            print(f"Error fetching station data for {stop_id}: {e}")
            return self._get_mock_station_data(stop_id, line)
    
    def _get_mock_station_data(self, stop_id, line):
        """Generate mock station data for testing"""
        import random
        
        station_info = config.STATION_IDS.get(stop_id, {'name': 'Unknown'})
        
        # Generate 3-5 trains
        num_trains = random.randint(3, 5)
        trains = []
        
        for i in range(num_trains):
            minutes = random.randint(2, 20) + (i * 5)
            direction = random.choice(['Manhattan', 'Queens', 'Uptown', 'Downtown'])
            trains.append({
                'minutes': minutes,
                'direction': direction,
                'route': line
            })
        
        trains.sort(key=lambda x: x['minutes'])
        
        # Randomly add delays
        status = 'normal' if random.random() > 0.3 else 'delays'
        
        return {
            'name': station_info.get('name', 'Unknown'),
            'line': line,
            'stop_id': stop_id,
            'status': status,
            'next_trains': trains,
            'alerts': [],
            'updated_at': datetime.now().isoformat()
        }
        """Fetch F train real-time data from MTA GTFS-RT feed"""
        
        # Mock data mode for development
        if USE_MOCK_DATA or not config.MTA_API_KEY or config.MTA_API_KEY == "YOUR_MTA_API_KEY_HERE":
            print("Using mock F train data")
            return self._get_mock_train_data()
        
        try:
            headers = {'x-api-key': config.MTA_API_KEY}
            response = requests.get(config.MTA_FEEDS['f_train'], headers=headers, timeout=10)
            
            if response.status_code != 200:
                print(f"MTA API error: {response.status_code}")
                return self._get_mock_train_data()
            
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
                    for informed_entity in alert.informed_entity:
                        if informed_entity.route_id == 'F':
                            alerts.append({
                                'header': alert.header_text.translation[0].text,
                                'description': alert.description_text.translation[0].text
                            })
            
            trains.sort(key=lambda x: x['minutes'])
            status = self._determine_train_status(trains, alerts)
            
            train_data = {
                'status': status,
                'next_trains': trains[:5],
                'alerts': alerts,
                'updated_at': datetime.now().isoformat()
            }
            
            self.cached_data['f_train'] = train_data
            return train_data
            
        except Exception as e:
            print(f"Error fetching F train data: {e}")
            return self._get_mock_train_data()
    
    def get_f_train_status(self):
        """Fetch F train real-time data (Roosevelt Island line)"""
        # Convenience method: fetch F train data from Roosevelt Island station
        return self.get_station_data('F09', 'F')
    
    def _get_mock_train_data(self):
        """Return mock train data for development"""
        import random
        
        # Generate realistic mock data
        trains = [
            {'minutes': 3, 'direction': 'Manhattan'},
            {'minutes': 8, 'direction': 'Manhattan'},
            {'minutes': 12, 'direction': 'Queens'},
            {'minutes': 15, 'direction': 'Manhattan'},
            {'minutes': 20, 'direction': 'Queens'},
        ]
        
        # Randomly add a delay sometimes
        if random.random() > 0.8:
            trains[0]['minutes'] = 12
            status = 'delays'
        else:
            status = 'normal'
        
        return {
            'status': status,
            'next_trains': trains,
            'alerts': [],
            'updated_at': datetime.now().isoformat()
        }
    
    def _determine_train_status(self, trains, alerts):
        """Determine overall train status based on delays and alerts"""
        if alerts:
            return 'problems'
        
        if not trains:
            return 'offline'
        
        if trains[0]['minutes'] > config.DELAY_THRESHOLDS['major']:
            return 'delays'
        elif trains[0]['minutes'] > config.DELAY_THRESHOLDS['minor']:
            return 'delays'
        
        return 'normal'
    
    def get_tram_status(self):
        """Get Roosevelt Island Tram status"""
        try:
            now = datetime.now()
            current_time = now.time()
            
            # Parse operating hours (Tram operates 6 AM to 2 AM next day)
            start_time = datetime.strptime(config.TRAM_SCHEDULE['operating_hours']['start'], '%H:%M').time()
            end_time = datetime.strptime(config.TRAM_SCHEDULE['operating_hours']['end'], '%H:%M').time()
            
            # Check if tram is operating
            # Special case: if end_time is after midnight (like 2 AM), it wraps to next day
            if end_time < start_time:
                # Operates past midnight (e.g., 6 AM to 2 AM)
                is_operating = current_time >= start_time or current_time <= end_time
            else:
                # Normal same-day operation
                is_operating = start_time <= current_time <= end_time
            
            print(f"[DEBUG] Tram check - Current time: {current_time.strftime('%H:%M')}, Operating hours: {start_time.strftime('%H:%M')}-{end_time.strftime('%H:%M')}, Is operating: {is_operating}")
            
            if is_operating:
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
            # Fallback to operating status
            return {
                'status': 'normal',
                'next_departure': 5,
                'frequency': 'Every 7.5 min',
                'updated_at': datetime.now().isoformat()
            }
    
    def get_ferry_status(self):
        """Fetch NYC Ferry schedule data"""
        
        # For now, always show ferry as operating during daytime hours
        now = datetime.now()
        current_hour = now.hour
        
        # Ferry typically operates 7 AM to 10 PM
        is_operating = 7 <= current_hour <= 22
        
        print(f"[DEBUG] Ferry check - Current hour: {current_hour}, Is operating: {is_operating}")
        
        if USE_MOCK_DATA:
            print("Using mock ferry data")
            if is_operating:
                return {
                    'status': 'normal',
                    'next_arrival': 12,
                    'route': 'Astoria Route',
                    'updated_at': datetime.now().isoformat()
                }
            else:
                return {
                    'status': 'offline',
                    'next_arrival': None,
                    'route': 'Not operating',
                    'updated_at': datetime.now().isoformat()
                }
        
        try:
            response = requests.get(config.FERRY_API_URL, timeout=10)
            
            if response.status_code != 200:
                return self._get_fallback_ferry_data()
            
            ferries = response.json()
            roosevelt_ferries = [f for f in ferries if 'Roosevelt' in f.get('stop_name', '')]
            
            if roosevelt_ferries:
                next_ferry = roosevelt_ferries[0]
                ferry_data = {
                    'status': 'normal',
                    'next_arrival': 12,
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
        return {
            'status': 'normal',
            'next_arrival': 12,
            'route': 'Astoria Route',
            'updated_at': datetime.now().isoformat()
        }
    
    def get_weather_data(self):
        """Fetch weather data from OpenWeather API"""
        
        # Mock data for development
        if USE_MOCK_DATA or not config.OPENWEATHER_API_KEY or config.OPENWEATHER_API_KEY == "YOUR_OPENWEATHER_API_KEY_HERE":
            print("Using mock weather data")
            return self._get_mock_weather_data()
        
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
                print(f"Weather API error: {response.status_code}")
                return self._get_mock_weather_data()
            
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
            return self._get_mock_weather_data()
    
    def _get_mock_weather_data(self):
        """Return mock weather data for development"""
        import random
        
        conditions = [
            ('Clear', 'Clear Sky', 'sun', 68),
            ('Clouds', 'Partly Cloudy', 'cloud', 65),
            ('Rain', 'Light Rain', 'rain', 58),
        ]
        
        condition = random.choice(conditions)
        
        return {
            'temp': condition[3],
            'feels_like': condition[3] - 2,
            'condition': condition[0],
            'description': condition[1],
            'wind_speed': random.randint(5, 12),
            'humidity': random.randint(50, 70),
            'icon': '01d',
            'updated_at': datetime.now().isoformat()
        }
    
    def get_all_transit_data(self):
        """Fetch all transit data and return combined status"""
        print("Fetching all transit data...")
        
        # Get F train status from Roosevelt Island station
        f_train = self.get_station_data('F09', 'F')
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
        
        result = {
            'overall_status': overall,
            'f_train': f_train,
            'tram': tram,
            'ferry': ferry,
            'weather': weather,
            'timestamp': datetime.now().isoformat()
        }
        
        print(f"Data fetched successfully at {datetime.now().strftime('%H:%M:%S')}")
        return result
