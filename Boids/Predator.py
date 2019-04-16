import pygame
from Boid import Boid
from math import sqrt


class Predator(Boid):

    size = 12
    render_view_range = False

    eat_range = 7

    max_speed = 1.3
    turn_factor = 0.6 * Boid.turn_factor    # Turn 40% faster than Boids (compensates for wide turns at higher speeds)

    def __init__(self, species=None):

        super().__init__(species)
        self.speed = 1
        self.collision_box = None

    def update(self):

        super().update()
        if self.speed < Predator.max_speed:
            self.speed += 0.001
        self.collision_box = pygame.Rect(self.x - Predator.eat_range, self.y - Predator.eat_range,
                                         2 * Predator.eat_range, 2 * Predator.eat_range)

        if Predator.render_view_range:
            pygame.draw.circle(pygame.display.get_surface(),
                               (255, 0, 0),
                               (round(self.x), round(self.y)),
                               self.view_dist,
                               1)

    def calculate_new_direction(self, boids, game_objects, predators):

        vectors = [self.direction]

        avoidance = self.avoidance(boids, game_objects, predators)
        hunting = self.hunt(boids)
        if avoidance != (0, 0):    # If there's a separation value, we only care about that
            vectors.append(avoidance)
        elif hunting != (0, 0):
            vectors.append(hunting)
        else:                       # Otherwise let's focus on being a group
            vectors.append(self.alignment(boids))
            vectors.append(self.cohesion(boids))

        x = sum(vectors[i][0] for i in range(len(vectors)))
        y = sum(vectors[i][1] for i in range(len(vectors)))

        target_direction = (x / len(vectors),
                            y / len(vectors))

        target_direction = Boid.get_unit_vector(target_direction)
        target_direction = (target_direction[0] / Predator.turn_factor,
                            target_direction[1] / Predator.turn_factor)

        new_direction = (target_direction[0] + self.direction[0],
                         target_direction[1] + self.direction[1])

        self.direction = Boid.get_unit_vector(new_direction)
        self.direction = (self.speed * self.direction[0],
                          self.speed * self.direction[1])

    def avoidance(self, boids, game_objects, predators):

        avg_x = 0
        avg_y = 0

        close_obstacles = self.get_objects_within_distance(game_objects, 2 * self.neighbour_dist_min)
        close_obstacles.extend(self.get_objects_within_distance(predators, 2 * self.neighbour_dist_min))
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

    # Very similar to cohesion (Boid class), except it targets a specific boid
    def hunt(self, boids):

        close_boids = self.get_objects_within_distance(boids, self.view_dist)

        if len(close_boids) == 0:
            return 0, 0

        closest_boid = None
        distance_to_closest_boid = 10000
        for boid in close_boids:
            distance_to_boid = sqrt((boid.x - self.x) ** 2 + (boid.y - self.y) ** 2)
            if distance_to_boid < distance_to_closest_boid:
                distance_to_closest_boid = distance_to_boid
                closest_boid = boid

        if closest_boid is None:
            return 0, 0

        if Predator.render_view_range:
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
