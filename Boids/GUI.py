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

    start = 10
    spacing = 22

    print_gui_text("UPS: " + str(last_measured_UPS), start)
    start += spacing
    print_gui_text("(Space) Pause", start)
    start += spacing
    print_gui_text("(R) Restart", start)
    start += spacing
    print_gui_text("(S) Species: " + str(config.num_of_species), start)
    start += spacing
    print_gui_text("(P) Predator Vision", start)
    start += spacing


# @staticmethod
def print_gui_text(words, y):

    text.render_to(pygame.display.get_surface(),
                   (10, y),
                   words)
