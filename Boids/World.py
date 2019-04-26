import pygame
import pygame.freetype
import sys
from time import time

import config
from Boid import Boid
from Entity import Entity
from GUI import GUI
from Predator import Predator
from Species import Species

pygame.init()
# set_repeat doesn't want parameters, but requires them on Windows to function
# noinspection PyArgumentList
pygame.key.set_repeat(200, 100)
screen = pygame.display.set_mode(config.world_size)
pygame.display.set_caption("Boid Simulation")
icon = pygame.image.load("icon.png")
pygame.display.set_icon(icon)


# noinspection PyPep8Naming
class World:
    """Contains and acts upon the simulation"""

    def __init__(self):

        self.clock = pygame.time.Clock()
        self.GUI = GUI()

        self.boids = []
        self.predators = []
        self.entities = []

        self.UPS_to_display = 0

    def run(self):
        """Run the main cycle until terminated
        Update and render all entities"""

        self.spawn_boids()
        # self.predators.append(Predator())

        for i in range(240, 480, 10):
            self.entities.append(Entity(None, 320, i))      # Wall on the left
        self.entities.append(Entity(None, 640, 360))        # Obstacle on the right

        while True:
            frame_start_time = time()
            self.process_events()
            screen.fill((220, 225, 230))  # Slightly blue       Does not go with Display Update because of predator view

            # Create dictionary of boids by location
            boid_dict = {}
            for boid in self.boids:
                coord = (round(boid.x / Boid.view_dist),
                         round(boid.y / Boid.view_dist))
                if coord in boid_dict:
                    boid_dict[coord].append(boid)
                else:
                    boid_dict[coord] = [boid]

            """ Update Entities """
            for predator in self.predators:
                predator.calculate_new_direction(self.boids, self.entities, self.predators)
            for boid in self.boids:
                # boid.calculate_new_direction(self.boids, self.entities, self.predators)
                boid.calculate_new_direction(boid_dict, self.entities, self.predators)

            """ Update Display """
            for predator in self.predators:
                predator.update()
            for boid in self.boids:
                boid.update()
            for obstacle in self.entities:
                obstacle.update()
            self.GUI.render(self.UPS_to_display)
            pygame.display.flip()

            self.measure_UPS(frame_start_time)
            self.clock.tick(config.UPS_max)

    def spawn_boids(self):
        """Generate initial set of Boids based on system settings"""

        self.boids = []

        species_counter = 0
        for species in Species:
            for i in range(int(config.total_boid_cap / config.num_of_species_to_display)):
                self.boids.append(Boid(species))
            species_counter += 1
            if species_counter == config.num_of_species_to_display:
                break

    def process_events(self):
        """Checks for any and all events occurring during runtime"""

        for event in pygame.event.get():
            if (event.type == pygame.QUIT or
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_q)):  # End simulation
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:     # Pause
                    if config.UPS_max == 1:
                        config.UPS_max = 240
                    else:
                        config.UPS_max = 1
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
        """Takes the beginning and end time of the cycle to determine how fast the system is actually operating at"""

        frame_time_end = time()
        time_elapsed = frame_time_end - start_time

        # When the frame renders as fast as possible (minimal/zero values), UPS reaches the maximum allowed
        try:
            measured_UPS = min((1 / time_elapsed), config.UPS_max)
        except ZeroDivisionError:
            measured_UPS = 120
        config.UPS_measured += measured_UPS

        config.frame_counter += 1
        if config.frame_counter == config.num_frames_to_measure:
            self.UPS_to_display = round(config.UPS_measured / config.frame_counter)
            config.UPS_measured = 0
            config.frame_counter = 0


world = World()
world.run()
