#!/usr/bin/env python3
"""
Roosevelt Transit Lens - Enhanced App
Web-based transit information display without LED controller
"""

from flask import Flask, render_template, jsonify
import threading
import time
from datetime import datetime
from data_fetcher import TransitDataFetcher
import config

app = Flask(__name__)

# Global state
transit_data = {
    'overall_status': 'offline',
    'f_train': None,
    'weather': None,
    'timestamp': None
}

data_lock = threading.Lock()

def fetch_transit_data():
    """Background thread to fetch transit data periodically"""
    global transit_data
    
    fetcher = TransitDataFetcher()
    
    while True:
        try:
            print(f"[APP] [{datetime.now().strftime('%H:%M:%S')}] Fetching transit data...")
            
            # Fetch all data
            data = fetcher.get_all_transit_data()
            
            # Update global state
            with data_lock:
                transit_data = data
            
            print(f"[APP] [{datetime.now().strftime('%H:%M:%S')}] Data updated successfully")
            
        except Exception as e:
            print(f"[APP] Error fetching data: {e}")
        
        # Wait before next update
        time.sleep(config.UPDATE_INTERVALS['transit'])

# Start background data fetching
data_thread = threading.Thread(target=fetch_transit_data, daemon=True)
data_thread.start()

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/api/status')
def api_status():
    """Get current transit status"""
    with data_lock:
        return jsonify(transit_data)

@app.route('/api/station/<stop_id>/<line>')
def get_station_detail(stop_id, line):
    """Get detailed information for a specific station and line"""
    try:
        print(f"[APP] [{datetime.now().strftime('%H:%M:%S')}] Fetching station: {stop_id} ({line} line)")
        
        fetcher = TransitDataFetcher()
        station_data = fetcher.get_station_data(stop_id, line)
        
        print(f"[APP] [{datetime.now().strftime('%H:%M:%S')}] Station data retrieved:")
        print(f"[APP]   Name: {station_data.get('name')}")
        print(f"[APP]   Status: {station_data.get('status')}")
        print(f"[APP]   Trains: {len(station_data.get('next_trains', []))}")
        
        return jsonify(station_data)
    except Exception as e:
        print(f"[APP] Error fetching station detail: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/refresh')
def api_refresh():
    """Force refresh all data"""
    try:
        print(f"[APP] [{datetime.now().strftime('%H:%M:%S')}] Force refresh requested")
        
        fetcher = TransitDataFetcher()
        data = fetcher.get_all_transit_data()
        
        with data_lock:
            global transit_data
            transit_data = data
        
        return jsonify({'success': True, 'data': data})
    except Exception as e:
        print(f"[APP] Error refreshing: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/touch/<stop_id>/<line>')
def api_touch(stop_id, line):
    """Handle station touch event (for hardware integration)"""
    try:
        print(f"\n{'='*60}")
        print(f"[APP] [{datetime.now().strftime('%H:%M:%S')}] TOUCH DETECTED!")
        
        # Get station info
        station_info = config.STATION_IDS.get(stop_id, {})
        station_name = station_info.get('name', 'Unknown')
        
        print(f"[APP] [{datetime.now().strftime('%H:%M:%S')}] Station: {station_name}")
        print(f"[APP] [{datetime.now().strftime('%H:%M:%S')}] Stop ID: {stop_id}")
        print(f"[APP] [{datetime.now().strftime('%H:%M:%S')}] Line: {line}")
        print(f"{'='*60}")
        
        # Fetch station data
        fetcher = TransitDataFetcher()
        station_data = fetcher.get_station_data(stop_id, line)
        
        print(f"[APP] [{datetime.now().strftime('%H:%M:%S')}] Data fetched - Status: {station_data.get('status')}")
        
        # Log train arrivals
        trains = station_data.get('next_trains', [])
        if trains:
            print(f"[APP] [{datetime.now().strftime('%H:%M:%S')}] Upcoming trains:")
            for i, train in enumerate(trains[:5], 1):
                print(f"[APP]   Train {i}: {train['minutes']}min to {train['direction']}")
        else:
            print(f"[APP] [{datetime.now().strftime('%H:%M:%S')}] No upcoming trains")
        
        return jsonify({
            'success': True,
            'station': station_name,
            'data': station_data
        })
        
    except Exception as e:
        print(f"[APP] Error handling touch: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Roosevelt Transit Lens - Enhanced App")
    print("="*60)
    print(f"Starting server at http://{config.FLASK_CONFIG['host']}:{config.FLASK_CONFIG['port']}")
    print("Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    # Give the data thread a moment to fetch initial data
    print("Fetching initial transit data...")
    time.sleep(2)
    
    app.run(
        host=config.FLASK_CONFIG['host'],
        port=config.FLASK_CONFIG['port'],
        debug=config.FLASK_CONFIG['debug']
    )