"""
Game Manager - Manages game states and scene transitions
"""
import pygame
from enum import Enum

class GameManagerState(Enum):
    MAIN_MENU = 0
    PLAYING = 1
    SETTINGS = 2
    LOAD_GAME = 3

class GameManager:
    def __init__(self, screen):
        self.screen = screen
        self.state = GameManagerState.MAIN_MENU
        self._previous_state = None  # Track previous state
        self.game_instance = None
        self.main_menu = None
        self.settings_menu = None
        self.load_menu = None
        
    def set_main_menu(self, main_menu):
        """Set the main menu instance"""
        self.main_menu = main_menu
        
    def set_game_instance(self, game_instance):
        """Set the game instance"""
        self.game_instance = game_instance
        
    def set_settings_menu(self, settings_menu):
        """Set the settings menu instance"""
        self.settings_menu = settings_menu
        
    def set_load_menu(self, load_menu):
        """Set the load game menu instance"""
        self.load_menu = load_menu
    
    def start_new_game(self):
        """Start a new game"""
        self.state = GameManagerState.PLAYING
        if self.game_instance:
            # Reset game state for new game
            self.game_instance.reset_game()
        print("Starting new game...")
    
    def continue_game(self):
        """Continue existing game"""
        self.state = GameManagerState.PLAYING
        print("Continuing game...")
    
    def switch_to_main_menu(self):
        """Switch back to main menu"""
        self.state = GameManagerState.MAIN_MENU
        print("Switching to main menu...")
    
    def switch_to_settings(self):
        """Switch to settings menu"""
        self._previous_state = self.state  # Save current state before switching
        self.state = GameManagerState.SETTINGS
        print("Switching to settings...")
    
    def switch_to_load_menu(self):
        """Switch to load game menu"""
        self.state = GameManagerState.LOAD_GAME
        print("Switching to load game...")
    
    def get_current_state(self):
        """Get current game manager state"""
        return self.state
    
    def handle_input(self, event):
        """Handle input based on current state"""
        if self.state == GameManagerState.MAIN_MENU and self.main_menu:
            self.main_menu.handle_input(event)
        elif self.state == GameManagerState.PLAYING and self.game_instance:
            # Game handles its own input
            pass
        elif self.state == GameManagerState.SETTINGS and self.settings_menu:
            self.settings_menu.handle_input(event)
        elif self.state == GameManagerState.LOAD_GAME and self.load_menu:
            self.load_menu.handle_input(event)
    
    def update(self):
        """Update based on current state"""
        if self.state == GameManagerState.MAIN_MENU and self.main_menu:
            self.main_menu.update()
        elif self.state == GameManagerState.PLAYING and self.game_instance:
            self.game_instance.update()
        elif self.state == GameManagerState.SETTINGS and self.settings_menu:
            self.settings_menu.update()
        elif self.state == GameManagerState.LOAD_GAME and self.load_menu:
            self.load_menu.update()
    
    def draw(self):
        """Draw based on current state"""
        if self.state == GameManagerState.MAIN_MENU and self.main_menu:
            self.main_menu.draw()
        elif self.state == GameManagerState.PLAYING and self.game_instance:
            self.game_instance.draw()
        elif self.state == GameManagerState.SETTINGS and self.settings_menu:
            self.settings_menu.draw()
        elif self.state == GameManagerState.LOAD_GAME and self.load_menu:
            self.load_menu.draw()
