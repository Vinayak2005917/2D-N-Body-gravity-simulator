import pygame
import sys
import utils
import Object
import Object_systems
import time
import bake
import arrow
import math
import random
import asyncio
import os

# Initialize Pygame
pygame.init()

# Asset loading functions for Pygbag compatibility
async def load_assets():
    """
    Async asset loading for browser compatibility with Pygbag.
    
    Place your assets in an 'assets/' folder in the same directory as main.py:
    - assets/images/  (for image files)
    - assets/fonts/   (for font files)
    - assets/sounds/  (for audio files)
    
    This function loads assets asynchronously to prevent browser freezing.
    """
    assets = {}
    
    # Check if assets directory exists
    assets_dir = "assets"
    if os.path.exists(assets_dir):
        # Load fonts asynchronously
        font_dir = os.path.join(assets_dir, "fonts")
        if os.path.exists(font_dir):
            # Example: assets['custom_font'] = pygame.font.Font("assets/fonts/custom.ttf", 30)
            pass
        
        # Load images asynchronously
        image_dir = os.path.join(assets_dir, "images")
        if os.path.exists(image_dir):
            # Example: assets['background'] = pygame.image.load("assets/images/background.png")
            pass
        
        # Yield control to browser after each asset load operation
        await asyncio.sleep(0)
    
    return assets

# Set up display
WIDTH, HEIGHT = 1600, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2D N-Body Simulator")
font = pygame.font.SysFont(None, 30)
dt = 0.05
iterations = 1000

# Global variable to store loaded assets
game_assets = {}

#Object List
Objects_List = []
trail_list = []
selected_object_no = None
arrows = []
integrators = ["Semi-Implicit Euler", "Verlet", "RK4"]
presets = ["Custom", "Random", "Three planet system","Four planet system","Small star cluster"]


# button
add = utils.Button(20, 20, 150, 50, "Add", font, (150,0,0), (200,0,0))
start = utils.Button(20, 80, 150, 50, "Start", font, (0,150,0), (0,200,0))
reset = utils.Button(20, 140, 150, 50, "Reset", font, (0,0,150), (0,0,200))
stop = utils.Button(20, 200, 150, 50, "Stop", font, (150,150,0), (200,200,0))
trail_off_on = utils.Button(20, 260, 150, 50, "Trail", font, (50,50,50), (70,70,70))
make_bake = utils.Button(1440,760, 150, 50, "Bake", font, (50,50,50), (70,70,70))
run_bake = utils.Button(1440, 820, 150, 50, "Run Bake", font, (50,50,50), (70,70,70))
delete_obj = utils.Button(20, 530, 90, 45, "Delete", font, (150,0,0), (200,0,0))

#input feilds
iterations_input_box = utils.InputBox(1300, 705, 200, 30)
Apply_iterations = utils.Button(1510, 700, 80, 40, "Apply", font, (50,50,50), (70,70,70))

dt_input_box = utils.InputBox(1300, 655, 200, 30)
Apply_dt = utils.Button(1510, 650, 80, 40, "Apply", font, (50,50,50), (70,70,70))

mass_input_box = utils.InputBox(85, 745, 200, 30)
Apply_mass = utils.Button(300, 740, 80, 40, "Apply", font, (50,50,50), (70,70,70))
vertical_velocity_input_box = utils.InputBox(200, 795, 200, 30)
Apply_vertical_velocity = utils.Button(415, 790, 80, 40, "Apply", font, (50,50,50), (70,70,70))
horizontal_velocity_input_box = utils.InputBox(220, 845, 200, 30)
Apply_horizontal_velocity = utils.Button(435, 840, 80, 40, "Apply", font, (50,50,50), (70,70,70))

# Drop down menu
Integrator_dropdown = utils.DropdownMenu(315, 60, 200, 40, integrators, font)
presets_dropdown = utils.DropdownMenu(1085, 10, #position
									  200, 40, #size
									  presets, 
									  font,
                 					  main_color=(100,100,100), 
									  hover_color=(50,50,50),
                 					  text_color=(255, 255, 255))


#flags
sim_state = False
baked = False
baked_state = False
running = True
temp = 0
baked_positions = []
run_bake_var = False
box_size = 40
stop_var = False
trail_var = True
elapsed_time_frozen = 0.0

