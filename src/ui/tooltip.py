import pygame

class Tooltip:
    """Class tooltip độc lập để hiển thị thông tin khi hover"""
    
    def __init__(self, text: str, font_size: int = 24, 
                 bg_color: tuple[int, int, int] = (50, 50, 50),
                 text_color: tuple[int, int, int] = (255, 255, 255),
                 border_color: tuple[int, int, int] = (200, 200, 200),
                 padding: int = 10):
        """
        Khởi tạo tooltip
        
        Args:
            text: Văn bản hiển thị trong tooltip
            font_size: Kích thước font cho văn bản
            bg_color: Màu nền (RGB)
            text_color: Màu chữ (RGB)
            border_color: Màu viền (RGB)
            padding: Khoảng cách đệm xung quanh văn bản
        """
        self.text = text
        self.font_size = font_size
        self.bg_color = bg_color
        self.text_color = text_color
        self.border_color = border_color
        self.padding = padding
        
        # Create font and render text
        self.font = pygame.font.Font(None, font_size)
        self.text_surface = self.font.render(text, True, text_color)
        
        # Calculate tooltip dimensions
        self.width = self.text_surface.get_width() + padding * 2
        self.height = self.text_surface.get_height() + padding * 2
    
    def draw(self, screen: pygame.Surface, mouse_pos: tuple[int, int]):
        """
        Vẽ tooltip tại vị trí chuột
        
        Args:
            screen: Surface để vẽ lên
            mouse_pos: Vị trí chuột (x, y)
        """
        # Calculate tooltip position (above and centered on mouse)
        tooltip_x = mouse_pos[0] - self.width // 2
        tooltip_y = mouse_pos[1] - self.height - 10
        
        # Keep tooltip within screen bounds
        tooltip_x = max(5, min(tooltip_x, screen.get_width() - self.width - 5))
        tooltip_y = max(5, tooltip_y)
        
        tooltip_rect = pygame.Rect(tooltip_x, tooltip_y, self.width, self.height)
        
        # Draw background
        pygame.draw.rect(screen, self.bg_color, tooltip_rect)
        # Draw border
        pygame.draw.rect(screen, self.border_color, tooltip_rect, 2)
        
        # Draw text
        text_pos = (tooltip_x + self.padding, tooltip_y + self.padding)
        screen.blit(self.text_surface, text_pos)
