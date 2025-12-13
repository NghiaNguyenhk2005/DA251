"""
Suspect Selection Popup
Hiển thị 3 nghi phạm với avatar để chọn trước khi vào interrogation
"""
import pygame
from typing import Callable, Optional, List, Dict

class SuspectOption:
    """Single suspect option with avatar and name"""
    
    def __init__(self, x: int, y: int, width: int, height: int, name: str, 
                 avatar_path: str, bg_scene: str, font: pygame.font.Font):
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name
        self.avatar_path = avatar_path
        self.bg_scene = bg_scene
        self.font = font
        self.is_selected = False
        
        # Load avatar
        self.avatar = None
        try:
            self.avatar = pygame.image.load(avatar_path).convert_alpha()
            self.avatar = pygame.transform.scale(self.avatar, (80, 80))
        except Exception as e:
            print(f"Warning: Could not load avatar {avatar_path}: {e}")
    
    def draw(self, screen: pygame.Surface):
        # Background color
        if self.is_selected:
            bg_color = (100, 150, 200)  # Blue when selected
            border_color = (150, 200, 255)
        else:
            bg_color = (60, 60, 80)
            border_color = (120, 120, 140)
        
        # Draw background
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=10)
        pygame.draw.rect(screen, border_color, self.rect, 3, border_radius=10)
        
        # Draw avatar
        if self.avatar:
            avatar_x = self.rect.x + (self.rect.width - 80) // 2
            avatar_y = self.rect.y + 15
            screen.blit(self.avatar, (avatar_x, avatar_y))
            
            # Border around avatar
            avatar_rect = pygame.Rect(avatar_x, avatar_y, 80, 80)
            pygame.draw.rect(screen, border_color, avatar_rect, 2, border_radius=8)
        
        # Draw name
        name_surface = self.font.render(self.name, True, (255, 255, 255))
        name_rect = name_surface.get_rect(centerx=self.rect.centerx, y=self.rect.y + 105)
        screen.blit(name_surface, name_rect)


class SuspectSelectionPopup:
    """Popup để chọn nghi phạm trước khi vào interrogation"""
    
    def __init__(self, screen_width: int, screen_height: int, on_select: Optional[Callable[[str], None]] = None):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.on_select = on_select
        self.visible = False
        self.selected_index = 0
        
        # Font
        try:
            self.title_font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 28)
            self.option_font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 16)
            self.instruction_font = pygame.font.Font("assets/fonts/PressStart2P.ttf", 14)
        except:
            self.title_font = pygame.font.Font(None, 36)
            self.option_font = pygame.font.Font(None, 22)
            self.instruction_font = pygame.font.Font(None, 20)
        
        # Suspects data
        self.suspects_data = [
            {
                "name": "Suspect A",
                "avatar": "assets/images/player/avatar1.png",
                "bg_scene": "assets/images/scenes/interrogation-bg.png"
            },
            {
                "name": "Suspect B",
                "avatar": "assets/images/player/avatar2.png",
                "bg_scene": "assets/images/scenes/interrogation-bg2.png"
            },
            {
                "name": "Suspect C",
                "avatar": "assets/images/player/avatar3.png",
                "bg_scene": "assets/images/scenes/interrogation-bg3.png"
            }
        ]
        
        self.setup_ui()
    
    def setup_ui(self):
        """Setup suspect option cards"""
        self.suspect_options = []
        
        # Calculate positions for 3 suspects (horizontal layout)
        card_width = 150
        card_height = 140
        total_width = card_width * 3 + 40 * 2  # 40px spacing between cards
        start_x = (self.screen_width - total_width) // 2
        y = self.screen_height // 2 - 20
        
        for i, suspect in enumerate(self.suspects_data):
            x = start_x + i * (card_width + 40)
            option = SuspectOption(
                x, y, card_width, card_height,
                suspect["name"],
                suspect["avatar"],
                suspect["bg_scene"],
                self.option_font
            )
            self.suspect_options.append(option)
    
    def show(self):
        """Show the popup"""
        self.visible = True
        self.selected_index = 0
        self.update_selection()
    
    def hide(self):
        """Hide the popup"""
        self.visible = False
    
    def update_selection(self):
        """Update which option is selected"""
        for i, option in enumerate(self.suspect_options):
            option.is_selected = (i == self.selected_index)
    
    def handle_event(self, event: pygame.event.Event) -> bool:
        """Handle input events. Returns True if event was consumed."""
        if not self.visible:
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.selected_index = (self.selected_index - 1) % len(self.suspect_options)
                self.update_selection()
                return True
            elif event.key == pygame.K_RIGHT:
                self.selected_index = (self.selected_index + 1) % len(self.suspect_options)
                self.update_selection()
                return True
            elif event.key == pygame.K_RETURN:
                # Confirm selection
                selected_suspect = self.suspects_data[self.selected_index]
                self.hide()
                if self.on_select:
                    self.on_select(selected_suspect["bg_scene"])
                return True
            elif event.key == pygame.K_ESCAPE:
                # Cancel
                self.hide()
                return True
        
        return False
    
    def draw(self, screen: pygame.Surface):
        """Draw the popup"""
        if not self.visible:
            return
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((self.screen_width, self.screen_height))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Draw title
        title_text = "SELECT SUSPECT TO INTERROGATE"
        title_surface = self.title_font.render(title_text, True, (255, 255, 100))
        title_rect = title_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 120))
        screen.blit(title_surface, title_rect)
        
        # Draw suspect options
        for option in self.suspect_options:
            option.draw(screen)
        
        # Draw instructions
        instruction_text = "LEFT/RIGHT to select • ENTER to confirm • ESC to cancel"
        instruction_surface = self.instruction_font.render(instruction_text, True, (200, 200, 200))
        instruction_rect = instruction_surface.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 140))
        screen.blit(instruction_surface, instruction_rect)
