import pygame

RESOLUTION = (500, 500)
SCREEN = pygame.display.set_mode(RESOLUTION)
LETTERCRUNCH = 0.1 # Rate of character scaling relative to character count
PEAKCRUNCH = 25 # How much can it get crunched