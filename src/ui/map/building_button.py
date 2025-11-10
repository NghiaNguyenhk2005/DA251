import pygame
from typing import Callable, Optional
from ..tooltip import Tooltip

OFFICE_MAP_SCENE_IMG = "assets/images/ui/office-map-scene.png"
TOA_THI_CHINH_IMG = "assets/images/ui/toa-chi-chinh.png"


class BuildingButton:
    """Button cho các tòa nhà trên bản đồ"""
    def __init__(self, image_path: str, position: tuple[int, int], 
                 scale: float = 1.0, building_id: str = "", 
                 tooltip_text: str = ""):
        """
        Args:
            image_path: Đường dẫn đến ảnh của tòa nhà
            position: Vị trí (x, y) trên bản đồ (tọa độ tương đối trong popup)
            scale: Tỷ lệ scale của ảnh
            building_id: ID của tòa nhà (để callback biết tòa nào được click)
            tooltip_text: Text to display in tooltip when hovering
        """
        self.building_id = building_id
        
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







    
