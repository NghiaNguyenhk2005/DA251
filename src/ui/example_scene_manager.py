"""
Example: Cách tích hợp Map System với Scene Manager

File này demo cách sử dụng map system với một scene manager đơn giản
"""

import pygame
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


class Scene:
    """Base class cho tất cả các scene"""
    def __init__(self, name: str):
        self.name = name
    
    def handle_event(self, event):
        pass
    
    def update(self):
        pass
    
    def draw(self, screen: pygame.Surface):
        pass


class MainScene(Scene):
    """Scene chính với bản đồ"""
    def __init__(self, screen_width: int, screen_height: int, scene_manager):
        super().__init__("MainScene")
        self.scene_manager = scene_manager
        
        # Import ở đây để tránh import khi chưa cần
        from src.ui.main_scene import MainSceneUi
        
        # Khởi tạo UI với callback
        self.ui = MainSceneUi(
            screen_width=screen_width,
            screen_height=screen_height,
            on_building_click=self.on_building_click
        )
    
    def on_building_click(self, building_id: str):
        """Xử lý khi click vào tòa nhà trên bản đồ"""
        print(f"[MainScene] Chuyển đến: {building_id}")
        
        # Chuyển scene dựa trên building_id
        if building_id == "office":
            self.scene_manager.change_scene("office")
        elif building_id == "toa_thi_chinh":
            self.scene_manager.change_scene("toa_thi_chinh")
    
    def handle_event(self, event):
        self.ui.handle_event(event)
    
    def update(self):
        self.ui.update()
    
    def draw(self, screen: pygame.Surface):
        # Vẽ background
        screen.fill((200, 220, 240))
        
        # Vẽ title
        font = pygame.font.Font(None, 48)
        title = font.render("Main Scene - Click Map button", True, (50, 50, 50))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 30))
        
        # Vẽ UI
        self.ui.draw(screen)


class OfficeScene(Scene):
    """Scene của Office Building"""
    def __init__(self, screen_width: int, screen_height: int, scene_manager):
        super().__init__("OfficeScene")
        self.scene_manager = scene_manager
        self.screen_width = screen_width
        self.screen_height = screen_height
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                # Quay lại main scene
                self.scene_manager.change_scene("main")
    
    def draw(self, screen: pygame.Surface):
        # Background
        screen.fill((50, 100, 150))
        
        # Title
        font_large = pygame.font.Font(None, 72)
        font_small = pygame.font.Font(None, 36)
        
        title = font_large.render("🏢 OFFICE BUILDING", True, (255, 255, 255))
        instruction = font_small.render("Press BACKSPACE to return", True, (200, 200, 200))
        
        screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 
                           self.screen_height // 2 - 50))
        screen.blit(instruction, (self.screen_width // 2 - instruction.get_width() // 2, 
                                 self.screen_height // 2 + 50))
        
        # TODO: Vẽ nội dung scene office
        placeholder = font_small.render("TODO: Implement office scene content", True, (150, 150, 150))
        screen.blit(placeholder, (self.screen_width // 2 - placeholder.get_width() // 2, 
                                 self.screen_height // 2 + 150))


class ToaThiChinhScene(Scene):
    """Scene của Tòa Thi Chính"""
    def __init__(self, screen_width: int, screen_height: int, scene_manager):
        super().__init__("ToaThiChinhScene")
        self.scene_manager = scene_manager
        self.screen_width = screen_width
        self.screen_height = screen_height
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                # Quay lại main scene
                self.scene_manager.change_scene("main")
    
    def draw(self, screen: pygame.Surface):
        # Background
        screen.fill((100, 50, 150))
        
        # Title
        font_large = pygame.font.Font(None, 72)
        font_small = pygame.font.Font(None, 36)
        
        title = font_large.render("🏛️ TÒA THI CHÍNH", True, (255, 255, 255))
        instruction = font_small.render("Press BACKSPACE to return", True, (200, 200, 200))
        
        screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 
                           self.screen_height // 2 - 50))
        screen.blit(instruction, (self.screen_width // 2 - instruction.get_width() // 2, 
                                 self.screen_height // 2 + 50))
        
        # TODO: Vẽ nội dung scene tòa thi chính
        placeholder = font_small.render("TODO: Implement tòa thi chính scene content", True, (150, 150, 150))
        screen.blit(placeholder, (self.screen_width // 2 - placeholder.get_width() // 2, 
                                 self.screen_height // 2 + 150))


class SceneManager:
    """Quản lý chuyển đổi giữa các scene"""
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.scenes = {}
        self.current_scene = None
        
        # Đăng ký các scene
        self._register_scenes()
    
    def _register_scenes(self):
        """Đăng ký tất cả các scene"""
        self.scenes["main"] = MainScene(self.screen_width, self.screen_height, self)
        self.scenes["office"] = OfficeScene(self.screen_width, self.screen_height, self)
        self.scenes["toa_thi_chinh"] = ToaThiChinhScene(self.screen_width, self.screen_height, self)
        
        # Set scene mặc định
        self.current_scene = self.scenes["main"]
        print(f"[SceneManager] Khởi tạo với scene: {self.current_scene.name}")
    
    def change_scene(self, scene_name: str):
        """Chuyển sang scene khác"""
        if scene_name in self.scenes:
            old_scene = self.current_scene.name if self.current_scene else "None"
            self.current_scene = self.scenes[scene_name]
            print(f"[SceneManager] Chuyển scene: {old_scene} -> {self.current_scene.name}")
        else:
            print(f"[SceneManager] Warning: Scene '{scene_name}' không tồn tại!")
    
    def handle_event(self, event):
        if self.current_scene:
            self.current_scene.handle_event(event)
    
    def update(self):
        if self.current_scene:
            self.current_scene.update()
    
    def draw(self, screen: pygame.Surface):
        if self.current_scene:
            self.current_scene.draw(screen)


def main():
    """Main game loop với scene manager"""
    pygame.init()
    
    # Thiết lập màn hình
    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 768
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Map System + Scene Manager Demo")
    
    clock = pygame.time.Clock()
    
    # Khởi tạo scene manager
    scene_manager = SceneManager(SCREEN_WIDTH, SCREEN_HEIGHT)
    
    # In hướng dẫn
    print("\n" + "="*70)
    print("🎮 MAP SYSTEM + SCENE MANAGER DEMO")
    print("="*70)
    print("📋 HƯỚNG DẪN:")
    print("  1. Click nút MAP để mở bản đồ")
    print("  2. Click vào tòa nhà để chuyển scene")
    print("  3. Nhấn BACKSPACE để quay lại main scene")
    print("  4. Nhấn ESC để thoát")
    print("="*70 + "\n")
    
    # Game loop
    running = True
    while running:
        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            
            scene_manager.handle_event(event)
        
        # Update
        scene_manager.update()
        
        # Draw
        screen.fill((0, 0, 0))
        scene_manager.draw(screen)
        
        # FPS counter
        fps = int(clock.get_fps())
        font = pygame.font.Font(None, 24)
        fps_text = font.render(f"FPS: {fps}", True, (100, 255, 100))
        screen.blit(fps_text, (10, SCREEN_HEIGHT - 30))
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    print("\n👋 Thoát game\n")


if __name__ == "__main__":
    main()
