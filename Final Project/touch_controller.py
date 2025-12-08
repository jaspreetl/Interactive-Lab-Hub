# touch_controller.py
"""
Handles capacitive touch sensing for interactive subway map
Uses MPR121 to detect touches on copper pads behind stations
"""

import time
import threading

try:
    import board
    import busio
    import adafruit_mpr121
    TOUCH_AVAILABLE = True
except (ImportError, NotImplementedError):
    print("[WARNING] MPR121 library not available")
    TOUCH_AVAILABLE = False

class TouchController:
    def __init__(self, on_touch_callback=None):
        self.touch_sensor = None
        self.on_touch_callback = on_touch_callback
        self.last_touched = None
        self.monitoring = False
        
        # Map touch pad numbers (0-11) to the 12 most important stations
        self.station_map = {
            0: {'name': 'Roosevelt Island', 'line': 'F', 'stop_id': 'F09'},
            1: {'name': 'Lexington Av/63 St', 'line': 'F', 'stop_id': 'F11'},
            2: {'name': '21 St-Queensbridge', 'line': 'F', 'stop_id': 'F08'},
            3: {'name': '57 St-7 Av', 'line': 'F', 'stop_id': 'F15'},
            4: {'name': 'Queens Plaza', 'line': 'E', 'stop_id': 'G08'},
            5: {'name': 'Court Sq-23 St', 'line': 'E', 'stop_id': 'G06'},
            6: {'name': '34 St-Penn Station', 'line': 'A', 'stop_id': 'A28'},
            7: {'name': 'Grand Central-42 St', 'line': '4', 'stop_id': '631'},
            8: {'name': 'Queensboro Plaza', 'line': 'N', 'stop_id': 'R09'},
            9: {'name': 'Lexington Av/59 St', 'line': 'N', 'stop_id': 'E13'},
            10: {'name': 'Union Sq-14 St', 'line': '4', 'stop_id': '635'},
            11: {'name': 'Times Sq-42 St', 'line': 'N', 'stop_id': '902'},
        }
        
        if TOUCH_AVAILABLE:
            try:
                # Initialize I2C and MPR121
                i2c = busio.I2C(board.SCL, board.SDA)
                self.touch_sensor = adafruit_mpr121.MPR121(i2c)
                
                print("[OK] MPR121 touch sensor initialized")
                print(f"[INFO] Monitoring {len(self.station_map)} stations")
                
                # Start monitoring thread
                self.monitoring = True
                self.monitor_thread = threading.Thread(target=self._monitor_touches, daemon=True)
                self.monitor_thread.start()
                
            except Exception as e:
                print(f"[ERROR] Failed to initialize MPR121: {e}")
                print("  Check I2C connection (SDA=Pin 3, SCL=Pin 5)")
                self.touch_sensor = None
        else:
            print("[INFO] Running in simulation mode (no touch sensor)")
    
    def _monitor_touches(self):
        """Background thread to monitor touch events"""
        while self.monitoring:
            try:
                if not self.touch_sensor:
                    time.sleep(0.1)
                    continue
                
                # Check each touch pad
                for i in range(12):
                    if self.touch_sensor[i].value:
                        if i != self.last_touched:
                            self.last_touched = i
                            self._handle_touch(i)
                            time.sleep(0.3)  # Debounce
                
                time.sleep(0.05)  # Check every 50ms
                
            except Exception as e:
                print(f"[ERROR] Touch monitoring error: {e}")
                time.sleep(1)
    
    def _handle_touch(self, pad_number):
        """Handle touch event on specific pad"""
        station = self.station_map.get(pad_number)
        
        if station:
            print(f"[TOUCH] Station touched: {station['name']} ({station['line']} line)")
            
            # Call callback if provided
            if self.on_touch_callback:
                self.on_touch_callback(station)
    
    def get_station_info(self, pad_number):
        """Get station information for a touch pad"""
        return self.station_map.get(pad_number)
    
    def shutdown(self):
        """Clean shutdown"""
        self.monitoring = False
        print("[INFO] Touch controller shut down")


class MockTouchController:
    """Mock touch controller for development without hardware"""
    
    def __init__(self, on_touch_callback=None):
        self.on_touch_callback = on_touch_callback
        print("[INFO] Mock touch controller initialized")
        print("[INFO] Use /api/touch/<station_id> to simulate touches")
        
        # Keep mock map in sync with real map
        self.station_map = {
            0: {'name': 'Roosevelt Island', 'line': 'F', 'stop_id': 'F09'},
            1: {'name': 'Lexington Av/63 St', 'line': 'F', 'stop_id': 'F11'},
            2: {'name': '21 St-Queensbridge', 'line': 'F', 'stop_id': 'F08'},
            3: {'name': '57 St-7 Av', 'line': 'F', 'stop_id': 'F15'},
            4: {'name': 'Queens Plaza', 'line': 'E', 'stop_id': 'G08'},
            5: {'name': 'Court Sq-23 St', 'line': 'E', 'stop_id': 'G06'},
            6: {'name': '34 St-Penn Station', 'line': 'A', 'stop_id': 'A28'},
            7: {'name': 'Grand Central-42 St', 'line': '4', 'stop_id': '631'},
            8: {'name': 'Queensboro Plaza', 'line': 'N', 'stop_id': 'R09'},
            9: {'name': 'Lexington Av/59 St', 'line': 'N', 'stop_id': 'E13'},
            10: {'name': 'Union Sq-14 St', 'line': '4', 'stop_id': '635'},
            11: {'name': 'Times Sq-42 St', 'line': 'N', 'stop_id': '902'},
        }
    
    def simulate_touch(self, pad_number):
        """Simulate a touch event (for testing)"""
        station = self.station_map.get(pad_number)
        if station and self.on_touch_callback:
            print(f"[SIMULATED TOUCH] {station['name']}")
            self.on_touch_callback(station)
    
    def get_station_info(self, pad_number):
        """Get station information"""
        return self.station_map.get(pad_number)
    
    def shutdown(self):
        print("[INFO] Mock touch controller shut down")