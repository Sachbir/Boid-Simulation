import config
import pygame
import sys
from Boid import Boid
from Species import Species


class World:

    pygame.init()
    pygame.key.set_repeat(200, 100)
    screen = pygame.display.set_mode(config.world_size)

    def __init__(self):

        self.clock = pygame.time.Clock()

        self.boids = []
        self.obstacles = []

        # self.obstacles.append(Obstacle(320, 240))

    def run(self):

        self.boids = World.spawn_boids()

        while True:

            self.process_events()

            World.screen.fill((225, 225, 225))  # Off-white

            for boid in self.boids:
                boid.calculate_new_direction(self.boids, self.obstacles)
            for boid in self.boids:
                boid.update()
            for obstacle in self.obstacles:
                obstacle.update()

            pygame.display.flip()
            self.clock.tick(config.FPS)

    def process_events(self):

        for event in pygame.event.get():
            if (event.type == pygame.QUIT or
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_q)):  # End simulation
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.boids.append(Boid())
                if event.key == pygame.K_DOWN and len(self.boids) > 0:
                    self.boids.pop(-1)
                if event.key == pygame.K_r:
                    self.boids = World.spawn_boids()

    @staticmethod
    def spawn_boids() -> [Boid]:

        boids = []

        for i in range(config.boid_cap):
            boids.append(Boid(Species.Cardinal))
        for i in range(config.boid_cap):
            boids.append(Boid(Species.Bluebird))
        # for i in range(config.boid_cap):
        #     boids.append(Boid(Species.Raven))
        # for i in range(config.boid_cap):
        #     boids.append(Boid(Species.Sparrow))

        return boids


world = World()
world.run()
