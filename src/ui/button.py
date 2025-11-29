from abc import abstractmethod
from typing import Callable, Optional
import pygame

from interfaces import Drawable, Updatable

class IButton:
    """Interface cơ bản cho các button"""
    @abstractmethod
    def was_clicked(self) -> bool: return False
    def is_pressed(self) -> bool: return False

class Button(IButton, Drawable, Updatable):
    """Button tương tác với các trạng thái hover và click sử dụng sprite frames"""
    
    def __init__(
        self, 
        position: tuple[int, int], 
        image: pygame.Surface, 
        scale: int=1, split: int=5,
        on_click: Optional[Callable[[], None]] = None
    ) -> None:
        """
        Khởi tạo button với animation frames dựa trên sprite
        
        Args:
            position: Vị trí (x, y) của button trên màn hình
            image: Sprite sheet chứa các frame của button (normal, hover, clicked)
            scale: Hệ số scale để thay đổi kích thước ảnh button
            split: Số lượng frames trong sprite sheet (mặc định: 5)
            on_click: Hàm callback khi button được click
        """
        self.frame = 0
        self.image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
        self.frame_width = self.image.get_width() // split
        self.frame_height = self.image.get_height()
        self.rect = pygame.Rect(position[0], position[1], self.frame_width, self.frame_height)
        self._is_hover = False
        self._is_pressed = False
        self._was_clicked = False
        self.on_click = on_click

    def update(self, delta_time: float = 0):
        """
        Cập nhật trạng thái của button dựa trên tương tác chuột
        
        Cập nhật trạng thái button dựa trên hover và click:
        - Kiểm tra xem chuột có đang hover không
        - Phát hiện các lần click (edge-triggered)
        - Cập nhật frame cho trạng thái hiển thị
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.frame = 1
            self._is_hover = True
            if pygame.mouse.get_pressed()[0]:
                self.frame = 2
                if not self._was_clicked:
                    self._is_pressed = True
                    self._was_clicked = True
                    if self.on_click: self.on_click()
                else:
                    self._is_pressed = False
            else:
                self._is_pressed = False
                self._was_clicked = False
        else: 
            self.frame = 0
            self._is_pressed = False
            self._is_hover = False
            self._was_clicked = False

    def draw(self, screen: pygame.Surface):
        """
        Vẽ button với trạng thái hiện tại
        
        Vẽ frame của button dựa trên trạng thái hiện tại:
        - Frame 0: Trạng thái bình thường
        - Frame 1: Trạng thái hover
        - Frame 2: Trạng thái clicked
        
        Args:
            screen: Màn hình game - Surface để vẽ button lên
        """
        source_rect = pygame.Rect(self.frame * self.frame_width, 0, self.frame_width, self.frame_height)
        screen.blit(self.image, self.rect, source_rect)

    def handle_event(self, event: pygame.event.Event):
        """Xử lý sự kiện pygame (hiện tại không sử dụng)"""
        pass

    def is_hover(self):
        """
        Kiểm tra xem chuột có đang hover trên button không
        
        Returns:
            bool: True nếu chuột đang hover, False nếu không
        """
        return self._is_hover

    def is_pressed(self):
        """
        Kiểm tra xem button có đang được click không (level-based - True khi đang giữ)
        
        Để phát hiện edge (sự kiện kích hoạt một lần), sử dụng thuộc tính _was_clicked hoặc method was_clicked().
        was_clicked chỉ True ở frame đầu tiên của click, không phải khi đang giữ.
        
        Returns:
            bool: True nếu button đang được click, False nếu không
        """
        return self._is_pressed
    
    def was_clicked(self):
        """
        Kiểm tra xem button vừa được click không (edge detection - chỉ True ở frame đầu tiên)
        
        Hữu ích cho các sự kiện kích hoạt một lần như toggle, mở dialog, v.v.
        Chỉ trả về True ở lần click đầu tiên, không phải khi button đang được giữ.
        
        Returns:
            bool: True nếu button vừa được click (chỉ frame đầu tiên), False nếu không
        """
        return self._was_clicked


class TextButton(IButton, Drawable, Updatable):
    """Button văn bản tương tác với các trạng thái hover và click"""
    
    def __init__(self, position: tuple[int, int], text: str,
                 on_click: Optional[Callable[[], None]] = None,
                 font_size: int = 32,
                 padding: int = 10,
                 normal_bg: tuple[int, int, int] = (100, 100, 100),
                 normal_text: tuple[int, int, int] = (255, 255, 255),
                 hover_bg: tuple[int, int, int] = (150, 150, 150),
                 hover_text: tuple[int, int, int] = (255, 255, 255),
                 click_bg: tuple[int, int, int] = (80, 80, 80),
                 click_text: tuple[int, int, int] = (200, 200, 200),
                 border_color: tuple[int, int, int] = (200, 200, 200),
                 border_width: int = 2,
                 border_radius: int = 10) -> None:
        """
        Khởi tạo text button với hiển thị trạng thái dựa trên màu sắc
        
        Args:
            position: Vị trí (x, y) của button trên màn hình
            text: Văn bản hiển thị trên button
            on_click: Hàm callback khi button được click
            font_size: Kích thước font cho văn bản button
            padding: Khoảng cách đệm xung quanh văn bản
            normal_bg: Màu nền ở trạng thái bình thường (RGB)
            normal_text: Màu chữ ở trạng thái bình thường (RGB)
            hover_bg: Màu nền ở trạng thái hover (RGB)
            hover_text: Màu chữ ở trạng thái hover (RGB)
            click_bg: Màu nền ở trạng thái clicked (RGB)
            click_text: Màu chữ ở trạng thái clicked (RGB)
            border_color: Màu viền (RGB)
            border_width: Độ dày của viền
            border_radius: Bán kính của góc bo tròn
        """
        self.position = position
        self.text = text
        self.font_size = font_size
        self.padding = padding
        self.on_click = on_click
        
        # State colors
        self.normal_bg = normal_bg
        self.normal_text = normal_text
        self.hover_bg = hover_bg
        self.hover_text = hover_text
        self.click_bg = click_bg
        self.click_text = click_text
        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
        
        # Create font and render text surfaces for each state
        self.font = pygame.font.Font(None, font_size)
        self.text_surface_normal = self.font.render(text, True, normal_text)
        self.text_surface_hover = self.font.render(text, True, hover_text)
        self.text_surface_click = self.font.render(text, True, click_text)
        
        # Calculate button dimensions
        text_width = self.text_surface_normal.get_width()
        text_height = self.text_surface_normal.get_height()
        self.rect = pygame.Rect(position[0], position[1], 
                               text_width + padding * 2, 
                               text_height + padding * 2)
        
        self._is_hover = False
        self._is_pressed = False
        self._was_clicked = False
        
        # Current visual state
        self._current_bg = normal_bg
        self._current_text_surface = self.text_surface_normal

    def update(self, delta_time: float = 0):
        """
        Cập nhật trạng thái của text button dựa trên tương tác chuột
        
        Cập nhật trạng thái và hiển thị của button dựa trên hover và click
        """
        mouse_pos = pygame.mouse.get_pos()
        
        # Determine current state
        if self.rect.collidepoint(mouse_pos):
            self._is_hover = True
            if pygame.mouse.get_pressed()[0]:
                self._current_bg = self.click_bg
                self._current_text_surface = self.text_surface_click
                if not self._was_clicked:
                    self._is_pressed = True
                    self._was_clicked = True
                    if self.on_click: self.on_click()
                else:
                    self._is_pressed = False
            else:
                self._current_bg = self.hover_bg
                self._current_text_surface = self.text_surface_hover
                self._is_pressed = False
                self._was_clicked = False
        else:
            self._current_bg = self.normal_bg
            self._current_text_surface = self.text_surface_normal
            self._is_hover = False
            self._is_pressed = False
            self._was_clicked = False

    def handle_event(self, event: pygame.event.Event):
        """Xử lý sự kiện pygame (hiện tại không sử dụng)"""
        pass

    def draw(self, screen: pygame.Surface):
        """
        Vẽ text button với trạng thái hiện tại
        
        Vẽ giao diện button dựa trên trạng thái hiện tại:
        - Trạng thái bình thường: màu normal_bg và normal_text
        - Trạng thái hover: màu hover_bg và hover_text
        - Trạng thái clicked: màu click_bg và click_text
        
        Args:
            screen: Màn hình game - Surface để vẽ button lên
        """
        # Draw background with rounded corners
        pygame.draw.rect(screen, self._current_bg, self.rect, border_radius=self.border_radius)
        
        # Draw border with rounded corners
        if self.border_width > 0:
            pygame.draw.rect(screen, self.border_color, self.rect, self.border_width, border_radius=self.border_radius)
        
        # Draw text centered in button
        text_x = self.rect.x + self.padding
        text_y = self.rect.y + self.padding
        screen.blit(self._current_text_surface, (text_x, text_y))

    def is_hover(self):
        """
        Kiểm tra xem chuột có đang hover trên button không
        
        Returns:
            bool: True nếu chuột đang hover, False nếu không
        """
        return self._is_hover

    def is_pressed(self):
        """
        Kiểm tra xem button có đang được click không (level-based - True khi đang giữ)
        
        Để phát hiện edge (sự kiện kích hoạt một lần), sử dụng thuộc tính _was_clicked hoặc method was_clicked().
        was_clicked chỉ True ở frame đầu tiên của click, không phải khi đang giữ.
        
        Returns:
            bool: True nếu button đang được click, False nếu không
        """
        return self._is_pressed
    
    def was_clicked(self):
        """
        Kiểm tra xem button vừa được click không (edge detection - chỉ True ở frame đầu tiên)
        
        Hữu ích cho các sự kiện kích hoạt một lần như toggle, mở dialog, v.v.
        Chỉ trả về True ở lần click đầu tiên, không phải khi button đang được giữ.
        
        Returns:
            bool: True nếu button vừa được click (chỉ frame đầu tiên), False nếu không
        """
        return self._was_clicked
