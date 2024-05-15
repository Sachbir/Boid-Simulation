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

    # noinspection PyPep8Naming
    def render(self, last_measured_UPS):

        num_lines = 5

        gui_background = pygame.Rect(20, 20, 150, GUI.text_spacing_vertical + num_lines * 24)
        pygame.draw.rect(pygame.display.get_surface(),
                         (62, 62, 66),
                         gui_background)

        self.add_label("UPS: " + str(last_measured_UPS))
        if config.paused:
            self.add_label("(Space) Resume")
        else:
            self.add_label("(Space) Pause")
        self.add_label("(R) Restart")
        self.add_label("(M) Mode: " + config.modes[config.mode])
        if config.debug_mode:
            self.add_label("(D) Debug: On")
        else:
            self.add_label("(D) Debug: Off")
        self.add_label("(Q) Quit")

        self.display_coordinates = GUI.GUI_start_coordinates    # Reset the coordinate for the next cycle

    def add_label(self, words):
        """Decides where the next string will appear in the menu"""

        text.render_to(pygame.display.get_surface(),
                       self.display_coordinates,
                       words,
                       (200, 200, 200))

        self.display_coordinates = self.display_coordinates[0], self.display_coordinates[1] + GUI.text_spacing_vertical
