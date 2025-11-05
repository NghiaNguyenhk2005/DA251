import pygame
from typing import Optional, Callable

MAIN_MENU_IMG = "assets/images/ui/menu-button.png"
MAP_IMG = "assets/images/ui/map-button.png"
JOURNAL_IMG = "assets/images/ui/journal-button.png"
MAP_SCENE_IMG = "assets/images/ui/map_scene.png"
OFFICE_MAP_SCENE_IMG = "assets/images/ui/office-map-scene.png"
TOA_THI_CHINH_IMG = "assets/images/ui/toa-chi-chinh.png"

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
    def __init__(self, screen_width: int = 800, screen_height: int = 600,
                 on_building_click: Optional[Callable[[str], None]] = None) -> None:
        """
        Args:
            screen_width: Chiều rộng màn hình
            screen_height: Chiều cao màn hình
            on_building_click: Callback khi click vào tòa nhà (nhận building_id: str)
                              Ví dụ: lambda building_id: print(f"Chuyển đến scene: {building_id}")
        """
        # Import MapButton ở đây để tránh circular import
        from map_button import MapButton
        
        menu_img = pygame.image.load(MAIN_MENU_IMG)
        journal_img = pygame.image.load(JOURNAL_IMG)
        map_img = pygame.image.load(MAP_IMG)
        
        self.menu_button = Button(position=(10, 10), image=menu_img, scale=2, split=5)
        self.map_button = MapButton(
            position=(10, self.menu_button.rect.bottom + 10), 
            image=map_img, 
            screen_width=screen_width, 
            screen_height=screen_height,
            scale=2, 
            split=3,
            on_building_click=on_building_click or self._default_building_click_handler
        )
        self.journal_button = Button(position=(10, self.map_button.rect.bottom + 10), image=journal_img, scale=2, split=3)
    
    def _default_building_click_handler(self, building_id: str):
        """
        Handler mặc định khi click vào tòa nhà (nếu không có callback được cung cấp)
        
        Args:
            building_id: ID của tòa nhà được click ("office", "toa_thi_chinh", etc.)
        """
        print(f"[MainSceneUi] Building clicked: {building_id}")
        print(f"[MainSceneUi] TODO: Implement scene transition to {building_id}")
        # TODO: Thêm logic chuyển scene ở đây
        # Ví dụ: self.game.change_scene(building_id)
    
    def set_building_click_handler(self, handler: Callable[[str], None]):
        """
        Thiết lập callback handler cho building clicks
        
        Args:
            handler: Function nhận building_id và xử lý chuyển scene
        """
        self.map_button.map_popup.building_buttons[0].on_click = handler
        self.map_button.map_popup.building_buttons[1].on_click = handler
    
    def handle_event(self, event):
        """Xử lý sự kiện cho các button"""
        self.map_button.handle_event(event)
    
    def update(self):
        """Cập nhật trạng thái UI"""
        self.map_button.update()

    def draw(self, screen: pygame.Surface):
        self.menu_button.draw(screen)
        self.journal_button.draw(screen)
        self.map_button.draw(screen)
