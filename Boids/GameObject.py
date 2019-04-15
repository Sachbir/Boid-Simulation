import pygame


class GameObject:

    color = (0, 0, 0)
    screen = None
    radius = 10

    def __init__(self, x, y):

        self.x = x
        self.y = y

        GameObject.screen = pygame.display.get_surface()

    def update(self):
        pygame.draw.circle(GameObject.screen,
                           GameObject.color,
                           (round(self.x), round(self.y)),
                           self.__class__.radius)