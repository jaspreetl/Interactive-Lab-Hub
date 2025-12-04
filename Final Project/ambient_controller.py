# ambient_controller.py
"""
Controls NeoPixel LED ring to display ambient transit status
"""

import time
import threading

try:
    import board
    import neopixel
    NEOPIXEL_AVAILABLE = True
except (ImportError, NotImplementedError):
    print("NeoPixel library not available - LED control disabled")
    print("This is normal if not running on Raspberry Pi")
    NEOPIXEL_AVAILABLE = False

import config

class AmbientLEDController:
    def __init__(self, display_controller=None):
        self.current_status = 'offline'
        # optional display controller reference (enhanced apps may pass this)
        self.display_controller = display_controller
        self.pixels = None
        self.animation_thread = None
        self.running = False
        
        if NEOPIXEL_AVAILABLE:
            try:
                # Initialize NeoPixel
                self.pixels = neopixel.NeoPixel(
                    board.D18,  # GPIO 18
                    config.LED_CONFIG['num_pixels'],
                    brightness=config.LED_CONFIG['brightness'],
                    auto_write=False,
                    pixel_order=neopixel.GRB
                )
                print("NeoPixel LED ring initialized on GPIO 18")
                self.running = True
                
                # Start animation thread
                self.animation_thread = threading.Thread(target=self._animate_loop, daemon=True)
                self.animation_thread.start()
                
            except Exception as e:
                print(f"Failed to initialize NeoPixel: {e}")
                print("Make sure you're running as root: sudo python app.py")
                self.pixels = None
        else:
            print("Running in simulation mode (no physical LEDs)")
    
    def set_status(self, status):
        """Update LED status (normal, delays, problems, offline)"""
        if status != self.current_status:
            print(f"LED Status changed: {self.current_status} -> {status}")
            self.current_status = status
    
    def _animate_loop(self):
        """Background animation thread"""
        while self.running:
            try:
                if self.current_status == 'normal':
                    self._solid_color(config.LED_CONFIG['colors']['normal'])
                
                elif self.current_status == 'delays':
                    self._pulse_color(config.LED_CONFIG['colors']['delays'])
                
                elif self.current_status == 'problems':
                    self._pulse_color(config.LED_CONFIG['colors']['problems'], speed=0.5)
                
                else:  # offline
                    self._breathing_color(config.LED_CONFIG['colors']['offline'])
                
            except Exception as e:
                print(f"Error in LED animation: {e}")
                time.sleep(1)
    
    def _solid_color(self, color):
        """Display solid color (for normal status)"""
        if not self.pixels:
            time.sleep(0.1)
            return
        
        self.pixels.fill(color)
        self.pixels.show()
        time.sleep(0.1)
    
    def _pulse_color(self, color, speed=1.0):
        """Pulse color (for delays/problems)"""
        if not self.pixels:
            time.sleep(0.1)
            return
        
        # Pulse brightness up and down
        for brightness in range(30, 100, 5):
            if self.current_status not in ['delays', 'problems']:
                break
            
            adjusted_color = tuple(int(c * brightness / 100) for c in color)
            self.pixels.fill(adjusted_color)
            self.pixels.show()
            time.sleep(0.03 / speed)
        
        for brightness in range(100, 30, -5):
            if self.current_status not in ['delays', 'problems']:
                break
            
            adjusted_color = tuple(int(c * brightness / 100) for c in color)
            self.pixels.fill(adjusted_color)
            self.pixels.show()
            time.sleep(0.03 / speed)
    
    def _breathing_color(self, color):
        """Slow breathing effect (for offline status)"""
        if not self.pixels:
            time.sleep(0.1)
            return
        
        # Slow breathing
        for brightness in range(10, 60, 2):
            if self.current_status != 'offline':
                break
            
            adjusted_color = tuple(int(c * brightness / 100) for c in color)
            self.pixels.fill(adjusted_color)
            self.pixels.show()
            time.sleep(0.05)
        
        for brightness in range(60, 10, -2):
            if self.current_status != 'offline':
                break
            
            adjusted_color = tuple(int(c * brightness / 100) for c in color)
            self.pixels.fill(adjusted_color)
            self.pixels.show()
            time.sleep(0.05)
    
    def rainbow_test(self):
        """Test animation - cycle through rainbow colors"""
        if not self.pixels:
            print("LED test: No physical LEDs connected")
            return
        
        print("Running LED rainbow test...")
        
        def wheel(pos):
            """Generate rainbow colors across 0-255 positions"""
            if pos < 85:
                return (pos * 3, 255 - pos * 3, 0)
            elif pos < 170:
                pos -= 85
                return (255 - pos * 3, 0, pos * 3)
            else:
                pos -= 170
                return (0, pos * 3, 255 - pos * 3)
        
        for j in range(255):
            for i in range(config.LED_CONFIG['num_pixels']):
                pixel_index = (i * 256 // config.LED_CONFIG['num_pixels']) + j
                self.pixels[i] = wheel(pixel_index & 255)
            self.pixels.show()
            time.sleep(0.01)
        
        print("Rainbow test complete")
    
    def clear(self):
        """Turn off all LEDs"""
        if self.pixels:
            self.pixels.fill((0, 0, 0))
            self.pixels.show()
    
    def shutdown(self):
        """Clean shutdown"""
        self.running = False
        if self.animation_thread:
            self.animation_thread.join(timeout=2)
        self.clear()
        print("LED controller shut down")

# Create a mock controller for development without hardware
class MockLEDController:
    """Mock LED controller for development without hardware"""
    def __init__(self, display_controller=None):
        self.current_status = 'offline'
        # accept optional display controller for API compatibility
        self.display_controller = display_controller
        print("Info: Mock LED controller initialized (no hardware)")
    
    def set_status(self, status):
        if status != self.current_status:
            print(f"LED Status: {status}")
            self.current_status = status
    
    def rainbow_test(self):
        print("Rainbow test (simulated)")
    
    def clear(self):
        print("LEDs cleared (simulated)")
    
    def shutdown(self):
        print("LED controller shut down (simulated)")