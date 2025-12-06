#!/usr/bin/env python3
"""
Roosevelt Transit Lens - Enhanced App with Touch Controller Integration
Web-based transit information display with physical touch sensor support
"""

from flask import Flask, render_template, jsonify
import threading
import time
from datetime import datetime
from data_fetcher import TransitDataFetcher
from touch_controller import TouchController, MockTouchController, TOUCH_AVAILABLE
import config

app = Flask(__name__)

# Global state
transit_data = {
    'overall_status': 'offline',
    'f_train': None,
    'weather': None,
    'timestamp': None
}

current_station_data = None
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

def handle_station_touch(station_info):
    """
    Callback function for when a station is touched
    Updates the display with station-specific data
    """
    global current_station_data
    
    try:
        print(f"\n{'='*60}")
        print(f"[APP] [{datetime.now().strftime('%H:%M:%S')}] TOUCH DETECTED!")
        print(f"[APP] [{datetime.now().strftime('%H:%M:%S')}] Station: {station_info['name']}")
        print(f"[APP] [{datetime.now().strftime('%H:%M:%S')}] Stop ID: {station_info['stop_id']}")
        print(f"[APP] [{datetime.now().strftime('%H:%M:%S')}] Line: {station_info['line']}")
        print(f"{'='*60}")
        
        # Fetch real-time data for this station
        print(f"[APP] [{datetime.now().strftime('%H:%M:%S')}] Fetching real-time data...")
        fetcher = TransitDataFetcher()
        station_data = fetcher.get_station_data(station_info['stop_id'], station_info['line'])
        
        print(f"[APP] [{datetime.now().strftime('%H:%M:%S')}] Updating display...")
        
        # Update current station data
        with data_lock:
            current_station_data = station_data
        
        # Log train information
        trains = station_data.get('next_trains', [])
        if trains:
            print(f"[DISPLAY] [{datetime.now().strftime('%H:%M:%S')}] STATION TOUCHED: {station_info['name']} ({station_info['line']} line)")
            print(f"[DISPLAY] [{datetime.now().strftime('%H:%M:%S')}] Showing {len(trains)} upcoming trains")
            print(f"[DISPLAY] [{datetime.now().strftime('%H:%M:%S')}] No physical display - running in console mode")
            print(f"[DISPLAY] [{datetime.now().strftime('%H:%M:%S')}] Station: {station_info['name']} | Line: {station_info['line']}")
            for i, train in enumerate(trains[:5], 1):
                print(f"[DISPLAY] [{datetime.now().strftime('%H:%M:%S')}]   Train {i}: {train['minutes']}min to {train['direction']}")
        
        print(f"[APP] [{datetime.now().strftime('%H:%M:%S')}] [OK] Successfully updated display for {station_info['name']}")
        
    except Exception as e:
        print(f"[APP] [{datetime.now().strftime('%H:%M:%S')}] [ERROR] Failed to handle touch: {e}")

# Initialize touch controller with callback
if TOUCH_AVAILABLE:
    touch_controller = TouchController(on_touch_callback=handle_station_touch)
else:
    touch_controller = MockTouchController(on_touch_callback=handle_station_touch)

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

@app.route('/api/current_station')
def api_current_station():
    """Get currently selected station data"""
    with data_lock:
        if current_station_data:
            return jsonify(current_station_data)
        else:
            return jsonify({'error': 'No station selected'}), 404

@app.route('/api/station/<stop_id>/<line>')
def get_station_detail(stop_id, line):
    """Get detailed information for a specific station and line"""
    try:
        print(f"[APP] [{datetime.now().strftime('%H:%M:%S')}] API request for station: {stop_id} ({line} line)")
        
        fetcher = TransitDataFetcher()
        station_data = fetcher.get_station_data(stop_id, line)
        
        print(f"[APP] [{datetime.now().strftime('%H:%M:%S')}] Station data retrieved:")
        print(f"[APP]   Name: {station_data.get('name')}")
        print(f"[APP]   Status: {station_data.get('status')}")
        print(f"[APP]   Trains: {len(station_data.get('next_trains', []))}")
        
        # Also update current station data
        with data_lock:
            global current_station_data
            current_station_data = station_data
        
        return jsonify(station_data)
    except Exception as e:
        print(f"[APP] Error fetching station detail: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/simulate_touch/<int:pad_number>')
def simulate_touch(pad_number):
    """Simulate a touch event (for testing without hardware)"""
    try:
        station_info = touch_controller.get_station_info(pad_number)
        
        if not station_info:
            return jsonify({'error': f'Invalid pad number: {pad_number}'}), 400
        
        print(f"\n[API] Simulating touch on pad {pad_number}")
        
        # Trigger the touch callback
        handle_station_touch(station_info)
        
        return jsonify({
            'success': True,
            'station': station_info['name'],
            'pad': pad_number
        })
        
    except Exception as e:
        print(f"[API] Error simulating touch: {e}")
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

if __name__ == '__main__':
    print("\n" + "="*60)
    print("Roosevelt Transit Lens - Enhanced App")
    print("="*60)
    print(f"Touch Controller: {'Hardware MPR121' if TOUCH_AVAILABLE else 'Mock/Simulation'}")
    print(f"Starting server at http://{config.FLASK_CONFIG['host']}:{config.FLASK_CONFIG['port']}")
    print("Press Ctrl+C to stop")
    print("="*60 + "\n")
    
    # Give the data thread a moment to fetch initial data
    print("Fetching initial transit data...")
    time.sleep(2)
    
    try:
        app.run(
            host=config.FLASK_CONFIG['host'],
            port=config.FLASK_CONFIG['port'],
            debug=config.FLASK_CONFIG['debug']
        )
    finally:
        print("\nShutting down touch controller...")
        touch_controller.shutdown()