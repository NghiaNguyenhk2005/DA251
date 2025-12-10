import pygame
from interfaces import Drawable, Updatable
from .button import Button, TextButton
from .map.building_button import *

MAP_SCENE_IMG = "assets/images/ui/map_scene.png"
CLOSE_BUTTON_IMG = "assets/images/ui/close-button.png"


class MapPopup(Drawable, Updatable):
    """Popup window hiển thị bản đồ"""
    def __init__(self, screen_width: int, screen_height: int, on_building_click: Optional[Callable[[str], Any]] = None):
        """
        Args:
            screen_width: Chiều rộng màn hình
            screen_height: Chiều cao màn hình
            on_building_click: Callback khi click vào tòa nhà
        """
        # Load ảnh bản đồ
        self.map_image = pygame.image.load(MAP_SCENE_IMG)
        
        # Tính toán kích thước popup (80% màn hình)
        popup_width = int(screen_width * 0.8)
        popup_height = int(screen_height * 0.8)
        
        # Scale ảnh bản đồ vừa với popup
        self.map_image = pygame.transform.scale(self.map_image, (popup_width - 40, popup_height - 40))
        
        # Tạo background cho popup (semi-transparent)
        self.overlay = pygame.Surface((screen_width, screen_height))
        self.overlay.set_alpha(180)
        self.overlay.fill((0, 0, 0))
        
        # Tạo popup window
        self.popup_rect = pygame.Rect(
            (screen_width - popup_width) // 2,
            (screen_height - popup_height) // 2,
            popup_width,
            popup_height
        )
        
        # Vị trí của bản đồ trong popup
        self.map_pos = (self.popup_rect.x + 20, self.popup_rect.y + 20)
        
        # Tạo nút đóng
        self.close_button = Button(
            position=(self.popup_rect.right-80,self.popup_rect.top + 40),
            image=pygame.image.load(CLOSE_BUTTON_IMG),
            scale=2,
            split=3,
            on_click=lambda: self.toggle()
        )
        self._is_open = False
        self.was_clicked = False
        
        # Khởi tạo các building buttons
        self.building_buttons = self._create_building_buttons()

        # init on_click for building_buttons
        for building in self.building_buttons:
            building.on_click = on_building_click

    def is_open(self) -> bool:
        """
        Kiểm tra xem popup có đang mở không
        
        Returns:
            bool: True nếu popup đang mở, False nếu không
        """
        return self._is_open
    
    def _create_building_buttons(self) -> list[BuildingButton]:
        """
        Tạo các building buttons trên bản đồ
        
        Returns:
            list[BuildingButton]: Danh sách các BuildingButton
        """
        buttons = []
        
        # OFFICE BUILDING
        # Điều chỉnh SCALE và POSITION ở đây:
        office_button = BuildingButton(
            image_path=OFFICE_MAP_SCENE_IMG,
            position=(330, 70),  # Vị trí X, Y trên bản đồ
            scale=0.05,  # <-- ĐIỀU CHỈNH SCALE TẠI ĐÂY (0.1 = 10%, 0.5 = 50%, 1.0 = 100%)
            building_id="office",
            tooltip_text="Office Building"
        )
        buttons.append(office_button)
        print(f"[MapPopup] Office button created - Original: {office_button.original_image.get_size()}, Scaled: {office_button.image.get_size()}")
        
        # TÒA THI CHÍNH
        # Điều chỉnh SCALE và POSITION ở đây:
        toa_thi_chinh_button = BuildingButton(
            image_path=TOA_THI_CHINH_IMG,
            position=(360, 220),  # Vị trí X, Y trên bản đồ
            scale=0.05,  # <-- ĐIỀU CHỈNH SCALE TẠI ĐÂY (0.1 = 10%, 0.5 = 50%, 1.0 = 100%)
            building_id="toa_thi_chinh",
            tooltip_text="Tòa Thị Chính"
        )
        buttons.append(toa_thi_chinh_button)
        print(f"[MapPopup] Tòa Thi Chính button created - Original: {toa_thi_chinh_button.original_image.get_size()}, Scaled: {toa_thi_chinh_button.image.get_size()}")
        
        return buttons
    
    def close(self):
        """Đóng popup một cách tường minh."""
        self._is_open = False

    def toggle(self):
        """Bật/tắt popup"""
        self._is_open = not self._is_open
        if self._is_open:
            print(f"\n[MapPopup] Popup opened - Map size: {self.map_image.get_size()}")
            print(f"[MapPopup] Popup rect: {self.popup_rect}")
            print(f"[MapPopup] Map position: {self.map_pos}")
            print(f"[MapPopup] Number of buildings: {len(self.building_buttons)}\n")
    
    def handle_event(self, event):
        """
        Xử lý sự kiện click để đóng popup
        
        Chỉ xử lý sự kiện đóng popup khi click bên ngoài.
        Logic xử lý click của self.close_button được thực hiện trong update().
        
        Args:
            event: Sự kiện pygame cần xử lý
        """
        if not self._is_open:
            return
        
        # Dòng này đã bị loại bỏ để khắc phục lỗi 'Button' object has no attribute 'handle_event'
        # self.close_button.handle_event(event) 
        
        # Bổ sung logic đóng bằng phím ESC (tùy chọn)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.close()

        # Click bên ngoài popup để đóng
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if not self.popup_rect.collidepoint(mouse_pos):
                self.close() # SỬ DỤNG close() ĐỂ KHẮC PHỤC LỖI AttributeEror

    
    def update(self, delta_time: float = 0):
        # ... (Phần update giữ nguyên)
        """
        Cập nhật trạng thái của MapPopup
        
        Cập nhật trạng thái của close button và tất cả building buttons trên bản đồ.
        Chỉ hoạt động khi popup đang mở.
        """
        if not self._is_open:
            return
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        self.close_button.update()
        
        # Cập nhật tất cả building buttons
        for button in self.building_buttons:
            # Lưu ý: BuildingButton.update() nhận mouse_pos, mouse_pressed, offset
            button.update(mouse_pos, mouse_pressed, self.map_pos)

    def draw(self, screen: pygame.Surface):
        """Vẽ popup nếu đang mở"""
        if not self._is_open:
            return
        
        # Vẽ overlay tối
        screen.blit(self.overlay, (0, 0))
        
        # Vẽ popup background (màu trắng với viền)
        pygame.draw.rect(screen, (255, 255, 255), self.popup_rect)
        pygame.draw.rect(screen, (50, 50, 50), self.popup_rect, 3)
        
        # Vẽ ảnh bản đồ
        screen.blit(self.map_image, self.map_pos)
        
        # Vẽ các building buttons trên bản đồ
        for button in self.building_buttons:
            button.draw(screen, offset=self.map_pos)

        self.close_button.draw(screen=screen)
        
        # Vẽ tooltip khi hover vào tòa nhà
        for button in self.building_buttons:
            button.draw_tooltip(screen)

