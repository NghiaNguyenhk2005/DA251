"""
Wrath Case Scene
================
Scene điều tra vụ án thịnh nộ - scene top-down với hệ thống va chạm.
Người chơi có thể di chuyển tự do để khám phá hiện trường vụ án.

Collision System:
- Sử dụng AABB (Axis-Aligned Bounding Box) collision detection
- Các vùng va chạm được định nghĩa dựa trên bố cục hiện trường
- Obstacles bao gồm: tường, đồ vật, khu vực bị phá hoại
"""

import pygame
from typing import List, Optional
from .i_scene import IScene


class WrathCaseScene(IScene):
    """
    Wrath Case scene với top-down movement và collision detection
    
    Features:
    - Background rendering từ assets (wrath-bg.png, wrath-woodpad.png, wrath-npc.png)
    - Collision detection với obstacles (AABB)
    - Integration với Player entity từ game.py
    - Khu vực điều tra vụ án thịnh nộ
    """
    
    def __init__(self, screen_width: int = 1280, screen_height: int = 720) -> None:
        """
        Khởi tạo Wrath Case Scene
        
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
        Load background image và các layer cho scene wrath case
        Composite: background -> woodpad -> NPC
        """
        # Tạo surface tổng hợp
        self.background = pygame.Surface((self.screen_width, self.screen_height))
        
        # Load background chính
        bg_loaded = False
        try:
            bg_img = pygame.image.load("assets/images/scenes/wrath-bg.png").convert()
            bg_img = pygame.transform.scale(bg_img, (self.screen_width, self.screen_height))
            self.background.blit(bg_img, (0, 0))
            bg_loaded = True
            print("✅ Loaded wrath-bg.png")
        except (pygame.error, FileNotFoundError) as e:
            print(f"⚠️  Could not load wrath-bg.png: {e}")
        
        # Load woodpad layer (scale nhỏ lại và căn giữa)
        try:
            woodpad_img = pygame.image.load("assets/images/scenes/wrath-woodpad.png").convert_alpha()
            # Scale nhỏ lại 50% kích thước gốc
            original_size = woodpad_img.get_size()
            new_size = (original_size[0] // 2, original_size[1] // 2)
            woodpad_img = pygame.transform.scale(woodpad_img, new_size)
            # Tính toán vị trí để căn giữa
            woodpad_x = (self.screen_width - new_size[0]) // 2 + 150
            woodpad_y = (self.screen_height - new_size[1]) // 2 + 200
            self.background.blit(woodpad_img, (woodpad_x, woodpad_y))
            print(f"✅ Loaded wrath-woodpad.png (scaled to {new_size}, centered at {woodpad_x}, {woodpad_y})")
        except (pygame.error, FileNotFoundError) as e:
            print(f"⚠️  Could not load wrath-woodpad.png: {e}")
        
        # Load NPC layer (scale nhỏ lại và căn giữa)
        try:
            npc_img = pygame.image.load("assets/images/scenes/wrath-npc.png").convert_alpha()
            # Scale nhỏ lại 50% kích thước gốc
            original_size = npc_img.get_size()
            new_size = (original_size[0] , original_size[1])
            npc_img = pygame.transform.scale(npc_img, new_size)
            # Tính toán vị trí để căn giữa
            npc_x = (self.screen_width - new_size[0]) // 2
            npc_y = (self.screen_height - new_size[1]) // 2 + 160
            self.background.blit(npc_img, (npc_x, npc_y))
            print(f"✅ Loaded wrath-npc.png (scaled to {new_size}, centered at {npc_x}, {npc_y})")
        except (pygame.error, FileNotFoundError) as e:
            print(f"⚠️  Could not load wrath-npc.png: {e}")
        
        # Fallback: tạo background placeholder nếu không load được gì
        if not bg_loaded:
            print("⚠️  Using placeholder background for wrath case")
            self.background.fill((40, 20, 20))  # Dark red crime scene
            
            # Vẽ grid pattern
            grid_color = (50, 30, 30)
            for x in range(0, self.screen_width, 64):
                pygame.draw.line(self.background, grid_color, (x, 0), (x, self.screen_height))
            for y in range(0, self.screen_height, 64):
                pygame.draw.line(self.background, grid_color, (0, y), (self.screen_width, y))
            
            # Vẽ text "CRIME SCENE - WRATH CASE"
            try:
                font = pygame.font.Font(None, 48)
                text = font.render("CRIME SCENE - WRATH CASE", True, (200, 100, 100))
                text_rect = text.get_rect(center=(self.screen_width // 2, 50))
                self.background.blit(text, text_rect)
            except:
                pass
    
    def _setup_obstacles(self) -> None:
        """
        Setup collision obstacles cho wrath crime scene
        
        Các vùng va chạm bao gồm:
        - Tường xung quanh
        - Đồ đạc bị phá hủy
        - Khu vực nguy hiểm
        - Vật thể bị đổ ngã
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
        
        # === BÀN LÀM VIỆC BỊ LẬT ĐỔ (Overturned Desks) ===
        # Bàn 1 - Bị lật úp góc trái
        self.obstacles.append(pygame.Rect(150, 100, 220, 130))
        
        # Bàn 2 - Bị lật úp góc phải
        self.obstacles.append(pygame.Rect(self.screen_width - 370, 100, 220, 130))
        
        # Bàn 3 - Bị đổ giữa phòng
        self.obstacles.append(pygame.Rect(self.screen_width // 2 - 100, 
                                         self.screen_height // 2 - 80, 200, 140))
        
        # === TỦ VÀ KỆ BỊ ĐỔ (Fallen Cabinets & Shelves) ===
        # Tủ lật đổ bên trái
        self.obstacles.append(pygame.Rect(80, 300, 140, 100))
        
        # Tủ lật đổ bên phải
        self.obstacles.append(pygame.Rect(self.screen_width - 220, 300, 140, 100))
        
        # Kệ sách đổ - tường trái
        self.obstacles.append(pygame.Rect(60, self.screen_height - 200, 110, 140))
        
        # Kệ sách đổ - tường phải
        self.obstacles.append(pygame.Rect(self.screen_width - 170, 
                                         self.screen_height - 200, 110, 140))
        
        # === GHẾ BỊ ĐỔ VÀ PHÁ VỠ (Broken Chairs) ===
        # Ghế đổ 1
        self.obstacles.append(pygame.Rect(400, 200, 70, 70))
        
        # Ghế đổ 2
        self.obstacles.append(pygame.Rect(self.screen_width - 470, 200, 70, 70))
        
        # Ghế vỡ giữa phòng
        self.obstacles.append(pygame.Rect(self.screen_width // 2 - 200, 
                                         self.screen_height - 250, 65, 65))
        
        # Ghế đổ gần cửa
        self.obstacles.append(pygame.Rect(self.screen_width // 2 + 150, 
                                         self.screen_height - 250, 65, 65))
        
        # === KHU VỰC VỠ VỤN VÀ MẢN VỠ (Debris & Broken Glass) ===
        # Đống đổ nát 1 - góc trên trái
        self.obstacles.append(pygame.Rect(250, 250, 90, 90))
        
        # Đống đổ nát 2 - góc trên phải
        self.obstacles.append(pygame.Rect(self.screen_width - 340, 250, 90, 90))
        
        # Khu vực mảnh vỡ giữa phòng
        self.obstacles.append(pygame.Rect(self.screen_width // 2 + 80, 
                                         self.screen_height // 2, 100, 100))
        
        # Đống vật dụng bị đổ - dưới trái
        self.obstacles.append(pygame.Rect(200, self.screen_height - 180, 120, 90))
        
        # Đống vật dụng bị đổ - dưới phải
        self.obstacles.append(pygame.Rect(self.screen_width - 320, 
                                         self.screen_height - 180, 120, 90))
        
        # === CỬA SỔ VÀ TƯỜNG BỊ HỎNG (Damaged Windows & Walls) ===
        # Mảnh vỡ cửa sổ trái
        self.obstacles.append(pygame.Rect(100, self.screen_height // 2 - 50, 80, 100))
        
        # Mảnh vỡ cửa sổ phải
        self.obstacles.append(pygame.Rect(self.screen_width - 180, 
                                         self.screen_height // 2 - 50, 80, 100))
        
        # === VẬT THỂ NGUY HIỂM (Dangerous Objects) ===
        # Đồ vật sắc nhọn 1
        self.obstacles.append(pygame.Rect(self.screen_width // 2 - 250, 
                                         self.screen_height // 2 + 120, 60, 60))
        
        # Đồ vật sắc nhọn 2
        self.obstacles.append(pygame.Rect(self.screen_width // 2 + 190, 
                                         self.screen_height // 2 + 120, 60, 60))
        
        # === ĐỒ TRANG TRÍ BỊ PHÁ (Destroyed Decorations) ===
        # Chậu cây đổ 1
        self.obstacles.append(pygame.Rect(120, 80, 55, 55))
        
        # Chậu cây đổ 2
        self.obstacles.append(pygame.Rect(self.screen_width - 175, 80, 55, 55))
        
        # Khung tranh rơi
        self.obstacles.append(pygame.Rect(450, self.screen_height - 130, 80, 50))
        
        # Đèn bị đổ
        self.obstacles.append(pygame.Rect(self.screen_width - 530, 
                                         self.screen_height - 130, 70, 70))
        
        print(f"\n✅ Setup {len(self.obstacles)} total collision obstacles in wrath case scene")
    
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
