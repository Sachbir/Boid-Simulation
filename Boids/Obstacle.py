import pygame
from Species import Species


class Obstacle:

    screen = None
    radius = 4

    def __init__(self, species=None):

        self.x = None
        self.y = None

        self.species = species

        Obstacle.screen = pygame.display.get_surface()

    def update(self):

        if self.species is None:
            color = (0, 0, 0)
        else:
            color = self.species.value

        pygame.draw.circle(Obstacle.screen,
                           color,
                           (round(self.x), round(self.y)),
                           self.__class__.radius)
