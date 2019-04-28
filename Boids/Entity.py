import pygame


class Entity:

    size = 10
    screen = None

    def __init__(self, species=None, x=None, y=None):

        self.x = x
        self.y = y
        self.species = species

        Entity.screen = pygame.display.get_surface()

    def update_and_render(self):
        """Render a generic Entity image"""

        if self.species is None:
            color = (0, 0, 0)
        else:
            color = self.species.value

        rect = pygame.Rect(self.x - Entity.size, self.y - Entity.size,
                           2 * Entity.size, 2 * Entity.size)
        pygame.draw.rect(pygame.display.get_surface(),
                         color,
                         rect)
