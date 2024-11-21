import pygame
from pygame import mixer

# Initialize Pygame
pygame.init()
mixer.init()

# Create the display window
screen = pygame.display.set_mode((600, 400))
pygame.display.set_caption("Music Player with Visualization")

# Load music
song = "Songs\Shitty_programmer.mp3"
mixer.music.load(song)

# Play music
mixer.music.play(-1)

# Main loop
running = True
while running:
    screen.fill((0, 0, 0))  # Clear screen

    # Example of visualizing something (just a simple rectangle as placeholder)
    pygame.draw.rect(screen, (255, 0, 0), (50, 50, 200, 100))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.update()

pygame.quit()
