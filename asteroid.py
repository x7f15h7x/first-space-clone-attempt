import pygame
import random
import math

class Asteroid:
    def __init__(self, start_x, start_y, size=50):
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        points = self.generate_points(size)
        pygame.draw.polygon(self.image, (255, 255, 255), points)
        self.rect = self.image.get_rect(center=(start_x, start_y))
        self.direction = random.uniform(0, 360)
        self.speed = random.uniform(1.5, 3.5)
        self.size = size

    def generate_points(self, size):
        num_points = random.randint(6, 12)
        points = []
        for i in range(num_points):
            angle = i * (360 / num_points)
            distance = random.uniform(size * 0.4, size * 0.6)
            x = size / 2 + distance * math.cos(math.radians(angle))
            y = size / 2 + distance * math.sin(math.radians(angle))
            points.append((x, y))
        return points

    def update(self):
        radian_direction = math.radians(self.direction)
        self.rect.x += self.speed * math.cos(radian_direction)
        self.rect.y += self.speed * math.sin(radian_direction)

        self.rect.x %= 800  # Wrap horizontally
        self.rect.y %= 600  # Wrap vertically

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

