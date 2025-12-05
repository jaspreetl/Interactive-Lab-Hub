# display_controller.py
"""
Controls physical display screen to show detailed transit information
Supports multiple display types: OLED, TFT, HDMI
"""

import time
import os
from datetime import datetime

# Try to import display libraries
DISPLAY_TYPE = None

# Configure for VNC/X11 display if needed
if 'DISPLAY' not in os.environ:
    # Try to detect common VNC display settings
    if os.path.exists('/tmp/.X11-unix'):
        # X11 is available, set default display
        os.environ['DISPLAY'] = ':0'
    else:
        # Try to find active display
        os.environ['DISPLAY'] = ':0'

try:
    import board
    import busio
    from adafruit_ssd1306 import SSD1306_I2C
    from PIL import Image, ImageDraw, ImageFont
    DISPLAY_TYPE = 'OLED'
    print("[INFO] OLED display library available")
except ImportError:
    try:
        import pygame
        # Set SDL to use X11 for VNC compatibility
        if 'SDL_VIDEODRIVER' not in os.environ:
            os.environ['SDL_VIDEODRIVER'] = 'x11'
        DISPLAY_TYPE = 'PYGAME'
        print("[INFO] Using pygame for display (HDMI/TFT/VNC)")
    except ImportError:
        print("[WARNING] No display library available")
        DISPLAY_TYPE = None


