# Distributed Interaction

**NAMES OF COLLABORATORS HERE**
Nana Takada, Celeste (Lianne) Bisch, Jaspreet Lal

---

## Prep

1. Pull the new changes
2. Read: [The Presence Table](https://dl.acm.org/doi/10.1145/1935701.1935800) ([video](https://vimeo.com/15932020))

## Overview

Build interactive systems where **multiple devices communicate over a network** using MQTT messaging. Work in teams of 3+ with Raspberry Pis.

**Parts:**
- A: Learn MQTT messaging
- B: Try collaborative pixel grid demo  
- C: Build your own distributed system

---

## Part A: MQTT Messaging

**💡 Brainstorm 5 ideas for messaging between devices**

1. Client Input Topics (Game Control)This is the primary communication path for gameplay. Each Raspberry Pi client publishes its joystick and shooting state to a unique, player-specific topic (e.g., game/player1/input). The message payload is a small, efficient package containing the $(x, y)$ coordinates and the current shoot status. The central Server subscribes to all four of these topics to capture all player actions simultaneously, making it the most direct and critical application of MQTT for low-latency game control.

2. Server State Topics (Display Updates)The central Server must broadcast the updated game state so the Screen component can render it. The Server publishes real-time game data—including all player and bullet positions, and current health values—to a single topic, such as game/state/updates. If the screen were a separate device, it would subscribe here. This mechanism efficiently pushes thousands of updates per second, ensuring the visual feedback is instant and synchronized across all game elements.

3. Health/Scoreboard EventsInstead of mixing constant movement updates with discrete events, a dedicated topic like game/event/hit handles specific, important occurrences. When a hit or a game-over condition occurs, the Server publishes a message identifying the source and target players and the resulting health change. This decouples event logging and secondary displays (like a scoreboard or a persistent logging service) from the main, high-frequency game loop, allowing them to subscribe only when meaningful state changes happen.

4. Game Setup and ConfigurationA command topic, such as game/control/command, is essential for managing the project lifecycle. The Server can publish simple command strings (e.g., "START_ROUND", "RESET_HARDWARE") to this topic. All Raspberry Pi clients can subscribe to this central command stream, ensuring that every device in the distributed system starts, stops, or resets its software and hardware in perfect synchronization before a new match begins.

5. Client Health/Status ReportingTo ensure a game starts fairly, the Server needs to confirm all four clients are ready. Each Raspberry Pi can periodically publish its operational status (e.g., "READY", "OFFLINE", or "RESTARTING") to a specific status topic (e.g., system/client/player2/status). The Server subscribes using a wildcard (system/client/#/status) to monitor the health of the entire input system, preventing the game from beginning if any player's control unit is not fully functional.

---

## Part B: Collaborative Pixel Grid

**📸 Include: Screenshot of grid + photo of your Pi setup**
Image here: https://drive.google.com/file/d/1gsUKeRz6Bl3dkYpZF5xujZkaf2TWNmDG/view?usp=sharing
---

## Part C: Make Your Own
**1. Project Description**
- What does it do? Why interesting? User experience?
Our project is a multiplayer shooting game that uses Raspberry Pis connected to joysticks for real-time control. Players join one of two teams—left or right—and can move freely within their team’s area. Each player begins with three lives, and getting hit three times results in elimination. The match continues until all players on one team are eliminated, ending the game.

Each Raspberry Pi is assigned a unique identifier (e.g., game/player1) and publishes its joystick data—tilt movements for direction and button clicks for shooting—through MQTT. The server receives these messages, interprets each player’s position and actions, and updates the shared game state accordingly.

**2. Architecture Diagram**
See diagram here: https://drive.google.com/file/d/1shzHTsd6wPaJoC5EQLJPGhPGuqQOk8f2/view?usp=sharing

**3. Build Documentation**
- Photos of each Pi + sensors
- https://drive.google.com/file/d/1t-SQIwAuWOKSZGCJERDcNbRNdrBR1R12/view?usp=sharing
- https://drive.google.com/file/d/1dQxroKectK99O5K4UOnOnNuJ-6b2VyCO/view?usp=sharing


- MQTT topics used: game/player1, game/player2, game/player3, game/player4

This project is a four-player canvas-based shooting game that connects physical joysticks to on-screen action through MQTT and Socket.IO. Each player controls a colored character on the browser, moving and shooting based on live joystick input. The game’s client listens to joystick updates from the server, which relays MQTT messages containing joy_x, joy_y, and shoot values. These inputs are mapped to target positions on the canvas—players move smoothly within their assigned half of the screen while staying within the canvas bounds. When a joystick payload includes shoot: true, a bullet is spawned in the player’s direction. Each frame, bullets update their position, collisions are checked, and hits are registered. A player loses after being hit three times, and the first to knock out their opponent wins the round.

The game loop runs continuously with requestAnimationFrame, updating player movement, bullet trajectories, and collision logic while keeping the DOM updates minimal. The interface displays health bars and hit counters beneath each player’s card, and when the game ends, an overlay announces the winner with an option to restart. Communication between server and client is handled through Socket.IO events—mqtt_message delivers joystick data from the server to the browser, and restart_game resets the session. To run the game, set up a virtual environment, install dependencies, and launch both the server and joystick scripts. Once active, players can connect via a browser at http://0.0.0.0:5002 to engage in a fast-paced, real-time multiplayer match powered by live hardware input.

Final game video: https://drive.google.com/file/d/1vukRjIqbEwK9VQyV1kWV49HtCRFkoGgR/view?usp=sharing

**4. User Testing**
- **Test with 2+ people NOT on your team**
- Photos/video of use
- What did they think before trying?
- What surprised them?
- What would they change?

**5. Reflection**
- What worked well?
Decoupled Architecture: Using MQTT as an event bus created clear boundaries: joystick.py (read and published hardware input), game_server.py (managed messaging and player/bot states), and game.html (handled rendering and events). This made the system modular and reliable.

AI Bot Takeover: The 5-second timeout and auto bot replacement worked perfectly, keeping gameplay smooth even if a player’s Pi crashed or disconnected.

Real-Time Feel: MQTT + Socket.IO provided low latency. Small JSON payloads and client-side smoothing made controls responsive.

- Challenges with distributed interaction?
Player Disconnection: Since disconnects sent no signal, a heartbeat system detected drop-offs and triggered AI replacements.
Latency: The long path (Pi → MQTT → Server → Browser) risked lag, but minimal payloads kept it manageable.
State Management: With the browser holding the “true” state, syncing could be tricky. A server-driven model would be more consistent.
- How did sensor events work?
The joystick script continuously reads raw input data, normalizes the X and Y values to a -1.0 to 1.0 range, and detects button press transitions to trigger single “shoot” events. It then packages this data into a JSON payload and publishes it to the player’s MQTT topic (e.g., IDD/game/player#).
- What would you improve?
Authoritative Server: Move game logic to the server for consistency and fairness.
Smarter Bots: Add strategy—aiming, dodging, team tactics.
Team Play: Change win logic to “last team standing.”

6. Distribution of Work

Nana worked on the server code on game folder for two players game. 
Celest worked on the controller code on game folder. 
Iqra worked on modifying the server code to the multiple players game. 
Jaspreet worked on documentation & troubleshooting hardware issues. 

**AI/Team Contributions**
Gemini supported this project, particularly during the initial ideation and documentation phases. It was helped refine the visual assets (including the sketch and architecture diagram), and assisting with code development. All team members actively participated in both the ideation and software development stages.
All team members helped in both the ideation and software development stages of this project.

Resources: [MQTT Guide](https://www.hivemq.com/mqtt-essentials/) | [Paho Python](https://www.eclipse.org/paho/index.php?page=clients/python/docs/index.php) | [Flask-SocketIO](https://flask-socketio.readthedocs.io/)
