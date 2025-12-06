"""
Office Scene
============
Văn phòng chính - scene top-down với hệ thống va chạm.
Người chơi có thể di chuyển tự do nhưng không thể đi xuyên qua các vật cản.

Collision System:
- Sử dụng AABB (Axis-Aligned Bounding Box) collision detection
- Các vùng va chạm được định nghĩa hardcoded dựa trên bố cục background
- Obstacles bao gồm: tường, bàn làm việc, ghế, tủ hồ sơ, v.v.
"""

import pygame
from typing import List, Optional
from .i_scene import IScene


class OfficeScene(IScene):
    """
    Office scene với top-down movement và collision detection
    
    Features:
    - Background rendering từ assets
    - Collision detection với obstacles (AABB)
    - Integration với Player entity từ game.py
    """
    
    def __init__(self, screen_width: int = 1280, screen_height: int = 720) -> None:
        """
        Khởi tạo Office Scene
        
        Args:
            screen_width: Chiều rộng màn hình (default: 1280)
            screen_height: Chiều cao màn hình (default: 720)
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Khởi tạo obstacles list TRƯỚC để furniture có thể dùng
        self.obstacles: List[pygame.Rect] = []
        
        # Load background và furniture
        self._load_background()
        
        # Setup collision obstacles (bao gồm cả furniture)
        self._setup_obstacles()
        
        # Player reference (sẽ được set từ game.py)
        self.player: Optional[object] = None
        
        # Debug mode để hiển thị collision boxes
        self.debug_mode: bool = False
    
    def _load_background(self) -> None:
        """
        Load background image và các decorative objects (ghế, đồ đạc)
        """
        # Load background chính
        bg_paths = [
            "assets/images/scenes/office-bg.jpg",
            "assets/images/scenes/office.png",
            "src/assets/images/scenes/office-bg.jpg"
        ]
        
        self.background = None
        for bg_path in bg_paths:
            try:
                self.background = pygame.image.load(bg_path).convert()
                self.background = pygame.transform.scale(
                    self.background,
                    (self.screen_width, self.screen_height)
                )
                print(f"✅ Loaded office background: {bg_path}")
                break
            except (pygame.error, FileNotFoundError):
                continue
        
        # Fallback: tạo background placeholder nếu không load được
        if self.background is None:
            print("⚠️  Could not load office background. Using placeholder.")
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((40, 40, 50))  # Dark gray office floor
            
            # Vẽ grid pattern để giống sàn văn phòng
            grid_color = (50, 50, 60)
            for x in range(0, self.screen_width, 64):
                pygame.draw.line(self.background, grid_color, (x, 0), (x, self.screen_height))
            for y in range(0, self.screen_height, 64):
                pygame.draw.line(self.background, grid_color, (0, y), (self.screen_width, y))
        
        # Load các ảnh ghế và đồ đạc
        self._load_furniture()
    
    def _load_furniture(self) -> None:
        """
        Load các ảnh ghế và đồ đạc trong văn phòng
        Mỗi item là dict chứa: image, position (x, y), scale
        """
        self.furniture_items: List[dict] = []
        
        # Danh sách các ảnh ghế cần load
        chair_files = [
            "assets/images/scenes/office-chair1.png",
            "assets/images/scenes/office-chair2.png",
            "assets/images/scenes/office-chair3.png"
        ]
        
        # Vị trí đặt các ghế (x, y, scale)
        # Bạn có thể điều chỉnh tọa độ này cho phù hợp với background
        # Hướng dẫn: Tăng x = SANG PHẢI, Tăng y = XUỐNG DƯỚI
        chair_positions = [
            (50, 160, 1.3),   # Chair 1 - Góc trên trái
            (220, 130, 1.3),  # Chair 2 - Góc trên phải
            (self.screen_width // 2 - 300, 180, 1.3),  # Chair 3 - Giữa trên
        ]
        
        # Load và setup từng ghế
        for i, chair_path in enumerate(chair_files):
            if i >= len(chair_positions):
                break
                
            try:
                # Load ảnh ghế với alpha channel (trong suốt)
                chair_img = pygame.image.load(chair_path).convert_alpha()
                
                # Lấy vị trí và scale
                x, y, scale = chair_positions[i]
                
                # Scale ảnh ghế
                original_size = chair_img.get_size()
                new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
                chair_img_scaled = pygame.transform.scale(chair_img, new_size)
                
                # Tạo collision box cho ghế
                # Sử dụng toàn bộ kích thước ảnh để đảm bảo collision chính xác
                collision_rect = pygame.Rect(x, y, new_size[0], new_size[1])
                
                # Thêm vào list furniture
                self.furniture_items.append({
                    'image': chair_img_scaled,
                    'position': (x, y),
                    'rect': collision_rect,
                    'name': f'chair{i+1}'
                })
                
                # Thêm collision box trực tiếp vào obstacles
                self.obstacles.append(collision_rect)
                
                print(f"✅ Loaded furniture: {chair_path} at ({x}, {y}), size: {new_size}, collision added")
                
            except (pygame.error, FileNotFoundError) as e:
                print(f"⚠️  Could not load {chair_path}: {e}")
                continue
    
    def _setup_obstacles(self) -> None:
        """
        Setup collision obstacles (hardcoded rectangles)
        
        Các vùng va chạm được định nghĩa dựa trên layout văn phòng điển hình:
        - Tường xung quanh (boundaries)
        - Bàn làm việc (desks)
        - Tủ hồ sơ (filing cabinets)
        - Ghế (chairs - optional, có thể bỏ qua)
        - Cửa ra vào (doors - để trống để người chơi đi qua)
        
        Note: Tọa độ này là ví dụ - bạn nên điều chỉnh dựa trên background thực tế
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
        # Desk 1 - Góc trên bên trái
        self.obstacles.append(pygame.Rect(100, 80, 180, 120))
        
        # Desk 2 - Góc trên bên phải
        self.obstacles.append(pygame.Rect(self.screen_width - 280, 80, 180, 120))
        
        # Desk 3 - Trung tâm phía trên
        self.obstacles.append(pygame.Rect(self.screen_width // 2 - 90, 100, 180, 120))
        
        # Desk 4 - Bên trái giữa
        self.obstacles.append(pygame.Rect(100, self.screen_height // 2 - 60, 180, 120))
        
        # Desk 5 - Bên phải giữa
        self.obstacles.append(pygame.Rect(self.screen_width - 280, 
                                         self.screen_height // 2 - 60, 180, 120))
        
        # === Tủ HỒ SƠ (Filing Cabinets) ===
        # Cabinet 1 - Góc dưới trái
        self.obstacles.append(pygame.Rect(80, self.screen_height - 180, 120, 80))
        
        # Cabinet 2 - Góc dưới phải
        self.obstacles.append(pygame.Rect(self.screen_width - 200, 
                                         self.screen_height - 180, 120, 80))
        
        # === BÀN HỘI NGHỊ (Meeting Table) - Giữa phòng ===
        meeting_table_width = 240
        meeting_table_height = 160
        meeting_table_x = (self.screen_width - meeting_table_width) // 2
        meeting_table_y = (self.screen_height - meeting_table_height) // 2 + 50
        
        self.obstacles.append(pygame.Rect(meeting_table_x, meeting_table_y, 
                                         meeting_table_width, meeting_table_height))
        
        # === CÂY CỐI TRANG TRÍ (Decorative Plants) ===
        # Plant 1
        self.obstacles.append(pygame.Rect(60, 250, 40, 40))
        
        # Plant 2
        self.obstacles.append(pygame.Rect(self.screen_width - 100, 250, 40, 40))
        
        print(f"\n✅ Setup {len(self.obstacles)} total collision obstacles in office")
    
    def set_player(self, player: object) -> None:
        """
        Set player reference để có thể kiểm tra collision
        
        Args:
            player: Player object từ game.py
        """
        self.player = player
    
    def check_collision(self, rect: pygame.Rect) -> bool:
        """
        Kiểm tra va chạm giữa một rect với các obstacles
        
        Args:
            rect: pygame.Rect cần kiểm tra (thường là player.rect)
            
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
            tuple (new_x, new_y): Vị trí hợp lệ (không va chạm)
        """
        # Nếu không va chạm, giữ nguyên vị trí hiện tại
        if not self.check_collision(player_rect):
            return player_rect.x, player_rect.y
        
        # Nếu va chạm, thử sliding collision (cho phép trượt dọc tường)
        # Thử chỉ revert X
        test_rect = player_rect.copy()
        test_rect.x = old_x
        if not self.check_collision(test_rect):
            return old_x, player_rect.y
        
        # Thử chỉ revert Y
        test_rect = player_rect.copy()
        test_rect.y = old_y
        if not self.check_collision(test_rect):
            return player_rect.x, old_y
        
        # Nếu cả hai đều không được, revert cả hai
        return old_x, old_y
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """
        Xử lý events cho scene này
        
        Args:
            event: Pygame event
        """
        if event.type == pygame.KEYDOWN:
            # Toggle debug mode với F3
            if event.key == pygame.K_F3:
                self.debug_mode = not self.debug_mode
                print(f"Debug mode: {'ON' if self.debug_mode else 'OFF'}")
            
            # ESC để quay về map (sẽ được xử lý ở game.py)
            if event.key == pygame.K_ESCAPE:
                pass  # Game.py sẽ handle
    
    def update(self) -> None:
        """
        Update scene logic
        
        Note: Collision detection với player được xử lý sau khi player.update()
        trong game.py thông qua method check_collision()
        """
        pass  # Office scene không có logic đặc biệt cần update
    
    def draw(self, screen: pygame.Surface) -> None:
        """
        Render scene lên màn hình với layer system
        
        Args:
            screen: Pygame surface để vẽ
        """
        # Vẽ background
        screen.blit(self.background, (0, 0))
        
        # Layer system không cần vẽ furniture ở đây nữa
        # Furniture sẽ được vẽ trong draw_with_player() để sort theo Y
        
        # Debug mode: vẽ collision boxes
        if self.debug_mode:
            for obstacle in self.obstacles:
                # Vẽ obstacle với màu đỏ trong suốt
                debug_surface = pygame.Surface((obstacle.width, obstacle.height))
                debug_surface.set_alpha(100)  # Semi-transparent
                debug_surface.fill((255, 0, 0))  # Red
                screen.blit(debug_surface, (obstacle.x, obstacle.y))
                
                # Vẽ viền
                pygame.draw.rect(screen, (255, 0, 0), obstacle, 2)
            
            # Vẽ debug text
            font = pygame.font.Font(None, 24)
            debug_text = font.render(f"Obstacles: {len(self.obstacles)} | Press F3 to toggle", 
                                    True, (255, 255, 0))
            screen.blit(debug_text, (10, 10))
    
    def draw_with_player(self, screen: pygame.Surface, player) -> None:
        """
        Vẽ scene với player theo layer system (depth sorting)
        Objects và player được sort theo tọa độ Y - càng xuống thì vẽ sau (đè lên)
        
        Args:
            screen: Pygame surface để vẽ
            player: Player object
        """
        # Vẽ background trước
        screen.blit(self.background, (0, 0))
        
        # Tạo list các objects cần vẽ (furniture + player)
        drawable_objects = []
        
        # Thêm furniture items
        if hasattr(self, 'furniture_items'):
            for item in self.furniture_items:
                # Y position để sort = bottom của object
                y_pos = item['position'][1] + item['rect'].height
                drawable_objects.append({
                    'type': 'furniture',
                    'y': y_pos,
                    'item': item
                })
        
        # Thêm player
        # Y position của player = bottom của player rect
        player_y = player.rect.y + player.rect.height
        drawable_objects.append({
            'type': 'player',
            'y': player_y,
            'item': player
        })
        
        # Sort theo Y coordinate (càng nhỏ vẽ trước, càng lớn vẽ sau)
        drawable_objects.sort(key=lambda obj: obj['y'])
        
        # Vẽ theo thứ tự đã sort
        for obj in drawable_objects:
            if obj['type'] == 'furniture':
                item = obj['item']
                screen.blit(item['image'], item['position'])
            elif obj['type'] == 'player':
                player.draw(screen)
        
        # Debug mode: vẽ collision boxes
        if self.debug_mode:
            for obstacle in self.obstacles:
                debug_surface = pygame.Surface((obstacle.width, obstacle.height))
                debug_surface.set_alpha(100)
                debug_surface.fill((255, 0, 0))
                screen.blit(debug_surface, (obstacle.x, obstacle.y))
                pygame.draw.rect(screen, (255, 0, 0), obstacle, 2)
            
            # Vẽ Y-line references
            for obj in drawable_objects:
                y = obj['y']
                pygame.draw.line(screen, (0, 255, 0), (0, y), (50, y), 2)
            
            font = pygame.font.Font(None, 24)
            debug_text = font.render(f"Obstacles: {len(self.obstacles)} | Press F3 to toggle | Layer Sort: ON", 
                                    True, (255, 255, 0))
            screen.blit(debug_text, (10, 10))
