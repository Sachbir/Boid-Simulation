import pygame
import random
import sys
from Boid import Boid


class World:

    pygame.init()
    screen = pygame.display.set_mode((900, 900))

    def __init__(self):

        self.clock = pygame.time.Clock()

        # noinspection PyUnusedLocal
        # self.boids = [Boid(random.randrange(900), random.randrange(900))
        #               for i in range(4)]
        self.boids = [Boid(450, 450),
                      Boid(600, 500)]

    def run(self):

        fps = 600

        while True:

            for event in pygame.event.get():
                if (event.type == pygame.QUIT or
                        (event.type == pygame.KEYDOWN and event.key == pygame.K_q)):  # End simulation
                    sys.exit(0)

            World.screen.fill((225, 225, 225))  # Off-white

            for boid in self.boids:
                boid.calculate_new_direction(self.boids)
            for boid in self.boids:
                boid.update()
            pygame.display.flip()
            self.clock.tick(fps)  # 60 ticks/second


world = World()
world.run()
