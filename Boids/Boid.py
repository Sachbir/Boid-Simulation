from math import sqrt, sin, cos, pi
import pygame
import random

import config
from Entity import Entity
from Species import Species


class Boid(Entity):
    """The structure of a moving entity interacting with its environment"""

    screen = None
    size = 9

    view_dist = 150
    neighbour_dist_min = 25
    avoidance_dist = 50

    speed = 1
    turn_factor = 20

    def __init__(self, species=Species.Cardinal):

        super().__init__(species)

        self.speed = Boid.speed
        self.direction = None

        self.respawn()

    def update(self):
        """Update Boid's location, and draw it as appropriate"""

        """ Update Coordinates """
        self.x += self.direction[0]
        self.y += self.direction[1]

        self.x %= config.world_size[0]
        self.y %= config.world_size[1]

        """ Update Entity View """

        size = self.__class__.size

        coord_1 = Boid.get_unit_vector(self.direction)
        coord_2 = Boid.rotate_vector(coord_1, 140)
        coord_3 = Boid.rotate_vector(coord_1, 180)
        coord_4 = Boid.rotate_vector(coord_1, -140)

        coord_1 = (round(self.x + size * coord_1[0]),
                   round(self.y + size * coord_1[1]))
        coord_2 = (round(self.x + size * coord_2[0]),
                   round(self.y + size * coord_2[1]))
        coord_3 = (round(self.x + size / 3 * coord_3[0]),
                   round(self.y + size / 3 * coord_3[1]))   # Looks better if back point is like this, trust me
        coord_4 = (round(self.x + size * coord_4[0]),
                   round(self.y + size * coord_4[1]))

        if self.species is None:
            color = 0, 0, 0
        else:
            color = self.species.value

        pygame.draw.polygon(pygame.display.get_surface(),
                            color,
                            [coord_1, coord_2, coord_3, coord_4])

    def calculate_new_direction(self, boids, entities, predators):
        """Determines which way the Boid should face given its surroundings"""

        vectors = [self.direction]

        avoidance = self.avoidance(boids, entities, predators)
        if avoidance != (0, 0):    # If there's an avoidance value, we only care about that
            vectors.append(avoidance)
        else:
            vectors.append(self.alignment(boids))
            vectors.append(self.cohesion(boids))

        x = sum(vectors[i][0] for i in range(len(vectors)))
        y = sum(vectors[i][1] for i in range(len(vectors)))

        target_direction = (x / len(vectors),
                            y / len(vectors))

        target_direction = Boid.get_unit_vector(target_direction)
        target_direction = (target_direction[0] / self.__class__.turn_factor,
                            target_direction[1] / self.__class__.turn_factor)

        new_direction = (target_direction[0] + self.direction[0],
                         target_direction[1] + self.direction[1])

        self.direction = Boid.get_unit_vector(new_direction)
        self.direction = (self.speed * self.direction[0],
                          self.speed * self.direction[1])

    def distance_to(self, entity):
        """Gets the scalar distance from the given entity"""

        x_sq = (self.x - entity.x) ** 2
        y_sq = (self.y - entity.y) ** 2

        return sqrt(x_sq + y_sq)

    def avoidance(self, boids, entities, predators):
        """Boids should maintain distance between themselves and other entities"""

        avg_x = 0
        avg_y = 0

        # Get all 'other' entities
        close_entities = self.get_entities_within_distance(predators, Boid.avoidance_dist)
        close_entities.extend(self.get_entities_within_distance(entities, Boid.avoidance_dist))
        # close_entities.extend(self.get_entities_within_distance(boids, Boid.avoidance_dist, False))
        close_entities.extend(self.get_boids_within_distance(boids, Boid.avoidance_dist, False))
        if len(close_entities) == 0:   # If none, get Boids of same species
            # close_entities = self.get_entities_within_distance(boids, Boid.neighbour_dist_min, True)
            close_entities = self.get_boids_within_distance(boids, Boid.neighbour_dist_min, True)
        if len(close_entities) == 0:
            return 0, 0

        for obstacle in close_entities:
            avg_x += obstacle.x
            avg_y += obstacle.y

        avg_x /= len(close_entities)
        avg_y /= len(close_entities)

        vector_from_center = (self.x - avg_x,
                              self.y - avg_y)
        vector_from_center = Boid.get_unit_vector(vector_from_center)

        return vector_from_center

    def alignment(self, boids):
        """Boids should try to move in the same direction as their neighbours"""

        # close_boids = self.get_entities_within_distance(boids, self.view_dist, True)
        close_boids = self.get_boids_within_distance(boids, self.view_dist, True)

        directions = []
        for boid in close_boids:
            directions.append(boid.direction)

        total_direction = (sum(boid.direction[0] for boid in close_boids),
                           sum(boid.direction[1] for boid in close_boids))

        average_direction = Boid.get_unit_vector(total_direction)

        return average_direction

    def cohesion(self, boids):
        """Boids should stay close to their neighbours"""

        # close_boids = self.get_entities_within_distance(boids, self.view_dist, True)
        close_boids = self.get_boids_within_distance(boids, self.view_dist, True)

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

    def get_boids_within_distance(self, boid_dict, distance, should_get_same_species=None):
        """Gets all boids near the Boid"""

        self_coord_rounded = (round(self.x / Boid.view_dist),
                              round(self.y / Boid.view_dist))

        close_boids = []

        # Future improvement: parse 4 quadrants, not 9
        for x in range(-1, 1):
            for y in range(-1, 1):
                coord = (x + self_coord_rounded[0],
                         y + self_coord_rounded[1])
                try:
                    close_boids += boid_dict[coord]
                except KeyError:
                    continue

        return self.get_entities_within_distance(close_boids, distance, should_get_same_species)

    def get_entities_within_distance(self, entities, distance, should_get_same_species=None):
        """Gets all entities near the Boid"""

        close_entities = []
        for entity in entities:
            if entity == self:
                continue    # Ignore self
            if should_get_same_species is not None:
                if should_get_same_species and self.species != entity.species:
                    continue    # If we want similar species, ignore the dissimilar
                if not should_get_same_species and self.species == entity.species:
                    continue    # If we want dissimilar species, ignore the similar
            if self.distance_to(entity) < distance:
                close_entities.append(entity)   # For the remainder, if it's close enough, accept it

        return close_entities

    def respawn(self):
        """Sets Boid's initial conditions"""

        self.x = random.randrange(config.world_size[0])
        self.y = random.randrange(config.world_size[1])

        self.direction = (random.uniform(1, -1), random.uniform(1, -1))
        self.direction = Boid.get_unit_vector(self.direction)

    @staticmethod
    def get_unit_vector(vector):
        """Takes a given vector and normalizes it to a magnitude of 1"""

        vector_magnitude = sqrt(vector[0] ** 2 + vector[1] ** 2)

        if vector_magnitude == 0:
            return 0, 0

        unit_vector = (vector[0] / vector_magnitude,
                       vector[1] / vector_magnitude)
        return unit_vector

    @staticmethod
    def rotate_vector(vector, angle_degrees):
        """Orients a given vector towards a given angle"""

        angle_radians = angle_degrees / 180 * pi

        x = vector[0]
        y = vector[1]

        cos_angle = cos(angle_radians)
        sin_angle = sin(angle_radians)

        new_vector = (cos_angle * x - sin_angle * y,
                      sin_angle * x + cos_angle * y)

        return new_vector
