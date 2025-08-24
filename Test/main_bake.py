import Object
import Object_systems
import sys
import time

# --- Simulation parameters ---
Objects_List = Object_systems.Two_binary_stars()
iterations = 1000000
done = 0
dt = 0.001
G = 1

q = input("DO you want to delete the current bake (Y/N) : ")
if q.lower() == 'y':
    # Clean the bake file
    with open("bake_files/bake_data_Two_star_binary.txt", "w") as file:
        file.write("")
        print("Cleaning the file...")
        time.sleep(5)
    print("Cleaned the bake file.")
else:
    sys.exit()

# Main baking loop
for _ in range(iterations):
    for obj in Objects_List:
        obj.acceleration_x = 0
        obj.acceleration_y = 0
    for i in Objects_List:
        for j in Objects_List:
            if i != j:
                i.apply_gravity_on(j, dt=dt)


    for obj in Objects_List:
        obj.update_velocity(dt=dt)
        obj.update_position(dt=dt)

    for i in Objects_List:
        for j in Objects_List:
            if i != j:
                i.check_collision_bounce(j)


    with open("bake_files/bake_data_Two_star_binary.txt", "a") as file:
        line = ",".join(f"{obj.x_position},{obj.y_position}" for obj in Objects_List)
        file.write(line + "\n")

    done += 1
    if done % 1000 == 0:
        print(f"{done}/{iterations} Iterations complete.")

print("Baking complete! Positions saved to bake bake_files/bake_data_Two_star_binary.txt")
