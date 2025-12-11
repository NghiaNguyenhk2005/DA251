import pygame
from typing import Callable, Optional
from .button import Button
from .tooltip import Tooltip
# FIX: Import MapPopup từ popups.py (khắc phục lỗi trùng lặp)
from .popups import MapPopup

MAP_SCENE_IMG = "assets/images/ui/map_scene.png"
OFFICE_MAP_SCENE_IMG = "assets/images/ui/office-map-scene.png"
TOA_THI_CHINH_IMG = "assets/images/ui/toa-chi-chinh.png"
CLOSE_BUTTON_IMG = "assets/images/ui/close-button.png"

# Sin Icons (7 deadly sins)
GREED_ICON = "assets/images/ui/greed-icon.png"
ENVY_ICON = "assets/images/ui/envy-icon.png"
WRATH_ICON = "assets/images/ui/wrath-icon.png"
SLOTH_ICON = "assets/images/ui/sloth-icon.png"
GLUTTONY_ICON = "assets/images/ui/gluttony-icon.png"
LUST_ICON = "assets/images/ui/lust-icon.png"
PRIDE_ICON = "assets/images/ui/pride-icon.png"


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
        
        # Load và scale ảnh (GIỮ NGUYÊN SCALE)
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
        """
        # Tính toán vị trí thực tế của button trên màn hình
        actual_rect = self.rect.copy()
        actual_rect.x += popup_offset[0]
        actual_rect.y += popup_offset[1]
        
        # Kiểm tra hover
        self.is_hovered = actual_rect.collidepoint(mouse_pos)
        
        # Kiểm tra click
        if self.is_hovered and mouse_pressed and not self.was_clicked:
            # Bắt đầu click
            self.was_clicked = True
        elif self.was_clicked and not mouse_pressed:
            # Nhả chuột sau khi click (thực hiện action)
            if self.on_click:
                self.on_click(self.building_id)
            self.was_clicked = False
        elif not self.is_hovered and not mouse_pressed:
            # Reset nếu chuột nhả ra ngoài
            self.was_clicked = False
    
    def draw(self, surface: pygame.Surface, offset: tuple[int, int] = (0, 0)):
        """
        Vẽ building button
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
        """
        if self.is_hovered and self.tooltip:
            mouse_pos = pygame.mouse.get_pos()
            self.tooltip.draw(surface, mouse_pos)


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
            scale: Tỷ lệ scale (GIỮ NGUYÊN)
            split: Số frame trong sprite sheet
            on_building_click: Callback khi click vào tòa nhà trên bản đồ
        """
        # GIỮ NGUYÊN: super().__init__ không có on_click
        super().__init__(position, image, scale, split)
        self.map_popup = MapPopup(screen_width, screen_height, on_building_click)
        # GIỮ NGUYÊN: self.was_clicked
        self.was_clicked = False
    
    def update(self):
        """Cập nhật trạng thái button và xử lý click"""
        super().update() # Cập nhật self._is_clicked của Button
        
        # GIỮ NGUYÊN: Logic click edge-triggered (khắc phục lỗi gọi 2 lần, giữ nguyên hành vi cũ)
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