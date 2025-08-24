import time
import pygame
import utils
font = pygame.font.SysFont(None, 28)
import copy

def clean_bake():
    with open("temp_bake.txt", "w") as file:
        file.write("")
        time.sleep(0.5)				

def Bake(Objects_List, dt, iterations=1000):
    objects_copy = [copy.deepcopy(obj) for obj in Objects_List]

    for _ in range(iterations):
        for obj in objects_copy:
            obj.acceleration_x = 0
            obj.acceleration_y = 0
        for i in objects_copy:
            for j in objects_copy:
                if i != j:
                    i.apply_gravity_on(j, dt=dt)

        for obj in objects_copy:
            obj.update_velocity(dt=dt)
            obj.update_position(dt=dt)

        for i in objects_copy:
            for j in objects_copy:
                if i != j:
                    i.check_collision_bounce(j)

        with open("temp_bake.txt", "a") as file:
            line = ",".join(f"{obj.x_position},{obj.y_position}" for obj in objects_copy)
            file.write(line + "\n")


def run_bake():
    baked_positions = []
    print("Loading Baked data from temp_bake.txt")
    with open("temp_bake.txt", "r") as file:
        for line in file:
            line = line.strip().rstrip(',')
            if not line:
                continue
            numbers = list(map(float, line.split(',')))
            frame = [(numbers[i], numbers[i+1]) for i in range(0, len(numbers), 2)]
            baked_positions.append(frame)
    return baked_positions

    if not baked_positions:
        print("Error: No baked data found!")
        return