import pygame


class Entity:

    size = 10
    screen = None

    def __init__(self, species=None, x=None, y=None):

        self.x = x
        self.y = y
        self.species = species

        Entity.screen = pygame.display.get_surface()

    def update(self):
        """Render a generic Entity image"""

        if self.species is None:
            color = (0, 0, 0)
        else:
            color = self.species.value

        pygame.draw.circle(Entity.screen,
                           color,
                           (round(self.x), round(self.y)),
                           self.__class__.size)
