import pygame
import sys
import textwrap

# === IMPORTS FOR NOTEBOOK ===
from Notebook import Notebook
from Notebook_clues import * 

# === IMPORTS FOR INVENTORY ===
from Inventory_UI import *

# ======================
#  SHARED GAME SETTINGS
# ======================
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

BG_COLOR = (112, 128, 144)

# Notebook icon settings
CLOSED_BOOK_ICON_SIZE = (64, 64)
CLOSED_BOOK_ICON_POS = (SCREEN_WIDTH - CLOSED_BOOK_ICON_SIZE[0] - 20, 20)


# ======================
#  LOAD FONTS (From File 1)
# ======================
def load_fonts():
    fonts = {}
    try:
        fonts['list'] = pygame.font.Font("../Asset Package/Font/Harmonic.ttf", 36)
        fonts['title_options'] = {
            size: pygame.font.Font("../Asset Package/Font/Harmonic.ttf", size) 
            for size in [42, 36, 32, 28, 24]
        }
        fonts['desc_options'] = {
            size: pygame.font.Font("../Asset Package/Font/Harmonic.ttf", size) 
            for size in [36, 32, 28, 24]
        }
        fonts['page_count'] = pygame.font.Font("../Asset Package/Font/Harmonic.ttf", 28)

    except FileNotFoundError:
        print("Warning: Harmonic.ttf missing, using default font.")
        fonts['list'] = pygame.font.Font(None, 40)
        fonts['title_options'] = {size: pygame.font.Font(None, size + 4) for size in [42, 36, 32, 28, 24]}
        fonts['desc_options'] = {size: pygame.font.Font(None, size + 4) for size in [36, 32, 28, 24]}
        fonts['page_count'] = pygame.font.Font(None, 32)

    return fonts


# ======================
#  LOAD IMAGES (From File 1)
# ======================
def load_images():
    images = {}
    images['closed_book_icon'] = pygame.image.load("../Asset Package/brownbook.png").convert_alpha()
    images['closed_book_icon'] = pygame.transform.scale(images['closed_book_icon'], CLOSED_BOOK_ICON_SIZE)
    return images

# ======================
#        MAIN GAME
# ======================
def main():
    pygame.init()
    pygame.font.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("The Se7enth Code + Notebook System")
    clock = pygame.time.Clock()

    #Inventory System
    inventory_ui = InventoryUI(screen)

    # Notebook System
    all_fonts = load_fonts()
    all_images = load_images()
    game_notebook = Notebook(
        screen=screen,
        clock=clock,
        clues_data=clues,
        fonts=all_fonts,
        screen_width=SCREEN_WIDTH,
        screen_height=SCREEN_HEIGHT
    )
    closed_book_icon_rect = pygame.Rect(CLOSED_BOOK_ICON_POS, CLOSED_BOOK_ICON_SIZE)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(BG_COLOR)

        # ===============================
        #          EVENT LOOP
        # ===============================
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # ============================
            #         NOTEBOOK EVENTS
            # ============================
            if not game_notebook.get_state():  
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if closed_book_icon_rect.collidepoint(mouse_pos):
                        game_notebook.open_notebook()

            else:
                game_notebook.handle_event(event, mouse_pos)

            # ============================
            #        INVENTORY EVENTS
            # ============================
            if not inventory_ui._inventory_get_state():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        inventory_ui._inventory_set_state("OPEN")
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        inventory_ui._handle_keys_inventory("LMB_CLICK", mouse_pos)
            else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE or event.key == pygame.K_e:
                            inventory_ui._inventory_set_state("CLOSED")
                        else:
                            inventory_ui._handle_keys_inventory(event.key, mouse_pos)
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            inventory_ui._handle_keys_inventory("LMB_CLICK", mouse_pos)


        # ===============================
        #          UPDATE LOGIC
        # ===============================
        game_notebook.update()

        # ===============================
        #            DRAWING
        # ===============================
        # Draw Notebook
        if game_notebook.get_state():
            game_notebook.draw(mouse_pos)
        else:
            screen.blit(all_images['closed_book_icon'], closed_book_icon_rect)
            if closed_book_icon_rect.collidepoint(mouse_pos):
                pygame.draw.rect(screen, (255, 255, 255), closed_book_icon_rect, 2)

        # Draw Inventory
        if not inventory_ui._inventory_get_state():
            inventory_ui.draw_inventory_icon(mouse_pos)
        else:
            inventory_ui.initialize_inventory()
            inventory_ui.draw_inventory(mouse_pos)
        # Final update
        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
