import pygame
import math

class Player:
    def __init__(self, start_x, start_y):
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (255, 255, 255), [(25, 0), (5, 50), (45, 50)])
        self.rect = self.image.get_rect(center=(start_x, start_y))
        self.angle = 0
        self.velocity = 5
        self.bullet_speed = 7

    def update(self, keys):
        if keys[pygame.K_a]:
            self.angle += 5
        if keys[pygame.K_d]:
            self.angle -= 5
        if keys[pygame.K_w]:
            radian_angle = math.radians(self.angle)
            self.rect.x += self.velocity * math.cos(radian_angle)
            self.rect.y -= self.velocity * math.sin(radian_angle)

        self.rect.x %= 800  # Wrap horizontally
        self.rect.y %= 600  # Wrap vertically

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, new_rect.topleft)

    def shoot(self):
        bullet_x = self.rect.centerx + math.cos(math.radians(self.angle)) * 25
        bullet_y = self.rect.centery - math.sin(math.radians(self.angle)) * 25
        return Bullet(bullet_x, bullet_y, self.angle, self.bullet_speed)

# Bullet class needed for shooting functionality
class Bullet:
    def __init__(self, x, y, angle, speed):
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = angle
        self.speed = speed

    def update(self):
        self.rect.x += self.speed * math.cos(math.radians(self.angle))
        self.rect.y -= self.speed * math.sin(math.radians(self.angle))

    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

