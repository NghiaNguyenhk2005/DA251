import pygame
from .button import Button
from .map.building_button import *

MAP_SCENE_IMG = "assets/images/ui/map_scene.png"
CLOSE_BUTTON_IMG = "assets/images/ui/close-button.png"

class MapButton(Button):
    """Button để mở/đóng popup bản đồ"""
    def __init__(self, position: tuple[int, int], image: pygame.Surface, 
            screen_width: int, screen_height: int, scale: int=1, split: int=3
        ) -> None:
        """
        Args:
            position: Vị trí button
            image: Ảnh button
            screen_width: Chiều rộng màn hình
            screen_height: Chiều cao màn hình
            scale: Tỷ lệ scale
            split: Số frame trong sprite sheet
        """
        super().__init__(position, image, scale, split)
        self.map_popup = MapPopup(screen_width, screen_height)
    
    def update(self, delta_time: float = 0):
        super().update()
        """Cập nhật trạng thái button và xử lý click"""
        # Kiểm tra nếu button được click (chuyển từ không click sang click)
        if self.is_pressed():
            self.map_popup.toggle()
        
        # Cập nhật building buttons trong popup
        self.map_popup.update()
    
    def handle_event(self, event):
        """Xử lý sự kiện cho popup"""
        self.map_popup.handle_event(event)
    
    def draw(self, screen: pygame.Surface):
        """Vẽ button và popup (nếu đang mở)"""
        # Vẽ button
        super().draw(screen)
        
        # Vẽ popup nếu đang mở
        self.map_popup.draw(screen)

class MapPopup:
    """Popup window hiển thị bản đồ"""
    def __init__(self, screen_width: int, screen_height: int):
        """
        Args:
            screen_width: Chiều rộng màn hình
            screen_height: Chiều cao màn hình
            on_building_click: Callback khi click vào tòa nhà (nhận building_id)
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
            split=3
        )
        self.is_open = False
        self.was_clicked = False
        
        # Khởi tạo các building buttons
        self.building_buttons = self._create_building_buttons()
    
    def _create_building_buttons(self) -> list[BuildingButton]:
        """
        Tạo các building buttons trên bản đồ
        
        Returns:
            List các BuildingButton
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
    
    def toggle(self):
        """Bật/tắt popup"""
        self.is_open = not self.is_open
        if self.is_open:
            print(f"\n[MapPopup] Popup opened - Map size: {self.map_image.get_size()}")
            print(f"[MapPopup] Popup rect: {self.popup_rect}")
            print(f"[MapPopup] Map position: {self.map_pos}")
            print(f"[MapPopup] Number of buildings: {len(self.building_buttons)}\n")
    
    def handle_event(self, event):
        """Xử lý sự kiện click để đóng popup"""
        if not self.is_open:
            return
        
        # Click vào nút "close_button" để đóng
        if self.close_button.was_clicked():
            self.is_open = False
        # Click bên ngoài popup để đóng
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if not self.popup_rect.collidepoint(mouse_pos):
                self.is_open = False
    
    def update(self):
        """Cập nhật trạng thái của các building buttons"""
        if not self.is_open:
            return
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
        self.close_button.update()
        
        # Cập nhật tất cả building buttons
        for button in self.building_buttons:
            button.update(mouse_pos, mouse_pressed, self.map_pos)

    def draw(self, screen: pygame.Surface):
        """Vẽ popup nếu đang mở"""
        if not self.is_open:
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
        
        # # Vẽ nút đóng (X)
        # pygame.draw.rect(screen, (220, 50, 50), self.close_button_rect)
        # pygame.draw.rect(screen, (150, 30, 30), self.close_button_rect, 2)
        #
        # # Vẽ chữ X
        # font = pygame.font.Font(None, 30)
        # close_text = font.render("X", True, (255, 255, 255))
        # text_rect = close_text.get_rect(center=self.close_button_rect.center)
        # screen.blit(close_text, text_rect)

        self.close_button.draw(screen=screen)
        
        # Vẽ tooltip khi hover vào tòa nhà
        for button in self.building_buttons:
            button.draw_tooltip(screen)
