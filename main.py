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

        proximityRects = casting.proximity_check(source, nodeRects, 200)
        for rect in proximityRects:
            for point in [rect.topleft, rect.topright, rect.bottomright, rect.bottomleft]:
                sourceLine = casting.Line(source, point)

                for side in [(rect.topleft, rect.topright),
                                (rect.topright, rect.bottomright),
                                (rect.bottomright, rect.bottomleft),
                                (rect.bottomleft, rect.topleft)]:
                    nodeLine = casting.Line(side[0], side[1])
                    intersection = sourceLine.line_intersection(nodeLine)
                    if intersection:
                        pygame.draw.line(
                            settings.SCREEN, (255, 50, 50), source, point, 10)  # Red line
                        print(f"RED at source-pos {source} with output {intersection}\nProjected to point {point}\n")
                    else:
                        print(f"GREEN at source-pos {source} with output {intersection}\nProjected to point {point}\n")
                        pygame.draw.line(
                            settings.SCREEN, (150, 150, 5), source, point, 5)  # Green line
            

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()