# Note: Species-specific code is included, but the implementation needs work

import config
import pygame
import random
from math import sqrt, pi
from Species import Species


class Boid:

    view_distance = 200
    min_distance = 25
    speed = 1

    screen = None

    def __init__(self, species=Species.Raven):

        self.species = species.value

        Boid.screen = pygame.display.get_surface()

        self.x = random.randrange(config.world_size[0])
        self.y = random.randrange(config.world_size[1])

        self.direction = (random.uniform(1, -1), random.uniform(1, -1))
        self.direction = Boid.get_unit_vector(self.direction)

    def update(self):

        self.x += self.direction[0]
        self.y += self.direction[1]

        self.x %= config.world_size[0]
        self.y %= config.world_size[1]

        # Keep this for demos until triangle turning is complete
        pygame.draw.circle(Boid.screen,
                           self.species,
                           (round(self.x), round(self.y)),
                           4)

        # size = 10

        # Terribly ugly
        # front_coord = [round(self.x + self.direction[0]) * size,
        #                round(self.y + self.direction[1]) * size]
        # back_left_coord = [round(self.x - self.direction[0] * cos(3 * pi / 4)) * size,
        #                    round(self.y - self.direction[1] * sin(3 * pi / 4)) * size]
        # back_right_coord = [round(self.x - self.direction[0] * cos(5 * pi / 4)) * size,
        #                     round(self.y - self.direction[1] * sin(5 * pi / 4)) * size]
        #
        # pygame.draw.polygon(Boid.screen,
        #                     (0, 0, 0),
        #                     [front_coord, back_left_coord, back_right_coord])

    def calculate_new_direction(self, boids, obstacles):

        # noinspection PyUnusedLocal
        vectors = [(0, 0)
                   for i in range(4)]

        avoidance_factor = 100

        vectors[0] = self.direction
        vectors[1] = self.separation(boids, obstacles)
        vectors[1] = avoidance_factor * vectors[1][0], avoidance_factor * vectors[1][1]       # Separation takes precedence
        vectors[2] = self.alignment(boids)
        vectors[3] = self.cohesion(boids)

        x = sum(vectors[i][0] for i in range(len(vectors)))
        y = sum(vectors[i][1] for i in range(len(vectors)))

        target_direction = (x / len(vectors),
                            y / len(vectors))

        target_direction = Boid.get_unit_vector(target_direction)
        target_direction = (target_direction[0] / config.turn_factor,
                            target_direction[1] / config.turn_factor)

        new_direction = (target_direction[0] + self.direction[0],
                         target_direction[1] + self.direction[1])

        self.direction = Boid.get_unit_vector(new_direction)

    def distance_to(self, boid):

        x_sq = (self.x - boid.x) ** 2
        y_sq = (self.y - boid.y) ** 2

        return sqrt(x_sq + y_sq)

    def separation(self, boids, obstacles):

        close_boids = self.get_objects_within_distance(boids, self.min_distance)
        close_obstacles = self.get_objects_within_distance(obstacles, self.min_distance)

        if len(close_boids) == 0:
            return 0, 0

        avg_x = 0
        avg_y = 0

        for boid in close_boids:
            avg_x += boid.x
            avg_y += boid.y

        avoidance_factor = 1000

        for obstacle in close_obstacles:
            avg_x += obstacle.x * avoidance_factor
            avg_y += obstacle.y * avoidance_factor

        avg_x /= len(close_boids) + len(close_obstacles) * avoidance_factor
        avg_y /= len(close_boids) + len(close_obstacles) * avoidance_factor

        vector_from_center = (self.x - avg_x,
                              self.y - avg_y)
        vector_from_center = Boid.get_unit_vector(vector_from_center)

        return vector_from_center

    def alignment(self, boids):

        close_boids = self.get_objects_within_distance(boids, self.view_distance, True)

        directions = []
        for boid in close_boids:
            directions.append(boid.direction)

        total_direction = (sum(boid.direction[0] for boid in close_boids),
                           sum(boid.direction[1] for boid in close_boids))

        average_direction = Boid.get_unit_vector(total_direction)

        return average_direction

    def cohesion(self, boids):

        close_boids = self.get_objects_within_distance(boids, self.view_distance, True)

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

    def get_objects_within_distance(self, objects, distance, should_consider_species=False):

        close_objects = []
        for obj in objects:
            if obj == self:
                continue
            if should_consider_species:
                if self.species != obj.species:
                    continue
            if self.distance_to(obj) < distance:
                close_objects.append(obj)

        return close_objects

    @staticmethod
    def get_unit_vector(vector):

        vector_magnitude = sqrt(vector[0] ** 2 + vector[1] ** 2)

        if vector_magnitude == 0:
            return 0, 0

        unit_vector = (vector[0] / vector_magnitude,
                       vector[1] / vector_magnitude)
        return unit_vector
