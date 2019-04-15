import config
import pygame.freetype


pygame.font.init()
pygame.freetype.init()
system_font = pygame.freetype.get_default_font()
text = pygame.freetype.SysFont(system_font, 15)


class GUI:

    init_display_coordinates = 10, 10
    text_spacing = 22

    def __init__(self):

        self.display_coordinates = GUI.init_display_coordinates

    # noinspection PyPep8Naming
    def render(self, last_measured_UPS):

        gui_background = pygame.Rect(0, 0, 150, 120)
        pygame.draw.rect(pygame.display.get_surface(),
                         (170, 170, 170),
                         gui_background)

        self.add_label("UPS: " + str(last_measured_UPS))
        self.add_label("(Space) Pause")
        self.add_label("(R) Restart")
        self.add_label("(S) Species: " + str(config.num_of_species_to_display))
        self.add_label("(P) Predator Vision")

        self.display_coordinates = GUI.init_display_coordinates

    def add_label(self, words):

        text.render_to(pygame.display.get_surface(),
                       self.display_coordinates,
                       words)

        self.display_coordinates = self.display_coordinates[0], self.display_coordinates[1] + GUI.text_spacing
