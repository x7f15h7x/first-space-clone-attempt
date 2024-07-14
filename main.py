import pygame
import random
from player import Player
from asteroid import Asteroid
from bullet import Bullet

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asteroids")

# Function to detect collision between two rectangles
def detect_collision(rect1, rect2):
    return rect1.colliderect(rect2)

# Main game loop
def main():
    clock = pygame.time.Clock()
    game_active = True
    player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    asteroids = [Asteroid(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT)) for _ in range(5)]
    bullets = []
    score = 0
    lives = 3

    while game_active:
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_active = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(player.shoot())

        # Update game objects
        keys = pygame.key.get_pressed()
        player.update(keys)
        for bullet in bullets:
            bullet.update()
        for asteroid in asteroids:
            asteroid.update()

        # Check for collisions between bullets and asteroids
        for bullet in bullets[:]:
            for asteroid in asteroids[:]:
                if detect_collision(bullet.rect, asteroid.rect):
                    bullets.remove(bullet)
                    asteroids.remove(asteroid)
                    score += 10
                    break

        # Check for collisions between player and asteroids
        for asteroid in asteroids[:]:
            if detect_collision(player.rect, asteroid.rect):
                lives -= 1
                asteroids.remove(asteroid)
                if lives <= 0:
                    game_active = False
                break

        # Remove off-screen bullets
        bullets = [bullet for bullet in bullets if bullet.rect.x >= 0 and bullet.rect.x <= SCREEN_WIDTH and bullet.rect.y >= 0 and bullet.rect.y <= SCREEN_HEIGHT]

        # Render everything
        screen.fill((0, 0, 0))  # Clear screen with black
        player.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        for asteroid in asteroids:
            asteroid.draw(screen)
        
        # Display the current score and lives
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))

        pygame.display.flip()  # Update the full display
        clock.tick(FPS)  # Maintain frame rate

    pygame.quit()  # Clean up and exit

if __name__ == "__main__":
    main()

