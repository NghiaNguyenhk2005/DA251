# --- FILE: src/game.py ---
import pygame
import sys
from enum import Enum

# --- IMPORTS ---
from src.scenes.envy_case import EnvyCaseScene
from src.scenes.wrath_case import WrathCaseScene
from src.ui.main_scene import MainSceneUi
from src.scenes.office import OfficeScene
from src.scenes.interrogation_room import InterrogationRoomScene
from src.tools.Notebook import Notebook
from src.tools.Notebook_clues import * 
from src.tools.Inventory_UI import *

from src.player import Player
from src.scenes.greed_case import GreedCaseScene
from src.scenes.gluttony_case import GluttonyCaseScene
from src.scenes.lust_case import LustCaseScene
from src.scenes.pride_case import PrideCaseScene 
from src.scenes.sloth_case import SlothCaseScene

# Import Dialogue
from src.tools.dialogue import DialogueBox

class GameState(Enum):
    MENU = 0
    PLAYING = 1
    INVENTORY = 2
    NOTEBOOK = 3
    ACCUSATION = 4
    DIALOGUE = 5

class Game:
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Seven Deadly Sins")
        self.clock = pygame.time.Clock()
        self.running = True
        self.state = GameState.PLAYING 
        self.game_manager = None 

        # Assets
        self.load_assets()

        # Systems
        self.init_player()  
        self.init_ui()
        self.init_inventory() 
        self.init_notebook()
        
        # --- KHỞI TẠO DIALOGUE UI (QUAN TRỌNG) ---
        # Đặt tên là dialogue_ui để khớp với hàm start_dialogue
        self.dialogue_ui = DialogueBox(self.screen)
        
        # Init Scenes (Phải để sau khi có self.dialogue_ui để truyền self vào scene)
        self.init_scenes()  

    def set_game_manager(self, game_manager):
        self.game_manager = game_manager

    # --- HÀM TRUNG GIAN KÍCH HOẠT HỘI THOẠI ---
    def start_dialogue(self, dialogue_id):
        """Scene sẽ gọi hàm này để bắt đầu hội thoại"""
        if hasattr(self, 'dialogue_ui') and self.dialogue_ui is not None:
            print(f"▶️ Game System starting dialogue: {dialogue_id}")
            self.dialogue_ui.start_conversation(dialogue_id)
            self.state = GameState.DIALOGUE # Chuyển state ngay lập tức
        else:
            print(f"⚠️ Cannot start dialogue '{dialogue_id}': Dialogue UI not initialized!")

    def open_settings(self):
        print("Opening settings from game...")
        if self.game_manager:
            self.game_manager.switch_to_settings()
    
    def quit_to_menu(self):
        print("Quitting to main menu...")
        if self.game_manager:
            self.game_manager.switch_to_main_menu()
    
    def open_accusation_system(self):
        print("Opening accusation system...")
        from src.scenes.accusation_system import AccusationSystem
        self.accusation_system = AccusationSystem(
            self.screen,
            self.game_manager
        )
        self.state = GameState.ACCUSATION
    
    def close_accusation_system(self):
        print("Closing accusation system, returning to office...")
        self.accusation_system = None
        self.state = GameState.PLAYING
        self.change_scene("office")

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
            on_building_click=self.change_scene,
            on_settings_click=self.open_settings,
            on_quit_click=self.quit_to_menu
        )

    def init_scenes(self):
        # Truyền game_system=self vào TẤT CẢ các scene điều tra để chúng gọi được start_dialogue
        self.scenes = {
            "office": OfficeScene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, on_scene_change=self.change_scene),
            "interrogation_room": InterrogationRoomScene(
                self.SCREEN_WIDTH, 
                self.SCREEN_HEIGHT,
                on_interrogation_complete=self.open_accusation_system
            ),
            
            # Các Scene vụ án (Đầy đủ)
            "greed_case": GreedCaseScene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, game_system=self),
            "envy_case": EnvyCaseScene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, game_system=self),
            "wrath_case": WrathCaseScene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, game_system=self),
            "sloth_case": SlothCaseScene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, game_system=self),
            "gluttony_case": GluttonyCaseScene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, game_system=self),
            "lust_case": LustCaseScene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, game_system=self),
            "pride_case": PrideCaseScene(self.SCREEN_WIDTH, self.SCREEN_HEIGHT, game_system=self),
        }
        self.current_scene = self.scenes["office"] 
        
        if hasattr(self.current_scene, 'set_player'):
            self.current_scene.set_player(self.player)

    def init_inventory(self):
        self.inventory_ui = InventoryUI(self.screen)
        self.inventory_ui.initialize_inventory()

    def add_item_to_inventory(self, item) -> bool:
        if self.inventory_ui and self.inventory_ui.inventory_logic:
            success = self.inventory_ui.inventory_logic.add_item(item)
            if success:
                print(f"📦 Collected: {item.name}")
            else:
                print(f"❌ Inventory is full. Could not collect: {item.name}")
            return success
        return False

    def remove_item_from_inventory(self, item) -> bool:
        if self.inventory_ui and self.inventory_ui.inventory_logic:
            success = self.inventory_ui.inventory_logic.remove_item(item)
            return success
        return False
    
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
        self.player = Player(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2)

    def load_notebook_fonts(self):
        fonts = {}
        try:
            fonts['list'] = pygame.font.Font("assets/fonts/Harmonic.ttf", 36)
            font_title_sizes = [42, 36, 32, 28, 24]
            fonts['title_options'] = {size: pygame.font.Font("assets/fonts/Harmonic.ttf", size) for size in font_title_sizes}
            font_desc_sizes = [36, 32, 28, 24]
            fonts['desc_options'] = {size: pygame.font.Font("assets/fonts/Harmonic.ttf", size + 4) for size in font_desc_sizes}
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
            # Special handling for interrogation room - use custom background and suspect if available
            if scene_id == "interrogation_room":
                office_scene = self.scenes.get("office")
                bg_path = None
                suspect_index = 0
                
                if hasattr(office_scene, 'selected_interrogation_bg'):
                    bg_path = office_scene.selected_interrogation_bg
                if hasattr(office_scene, 'selected_suspect_index'):
                    suspect_index = office_scene.selected_suspect_index
                    
                # Recreate interrogation scene with custom background and suspect
                self.scenes["interrogation_room"] = InterrogationRoomScene(
                    self.SCREEN_WIDTH,
                    self.SCREEN_HEIGHT,
                    on_interrogation_complete=self.open_accusation_system,
                    background_path=bg_path,
                    suspect_index=suspect_index,
                    on_back=lambda: self.change_scene("office")
                )
                print(f"🎬 Created interrogation room with suspect {suspect_index}, background: {bg_path}")
            
            self.current_scene = self.scenes[scene_id]
            self.player.x = self.SCREEN_WIDTH // 2
            self.player.y = self.SCREEN_HEIGHT // 2
            self.player.rect.x = self.player.x
            self.player.rect.y = self.player.y

            if hasattr(self.current_scene, 'set_player'):
                self.current_scene.set_player(self.player)
                
            print(f"Switched to scene: {scene_id}")
        else:
            print(f"Scene {scene_id} not found!")

    def reset_game(self):
        from src.tools.Notebook_clues import reset_clues
        self.player.x = self.SCREEN_WIDTH // 2
        self.player.y = self.SCREEN_HEIGHT // 2
        self.change_scene("office")
        reset_clues()
        self.state = GameState.PLAYING
        print("✅ Game has been reset!")
    
    def run(self):
        while self.running:
            for event in pygame.event.get():
                self.handle_events_single(event)
            self.update()
            self.draw()
            self.clock.tick(60)
        pygame.quit()
        sys.exit()
    
    def handle_events_single(self, event):
        """Hàm xử lý sự kiện đơn lẻ"""
        mouse_pos = pygame.mouse.get_pos()
        keys = pygame.key.get_pressed()
        
        if event.type == pygame.QUIT:
            self.running = False

        # --- 1. XỬ LÝ HỘI THOẠI (Ưu tiên cao nhất) ---
        if self.state == GameState.DIALOGUE:
            if hasattr(self, 'dialogue_ui'):
                # Xử lý input chuột
                if event.type == pygame.MOUSEMOTION:
                     self.dialogue_ui.handle_mouse_move(mouse_pos)
                
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    # Nếu đang chọn đáp án
                    if self.dialogue_ui.is_choice_mode:
                        if not self.dialogue_ui.handle_mouse_click_choice(mouse_pos):
                             # Nếu click ra ngoài thì skip text
                             self.dialogue_ui.handle_input() 
                    else:
                        # Nếu đang thoại thường -> next text
                        self.dialogue_ui.handle_input() 
                
                # Xử lý input phím
                elif event.type == pygame.KEYDOWN:
                    if self.dialogue_ui.is_choice_mode:
                        self.dialogue_ui.handle_choice_key_input(event.key)
                    else:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                            self.dialogue_ui.handle_input()
                
                # Kiểm tra kết thúc hội thoại
                if not self.dialogue_ui.is_active:
                    self.state = GameState.PLAYING
            return  # Dừng xử lý các event khác

        # --- Global ESC key check ---
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.state == GameState.NOTEBOOK:
                self.notebook.close_notebook()
                self.state = GameState.PLAYING
            elif self.state == GameState.INVENTORY:
                self.inventory_ui._inventory_set_state("CLOSED")
                self.state = GameState.PLAYING
        
        # --- Global Toggles ---
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e: 
                if self.state == GameState.NOTEBOOK:
                    self.notebook.close_notebook()
                    self.state = GameState.PLAYING
                elif self.state == GameState.PLAYING:
                    if self.inventory_ui._inventory_get_state():
                        self.inventory_ui._inventory_set_state("CLOSED")
                    self.notebook.open_notebook()
                    self.state = GameState.NOTEBOOK
                    
            elif event.key == pygame.K_r: 
                if self.state == GameState.INVENTORY:
                    self.inventory_ui._inventory_set_state("CLOSED")
                    self.state = GameState.PLAYING
                elif self.state == GameState.PLAYING:
                    if self.notebook.get_state():
                        self.notebook.close_notebook()
                    self.inventory_ui._inventory_set_state("OPEN")
                    self.state = GameState.INVENTORY
                    
            # --- Quick Scene Switching (Debug) ---
            if self.state == GameState.PLAYING:
                if event.key == pygame.K_1: self.change_scene("office")
                elif event.key == pygame.K_2: self.change_scene("interrogation_room")
                elif event.key == pygame.K_3: self.change_scene("pride_case")
                elif event.key == pygame.K_4: self.change_scene("lust_case")
                elif event.key == pygame.K_5: self.change_scene("gluttony_case")
                elif event.key == pygame.K_6: self.change_scene("greed_case")
                elif event.key == pygame.K_7: self.change_scene("envy_case")
                elif event.key == pygame.K_8: self.change_scene("wrath_case")
                elif event.key == pygame.K_9: self.change_scene("sloth_case")
                elif event.key == pygame.K_F5: self.reset_game()

        # --- State-specific handling ---
        if self.state == GameState.NOTEBOOK:
            self.notebook.handle_event(event, mouse_pos)
            if not self.notebook.get_state():
                self.state = GameState.PLAYING

        elif self.state == GameState.INVENTORY:
            if event.type == pygame.KEYDOWN:
                self.inventory_ui._handle_keys_inventory(event.key, mouse_pos)
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                self.inventory_ui._handle_keys_inventory("LMB_CLICK", mouse_pos)
                if not self.inventory_ui._inventory_get_state():
                    self.state = GameState.PLAYING

        elif self.state == GameState.ACCUSATION:
            if hasattr(self, 'accusation_system'):
                self.accusation_system.handle_input(event)

        elif self.state == GameState.PLAYING:
            popup_visible = False
            if hasattr(self.current_scene, 'suspect_popup'):
                popup_visible = self.current_scene.suspect_popup.visible
            
            if not popup_visible:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if self.closed_book_icon_rect.collidepoint(mouse_pos):
                        self.notebook.open_notebook()
                        self.state = GameState.NOTEBOOK

                    self.inventory_ui._handle_keys_inventory("LMB_CLICK", mouse_pos)
                    if self.inventory_ui._inventory_get_state():
                        self.state = GameState.INVENTORY

                self.ui.handle_event(event)
            
            if hasattr(self.current_scene, 'handle_event'):
                self.current_scene.handle_event(event)

        # --- Continuous Input (Movement) ---
        if self.state == GameState.PLAYING:
            popup_visible = False
            if hasattr(self.current_scene, 'suspect_popup'):
                popup_visible = self.current_scene.suspect_popup.visible
            
            if not popup_visible:
                self.player.handle_input(keys)

    def update(self):
        if self.state == GameState.ACCUSATION:
            if hasattr(self, 'accusation_system'):
                self.accusation_system.update()

        elif self.state == GameState.DIALOGUE:
            # Update hội thoại
            if hasattr(self, 'dialogue_ui'):
                self.dialogue_ui.update()

        elif self.state == GameState.PLAYING:
            old_x = self.player.x
            old_y = self.player.y
            
            dt = self.clock.get_time() / 1000.0
            if hasattr(self.current_scene, 'update'):
                import inspect
                sig = inspect.signature(self.current_scene.update)
                if len(sig.parameters) > 0:
                    self.current_scene.update(dt)
                else:
                    self.current_scene.update()
            
            self.player.update()
            
            if hasattr(self.current_scene, 'check_collision'):
                if self.current_scene.check_collision(self.player.rect):
                    if hasattr(self.current_scene, 'prevent_collision'):
                        new_x, new_y = self.current_scene.prevent_collision(
                            self.player.rect, old_x, old_y
                        )
                        self.player.x = new_x
                        self.player.y = new_y
                        self.player.rect.x = new_x
                        self.player.rect.y = new_y
                    else:
                        self.player.x = old_x
                        self.player.y = old_y
                        self.player.rect.x = old_x
                        self.player.rect.y = old_y
            
            self.ui.update()
        elif self.state == GameState.NOTEBOOK:
            self.notebook.update()
        elif self.state == GameState.INVENTORY:
            pass 

    def draw(self):
        self.screen.fill((0, 0, 0))
        mouse_pos = pygame.mouse.get_pos()

        if self.state == GameState.ACCUSATION:
            if hasattr(self, 'accusation_system'):
                self.accusation_system.draw()
            return  
        
        # Draw Scene (Vẽ nền ngay cả khi đang hội thoại)
        if self.state == GameState.PLAYING or self.state == GameState.DIALOGUE:
            from src.scenes.interrogation_room import InterrogationRoomScene
            is_interrogation = isinstance(self.current_scene, InterrogationRoomScene)
            
            if is_interrogation:
                self.current_scene.draw(self.screen)
            else:
                if hasattr(self.current_scene, 'draw_with_player'):
                    self.current_scene.draw_with_player(self.screen, self.player)
                else:
                    self.current_scene.draw(self.screen)
                    self.player.draw(self.screen)
        else:
            self.current_scene.draw(self.screen)

        # Draw UI
        from src.scenes.interrogation_room import InterrogationRoomScene
        is_interrogation = isinstance(self.current_scene, InterrogationRoomScene)
        
        if not is_interrogation:
            self.ui.draw(self.screen)
            if not self.notebook.get_state():
                 self.screen.blit(self.closed_book_icon, self.closed_book_icon_rect)
                 if self.closed_book_icon_rect.collidepoint(mouse_pos):
                     pygame.draw.rect(self.screen, (255, 255, 255), self.closed_book_icon_rect, 2)
            if self.state != GameState.INVENTORY:
                self.inventory_ui.draw_inventory_icon(mouse_pos)

        # Draw Overlay States
        if self.state == GameState.NOTEBOOK:
            self.notebook.draw(mouse_pos)
        
        if self.state == GameState.INVENTORY:
            self.inventory_ui.draw_inventory(mouse_pos)

        # VẼ HỘI THOẠI TRÊN CÙNG
        if self.state == GameState.DIALOGUE:
            if hasattr(self, 'dialogue_ui'):
                self.dialogue_ui.draw()

        pygame.display.flip()