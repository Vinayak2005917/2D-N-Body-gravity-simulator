import pygame
import Object
import sys
import time
import Object_systems
import utils

# Initialize Pygame
pygame.init()
font = pygame.font.SysFont(None, 28)

# Set up display
WIDTH, HEIGHT =1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D N-Body Gravity Simulation")


#Objects
Objects_List = Object_systems.Two_binary_stars()

# Main loop
clock = pygame.time.Clock()
running = True
dt = 0.001
sim_on = True
skip_frames = 100

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False

	screen.fill((0, 0, 0))  # Fill screen with black

	# ...draw/update simulation here...
	if sim_on:
		for _ in range(skip_frames):
			for obj in Objects_List:
				obj.acceleration_x = 0
				obj.acceleration_y = 0
			
		for i in Objects_List:
			i.draw(screen)
			for j in Objects_List:  
				if i != j:
					i.apply_gravity_on(j, dt=dt)
					i.check_collision_bounce(j)
			i.update_velocity(dt=dt)
			i.update_position(dt=dt)
	else:
		for i in Objects_List:
			i.draw(screen)
	
    
	for i in range(0,2):
		Obj1_vel = utils.Text(f"Object {i} velocity : {abs(Objects_List[i].velocity_x):.2f} km/s", 50, 50+(i*20), font, (255, 255, 255))
		Obj1_vel.draw(screen)

	pygame.display.flip()
	#clock.tick(60)  # Limit to 60 FPS

pygame.quit()
sys.exit()
