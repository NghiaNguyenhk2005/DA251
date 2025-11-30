import pygame
from .button import Button
from .map_button import MapButton
from .popups import MenuPopup
from typing import Optional, Callable

MAIN_MENU_IMG = "src/assets/images/ui/menu-button.png"
MAP_IMG = "src/assets/images/ui/map-button.png"
JOURNAL_IMG = "src/assets/images/ui/journal-button.png"
MAP_SCENE_IMG = "src/assets/images/ui/map_scene.png"
OFFICE_MAP_SCENE_IMG = "src/assets/images/ui/office-map-scene.png"
TOA_THI_CHINH_IMG = "src/assets/images/ui/toa-chi-chinh.png"


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
        
        menu_img = pygame.image.load(MAIN_MENU_IMG)
        journal_img = pygame.image.load(JOURNAL_IMG)
        map_img = pygame.image.load(MAP_IMG)
        
        self.menu_popup = MenuPopup(screen_width, screen_height)
        self.menu_button = Button(
            position=(10, 10), 
            image=menu_img, 
            scale=2, 
            split=3,
            on_click=lambda: self.menu_popup.toggle()
        )
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
        if self.menu_popup.is_open():
            self.menu_popup.handle_event(event)
            return

        self.map_button.handle_event(event)
    
    def update(self):
        """Cập nhật trạng thái UI"""
        self.menu_button.update()
        self.journal_button.update()
        self.map_button.update()
        
        if self.menu_popup.is_open():
            self.menu_popup.update()

    def draw(self, screen: pygame.Surface):

        self.menu_button.draw(screen)
        self.journal_button.draw(screen)
        self.map_button.draw(screen)
        
        if self.menu_popup.is_open():
            self.menu_popup.draw(screen)
