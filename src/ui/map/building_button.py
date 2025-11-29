import pygame
from typing import Any, Callable, Optional
from ..tooltip import Tooltip

OFFICE_MAP_SCENE_IMG = "assets/images/ui/office-map-scene.png"
TOA_THI_CHINH_IMG = "assets/images/ui/toa-chi-chinh.png"


class BuildingButton:
    """Button cho các tòa nhà trên bản đồ"""
    def __init__(self, image_path: str, position: tuple[int, int], 
                 scale: float = 1.0, building_id: str = "", 
                 tooltip_text: str = "",
                 on_click: Optional[Callable[[str], Any]] = None):
        """
        Khởi tạo button cho tòa nhà trên bản đồ
        
        Args:
            image_path: Đường dẫn đến ảnh của tòa nhà
            position: Vị trí (x, y) trên bản đồ (tọa độ tương đối trong popup)
            scale: Tỷ lệ scale của ảnh
            building_id: ID của tòa nhà (để callback biết tòa nào được click)
            tooltip_text: Văn bản hiển thị trong tooltip khi hover
            on_click: Hàm callback khi click vào tòa nhà
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

        self.on_click = on_click
    
    def update(self, mouse_pos: tuple[int, int], mouse_pressed: bool, popup_offset: tuple[int, int]):
        """
        Cập nhật trạng thái của building button
        
        Kiểm tra hover và click, gọi callback nếu button được click
        
        Args:
            mouse_pos: Vị trí chuột (x, y)
            mouse_pressed: Chuột có đang được nhấn không
            popup_offset: Offset của popup (để tính toán vị trí thực tế của button)
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
        
        # Reset was_clicked when mouse is released
        if not mouse_pressed:
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
        Vẽ tooltip nếu button đang được hover và tooltip tồn tại
        
        Args:
            surface: Surface để vẽ tooltip lên
        """
        if self.is_hovered and self.tooltip:
            mouse_pos = pygame.mouse.get_pos()
            self.tooltip.draw(surface, mouse_pos)







    
