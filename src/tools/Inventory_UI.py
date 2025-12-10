import pygame
import sys
import textwrap
from .help_func import get_sprite, slice_9, draw_9slice_box
from .Inventory_Manager import InventoryManager
from .Inventory_Item import *

class InventoryUI:
    def __init__(self, screen):
        self.screen = screen
        self.state = "CLOSED"  # Possible states: "CLOSED", "OPEN"

        # Config
        self.ROWS = 6
        self.COLS = 4
        self.SLOT_SIZE = 40
        self.MARGIN = 12

        # Colors
        self.BOX_COLOR = (20, 20, 20)
        self.LINE_COLOR = (100, 100, 100)
        self.TEXT_COLOR = (220, 220, 220)
        self.HOVER_COLOR = (211, 211, 211)
        self.HIGHLIGHT_COLOR = (255, 255, 0)
        self.ICON_HIGHLIGHT_COLOR = (255, 215, 0)

        # State
        self.SLOT_HOVERING = False
        self.ICON_HOVERING = False
        self.CLOSE_BTN_HOVERING = False

        self.selected_index = -1
        self.inventory_rects = []
        self.inventory_logic = InventoryManager(self.ROWS, self.COLS)

        # Load item icon sheet (only once)
        self.item_sheet = pygame.image.load("assets/images/tools/UI_Item_icon_temp.png").convert_alpha()

        # Icon config
        self.ICON_SIZE = 32
        self.ICONS_PER_ROW = 3
        self.ICON_GRID_SIZE = 340
    def initialize_inventory(self):
        self.inventory_logic = InventoryManager(self.ROWS, self.COLS)
        for i, item in enumerate(item_list):
            self.inventory_logic.add_item(item, i)

    def get_item_icon(self, item):
        col = item.icon_id % self.ICONS_PER_ROW
        row = item.icon_id // self.ICONS_PER_ROW

        x = col * self.ICON_GRID_SIZE + 10
        y = row * self.ICON_GRID_SIZE + 15
        icon = get_sprite(self.item_sheet, x, y, self.ICON_GRID_SIZE, self.ICON_GRID_SIZE)
        icon_scaled = pygame.transform.scale(icon, (self.ICON_SIZE, self.ICON_SIZE))
        return icon_scaled

    def draw_inventory_icon(self, mouse_pos):
        WIDTH, HEIGHT = self.screen.get_size()
        ICON_WIDTH, ICON_HEIGHT = 64, 64
        ICON_X = WIDTH - ICON_WIDTH - 20
        ICON_Y = ICON_HEIGHT + 50 - 20

        # Load inventory icon sprite sheet
        inventory_icon_sprite_sheet = pygame.image.load("assets/images/tools/UI_Inventory_icon.png").convert_alpha()
        inventory_icon_sprite = get_sprite(inventory_icon_sprite_sheet, 20, 15, 85, 100)
        inventory_icon_scaled = pygame.transform.scale(inventory_icon_sprite, (ICON_WIDTH, ICON_HEIGHT))

        icon_rect = pygame.Rect(ICON_X, ICON_Y, ICON_WIDTH, ICON_HEIGHT)
        self.screen.blit(inventory_icon_scaled, (ICON_X, ICON_Y))

        if icon_rect.collidepoint(mouse_pos):
            self.ICON_HOVERING = True
            pygame.draw.rect(self.screen, self.ICON_HIGHLIGHT_COLOR, icon_rect, 2)
        else:
            self.ICON_HOVERING = False

    def draw_inventory(self, mouse_pos):
        WIDTH, HEIGHT = self.screen.get_size()
        BOX_WIDTH, BOX_HEIGHT = 650, 400
        BOX_X = (WIDTH - BOX_WIDTH) // 2
        BOX_Y = (HEIGHT - BOX_HEIGHT) // 2

        GRID_X = BOX_X + 30
        GRID_Y = BOX_Y + 60

        CLOSE_BTN_SCALE = 2
        CLOSE_BTN_SIZE = 13 * CLOSE_BTN_SCALE  # 26x26

        if not self.inventory_rects:
            for i in range(self.ROWS * self.COLS):
                col = i % self.COLS
                row = i // self.COLS
                x = GRID_X + col * (self.SLOT_SIZE + self.MARGIN)
                y = GRID_Y + row * (self.SLOT_SIZE + self.MARGIN)
                if len(self.inventory_rects) < self.ROWS * self.COLS:
                    self.inventory_rects.append(pygame.Rect(x, y, self.SLOT_SIZE, self.SLOT_SIZE))

        # Load assets
        inventory_sprite_sheet = pygame.image.load("assets/images/tools/UI Inventory.png").convert_alpha()
        border_sprite_sheet = pygame.image.load("assets/images/tools/BlackGrey UI Border.png").convert_alpha()
        button_sprite_sheet = pygame.image.load("assets/images/tools/UI Buttons.png").convert_alpha()

        slot_sprite = get_sprite(inventory_sprite_sheet, 100, 68, 39, 39)
        border_sprite = get_sprite(border_sprite_sheet, 116, 5, 48, 48)
    
        # Load and scale close button sprite
        close_button_sprite = get_sprite(button_sprite_sheet, 172, 1, 13, 13)
        close_button_scaled = pygame.transform.scale(close_button_sprite, (CLOSE_BTN_SIZE, CLOSE_BTN_SIZE))

        # Fonts
        title_font = pygame.font.SysFont("consolas", 28, bold=True)
        name_font = pygame.font.SysFont("consolas", 24)
        desc_font = pygame.font.SysFont("consolas", 16)

        slices = slice_9(border_sprite)

        # Close button position
        CLOSE_BTN_X = BOX_X + BOX_WIDTH - CLOSE_BTN_SIZE - 8
        CLOSE_BTN_Y = BOX_Y + 8
        close_button_rect = pygame.Rect(CLOSE_BTN_X, CLOSE_BTN_Y, CLOSE_BTN_SIZE, CLOSE_BTN_SIZE)

        # Inventory box with 9-slice border
        pygame.draw.rect(self.screen, self.BOX_COLOR, (BOX_X, BOX_Y, BOX_WIDTH, BOX_HEIGHT))
        draw_9slice_box(self.screen, slices, BOX_X, BOX_Y, BOX_WIDTH, BOX_HEIGHT)

        # Title label with 9-slice border
        title_text = title_font.render("INVENTORY", True, self.TEXT_COLOR)
        title_rect = title_text.get_rect(center=(BOX_X + BOX_WIDTH // 2, BOX_Y - 0))
        label_bg_rect = title_rect.inflate(40, 20)
        draw_9slice_box(self.screen, slices, label_bg_rect.x, label_bg_rect.y, label_bg_rect.width, label_bg_rect.height)
        self.screen.blit(title_text, title_rect)

        # Left panel: inventory grid
        self.SLOT_HOVERING = False
        for i, slot in enumerate(self.inventory_rects):
            self.screen.blit(slot_sprite, (slot.x, slot.y))
            if slot.collidepoint(mouse_pos):
                self.SLOT_HOVERING = True
                pygame.draw.rect(self.screen, self.HOVER_COLOR, slot, 2)
            if i == self.selected_index:
                pygame.draw.rect(self.screen, self.HIGHLIGHT_COLOR, slot, 2)
            # Draw item icon inside slot
            item = self.inventory_logic.get_item(i)
            if item:
                icon = self.get_item_icon(item)
                icon_x = slot.x + (self.SLOT_SIZE - self.ICON_SIZE) // 2
                icon_y = slot.y + (self.SLOT_SIZE - self.ICON_SIZE) // 2
                self.screen.blit(icon, (icon_x, icon_y))

        # Divider line
        divider_x = GRID_X + self.COLS * (self.SLOT_SIZE + self.MARGIN) + 20
        divider_top = GRID_Y
        divider_bottom = GRID_Y + self.ROWS * (self.SLOT_SIZE + self.MARGIN) - self.MARGIN
        pygame.draw.line(self.screen, self.LINE_COLOR, (divider_x, divider_top), (divider_x, divider_bottom), 2)

        # Right panel
        panel_x = divider_x + 20
        panel_width = BOX_X + BOX_WIDTH - panel_x - 20

        # Draw close button
        self.screen.blit(close_button_scaled, (close_button_rect.x, close_button_rect.y))
        if close_button_rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, self.HOVER_COLOR, close_button_rect, 2)
            self.CLOSE_BTN_HOVERING = True
        else:
            self.CLOSE_BTN_HOVERING = False
        # Display selected item details
        item = self.inventory_logic.get_item(self.selected_index)
        if item:
            item_name = name_font.render(item.name, True, self.TEXT_COLOR)
            item_code = desc_font.render(f"Code: {item.code}", True, self.TEXT_COLOR)
            item_desc = textwrap.wrap(item.description, width=panel_width // 9)
        else:
            item_name = name_font.render("Empty Slot", True, self.TEXT_COLOR)
            item_code = desc_font.render("N/A", True, self.TEXT_COLOR)
            item_desc = textwrap.wrap("No item in this slot.", width=panel_width // 9)
        
        # Render item name
        item_name_x = panel_x + (panel_width - item_name.get_width()) // 2
        self.screen.blit(item_name, (item_name_x, GRID_Y + 10))

        # Render item code
        item_code_x = panel_x + (panel_width - item_code.get_width()) // 2
        self.screen.blit(item_code, (item_code_x, GRID_Y + 40))

        # Divider line
        pygame.draw.line(self.screen, self.LINE_COLOR, (panel_x, GRID_Y + 65), (panel_x + panel_width, GRID_Y + 65), 2)

        # Render description
        for i, line in enumerate(item_desc):
            desc = desc_font.render(line, True, self.TEXT_COLOR)
            self.screen.blit(desc, (panel_x, GRID_Y + 80 + i * 20))

    def _inventory_get_state(self):
        return self.state == "OPEN"
    
    def _inventory_set_state(self, new_state):
        self.state = new_state  
        if new_state == "CLOSED":
            self.selected_index = -1
            self.SLOT_HOVERING = False
            self.CLOSE_BTN_HOVERING = False   
            self.ICON_HOVERING = False

    def _hovering_icon(self):
        return self.ICON_HOVERING

    def _hovering_close_button(self):
        return self.CLOSE_BTN_HOVERING

    def _select_slot(self, mouse_pos):
        for i, slot in enumerate(self.inventory_rects):
            if slot.collidepoint(mouse_pos):
                return i
    
    def _handle_keys_inventory(self, key, mouse_pos):
        if key == pygame.K_RIGHT:
            self.selected_index = (self.selected_index + 1) % len(self.inventory_rects)
        elif key == pygame.K_LEFT:
            self.selected_index = (self.selected_index - 1) % len(self.inventory_rects)
        elif key == pygame.K_DOWN:
            self.selected_index = (self.selected_index + self.COLS) % len(self.inventory_rects)
        elif key == pygame.K_UP:
            self.selected_index = (self.selected_index - self.COLS) % len(self.inventory_rects)
        elif key == "LMB_CLICK":
            if self.SLOT_HOVERING:
                self.selected_index = self._select_slot(mouse_pos)
            elif self.ICON_HOVERING:
                self.state = "OPEN"
                self.selected_index = -1
                self.ICON_HOVERING = False
            elif self.CLOSE_BTN_HOVERING:
                self.state = "CLOSED"
                self.CLOSE_BTN_HOVERING = False



