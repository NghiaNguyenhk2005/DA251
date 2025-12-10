import pygame
import sys
from enum import Enum

from scenes.envy_case import EnvyCaseScene
from scenes.wrath_case import WrathCaseScene
from src.ui.main_scene import MainSceneUi
from src.scenes.office import OfficeScene
from src.scenes.interrogation_room import InterrogationRoomScene
from src.notebook.notebook import Notebook
from src.notebook.clues_data import clues
import src.inventory.GUI_Func as InventoryUI
from src.inventory.Item import item_list
from src.player import Player
from src.scenes.greed_case import GreedCaseScene
from src.scenes.sloth_case import SlothCaseScene

class GameState(Enum):
    MENU = 0
    PLAYING = 1
    INVENTORY = 2
    NOTEBOOK = 3

class Game:
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("The Se7enth Code")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.PLAYING 

        # Assets
        self.load_assets()

        # Systems
        self.init_player()  # Initialize player first
        self.init_ui()
        self.init_scenes()  # Then scenes (which may reference player)
        self.init_inventory()
        self.init_notebook()

    def load_assets(self):
        self.closed_book_icon_size = (64, 64)
        self.closed_book_icon_pos = (self.SCREEN_WIDTH - self.closed_book_icon_size[0] - 20, 20)
        self.closed_book_icon_rect = pygame.Rect(self.closed_book_icon_pos, self.closed_book_icon_size)
        
        try:
            self.closed_book_icon = pygame.image.load("src/assets/notebook/brownbook.png").convert_alpha()
            self.closed_book_icon = pygame.transform.scale(self.closed_book_icon, self.closed_book_icon_size)
        except FileNotFoundError:
            print("Warning: brownbook.png not found. Creating placeholder.")
            self.closed_book_icon = pygame.Surface(self.closed_book_icon_size)
            self.closed_book_icon.fill((139, 69, 19))

    def init_ui(self):
        self.ui = MainSceneUi(
            screen_width=self.SCREEN_WIDTH,
            screen_height=self.SCREEN_HEIGHT,
            on_building_click=self.change_scene
        )

    def init_scenes(self):
        # Initialize all scenes
        self.scenes = {
            "office": OfficeScene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT),
            "interrogation_room": InterrogationRoomScene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT),
            "toa_thi_chinh": InterrogationRoomScene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT),  # Placeholder
            
            # 7 Deadly Sins Cases
            "greed_case": GreedCaseScene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT),
            "envy_case": EnvyCaseScene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT),
            "wrath_case": WrathCaseScene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT),
            "sloth_case": SlothCaseScene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT),
            # TODO: Add remaining cases when implemented
            # "gluttony_case": GluttonyCaseScene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT),
            # "lust_case": LustCaseScene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT),
            # "pride_case": PrideCaseScene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT),
        }
        self.current_scene = self.scenes["office"]
        
        # Set player reference for collision detection
        if hasattr(self.current_scene, 'set_player'):
            self.current_scene.set_player(self.player)

    def init_inventory(self):
        InventoryUI.initialize_inventory()

    def init_notebook(self):
        fonts = self.load_notebook_fonts()
        self.notebook = Notebook(
            screen=self.screen,
            clock=self.clock,
            clues_data=clues,
            fonts=fonts,
            screen_width=self.SCREEN_WIDTH,
            screen_height=self.SCREEN_HEIGHT
        )

    def init_player(self):
        # Start player in the middle of the screen
        self.player = Player(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)

    def load_notebook_fonts(self):
        fonts = {}
        try:
            fonts['list'] = pygame.font.Font("src/assets/fonts/Harmonic.ttf", 36)
            font_title_sizes = [42, 36, 32, 28, 24]
            fonts['title_options'] = {size: pygame.font.Font("src/assets/fonts/Harmonic.ttf", size) for size in font_title_sizes}
            font_desc_sizes = [36, 32, 28, 24]
            fonts['desc_options'] = {size: pygame.font.Font("src/assets/fonts/Harmonic.ttf", size) for size in font_desc_sizes}
            fonts['page_count'] = pygame.font.Font("src/assets/fonts/Harmonic.ttf", 28)
        except FileNotFoundError:
            print("Warning: 'Harmonic.ttf' not found. Using default font.")
            fonts['list'] = pygame.font.Font(None, 40)
            font_title_sizes = [42, 36, 32, 28, 24]
            fonts['title_options'] = {size: pygame.font.Font(None, size + 4) for size in font_title_sizes}
            font_desc_sizes = [36, 32, 28, 24]
            fonts['desc_options'] = {size: pygame.font.Font(None, size + 4) for size in font_desc_sizes}
            fonts['page_count'] = pygame.font.Font(None, 32)
        return fonts

    def change_scene(self, scene_id):
        if scene_id in self.scenes:
            self.current_scene = self.scenes[scene_id]
            
            # Set player reference for collision detection
            if hasattr(self.current_scene, 'set_player'):
                self.current_scene.set_player(self.player)
                
            print(f"Switched to scene: {scene_id}")
        else:
            print(f"Scene {scene_id} not found!")

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()

    def handle_events(self):
        mouse_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            # Toggle Inventory
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    if self.state == GameState.INVENTORY:
                        self.state = GameState.PLAYING
                    elif self.state == GameState.PLAYING:
                        self.state = GameState.INVENTORY
                        InventoryUI.initialize_inventory()

            # Notebook events
            if self.state == GameState.NOTEBOOK:
                self.notebook.handle_event(event, mouse_pos)
                if not self.notebook.get_state(): # Closed
                    self.state = GameState.PLAYING
            elif self.state == GameState.PLAYING:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.closed_book_icon_rect.collidepoint(mouse_pos):
                        self.notebook.open_notebook()
                        self.state = GameState.NOTEBOOK

            # Inventory events
            if self.state == GameState.INVENTORY:
                if event.type == pygame.KEYDOWN:
                     if event.key == pygame.K_ESCAPE:
                         self.state = GameState.PLAYING
                     else:
                         InventoryUI.handle_keys_inventory(event.key, mouse_pos)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        InventoryUI.handle_keys_inventory("LMB_CLICK", mouse_pos)
                        if InventoryUI.get_close_btn_flag():
                            self.state = GameState.PLAYING
                            InventoryUI.set_close_btn_flag(False)

            # UI events (Map, etc)
            if self.state == GameState.PLAYING:
                self.ui.handle_event(event)
                
                # Scene-specific events (for evidence collection, etc)
                if hasattr(self.current_scene, 'handle_event'):
                    self.current_scene.handle_event(event)
                
            # Inventory Icon Click (in Playing mode)
            if self.state == GameState.PLAYING:
                 if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                     if InventoryUI.get_icon_flag():
                         self.state = GameState.INVENTORY
                         InventoryUI.initialize_inventory()

        # Player Movement (Continuous Input)
        if self.state == GameState.PLAYING:
            self.player.handle_input(keys)

    def update(self):
        if self.state == GameState.PLAYING:
            # Store old position before update for collision rollback
            old_x = self.player.x
            old_y = self.player.y
            
            # Update scene (pass delta time if needed)
            dt = self.clock.get_time() / 1000.0  # Convert to seconds
            if hasattr(self.current_scene, 'update'):
                # Check if update accepts dt parameter
                import inspect
                sig = inspect.signature(self.current_scene.update)
                if len(sig.parameters) > 0:
                    self.current_scene.update(dt)
                else:
                    self.current_scene.update()
            
            # Update player position
            self.player.update()
            
            # Check collision with current scene (if scene supports collision)
            if hasattr(self.current_scene, 'check_collision'):
                if self.current_scene.check_collision(self.player.rect):
                    # Prevent collision - use sliding collision if available
                    if hasattr(self.current_scene, 'prevent_collision'):
                        new_x, new_y = self.current_scene.prevent_collision(
                            self.player.rect, old_x, old_y
                        )
                        self.player.x = new_x
                        self.player.y = new_y
                        self.player.rect.x = new_x
                        self.player.rect.y = new_y
                    else:
                        # Simple rollback
                        self.player.x = old_x
                        self.player.y = old_y
                        self.player.rect.x = old_x
                        self.player.rect.y = old_y
            
            # Update UI
            self.ui.update()
        elif self.state == GameState.NOTEBOOK:
            self.notebook.update()
        elif self.state == GameState.INVENTORY:
            pass 

    def draw(self):
        self.screen.fill((0, 0, 0))
        mouse_pos = pygame.mouse.get_pos()

        # Draw Scene với layer system (bao gồm cả player)
        if self.state == GameState.PLAYING:
            # Nếu scene hỗ trợ layer system, dùng draw_with_player
            if hasattr(self.current_scene, 'draw_with_player'):
                self.current_scene.draw_with_player(self.screen, self.player)
            else:
                # Fallback: vẽ scene rồi vẽ player
                self.current_scene.draw(self.screen)
                self.player.draw(self.screen)
        else:
            # Khi không PLAYING, chỉ vẽ scene
            self.current_scene.draw(self.screen)

        # Draw UI
        self.ui.draw(self.screen)

        # Draw Notebook Icon (if not open)
        if not self.notebook.get_state():
             self.screen.blit(self.closed_book_icon, self.closed_book_icon_rect)
             if self.closed_book_icon_rect.collidepoint(mouse_pos):
                 pygame.draw.rect(self.screen, (255, 255, 255), self.closed_book_icon_rect, 2)

        # Draw Inventory Icon (if not in inventory)
        if self.state != GameState.INVENTORY:
            InventoryUI.draw_inventory_icon(self.screen, mouse_pos)

        # Draw Notebook (Overlay)
        if self.state == GameState.NOTEBOOK:
            self.notebook.draw(mouse_pos)

        # Draw Inventory (Overlay)
        if self.state == GameState.INVENTORY:
            InventoryUI.draw_inventory(self.screen, mouse_pos)

        pygame.display.flip()
