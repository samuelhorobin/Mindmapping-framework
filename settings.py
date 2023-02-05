import pygame

RESOLUTION = (1000, 1000)
SCREEN = pygame.display.set_mode(RESOLUTION)
LETTERCRUNCH = 0.1 # Rate of character scaling relative to character count
PEAKCRUNCH = 25 # How much can it get crunched