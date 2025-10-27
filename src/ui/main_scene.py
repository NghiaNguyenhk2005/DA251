import pygame

MAIN_MENU_IMG = "assets/images/ui/main-button.png"

class Button:
    def __init__(self, position: tuple[int, int], image: pygame.Surface, scale: int=1) -> None:
        self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = position

    def draw(self, screen: pygame.Surface):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class MainSceneUi:
    def __init__(self) -> None:
        pass
    def draw(self):
        pass
