import pygame
import random
import math

class Asteroid:
    def __init__(self, start_x, start_y, size=50):
        self.size = size
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        self.points = self.generate_points()
        pygame.draw.polygon(self.image, (255, 255, 255), self.points)
        self.rect = self.image.get_rect(center=(start_x, start_y))
        self.direction = random.uniform(0, 360)
        self.speed = random.uniform(1.5, 3.5)
        self.is_active = True

    def generate_points(self):
        num_points = random.randint(6, 12)
        points = []
        for i in range(num_points):
            angle = i * (360 / num_points)
            distance = random.uniform(self.size * 0.4, self.size * 0.6)
            x = self.size / 2 + distance * math.cos(math.radians(angle))
            y = self.size / 2 + distance * math.sin(math.radians(angle))
            points.append((x, y))
        return points

    def update(self):
        radian_direction = math.radians(self.direction)
        self.rect.x += self.speed * math.cos(radian_direction)
        self.rect.y += self.speed * math.sin(radian_direction)

        # Wrap around screen
        self.rect.x %= 800
        self.rect.y %= 600

    def draw(self, screen):
        if self.is_active:
            screen.blit(self.image, self.rect.topleft)

    def break_apart(self):
        if self.size > 20:  # Break into smaller asteroids if size is greater than 20
            new_size = self.size // 2
            return [
                Asteroid(self.rect.centerx, self.rect.centery, new_size),
                Asteroid(self.rect.centerx, self.rect.centery, new_size)
            ]
        else:
            self.is_active = False
            return []

    def detect_collision(self, other_rect):
        return self.rect.colliderect(other_rect)
