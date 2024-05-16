import pygame
from math import sqrt

from Boid import Boid
import config


class Predator(Boid):
    """A type of Boid that hunts and kills other Boids"""

    size = 12

    eat_range = 7

    max_speed = 1.3
    turn_factor = 0.6 * Boid.turn_factor    # Turn 40% faster than Boids (compensates for wide turns at higher speeds)

    def __init__(self, species=None):

        super().__init__(species)
        self.speed = 1
        self.collision_box = None

    def update_and_render(self):
        """Update Predator's location, and renders it as appropriate
        Also renders its view distance if appropriate"""

        super().update_and_render()
        if self.speed < Predator.max_speed:
            self.speed += 0.001
        self.collision_box = pygame.Rect(self.x - Predator.eat_range, self.y - Predator.eat_range,
                                         2 * Predator.eat_range, 2 * Predator.eat_range)    # range in all directions

        if config.debug_mode:
            pygame.draw.circle(pygame.display.get_surface(),
                               (255, 0, 0),
                               (round(self.x), round(self.y)),
                               self.view_dist,
                               1)

    def avoidance_vector(self, boids, entities, predators):
        """Predators should maintain distance between themselves and other entities
        Could potentially combine this with Boid.avoidance, but you'd need to somehow account for Predators not avoiding
        their prey"""

        avg_x = 0
        avg_y = 0

        close_obstacles = self.get_entities_within_distance(entities, 2 * self.neighbour_dist_min)
        close_obstacles.extend(self.get_entities_within_distance(predators, 2 * self.neighbour_dist_min))
        if len(close_obstacles) == 0:
            return 0, 0

        for obstacle in close_obstacles:
            avg_x += obstacle.x
            avg_y += obstacle.y

        avg_x /= len(close_obstacles)
        avg_y /= len(close_obstacles)

        vector_from_center = (self.x - avg_x,
                              self.y - avg_y)
        vector_from_center = Boid.get_unit_vector(vector_from_center)

        return vector_from_center

    def cohesion(self, boids):
        """Search, target, and if possible, eat the nearest Boid
        Also draws a path towards the nearest Boid if required
        Extension of cohesion, as hunting is akin to the cohesion of predator and prey
        Cannot combine with Boid.cohesion because that looks for multiple Boids; this finds only the closest"""

        close_boids = self.get_entities_within_distance(boids, self.view_dist)

        if len(close_boids) == 0:
            return 0, 0

        closest_boid = None
        distance_to_closest_boid = 1000000    # Set high enough that the first boid will always be closer
        for boid in close_boids:
            distance_to_boid = sqrt((boid.x - self.x) ** 2 + (boid.y - self.y) ** 2)
            if distance_to_boid < distance_to_closest_boid:
                distance_to_closest_boid = distance_to_boid
                closest_boid = boid

        if closest_boid is None:
            return 0, 0

        if config.debug_mode:
            pygame.draw.line(pygame.display.get_surface(),
                             (255, 0, 0),
                             (round(self.x), round(self.y)),
                             (round(closest_boid.x), round(closest_boid.y)),
                             1)

        self.collision_box = pygame.Rect(self.x - Predator.eat_range, self.y - Predator.eat_range,
                                         2 * Predator.eat_range, 2 * Predator.eat_range)

        if self.collision_box.collidepoint(closest_boid.x, closest_boid.y):
            closest_boid.respawn()
            self.speed = 0.5
            return 0, 0

        vector_to_closest_boid = (closest_boid.x - self.x,
                                  closest_boid.y - self.y)
        vector_to_closest_boid = Boid.get_unit_vector(vector_to_closest_boid)

        return vector_to_closest_boid
