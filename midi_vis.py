import time
import pygame
import mido
import random
import pymunk
import pymunk.pygame_util
from title_screen import show_title_screen


# ─────────────────── Constants, change these if you'd like ─────────────────── #
FRAMERATE = 144
WIDTH, HEIGHT = 1760, 880
KEYS = 88
SECTION_WIDTH = WIDTH // KEYS
GRAVITY = 900
BOUNCE_DAMPING = 0.7
KEY_TOP_HEIGHT = 5
TIME_TO_FADE = 120
SEGMENT_ELASTICITY = 0.95
SEGMENT_FRICTION = 0.0
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

# ─────────────────── Pygame + Pymunk Setup ─────────────────── #
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
draw_options = pymunk.pygame_util.DrawOptions(screen)
font = pygame.font.Font(None, 36)

space = pymunk.Space()
space.gravity = (0, GRAVITY)

floor = pymunk.Segment(space.static_body, (0, HEIGHT), (WIDTH, HEIGHT), 20)
floor.elasticity = SEGMENT_ELASTICITY
floor.friction = SEGMENT_FRICTION
space.add(floor)

right_wall = pymunk.Segment(space.static_body, (WIDTH, 0), (WIDTH, HEIGHT), 20)
right_wall.elasticity = SEGMENT_ELASTICITY
right_wall.friction = SEGMENT_FRICTION
space.add(right_wall)

left_wall = pymunk.Segment(space.static_body, (0, 0), (0, HEIGHT), 20)
left_wall.elasticity = SEGMENT_ELASTICITY
left_wall.friction = SEGMENT_FRICTION
space.add(left_wall)

# ─────────────────── Midi Setup ─────────────────── #
midi_inputs = mido.get_input_names()
if not midi_inputs:
    print("No MIDI input devices found.")
    exit()
port = mido.open_input(midi_inputs[0])

# ─────────────────── Keys Setup ─────────────────── #
keys = [pygame.Rect(i * SECTION_WIDTH, 0, SECTION_WIDTH, HEIGHT) for i in range(KEYS)]
active_keys = {}
keys_to_color = {
    i: (random.randint(50, 255), random.randint(50, 255), random.randint(50, 255))
    for i in range(KEYS)
}


class Ball:
    def __init__(self, x, key, noteIntensity):
        self.radius = 1 + int((noteIntensity / 127) * 15)
        self.color = keys_to_color[key]
        self.created_time = time.time()

        mass = self.radius**2
        moment = pymunk.moment_for_circle(mass, 0, self.radius)

        self.body = pymunk.Body(mass, moment)
        self.body.position = (x + random.randint(0, SECTION_WIDTH), 10)
        self.body.velocity = (random.uniform(-50, 50), 0)

        self.shape = pymunk.Circle(self.body, self.radius)
        self.shape.elasticity = ELASTICITY
        self.shape.friction = FRICTION

        space.add(self.body, self.shape)

    def draw(self):
        age = time.time() - self.created_time
        if age >= TIME_TO_FADE:
            space.remove(self.body, self.shape)
            balls.remove(self)
            return

        fade_factor = max(0, 1 - (age / TIME_TO_FADE))

        faded_color = (
            int(self.color[0] * fade_factor),
            int(self.color[1] * fade_factor),
            int(self.color[2] * fade_factor),
        )

        pos = int(self.body.position.x), int(self.body.position.y)
        pygame.draw.circle(screen, faded_color, pos, self.radius)


# ─────────────────── Mutable Variables ─────────────────── #
balls = []
pedal_held = False
total_keys_pressed = 0

# ─────────────────── Title Screen ─────────────────── #
started, ELASTICITY, FRICTION = show_title_screen(screen)

# ─────────────────── Main Game Loop ─────────────────── #
running = True
while started and running:
    screen.fill(BLACK)

    for msg in port.iter_pending():
        if msg.type == "note_on" and msg.velocity > 0:
            key = msg.note - 21
            if 0 <= key < KEYS:
                active_keys[key] = True
                balls.append(Ball(keys[key].x, key, msg.velocity))
                total_keys_pressed += 1
        elif msg.type == "note_off" or (msg.type == "note_on" and msg.velocity == 0):
            key = msg.note - 21
            active_keys.pop(key, None)
        elif msg.type == "control_change" and msg.control == 64:
            pedal_held = msg.value > 0
            space.gravity = (0, 0 if pedal_held else GRAVITY)

    for i, rect in enumerate(keys):
        if i in active_keys:
            pygame.draw.rect(screen, GREEN, rect, 0)
        pygame.draw.rect(
            screen, keys_to_color[i], (rect.x, rect.y, rect.width, KEY_TOP_HEIGHT)
        )

    for ball in balls[:]:
        ball.draw()

    keys_pressed_text = font.render(
        f"Total Keys Pressed: {total_keys_pressed}", True, WHITE
    )
    text_width, text_height = keys_pressed_text.get_size()
    screen.blit(keys_pressed_text, (WIDTH - text_width - 20, 20))
    pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                balls = []
                total_keys_pressed = 0
                print("Reset!")

    space.step(1 / FRAMERATE)
    clock.tick(FRAMERATE)

pygame.quit()
