import sys
import os
import pygame

# Ensure the project root is in sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.game import Game
from src.game_manager import GameManager, GameManagerState
from src.scenes.main_menu import MainMenu
from src.scenes.setting_menu import SettingsMenu

def main():
    pygame.init()
    
    # Screen setup
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 720
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("The Se7enth Code")
    clock = pygame.time.Clock()
    
    # Initialize game manager
    game_manager = GameManager(screen)
    
    # Initialize menus
    main_menu = MainMenu(screen, game_manager)
    settings_menu = SettingsMenu(screen, game_manager)
    load_menu = None  # TODO: Create SaveLoadMenu later
    
    # Initialize game instance
    game = Game()
    
    # Set references (bi-directional)
    game_manager.set_main_menu(main_menu)
    game_manager.set_settings_menu(settings_menu)
    if load_menu:
        game_manager.set_load_menu(load_menu)
    game_manager.set_game_instance(game)
    game.set_game_manager(game_manager)  # Allow game to call back to manager
    
    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle input based on current state
            if game_manager.get_current_state() == GameManagerState.MAIN_MENU:
                main_menu.handle_input(event)
            elif game_manager.get_current_state() == GameManagerState.PLAYING:
                # Let game handle its own events
                game.handle_events_single(event)
            elif game_manager.get_current_state() == GameManagerState.SETTINGS:
                settings_menu.handle_input(event)
            elif game_manager.get_current_state() == GameManagerState.LOAD_GAME and load_menu:
                load_menu.handle_input(event)
        
        # Update based on current state
        if game_manager.get_current_state() == GameManagerState.MAIN_MENU:
            main_menu.update()
        elif game_manager.get_current_state() == GameManagerState.PLAYING:
            game.update()
        elif game_manager.get_current_state() == GameManagerState.SETTINGS:
            settings_menu.update()
        elif game_manager.get_current_state() == GameManagerState.LOAD_GAME and load_menu:
            load_menu.update()
        
        # Draw based on current state
        screen.fill((0, 0, 0))
        if game_manager.get_current_state() == GameManagerState.MAIN_MENU:
            main_menu.draw()
        elif game_manager.get_current_state() == GameManagerState.PLAYING:
            game.draw()
        elif game_manager.get_current_state() == GameManagerState.SETTINGS:
            settings_menu.draw()
        elif game_manager.get_current_state() == GameManagerState.LOAD_GAME and load_menu:
            load_menu.draw()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()