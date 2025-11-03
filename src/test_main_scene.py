import pygame
import sys

from ui.main_scene import MAIN_MENU_IMG, Button, MainSceneUi

pygame.init()

# Screen setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("The se7enth code")
font = pygame.font.SysFont(None, 60)

# Colors
RED = (255, 0, 0)
CYAN = (0, 255, 255)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
BLACK = (0, 0, 0)


def test():
    while True:
        screen.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        main_scene = MainSceneUi()
        main_scene.draw(screen)
        pygame.display.update()

test()
