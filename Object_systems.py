import Object  # Your Physics_Object class

WIDTH, HEIGHT = 800, 600  # Example canvas size

# -------------------------------
# System 1: One star, three planets in simple circular-ish orbits
# -------------------------------
def One_star_three_planets():
    star = Object.Physics_Object(x_position=WIDTH//2, y_position=HEIGHT//2,
                                 velocity_x=0, velocity_y=0,
                                 radius=40, mass=10000)
    
    planet1 = Object.Physics_Object(x_position=WIDTH//2 + 250, y_position=HEIGHT//2,
                                    velocity_x=0, velocity_y=3,
                                    radius=12, mass=300)
    planet2 = Object.Physics_Object(x_position=WIDTH//2 + 300, y_position=HEIGHT//2,
                                    velocity_x=0, velocity_y=2.5,
                                    radius=12, mass=300)
    planet3 = Object.Physics_Object(x_position=WIDTH//2 + 200, y_position=HEIGHT//2,
                                    velocity_x=0, velocity_y=3.5,
                                    radius=12, mass=300)
    
    return [star, planet1, planet2, planet3]


# -------------------------------
# System 2: Binary stars with planets
# -------------------------------
def Two_binary_stars_with_two_planets():
    star1 = Object.Physics_Object(x_position=WIDTH//2 - 50, y_position=HEIGHT//2,
                                  velocity_x=0, velocity_y=-1,
                                  radius=35, mass=8000)
    star2 = Object.Physics_Object(x_position=WIDTH//2 + 50, y_position=HEIGHT//2,
                                  velocity_x=0, velocity_y=1,
                                  radius=35, mass=8000)
    
    planet1 = Object.Physics_Object(x_position=WIDTH//2, y_position=HEIGHT//2 + 150,
                                    velocity_x=2, velocity_y=0,
                                    radius=10, mass=200)
    planet2 = Object.Physics_Object(x_position=WIDTH//2, y_position=HEIGHT//2 + 200,
                                    velocity_x=1.8, velocity_y=0,
                                    radius=10, mass=200)
    
    return [star1, star2, planet1, planet2]


# -------------------------------
# System 3: Small star cluster
# -------------------------------
def One_star_cluster():
    objects = []
    center_x, center_y = WIDTH//2, HEIGHT//2
    # Central massive star
    central_star = Object.Physics_Object(center_x, center_y, 0, 0, radius=50, mass=15000)
    objects.append(central_star)
    
    # 6 smaller stars orbiting central star
    positions = [(100,0),(0,100),(-100,0),(0,-100),(70,70),(-70,-70)]
    velocities = [(0,2),(-2,0),(0,-2),(2,0),(1.5,-1.5),(-1.5,1.5)]
    
    for (dx, dy), (vx, vy) in zip(positions, velocities):
        objects.append(Object.Physics_Object(center_x + dx, center_y + dy,
                                             vx, vy, radius=15, mass=500))
    return objects

# -------------------------------
# System 4: One star, three planets in simple circular-ish orbits
# -------------------------------

def Two_binary_stars():
    star1 = Object.Physics_Object(x_position=WIDTH//2 - 100, y_position=HEIGHT//2,
                                  velocity_x=0, velocity_y=-5,
                                  radius=35, mass=8000)
    star2 = Object.Physics_Object(x_position=WIDTH//2 + 100, y_position=HEIGHT//2,
                                  velocity_x=0, velocity_y=5,
                                  radius=35, mass=8000)
    return [star1, star2]