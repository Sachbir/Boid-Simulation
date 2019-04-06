import pygame


class Obstacle:

    screen = None
    color = (0, 0, 0)
    radius = 10

    def __init__(self, x, y):

        self.x = x
        self.y = y
        Obstacle.screen = pygame.display.get_surface()

    def update(self):
        pygame.draw.circle(Obstacle.screen,
                           Obstacle.color,
                           (round(self.x), round(self.y)),
                           Obstacle.radius)
