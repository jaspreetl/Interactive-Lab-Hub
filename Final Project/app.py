# app.py
"""
Flask web application for Roosevelt Transit Lens
Serves web interface and provides API endpoints for transit data
"""

from flask import Flask, render_template, jsonify
from flask_cors import CORS
from datetime import datetime
import threading
import time

import config
from data_fetcher import TransitDataFetcher
from ambient_controller import AmbientLEDController, MockLEDController, NEOPIXEL_AVAILABLE

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for API access

# Initialize data fetcher
data_fetcher = TransitDataFetcher()

# Initialize LED controller
if NEOPIXEL_AVAILABLE:
    led_controller = AmbientLEDController()
else:
    led_controller = MockLEDController()

# Global variable to store current transit data
current_data = {}
data_lock = threading.Lock()

def background_updater():
    """Background thread to continuously fetch transit data"""
    global current_data
    
    print("Background updater started...")
    
    # Do initial fetch immediately
    try:
        print("Performing initial data fetch...")
        new_data = data_fetcher.get_all_transit_data()
        with data_lock:
            current_data = new_data
        
        # Update LED status
        led_controller.set_status(new_data['overall_status'])
        
        print(f"✓ Initial data loaded successfully")
    except Exception as e:
        print(f"✗ Error in initial fetch: {e}")
    
    while True:
        try:
            # Fetch all transit data
            new_data = data_fetcher.get_all_transit_data()
            
            with data_lock:
                current_data = new_data
            
            # Update LED ring with new status
            led_controller.set_status(new_data['overall_status'])
            
            print(f"✓ Data updated at {datetime.now().strftime('%H:%M:%S')}")
            
            # Wait before next update
            time.sleep(config.UPDATE_INTERVALS['transit'])
            
        except Exception as e:
            print(f"✗ Error in background updater: {e}")
            time.sleep(5)  # Wait a bit before retrying

# Start background updater thread
updater_thread = threading.Thread(target=background_updater, daemon=True)
updater_thread.start()

@app.route('/')
def index():
    """Serve main dashboard page"""
    return render_template('index.html')

@app.route('/api/status')
def get_status():
    """API endpoint: Get all transit status data"""
    with data_lock:
        return jsonify(current_data if current_data else {
            'overall_status': 'offline',
            'f_train': {'status': 'offline', 'next_trains': [], 'alerts': []},
            'tram': {'status': 'offline'},
            'ferry': {'status': 'offline'},
            'weather': {},
            'timestamp': datetime.now().isoformat()
        })

@app.route('/api/train/<route>')
def get_train_details(route):
    """API endpoint: Get detailed info for specific train route"""
    if route == 'f':
        train_data = data_fetcher.get_f_train_status()
        return jsonify(train_data)
    else:
        return jsonify({'error': 'Route not found'}), 404

@app.route('/api/weather')
def get_weather():
    """API endpoint: Get current weather data"""
    weather_data = data_fetcher.get_weather_data()
    return jsonify(weather_data)

@app.route('/api/refresh')
def force_refresh():
    """API endpoint: Force immediate data refresh"""
    global current_data
    
    try:
        new_data = data_fetcher.get_all_transit_data()
        with data_lock:
            current_data = new_data
        return jsonify({'success': True, 'data': new_data})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/led/test')
def test_led():
    """API endpoint: Test LED ring with rainbow animation"""
    try:
        led_controller.rainbow_test()
        return jsonify({'success': True, 'message': 'Rainbow test running'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@app.route('/api/led/status/<status>')
def set_led_status(status):
    """API endpoint: Manually set LED status (for testing)"""
    valid_statuses = ['normal', 'delays', 'problems', 'offline']
    if status in valid_statuses:
        led_controller.set_status(status)
        return jsonify({'success': True, 'status': status})
    else:
        return jsonify({'success': False, 'error': 'Invalid status'}), 400

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'data_available': bool(current_data)
    })

if __name__ == '__main__':
    print("=" * 60)
    print("🚇 Starting Roosevelt Transit Lens...")
    print("=" * 60)
    print(f"✓ Flask server starting on port {config.FLASK_CONFIG['port']}")
    print(f"✓ Access locally at: http://localhost:{config.FLASK_CONFIG['port']}")
    print(f"✓ Access from iPad at: http://[your-pi-ip]:{config.FLASK_CONFIG['port']}")
    print(f"✓ Background updates every {config.UPDATE_INTERVALS['transit']} seconds")
    print("=" * 60)
    print()
    
    app.run(
        host=config.FLASK_CONFIG['host'],
        port=config.FLASK_CONFIG['port'],
        debug=config.FLASK_CONFIG['debug']
    )