import math
import random
import pygame
import sys


class Boid:

    view_distance = 100
    min_distance = 25
    speed = 1
    turn_angle = math.pi / 32

    screen = None

    def __init__(self, x, y):

        Boid.screen = pygame.display.get_surface()

        self.x = x
        self.y = y
        self.direction = random.uniform(1, 2 * math.pi + 1) % (2 * math.pi)

    def update(self, boids):

        self.move_towards(boids)

        self.x += Boid.speed * math.cos(self.direction)
        self.y += Boid.speed * math.sin(self.direction)

        pygame.draw.circle(Boid.screen,
                           (0, 0, 0),
                           (round(self.x), round(self.y)),
                           4)

    def move_towards(self, boids):

        # Get close boids
        close_boids = []
        for boid in boids:
            if boid == self:
                continue
            if self.distance_to(boid) < Boid.view_distance:
                close_boids.append(boid)

        # Get center-point of close boids
        if len(close_boids) == 0:
            return
        # elif len(close_boids) == 1:
        #     center_point = [close_boids[0].x,
        #                     close_boids[0].y]
        else:
            center_point = [sum(boid.x for boid in close_boids),
                            sum(boid.y for boid in close_boids)]

        # Get boid movement
        m, b, facing_right = self.get_movement()

        point_is_below = False

        if center_point[1] > (m * center_point[0] + b):
            point_is_below = True

        if ((facing_right and point_is_below) or
                (not facing_right and not point_is_below)):
            self.direction += Boid.turn_angle
        else:
            self.direction -= Boid.turn_angle

    def distance_to(self, boid):

        x_sq = (self.x - boid.x) ** 2
        y_sq = (self.y - boid.y) ** 2

        return math.sqrt(x_sq + y_sq)

    def get_movement(self):

        delta_x = self.x + math.cos(self.direction)  # * 100
        delta_y = self.y + math.sin(self.direction)  # * 100
        # solve the line equation, y = mx + b, of the direction of travel
        m = (delta_y - self.y) / (delta_x - self.x)
        b = delta_y - m * delta_x

        facing_right = ((self.direction - math.pi / 2) % (2 * math.pi)) > math.pi

        return m, b, facing_right
