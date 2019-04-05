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

        self.direction = (random.uniform(1, -1), random.uniform(1, -1))
        self.direction = Boid.get_unit_vector(self.direction)

    def update(self):

        # self.x += Boid.speed * math.cos(self.direction)
        # self.y += Boid.speed * math.sin(self.direction)

        self.x += self.direction[0]    # * .5  # factor if necessary
        self.y += self.direction[1]    # * .5  # factor if necessary

        pygame.draw.circle(Boid.screen,
                           (0, 0, 0),
                           (round(self.x), round(self.y)),
                           4)

    def calculate_new_direction(self, boids):

        # noinspection PyUnusedLocal
        vectors = [(0, 0)
                   for i in range(4)]

        vectors[0] = self.direction
        # vectors[1] = self.move_towards(boids)     # Vector towards nearby boids
        # vectors[2] = self.move_away(boids)        # Vector away from boids too close
        vectors[3] = self.alignment(boids)

        x = vectors[0][0] + vectors[1][0] + vectors[2][0] + vectors[3][0]
        y = vectors[0][1] + vectors[1][1] + vectors[2][1] + vectors[3][1]

        new_vector = (x / len(vectors),
                      y / len(vectors))

        self.direction = Boid.get_unit_vector(new_vector)

    def distance_to(self, boid):

        x_sq = (self.x - boid.x) ** 2
        y_sq = (self.y - boid.y) ** 2

        return math.sqrt(x_sq + y_sq)

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
            return 0, 0
        # elif len(close_boids) == 1:
        #     center_point = [close_boids[0].x,
        #                     close_boids[0].y]
        else:
            center_point = [sum(boid.x for boid in close_boids),
                            sum(boid.y for boid in close_boids)]

        # Get unit vector from bird to center_point
        vector = (center_point[0] - self.x,
                  center_point[1] - self.y)

        # Return unit vector
        return Boid.get_unit_vector(vector)

    def move_away(self, boids):

        # Get close boids
        close_boids = []
        for boid in boids:
            if boid == self:
                continue
            if self.distance_to(boid) < Boid.min_distance:
                close_boids.append(boid)

        # Get center-point of close boids
        if len(close_boids) == 0:
            return 0, 0
        # elif len(close_boids) == 1:
        #     center_point = [close_boids[0].x,
        #                     close_boids[0].y]
        else:
            center_point = [sum(boid.x for boid in close_boids),
                            sum(boid.y for boid in close_boids)]

        # Get unit vector from bird to center_point
        vector = (self.x - center_point[0],
                  self.y - center_point[1])

        # Return unit vector
        return Boid.get_unit_vector(vector)

    # Redoing code below

    def separation(self):
        print("separation")

    def alignment(self, boids):

        close_boids = self.get_boids_within_range(boids, self.view_distance)

        directions = []
        for boid in close_boids:
            directions.append(boid.direction)

        total_direction = (sum(boid.direction[0] for boid in close_boids),
                           sum(boid.direction[1] for boid in close_boids))

        average_direction = Boid.get_unit_vector(total_direction)

        return average_direction

    def cohesion(self):
        print("cohesion")

    def get_boids_within_range(self, boids, range):

        close_boids = []
        for boid in boids:
            if boid == self:
                continue
            if self.distance_to(boid) < range:
                close_boids.append(boid)

        return close_boids

    @staticmethod
    def get_unit_vector(vector):

        try:
            vector_magnitude = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
            unit_vector = (vector[0] / vector_magnitude,
                           vector[1] / vector_magnitude)
            return unit_vector
        except ZeroDivisionError:
            return 0, 0