# Safely resolve pairwise overlaps by merging after integration,
# avoiding mutations of the object list during iteration.
def resolve_collisions_and_merge(objects):
	n = len(objects)
	if n <= 1:
		return objects

	merged = [False] * n
	new_objects = []

	for i in range(n):
		if merged[i]:
			continue
		base = objects[i]
		for j in range(i + 1, n):
			if merged[j]:
				continue
			other = objects[j]
			dx = base.x_position - other.x_position
			dy = base.y_position - other.y_position
			# Check overlap
			if dx * dx + dy * dy <= (base.radius + other.radius) ** 2:
				# Merge base and other conserving momentum; radius via volume sum
				total_mass = base.mass + other.mass
				if total_mass == 0:
					# Avoid division by zero; keep as tiny mass
					total_mass = 1e-9
				vx = (base.velocity_x * base.mass + other.velocity_x * other.mass) / total_mass
				vy = (base.velocity_y * base.mass + other.velocity_y * other.mass) / total_mass
				new_radius = (base.radius ** 3 + other.radius ** 3) ** (1 / 3)

				# Use base's position and color for the merged object
				base = Object.Physics_Object(
					x_position=base.x_position,
					y_position=base.y_position,
					velocity_x=vx,
					velocity_y=vy,
					radius=new_radius,
					mass=total_mass,
					color=getattr(base, 'color', (255, 0, 0))
				)
				merged[j] = True
		new_objects.append(base)

	return new_objects

