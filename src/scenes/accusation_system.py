import pygame
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from utils.menu_base import MenuBase
from utils.ui_components import Button
from utils.text_effects import TextRenderer
from config import COLORS, SCREEN_WIDTH, SCREEN_HEIGHT, IMAGES_DIR

class SuspectCard:
    """Card component for suspect selection"""
    
    def __init__(self, x, y, width, height, name, icon_path, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name
        self.icon_path = icon_path
        self.font = font
        self.is_selected = False
        self.is_hovered = False
        self.border_radius = 12
        
        # Load avatar image
        self.avatar = None
        if icon_path:
            try:
                print(f"[SuspectCard] Attempting to load avatar: {icon_path}")
                self.avatar = pygame.image.load(icon_path).convert_alpha()
                # Scale to fit icon size (50x50)
                self.avatar = pygame.transform.scale(self.avatar, (50, 50))
                print(f"[SuspectCard] ✅ Successfully loaded avatar: {icon_path}")
            except Exception as e:
                print(f"[SuspectCard] ❌ Could not load avatar {icon_path}: {e}")
                self.avatar = None
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True  # Selected
        return False
    
    def draw(self, screen):
        # Determine colors - Purple theme for suspects
        if self.is_selected:
            bg_color = (120, 60, 140)      # Selected purple
            border_color = (180, 120, 200)
        elif self.is_hovered:
            bg_color = (90, 50, 110)       # Hover purple
            border_color = (150, 100, 170)
        else:
            bg_color = (70, 40, 90)        # Default purple
            border_color = (110, 70, 130)
        
        # Draw rounded rectangle with pixel art style
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(screen, border_color, self.rect, 3, border_radius=self.border_radius)
        
        # Draw highlight for 3D effect
        inner_rect = pygame.Rect(
            self.rect.x + 4,
            self.rect.y + 4,
            self.rect.width - 8,
            self.rect.height - 8
        )
        highlight_color = tuple(min(255, c + 20) for c in bg_color)
        pygame.draw.rect(screen, highlight_color, inner_rect, 1, border_radius=self.border_radius - 2)
        
        # Draw avatar or icon placeholder (top section)
        icon_size = 50
        icon_x = self.rect.centerx - icon_size // 2
        icon_y = self.rect.y + 15
        icon_rect = pygame.Rect(icon_x, icon_y, icon_size, icon_size)
        
        if self.avatar:
            # Draw avatar image
            screen.blit(self.avatar, icon_rect)
            # Draw border around avatar
            pygame.draw.rect(screen, border_color, icon_rect, 2, border_radius=8)
        else:
            # Draw placeholder
            pygame.draw.rect(screen, (100, 60, 120), icon_rect, border_radius=8)
            pygame.draw.rect(screen, border_color, icon_rect, 2, border_radius=8)
        
        # Draw name (bottom section) with truncation to fit in card
        max_width = self.rect.width - 12  # 6px padding on each side
        name_text = self.name
        name_surface = self.font.render(name_text, True, COLORS['WHITE'])
        
        # If text is too wide, truncate with "..."
        while name_surface.get_width() > max_width and len(name_text) > 3:
            name_text = name_text[:-1]
            name_surface = self.font.render(name_text + "...", True, COLORS['WHITE'])
        
        name_rect = name_surface.get_rect(centerx=self.rect.centerx, y=icon_y + icon_size + 10)
        screen.blit(name_surface, name_rect)


class EvidenceCard:
    """Card component for evidence display"""
    
    def __init__(self, x, y, width, height, title, location, font):
        self.rect = pygame.Rect(x, y, width, height)
        self.title = title
        self.location = location
        self.font = font
        self.is_selected = False
        self.is_hovered = False
        self.border_radius = 10
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.is_selected = not self.is_selected
                return True
        return False
    
    def draw(self, screen):
        # Brown/tan theme for evidence
        if self.is_selected:
            bg_color = (140, 100, 60)      # Selected brown
            border_color = (200, 150, 100)
        elif self.is_hovered:
            bg_color = (110, 80, 50)       # Hover brown
            border_color = (170, 130, 90)
        else:
            bg_color = (80, 60, 40)        # Default brown
            border_color = (130, 100, 70)
        
        # Draw rounded rectangle
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(screen, border_color, self.rect, 2, border_radius=self.border_radius)
        
        # Draw highlight
        inner_rect = pygame.Rect(
            self.rect.x + 3,
            self.rect.y + 3,
            self.rect.width - 6,
            self.rect.height - 6
        )
        highlight_color = tuple(min(255, c + 20) for c in bg_color)
        pygame.draw.rect(screen, highlight_color, inner_rect, 1, border_radius=self.border_radius - 2)
        
        # Truncate text if too long to fit in card
        max_width = self.rect.width - 16  # 8px padding on each side
        
        # Draw title with truncation
        title_text = self.title
        title_surface = self.font.render(title_text, True, COLORS['WHITE'])
        
        # If text is too wide, truncate with "..."
        while title_surface.get_width() > max_width and len(title_text) > 3:
            title_text = title_text[:-1]
            title_surface = self.font.render(title_text + "...", True, COLORS['WHITE'])
        
        title_rect = title_surface.get_rect(centerx=self.rect.centerx, y=self.rect.y + 8)
        screen.blit(title_surface, title_rect)
        
        # Draw location with truncation (smaller text)
        location_text = self.location
        location_surface = self.font.render(location_text, True, (200, 200, 200))
        
        # If location text is too wide, truncate with "..."
        while location_surface.get_width() > max_width and len(location_text) > 3:
            location_text = location_text[:-1]
            location_surface = self.font.render(location_text + "...", True, (200, 200, 200))
        
        location_rect = location_surface.get_rect(centerx=self.rect.centerx, y=self.rect.y + 30)
        screen.blit(location_surface, location_rect)


class ConfirmationDialog:
    """Confirmation dialog for accusation"""
    
    def __init__(self, x, y, width, height, suspect_name, font, on_confirm, on_cancel):
        self.rect = pygame.Rect(x, y, width, height)
        self.suspect_name = suspect_name
        self.font = font
        self.on_confirm = on_confirm
        self.on_cancel = on_cancel
        self.border_radius = 15
        self.visible = False
        self.is_locked = False  # Track if dialog is locked
        
        # Create buttons - responsive sizing
        button_width = min(150, int(width * 0.28))  # 28% of dialog width
        button_height = min(50, int(height * 0.25))  # 25% of dialog height
        button_y = y + height - button_height - int(height * 0.1)  # 10% from bottom
        button_spacing = int(width * 0.02)  # 2% of dialog width
        
        self.confirm_button = Button(
            x + width // 2 - button_width - button_spacing,
            button_y,
            button_width,
            button_height,
            "CONFIRM",
            font,
            self.confirm,
            show_icon=False
        )
        
        self.cancel_button = Button(
            x + width // 2 + button_spacing,
            button_y,
            button_width,
            button_height,
            "CANCEL",
            font,
            self.cancel,
            show_icon=False
        )
    
    def show(self):
        self.visible = True
    
    def hide(self):
        self.visible = False
    
    def confirm(self):
        self.is_locked = True  # Lock the dialog
        if self.on_confirm:
            self.on_confirm()
        # Don't hide - keep visible but locked
    
    def cancel(self):
        self.is_locked = False  # Unlock the dialog
        self.hide()
        if self.on_cancel:
            self.on_cancel()
    
    def handle_event(self, event):
        if not self.visible:
            return
        self.confirm_button.handle_event(event)
        self.cancel_button.handle_event(event)
    
    def draw(self, screen):
        if not self.visible:
            return
        
        # No overlay - allow interaction with background elements
        
        # Draw dialog box with different color when locked
        if self.is_locked:
            bg_color = (40, 80, 50)       # Green tint when locked
            border_color = (80, 200, 100)  # Bright green border
        else:
            bg_color = (60, 60, 60)
            border_color = (150, 150, 150)
        
        pygame.draw.rect(screen, bg_color, self.rect, border_radius=self.border_radius)
        pygame.draw.rect(screen, border_color, self.rect, 4, border_radius=self.border_radius)
        
        # Draw highlight
        inner_rect = pygame.Rect(
            self.rect.x + 5,
            self.rect.y + 5,
            self.rect.width - 10,
            self.rect.height - 10
        )
        highlight_color = (90, 90, 90) if not self.is_locked else (60, 120, 70)
        pygame.draw.rect(screen, highlight_color, inner_rect, 2, border_radius=self.border_radius - 2)
        
        # Draw question text - responsive positioning
        text_y_offset = int(self.rect.height * 0.2)  # 20% from top
        text_spacing = int(self.rect.height * 0.15)  # 15% spacing between lines
        
        # Show different text when locked
        if self.is_locked:
            question = f"LOCKED! PRESS ACCUSE TO"
            question2 = f"CONFIRM {self.suspect_name.upper()}"
        else:
            question = f"ARE YOU SURE YOU WANT TO"
            question2 = f"ACCUSE {self.suspect_name.upper()}?"
        
        question_surface = self.font.render(question, True, COLORS['WHITE'])
        question_rect = question_surface.get_rect(centerx=self.rect.centerx, y=self.rect.y + text_y_offset)
        screen.blit(question_surface, question_rect)
        
        question2_surface = self.font.render(question2, True, (255, 200, 100))
        question2_rect = question2_surface.get_rect(centerx=self.rect.centerx, y=self.rect.y + text_y_offset + text_spacing)
        screen.blit(question2_surface, question2_rect)
        
        # Only show buttons when not locked
        if not self.is_locked:
            # Draw buttons with custom colors
            # Green confirm button
            confirm_rect = self.confirm_button.rect
            pygame.draw.rect(screen, (40, 120, 60), confirm_rect, border_radius=12)
            pygame.draw.rect(screen, (80, 200, 100), confirm_rect, 3, border_radius=12)
            confirm_text = self.confirm_button.font.render("CONFIRM", True, COLORS['WHITE'])
            confirm_text_rect = confirm_text.get_rect(center=confirm_rect.center)
            screen.blit(confirm_text, confirm_text_rect)
            
            # Red cancel button
            cancel_rect = self.cancel_button.rect
            pygame.draw.rect(screen, (120, 40, 40), cancel_rect, border_radius=12)
            pygame.draw.rect(screen, (200, 80, 80), cancel_rect, 3, border_radius=12)
            cancel_text = self.cancel_button.font.render("CANCEL", True, COLORS['WHITE'])
            cancel_text_rect = cancel_text.get_rect(center=cancel_rect.center)
            screen.blit(cancel_text, cancel_text_rect)


class AccusationSystem(MenuBase):
    """Accusation system screen for selecting suspects and evidence"""
    
    def __init__(self, screen, game_manager):
        super().__init__(screen)
        self.game_manager = game_manager
        self.background = self.load_background()
        self.text_renderer = TextRenderer()
        
        # Create small font for cards
        self.font_small = self.load_pixel_font(18)
        
        # Title
        self.title_surface = None
        self.title_rect = None
        self.subtitle_surface = None
        self.subtitle_rect = None
        self.render_titles()
        
        # Sample data with avatars
        avatar_path = "assets/images/player"
        self.suspects = [
            {"name": "John Doe", "icon": f"{avatar_path}/avatar1.png"},
            {"name": "Jane Smith", "icon": f"{avatar_path}/avatar2.png"},
            {"name": "Victor Reznov", "icon": f"{avatar_path}/avatar3.png"},
            {"name": "Sarah Connor", "icon": f"{avatar_path}/avatar1.png"},
            {"name": "Mike Wilson", "icon": f"{avatar_path}/avatar2.png"},
        ]
        
        self.evidence_items = [
            {"title": "Bloody Knife", "location": "Kitchen"},
            {"title": "Threatening Letter", "location": "Office"},
            {"title": "Muddy Boots", "location": "Alley"},
            {"title": "Broken Glass", "location": "Living Room"},
            {"title": "Security Footage", "location": "Entrance"},
        ]
        
        # Correct answer (0-indexed: 0=John Doe, 1=Jane Smith, 2=Victor Reznov, etc.)
        self.correct_suspect_index = 1  # Jane Smith is the correct suspect
        
        self.selected_suspect_index = -1
        self.selected_evidence = []
        
        # Scroll state for suspect cards
        self.suspect_scroll_offset = 0
        self.suspect_scroll_max = 0
        self.is_scrolling = False
        
        # Lock state for modal
        self.modal_locked = False  # When True, modal won't change on hover
        
        # Result dialog state
        self.show_result = False
        self.result_is_win = False
        self.result_timer = 0
        self.result_display_time = 3000  # 3 seconds
        
        self.setup_ui()
    
    def load_background(self):
        """Load background image (same as menu)"""
        try:
            bg_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), IMAGES_DIR, "menu_background.png")
            background = pygame.image.load(bg_path)
            background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
            return background
        except Exception as e:
            print(f"Warning: Could not load background image: {e}")
            return None
    
    def render_titles(self):
        """Render title and subtitle with pixel font - responsive"""
        # Main title - responsive font size
        title_font_size = min(48, int(SCREEN_WIDTH * 0.047))
        self.title_surface, self.title_rect = self.text_renderer.render_glow_text(
            text="ACCUSATION SYSTEM",
            color=(180, 140, 60),
            glow_color=(120, 80, 0),
            font_size=title_font_size,
            screen_width=SCREEN_WIDTH,
            glow_amount=3,
            letter_spacing=-3,
            word_spacing=15
        )
        self.title_rect.y = int(SCREEN_HEIGHT * 0.04)  # 4% from top
        
        # Subtitle - responsive font size
        subtitle_font_size = min(24, int(SCREEN_WIDTH * 0.023))
        self.subtitle_surface, self.subtitle_rect = self.text_renderer.render_glow_text(
            text="SELECT A SUSPECT",
            color=(150, 120, 80),
            glow_color=(100, 70, 40),
            font_size=subtitle_font_size,
            screen_width=SCREEN_WIDTH,
            glow_amount=2,
            letter_spacing=-2,
            word_spacing=10
        )
        self.subtitle_rect.y = int(SCREEN_HEIGHT * 0.12)  # 12% from top
    
    def setup_ui(self):
        """Setup all UI components - responsive design"""
        # Calculate responsive dimensions
        screen_margin = int(SCREEN_WIDTH * 0.04)  # 4% margin
        
        # Suspect container box dimensions
        self.suspect_container_x = screen_margin
        self.suspect_container_y = int(SCREEN_HEIGHT * 0.19)  # 19% from top
        self.suspect_container_width = min(200, int(SCREEN_WIDTH * 0.19))  # Container width
        self.suspect_container_height = int(SCREEN_HEIGHT * 0.55)  # 55% height for container
        
        # Suspect cards (left side) - responsive, inside container
        self.suspect_cards = []
        card_width = min(180, int(SCREEN_WIDTH * 0.17))  # Max 180px or 17% of screen
        card_height = min(100, int(SCREEN_HEIGHT * 0.12))  # Reduced from 0.15 to 0.12 to fit better
        start_x = self.suspect_container_x + 10  # 10px padding inside container
        start_y = self.suspect_container_y + 10  # 10px padding from top
        spacing = max(8, int(SCREEN_HEIGHT * 0.012))  # Reduced spacing
        
        # Create ALL suspect cards (not limited)
        for i, suspect in enumerate(self.suspects):
            card = SuspectCard(
                start_x,
                start_y + i * (card_height + spacing),
                card_width,
                card_height,
                suspect["name"],
                suspect["icon"],
                self.font_small
            )
            self.suspect_cards.append(card)
        
        # Calculate scroll max
        total_cards_height = len(self.suspects) * (card_height + spacing)
        available_height = self.suspect_container_height - 20  # Minus padding
        self.suspect_scroll_max = max(0, total_cards_height - available_height)
        
        # Scrollbar dimensions
        self.scrollbar_width = 8
        self.scrollbar_x = self.suspect_container_x + self.suspect_container_width - self.scrollbar_width - 5
        self.scrollbar_y = self.suspect_container_y + 10
        self.scrollbar_height = self.suspect_container_height - 20
        
        # Scrollbar handle
        if self.suspect_scroll_max > 0:
            handle_ratio = available_height / total_cards_height
            self.scrollbar_handle_height = max(30, int(self.scrollbar_height * handle_ratio))
        else:
            self.scrollbar_handle_height = self.scrollbar_height
        
        # Evidence cards (bottom) - responsive
        self.evidence_cards = []
        ev_width = min(180, int(SCREEN_WIDTH * 0.17))
        ev_height = min(60, int(SCREEN_HEIGHT * 0.08))
        ev_start_x = screen_margin
        ev_start_y = int(SCREEN_HEIGHT * 0.80)  # 80% from top
        ev_spacing = max(15, int(SCREEN_WIDTH * 0.015))
        ev_row_spacing = max(10, int(SCREEN_HEIGHT * 0.015))
        
        for i, evidence in enumerate(self.evidence_items):
            # Arrange in 2 rows, responsive
            row = i // 3
            col = i % 3
            card = EvidenceCard(
                ev_start_x + col * (ev_width + ev_spacing),
                ev_start_y + row * (ev_height + ev_row_spacing),
                ev_width,
                ev_height,
                evidence["title"],
                evidence["location"],
                self.font_small
            )
            self.evidence_cards.append(card)
        
        # Confirmation dialog - responsive, always centered
        dialog_width = min(500, int(SCREEN_WIDTH * 0.48))
        dialog_height = min(200, int(SCREEN_HEIGHT * 0.26))
        dialog_x = SCREEN_WIDTH // 2 - dialog_width // 2
        dialog_y = SCREEN_HEIGHT // 2 - dialog_height // 2
        
        self.confirmation_dialog = ConfirmationDialog(
            dialog_x,
            dialog_y,
            dialog_width,
            dialog_height,
            "",
            self.font_small,
            self.on_modal_confirm,  # Changed: lock modal on confirm
            self.on_cancel_accusation
        )
        
        # Action buttons (right side) - responsive
        button_width = min(200, int(SCREEN_WIDTH * 0.19))
        button_height = min(60, int(SCREEN_HEIGHT * 0.08))
        button_x = SCREEN_WIDTH - button_width - screen_margin
        
        # Accuse button (large, purple) - middle of screen
        self.accuse_button = Button(
            button_x,
            int(SCREEN_HEIGHT * 0.39),  # 39% from top
            button_width,
            button_height,
            "ACCUSE",
            self.font_medium,
            self.show_confirmation,
            show_icon=False
        )
        
        # Back button (smaller) - bottom right
        back_width = min(150, int(SCREEN_WIDTH * 0.14))
        back_height = min(50, int(SCREEN_HEIGHT * 0.065))
        self.back_button = Button(
            button_x + (button_width - back_width) // 2,  # Centered relative to accuse button
            int(SCREEN_HEIGHT * 0.87),  # 87% from top
            back_width,
            back_height,
            "BACK",
            self.font_small,
            self.go_back,
            show_icon=False
        )
    
    def show_confirmation(self):
        """Show confirmation dialog"""
        if self.selected_suspect_index >= 0 and self.modal_locked:
            # Only execute accusation if modal is locked (confirmed)
            self.on_confirm_accusation()
    
    def on_confirm_accusation(self):
        """Handle confirmed accusation - called when ACCUSE button is pressed"""
        accused_name = self.suspects[self.selected_suspect_index]['name']
        evidence_names = [self.evidence_items[i]['title'] for i in self.selected_evidence]
        
        print(f"Accused: {accused_name}")
        print(f"Evidence: {evidence_names}")
        
        # Check if correct suspect
        if self.selected_suspect_index == self.correct_suspect_index:
            print("✅ CORRECT! You win!")
            self.result_is_win = True
        else:
            print("❌ WRONG! You lose!")
            self.result_is_win = False
        
        # Show result dialog
        self.show_result = True
        self.result_timer = pygame.time.get_ticks()
    
    def on_modal_confirm(self):
        """Handle modal CONFIRM button - locks the selection"""
        # Lock the modal so hover won't change selection
        self.modal_locked = True
        # Keep modal visible but locked
        # Don't hide the modal
    
    def on_cancel_accusation(self):
        """Handle cancelled accusation - unlock and deselect suspect"""
        # Unlock modal and deselect the suspect when user cancels
        self.modal_locked = False
        self.confirmation_dialog.hide()
        if self.selected_suspect_index >= 0:
            self.suspect_cards[self.selected_suspect_index].is_selected = False
            self.selected_suspect_index = -1
    
    def go_back(self):
        """Return to previous screen"""
        print("Back button pressed in accusation system")
        # Get game instance from game_manager
        if hasattr(self.game_manager, 'game_instance'):
            self.game_manager.game_instance.close_accusation_system()
        else:
            print("Warning: Could not find game instance to close accusation system")
    
    def handle_input(self, event):
        """Handle all input events"""
        # Don't handle input if showing result
        if self.show_result:
            return
        
        # Handle confirmation dialog if visible (but don't block other interactions)
        if self.confirmation_dialog.visible:
            self.confirmation_dialog.handle_event(event)
            # Don't return - allow other interactions to continue
        
        # Handle mouse wheel scrolling for suspects
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if mouse is over suspect container
            container_rect = pygame.Rect(
                self.suspect_container_x,
                self.suspect_container_y,
                self.suspect_container_width,
                self.suspect_container_height
            )
            if container_rect.collidepoint(event.pos):
                if event.button == 4:  # Scroll up
                    self.suspect_scroll_offset = max(0, self.suspect_scroll_offset - 30)
                elif event.button == 5:  # Scroll down
                    self.suspect_scroll_offset = min(self.suspect_scroll_max, self.suspect_scroll_offset + 30)
        
        # Handle mouse motion for hover effects on suspects
        if event.type == pygame.MOUSEMOTION:
            # Only allow hover changes if modal is not locked
            if not self.modal_locked:
                hovered_suspect = -1
                
                for i, card in enumerate(self.suspect_cards):
                    # Create a temporary rect with scroll offset applied
                    scrolled_rect = pygame.Rect(
                        card.rect.x,
                        card.rect.y - self.suspect_scroll_offset,
                        card.rect.width,
                        card.rect.height
                    )
                    
                    # Check if card is visible in container
                    container_rect = pygame.Rect(
                        self.suspect_container_x,
                        self.suspect_container_y,
                        self.suspect_container_width,
                        self.suspect_container_height
                    )
                    
                    # Check if mouse is over this card
                    if scrolled_rect.colliderect(container_rect) and scrolled_rect.collidepoint(event.pos):
                        card.is_hovered = True
                        hovered_suspect = i
                        
                        # Show modal when hovering over a suspect
                        suspect_name = self.suspects[i]["name"]
                        self.confirmation_dialog.suspect_name = suspect_name
                        self.selected_suspect_index = i
                        
                        # Deselect all others and select this one
                        for j, other_card in enumerate(self.suspect_cards):
                            other_card.is_selected = (j == i)
                        
                        # Show confirmation dialog on hover
                        if not self.confirmation_dialog.visible:
                            self.confirmation_dialog.show()
                    else:
                        card.is_hovered = False
        
        # Handle suspect click (for additional interaction if needed)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left click
            # Only allow click changes if modal is not locked
            if not self.modal_locked:
                for i, card in enumerate(self.suspect_cards):
                    # Create a temporary rect with scroll offset applied
                    scrolled_rect = pygame.Rect(
                        card.rect.x,
                        card.rect.y - self.suspect_scroll_offset,
                        card.rect.width,
                        card.rect.height
                    )
                    
                    # Check if card is visible in container
                    container_rect = pygame.Rect(
                        self.suspect_container_x,
                        self.suspect_container_y,
                        self.suspect_container_width,
                        self.suspect_container_height
                    )
                    
                    # Only handle events for visible cards
                    if scrolled_rect.colliderect(container_rect) and scrolled_rect.collidepoint(event.pos):
                        # Deselect all others
                        for j, other_card in enumerate(self.suspect_cards):
                            other_card.is_selected = (j == i)
                        self.selected_suspect_index = i
                        
                        # Show confirmation dialog
                        suspect_name = self.suspects[self.selected_suspect_index]["name"]
                        self.confirmation_dialog.suspect_name = suspect_name
                        self.confirmation_dialog.show()
                        return  # Don't process other events
        
        # Handle evidence selection
        for i, card in enumerate(self.evidence_cards):
            if card.handle_event(event):
                if card.is_selected and i not in self.selected_evidence:
                    self.selected_evidence.append(i)
                elif not card.is_selected and i in self.selected_evidence:
                    self.selected_evidence.remove(i)
        
        # Handle buttons
        self.accuse_button.handle_event(event)
        self.back_button.handle_event(event)
    
    def update(self):
        """Update game state"""
        # Handle result display timer
        if self.show_result:
            current_time = pygame.time.get_ticks()
            if current_time - self.result_timer > self.result_display_time:
                # Time's up, return to office
                self.show_result = False
                self.go_back()
    
    def draw_result_dialog(self, screen):
        """Draw win/lose result dialog"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(220)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Dialog box
        dialog_width = min(600, int(SCREEN_WIDTH * 0.6))
        dialog_height = min(300, int(SCREEN_HEIGHT * 0.4))
        dialog_x = (SCREEN_WIDTH - dialog_width) // 2
        dialog_y = (SCREEN_HEIGHT - dialog_height) // 2
        
        if self.result_is_win:
            bg_color = (40, 100, 40)  # Green
            border_color = (80, 200, 80)
            title_text = "CONGRATULATIONS!"
            message_text = "You caught the right suspect!"
        else:
            bg_color = (100, 40, 40)  # Red
            border_color = (200, 80, 80)
            title_text = "WRONG SUSPECT!"
            message_text = "The real culprit got away..."
        
        # Draw dialog background
        dialog_rect = pygame.Rect(dialog_x, dialog_y, dialog_width, dialog_height)
        pygame.draw.rect(screen, bg_color, dialog_rect, border_radius=15)
        pygame.draw.rect(screen, border_color, dialog_rect, 5, border_radius=15)
        
        # Title
        title_font = self.load_pixel_font(36)
        title_surface = title_font.render(title_text, True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, dialog_y + 80))
        screen.blit(title_surface, title_rect)
        
        # Message
        msg_font = self.load_pixel_font(20)
        msg_surface = msg_font.render(message_text, True, (220, 220, 220))
        msg_rect = msg_surface.get_rect(center=(SCREEN_WIDTH // 2, dialog_y + 150))
        screen.blit(msg_surface, msg_rect)
        
        # "Returning to office..." text
        info_font = self.load_pixel_font(16)
        info_surface = info_font.render("Returning to office...", True, (180, 180, 180))
        info_rect = info_surface.get_rect(center=(SCREEN_WIDTH // 2, dialog_y + 200))
        screen.blit(info_surface, info_rect)
    
    def draw(self):
        """Draw all components"""
        # Draw background
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(COLORS['BLACK'])
        
        # Draw semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(100)
        overlay.fill(COLORS['BLACK'])
        self.screen.blit(overlay, (0, 0))
        
        # Draw titles
        if self.title_surface and self.title_rect:
            self.screen.blit(self.title_surface, self.title_rect)
        if self.subtitle_surface and self.subtitle_rect:
            self.screen.blit(self.subtitle_surface, self.subtitle_rect)
        
        # Draw section labels - responsive positions
        screen_margin = int(SCREEN_WIDTH * 0.04)
        label_y_suspects = int(SCREEN_HEIGHT * 0.16)  # Just above suspect cards
        label_y_evidence = int(SCREEN_HEIGHT * 0.765)  # Just above evidence cards
        
        suspect_label = self.font_small.render("SUSPECTS", True, (200, 150, 100))
        self.screen.blit(suspect_label, (screen_margin, label_y_suspects))
        
        evidence_label = self.font_small.render("EVIDENCE", True, (200, 150, 100))
        self.screen.blit(evidence_label, (screen_margin, label_y_evidence))
        
        # Draw suspect container box (frame)
        container_rect = pygame.Rect(
            self.suspect_container_x,
            self.suspect_container_y,
            self.suspect_container_width,
            self.suspect_container_height
        )
        # Background with slight transparency
        container_bg = pygame.Surface((self.suspect_container_width, self.suspect_container_height))
        container_bg.set_alpha(30)
        container_bg.fill((50, 30, 70))  # Dark purple tint
        self.screen.blit(container_bg, (self.suspect_container_x, self.suspect_container_y))
        
        # Border frame
        pygame.draw.rect(self.screen, (110, 70, 130), container_rect, 3, border_radius=10)
        
        # Inner highlight for 3D effect
        inner_container = pygame.Rect(
            container_rect.x + 3,
            container_rect.y + 3,
            container_rect.width - 6,
            container_rect.height - 6
        )
        pygame.draw.rect(self.screen, (80, 50, 100), inner_container, 1, border_radius=8)
        
        # Create clipping mask for suspect cards (so they don't draw outside container)
        clip_rect = pygame.Rect(
            self.suspect_container_x + 5,
            self.suspect_container_y + 5,
            self.suspect_container_width - 10,
            self.suspect_container_height - 10
        )
        self.screen.set_clip(clip_rect)
        
        # Draw suspect cards (inside container) with scroll offset
        for card in self.suspect_cards:
            # Calculate scrolled position
            scrolled_y = card.rect.y - self.suspect_scroll_offset
            
            # Only draw if visible in container
            if scrolled_y + card.rect.height > self.suspect_container_y and scrolled_y < self.suspect_container_y + self.suspect_container_height:
                # Temporarily update position for drawing
                original_y = card.rect.y
                card.rect.y = scrolled_y
                card.draw(self.screen)
                card.rect.y = original_y  # Restore original position
        
        # Remove clipping
        self.screen.set_clip(None)
        
        # Draw scrollbar if needed
        if self.suspect_scroll_max > 0:
            # Scrollbar track
            scrollbar_track_rect = pygame.Rect(
                self.scrollbar_x,
                self.scrollbar_y,
                self.scrollbar_width,
                self.scrollbar_height
            )
            pygame.draw.rect(self.screen, (40, 25, 50), scrollbar_track_rect, border_radius=4)
            
            # Scrollbar handle
            handle_y_offset = (self.suspect_scroll_offset / self.suspect_scroll_max) * (self.scrollbar_height - self.scrollbar_handle_height)
            scrollbar_handle_rect = pygame.Rect(
                self.scrollbar_x,
                self.scrollbar_y + handle_y_offset,
                self.scrollbar_width,
                self.scrollbar_handle_height
            )
            pygame.draw.rect(self.screen, (130, 90, 150), scrollbar_handle_rect, border_radius=4)
            pygame.draw.rect(self.screen, (160, 120, 180), scrollbar_handle_rect, 1, border_radius=4)
        
        # Draw evidence cards
        for card in self.evidence_cards:
            card.draw(self.screen)
        
        # Draw action buttons with custom styling
        # Accuse button (purple theme with 3 states)
        accuse_rect = self.accuse_button.rect
        if self.modal_locked:
            # Ready state - bright purple (confirmed and ready to accuse)
            bg_color = (140, 70, 180)
            border_color = (200, 140, 220)
            text_color = (255, 255, 150)  # Yellow text for emphasis
        elif self.selected_suspect_index >= 0:
            # Selected state - normal purple
            bg_color = (100, 50, 130)
            border_color = (160, 100, 180)
            text_color = COLORS['WHITE']
        else:
            # Disabled state - gray
            bg_color = (60, 60, 60)
            border_color = (100, 100, 100)
            text_color = COLORS['WHITE']
        
        pygame.draw.rect(self.screen, bg_color, accuse_rect, border_radius=15)
        pygame.draw.rect(self.screen, border_color, accuse_rect, 3, border_radius=15)
        
        # Add highlight
        inner_rect = pygame.Rect(
            accuse_rect.x + 4,
            accuse_rect.y + 4,
            accuse_rect.width - 8,
            accuse_rect.height - 8
        )
        pygame.draw.rect(self.screen, tuple(min(255, c + 20) for c in bg_color), inner_rect, 1, border_radius=13)
        
        accuse_text = self.accuse_button.font.render("ACCUSE", True, text_color)
        accuse_text_rect = accuse_text.get_rect(center=accuse_rect.center)
        self.screen.blit(accuse_text, accuse_text_rect)
        
        # Back button (standard style)
        self.back_button.draw(self.screen)
        
        # Draw result dialog if showing
        if self.show_result:
            self.draw_result_dialog(self.screen)
        
        # Draw confirmation dialog (on top)
        self.confirmation_dialog.draw(self.screen)
