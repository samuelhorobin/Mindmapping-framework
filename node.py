import pygame
import settings
import numpy as np

pygame.font.init()
    
class UITextBox(pygame.sprite.Sprite):
    def __init__(self, title, description, res, pos, colour, groups, parent=None, boolWrapped=True) -> None:
        super().__init__(groups)

        self.colour = colour
        self.nodeRect = pygame.Rect((pos[0], pos[1]), (res[0], res[1]))
        

    def update(self):
        pygame.draw.rect(surface=settings.SCREEN, color=self.colour, rect=self.nodeRect)
        