class MenuPopup(Updatable, Drawable):
    """Popup menu với các buttons Settings, Resume, và Quit"""
    
    def __init__(self, screen_width: int = 800, screen_height: int = 600) -> None:
        """
        Khởi tạo popup menu với các buttons Settings, Resume, và Quit
        
        Args:
            screen_width: Chiều rộng màn hình
            screen_height: Chiều cao màn hình
        """
        self._is_open: bool = False
        # Calculate center position for buttons
        center_x = screen_width // 2 - 75  # Approximate button center
        start_y = screen_height // 2 - 60
        
        # Settings button
        self.resume_button = TextButton(
            position=(center_x, start_y),
            text="Resume",
            font_size=32,
            padding=10,
            normal_bg=(70, 70, 70),
            normal_text=(255, 255, 255),
            hover_bg=(120, 120, 120),
            hover_text=(255, 255, 255),
            click_bg=(50, 50, 50),
            click_text=(200, 200, 200),
            border_color=(200, 200, 200),
            border_width=2,
            on_click=lambda: self.toggle()
        )
        
        # Resume button
        self.settings_button = TextButton(
            position=(center_x, start_y + 70),
            text="Settings",
            font_size=32,
            padding=10,
            normal_bg=(85, 85, 85),
            normal_text=(255, 255, 255),
            hover_bg=(135, 135, 135),
            hover_text=(255, 255, 255),
            click_bg=(65, 65, 65),
            click_text=(200, 200, 200),
            border_color=(200, 200, 200),
            border_width=2
        )
        
        # Quit button
        self.quit_button = TextButton(
            position=(center_x, start_y + 140),
            text="Quit",
            font_size=32,
            padding=10,
            normal_bg=(100, 100, 100),
            normal_text=(255, 255, 255),
            hover_bg=(150, 150, 150),
            hover_text=(255, 255, 255),
            click_bg=(80, 80, 80),
            click_text=(200, 200, 200),
            border_color=(200, 200, 200),
            border_width=2
        )

    def toggle(self):
        """Bật/tắt trạng thái mở của menu popup"""
        if self.is_open():
            self._is_open = False
        else:
            self._is_open = True

    def is_open(self) -> bool:
        """
        Kiểm tra xem menu popup có đang mở không
        
        Returns:
            bool: True nếu menu đang mở, False nếu không
        """
        return self._is_open
    
    def update(self, delta_time: float = 0):
        """
        Cập nhật trạng thái của MenuPopup
        
        Cập nhật trạng thái của tất cả các menu buttons (Resume, Settings, Quit).
        Chỉ hoạt động khi menu đang mở.
        """
        if self._is_open:
            # Update button states
            self.resume_button.update()
            self.settings_button.update()
            self.quit_button.update()

    def handle_event(self, event: pygame.event.Event):
        """
        Xử lý sự kiện pygame (hiện tại không sử dụng)
        
        Args:
            event: Sự kiện pygame cần xử lý
        """
        pass

    def draw(self, screen: pygame.Surface):
        """
        Vẽ tất cả menu buttons lên màn hình
        
        Args:
            screen: Surface để vẽ menu lên
        """
        if self._is_open:
            self.settings_button.draw(screen)
            self.resume_button.draw(screen)
            self.quit_button.draw(screen)
