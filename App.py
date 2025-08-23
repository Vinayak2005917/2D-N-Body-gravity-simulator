import pygame
import sys
import utils
import Object
import Object_systems
import time

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basic Pygame Window")
font = pygame.font.SysFont(None, 28)
dt = 0.1


#Object List
Objects_List = []


#start button
add = utils.Button(20, 20, 150, 50, "Add", font, (150,0,0), (200,0,0))
start = utils.Button(20, 80, 150, 50, "Start", font, (0,150,0), (0,200,0))
reset = utils.Button(20, 140, 150, 50, "Reset", font, (0,0,150), (0,0,200))

sim_state = False
start_time = time.time()
# Main loop
clock = pygame.time.Clock()
running = True
while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if add.is_clicked(event.pos, (1,0,0)):  # fake tuple since we're not checking pressed[]
				Objects_List.append(Object.Physics_Object(
					x_position=WIDTH//2 - 100,
					y_position=HEIGHT//2,
					velocity_x=0,
					velocity_y=0,
					radius=35,
					mass=8000
				))

			if start.is_clicked(event.pos, (1,0,0)):
				sim_state = True
				start_time = time.time()
			if reset.is_clicked(event.pos, (1,0,0)):
				Objects_List.clear()
				start_time = time.time()
				sim_state = False
	screen.fill((0, 0, 0))

	add.draw(screen, pygame.mouse.get_pos())
	start.draw(screen, pygame.mouse.get_pos())
	reset.draw(screen, pygame.mouse.get_pos())
	
	for obj in Objects_List:
		obj.handle_event(event)
		
	for i in Objects_List:
		i.draw(screen)

	

	if sim_state:
		for obj in Objects_List:
			obj.acceleration_x = 0
			obj.acceleration_y = 0
		for i in Objects_List:
			for j in Objects_List:
				if i != j:
					i.apply_gravity_on(j, dt=dt)
					i.check_collision_bounce(j)
			i.update_velocity(dt=dt)
			i.update_position(dt=dt)
		
	for i in range(0,len(Objects_List)):
		Obj1_vel = utils.Text(f"Object {i} velocity : {abs(Objects_List[i].velocity_x):.2f} km/s", 800, 20+(i*25), font, (255, 255, 255))
		Obj1_vel.draw(screen)
	sim_state_info = utils.Text(f"Simulation running : {sim_state}", 200, 20, font, (255, 255, 255))
	sim_state_info.draw(screen)
	integrator = utils.Text(f"Integrator : Semi-Implicit Euler", 200, 45, font, (255, 255, 255))
	integrator.draw(screen)
	
	if sim_state:
		elapsed_time = time.time() - start_time
		timer = utils.Text(f"Time: {elapsed_time:.2f} s", 200, 70, font, (255, 255, 255))
		timer.draw(screen)




	pygame.display.flip()
	clock.tick(60)  # Limit to 60 FPS
pygame.quit()
sys.exit()