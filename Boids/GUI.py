import pygame.freetype

import config


pygame.font.init()
pygame.freetype.init()
system_font = pygame.freetype.get_default_font()
text = pygame.freetype.SysFont(system_font, 15)


class GUI:
    """Rendering instructions and information for the user"""

    GUI_start_coordinates = 30, 30
    text_spacing_vertical = 22

    def __init__(self):

        self.display_coordinates = GUI.GUI_start_coordinates
        self.labels = []

    # noinspection PyPep8Naming
    def render(self, last_measured_UPS):

        self.labels = []

        self.labels.append("UPS: " + str(last_measured_UPS))
        self.labels.append("Boid Count: " + str(config.num_boids))
        self.labels.append("")
        # self.labels.append("UPS: " + str(last_measured_UPS))
        if config.paused:
            self.labels.append("(Space) Resume")
        else:
            self.labels.append("(Space) Pause")
        self.labels.append("(R) Restart")
        self.labels.append("(M) Mode: " + config.modes[config.mode])
        if config.debug_mode:
            self.labels.append("(D) Debug: On")
        else:
            self.labels.append("(D) Debug: Off")
        self.labels.append("(W) Walls")
        self.labels.append("(Q) Quit")

        num_lines = len(self.labels) - 1

        config.gui_height = GUI.text_spacing_vertical + num_lines * 24

        gui_background = pygame.Rect(20, 20, 150, config.gui_height)
        pygame.draw.rect(pygame.display.get_surface(),
                         (62, 62, 66),
                         gui_background)

        for label in self.labels:
            self.render_label(label)

        self.display_coordinates = GUI.GUI_start_coordinates    # Reset the coordinate for the next cycle

    def render_label(self, words):
        """Decides where the next string will appear in the menu"""

        text.render_to(pygame.display.get_surface(),
                       self.display_coordinates,
                       words,
                       (200, 200, 200))

        self.display_coordinates = self.display_coordinates[0], self.display_coordinates[1] + GUI.text_spacing_vertical
