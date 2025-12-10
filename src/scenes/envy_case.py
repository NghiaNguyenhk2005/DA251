"""
Envy Case Scene
===============
Scene điều tra vụ án ganh tỵ - scene top-down với hệ thống va chạm.
Người chơi có thể di chuyển tự do để khám phá hiện trường vụ án.

Collision System:
- Sử dụng AABB (Axis-Aligned Bounding Box) collision detection
- Các vùng va chạm được định nghĩa dựa trên bố cục hiện trường
- Obstacles bao gồm: tường, đồ vật, khu vực bị phong tỏa
"""

import pygame
from typing import List, Optional
from .i_scene import IScene


class EnvyCaseScene(IScene):
    """
    Envy Case scene với top-down movement và collision detection
    
    Features:
    - Background rendering từ assets (envy-bg.png)
    - Collision detection với obstacles (AABB)
    - Integration với Player entity từ game.py
    - Khu vực điều tra vụ án ganh tỵ
    """
    
    def __init__(self, screen_width: int = 1280, screen_height: int = 720) -> None:
        """
        Khởi tạo Envy Case Scene
        
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
        Load background image và các layer cho scene envy case
        Composite: background -> mask -> NPC
        """
        # Tạo surface tổng hợp
        self.background = pygame.Surface((self.screen_width, self.screen_height))
        
        # Load background chính
        bg_loaded = False
        try:
            bg_img = pygame.image.load("assets/images/scenes/envy-bg.png").convert()
            bg_img = pygame.transform.scale(bg_img, (self.screen_width, self.screen_height))
            self.background.blit(bg_img, (0, 0))
            bg_loaded = True
            print("✅ Loaded envy-bg.png")
        except (pygame.error, FileNotFoundError) as e:
            print(f"⚠️  Could not load envy-bg.png: {e}")
        
        # Load mask layer (scale nhỏ lại và căn giữa)
        try:
            mask_img = pygame.image.load("assets/images/scenes/envy-mask.png").convert_alpha()
            # Scale nhỏ lại 50% kích thước gốc
            original_size = mask_img.get_size()
            new_size = (original_size[0] // 3, original_size[1] // 3)
            mask_img = pygame.transform.scale(mask_img, new_size)
            # Tính toán vị trí để căn giữa
            mask_x = (self.screen_width - new_size[0]) // 2 + 50
            mask_y = (self.screen_height - new_size[1]) // 2 + 80
            self.background.blit(mask_img, (mask_x, mask_y))
            print(f"✅ Loaded envy-mask.png (scaled to {new_size}, centered at {mask_x}, {mask_y})")
        except (pygame.error, FileNotFoundError) as e:
            print(f"⚠️  Could not load envy-mask.png: {e}")
        
        # Load NPC layer (scale nhỏ lại và căn giữa)
        try:
            npc_img = pygame.image.load("assets/images/scenes/envy-npc.png").convert_alpha()
            # Scale nhỏ lại 50% kích thước gốc
            original_size = npc_img.get_size()
            new_size = (original_size[0] // 2, original_size[1] // 2)
            npc_img = pygame.transform.scale(npc_img, new_size)
            # Tính toán vị trí để căn giữa
            npc_x = (self.screen_width - new_size[0] ) // 2
            npc_y = (self.screen_height - new_size[1]) // 2 + 30
            self.background.blit(npc_img, (npc_x, npc_y))
            print(f"✅ Loaded envy-npc.png (scaled to {new_size}, centered at {npc_x}, {npc_y})")
        except (pygame.error, FileNotFoundError) as e:
            print(f"⚠️  Could not load envy-npc.png: {e}")
        
        # Fallback: tạo background placeholder nếu không load được gì
        if not bg_loaded:
            print("⚠️  Using placeholder background for envy case")
            self.background.fill((25, 35, 25))  # Dark green crime scene
            
            # Vẽ grid pattern
            grid_color = (35, 45, 35)
            for x in range(0, self.screen_width, 64):
                pygame.draw.line(self.background, grid_color, (x, 0), (x, self.screen_height))
            for y in range(0, self.screen_height, 64):
                pygame.draw.line(self.background, grid_color, (0, y), (self.screen_width, y))
            
            # Vẽ text "CRIME SCENE - ENVY CASE"
            try:
                font = pygame.font.Font(None, 48)
                text = font.render("CRIME SCENE - ENVY CASE", True, (150, 200, 150))
                text_rect = text.get_rect(center=(self.screen_width // 2, 50))
                self.background.blit(text, text_rect)
            except:
                pass
    
    def _setup_obstacles(self) -> None:
        """
        Setup collision obstacles cho envy crime scene
        
        Các vùng va chạm bao gồm:
        - Tường xung quanh
        - Đồ đạc trong phòng
        - Khu vực bị phá hoại
        - Các vật thể cản trở
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
        
        # === BÀN LÀM VIỆC (Desks) ===
        # Bàn chính - bàn của nạn nhân
        victim_desk_x = 200
        victim_desk_y = 120
        self.obstacles.append(pygame.Rect(victim_desk_x, victim_desk_y, 200, 120))
        
        # Bàn đối thủ - bàn của nghi phạm
        rival_desk_x = self.screen_width - 400
        rival_desk_y = 120
        self.obstacles.append(pygame.Rect(rival_desk_x, rival_desk_y, 200, 120))
        
        # === TỦ HỒ SƠ VÀ KỆ SÁCH (Cabinets & Shelves) ===
        # Tủ hồ sơ bên trái
        self.obstacles.append(pygame.Rect(80, 300, 120, 100))
        
        # Tủ hồ sơ bên phải
        self.obstacles.append(pygame.Rect(self.screen_width - 200, 300, 120, 100))
        
        # Kệ sách tường trái
        self.obstacles.append(pygame.Rect(60, self.screen_height - 180, 100, 120))
        
        # Kệ sách tường phải
        self.obstacles.append(pygame.Rect(self.screen_width - 160, 
                                         self.screen_height - 180, 100, 120))
        
        # === GHẾ (Chairs) ===
        # Ghế bàn nạn nhân
        self.obstacles.append(pygame.Rect(victim_desk_x + 210, victim_desk_y + 30, 60, 60))
        
        # Ghế bàn đối thủ
        self.obstacles.append(pygame.Rect(rival_desk_x - 70, rival_desk_y + 30, 60, 60))
        
        # Ghế giữa phòng (khu vực nghỉ)
        self.obstacles.append(pygame.Rect(self.screen_width // 2 - 150, 
                                         self.screen_height // 2 + 80, 60, 60))
        self.obstacles.append(pygame.Rect(self.screen_width // 2 + 90, 
                                         self.screen_height // 2 + 80, 60, 60))
        
        # === BÀN TRUNG TÂM (Center Table) ===
        # Bàn họp/bàn trà
        center_table_x = self.screen_width // 2 - 100
        center_table_y = self.screen_height // 2 - 60
        self.obstacles.append(pygame.Rect(center_table_x, center_table_y, 200, 120))
        
        # === KHU VỰC ĐÃ BỊ PHÁ HOẠI (Damaged Areas) ===
        # Đống giấy tờ bị xé - bên trái
        self.obstacles.append(pygame.Rect(250, self.screen_height // 2, 80, 80))
        
        # Tủ bị lật đổ - góc dưới trái
        fallen_cabinet_x = 300
        fallen_cabinet_y = self.screen_height - 200
        self.obstacles.append(pygame.Rect(fallen_cabinet_x, fallen_cabinet_y, 140, 90))
        
        # Khu vực vỡ vụn - giữa phòng phía dưới
        self.obstacles.append(pygame.Rect(self.screen_width // 2 - 50, 
                                         self.screen_height - 180, 100, 100))
        
        # === CÂY VÀ ĐỒ TRANG TRÍ (Plants & Decorations) ===
        # Chậu cây 1 - góc trên trái
        self.obstacles.append(pygame.Rect(100, 80, 50, 50))
        
        # Chậu cây 2 - góc trên phải
        self.obstacles.append(pygame.Rect(self.screen_width - 150, 80, 50, 50))
        
        # Chậu cây 3 - bên tường trái
        self.obstacles.append(pygame.Rect(60, self.screen_height // 2 - 100, 50, 50))
        
        # Chậu cây 4 - bên tường phải
        self.obstacles.append(pygame.Rect(self.screen_width - 110, 
                                         self.screen_height // 2 - 100, 50, 50))
        
        # === ĐỒ VẬT KHÁC (Other Objects) ===
        # Thùng rác bị đổ
        self.obstacles.append(pygame.Rect(self.screen_width - 250, 
                                         self.screen_height - 150, 40, 50))
        
        # Khung ảnh bị rơi
        self.obstacles.append(pygame.Rect(500, self.screen_height - 120, 60, 40))
        
        print(f"\n✅ Setup {len(self.obstacles)} total collision obstacles in envy case scene")
    
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
