import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
import pygame

from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot

def main():
    pygame.init()
    print("Starting Asteroids!")
    print(".")
    print(".")
    print(".")
#    print(f"Screen width: {SCREEN_WIDTH}")
#    print(f"Screen height: {SCREEN_HEIGHT}")
    Clock = pygame.time.Clock()
    title_font = pygame.font.SysFont(None, 72)
    score_font = pygame.font.SysFont(None, 32)

    dt = 0
    score = 0

    pygame.display.set_caption("Asteroids Game")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    welcome_surface = title_font.render("Welcome to Asteroids!", True, "white")
    welcome_rect = welcome_surface.get_rect()
    welcome_rect.center = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Player.containers = (updatable, drawable)
    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Shot.containers = (updatable, drawable, shots)

    asteroidfield = AsteroidField()
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

# display welcome message
    screen.blit(welcome_surface, welcome_rect)
    pygame.display.flip()
    pygame.time.wait(2000)

    with open("high_score.txt","r") as f:
        high_score = int(f.read())
    score_surface = score_font.render(f"Current Score: {score}", True, "white")
    high_score_surface = score_font.render(f"High score: {high_score}", True, "white")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        screen.fill("black")
        updatable.update(dt)
        for asteroid in asteroids:
# game end condition
            if asteroid.collision(player) == True:
                print("Game over!")
                print(f"Your score was: {score}")
                if score > high_score:
                    print("New high score!")
                    with open("high_score.txt", "w") as f:
                        f.write(f"{score}")
                return
            for shot in shots:
                if asteroid.collision(shot):
                    asteroid.split()
                    shot.kill()
                    score += 1
                    score_surface = score_font.render(f"Current Score: {score}", True, "white")
        for drawn in drawable:
            drawn.draw(screen)
        screen.blit(score_surface, (50, 50))
        screen.blit(high_score_surface, (50, 80))
        pygame.display.flip()
        dt = Clock.tick(60) / 1000


if __name__ == "__main__":
    main()
