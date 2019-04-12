import config
import pygame.freetype


pygame.font.init()
pygame.freetype.init()
system_font = pygame.freetype.get_default_font()
text = pygame.freetype.SysFont(system_font, 15)


# noinspection PyPep8Naming
# @staticmethod
def render(last_measured_UPS):

    gui_background = pygame.Rect(0, 0, 150, 120)
    pygame.draw.rect(pygame.display.get_surface(),
                     (170, 170, 170),
                     gui_background)

    top_border_spacing = 10
    text_spacing = 22

    add_label("UPS: " + str(last_measured_UPS), top_border_spacing)
    top_border_spacing += text_spacing
    add_label("(Space) Pause", top_border_spacing)
    top_border_spacing += text_spacing
    add_label("(R) Restart", top_border_spacing)
    top_border_spacing += text_spacing
    add_label("(S) Species: " + str(config.num_of_species_to_display), top_border_spacing)
    top_border_spacing += text_spacing
    add_label("(P) Predator Vision", top_border_spacing)


# @staticmethod
def add_label(words, top_spacing):

    left_border_spacing = 10

    text.render_to(pygame.display.get_surface(),
                   (left_border_spacing, top_spacing),
                   words)
