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
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Basic Pygame Window")
font = pygame.font.SysFont(None, 30)
dt = 0.05
iterations = 1000

#Object List
Objects_List = []
trail_list = []
selected_object_no = None


# button
add = utils.Button(20, 20, 150, 50, "Add", font, (150,0,0), (200,0,0))
start = utils.Button(20, 80, 150, 50, "Start", font, (0,150,0), (0,200,0))
reset = utils.Button(20, 140, 150, 50, "Reset", font, (0,0,150), (0,0,200))
make_bake = utils.Button(20, 200, 150, 50, "Bake", font, (50,50,50), (70,70,70))
run_bake = utils.Button(20, 260, 150, 50, "Run Bake", font, (50,50,50), (70,70,70))

#input feilds
iterations_input_box = utils.InputBox(305, 145, 200, 30)
Apply_iterations = utils.Button(515, 140, 80, 40, "Apply", font, (50,50,50), (70,70,70))
dt_input_box = utils.InputBox(305, 195, 200, 30)
Apply_dt = utils.Button(515, 190, 80, 40, "Apply", font, (50,50,50), (70,70,70))

mass_input_box = utils.InputBox(85, 745, 200, 30)
Apply_mass = utils.Button(300, 740, 80, 40, "Apply", font, (50,50,50), (70,70,70))
vertical_velocity_input_box = utils.InputBox(200, 795, 200, 30)
Apply_vertical_velocity = utils.Button(415, 790, 80, 40, "Apply", font, (50,50,50), (70,70,70))
horizontal_velocity_input_box = utils.InputBox(220, 845, 200, 30)
Apply_horizontal_velocity = utils.Button(435, 840, 80, 40, "Apply", font, (50,50,50), (70,70,70))




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
	screen.fill((0, 0, 0))
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			if add.is_clicked(event.pos, (1,0,0)):  # fake tuple since we're not checking pressed[]
				Objects_List.append(Object.Physics_Object(
					x_position=WIDTH//2,
					y_position=HEIGHT//2,
					velocity_x=0,
					velocity_y=0,
					radius=35,
					mass=8000
				))
				trail_list.append([])

			#finding which object is selected
			for i, obj in enumerate(Objects_List):
				if obj.is_clicked(event.pos):
					selected_object_no = i
					break

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
				selected_object_no = None
				trail_list.clear()
			if make_bake.is_clicked(event.pos, (1,0,0)):
				baked = True
				sim_state = False
			if run_bake.is_clicked(event.pos, (1,0,0)):
				if baked_positions:  # only if something was baked
					temp = 0
					run_bake_var = True

			if Apply_iterations.is_clicked(event.pos, (1,0,0)):
				iterations = int(iterations_input)
			if Apply_dt.is_clicked(event.pos, (1,0,0)):
				dt = float(dt_input)
			if Apply_mass.is_clicked(event.pos, (1,0,0)) and selected_object_no is not None:
				Objects_List[selected_object_no].mass = float(mass_input_box.get_text())
			if Apply_vertical_velocity.is_clicked(event.pos, (1,0,0)) and selected_object_no is not None:
				Objects_List[selected_object_no].velocity_y = float(vertical_velocity_input_box.get_text())
			if Apply_horizontal_velocity.is_clicked(event.pos, (1,0,0)) and selected_object_no is not None:
				Objects_List[selected_object_no].velocity_x = float(horizontal_velocity_input_box.get_text())


		iterations_event = iterations_input_box.handle_event(event)
		iterations_input = iterations_input_box.get_text()

		dt_event = dt_input_box.handle_event(event)
		dt_input = dt_input_box.get_text()

		mass_event = mass_input_box.handle_event(event)
		mass_input = mass_input_box.get_text()

		vertical_velocity_event = vertical_velocity_input_box.handle_event(event)
		vertical_velocity_input = vertical_velocity_input_box.get_text()

		horizontal_velocity_event = horizontal_velocity_input_box.handle_event(event)
		horizontal_velocity_input = horizontal_velocity_input_box.get_text()

	# Grid
	pygame.draw.rect(screen, (255,255,255), pygame.Rect(WIDTH // 2 - 1, 0, 2, HEIGHT))  # center vertical
	pygame.draw.rect(screen, (255,255,255), pygame.Rect(0, HEIGHT // 2 - 1, WIDTH, 2))  # center horizontal

	# Smaller boxes
	box_size = 40

	# Vertical lines
	vertical_lines = []
	edge_offset_x = 0
	edge_offset_y = 10
	for i in range(WIDTH // box_size + 1):
		pos_x = i * box_size
		vertical_lines.append(pygame.Rect(pos_x + edge_offset_x, 0, 1, HEIGHT))

	# Horizontal lines
	horizontal_lines = []
	for i in range(HEIGHT // box_size + edge_offset_y):
		pos_y = i * box_size
		horizontal_lines.append(pygame.Rect(0, pos_y + edge_offset_y, WIDTH, 1))

	# Draw grid
	for line in vertical_lines:
		pygame.draw.rect(screen, (50, 50, 50), line)
	for line in horizontal_lines:
		pygame.draw.rect(screen, (50, 50, 50), line)

	if sim_state:
		for i in range(len(Objects_List)):
			trail_list[i].append((Objects_List[i].x_position, Objects_List[i].y_position))
		for i in range(len(Objects_List)):
			trail_list[i].append((Objects_List[i].x_position, Objects_List[i].y_position))
			if len(trail_list[i]) > 1:
				pygame.draw.lines(screen, (255, 255, 255), False, trail_list[i])

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
		frame_no = utils.Text(f"t = {temp} / {len(baked_positions)}", 200, 95, font, (255, 255, 255))
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
			Obj1_vel = utils.Text(f"Object {i+1} velocity : {abs(speed):.2f} km/s", 1300, 20+(i*25), font, (255, 255, 255))
			Obj1_vel.draw(screen)
	else:
		for i in range(0,len(Objects_List)):
			Obj1_vel = utils.Text(f"Object {i+1} velocity : {abs(Objects_List[i].velocity_x):.2f} km/s", 1300, 20+(i*25), font, (255, 255, 255))
			Obj1_vel.draw(screen)



	sim_state_info = utils.Text(f"Simulation running : {sim_state}", 200, 20, font, (255, 255, 255))
	sim_state_info.draw(screen)
	bake_state_info = utils.Text(f"Baked replay running : {run_bake_var}", 200, 45, font, (255, 255, 255))
	bake_state_info.draw(screen)
	integrator = utils.Text(f"Integrator  :  Semi-Implicit  Euler  at  dt = {dt} and iterations = {iterations}", 200, 70, font, (255, 255, 255))
	integrator.draw(screen)
	iterations_change = utils.Text(f"Iterations:", 200, 150, font, (255, 255, 255))
	iterations_change.draw(screen)
	dt_change = utils.Text(f"dt:", 275, 200, font, (255, 255, 255))
	dt_change.draw(screen)

	if selected_object_no is not None:
		# --- Sync input boxes with object if not actively editing ---
		selected_obj = Objects_List[selected_object_no]
		if not mass_input_box.if_selected():
			mass_input_box.text = f"{selected_obj.mass:.2f}"
			mass_input_box.txt_surface = font.render(mass_input_box.text, True, (255,255,255))
		if not vertical_velocity_input_box.if_selected():
			vertical_velocity_input_box.text = f"{selected_obj.velocity_y:.2f}"
			vertical_velocity_input_box.txt_surface = font.render(vertical_velocity_input_box.text, True, (255,255,255))
		if not horizontal_velocity_input_box.if_selected():
			horizontal_velocity_input_box.text = f"{selected_obj.velocity_x:.2f}"
			horizontal_velocity_input_box.txt_surface = font.render(horizontal_velocity_input_box.text, True, (255,255,255))
		mass_text = utils.Text(f"Mass:", 20, 750, font, (255, 255, 255))
		mass_text.draw(screen)
		if not mass_input_box.if_selected():
			mass_value = utils.Text(f"{Objects_List[selected_object_no].mass:.2f}", 90, 750, font, (255, 255, 255))
			mass_value.draw(screen)

		vertical_velocity_text = utils.Text(f"Vertical Velocity:", 20, 800, font, (255, 255, 255))
		vertical_velocity_text.draw(screen)
		if not vertical_velocity_input_box.if_selected():
			vertical_velocity_value = utils.Text(f"{Objects_List[selected_object_no].velocity_y:.2f}", 205, 800, font, (255, 255, 255))
			vertical_velocity_value.draw(screen)

		horizontal_velocity_text = utils.Text(f"Horizontal Velocity:", 20, 850, font, (255, 255, 255))
		horizontal_velocity_text.draw(screen)
		if not horizontal_velocity_input_box.if_selected():
			horizontal_velocity_value = utils.Text(f"{Objects_List[selected_object_no].velocity_x:.2f}", 225, 850, font, (255, 255, 255))
			horizontal_velocity_value.draw(screen)

		Apply_mass.draw(screen, pygame.mouse.get_pos())
		mass_input_box.draw(screen)

		Apply_vertical_velocity.draw(screen, pygame.mouse.get_pos())
		vertical_velocity_input_box.draw(screen)

		Apply_horizontal_velocity.draw(screen, pygame.mouse.get_pos())
		horizontal_velocity_input_box.draw(screen)

	if sim_state and not run_bake_var:
		elapsed_time = time.time() - start_time
		timer = utils.Text(f"Time: {elapsed_time:.2f} s", 200, 95, font, (255, 255, 255))
		timer.draw(screen)

	add.draw(screen, pygame.mouse.get_pos())
	start.draw(screen, pygame.mouse.get_pos())
	reset.draw(screen, pygame.mouse.get_pos())
	make_bake.draw(screen, pygame.mouse.get_pos())
	Apply_iterations.draw(screen, pygame.mouse.get_pos())
	Apply_dt.draw(screen, pygame.mouse.get_pos())

	iterations_input_box.draw(screen)
	dt_input_box.draw(screen)


	pygame.display.flip()
	clock.tick(60)  # Limit to 60 FPS
pygame.quit()
sys.exit()