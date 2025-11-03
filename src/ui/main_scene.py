import pygame

MAIN_MENU_IMG = "assets/images/ui/menu-button.png"
MAP_IMG = "assets/images/ui/map-button.png"
JOURNAL_IMG = "assets/images/ui/journal-button.png"

class Button:
    def __init__(self, position: tuple[int, int], image: pygame.Surface, scale: int=1, split: int=5) -> None:
        self.frame = 0
        self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.frame_width = self.image.get_width() // split
        self.frame_height = self.image.get_height()
        self.rect = pygame.Rect(position[0], position[1], self.frame_width, self.frame_height)
        self._is_hover = False
        self._is_clicked = False

    def draw(self, screen: pygame.Surface):
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.frame = 1
            self._is_hover = True
            if pygame.mouse.get_pressed()[0]: 
                self.frame = 2
                self._is_clicked = True
        else: 
            self.frame = 0
            self._is_clicked = False
            self._is_hover = False
        source_rect = pygame.Rect(self.frame * self.frame_width, 0, self.frame_width, self.frame_height)
        screen.blit(self.image, self.rect, source_rect)

    def is_hover(self):
        return self._is_hover

    def is_clicked(self):
        return self._is_clicked

class MainSceneUi:
    def __init__(self) -> None:
        menu_img = pygame.image.load(MAIN_MENU_IMG)
        journal_img = pygame.image.load(JOURNAL_IMG)
        map_img = pygame.image.load(MAP_IMG)
        self.menu_button = Button(position=(10, 10), image=menu_img, scale=2, split=5)
        self.map_button = Button(position=(10, self.menu_button.rect.bottom + 10), image=map_img, scale=2, split=3)
        self.journal_button = Button(position=(10, self.map_button.rect.bottom + 10), image=journal_img, scale=2, split=3)

    def draw(self, screen: pygame.Surface):
        self.menu_button.draw(screen)
        self.journal_button.draw(screen)
        self.map_button.draw(screen)
