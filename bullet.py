import pygame
import math

class Bullet:
    def __init__(self, init_x, init_y, angle, speed):
        self.image = pygame.Surface((6, 6))
        pygame.draw.circle(self.image, (255, 255, 255), (3, 3), 3)
        self.rect = self.image.get_rect(center=(init_x, init_y))
        self.angle = angle
        self.speed = speed

    def update(self):
        radian_angle = math.radians(self.angle)
        self.rect.x += self.speed * math.cos(radian_angle)
        self.rect.y -= self.speed * math.sin(radian_angle)

        if self.rect.right < 0 or self.rect.left > 800 or self.rect.bottom < 0 or self.rect.top > 600:
            self.rect = None  # Mark the bullet for removal if it goes off-screen

    def draw(self, screen):
        if self.rect:  # Only draw if the bullet is still valid
            screen.blit(self.image, self.rect.topleft)
