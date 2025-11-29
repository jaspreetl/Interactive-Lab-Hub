#!/usr/bin/env python3
"""
Quick test script for NeoPixel LED ring
Run with: python3 test_leds.py (inside venv)
"""

import time
import sys
import os

try:
    import board
    import neopixel
except ImportError:
    print("ERROR: NeoPixel library not installed!")
    print("Install with: pip install rpi_ws281x adafruit-circuitpython-neopixel")
    sys.exit(1)

# Configuration
NUM_PIXELS = 12  # 12-LED NeoPixel ring
GPIO_PIN = board.D18
BRIGHTNESS = 0.5

def test_connection():
    """Test basic LED connection"""
    print("=" * 60)
    print("NeoPixel LED Ring Test (12 LEDs)")
    print("=" * 60)
    print(f"Number of LEDs: {NUM_PIXELS}")
    print(f"GPIO Pin: 18 (board.D18)")
    print(f"Brightness: {BRIGHTNESS}")
    print()
    
    try:
        # Initialize NeoPixel
        print("Initializing NeoPixel...")
        pixels = neopixel.NeoPixel(
            GPIO_PIN,
            NUM_PIXELS,
            brightness=BRIGHTNESS,
            auto_write=False,
            pixel_order=neopixel.GRB
        )
        print("[OK] NeoPixel initialized successfully!")
        print()
        
        # Test 1: All Red
        print("Test 1: All LEDs Red (3 seconds)")
        pixels.fill((255, 0, 0))
        pixels.show()
        time.sleep(3)
        
        # Test 2: All Green
        print("Test 2: All LEDs Green (3 seconds)")
        pixels.fill((0, 255, 0))
        pixels.show()
        time.sleep(3)
        
        # Test 3: All Blue
        print("Test 3: All LEDs Blue (3 seconds)")
        pixels.fill((0, 0, 255))
        pixels.show()
        time.sleep(3)
        
        # Test 4: Rainbow
        print("Test 4: Rainbow animation")
        rainbow_cycle(pixels, 0.01)
        
        # Test 5: Individual LEDs
        print("Test 5: Individual LED test")
        pixels.fill((0, 0, 0))
        for i in range(NUM_PIXELS):
            pixels[i] = (50, 50, 50)
            pixels.show()
            print(f"  LED {i + 1}/{NUM_PIXELS}", end='\r')
            time.sleep(0.2)
            pixels[i] = (0, 0, 0)
        print()
        
        # Test 6: Transit status colors
        print("Test 6: Transit status colors")
        
        print("  Normal (Green) - 2 seconds")
        pixels.fill((0, 255, 0))
        pixels.show()
        time.sleep(2)
        
        print("  Delays (Yellow) - 2 seconds")
        pixels.fill((255, 215, 0))
        pixels.show()
        time.sleep(2)
        
        print("  Problems (Red) - 2 seconds")
        pixels.fill((255, 0, 0))
        pixels.show()
        time.sleep(2)
        
        # Turn off
        print()
        print("Turning off all LEDs...")
        pixels.fill((0, 0, 0))
        pixels.show()
        
        print()
        print("=" * 60)
        print("[OK] All tests completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print()
        print("=" * 60)
        print(f"[ERROR] {e}")
        print("=" * 60)
        print()
        print("Troubleshooting tips:")
        print("1. Make sure your virtual environment has GPIO access")
        print("2. Check your wiring:")
        print("   - 5V  → Pin 4")
        print("   - GND → Pin 6")
        print("   - DIN → Pin 12 (GPIO 18)")
        print("3. Try a different GND pin (e.g., Pin 14)")
        print("4. Verify the NeoPixel ring is the 12-LED version")
        sys.exit(1)

def rainbow_cycle(pixels, wait):
    """Rainbow animation"""
    def wheel(pos):
        if pos < 85:
            return (pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return (255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return (0, pos * 3, 255 - pos * 3)
    
    for j in range(255):
        for i in range(NUM_PIXELS):
            pixel_index = (i * 256 // NUM_PIXELS) + j
            pixels[i] = wheel(pixel_index & 255)
        pixels.show()
        time.sleep(wait)

if __name__ == "__main__":
    test_connection()