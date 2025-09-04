import pygame
import math

pygame.init()
zoom_factor = 1.0
zoom_step = 1.1

def world_to_screen(x, y, center_x, center_y):
	screen_x = center_x + (x - center_x) * zoom_factor
	screen_y = center_y + (y - center_y) * zoom_factor
	return screen_x, screen_y

class Physics_Object:
    def __init__(self, x_position, y_position, velocity_x=0, velocity_y=0,
                 radius=0, mass=0, color=(255, 0, 0)):
        self.x_position = x_position
        self.y_position = y_position
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.radius = radius
        self.mass = mass
        self.color = color
        self.acceleration_x = 0
        self.acceleration_y = 0

        # Dragging
        self.dragging = False
        self.drag_offset_x = 0
        self.drag_offset_y = 0

        # Resizing
        self.resizing = False
        self.resize_start_dist = 0
        self.initial_radius = radius

        # Hover states
        self.hover_resize = False
        self.hover_drag = False

    def draw(self, surface):
        # Draw main circle
        pygame.draw.circle(surface, self.color,
                           (int(self.x_position), int(self.y_position)),
                           self.radius)

        # If hover near edge → show resize ring
        if self.hover_resize:
            pygame.draw.circle(surface, (255, 255, 255),  # white highlight
                               (int(self.x_position), int(self.y_position)),
                               self.radius + 3, 2)

    def apply_gravity_on(self,other_object,dt=0.5):
        G = 66.743
        distance = ((self.x_position - other_object.x_position) ** 2 + (self.y_position - other_object.y_position) ** 2)**0.5
        if distance <1:
            distance =1
        direction_x, direction_y = (other_object.x_position - self.x_position) / distance, (other_object.y_position - self.y_position) / distance
        force = G * (self.mass * other_object.mass) / (distance**2)


        acc = G * other_object.mass / (distance**2)
        self.acceleration_x += acc * direction_x
        self.acceleration_y += acc * direction_y

    def update_velocity(self, dt=0.5):
        self.velocity_x += self.acceleration_x * dt
        self.velocity_y += self.acceleration_y * dt

    def update_position(self, dt=0.5):
        self.x_position += self.velocity_x * dt
        self.y_position += self.velocity_y * dt
    
    def check_collision_merge(self, other, Object_List):
        distance = ((self.x_position - other.x_position) ** 2 + (self.y_position - other.y_position) ** 2) ** 0.5
        if distance <= self.radius + other.radius and self is not other:
            return True
        else:
            return False
    def Collision_merge(self, other, Object_List):
            #combine the two objects, make a new one, add it to the list, and remove the current ones
            # Conservation of momentum
            total_mass = self.mass + other.mass
            new_velocity_x = (self.velocity_x * self.mass + other.velocity_x * other.mass) / total_mass
            new_velocity_y = (self.velocity_y * self.mass + other.velocity_y * other.mass) / total_mass

            # Volume conservation (assuming spheres)
            new_radius = ((self.radius ** 3 + other.radius ** 3) ** (1/3))

            # Update self
            new_mass = total_mass
            new_velocity_x = new_velocity_x
            new_velocity_y = new_velocity_y
            new_radius = new_radius


            New_object = Physics_Object(
                x_position=self.x_position,
                y_position=self.y_position,
                velocity_x=new_velocity_x,
                velocity_y=new_velocity_y,
                radius=new_radius,
                mass=new_mass
            )
        
            Object_List.remove(self)
            Object_List.remove(other)
            Object_List.append(New_object)

            return Object_List

    def check_collision_bounce(self, other, elasticity=0.9):
        distance = ((self.x_position - other.x_position) ** 2 + (self.y_position - other.y_position) ** 2)**0.5
        if distance <= self.radius + other.radius:
            self.velocity_x = self.velocity_x * -elasticity
            self.velocity_y = self.velocity_y * -elasticity
            other.velocity_x = other.velocity_x * -elasticity
            other.velocity_y = other.velocity_y * -elasticity

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            mouse_x, mouse_y = event.pos
            dist = ((mouse_x - self.x_position) ** 2 +
                    (mouse_y - self.y_position) ** 2) ** 0.5

            # Update hover states
            self.hover_resize = abs(dist - self.radius) <= 10
            self.hover_drag = (dist < self.radius and not self.hover_resize)

            # Dragging
            if self.dragging:
                self.x_position = mouse_x + self.drag_offset_x
                self.y_position = mouse_y + self.drag_offset_y

            # Resizing
            if self.resizing:
                self.radius = max(5, self.initial_radius + (dist - self.resize_start_dist))

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            dist = ((mouse_x - self.x_position) ** 2 +
                    (mouse_y - self.y_position) ** 2) ** 0.5

            if self.hover_resize:
                self.resizing = True
                self.resize_start_dist = dist
                self.initial_radius = self.radius
            elif self.hover_drag:
                self.dragging = True
                self.drag_offset_x = self.x_position - mouse_x
                self.drag_offset_y = self.y_position - mouse_y

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = False
            self.resizing = False
    def is_clicked(self, pos):
        mouse_x, mouse_y = pos
        dist = ((mouse_x - self.x_position) ** 2 +
                (mouse_y - self.y_position) ** 2) ** 0.5
        return dist <= self.radius