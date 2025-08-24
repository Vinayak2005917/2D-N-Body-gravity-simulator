import pygame
import sys
import utils
import Object
import Object_systems
import time
import bake

# Initialize Pygame
pygame.init()

# Set up display
WIDTH, HEIGHT = 1080, 720
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basic Pygame Window")
font = pygame.font.SysFont(None, 28)
dt = 0.05
iterations = 1000

#Object List
Objects_List = []


#start button
add = utils.Button(20, 20, 150, 50, "Add", font, (150,0,0), (200,0,0))
start = utils.Button(20, 80, 150, 50, "Start", font, (0,150,0), (0,200,0))
reset = utils.Button(20, 140, 150, 50, "Reset", font, (0,0,150), (0,0,200))
make_bake = utils.Button(20, 200, 150, 50, "Bake", font, (50,50,50), (70,70,70))
run_bake = utils.Button(20, 260, 150, 50, "Run Bake", font, (50,50,50), (70,70,70))

#flags
sim_state = False
baked = False
baked_state = False
running = True
temp = 0
baked_positions = []
run_bake_var = False

# Main loop
start_time = time.time()
clock = pygame.time.Clock()

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
				baked_state = False
				temp = 0
				baked_positions = []
			if make_bake.is_clicked(event.pos, (1,0,0)):
				baked = True
				sim_state = False
			if run_bake.is_clicked(event.pos, (1,0,0)):
				if baked_positions:  # only if something was baked
					temp = 0
					run_bake_var = True


	screen.fill((0, 0, 0))

	add.draw(screen, pygame.mouse.get_pos())
	start.draw(screen, pygame.mouse.get_pos())
	reset.draw(screen, pygame.mouse.get_pos())
	make_bake.draw(screen, pygame.mouse.get_pos())
	if baked:
		bake.clean_bake()
		bake.Bake(Objects_List, dt, iterations=iterations)
		baked_positions = bake.run_bake()
		print("Frames baked:", len(baked_positions))

		# Reset live objects to the first baked frame
		if baked_positions:
			for obj, (x, y) in zip(Objects_List, baked_positions[0]):
				obj.x_position = x
				obj.y_position = y
				obj.velocity_x = 0   # reset velocity too
				obj.velocity_y = 0

		baked = False
		baked_state = True
		temp = 0
	if baked_state:
		run_bake.draw(screen, pygame.mouse.get_pos())

	for obj in Objects_List:
		obj.handle_event(event)
		
	if not run_bake_var:  # only draw normally if not replaying baked data
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

	if run_bake_var and baked_positions:
		frame_no = utils.Text(f"t = {temp} / {len(baked_positions)}", 850, 650, font, (255, 255, 255))
		frame_no.draw(screen)

		# Calculate velocity from baked positions
		velocities = [(0, 0)] * len(Objects_List)
		if temp > 0 and temp < len(baked_positions):
			prev_frame = baked_positions[temp-1]
			curr_frame = baked_positions[temp]
			for idx, (obj, (x, y)) in enumerate(zip(Objects_List, curr_frame)):
				prev_x, prev_y = prev_frame[idx]
				vx = (x - prev_x) / dt
				vy = (y - prev_y) / dt
				velocities[idx] = (vx, vy)
				obj.x_position = x
				obj.y_position = y
				obj.draw(screen)
		elif temp < len(baked_positions):
			for obj, (x, y) in zip(Objects_List, baked_positions[temp]):
				obj.x_position = x
				obj.y_position = y
				obj.draw(screen)
		temp += 1
		if temp >= len(baked_positions):
			run_bake_var = False
			temp = len(baked_positions) - 1

		# Display calculated velocities
		for i in range(len(Objects_List)):
			vx, vy = velocities[i]
			speed = (vx**2 + vy**2)**0.5
			Obj1_vel = utils.Text(f"Object {i+1} velocity : {abs(speed):.2f} km/s", 800, 20+(i*25), font, (255, 255, 255))
			Obj1_vel.draw(screen)
	else:
		for i in range(0,len(Objects_List)):
			Obj1_vel = utils.Text(f"Object {i+1} velocity : {abs(Objects_List[i].velocity_x):.2f} km/s", 800, 20+(i*25), font, (255, 255, 255))
			Obj1_vel.draw(screen)



	sim_state_info = utils.Text(f"Simulation running : {sim_state}", 200, 20, font, (255, 255, 255))
	sim_state_info.draw(screen)
	bake_state_info = utils.Text(f"Baking : {run_bake_var}", 200, 45, font, (255, 255, 255))
	bake_state_info.draw(screen)
	integrator = utils.Text(f"Integrator  :  Semi-Implicit  Euler  at  dt = {dt}", 200, 70, font, (255, 255, 255))
	integrator.draw(screen)

	if sim_state and not run_bake_var:
		elapsed_time = time.time() - start_time
		timer = utils.Text(f"Time: {elapsed_time:.2f} s", 200, 95, font, (255, 255, 255))
		timer.draw(screen)

	pygame.display.flip()
	clock.tick(60)  # Limit to 60 FPS
pygame.quit()
sys.exit()