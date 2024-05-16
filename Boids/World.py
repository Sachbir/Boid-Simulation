import random
from math import floor
import pygame
import pygame.freetype
import sys
from time import time

import config
from Boid import Boid
from Chunk import Chunk
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

    chunk_size = 2 * Boid.view_dist

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
        self.predators.append(Predator())

        self.spawn_boids(config.num_boids)
        # self.predators.append(Predator())
        self.respawn_walls()

        # TODO: Chunks for all entities, not just Boids

        while True:
            frame_start_time = time()
            self.process_events()

            if not config.paused:
                # screen.fill((220, 225, 230))  # Slightly blue       Does not go with Display Update because of predator view
                screen.fill((30, 30, 30))  # Dark mode

                chunks_dict = self.sort_chunk_data()

                """ Update Entities """
                for predator in self.predators:
                    predator.calculate_new_direction(chunks_dict)
                for boid in self.boids:
                    boid.calculate_new_direction(chunks_dict)

                """ Update Display """
                if config.debug_mode:
                    World.render_chunk_lines(World.chunk_size)
                for predator in self.predators:
                    predator.update_and_render()
                for boid in self.boids:
                    boid.update_and_render()
                for obstacle in self.entities:
                    obstacle.update_and_render()

            self.GUI.render(self.UPS_to_display)
            pygame.display.flip()

            self.measure_UPS(frame_start_time)
            self.clock.tick(config.UPS_max)

    def spawn_boids(self, count):
        """Generate initial set of Boids based on system settings"""

        self.boids = []

        species_counter = 0
        for species in Species:
            for i in range(int(count / config.num_of_species_to_display)):
                self.boids.append(Boid(species))
            species_counter += 1
            if species_counter == config.num_of_species_to_display:
                break

    def respawn_walls(self):

        self.entities = []

        # for i in range(240, 480, 20):
        #     self.entities.append(Entity(None, 320, i))      # Wall on the left
        # self.entities.append(Entity(None, 640, 360))        # Obstacle on the right

        if config.world_border:
            for y in range(0, config.world_size[1]+20, 20):
                self.entities.append(Entity(None, 10,                       y))      # Wall on the left
                self.entities.append(Entity(None, config.world_size[0]-10,  y))      # Wall on the right
            for x in range(0, config.world_size[0]+20, 20):
                self.entities.append(Entity(None, x, 10))                           # Wall on the top
                self.entities.append(Entity(None, x, config.world_size[1]-10))      # Wall on the bottom
            # Shitty little box for the GUI (not done well but whatever)
            for y in range(0, config.gui_height+10, 20):
                self.entities.append(Entity(None, 160, y))
            for x in range(0, 180, 20):
                self.entities.append(Entity(None, x, config.gui_height+10))

        # self.entities.append(Entity(None, config.world_size[0]/2, config.world_size[1]/2))

    def process_events(self):
        """Checks for any and all events occurring during runtime"""

        for event in pygame.event.get():
            if (event.type == pygame.QUIT or
                    (event.type == pygame.KEYDOWN and event.key == pygame.K_q)):  # End simulation
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:     # Pause
                    config.paused = not config.paused
                if event.key == pygame.K_r:         # Restart
                    self.boids = []
                    self.spawn_boids(config.num_boids)
                    self.respawn_walls()
                if event.key == pygame.K_d:         # Display Predator View Range
                    config.debug_mode = not config.debug_mode
                if event.key == pygame.K_m:         # Change Mode
                    config.mode += 1
                    config.mode %= len(config.modes)
                    # Mode toggle
                    if config.mode == 0:
                        config.num_of_species_to_display = 2
                        config.flock_colouring = False
                    elif config.mode == 1:
                        config.num_of_species_to_display = 1
                        config.flock_colouring = True
                    self.boids = []
                    self.spawn_boids(config.num_boids)
                if event.key == pygame.K_c:
                    config.flock_colouring = not config.flock_colouring
                if event.key == pygame.K_w:
                    config.world_border = not config.world_border
                    if config.world_border:
                        self.respawn_walls()
                    else:
                        # self.entities = [Entity(None, config.world_size[0] / 2, config.world_size[1] / 2)]
                        self.entities = []
                if event.key == pygame.K_UP:
                    config.num_boids += 10
                    self.spawn_boids(10)
                if event.key == pygame.K_DOWN:
                    config.num_boids -= 10
                    random.shuffle(self.boids)
                    self.boids = self.boids[:-10]

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

    def sort_chunk_data(self):

        chunks_dict = {}

        for boid in self.boids:
            coord = (floor(boid.x / World.chunk_size),
                     floor(boid.y / World.chunk_size))
            if coord not in chunks_dict:
                chunks_dict[coord] = Chunk()
            chunks_dict[coord].add_boid(boid)
        for predator in self.predators:
            coord = (floor(predator.x / World.chunk_size),
                     floor(predator.y / World.chunk_size))
            if coord not in chunks_dict:
                chunks_dict[coord] = Chunk()
            chunks_dict[coord].add_predator(predator)
        for entity in self.entities:
            coord = (floor(entity.x / World.chunk_size),
                     floor(entity.y / World.chunk_size))
            if coord not in chunks_dict:
                chunks_dict[coord] = Chunk()
            chunks_dict[coord].add_entity(entity)

        return chunks_dict

    @staticmethod
    def render_chunk_lines(chunk_size):

        for i in range(1, round(config.world_size[0] / Boid.view_dist)):
            pygame.draw.line(pygame.display.get_surface(),
                             (0, 0, 0),
                             (i * chunk_size, 0),
                             (i * chunk_size, config.world_size[1]),
                             1)
            pygame.draw.line(pygame.display.get_surface(),
                             (0, 0, 0),
                             (0, i * chunk_size),
                             (config.world_size[0], i * chunk_size),
                             1)


world = World()
world.run()
