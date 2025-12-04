# enhanced_ambient_controller.py
"""
Enhanced LED controller that can show:
1. Overall transit status (ambient mode)
2. Specific station status (focused mode when touched)
"""

import time
import threading

try:
    import board
    import neopixel
    NEOPIXEL_AVAILABLE = True
except (ImportError, NotImplementedError):
    NEOPIXEL_AVAILABLE = False

import config

class EnhancedLEDController:
    def __init__(self, display_controller=None):
        self.pixels = None
        self.running = False
        self.mode = 'ambient'  # 'ambient' or 'station'
        self.current_status = 'offline'
        self.station_data = None
        self.display = display_controller  # Link to display controller
        
        if NEOPIXEL_AVAILABLE:
            try:
                self.pixels = neopixel.NeoPixel(
                    board.D18,
                    config.LED_CONFIG['num_pixels'],
                    brightness=config.LED_CONFIG['brightness'],
                    auto_write=False,
                    pixel_order=neopixel.GRB
                )
                print("[OK] Enhanced NeoPixel controller initialized")
                
                self.running = True
                self.animation_thread = threading.Thread(target=self._animate_loop, daemon=True)
                self.animation_thread.start()
                
            except Exception as e:
                print(f"[ERROR] Failed to initialize NeoPixel: {e}")
                self.pixels = None
    
    def set_ambient_status(self, status):
        """Set overall transit status (green/yellow/red)"""
        if self.mode == 'ambient' and status != self.current_status:
            print(f"[LED] Ambient status: {status}")
            self.current_status = status
            self.mode = 'ambient'
            
            # Update display too
            if self.display:
                self.display.show_ambient_status(status)
    
    def show_station_status(self, station_data):
        """Show specific station status on LED ring AND display"""
        print(f"[LED] Showing station: {station_data['name']}")
        self.mode = 'station'
        self.station_data = station_data
        
        # Update display with station details
        if self.display:
            self.display.show_station_detail(station_data)
    
    def return_to_ambient(self):
        """Return to ambient mode after timeout"""
        print("[LED] Returning to ambient mode")
        self.mode = 'ambient'
        self.station_data = None
        
        # Return display to ambient too
        if self.display:
            self.display.show_ambient_status(self.current_status)
    
    def _animate_loop(self):
        """Background animation thread"""
        station_timeout = 0
        
        while self.running:
            try:
                if self.mode == 'station' and self.station_data:
                    # Show station-specific visualization
                    self._show_station_visual(self.station_data)
                    
                    # Auto-return to ambient after 30 seconds
                    station_timeout += 1
                    if station_timeout > 300:  # 30 seconds at 0.1s intervals
                        self.return_to_ambient()
                        station_timeout = 0
                
                elif self.mode == 'ambient':
                    station_timeout = 0
                    # Show overall status
                    if self.current_status == 'normal':
                        self._solid_color(config.LED_CONFIG['colors']['normal'])
                    elif self.current_status == 'delays':
                        self._pulse_color(config.LED_CONFIG['colors']['delays'])
                    elif self.current_status == 'problems':
                        self._pulse_color(config.LED_CONFIG['colors']['problems'], speed=0.5)
                    else:
                        self._breathing_color(config.LED_CONFIG['colors']['offline'])
                
            except Exception as e:
                print(f"[ERROR] LED animation error: {e}")
                time.sleep(1)
    
    def _show_station_visual(self, station_data):
        """Visualize station-specific data on LED ring"""
        if not self.pixels:
            time.sleep(0.1)
            return
        
        # Example: Show train countdown on ring
        # Each LED represents 1 minute
        # Green LEDs = trains arriving in that many minutes
        
        trains = station_data.get('next_trains', [])
        
        if trains:
            self.pixels.fill((0, 0, 0))  # Clear
            
            for train in trains[:3]:  # Show first 3 trains
                minutes = train.get('minutes', 0)
                if minutes < 12:  # Only show if within 12 minutes (12 LEDs)
                    # Light up LED at that position
                    color = (0, 255, 0) if minutes < 5 else (255, 165, 0)
                    self.pixels[minutes] = color
            
            self.pixels.show()
            time.sleep(0.5)
            
        else:
            # No trains - show red
            self._solid_color((255, 0, 0))
    
    def _solid_color(self, color):
        """Display solid color"""
        if not self.pixels:
            time.sleep(0.1)
            return
        
        self.pixels.fill(color)
        self.pixels.show()
        time.sleep(0.1)
    
    def _pulse_color(self, color, speed=1.0):
        """Pulse color"""
        if not self.pixels:
            time.sleep(0.1)
            return
        
        for brightness in range(30, 100, 5):
            adjusted_color = tuple(int(c * brightness / 100) for c in color)
            self.pixels.fill(adjusted_color)
            self.pixels.show()
            time.sleep(0.03 / speed)
        
        for brightness in range(100, 30, -5):
            adjusted_color = tuple(int(c * brightness / 100) for c in color)
            self.pixels.fill(adjusted_color)
            self.pixels.show()
            time.sleep(0.03 / speed)
    
    def _breathing_color(self, color):
        """Slow breathing effect"""
        if not self.pixels:
            time.sleep(0.1)
            return
        
        for brightness in range(10, 60, 2):
            adjusted_color = tuple(int(c * brightness / 100) for c in color)
            self.pixels.fill(adjusted_color)
            self.pixels.show()
            time.sleep(0.05)
        
        for brightness in range(60, 10, -2):
            adjusted_color = tuple(int(c * brightness / 100) for c in color)
            self.pixels.fill(adjusted_color)
            self.pixels.show()
            time.sleep(0.05)
    
    def clear(self):
        """Turn off all LEDs"""
        if self.pixels:
            self.pixels.fill((0, 0, 0))
            self.pixels.show()
    
    def shutdown(self):
        """Clean shutdown"""
        self.running = False
        self.clear()
        print("[INFO] Enhanced LED controller shut down")


class MockEnhancedLEDController:
    """Mock controller for development"""
    
    def __init__(self, display_controller=None):
        print("[INFO] Mock enhanced LED controller initialized")
        self.mode = 'ambient'
        self.display = display_controller
    
    def set_ambient_status(self, status):
        print(f"[LED] Ambient: {status}")
        if self.display:
            self.display.show_ambient_status(status)
    
    def show_station_status(self, station_data):
        print(f"[LED] Station: {station_data['name']}")
        self.mode = 'station'
        if self.display:
            self.display.show_station_detail(station_data)
    
    def return_to_ambient(self):
        print("[LED] Back to ambient")
        self.mode = 'ambient'
        if self.display:
            self.display.show_ambient_status('normal')
    
    def clear(self):
        pass
    
    def shutdown(self):
        pass