# Main async game loop for Pygbag browser compatibility
async def main_game_loop():
    """
    Main async game loop that yields control to the browser to prevent freezing.
    
    The 'await asyncio.sleep(0)' calls are crucial for Pygbag - they allow the
    browser to handle other tasks and prevent the page from becoming unresponsive.
    """
    global game_assets, Objects_List, trail_list, selected_object_no, arrows
    global sim_state, baked, baked_state, running, temp, baked_positions
    global run_bake_var, box_size, stop_var, trail_var, elapsed_time_frozen
    global iterations, dt
    
    # Load assets asynchronously before starting the game
    game_assets = await load_assets()
    
    # Main loop variables
    start_time = time.time()
    clock = pygame.time.Clock()

    while running:
        # Yield control to browser - essential for Pygbag compatibility
        await asyncio.sleep(0)
        
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if Integrator_dropdown.handle_event(event, pygame.mouse.get_pos(), pygame.mouse.get_pressed()) and stop_var:
                drop_down_result = Integrator_dropdown.handle_event(event, pygame.mouse.get_pos(), pygame.mouse.get_pressed())
                Integrator_dropdown.handle_event(event, pygame.mouse.get_pos(), pygame.mouse.get_pressed())

            #when mouse clicks the preset dropdown box
            if presets_dropdown.handle_event(event, pygame.mouse.get_pos(), pygame.mouse.get_pressed()):
                presets_dropdown.handle_event(event, pygame.mouse.get_pos(), pygame.mouse.get_pressed())
                if presets_dropdown.get_selected():
                    if presets_dropdown.get_selected() == "Custom":
                        Objects_List = []
                    elif presets_dropdown.get_selected() == "Random":
                        Objects_List = []
                        for i in range(random.randrange(2, 5)):
                            Objects_List.append(Object.Physics_Object(
                                x_position=random.randrange(100, WIDTH),
                                y_position=random.randrange(200, HEIGHT),
                                velocity_x=random.uniform(-5, 5),
                                velocity_y=random.uniform(-5, 5),
                                radius=random.randrange(20, 100),
                                mass=random.uniform(100, 10000)
                            ))
                            trail_list = [[] for _ in Objects_List]
                    elif presets_dropdown.get_selected() == "Three planet system":
                        Objects_List = (Object_systems.One_star_three_planets())
                        trail_list = [[] for _ in Objects_List]
                    elif presets_dropdown.get_selected() == "Four planet system":
                        Objects_List = (Object_systems.Two_binary_stars_with_two_planets())
                        trail_list = [[] for _ in Objects_List]
                    elif presets_dropdown.get_selected() == "Small star cluster":
                        Objects_List = (Object_systems.One_star_cluster())
                        trail_list = [[] for _ in Objects_List]

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
                    # Start or resume without resetting the timer
                    if not sim_state or stop_var:
                        sim_state = True
                        start_time = time.time() - elapsed_time_frozen
                        stop_var = False
                if reset.is_clicked(event.pos, (1,0,0)):
                    Objects_List.clear()
                    start_time = time.time()
                    sim_state = False
                    baked_state = False
                    stop_var = False
                    elapsed_time_frozen = 0.0
                    temp = 0
                    baked_positions = []
                    selected_object_no = None
                    trail_list.clear()
                if stop.is_clicked(event.pos, (1,0,0)):
                    # Freeze the current elapsed time and pause
                    if sim_state and not stop_var:
                        elapsed_time_frozen = time.time() - start_time
                    stop_var = True
                if delete_obj.is_clicked(event.pos, (1,0,0)) and selected_object_no is not None:
                    Objects_List.pop(selected_object_no)
                    trail_list.pop(selected_object_no)
                    selected_object_no = None
                if make_bake.is_clicked(event.pos, (1,0,0)):
                    baked = True
                    sim_state = False
                if run_bake.is_clicked(event.pos, (1,0,0)):
                    if baked_positions:  # only if something was baked
                        temp = 0
                        run_bake_var = True

                if trail_off_on.is_clicked(event.pos, (1,0,0)):
                    trail_var = not trail_var

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

        # Yield control to browser after event handling
        await asyncio.sleep(0)
        center_x = WIDTH // 2
        center_y = HEIGHT // 2

        # Draw center axes
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(center_x - 1, 0, 2, HEIGHT))  # center vertical
        pygame.draw.rect(screen, (255,255,255), pygame.Rect(0, center_y - 1, WIDTH, 2))  # center horizontal

        # Vertical lines
        vertical_lines = []
        for i in range(-WIDTH // (2*box_size), WIDTH // (2*box_size) + 1):
            pos_x = center_x + i * box_size
            vertical_lines.append(pygame.Rect(pos_x, 0, 1, HEIGHT))

        # Horizontal lines
        horizontal_lines = []
        for j in range(-HEIGHT // (2*box_size), HEIGHT // (2*box_size) + 1):
            pos_y = center_y + j * box_size
            horizontal_lines.append(pygame.Rect(0, pos_y, WIDTH, 1))

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
                if len(trail_list[i]) > 1 and trail_var:
                    pygame.draw.lines(screen, (255, 255, 255), False, trail_list[i])

        if baked:
            # Yield control during intensive baking operations to prevent browser freezing
            await asyncio.sleep(0)
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
            # Yield after baking operations
            await asyncio.sleep(0)
        if baked_state:
            run_bake.draw(screen, pygame.mouse.get_pos())

        for obj in Objects_List:
            obj.handle_event(event)
            
        if not run_bake_var:  # only draw normally if not replaying baked data
            for i in Objects_List:
                i.draw(screen)
        

        # Yield control to browser during physics calculations
        if sim_state and not run_bake_var and not stop_var:
            # Reset accelerations
            for obj in Objects_List:
                obj.acceleration_x = 0
                obj.acceleration_y = 0

            # Accumulate gravitational accelerations (no list mutation here)
            for i in Objects_List:
                for j in Objects_List:
                    if i is not j:
                        i.apply_gravity_on(j, dt=dt)

            # Integrate velocities and positions
            for obj in Objects_List:
                obj.update_velocity(dt=dt)
                obj.update_position(dt=dt)

            # Resolve collisions after integration in a separate pass
            prev_len = len(Objects_List)
            Objects_List = resolve_collisions_and_merge(Objects_List)
            if len(Objects_List) != prev_len:
                selected_object_no = None
                trail_list = [[] for _ in Objects_List]
            
            # Yield after physics calculations to prevent browser freezing
            await asyncio.sleep(0)

        # Arrows
        for i in Objects_List:
            angle = -math.degrees(math.atan2(i.velocity_y, i.velocity_x))

            cx = i.x_position
            cy = i.y_position

            length = (i.velocity_x+i.velocity_y)+60+i.radius
            if length < 0:
                angle += 180
            elif angle > 360:
                angle = 0

            arrows.append(arrow.arrow(x = cx, y = cy, length = length, angle = angle, color = (255, 0, 0)))
        for i in arrows:
            i.draw(screen)


        # Yield control during rendering operations
        if run_bake_var and baked_positions and not stop_var:
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

        # Yield control during UI rendering
        await asyncio.sleep(0)



        sim_state_info = utils.Text(f"Simulation running : {sim_state}", 200, 20, font, (255, 255, 255))
        sim_state_info.draw(screen)
        bake_state_info = utils.Text(f"Baked replay running : {run_bake_var}", 200, 45, font, (255, 255, 255))
        bake_state_info.draw(screen)
        integrator = utils.Text(f"Integrator :", 200, 70, font, (255, 255, 255))
        integrator.draw(screen)
        presets_text = utils.Text(f"Presets:", 1000, 20, font, (255, 255, 255))
        presets_text.draw(screen)

        iterations_input_box.draw(screen)
        if not iterations_input_box.if_selected():
            iterations_input_box.text = f"{iterations}"
            iterations_input_box.txt_surface = font.render(iterations_input_box.text, True, (255,255,255))
        iterations_change = utils.Text(f"Iterations:", 1190, 710, font, (255, 255, 255))
        iterations_change.draw(screen)

        dt_input_box.draw(screen)
        if not dt_input_box.if_selected():
            dt_input_box.text = f"{dt}"
            dt_input_box.txt_surface = font.render(dt_input_box.text, True, (255,255,255))
        dt_change = utils.Text(f"Accuracy(dt):", 1165, 657, font, (255, 255, 255))
        dt_change.draw(screen)



        #If an Object is selected
        if selected_object_no is not None:
            Object_name = utils.Text(f"Object {selected_object_no + 1}", 20, 590, font, (255, 255, 255))
            Object_name.draw(screen)
            Object_x = utils.Text(f"X : {Objects_List[selected_object_no].x_position:.2f}", 20, 620, font, (255, 255, 255))
            Object_x.draw(screen)
            Object_y = utils.Text(f"Y : {Objects_List[selected_object_no].y_position:.2f}", 20, 650, font, (255, 255, 255))
            Object_y.draw(screen)
            Object_radius = utils.Text(f"Radius : {Objects_List[selected_object_no].radius:.2f} Km", 20, 680, font, (255, 255, 255))
            Object_radius.draw(screen)
            Object_density = utils.Text(f"Density : {Objects_List[selected_object_no].mass/Objects_List[selected_object_no].radius**3:.2f} Kg/Km^3", 20, 710, font, (255, 255, 255))
            Object_density.draw(screen)
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

            
            delete_obj.draw(screen, pygame.mouse.get_pos())
            Apply_mass.draw(screen, pygame.mouse.get_pos())
            mass_input_box.draw(screen)

            Apply_vertical_velocity.draw(screen, pygame.mouse.get_pos())
            vertical_velocity_input_box.draw(screen)

            Apply_horizontal_velocity.draw(screen, pygame.mouse.get_pos())
            horizontal_velocity_input_box.draw(screen)

        # Draw timer: when not replaying baked data, show live or frozen time
        if not run_bake_var:
            display_time = (time.time() - start_time) if (sim_state and not stop_var) else elapsed_time_frozen
            timer = utils.Text(f"Time: {display_time:.2f} s", 200, 95, font, (255, 255, 255))
            timer.draw(screen)

        add.draw(screen, pygame.mouse.get_pos())
        start.draw(screen, pygame.mouse.get_pos())
        reset.draw(screen, pygame.mouse.get_pos())
        stop.draw(screen, pygame.mouse.get_pos())
        trail_off_on.draw(screen, pygame.mouse.get_pos())
        make_bake.draw(screen, pygame.mouse.get_pos())
        Apply_iterations.draw(screen, pygame.mouse.get_pos())
        Apply_dt.draw(screen, pygame.mouse.get_pos())

        Integrator_dropdown.draw(screen, pygame.mouse.get_pos())
        presets_dropdown.draw(screen, pygame.mouse.get_pos())

        pygame.display.flip()
        clock.tick(60)  # Limit to 60 FPS
        arrows = []
        
        # Final yield at end of game loop for browser compatibility
        await asyncio.sleep(0)
    
    # Clean up when game loop ends
    pygame.quit()
    sys.exit()

# Run the async game loop
if __name__ == "__main__":
    """
    Entry point for the Pygbag-compatible N-Body simulator.
    
    For Pygbag deployment:
    1. Install pygbag: pip install pygbag
    2. Run with: pygbag main.py
    3. Ensure assets are in an 'assets/' folder structure
    
    The asyncio.run() approach ensures compatibility with both
    desktop Python and the browser WASM environment.
    """
    asyncio.run(main_game_loop())