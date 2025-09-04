import pygame
import math

class arrow:
    def __init__(self, x, y, length, angle, color=(255, 255, 255), width=3):
        self.x = x
        self.y = y
        self.length = length
        self.angle = angle  # in degrees
        self.color = color
        self.width = width
        self.update_points()

    def update_points(self):
        """Recalculate arrow tip and head points based on angle and length."""
        # Convert angle to radians
        rad = math.radians(self.angle)

        # Arrow tip (end point)
        self.end_x = self.x + self.length * math.cos(rad)
        self.end_y = self.y - self.length * math.sin(rad)  # y-axis inverted in pygame

        # Arrowhead size
        head_length = self.length * 0.2
        head_angle = math.radians(25)  # 25° spread

        # Left head point
        left_x = self.end_x - head_length * math.cos(rad - head_angle)
        left_y = self.end_y + head_length * math.sin(rad - head_angle)

        # Right head point
        right_x = self.end_x - head_length * math.cos(rad + head_angle)
        right_y = self.end_y + head_length * math.sin(rad + head_angle)

        self.head_points = [(self.end_x, self.end_y), (left_x, left_y), (right_x, right_y)]

    def set_angle(self, angle):
        """Change arrow direction."""
        self.angle = angle
        self.update_points()

    def set_length(self, length):
        """Change arrow length."""
        self.length = length
        self.update_points()

    def draw(self, screen):
        """Draw the arrow on the screen."""
        # Draw main line
        pygame.draw.line(screen, self.color, (self.x, self.y), (self.end_x, self.end_y), self.width)
        # Draw arrowhead
        pygame.draw.polygon(screen, self.color, self.head_points)
