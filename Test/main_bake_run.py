import pygame
import sys
import utils
import time

# Initialize Pygame
pygame.init()
font = pygame.font.SysFont(None, 28)

# Set up display
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D N-Body Gravity Simulation (Baked)")

# --- Read baked positions ---
baked_positions = []
print("Loading Baked data from bake_files/bake_data_Two_star_binary.txt")
with open("bake_files/bake_data_Two_star_binary.txt", "r") as file:
    for line in file:
        line = line.strip().rstrip(',')
        if not line:
            continue
        numbers = list(map(float, line.split(',')))
        frame = [(numbers[i], numbers[i+1]) for i in range(0, len(numbers), 2)]
        baked_positions.append(frame)

if not baked_positions:
    print("Error: No baked data found!")
    sys.exit()

num_objects = len(baked_positions[0])
print(f"Loaded {len(baked_positions)} frames with {num_objects} objects each.")

# --- Drawable object class ---
class DrawableObject:
    def __init__(self, color, radius):
        self.color = color
        self.radius = radius
        self.x = 0
        self.y = 0
    def draw(self, surface):
        pygame.draw.circle(surface, self.color, (int(self.x), int(self.y)), self.radius)

# --- Create drawable objects ---
objects = [DrawableObject((255, 0, 0), 50) for _ in range(num_objects)]

# --- Trajectories per object ---
trajectories = [[] for _ in range(num_objects)]

# --- Playback loop ---
clock = pygame.time.Clock()
running = True
frame_index = 0
speed_factor = 100  # Increase to skip frames

SCALE = 1
OFFSET_X = 0
OFFSET_Y = 0

start_time = time.time()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill((0, 0, 0))

    if frame_index < len(baked_positions):
        frame = baked_positions[frame_index]
        
        # First, update positions and store in trajectories
        for idx, (obj, pos) in enumerate(zip(objects, frame)):
            obj.x = pos[0]*SCALE + OFFSET_X
            obj.y = pos[1]*SCALE + OFFSET_Y
            trajectories[idx].append((obj.x, obj.y))
        
        # Draw trajectories first
        for traj in trajectories:
            if len(traj) > 1:
                pygame.draw.lines(screen, (255, 255, 255), False, traj)
        
        # Then draw circles on top
        for obj in objects:
            obj.draw(screen)

        frame_index += speed_factor
    else:
        # Loop playback
        frame_index = 0
        trajectories = [[] for _ in range(num_objects)]

    # --- Display text info ---
    integrator = utils.Text(f"Integrator : Semi-Implicit Euler", 50, 25, font, (255, 255, 255))
    integrator.draw(screen)
    frame_no = utils.Text(f"Frame: {frame_index}", 50, 50, font, (255, 255, 255))
    frame_no.draw(screen)
    speed_text = utils.Text(f"Speed: {speed_factor}X", 50, 75, font, (255, 255, 255))
    speed_text.draw(screen)
    elapsed_time = time.time() - start_time
    timer = utils.Text(f"Time: {elapsed_time:.2f} s", 50, 100, font, (255, 255, 255))
    timer.draw(screen)

    pygame.display.flip()
    #clock.tick(60)  # Play at 60 FPS
print("Simulation Ended!")
pygame.quit()
sys.exit()
