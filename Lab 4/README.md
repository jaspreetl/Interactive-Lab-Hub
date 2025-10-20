# Ph-UI!!!

Collaborators: Sachin Jojode, Viha Srinivas, Arya Prasad

## Part A
### Capacitive Sensing, a.k.a. Human-Twizzler Interaction

Video link: https://drive.google.com/drive/folders/1evbBFwEqHrcxWKOFQ3EYnI5o_75qGrA3?usp=drive_link

### Part B

#### Light/Proximity/Gesture sensor (APDS-9960), Rotary Encoder, Joystick, Distance Sensor

Video link: https://drive.google.com/file/d/1ehD8bH60lvMCg55lqQrunhwIYdJYobrk/view?usp=drive_link

Video link: https://drive.google.com/file/d/1W26ObfeldQtcrQ_N_Mj2as69f3vPGz32/view?usp=drive_link

Video link: https://drive.google.com/file/d/1sKus0hbDBE5S6jct1ch_gABQbDqCITnt/view?usp=drive_link

Video link: https://drive.google.com/file/d/1RMcxXh1X0-D-RV6Zxe65zknoet8rwYbv/view?usp=drive_link

Video link: https://drive.google.com/file/d/1q9l43qhkHAv8QIupwswECEeG_p4WJqSi/view?usp=drive_link

Video link: https://drive.google.com/file/d/1DYwKet88xD9-nZ_HSvOKJSka1yBPi9DI/view?usp=drive_link

### Part C
### Physical considerations for sensing

AstroClicker – This concept helps users navigate the night sky. Using a joystick as the main input, the user can select celestial objects and adjust their view to zoom in or out for a closer look.

