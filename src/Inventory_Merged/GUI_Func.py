import pygame
import sys
import textwrap
from Inventory_Manager import InventoryManager
from Item import item_list

# Inventory configuration
ROWS, COLS = 6, 4
SLOT_SIZE = 40
MARGIN = 12

# Colors
BOX_COLOR = (20, 20, 20)
LINE_COLOR = (100, 100, 100)
TEXT_COLOR = (220, 220, 220)
HOVER_COLOR = (211, 211, 211)
HIGHLIGHT_COLOR = (255, 255, 0)
ICON_HIGHLIGHT_COLOR = (255, 215, 0)

#FLAG
ICON_HOVERING = False
SLOT_HOVERING = False
CLOSE_BTN_HOVERING = False

inventory_logic = InventoryManager(ROWS, COLS)
inventory = []
selected_index = -1

# Extract slot sprite
def get_sprite(sheet, x, y, width, height):
    sprite = pygame.Surface((width, height), pygame.SRCALPHA)
    sprite.blit(sheet, (0, 0), (x, y, width, height))
    return sprite

# Slice border sprite into 9 parts
def slice_9(sprite):
    tile = 16
    slices = {}
    for row in range(3):
        for col in range(3):
            key = (row, col)
            x = col * tile
            y = row * tile
            part = pygame.Surface((tile, tile), pygame.SRCALPHA)
            part.blit(sprite, (0, 0), (x, y, tile, tile))
            slices[key] = part
    return slices

# Draw a box using 9-slice technique
def draw_9slice_box(screen, slices, x, y, width, height):
    tile = 16
    # Corners
    screen.blit(slices[(0, 0)], (x, y))
    screen.blit(slices[(0, 2)], (x + width - tile, y))
    screen.blit(slices[(2, 0)], (x, y + height - tile))
    screen.blit(slices[(2, 2)], (x + width - tile, y + height - tile))

    # Edges
    for i in range(tile, width - tile, tile):
        screen.blit(slices[(0, 1)], (x + i, y))
        screen.blit(slices[(2, 1)], (x + i, y + height - tile))
    for j in range(tile, height - tile, tile):
        screen.blit(slices[(1, 0)], (x, y + j))
        screen.blit(slices[(1, 2)], (x + width - tile, y + j))

    # Center
    for i in range(tile, width - tile, tile):
        for j in range(tile, height - tile, tile):
            screen.blit(slices[(1, 1)], (x + i, y + j))

def initialize_inventory():
    global inventory_logic, inventory, ROWS, COLS
    inventory.clear()
    inventory_logic = InventoryManager(ROWS, COLS)
    for i, item in enumerate(item_list):
        inventory_logic.add_item(item, i)

def draw_inventory_icon(screen, mouse_pos):
    global ICON_HOVERING

    WIDTH, HEIGHT = screen.get_size()
    ICON_WIDTH, ICON_HEIGHT = 68, 77
    ICON_X = WIDTH - ICON_WIDTH - 20
    ICON_Y = ICON_HEIGHT + 50 - 20

    # Load inventory icon sprite sheet
    inventory_icon_sprite_sheet = pygame.image.load("Asset Package/UI_Inventory_icon.png").convert_alpha()
    inventory_icon_sprite = get_sprite(inventory_icon_sprite_sheet, 20, 15, 85, 100)
    inventory_icon_scaled = pygame.transform.scale(inventory_icon_sprite, (ICON_WIDTH, ICON_HEIGHT))

    icon_rect = pygame.Rect(ICON_X, ICON_Y, ICON_WIDTH, ICON_HEIGHT)
    screen.blit(inventory_icon_scaled, (ICON_X, ICON_Y))

    if icon_rect.collidepoint(mouse_pos):
        ICON_HOVERING = True
        pygame.draw.rect(screen, ICON_HIGHLIGHT_COLOR, icon_rect, 2)
    else:
        ICON_HOVERING = False

