"""
Greed Case Scene
================
Scene điều tra vụ án tham lam - scene top-down với hệ thống va chạm.
Người chơi có thể di chuyển tự do để khám phá hiện trường vụ án.

Collision System:
- Sử dụng AABB (Axis-Aligned Bounding Box) collision detection
- Các vùng va chạm được định nghĩa dựa trên bố cục hiện trường
- Obstacles bao gồm: tường, đồ vật bằng chứng, khu vực bị phong tỏa
"""

import pygame
from typing import List, Optional
from .i_scene import IScene


class GreedCaseScene(IScene):
    """
    Greed Case scene với top-down movement và collision detection
    
    Features:
    - Background rendering từ assets (scene-greed.jpg)
    - Collision detection với obstacles (AABB)
    - Integration với Player entity từ game.py
    - Khu vực điều tra vụ án tham lam
    """
    
    def __init__(self, screen_width: int = 1280, screen_height: int = 720) -> None:
        """
        Khởi tạo Greed Case Scene
        
        Args:
            screen_width: Chiều rộng màn hình (default: 1280)
            screen_height: Chiều cao màn hình (default: 720)
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Khởi tạo obstacles list
        self.obstacles: List[pygame.Rect] = []
        
        # Load background
        self._load_background()
        
        # Setup collision obstacles
        self._setup_obstacles()
        
        # Player reference (sẽ được set từ game.py)
        self.player: Optional[object] = None
        
        # Debug mode để hiển thị collision boxes
        self.debug_mode: bool = False
    
    def _load_background(self) -> None:
        """
        Load background image cho scene greed case
        """
        # Đường dẫn đến background scene-greed
        bg_paths = [
            "assets/images/scenes/scene-greed.jpg",
            "src/assets/images/scenes/scene-greed.jpg"
        ]
        
        self.background = None
        for bg_path in bg_paths:
            try:
                self.background = pygame.image.load(bg_path).convert()
                self.background = pygame.transform.scale(
                    self.background,
                    (self.screen_width, self.screen_height)
                )
                print(f"✅ Loaded greed case background: {bg_path}")
                break
            except (pygame.error, FileNotFoundError):
                continue
        
        # Fallback: tạo background placeholder nếu không load được
        if self.background is None:
            print("⚠️  Could not load greed case background. Using placeholder.")
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((30, 25, 20))  # Dark brown crime scene floor
            
            # Vẽ grid pattern
            grid_color = (40, 35, 30)
            for x in range(0, self.screen_width, 64):
                pygame.draw.line(self.background, grid_color, (x, 0), (x, self.screen_height))
            for y in range(0, self.screen_height, 64):
                pygame.draw.line(self.background, grid_color, (0, y), (self.screen_width, y))
            
            # Vẽ text "CRIME SCENE - GREED CASE"
            try:
                font = pygame.font.Font(None, 48)
                text = font.render("CRIME SCENE - GREED CASE", True, (150, 150, 150))
                text_rect = text.get_rect(center=(self.screen_width // 2, 50))
                self.background.blit(text, text_rect)
            except:
                pass
    
    def _setup_obstacles(self) -> None:
        """
        Setup collision obstacles cho crime scene
        
        Các vùng va chạm bao gồm:
        - Tường xung quanh
        - Bàn làm việc của nạn nhân
        - Két sắt
        - Khu vực bằng chứng
        - Đồ vật hiện trường
        """
        # === TƯỜNG XUNG QUANH (Boundaries) ===
        wall_thickness = 40
        
        # Tường trên
        self.obstacles.append(pygame.Rect(0, 0, self.screen_width, wall_thickness))
        
        # Tường dưới
        self.obstacles.append(pygame.Rect(0, self.screen_height - wall_thickness, 
                                         self.screen_width, wall_thickness))
        
        # Tường trái
        self.obstacles.append(pygame.Rect(0, 0, wall_thickness, self.screen_height))
        
        # Tường phải
        self.obstacles.append(pygame.Rect(self.screen_width - wall_thickness, 0, 
                                         wall_thickness, self.screen_height))
        
        # === BÀN LÀM VIỆC CỦA NẠN NHÂN (Victim's Desk) ===
        # Bàn chính - nơi phát hiện dấu vết quan trọng
        victim_desk_x = self.screen_width // 2 - 120
        victim_desk_y = 150
        self.obstacles.append(pygame.Rect(victim_desk_x, victim_desk_y, 240, 140))
        
        # === KÉT SẮT (Safe) ===
        # Két sắt - mục tiêu của kẻ tham lam
        safe_x = 150
        safe_y = self.screen_height - 220
        self.obstacles.append(pygame.Rect(safe_x, safe_y, 100, 120))
        
        # === TỦ HỒ SƠ (Filing Cabinets) ===
        # Cabinet 1 - Bên trái
        self.obstacles.append(pygame.Rect(80, 200, 120, 90))
        
        # Cabinet 2 - Bên phải
        self.obstacles.append(pygame.Rect(self.screen_width - 200, 200, 120, 90))
        
        # === BÀN PHỤ (Side Tables) ===
        # Table 1 - Góc trên trái
        self.obstacles.append(pygame.Rect(100, 80, 140, 100))
        
        # Table 2 - Góc trên phải
        self.obstacles.append(pygame.Rect(self.screen_width - 240, 80, 140, 100))
        
        # === GHẾ (Chairs) ===
        # Chair 1 - Ghế của nạn nhân (đã bị đổ)
        chair1_x = victim_desk_x + 260
        chair1_y = victim_desk_y + 40
        self.obstacles.append(pygame.Rect(chair1_x, chair1_y, 60, 60))
        
        # Chair 2 - Ghế khách
        self.obstacles.append(pygame.Rect(self.screen_width // 2 - 180, 
                                         self.screen_height // 2 + 100, 60, 60))
        
        # === KHU VỰC BẰNG CHỨNG (Evidence Areas) ===
        # Khu vực vỡ kính
        broken_glass_x = self.screen_width // 2 + 150
        broken_glass_y = self.screen_height // 2 - 50
        self.obstacles.append(pygame.Rect(broken_glass_x, broken_glass_y, 80, 80))
        
        # Khu vực dấu chân
        footprint_x = safe_x + 150
        footprint_y = safe_y + 50
        self.obstacles.append(pygame.Rect(footprint_x, footprint_y, 60, 100))
        
        # === ĐỒ TRANG TRÍ (Decorations) ===
        # Chậu cây 1
        self.obstacles.append(pygame.Rect(60, self.screen_height // 2, 50, 50))
        
        # Chậu cây 2
        self.obstacles.append(pygame.Rect(self.screen_width - 110, 
                                         self.screen_height // 2, 50, 50))
        
        # Tủ sách
        bookshelf_x = self.screen_width - 180
        bookshelf_y = self.screen_height - 200
        self.obstacles.append(pygame.Rect(bookshelf_x, bookshelf_y, 100, 120))
        
        print(f"\n✅ Setup {len(self.obstacles)} total collision obstacles in greed case scene")
    
    def set_player(self, player: object) -> None:
        """
        Set player reference
        
        Args:
            player: Player object từ game.py
        """
        self.player = player
    
    def check_collision(self, rect: pygame.Rect) -> bool:
        """
        Kiểm tra va chạm giữa một rect với các obstacles
        
        Args:
            rect: pygame.Rect cần kiểm tra
            
        Returns:
            True nếu có va chạm, False nếu không
        """
        for obstacle in self.obstacles:
            if rect.colliderect(obstacle):
                return True
        return False
    
    def prevent_collision(self, player_rect: pygame.Rect, 
                         old_x: float, old_y: float) -> tuple:
        """
        Ngăn player đi xuyên qua obstacles bằng cách revert position
        
        Args:
            player_rect: Current player rect
            old_x: Previous x position
            old_y: Previous y position
            
        Returns:
            tuple (new_x, new_y): Vị trí hợp lệ
        """
        if not self.check_collision(player_rect):
            return player_rect.x, player_rect.y
        
        # Sliding collision
        test_rect = player_rect.copy()
        test_rect.x = old_x
        if not self.check_collision(test_rect):
            return old_x, player_rect.y
        
        test_rect = player_rect.copy()
        test_rect.y = old_y
        if not self.check_collision(test_rect):
            return player_rect.x, old_y
        
        return old_x, old_y
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Xử lý events cho scene
        
        Args:
            event: Pygame event
        """
        if event.type == pygame.KEYDOWN:
            # Toggle debug mode với F3
            if event.key == pygame.K_F3:
                self.debug_mode = not self.debug_mode
                print(f"Debug mode: {'ON' if self.debug_mode else 'OFF'}")
            
            # ESC để quay về
            if event.key == pygame.K_ESCAPE:
                pass  # Game.py sẽ handle
    
    def update(self, dt: float) -> None:
        """
        Update scene logic
        
        Args:
            dt: Delta time (seconds)
        """
        pass  # Có thể thêm animation hoặc effects sau
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        Vẽ scene lên screen
        
        Args:
            screen: Pygame display surface
        """
        # Vẽ background
        screen.blit(self.background, (0, 0))
        
        # Vẽ collision boxes nếu debug mode bật
        if self.debug_mode:
            for obstacle in self.obstacles:
                pygame.draw.rect(screen, (255, 0, 0), obstacle, 2)
