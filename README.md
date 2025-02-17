# MIDI Piano Physics Simulation

## Demo
Here's a demo of the simulation:

![MIDI Simulation Demo](demo.gif)

*Note: The framerate in the demo gif is low due to the limitations of gif encoding.*

This project visualizes MIDI input from a digital piano keyboard in real-time and simulates physics using Pygame and Pymunk. Each of the 88 keys on the MIDI keyboard is mapped to one of the rectangles at the top of the screen, where each rectangle represents a key on the virtual keyboard and lights up when the corresponding MIDI note is played. When a note is played, a ball will appear and fall according to gravity, with the ball's radius based on the note's intensity. Notes with more intensity will create balls with a large radius. Holding the sustain pedal causes gravity to stop.

## Features
- **MIDI Input**: The game listens for MIDI messages and reacts accordingly. When a note is played, a ball appears with a size corresponding to the note's intensity.
- **Gravity Control**: The gravity in the game can be toggled using a sustain pedal.
- **Ball Fade Out**: Balls fade out after a short time, simulating the "decay" of a note. 

## Controls
- **Press any key on the MIDI keyboard**: Plays a note and spawns a ball that falls with gravity.
- **Press `r` on the keyboard**: Resets the game, clearing all balls and resetting the key count.
- **Sustain Pedal (MIDI control change 64)**: Toggles gravity off when held down, making the balls float. Releasing the pedal restores normal gravity.

## Setup Instructions

### Requirements
- Python 3.x
- Pygame
- Pymunk
- Mido (for MIDI handling)

### Installation
1. Install Python dependencies:

```bash
pip install pygame pymunk mido
```

2. Clone the repository:
```bash
git clone https://github.com/yourusername/midivisualizer.git cd midivisualizer
```

3. Run the program:
```bash
python midi_vis.py
```
### MIDI Setup
The game uses the first available MIDI input device. Make sure your MIDI keyboard or controller is connected before starting the game.

## How it Works

1. **Pygame**: The graphical interface is powered by Pygame. It handles the rendering of the keyboard, balls, and background, as well as processing user input from the keyboard.
2. **Pymunk**: The physics engine used to simulate the movement and interaction of the balls. Balls are affected by gravity, and their size is based on the MIDI note intensity.
3. **Mido**: Mido is used to handle the MIDI input and send messages to control the behavior of the balls.

## Code Breakdown

- **Ball Class**: Each ball represents a MIDI note. The ball's radius is proportional to the intensity of the note (velocity). Balls are created when a `note_on` message is received and are removed after a set time (simulating note decay).
- **Pymunk Physics**: The balls are affected by gravity, with the option to turn gravity off when the sustain pedal is pressed.
- **Title Screen**: A title screen is shown at the start, where users can begin the game by pressing any key.

## Customization

- **Gravity**: You can adjust the gravity by changing the `GRAVITY` constant.
- **Key Count**: The game uses 88 keys, but you can adjust this by modifying the `KEYS` constant.
- **Ball Size**: You can adjust the maximum size of the balls by tweaking the `self.radius` formula in the `Ball` class.
