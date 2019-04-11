import config
import pygame
import sys
from Boid import Boid
from GameObject import GameObject
from Species import Species
from time import time


# noinspection PyPep8Naming
class World:

    pygame.init()
    # set_repeat doesn't want parameters, but requires them on Windows to function
    # noinspection PyArgumentList
    pygame.key.set_repeat(200, 100)
    screen = pygame.display.set_mode(config.world_size)

    def __init__(self):

        self.clock = pygame.time.Clock()

        Boid()

        self.boids = []
        self.game_objects = []

        for i in range(240, 480, 10):
            self.game_objects.append(GameObject(320, i))
        self.game_objects.append(GameObject(960, 360))

        self.display_UPS = False

    def run(self):

        self.boids = World.spawn_boids()

        while True:
            start_time = time()

            self.process_events()

            World.screen.fill((220, 225, 230))  # Slightly blue

            for boid in self.boids:
                boid.calculate_new_direction(self.boids, self.game_objects)
            for boid in self.boids:
                boid.update()
            for obstacle in self.game_objects:
                obstacle.update()

            pygame.display.flip()
            self.clock.tick(config.target_UPS)

            end_time = time()

            config.measured_UPS += (1 / (end_time - start_time))
            config.frame_counter += 1
            if config.frame_counter == config.num_frames_to_measure:
                if self.display_UPS:
                    print("Average UPS: ", round(config.measured_UPS / config.frame_counter))
                config.measured_UPS = 0
                config.frame_counter = 0

    def process_events(self):

        for event in pygame.event.get():
            if (event.type == pygame.QUIT or
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_q)):  # End simulation
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if config.target_UPS == 1:
                        config.target_UPS = 240
                    else:
                        config.target_UPS = 1
                if event.key == pygame.K_UP:
                    self.boids.append(Boid())
                if event.key == pygame.K_DOWN and len(self.boids) > 0:
                    self.boids.pop(-1)
                if event.key == pygame.K_r:
                    self.boids = World.spawn_boids()
                if event.key == pygame.K_u:
                    if self.display_UPS:
                        print("Stop displaying UPS")
                    else:
                        print("Start displaying UPS")
                    self.display_UPS = not self.display_UPS

    @staticmethod
    def spawn_boids():

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
