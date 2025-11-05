import pygame
from typing import Callable, Optional
from .button import Button
from .tooltip import Tooltip

MAP_SCENE_IMG = "assets/images/ui/map_scene.png"
OFFICE_MAP_SCENE_IMG = "assets/images/ui/office-map-scene.png"
TOA_THI_CHINH_IMG = "assets/images/ui/toa-chi-chinh.png"
CLOSE_BUTTON_IMG = "assets/images/ui/close-button.png"


class BuildingButton:
    """Button cho các tòa nhà trên bản đồ"""
    def __init__(self, image_path: str, position: tuple[int, int], 
                 scale: float = 1.0, building_id: str = "", 
                 on_click: Optional[Callable[[str], None]] = None,
                 tooltip_text: str = ""):
        """
        Args:
            image_path: Đường dẫn đến ảnh của tòa nhà
            position: Vị trí (x, y) trên bản đồ (tọa độ tương đối trong popup)
            scale: Tỷ lệ scale của ảnh
            building_id: ID của tòa nhà (để callback biết tòa nào được click)
            on_click: Callback function khi click vào tòa nhà
            tooltip_text: Text to display in tooltip when hovering
        """
        self.building_id = building_id
        self.on_click = on_click
        
        # Load và scale ảnh
        self.original_image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(
            self.original_image,
            (int(self.original_image.get_width() * scale),
             int(self.original_image.get_height() * scale))
        )
        
        # Tạo rect cho collision detection
        self.rect = self.image.get_rect(topleft=position)
        
        # Trạng thái
        self.is_hovered = False
        self.was_clicked = False
        
        # Hiệu ứng hover (tăng độ sáng)
        self.hover_overlay = pygame.Surface(self.image.get_size())
        self.hover_overlay.set_alpha(50)
        self.hover_overlay.fill((255, 255, 100))  # Màu vàng nhạt
        
        # Tooltip
        self.tooltip = Tooltip(tooltip_text) if tooltip_text else None
    
    def update(self, mouse_pos: tuple[int, int], mouse_pressed: bool, popup_offset: tuple[int, int]):
        """
        Cập nhật trạng thái của button
        
        Args:
            mouse_pos: Vị trí chuột
            mouse_pressed: Chuột có đang được nhấn không
            popup_offset: Offset của popup (để tính toán vị trí thực tế)
        """
        # Tính toán vị trí thực tế của button trên màn hình
        actual_rect = self.rect.copy()
        actual_rect.x += popup_offset[0]
        actual_rect.y += popup_offset[1]
        
        # Kiểm tra hover
        self.is_hovered = actual_rect.collidepoint(mouse_pos)
        
        # Kiểm tra click
        if self.is_hovered and mouse_pressed and not self.was_clicked:
            self.was_clicked = True
            if self.on_click:
                self.on_click(self.building_id)
        elif not mouse_pressed:
            self.was_clicked = False
    
    def draw(self, surface: pygame.Surface, offset: tuple[int, int] = (0, 0)):
        """
        Vẽ building button
        
        Args:
            surface: Surface để vẽ lên
            offset: Offset vị trí (thường là vị trí của bản đồ trong popup)
        """
        # Vẽ ảnh tòa nhà
        draw_pos = (self.rect.x + offset[0], self.rect.y + offset[1])
        surface.blit(self.image, draw_pos)
        
        # Vẽ hiệu ứng hover
        if self.is_hovered:
            surface.blit(self.hover_overlay, draw_pos)
            
            # Vẽ viền sáng khi hover
            actual_rect = self.rect.copy()
            actual_rect.x += offset[0]
            actual_rect.y += offset[1]
            pygame.draw.rect(surface, (255, 255, 0), actual_rect, 3)

            if self.was_clicked:
                pygame.draw.rect(surface, (255, 0, 0), actual_rect, 3)
    
    def draw_tooltip(self, surface: pygame.Surface):
        """
        Draw tooltip if button is hovered and tooltip exists
        
        Args:
            surface: Surface to draw on
        """
        if self.is_hovered and self.tooltip:
            mouse_pos = pygame.mouse.get_pos()
            self.tooltip.draw(surface, mouse_pos)



class MapPopup:
    """Popup window hiển thị bản đồ"""
    def __init__(self, screen_width: int, screen_height: int, 
                 on_building_click: Optional[Callable[[str], None]] = None):
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
        # self.close_button_rect = pygame.Rect(
        #     self.popup_rect.right - 40,
        #     self.popup_rect.top + 10,
        #     30,
        #     30
        # )
        
        self.is_open = False
        self.was_clicked = False
        
        # Khởi tạo các building buttons
        self.building_buttons = self._create_building_buttons(on_building_click)
    
    def _create_building_buttons(self, on_click: Optional[Callable[[str], None]]) -> list[BuildingButton]:
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
            on_click=on_click,
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
            on_click=on_click,
            tooltip_text="Tòa Thi Chính"
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
        
        # Click vào nút X để đóng
        if self.close_button.is_clicked():
            self.is_open = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Click vào nút X để đóng
            # if self.close_button.is_clicked():
            #     self.is_open = False
            # Click bên ngoài popup để đóng
            if not self.popup_rect.collidepoint(mouse_pos):
                self.is_open = False
    
    def update(self):
        """Cập nhật trạng thái của các building buttons"""
        if not self.is_open:
            return
        
        mouse_pos = pygame.mouse.get_pos()
        mouse_pressed = pygame.mouse.get_pressed()[0]
        
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


class MapButton(Button):
    """Button để mở/đóng popup bản đồ"""
    def __init__(self, position: tuple[int, int], image: pygame.Surface, 
                 screen_width: int, screen_height: int, scale: int=1, split: int=3,
                 on_building_click: Optional[Callable[[str], None]] = None) -> None:
        """
        Args:
            position: Vị trí button
            image: Ảnh button
            screen_width: Chiều rộng màn hình
            screen_height: Chiều cao màn hình
            scale: Tỷ lệ scale
            split: Số frame trong sprite sheet
            on_building_click: Callback khi click vào tòa nhà trên bản đồ
        """
        super().__init__(position, image, scale, split)
        self.map_popup = MapPopup(screen_width, screen_height, on_building_click)
        self.was_clicked = False
    
    def update(self):
        """Cập nhật trạng thái button và xử lý click"""
        # Kiểm tra nếu button được click (chuyển từ không click sang click)
        if self.is_clicked() and not self.was_clicked:
            self.map_popup.toggle()
            self.was_clicked = True
        elif not self.is_clicked():
            self.was_clicked = False
        
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
    
