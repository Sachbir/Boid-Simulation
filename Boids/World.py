import config
import pygame
import pygame.freetype
import sys
from Boid import Boid
from GameObject import GameObject
from GUI import GUI
from Predator import Predator
from Species import Species
from time import time

pygame.init()
# set_repeat doesn't want parameters, but requires them on Windows to function
# noinspection PyArgumentList
pygame.key.set_repeat(200, 100)
screen = pygame.display.set_mode(config.world_size)


# noinspection PyPep8Naming
class World:

    def __init__(self):

        self.clock = pygame.time.Clock()
        self.GUI = GUI()

        self.boids = []
        self.predators = []
        self.game_objects = []

        self.UPS_to_display = 0

    def run(self):

        self.spawn_boids()
        self.predators.append(Predator())

        for i in range(240, 480, 10):
            self.game_objects.append(GameObject(320, i))
        self.game_objects.append(GameObject(640, 360))

        while True:
            frame_start_time = time()
            self.process_events()
            screen.fill((220, 225, 230))  # Slightly blue

            """Update Entities"""
            for predator in self.predators:
                predator.calculate_new_direction(self.boids, self.game_objects, self.predators)
            for boid in self.boids:
                boid.calculate_new_direction(self.boids, self.game_objects, self.predators)

            """Update Display"""
            for predator in self.predators:
                predator.update()
            for boid in self.boids:
                boid.update()
            for obstacle in self.game_objects:
                obstacle.update()
            self.GUI.render(self.UPS_to_display)
            pygame.display.flip()

            self.measure_UPS(frame_start_time)
            self.clock.tick(config.max_UPS)

    def spawn_boids(self):

        self.boids = []

        species_counter = 0
        for species in Species:
            for i in range(int(config.total_boid_cap / config.num_of_species_to_display)):
                self.boids.append(Boid(species))
            species_counter += 1
            if species_counter == config.num_of_species_to_display:
                break

    def process_events(self):

        for event in pygame.event.get():
            if (event.type == pygame.QUIT or
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_q)):  # End simulation
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:     # Pause
                    if config.max_UPS == 1:
                        config.max_UPS = 240
                    else:
                        config.max_UPS = 1
                if event.key == pygame.K_r:         # Restart
                    self.spawn_boids()
                if event.key == pygame.K_p:         # Display Predator View Range
                    Predator.render_view_range = not Predator.render_view_range
                if event.key == pygame.K_s:         # Cycle Species Count
                    config.num_of_species_to_display += 1
                    # noinspection PyTypeChecker
                    if config.num_of_species_to_display > len(Species):
                        config.num_of_species_to_display = 1
                    self.spawn_boids()

    def measure_UPS(self, start_time):

        frame_time_end = time()
        time_elapsed = frame_time_end - start_time

        # When the frame renders as fast as possible (minimal/zero values), UPS reaches the maximum allowed
        try:
            measured_UPS = min((1 / time_elapsed), config.max_UPS)
        except ZeroDivisionError:
            measured_UPS = 120
        config.measured_UPS += measured_UPS

        config.frame_counter += 1
        if config.frame_counter == config.num_frames_to_measure:
            self.UPS_to_display = round(config.measured_UPS / config.frame_counter)
            config.measured_UPS = 0
            config.frame_counter = 0


world = World()
world.run()
