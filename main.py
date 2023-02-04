# Imports
import pygame
from sys import exit
from pygame.locals import *
from pathlib import Path
from os import path

import settings
import mapping
import casting

pygame.init()
def get_file(filePath): return path.join(Path(__file__).parent, filePath)


# Constants
pygame.init()
pygame.font.init()
clock = pygame.time.Clock()
border = pygame.Rect((0, 0), settings.RESOLUTION)
map = mapping.Map()
map.setup()

nodeRects = []
for node in map.nodes:
    nodeRects.append(node.nodeRect)


def main():
    while True:
        time_delta = clock.tick(60)/1000.0
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        settings.SCREEN.fill((0, 0, 0))

        map.run()

        source = pygame.mouse.get_pos()
        #source = (250,250)

        casting.cast(source, nodeRects, 200)
            

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()