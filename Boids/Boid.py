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
        # TODO: Test vector-based angles in place of present angle-based system
        #   Already written, just need to test
        # self.dir_vector = (random.uniform(1, -1), random.uniform(1, -1))
        # self.dir_vector = Boid.get_unit_vector(self.dir_vector)

    def update(self):

        self.x += Boid.speed * math.cos(self.direction)
        self.y += Boid.speed * math.sin(self.direction)

        # self.x += self.dir_vector[0]    # * .5  # factor if necessary
        # self.y += self.dir_vector[1]    # * .5  # factor if necessary

        pygame.draw.circle(Boid.screen,
                           (0, 0, 0),
                           (round(self.x), round(self.y)),
                           4)

    def calculate_new_direction(self, boids):

        try:
            delta_x = math.cos(self.direction)
            delta_y = math.sin(self.direction)

            # noinspection PyUnusedLocal
            vectors = [(0, 0)
                       for i in range(4)]

            # TODO: Fix the bottom-right drift
            #   Seems like boids don't average between one another correctly
            vectors[0] = (round(delta_x), round(delta_y))           # Vector of current trajectory
            # vectors[0] = self.dir_vector
            vectors[1] = self.move_towards(boids)     # Vector towards nearby boids
            vectors[2] = self.move_away(boids)        # Vector away from boids too close
            vectors[3] = self.move_in_avg_direction(boids)

            x = vectors[0][0] + vectors[1][0] + vectors[2][0] + vectors[3][0]
            y = vectors[0][1] + vectors[1][1] + vectors[2][1] + vectors[3][1]

            new_vector = (x / len(vectors),
                          y / len(vectors))
            # self.dir_vector = (x / len(vectors),
            #                    y / len(vectors))

            self.direction = math.atan(new_vector[1] / new_vector[0])
        except ArithmeticError:
            print("An error has occurred in vector calculations")
            sys.exit(-1)

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

    def move_in_avg_direction(self, boids):

        # Get close boids
        close_boids = []
        for boid in boids:
            if boid == self:
                continue
            if self.distance_to(boid) < Boid.min_distance:
                close_boids.append(boid)

        all_directions = []
        for boid in boids:
            all_directions.append(boid.dir_vector)

        avg_direction = (sum(boid.dir_vector[0] for boid in close_boids),
                         sum(boid.dir_vector[1] for boid in close_boids))

        return avg_direction

    @staticmethod
    def get_unit_vector(vector):

        vector_magnitude = math.sqrt(vector[0] ** 2 + vector[1] ** 2)
        unit_vector = (vector[0] / vector_magnitude,
                       vector[1] / vector_magnitude)
        return unit_vector
