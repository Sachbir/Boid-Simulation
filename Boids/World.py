import pygame
import sys
from Boid import Boid


class World:

    pygame.init()
    screen = pygame.display.set_mode((900, 900))

    def __init__(self):

        self.clock = pygame.time.Clock()

        self.boids = [Boid(300, 300),
                      Boid(600, 600),
                      Boid(300, 600),
                      Boid(600, 300)
                      ]

    def run(self):

        while True:

            for event in pygame.event.get():
                if (event.type == pygame.QUIT or
                        (event.type == pygame.KEYDOWN and event.key == pygame.K_q)):  # End simulation
                    sys.exit(0)

            World.screen.fill((225, 225, 225))  # Off-white

            for boid in self.boids:
                boid.update(self.boids)
            pygame.display.flip()
            self.clock.tick(60)  # 60 ticks/second


world = World()
world.run()
