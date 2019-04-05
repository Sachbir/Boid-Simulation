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

        # noinspection PyUnusedLocal
        self.boids = []
        for i in range(config.num_boids):
            self.boids.append(Boid(Species.Cardinal))
        for i in range(config.num_boids):
            self.boids.append(Boid(Species.Bluebird))
        for i in range(config.num_boids):
            self.boids.append(Boid(Species.Raven))
        for i in range(config.num_boids):
            self.boids.append(Boid(Species.Sparrow))

    def run(self):

        while True:

            self.process_events()

            World.screen.fill((225, 225, 225))  # Off-white

            for boid in self.boids:
                boid.calculate_new_direction(self.boids)
            for boid in self.boids:
                boid.update()

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
                    # noinspection PyUnusedLocal
                    self.boids = []
                    for i in range(config.num_boids):
                        self.boids.append(Boid(Species.Cardinal))
                    for i in range(config.num_boids):
                        self.boids.append(Boid(Species.Bluebird))
                    for i in range(config.num_boids):
                        self.boids.append(Boid(Species.Raven))
                    for i in range(config.num_boids):
                        self.boids.append(Boid(Species.Sparrow))


world = World()
world.run()
