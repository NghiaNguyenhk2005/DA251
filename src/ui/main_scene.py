import pygame
from .button import Button
# Đảm bảo MapPopup và MenuPopup được import từ cùng một thư mục hoặc thư mục cha
# Tôi giả định chúng nằm trong .popups
from .popups import MenuPopup, MapPopup # Thêm MapPopup
from typing import Optional, Callable, Any, Union

# Giữ nguyên các hằng số
MAIN_MENU_IMG = "assets/images/ui/menu-button.png"
MAP_IMG = "assets/images/ui/map-button.png"
JOURNAL_IMG = "assets/images/ui/journal-button.png"
MAP_SCENE_IMG = "assets/images/ui/map_scene.png"
OFFICE_MAP_SCENE_IMG = "assets/images/ui/office-map-scene.png"
TOA_THI_CHINH_IMG = "assets/images/ui/toa-chi-chinh.png"

# Thêm interface nếu cần, nhưng tôi loại bỏ chúng để đơn giản hóa như file gốc của bạn.
# class MainSceneUi(Updatable, Drawable): 
class MainSceneUi:
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
        # Sử dụng on_building_click handler trực tiếp trong MapPopup
        self.menu_popup: MenuPopup = MenuPopup(screen_width=screen_width, screen_height=screen_height)
        self.map_popup: MapPopup = MapPopup(
            screen_width=screen_width,
            screen_height=screen_height,
            # Nếu on_building_click không được cung cấp, sử dụng handler mặc định
            on_building_click=on_building_click or self._default_building_click_handler
        )

        # init buttons
        self.menu_button = Button(
            position=(10, 10),
            image=menu_img,
            scale=2,
            split=3,
            on_click=lambda: self.menu_popup.toggle()
        )
        # MapButton đã được thay thế bằng Button
        self.map_button = Button(
            position=(10, self.menu_button.rect.bottom + 10), 
            image=map_img,
            scale=2,
            split=3,
            on_click=lambda: self.map_popup.toggle() # Bật/tắt MapPopup
        )
        self.journal_button = Button(
            position=(10, self.map_button.rect.bottom + 10),
            image=journal_img,
            scale=2,
            split=3
        )
        
        # init dict for popups and buttons for easier management
        # Dùng Union để định kiểu nếu không muốn import Updatable, Drawable
        self.popups: dict[str, Union[MapPopup, MenuPopup]] = {
            "Menu": self.menu_popup,
            "Map": self.map_popup,
        }

        self.buttons: dict[str, Button] = {
            "Menu": self.menu_button,
            "Map": self.map_button,
            "Journal": self.journal_button
        }
    
    def _default_building_click_handler(self, building_id: str):
        """
        Handler mặc định khi click vào tòa nhà (nếu không có callback được cung cấp)
        """
        print(f"[MainSceneUi] Building clicked: {building_id}")
        print(f"[MainSceneUi] TODO: Implement scene transition to {building_id}")

    def set_building_click_handler(self, handler: Callable[[str], None]):
        """
        Thiết lập callback handler cho building clicks trong MapPopup.
        
        *Lưu ý: MapPopup cần có phương thức tương ứng để cập nhật handler.*
        """
        # Giả sử MapPopup có thuộc tính on_building_click để set
        self.map_popup.on_building_click = handler 
        # Tùy thuộc vào cách MapPopup quản lý BuildingButton, bạn có thể cần set
        # cho từng button trong MapPopup (như cách bạn làm trong phiên bản cũ).

    def handle_event(self, event):
        """Xử lý sự kiện cho các button và popup"""
        is_popup_open: bool = False

        # Xử lý sự kiện cho tất cả các popups
        for popup in self.popups.values():
            popup.handle_event(event=event)
            is_popup_open |= popup.is_open() # Kiểm tra xem có popup nào đang mở không

        # Chỉ xử lí event button khi không có Popup Ui open
        if is_popup_open: 
            return
    def update(self, delta_time: float = 0):
        """
        Cập nhật trạng thái UI
        """
        is_popup_open: bool = False
        
        # Cập nhật popups trước và kiểm tra trạng thái mở
        for popup in self.popups.values():
            popup.update()
            is_popup_open |= popup.is_open()

        # Nếu có popup mở, dừng cập nhật buttons
        if is_popup_open: return

        # Cập nhật buttons
        for button in self.buttons.values():
            button.update()

    def draw(self, screen: pygame.Surface):
        """
        Vẽ UI lên màn hình
        
        Vẽ popup nếu đang mở (ưu tiên Menu > Map), nếu không thì vẽ các buttons
        """
        if self.menu_popup.is_open():
            self.menu_popup.draw(screen=screen)
        elif self.map_popup.is_open():
            self.map_popup.draw(screen=screen)
        else:
            # Vẽ các buttons chỉ khi không có popup nào mở
            self.menu_button.draw(screen)
            self.journal_button.draw(screen)
            self.map_button.draw(screen)