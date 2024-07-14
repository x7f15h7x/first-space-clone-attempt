import pygame
import random
import os

from player import Player
from asteroid import Asteroid
from bullet import Bullet

# Initialize pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60
HIGH_SCORE_FILE = "highscore.txt"

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asteroids Game")

def check_collision(rect1, rect2):
    """Check if two rectangles overlap."""
    return rect1.colliderect(rect2)

def initialize_game():
    """Initialize game variables and objects."""
    player_ship = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    asteroids = [Asteroid(random.randint(0, SCREEN_WIDTH), random.randint(0, SCREEN_HEIGHT), random.randint(30, 50)) for _ in range(5)]
    bullets = []
    score = 0
    lives = 3
    return player_ship, asteroids, bullets, score, lives

def load_high_score():
    """Load high score from a file."""
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, 'r') as file:
            try:
                return int(file.read().strip())
            except ValueError:
                return 0
    return 0

def save_high_score(high_score):
    """Save high score to a file."""
    with open(HIGH_SCORE_FILE, 'w') as file:
        file.write(str(high_score))

def main():
    # Set up the game clock
    game_clock = pygame.time.Clock()
    game_running = True

    # Initialize the game state
    player_ship, asteroids, bullets, score, lives = initialize_game()
    high_score = load_high_score()

    # Main game loop
    while game_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullets.append(player_ship.shoot())

        # Update the player's position based on key presses
        pressed_keys = pygame.key.get_pressed()
        player_ship.update(pressed_keys)

        # Update the game state for bullets
        for bullet in bullets[:]:
            bullet.update()
            if bullet.rect is None:
                bullets.remove(bullet)

        # Update the game state for asteroids
        for asteroid in asteroids:
            asteroid.update()

        # Check for bullet-asteroid collisions
        new_asteroids = []
        for bullet in bullets[:]:
            for asteroid in asteroids[:]:
                if check_collision(bullet.rect, asteroid.rect):
                    bullets.remove(bullet)
                    new_asteroids.extend(asteroid.break_apart())
                    asteroids.remove(asteroid)
                    score += 10
                    break
        asteroids.extend(new_asteroids)

        # Check for player-asteroid collisions
        for asteroid in asteroids[:]:
            if check_collision(player_ship.rect, asteroid.rect):
                lives -= 1
                new_asteroids.extend(asteroid.break_apart())
                asteroids.remove(asteroid)
                if lives <= 0:
                    if score > high_score:
                        high_score = score
                        save_high_score(high_score)
                    player_ship, asteroids, bullets, score, lives = initialize_game()
                break
        asteroids.extend(new_asteroids)

        # Filter out bullets that are off-screen
        bullets = [bullet for bullet in bullets if bullet.rect and 0 <= bullet.rect.x <= SCREEN_WIDTH and 0 <= bullet.rect.y <= HEIGHT]

        # Render the game objects
        screen.fill((0, 0, 0))
        player_ship.draw(screen)
        for bullet in bullets:
            bullet.draw(screen)
        for asteroid in asteroids:
            asteroid.draw(screen)

        # Initialize font
        font = pygame.font.Font(None, 36)

        # Create text surfaces
        score_surface = font.render(f"Score: {score}", True, (255, 255, 255))
        lives_surface = font.render(f"Lives: {lives}", True, (255, 255, 255))
        high_score_surface = font.render(f"High Score: {high_score}", True, (255, 255, 255))

        # Blit text surfaces onto the screen at specified positions
        screen.blit(score_surface, (10, 10))
        screen.blit(lives_surface, (10, 50))
        screen.blit(high_score_surface, (10, 90))

        # Update the display
        pygame.display.update()

        # Control the frame rate
        game_clock.tick(FPS)

    # Quit the game
    pygame.quit()

if __name__ == "__main__":
    main()