def draw_inventory(screen, mouse_pos):
    # Inventory settings
    global ROWS
    global COLS
    global LINE_COLOR
    global BOX_COLOR
    global TEXT_COLOR
    global HIGHLIGHT_COLOR
    global SLOT_HOVERING
    global CLOSE_BTN_HOVERING
    global inventory_logic
    global inventory
    global selected_index

    WIDTH, HEIGHT = screen.get_size()
    BOX_WIDTH, BOX_HEIGHT = 650, 400
    BOX_X = (WIDTH - BOX_WIDTH) // 2
    BOX_Y = (HEIGHT - BOX_HEIGHT) // 2

    GRID_X = BOX_X + 30
    GRID_Y = BOX_Y + 60

    CLOSE_BTN_SCALE = 2
    CLOSE_BTN_SIZE = 13 * CLOSE_BTN_SCALE  # 26x26

    if not inventory:
        for i in range(ROWS * COLS):
            col = i % COLS
            row = i // COLS
            x = GRID_X + col * (SLOT_SIZE + MARGIN)
            y = GRID_Y + row * (SLOT_SIZE + MARGIN)
            inventory.append(pygame.Rect(x, y, SLOT_SIZE, SLOT_SIZE))

    # Load assets
    inventory_sprite_sheet = pygame.image.load("Asset Package/UI Inventory.png").convert_alpha()
    border_sprite_sheet = pygame.image.load("Asset Package/BlackGrey UI Border.png").convert_alpha()
    button_sprite_sheet = pygame.image.load("Asset Package/UI Buttons.png").convert_alpha()

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
    pygame.draw.rect(screen, BOX_COLOR, (BOX_X, BOX_Y, BOX_WIDTH, BOX_HEIGHT))
    draw_9slice_box(screen, slices, BOX_X, BOX_Y, BOX_WIDTH, BOX_HEIGHT)

    # Title label with 9-slice border
    title_text = title_font.render("INVENTORY", True, TEXT_COLOR)
    title_rect = title_text.get_rect(center=(BOX_X + BOX_WIDTH // 2, BOX_Y - 0))
    label_bg_rect = title_rect.inflate(40, 20)
    draw_9slice_box(screen, slices, label_bg_rect.x, label_bg_rect.y, label_bg_rect.width, label_bg_rect.height)
    screen.blit(title_text, title_rect)

    # Left panel: inventory grid
    SLOT_HOVERING = False
    for i, slot in enumerate(inventory):
        screen.blit(slot_sprite, (slot.x, slot.y))
        if slot.collidepoint(mouse_pos):
            SLOT_HOVERING = True
            pygame.draw.rect(screen, HOVER_COLOR, slot, 2)
        if i == selected_index:
            pygame.draw.rect(screen, HIGHLIGHT_COLOR, slot, 2)
    # Divider line
    divider_x = GRID_X + COLS * (SLOT_SIZE + MARGIN) + 20
    divider_top = GRID_Y
    divider_bottom = GRID_Y + ROWS * (SLOT_SIZE + MARGIN) - MARGIN
    pygame.draw.line(screen, LINE_COLOR, (divider_x, divider_top), (divider_x, divider_bottom), 2)

    # Right panel
    panel_x = divider_x + 20
    panel_width = BOX_X + BOX_WIDTH - panel_x - 20

    # Draw close button
    screen.blit(close_button_scaled, (close_button_rect.x, close_button_rect.y))
    if close_button_rect.collidepoint(mouse_pos):
        pygame.draw.rect(screen, HOVER_COLOR, close_button_rect, 2)
        CLOSE_BTN_HOVERING = True
    # Display selected item details
    item = inventory_logic.get_item(selected_index)
    if item:
        item_name = name_font.render(item.name, True, TEXT_COLOR)
        item_code = desc_font.render(f"Code: {item.code}", True, TEXT_COLOR)
        item_desc = textwrap.wrap(item.description, width=panel_width // 9)
    else:
        item_name = name_font.render("Empty Slot", True, TEXT_COLOR)
        item_code = desc_font.render("N/A", True, TEXT_COLOR)
        item_desc = textwrap.wrap("No item in this slot.", width=panel_width // 9)
    
    # Render item name
    item_name_x = panel_x + (panel_width - item_name.get_width()) // 2
    screen.blit(item_name, (item_name_x, GRID_Y + 10))

    # Render item code
    item_code_x = panel_x + (panel_width - item_code.get_width()) // 2
    screen.blit(item_code, (item_code_x, GRID_Y + 40))

    # Divider line
    pygame.draw.line(screen, LINE_COLOR, (panel_x, GRID_Y + 65), (panel_x + panel_width, GRID_Y + 65), 2)

    # Render description
    for i, line in enumerate(item_desc):
        desc = desc_font.render(line, True, TEXT_COLOR)
        screen.blit(desc, (panel_x, GRID_Y + 80 + i * 20))

def get_icon_flag():
    global ICON_HOVERING
    return ICON_HOVERING

def get_slot_flag():
    global SLOT_HOVERING
    return SLOT_HOVERING

def get_close_btn_flag():
    global CLOSE_BTN_HOVERING
    return CLOSE_BTN_HOVERING

def set_close_btn_flag(value):
    global CLOSE_BTN_HOVERING
    CLOSE_BTN_HOVERING = value

def select_slot(mouse_pos):
    for i, slot in enumerate(inventory):
        if slot.collidepoint(mouse_pos):
            return i
    return -1
def handle_keys_inventory(key, mouse_pos):
    return handle_keys_inventory_handler(key, mouse_pos, inventory, COLS)

def handle_keys_inventory_handler(key, mouse_pos, inventory, COLS):
    global selected_index
    global SLOT_HOVERING

    if key == pygame.K_RIGHT:
        selected_index = (selected_index + 1) % len(inventory)
    elif key == pygame.K_LEFT:
        selected_index = (selected_index - 1) % len(inventory)
    elif key == pygame.K_DOWN:
        selected_index = (selected_index + COLS) % len(inventory)
    elif key == pygame.K_UP:
        selected_index = (selected_index - COLS) % len(inventory)
    elif key == "LMB_CLICK":
        if SLOT_HOVERING:
            selected_index = select_slot(mouse_pos)



