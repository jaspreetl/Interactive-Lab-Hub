# app_enhanced.py
"""
Enhanced Flask app with interactive touch map support
"""

from flask import Flask, render_template, jsonify
from flask_cors import CORS
from datetime import datetime
import threading
import time

import config
from data_fetcher import TransitDataFetcher

# Import enhanced controllers
try:
    from touch_controller import TouchController, MockTouchController, TOUCH_AVAILABLE
    from enhanced_ambient_controller import EnhancedLEDController, MockEnhancedLEDController, NEOPIXEL_AVAILABLE
    from display_controller import DisplayController, MockDisplayController
    DISPLAY_AVAILABLE = True
except ImportError as e:
    print(f"[WARNING] Import error: {e}")
    # Fallback to original controllers if enhanced not available
    from ambient_controller import AmbientLEDController as EnhancedLEDController, MockLEDController as MockEnhancedLEDController, NEOPIXEL_AVAILABLE
    TOUCH_AVAILABLE = False
    DISPLAY_AVAILABLE = False
    TouchController = None
    MockTouchController = None
    DisplayController = None
    MockDisplayController = None

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Initialize data fetcher
data_fetcher = TransitDataFetcher()

# Global variables
current_data = {}
selected_station = None
data_lock = threading.Lock()

# Initialize display controller first
if DISPLAY_AVAILABLE and DisplayController:
    display_controller = DisplayController(display_type='auto')
elif MockDisplayController:
    display_controller = MockDisplayController()
else:
    display_controller = None

# Initialize LED controller with display reference
if NEOPIXEL_AVAILABLE:
    led_controller = EnhancedLEDController(display_controller=display_controller)
else:
    led_controller = MockEnhancedLEDController(display_controller=display_controller)

# Touch event handler
def on_station_touched(station):
    """Called when a station is touched on the map"""
    global selected_station
    
    print(f"[APP] Station touched: {station['name']}")
    selected_station = station
    
    # Fetch data for this specific station
    try:
        station_data = data_fetcher.get_station_data(station['stop_id'], station['line'])
        
        # Update LED to show station status
        led_controller.show_station_status(station_data)
        
    except Exception as e:
        print(f"[ERROR] Failed to fetch station data: {e}")

# Initialize touch controller
if TOUCH_AVAILABLE and TouchController:
    touch_controller = TouchController(on_touch_callback=on_station_touched)
elif MockTouchController:
    touch_controller = MockTouchController(on_touch_callback=on_station_touched)
else:
    touch_controller = None

def background_updater():
    """Background thread to continuously fetch transit data"""
    global current_data
    
    print("Background updater started...")
    
    # Initial fetch
    try:
        print("Performing initial data fetch...")
        new_data = data_fetcher.get_all_transit_data()
        with data_lock:
            current_data = new_data
        
        # Update ambient LED status
        led_controller.set_ambient_status(new_data['overall_status'])
        
        print(f"[OK] Initial data loaded successfully")
    except Exception as e:
        print(f"[ERROR] Error in initial fetch: {e}")
    
    while True:
        try:
            # Fetch all transit data
            new_data = data_fetcher.get_all_transit_data()
            
            with data_lock:
                current_data = new_data
            
            # Update ambient LED (only if not showing station detail)
            if led_controller.mode == 'ambient':
                led_controller.set_ambient_status(new_data['overall_status'])
            
            print(f"[OK] Data updated at {datetime.now().strftime('%H:%M:%S')}")
            
            time.sleep(config.UPDATE_INTERVALS['transit'])
            
        except Exception as e:
            print(f"[ERROR] Error in background updater: {e}")
            time.sleep(5)

# Start background updater
updater_thread = threading.Thread(target=background_updater, daemon=True)
updater_thread.start()

@app.route('/')
def index():
    """Serve main dashboard page"""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """Get all transit status data"""
    with data_lock:
        response = current_data if current_data else {
            'overall_status': 'offline',
            'f_train': {'status': 'offline', 'next_trains': [], 'alerts': []},
            'tram': {'status': 'offline'},
            'ferry': {'status': 'offline'},
            'weather': {},
            'timestamp': datetime.now().isoformat()
        }
        
        # Add selected station if any
        if selected_station:
            response['selected_station'] = selected_station
        
        return jsonify(response)

@app.route('/api/station/<stop_id>')
def get_station_detail(stop_id):
    """Get detailed data for specific station"""
    try:
        # Determine line from stop_id
        if stop_id.startswith('F'):
            line = 'F'
        elif stop_id.startswith('Q'):
            line = 'Q'
        elif stop_id.startswith('E'):
            line = 'E'
        elif stop_id.startswith('N'):
            line = 'N'
        elif stop_id == 'TRAM':
            return jsonify(data_fetcher.get_tram_status())
        elif stop_id == 'FERRY':
            return jsonify(data_fetcher.get_ferry_status())
        else:
            return jsonify({'error': 'Unknown station'}), 404
        
        station_data = data_fetcher.get_station_data(stop_id, line)
        return jsonify(station_data)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/touch/<int:pad_number>')
def simulate_touch(pad_number):
    """Simulate touching a station (for testing without hardware)"""
    if touch_controller:
        station = touch_controller.get_station_info(pad_number)
        if station:
            on_station_touched(station)
            return jsonify({
                'success': True,
                'station': station,
                'message': f'Simulated touch on {station["name"]}'
            })
    
    return jsonify({'success': False, 'error': 'Touch controller not available'}), 400

@app.route('/api/led/ambient')
def return_to_ambient():
    """Return LED display to ambient mode"""
    global selected_station
    selected_station = None
    led_controller.return_to_ambient()
    return jsonify({'success': True, 'mode': 'ambient'})

@app.route('/api/led/test')
def test_led():
    """Test LED ring with rainbow animation"""
    try:
        led_controller.rainbow_test()
        return jsonify({'success': True, 'message': 'Rainbow test running'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/debug')
def debug_info():
    """Debug endpoint"""
    now = datetime.now()
    return jsonify({
        'current_time': now.strftime('%H:%M:%S'),
        'led_mode': led_controller.mode if hasattr(led_controller, 'mode') else 'unknown',
        'selected_station': selected_station,
        'touch_available': TOUCH_AVAILABLE,
        'led_available': NEOPIXEL_AVAILABLE
    })

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'features': {
            'touch': TOUCH_AVAILABLE,
            'led': NEOPIXEL_AVAILABLE
        }
    })

if __name__ == '__main__':
    print("=" * 60)
    print("Roosevelt Transit Lens - Interactive Map Edition")
    print("=" * 60)
    print(f"[OK] Flask server starting on port {config.FLASK_CONFIG['port']}")
    print(f"[OK] Touch support: {'Enabled' if TOUCH_AVAILABLE else 'Simulation mode'}")
    print(f"[OK] LED support: {'Enabled' if NEOPIXEL_AVAILABLE else 'Simulation mode'}")
    print(f"[OK] Display support: {'Enabled' if DISPLAY_AVAILABLE else 'Simulation mode'}")
    print(f"[OK] Access at: http://192.168.1.40:{config.FLASK_CONFIG['port']}")
    print("=" * 60)
    print()
    
    app.run(
        host=config.FLASK_CONFIG['host'],
        port=config.FLASK_CONFIG['port'],
        debug=config.FLASK_CONFIG['debug']
    )