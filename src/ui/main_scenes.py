import pygame

from typing import Any, Optional, Callable, Union

from interfaces import Drawable, Updatable
from .button import Button
from .popups import MenuPopup, MapPopup

MAIN_MENU_IMG = "assets/images/ui/menu-button.png"
MAP_IMG = "assets/images/ui/map-button.png"
JOURNAL_IMG = "assets/images/ui/journal-button.png"
MAP_SCENE_IMG = "assets/images/ui/map_scene.png"
OFFICE_MAP_SCENE_IMG = "assets/images/ui/office-map-scene.png"
TOA_THI_CHINH_IMG = "assets/images/ui/toa-chi-chinh.png"


class MainSceneUi(Updatable, Drawable):
    """UI chính cho các scene trong game, bao gồm các buttons và popups"""
    
    def __init__(
        self,
        screen_width: int = 800,
        screen_height: int = 600,
        on_building_click: Optional[Callable[[str], Any]] = None
    ) -> None:
        """
        Khởi tạo UI chính với các buttons (Menu, Map, Journal) và popups
        
        Args:
            screen_width: Chiều rộng màn hình
            screen_height: Chiều cao màn hình
            on_building_click: Hàm callback khi click vào tòa nhà trên bản đồ
        """
        # load image for buttons
        menu_img = pygame.image.load(MAIN_MENU_IMG)
        journal_img = pygame.image.load(JOURNAL_IMG)
        map_img = pygame.image.load(MAP_IMG)

        # init popups
        self.menu_popup: MenuPopup = MenuPopup(screen_width=screen_width, screen_height=screen_height)
        self.map_popup: MapPopup = MapPopup(
            screen_width=screen_width,
            screen_height=screen_height,
            on_building_click=on_building_click
        )

        # init buttons
        self.menu_button = Button(
            position=(10, 10),
            image=menu_img,
            scale=2,
            split=3,
            on_click=lambda: self.menu_popup.toggle()
        )
        self.map_button = Button(
            position=(10, self.menu_button.rect.bottom + 10), 
            image=map_img,
            scale=2,
            split=3,
            on_click=lambda: self.map_popup.toggle()
        )
        self.journal_button = Button(
            position=(10, self.map_button.rect.bottom + 10),
            image=journal_img,
            scale=2,
            split=3
        )
        
        # init dict for popups and buttons for easier management
        self.popups: dict[str, Union[MapPopup, MenuPopup]] = {
            "Menu": self.menu_popup,
            "Map": self.map_popup,
        }

        self.buttons: dict[str, Button] = {
            "Menu": self.menu_button,
            "Map": self.map_button,
            "Journal": self.journal_button
        }
    
    def handle_event(self, event: pygame.event.Event):
        """
        Xử lý sự kiện pygame cho các button và popup
        
        Args:
            event: Sự kiện pygame cần xử lý
        """
        is_popup_open: bool = False

        for popup in self.popups.values():
            popup.handle_event(event=event)
            is_popup_open |= popup.is_open()

        # Chỉ xử lí event button khi không có Popup Ui open
        if is_popup_open: return

        for button in self.buttons.values():
            button.handle_event(event=event)

    def update(self, delta_time: float = 0):
        """
        Cập nhật trạng thái UI
        
        Cập nhật trạng thái của tất cả các buttons và popups theo thứ tự:
        - Cập nhật các buttons trước
        - Sau đó cập nhật các popups
        """
        is_popup_open: bool = False
        # Update buttons states first
        for popup in self.popups.values():
            popup.update()
            is_popup_open |= popup.is_open()

        # Chỉ update button khi Popup Ui ko open
        if is_popup_open: return

        # Update buttons
        for button in self.buttons.values():
            button.update()

    def draw(self, screen: pygame.Surface):
        """
        Vẽ UI lên màn hình
        
        Vẽ popup nếu đang mở, nếu không thì vẽ các buttons
        
        Args:
            screen: Surface để vẽ UI lên
        """
        if self.menu_popup.is_open():
            self.menu_popup.draw(screen=screen)
        elif self.map_popup.is_open():
            self.map_popup.draw(screen=screen)
        else:
            self.menu_button.draw(screen)
            self.journal_button.draw(screen)
            self.map_button.draw(screen)