[AstroClicker] : (https://drive.google.com/file/d/1spiTWBc2pxcqpkH5nn0u24bH49dgJ59T/view?usp=drive_link)

City Explorer – This idea focuses on urban exploration. The device helps users discover new places or uncover hidden gems in familiar cities. With a joystick for navigation, the device tracks where the user has already been and suggests new destinations.
[City Explorer] : (https://drive.google.com/file/d/1NPo4yFDo4cDgwPx_VDBPNtk57suxaHIC/view?usp=drive_link)

Remote Play – Designed for pet owners, this concept allows users to remotely engage with their pets. It combines joystick input with a gyroscopic ball that moves according to the user’s commands, enabling interactive play from a distance.
[Remote Play] : (https://drive.google.com/file/d/1sIXS5dy5and7Cz--u_Xos0ibYpNgiyjI/view?usp=sharing)

Flashcard Master – Inspired by learning tools like Anki, this concept turns studying into a more tactile experience. Instead of relying solely on buttons, users navigate flashcards using a joystick for a more dynamic learning interaction.
[Flashcard Master] : (https://drive.google.com/file/d/1wz6ATxtC0zEuNmIWsmjTSR9pP1zadzyh/view?usp=drive_link)

Store Navigator – This concept aims to simplify the grocery shopping experience. The device includes a digital store map and allows users to navigate aisles with a joystick to locate products and check their availability in real time.
[Store Navigator] : (https://drive.google.com/file/d/1pvEFYMG4iJKLgn7pzjw0iWjaMWEAnOdl/view?usp=drive_link)

These sketches raise important design questions:
* How can we incorporate additional sensory modalities beyond visual displays for interaction?
* How can we improve ergonomics for comfort during use?
* How can we make the device accessible to users with different abilities?
* How can we balance ease of use with meaningful user engagement without being overly guided?
After exploring all ideas, we’ve decided to continue developing the AstroClicker!

### Part D

These were the different designs we came up with for the AstroClicker:

- [AstroClicker Prototype 1](https://drive.google.com/file/d/1GMzrRrSL4l3woYrJLccYxwP9jXTAnzeE/view?usp=drive_link)
- [AstroClicker Prototype 2](https://drive.google.com/file/d/1POhscVklZM7njbFUzVe2SEgRM2EXgr6x/view?usp=drive_link)
- [AstroClicker Prototype 3](https://drive.google.com/file/d/18dT1ruhAVcGYKWqsz5goETqhqU517WQv/view?usp=drive_link)
- [AstroClicker Prototype 4](https://drive.google.com/file/d/1ZPfyM4x99vHU8GEfVwlT-O0_deb9U7TR/view?usp=drive_link)
- [AstroClicker Prototype 5](https://drive.google.com/file/d/1_Sv7lQg9gYbljeSBiP8plI4wSDGLTxRU/view?usp=drive_link)

Our initial design decisions (based on Prototype 1) were guided by several key considerations. The device is intended to be handheld, so the joystick should be positioned for comfortable and ergonomic use. The speaker must face the user to ensure clear audio output and prevent sound from being muffled. The Raspberry Pi requires adequate ventilation to avoid overheating, and sufficient space must be reserved for a battery compartment.
  
We then built a cardboard prototype to bring these design choices to life. The prototype incorporates our initial rationale, allowing us to physically test proportions, placement, and usability. For example, we used an Altoids can as a placeholder for the battery, and added a top cutout to represent the ventilation area for the Raspberry Pi.

See below for a video walk-around of the AstroClicker prototype. 
https://drive.google.com/file/d/1idpHfScn5C8fBoOJOxdtHWuUTcjamcaN/view?usp=sharing 

# LAB PART 2

### Part 2

Following exploration and reflection from Part 1, complete the "looks like," "works like" and "acts like" prototypes for your design, reiterated below.

We first started prototyping the software for the AstroClicker prototype, which you can find in the [astro_clicker_demo.py](astro_clicker_demo.py) file. Our main consideration when desigining teh script was that it should be user-friendly without feeling suffocating. After much prototyping, here is the code diagram that we landed on:


### Part E

<details>
#### Chaining Devices and Exploring Interaction Effects

For Part 2, you will design and build a fun interactive prototype using multiple inputs and outputs. This means chaining Qwiic and STEMMA QT devices (e.g., buttons, encoders, sensors, servos, displays) and/or combining with traditional breadboard prototyping (e.g., LEDs, buzzers, etc.).

**Your prototype should:**
- Combine at least two different types of input and output devices, inspired by your physical considerations from Part 1.
- Be playful, creative, and demonstrate multi-input/multi-output interaction.

**Document your system with:**
- Code for your multi-device demo
- Photos and/or video of the working prototype in action
- A simple interaction diagram or sketch showing how inputs and outputs are connected and interact
- Written reflection: What did you learn about multi-input/multi-output interaction? What was fun, surprising, or challenging?

**Questions to consider:**
- What new types of interaction become possible when you combine two or more sensors or actuators?
- How does the physical arrangement of devices (e.g., where the encoder or sensor is placed) change the user experience?
- What happens if you use one device to control or modulate another (e.g., encoder sets a threshold, sensor triggers an action)?
- How does the system feel if you swap which device is "primary" and which is "secondary"?

Try chaining different combinations and document what you discover!

See encoder_accel_servo_dashboard.py in the Lab 4 folder for an example of chaining together three devices.

**`Lab 4/encoder_accel_servo_dashboard.py`**

#### Using Multiple Qwiic Buttons: Changing I2C Address (Physically & Digitally)

If you want to use more than one Qwiic Button in your project, you must give each button a unique I2C address. There are two ways to do this:

##### 1. Physically: Soldering Address Jumpers

On the back of the Qwiic Button, you'll find four solder jumpers labeled A0, A1, A2, and A3. By bridging these with solder, you change the I2C address. Only one button on the chain can use the default address (0x6F).

**Address Table:**

| A3 | A2 | A1 | A0 | Address (hex) |
|----|----|----|----|---------------|
|  0 |  0 |  0 |  0 |    0x6F       |
|  0 |  0 |  0 |  1 |    0x6E       |
|  0 |  0 |  1 |  0 |    0x6D       |
|  0 |  0 |  1 |  1 |    0x6C       |
|  0 |  1 |  0 |  0 |    0x6B       |
|  0 |  1 |  0 |  1 |    0x6A       |
|  0 |  1 |  1 |  0 |    0x69       |
|  0 |  1 |  1 |  1 |    0x68       |
|  1 |  0 |  0 |  0 |    0x67       |
| ...| ...| ...| ... |     ...      |

For example, if you solder A0 closed (leave A1, A2, A3 open), the address becomes 0x6E.

**Soldering Tips:**
- Use a small amount of solder to bridge the pads for the jumper you want to close.
- Only one jumper needs to be closed for each address change (see table above).
- Power cycle the button after changing the jumper.

##### 2. Digitally: Using Software to Change Address

You can also change the address in software (temporarily or permanently) using the example script `qwiic_button_ex6_changeI2CAddress.py` in the Lab 4 folder. This is useful if you want to reassign addresses without soldering.

Run the script and follow the prompts:
```bash
python qwiic_button_ex6_changeI2CAddress.py
```
Enter the new address (e.g., 5B for 0x5B) when prompted. Power cycle the button after changing the address.

**Note:** The software method is less foolproof and you need to make sure to keep track of which button has which address!


##### Using Multiple Buttons in Code

After setting unique addresses, you can use multiple buttons in your script. See these example scripts in the Lab 4 folder:

- **`qwiic_1_button.py`**: Basic example for reading a single Qwiic Button (default address 0x6F). Run with:
    ```bash
    python qwiic_1_button.py
    ```

- **`qwiic_button_led_demo.py`**: Demonstrates using two Qwiic Buttons at different addresses (e.g., 0x6F and 0x6E) and controlling their LEDs. Button 1 toggles its own LED; Button 2 toggles both LEDs. Run with:
    ```bash
    python qwiic_button_led_demo.py
    ```

Here is a minimal code example for two buttons:
```python
import qwiic_button

# Default button (0x6F)
button1 = qwiic_button.QwiicButton()
# Button with A0 soldered (0x6E)
button2 = qwiic_button.QwiicButton(0x6E)

button1.begin()
button2.begin()

while True:
        if button1.is_button_pressed():
                print("Button 1 pressed!")
        if button2.is_button_pressed():
                print("Button 2 pressed!")
```

For more details, see the [Qwiic Button Hookup Guide](https://learn.sparkfun.com/tutorials/qwiic-button-hookup-guide/all#i2c-address).

---

### PCF8574 GPIO Expander: Add More Pins Over I²C

Sometimes your Pi’s header GPIO pins are already full (e.g., with a display or HAT). That’s where an I²C GPIO expander comes in handy.

We use the Adafruit PCF8574 I²C GPIO Expander, which gives you 8 extra digital pins over I²C. It’s a great way to prototype with LEDs, buttons, or other components on the breadboard without worrying about pin conflicts—similar to how Arduino users often expand their pinouts when prototyping physical interactions.

**Why is this useful?**
- You only need two wires (I²C: SDA + SCL) to unlock 8 extra GPIOs.
- It integrates smoothly with CircuitPython and Blinka.
- It allows a clean prototyping workflow when the Pi’s 40-pin header is already occupied by displays, HATs, or sensors.
- Makes breadboard setups feel more like an Arduino-style prototyping environment where it’s easy to wire up interaction elements.

**Demo Script:** `Lab 4/gpio_expander.py`

<p align="center">
    <img src="gpio_leds.gif" alt="GPIO Expander LED Demo" width="400"/>
</p>

We connected 8 LEDs (through 220 Ω resistors) to the expander and ran a little light show. The script cycles through three patterns:
- Chase (one LED at a time, left to right)
- Knight Rider (back-and-forth sweep)
- Disco (random blink chaos)

Every few runs, the script swaps to the next pattern automatically:
```bash
python gpio_expander.py
```

This is a playful way to visualize how the expander works, but the same technique applies if you wanted to prototype buttons, switches, or other interaction elements. It’s a lightweight, flexible addition to your prototyping toolkit.

---

### Servo Control with SparkFun Servo pHAT
For this lab, you will use the **SparkFun Servo pHAT** to control a micro servo (such as the Miuzei MS18 or similar 9g servo). The Servo pHAT stacks directly on top of the Adafruit Mini PiTFT (135×240) display without pin conflicts:
- The Mini PiTFT uses SPI (GPIO22, 23, 24, 25) for display and buttons ([SPI pinout](https://pinout.xyz/pinout/spi)).
- The Servo pHAT uses I²C (GPIO2 & 3) for the PCA9685 servo driver ([I2C pinout](https://pinout.xyz/pinout/i2c)).
- Since SPI and I²C are separate buses, you can use both boards together.
**⚡ Power:**
- Plug a USB-C cable into the Servo pHAT to provide enough current for the servos. The Pi itself should still be powered by its own USB-C supply. Do NOT power servos from the Pi’s 5V rail.

<p align="center">
    <img src="Servo_pHAT.gif" alt="Servo pHAT Demo" width="400"/>
</p>

**Basic Python Example:**
We provide a simple example script: `Lab 4/pi_servo_hat_test.py` (requires the `pi_servo_hat` Python package).
Run the example:
```
python pi_servo_hat_test.py
```
For more details and advanced usage, see the [official SparkFun Servo pHAT documentation](https://learn.sparkfun.com/tutorials/pi-servo-phat-v2-hookup-guide/all#resources-and-going-further).
A servo motor is a rotary actuator that allows for precise control of angular position. The position is set by the width of an electrical pulse (PWM). You can read [this Adafruit guide](https://learn.adafruit.com/adafruit-arduino-lesson-14-servo-motors/servo-motors) to learn more about how servos work.
</details>

Software: The AstroClicker software (see astro_clicker_demo.py) was made to create something that felt natural and intuitive to use—we didn't want it to feel clunky or confusing. We went through several rounds of prototyping and tweaking before landing on this structure. The script imports all the libraries we need to control hardware, handle timing, run shell commands, and parse arguments. We built a speak_text function that uses the espeak program for text-to-speech and logs everything to the console no matter which mode you're running in (speaker or silent). We organized the celestial data into three layers based on distance from Earth:
- Layer 0 (Closest): Constellations
- Layer 1 (Middle): Solar System objects
- Layer 2 (Farthest): Deep space objects


The SkyNavigator class is basically the brain of the program. It keeps track of (1) what layer you're currently on (you start at Layer 1 with the Solar System), (2) which objects you've already seen using an unseen_targets list. 

The _set_new_target() method picks a random object from your current layer. Once you've seen everything on a layer, it resets so you can explore it all over again.
The move(direction) method handles what happens when you move the joystick:
- 'up' / 'down': Zooms you in or out to a different layer, with safeguards to keep you from going too far in either direction
 'left' / 'right': Keeps you on the same layer but picks a new random target to look at
Whenever you make a move, the system tells you out loud where you are and what you're looking at.
  
The Main Loop: The runExample function gets everything set up—it starts the joystick, initializes the SkyNavigator, gives you a welcome message, and announces your first target.
IOt then runs an infinite loop that's constantly listening to your joystick. It checks which direction you're pushing it (x and y values) and whether you've clicked the button. To prevent accidental double-inputs, there's a debounce timer that gives you a little buffer between actions.
Here's what each action does:

To run the program, the main() function uses argparse to let you choose your output mode when you start the script—either --mode speaker for audio or --mode silent for text only. Exit by hitting Ctrl+C.

Click the Button: Stays on current target; the system reads the object's name and a fun fact, then asks what you want to do next.
Push Up (Y > 600): Zooms out farther; announces the zoom-out, then the new target's name and type. 
Push Down (Y < 400): Zooms in closer; announces the zoom-in, then the new target's name and type.
Push Left (X > 600): Scans to a new target; announces the scan left, then the new target's name and type.
Push Right (X < 400): Scans to a new target; announces the scan right, then the new target's name and type. 

See here: 
https://drive.google.com/file/d/1H_HfMfHKVElFFgs2zY64mGC1QpVSKP85/view?usp=sharing

Hardware: The joystick needs to be positioned so you can use it naturally while holding the device and the speaker has to face toward you so the audio comes through clearly and doesn't sound muffled. Also, the Raspberry Pi needs good airflow to stay cool, and we had to leave room for the battery. These priorities were similar to our cardboard prototype, but we made some refinements to make the final version more comfortable and practical to actually use.

Sees picture here: 
- https://drive.google.com/file/d/1tifWxaHYtIfDRb2sIJ8nEL6bgSCLxXfo/view?usp=sharing 
- https://drive.google.com/file/d/1e8HCZ9sC3PpO5cFvTWhEP0yuUrxE6XEE/view?usp=sharing
- https://drive.google.com/file/d/1RwBOhzYwkkrttk4ce2GzSumDK7BMUCWM/view?usp=sharing

### Part F

### Record
See here for video: https://drive.google.com/file/d/1H3ZmqcTg181csqCr8ORDpRanjS9P935U/view?usp=sharing

AI Contributions: Gemini was used with:
- Taking our rough paper sketches and turning them into polished images we could actually use
- Writing and organizing the code for the prototype

Coming up with ideas, gathering feedback, and actually designing and building was done by out team ourselves.
