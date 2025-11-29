import pygame
import sys
import textwrap
from GUI_Func import *
from Inventory_Manager import InventoryManager
from Item import item_list

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("The Se7enth code")
clock = pygame.time.Clock()

BG_COLOR = (112, 128, 144)

inventory_visible = False

# Main loop
while True:
    screen.fill(BG_COLOR)
    mouse_pos = pygame.mouse.get_pos()

    if not inventory_visible:
        draw_inventory_icon(screen, mouse_pos)
    else:
        initialize_inventory()
        draw_inventory(screen, mouse_pos)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Toggle inventory with 'E'
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                inventory_visible = not inventory_visible
            elif inventory_visible:
                if event.key == pygame.K_ESCAPE:
                    inventory_visible = False
                else:
                    handle_keys_inventory(event.key, mouse_pos)

        # Handle LMB click in inventory
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not inventory_visible and event.button == 1:
                if get_icon_flag():
                    inventory_visible = True
            if inventory_visible and event.button == 1:
                handle_keys_inventory("LMB_CLICK", mouse_pos)  # LMB
                if get_close_btn_flag():
                    inventory_visible = False
                    set_close_btn_flag(False)
    pygame.display.flip()
    clock.tick(60)