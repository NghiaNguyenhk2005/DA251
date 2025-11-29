import pygame
import sys
import textwrap
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
