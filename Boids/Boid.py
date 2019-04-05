import math
import random
import pygame
from Config import Config


class Boid:

    view_distance = 100
    min_distance = 25
    speed = 1
    turn_angle = math.pi / 32

    screen = None

    def __init__(self):

        Boid.screen = pygame.display.get_surface()

        self.x = random.randrange(Config.world_size[0])
        self.y = random.randrange(Config.world_size[1])

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
        vectors[1] = self.separation(boids)
        vectors[1] = 2 * vectors[1][0], 2 * vectors[1][1]       # Separation takes precedence
        vectors[2] = self.alignment(boids)
        vectors[3] = self.cohesion(boids)

        x = vectors[0][0] + vectors[1][0] + vectors[2][0] + vectors[3][0]
        y = vectors[0][1] + vectors[1][1] + vectors[2][1] + vectors[3][1]

        new_vector = (x / len(vectors),
                      y / len(vectors))

        self.direction = Boid.get_unit_vector(new_vector)

    def distance_to(self, boid):

        x_sq = (self.x - boid.x) ** 2
        y_sq = (self.y - boid.y) ** 2

        return math.sqrt(x_sq + y_sq)

    def separation(self, boids):

        close_boids = self.get_boids_within_range(boids, self.min_distance)

        if len(close_boids) == 0:
            return 0, 0

        avg_x = 0
        avg_y = 0

        for boid in close_boids:
            avg_x += boid.x
            avg_y += boid.y

        avg_x /= len(close_boids)
        avg_y /= len(close_boids)

        vector_from_center = (self.x - avg_x,
                              self.y - avg_y)
        vector_from_center = Boid.get_unit_vector(vector_from_center)

        return vector_from_center

    def alignment(self, boids):

        close_boids = self.get_boids_within_range(boids, self.view_distance)

        directions = []
        for boid in close_boids:
            directions.append(boid.direction)

        total_direction = (sum(boid.direction[0] for boid in close_boids),
                           sum(boid.direction[1] for boid in close_boids))

        average_direction = Boid.get_unit_vector(total_direction)

        return average_direction

    def cohesion(self, boids):

        close_boids = self.get_boids_within_range(boids, self.view_distance)

        if len(close_boids) == 0:
            return 0, 0

        avg_x = 0
        avg_y = 0

        for boid in close_boids:
            avg_x += boid.x
            avg_y += boid.y

        avg_x /= len(close_boids)
        avg_y /= len(close_boids)

        vector_to_center = (avg_x - self.x,
                            avg_y - self.y)
        vector_to_center = Boid.get_unit_vector(vector_to_center)

        return vector_to_center

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