class DisplayController:
    """Controls physical display showing transit information"""
    
    def __init__(self, display_type='auto'):
        self.display = None
        self.display_type = None
        self.width = 128
        self.height = 64
        
        if display_type == 'auto':
            # Check for environment variable to force pygame mode (useful for VNC)
            if os.environ.get('FORCE_PYGAME_DISPLAY', '').lower() in ('1', 'true', 'yes'):
                display_type = 'PYGAME'
            else:
                display_type = DISPLAY_TYPE
        
        if display_type == 'OLED':
            self._init_oled()
        elif display_type == 'PYGAME':
            self._init_pygame()
        elif display_type == 'TFT':
            self._init_tft()
        else:
            print("[INFO] Running in simulation mode (no physical display)")
    
    def _init_oled(self):
        """Initialize I2C OLED display (128x64)"""
        try:
            i2c = busio.I2C(board.SCL, board.SDA)
            self.display = SSD1306_I2C(128, 64, i2c, addr=0x3C)
            self.display_type = 'OLED'
            self.width = 128
            self.height = 64
            
            # Clear display
            self.display.fill(0)
            self.display.show()
            
            print("[OK] OLED display initialized (128x64)")
        except Exception as e:
            print(f"[ERROR] Failed to initialize OLED: {e}")
            self.display = None
    
    def _init_pygame(self):
        """Initialize pygame for HDMI display or VNC"""
        try:
            # Ensure DISPLAY is set for VNC
            if 'DISPLAY' not in os.environ:
                os.environ['DISPLAY'] = ':0'
            
            # Initialize pygame with error handling
            pygame.init()
            
            # Try to get display info to determine size
            try:
                # Get available video modes
                modes = pygame.display.list_modes()
                if modes and modes[0] != -1:
                    # Use first available mode or default
                    self.width = min(800, modes[0][0] if isinstance(modes[0], tuple) else 480)
                    self.height = min(600, modes[0][1] if isinstance(modes[0], tuple) else 320)
                else:
                    self.width = 480
                    self.height = 320
            except:
                # Default size if we can't detect
                self.width = 480
                self.height = 320
            
            # Create display window
            self.display = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption("Roosevelt Transit Lens")
            self.display_type = 'PYGAME'
            
            # Clear to black
            self.display.fill((0, 0, 0))
            pygame.display.flip()
            
            print(f"[OK] Pygame display initialized ({self.width}x{self.height})")
            print(f"[INFO] DISPLAY={os.environ.get('DISPLAY', 'not set')}")
        except Exception as e:
            print(f"[ERROR] Failed to initialize pygame: {e}")
            print(f"[INFO] DISPLAY={os.environ.get('DISPLAY', 'not set')}")
            print("[INFO] Try: export DISPLAY=:0")
            self.display = None
    
    def _init_tft(self):
        """Initialize TFT display (placeholder for SPI displays)"""
        # TODO: Add TFT display support
        print("[INFO] TFT display not yet implemented")
        self.display = None
    
    def show_ambient_status(self, overall_status):
        """Show overall transit status in ambient mode"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        print(f"[DISPLAY] [{timestamp}] Updating to AMBIENT mode - Status: {overall_status.upper()}")
        
        if not self.display:
            print(f"[DISPLAY] [{timestamp}] No physical display - running in console mode")
            return
        
        if self.display_type == 'OLED':
            self._show_ambient_oled(overall_status)
        elif self.display_type == 'PYGAME':
            self._show_ambient_pygame(overall_status)
        
            print(f"[DISPLAY] [{timestamp}] [OK] Ambient display updated successfully")
    
    def show_station_detail(self, station_data):
        """Show detailed information for touched station"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        station_name = station_data.get('name', 'Unknown')
        station_line = station_data.get('line', '?')
        trains_count = len(station_data.get('next_trains', []))
        
        # Use ASCII-only logging to avoid encoding issues on terminals with latin-1
        print(f"[DISPLAY] [{timestamp}] STATION TOUCHED: {station_name} ({station_line} line)")
        print(f"[DISPLAY] [{timestamp}] Showing {trains_count} upcoming trains")
        
        if not self.display:
            print(f"[DISPLAY] [{timestamp}] No physical display - running in console mode")
            print(f"[DISPLAY] [{timestamp}] Station: {station_name} | Line: {station_line}")
            for i, train in enumerate(station_data.get('next_trains', [])[:3], 1):
                print(f"[DISPLAY] [{timestamp}]   Train {i}: {train.get('minutes', '?')}min to {train.get('direction', 'Unknown')}")
            return
        
        if self.display_type == 'OLED':
            self._show_station_oled(station_data)
        elif self.display_type == 'PYGAME':
            self._show_station_pygame(station_data)
        
            print(f"[DISPLAY] [{timestamp}] [OK] Display updated with {station_name} details")
    
    def _show_ambient_oled(self, status):
        """OLED: Show ambient status"""
        try:
            # Create image
            image = Image.new('1', (self.width, self.height))
            draw = ImageDraw.Draw(image)
            
            # Load font
            try:
                font_large = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 16)
                font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 10)
            except:
                font_large = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Title
            draw.text((5, 5), "Transit Status", font=font_small, fill=255)
            
            # Status message
            if status == 'normal':
                msg = "ALL SYSTEMS\n   NORMAL"
            elif status == 'delays':
                msg = "  DELAYS\n DETECTED"
            elif status == 'problems':
                msg = "  SERVICE\n  ISSUES"
            else:
                msg = "  OFFLINE"
            
            draw.text((10, 25), msg, font=font_large, fill=255)
            
            # Time
            current_time = datetime.now().strftime('%I:%M %p')
            draw.text((5, 55), current_time, font=font_small, fill=255)
            
            # Update indicator
            update_time = datetime.now().strftime('%H:%M:%S')
            draw.text((70, 55), "UPD", font=font_small, fill=255)
            
            # Display
            self.display.image(image)
            self.display.show()
            
        except Exception as e:
            print(f"[ERROR] OLED display error: {e}")
    
    def _show_station_oled(self, station_data):
        """OLED: Show station details"""
        try:
            # Create image
            image = Image.new('1', (self.width, self.height))
            draw = ImageDraw.Draw(image)
            
            # Load fonts
            try:
                font_title = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 12)
                font_data = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 10)
                font_small = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 8)
            except:
                font_title = ImageFont.load_default()
                font_data = ImageFont.load_default()
                font_small = ImageFont.load_default()
            
            # Station name (truncated if needed)
            name = station_data.get('name', 'Unknown')
            if len(name) > 15:
                name = name[:15] + '.'
            draw.text((2, 2), name, font=font_title, fill=255)
            
            # Line indicator
            line = station_data.get('line', '?')
            draw.rectangle((2, 17, 15, 30), outline=255, fill=0)
            draw.text((5, 19), line, font=font_data, fill=255)
            
            # Next trains
            trains = station_data.get('next_trains', [])
            y_pos = 18
            
            if trains:
                for i, train in enumerate(trains[:3]):  # Show first 3 trains
                    minutes = train.get('minutes', '?')
                    direction = train.get('direction', '')
                    
                    # Truncate direction
                    if len(direction) > 8:
                        direction = direction[:8]
                    
                    train_text = f"{minutes}min  {direction}"
                    draw.text((20, y_pos), train_text, font=font_data, fill=255)
                    y_pos += 12
            else:
                draw.text((20, y_pos), "No trains", font=font_data, fill=255)
            
            # Status/alerts at bottom
            status = station_data.get('status', 'unknown')
            if status == 'delays':
                draw.text((2, 56), "DELAYS", font=font_small, fill=255)
            elif status == 'problems':
                draw.text((2, 56), "PROBLEMS", font=font_small, fill=255)
            
            # Update timestamp indicator
            update_time = datetime.now().strftime('%H:%M')
            draw.text((90, 56), update_time, font=font_small, fill=255)
            
            # Display
            self.display.image(image)
            self.display.show()
            
        except Exception as e:
            print(f"[ERROR] OLED station display error: {e}")
    
    def _show_ambient_pygame(self, status):
        """Pygame: Show ambient status (for HDMI displays)"""
        try:
            # Clear screen
            self.display.fill((0, 0, 0))
            
            # Load fonts
            font_large = pygame.font.Font(None, 72)
            font_medium = pygame.font.Font(None, 36)
            font_small = pygame.font.Font(None, 24)
            
            # Title
            title = font_medium.render("Transit Status", True, (255, 255, 255))
            self.display.blit(title, (20, 20))
            
            # Status with color
            if status == 'normal':
                color = (0, 255, 0)
                text = "ALL SYSTEMS NORMAL"
            elif status == 'delays':
                color = (255, 215, 0)
                text = "DELAYS DETECTED"
            elif status == 'problems':
                color = (255, 0, 0)
                text = "SERVICE ISSUES"
            else:
                color = (128, 128, 128)
                text = "OFFLINE"
            
            status_text = font_large.render(text, True, color)
            text_rect = status_text.get_rect(center=(self.width // 2, self.height // 2))
            self.display.blit(status_text, text_rect)
            
            # Time
            current_time = datetime.now().strftime('%I:%M %p')
            time_text = font_small.render(current_time, True, (128, 128, 128))
            self.display.blit(time_text, (20, self.height - 40))
            
            # Update indicator
            update_time = datetime.now().strftime('Updated: %H:%M:%S')
            update_text = font_small.render(update_time, True, (64, 64, 64))
            self.display.blit(update_text, (self.width - 200, self.height - 40))
            
            pygame.display.flip()
            
        except Exception as e:
            print(f"[ERROR] Pygame display error: {e}")
    
    def _show_station_pygame(self, station_data):
        """Pygame: Show station details"""
        try:
            # Clear screen
            self.display.fill((0, 0, 0))
            
            # Load fonts
            font_title = pygame.font.Font(None, 48)
            font_line = pygame.font.Font(None, 72)
            font_data = pygame.font.Font(None, 36)
            font_small = pygame.font.Font(None, 24)
            
            # Station name
            name = station_data.get('name', 'Unknown Station')
            name_text = font_title.render(name, True, (255, 255, 255))
            self.display.blit(name_text, (20, 20))
            
            # Line indicator (big colored circle/square)
            line = station_data.get('line', '?')
            line_color = self._get_line_color(line)
            pygame.draw.circle(self.display, line_color, (50, 120), 35)
            line_text = font_line.render(line, True, (255, 255, 255))
            line_rect = line_text.get_rect(center=(50, 120))
            self.display.blit(line_text, line_rect)
            
            # Next trains
            trains = station_data.get('next_trains', [])
            y_pos = 90
            
            if trains:
                for i, train in enumerate(trains[:4]):  # Show up to 4 trains
                    minutes = train.get('minutes', '?')
                    direction = train.get('direction', 'Unknown')
                    
                    # Time
                    time_text = font_data.render(f"{minutes} min", True, (0, 255, 0))
                    self.display.blit(time_text, (110, y_pos))
                    
                    # Direction
                    dir_text = font_small.render(f"to {direction}", True, (180, 180, 180))
                    self.display.blit(dir_text, (250, y_pos + 5))
                    
                    y_pos += 50
            else:
                no_trains = font_data.render("No upcoming trains", True, (255, 0, 0))
                self.display.blit(no_trains, (110, y_pos))
            
            # Status at bottom
            status = station_data.get('status', 'normal')
            if status == 'delays':
                status_text = font_small.render("DELAYS ON THIS LINE", True, (255, 215, 0))
                self.display.blit(status_text, (20, self.height - 40))
            elif status == 'problems':
                status_text = font_small.render("SERVICE DISRUPTION", True, (255, 0, 0))
                self.display.blit(status_text, (20, self.height - 40))
            
            # Update timestamp indicator (top right)
            update_time = datetime.now().strftime('%H:%M:%S')
            update_text = font_small.render(f"Updated: {update_time}", True, (100, 100, 100))
            update_rect = update_text.get_rect()
            self.display.blit(update_text, (self.width - update_rect.width - 10, 5))
            
            # Visual indicator that this is a station view
            indicator_text = font_small.render("STATION VIEW", True, (0, 255, 0))
            self.display.blit(indicator_text, (20, self.height - 60))
            
            pygame.display.flip()
            
        except Exception as e:
            print(f"[ERROR] Pygame station display error: {e}")
    
    def _get_line_color(self, line):
        """Get MTA line color"""
        colors = {
            'F': (255, 99, 25),    # Orange
            'Q': (255, 204, 0),    # Yellow
            'E': (0, 57, 166),     # Blue
            'M': (255, 99, 25),    # Orange
            'R': (255, 204, 0),    # Yellow
            'N': (255, 204, 0),    # Yellow
            'W': (255, 204, 0),    # Yellow
            '1': (238, 53, 46),    # Red
            '2': (238, 53, 46),    # Red
            '3': (238, 53, 46),    # Red
            '4': (0, 147, 60),     # Green
            '5': (0, 147, 60),     # Green
            '6': (0, 147, 60),     # Green
            '7': (185, 51, 173),   # Purple
        }
        return colors.get(line, (128, 128, 128))
    
    def clear(self):
        """Clear display"""
        if self.display:
            if self.display_type == 'OLED':
                self.display.fill(0)
                self.display.show()
            elif self.display_type == 'PYGAME':
                self.display.fill((0, 0, 0))
                pygame.display.flip()
    
    def shutdown(self):
        """Clean shutdown"""
        self.clear()
        if self.display_type == 'PYGAME':
            pygame.quit()
        print("[INFO] Display controller shut down")


class MockDisplayController:
    """Mock display for testing without hardware"""
    
    def __init__(self, display_type='mock'):
        print("[INFO] Mock display controller initialized")
    
    def show_ambient_status(self, status):
        print(f"[DISPLAY] Ambient: {status.upper()}")
    
    def show_station_detail(self, station_data):
        name = station_data.get('name', 'Unknown')
        trains = station_data.get('next_trains', [])
        print(f"[DISPLAY] Station: {name}")
        for train in trains[:3]:
            print(f"  - {train.get('minutes')}min to {train.get('direction')}")
    
    def clear(self):
        print("[DISPLAY] Cleared")
    
    def shutdown(self):
        print("[DISPLAY] Shutdown")