import pygame
import node
from random import randint
import settings


class Map():
    def __init__(self):
        self.nodes = pygame.sprite.Group()

    def gen_random_node(self):
        node.UITextBox(title="",
                       description="",
                       res=(randint(50, 100),randint(50, 100)),
                       pos=(randint(0,settings.RESOLUTION[0]-100), randint(0, settings.RESOLUTION[1]-100)),
                       colour=(randint(0, 255), randint(0, 255), randint(0, 255)),
                       groups=self.nodes)

    def setup(self):
        for _ in range(5):
            self.gen_random_node()

    def run(self):
        self.nodes.update()
