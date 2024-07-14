import pygame
import math

class Player:
    def __init__(self, start_x, start_y):
        self.size = 30  # Smaller size
        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        pygame.draw.polygon(self.image, (255, 255, 255), [(self.size // 2, 0), (0, self.size), (self.size, self.size)])
        self.rect = self.image.get_rect(center=(start_x, start_y))
        self.angle = 0
        self.speed = 0
        self.max_speed = 5
        self.acceleration = 0.2
        self.rotation_speed = 5
        self.bullet_speed = 7

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.angle += self.rotation_speed
        if keys[pygame.K_RIGHT]:
            self.angle -= self.rotation_speed
        if keys[pygame.K_UP]:
            self.speed += self.acceleration
        if keys[pygame.K_DOWN]:
            self.speed -= self.acceleration
        
        self.speed = max(-self.max_speed, min(self.speed, self.max_speed))  # Clamp speed

        radian_angle = math.radians(self.angle)
        self.rect.x += self.speed * math.cos(radian_angle)
        self.rect.y -= self.speed * math.sin(radian_angle)

        # Wrap around screen
        self.rect.x %= 800
        self.rect.y %= 600

    def draw(self, screen):
        rotated_image = pygame.transform.rotate(self.image, self.angle)
        new_rect = rotated_image.get_rect(center=self.rect.center)
        screen.blit(rotated_image, new_rect.topleft)

    def shoot(self):
        radian_angle = math.radians(self.angle)
        bullet_x = self.rect.centerx + math.cos(radian_angle) * (self.size // 2)
        bullet_y = self.rect.centery - math.sin(radian_angle) * (self.size // 2)
        return Bullet(bullet_x, bullet_y, self.angle, self.bullet_speed)

class Bullet:
    def __init__(self, x, y, angle, speed):
        self.image = pygame.Surface((5, 5))
        self.image.fill((255, 255, 255))
        self.rect = self.image.get_rect(center=(x, y))
        self.angle = angle
        self.speed = speed

    def update(self):
        radian_angle = math.radians(self.angle)
        self.rect.x += self.speed * math.cos(radian_angle)
        self.rect.y -= self.speed * math.sin(radian_angle)

        # Remove bullet if it goes off screen
        if self.rect.right < 0 or self.rect.left > 800 or self.rect.bottom < 0 or self.rect.top > 600:
            self.rect = None

    def draw(self, screen):
        if self.rect:  # Only draw if the bullet is still valid
            screen.blit(self.image, self.rect.topleft)


    def draw(self, screen):
        screen.blit(self.image, self.rect.topleft)

