import pygame
import sys
from enum import Enum

from scenes.envy_case import EnvyCaseScene
from scenes.wrath_case import WrathCaseScene
from src.ui.main_scene import MainSceneUi
from src.scenes.office import OfficeScene
from src.scenes.interrogation_room import InterrogationRoomScene
from src.tools.Notebook import Notebook
from src.tools.Notebook_clues import * 
from src.tools.Inventory_UI import *

from src.player import Player
from src.scenes.greed_case import GreedCaseScene
from src.scenes.gluttony_case import GluttonyScene
from src.scenes.lust_case import LustScene
from src.scenes.pride_case import PrideScene

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
        self.init_inventory() # FIX: Ensure this initializes the instance
        self.init_notebook()

    def load_assets(self):
        self.closed_book_icon_size = (64, 64)
        self.closed_book_icon_pos = (self.SCREEN_WIDTH - self.closed_book_icon_size[0] - 20, 20)
        self.closed_book_icon_rect = pygame.Rect(self.closed_book_icon_pos, self.closed_book_icon_size)
        
        try:
            self.closed_book_icon = pygame.image.load("assets/images/tools/brownbook.png").convert_alpha()
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
        self.scenes = {
            "office": OfficeScene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT),
            "interrogation_room": InterrogationRoomScene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT),
            "toa_thi_chinh": InterrogationRoomScene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT), # Placeholder
            "envy": EnvyCaseScene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT), # Added Envy
            "wrath": WrathCaseScene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT), # Added Wrath
            "greed": GreedCaseScene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT), # Added Greed
            "gluttony": GluttonyScene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT),
            "lust": LustScene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT),
            "pride": PrideScene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT) # New Pride Scene
        }
        self.current_scene = self.scenes["office"] # Start in Pride scene for testing
        
        # Set player reference for collision detection
        if hasattr(self.current_scene, 'set_player'):
            self.current_scene.set_player(self.player)

    def init_inventory(self):
        # FIX: Initialize the InventoryUI instance correctly
        self.inventory_ui = InventoryUI(self.screen)
        self.inventory_ui.initialize_inventory()

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
            fonts['list'] = pygame.font.Font("assets/fonts/Harmonic.ttf", 36)
            font_title_sizes = [42, 36, 32, 28, 24]
            fonts['title_options'] = {size: pygame.font.Font("assets/fonts/Harmonic.ttf", size) for size in font_title_sizes}
            font_desc_sizes = [36, 32, 28, 24]
            fonts['desc_options'] = {size: pygame.font.Font(None, size + 4) for size in font_desc_sizes}
            fonts['page_count'] = pygame.font.Font("assets/fonts/Harmonic.ttf", 28)
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
            
            # Reset player position to middle of the screen for the new scene
            self.player.x = self.SCREEN_WIDTH // 2
            self.player.y = self.SCREEN_HEIGHT // 2
            self.player.rect.x = self.player.x
            self.player.rect.y = self.player.y

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

                # --- Global ESC key check ---
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    if self.state == GameState.NOTEBOOK:
                        self.notebook.close_notebook()
                        self.state = GameState.PLAYING
                    elif self.state == GameState.INVENTORY:
                        self.inventory_ui._inventory_set_state("CLOSED")
                        self.state = GameState.PLAYING
                
                # --- Global Toggles (E key for Notebook, R key for Inventory) ---
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e: # Toggle Notebook
                        if self.state == GameState.NOTEBOOK:
                            self.notebook.close_notebook()
                            self.state = GameState.PLAYING
                        elif self.state == GameState.PLAYING:
                            # Đảm bảo Inventory đang đóng trước khi mở Notebook
                            if self.inventory_ui._inventory_get_state():
                                self.inventory_ui._inventory_set_state("CLOSED")
                            
                            self.notebook.open_notebook()
                            self.state = GameState.NOTEBOOK
                            
                    elif event.key == pygame.K_r: # Toggle Inventory (NEW LOGIC)
                        if self.state == GameState.INVENTORY:
                            self.inventory_ui._inventory_set_state("CLOSED")
                            self.state = GameState.PLAYING
                        elif self.state == GameState.PLAYING:
                            # Đảm bảo Notebook đang đóng trước khi mở Inventory
                            if self.notebook.get_state():
                                self.notebook.close_notebook()
                            
                            self.inventory_ui._inventory_set_state("OPEN")
                            self.state = GameState.INVENTORY
                            
                    # --- SCENE SWITCHING LOGIC (New addition for quick testing) ---
                    if self.state == GameState.PLAYING:
                        if event.key == pygame.K_1:
                            self.change_scene("office")
                        elif event.key == pygame.K_2:
                            self.change_scene("interrogation_room")
                        elif event.key == pygame.K_3:
                            self.change_scene("pride")
                        elif event.key == pygame.K_4:
                            self.change_scene("lust")
                        elif event.key == pygame.K_5:
                            self.change_scene("gluttony")
                        elif event.key == pygame.K_6:
                            self.change_scene("greed")
                        elif event.key == pygame.K_7:
                            self.change_scene("envy")
                        elif event.key == pygame.K_8:
                            self.change_scene("wrath")
                        #elif event.key == pygame.K_9:
                            #self.change_scene("toa_thi_chinh")


                # --- State-specific handling ---
                if self.state == GameState.NOTEBOOK:
                    self.notebook.handle_event(event, mouse_pos)
                    # Nếu notebook tự đóng (ví dụ: do ấn nút tắt bên trong), cập nhật state
                    if not self.notebook.get_state():
                        self.state = GameState.PLAYING

                elif self.state == GameState.INVENTORY:
                    # Inventory handling for movement and clicks
                    if event.type == pygame.KEYDOWN:
                        self.inventory_ui._handle_keys_inventory(event.key, mouse_pos)
                    elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        self.inventory_ui._handle_keys_inventory("LMB_CLICK", mouse_pos)
                        # Nếu inventory tự đóng (ví dụ: do click vào nút tắt), cập nhật state
                        if not self.inventory_ui._inventory_get_state():
                            self.state = GameState.PLAYING

                elif self.state == GameState.PLAYING:
                    # Loại bỏ logic click icon Notebook vì giờ dùng phím 'E'
                    # Loại bỏ logic click icon Inventory vì giờ dùng phím 'R'
                    
                    # Notebook icon click - Giữ lại nếu người dùng vẫn muốn click
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        if self.closed_book_icon_rect.collidepoint(mouse_pos):
                            self.notebook.open_notebook()
                            self.state = GameState.NOTEBOOK

                        # Inventory icon click (chỉ handle khi chưa vào Inventory state)
                        # Vẫn gọi để cập nhật trạng thái Inventory khi click vào icon của nó
                        self.inventory_ui._handle_keys_inventory("LMB_CLICK", mouse_pos)
                        if self.inventory_ui._inventory_get_state():
                            self.state = GameState.INVENTORY

                    # UI + Scene
                    self.ui.handle_event(event)
                    if hasattr(self.current_scene, 'handle_event'):
                        self.current_scene.handle_event(event)

            # --- Continuous Input ---
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

        # Draw Scene with layer system (including player)
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
            # FIX: Use instance method, which only needs mouse_pos
            self.inventory_ui.draw_inventory_icon(mouse_pos)

        # Draw Notebook (Overlay)
        if self.state == GameState.NOTEBOOK:
            self.notebook.draw(mouse_pos)

        # Draw Inventory (Overlay)
        if self.state == GameState.INVENTORY:
            # FIX: Call initialize before drawing open inventory, and use instance method
            self.inventory_ui.initialize_inventory()
            self.inventory_ui.draw_inventory(mouse_pos)

        pygame.display.flip()