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
from typing import List, Optional, Tuple, Dict, Any
from .i_scene import IScene


from src.utils.interaction_area import InteractionArea


class GreedCaseScene(IScene):
    """
    Office scene using a collision mask for walls and rects for other obstacles.
    """
    
    def __init__(self, screen_width: int = 1280, screen_height: int = 720) -> None:
        """
        Initializes the Office Scene.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.obstacles: List[Dict[str, Any]] = []
        self.collision_rects: List[pygame.Rect] = []
        self.interaction_areas: List[InteractionArea] = []
        self.wall_mask: Optional[pygame.mask.Mask] = None
        
        # Coin state
        self.coin_collected: bool = False
        self.coin_data: Optional[Dict[str, Any]] = None
        self.coin_interaction_area: Optional[InteractionArea] = None
        
        # NPCs data
        self.npcs: List[Dict[str, Any]] = []
        self.npc_interaction_areas: List[InteractionArea] = []

        self._load_background()
        self._load_wall_mask() # Load the new wall mask
        self._load_obstacles()
        self._load_npcs()  # Load NPCs
        self._setup_collision_rects()
        self._setup_interaction_areas()
        
        self.player: Optional[object] = None
        self.debug_mode: bool = True

    def _load_background(self) -> None:
        """Loads the background image for the scene."""
        # bg_paths = ["assets/images/scenes/office-bg.jpg", "assets/images/scenes/office.png", "src/assets/images/scenes/office-bg.jpg"]
        bg_paths = ["assets/images/scenes/greed-bg.png"]
        self.background = None
        for bg_path in bg_paths:
            try:
                self.background = pygame.image.load(bg_path).convert()
                self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
                print(f"✅ Loaded greed background: {bg_path}")
                break
            except (pygame.error, FileNotFoundError):
                continue
        
        if self.background is None:
            print("⚠️  Could not load greed background. Using placeholder.")
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((40, 40, 50))

    def _load_wall_mask(self) -> None:
        """Loads the wall collision mask from an image."""
        try:
            path = "assets/images/scenes/greed-walls.png"
            mask_image = pygame.image.load(path).convert()
            mask_image = pygame.transform.scale(mask_image, (self.screen_width, self.screen_height))
            # Set black pixels to be transparent, so the mask is only for the walls.
            mask_image.set_colorkey((0, 0, 0))
            self.wall_mask = pygame.mask.from_surface(mask_image)
            print(f"✅ Loaded wall collision mask from {path}.")
        except (pygame.error, FileNotFoundError) as e:
            print(f"⚠️  Could not load wall collision mask: {e}")
            self.wall_mask = pygame.mask.Mask((self.screen_width, self.screen_height), fill=False)

    def _load_obstacles(self) -> None:
        """Loads the coin (not an obstacle, just a drawable object)."""
        # Load coin - không tạo collision, chỉ hiển thị
        try:
            coin_img = pygame.image.load("assets/images/scenes/greed-coin.png").convert_alpha()
            coin_pos = (600, 250)
            coin_scale = 0.5
            original_size = coin_img.get_size()
            new_size = (int(original_size[0] * coin_scale), int(original_size[1] * coin_scale))
            coin_img_scaled = pygame.transform.scale(coin_img, new_size)
            
            # Tạo rect để biết vị trí (không dùng cho collision)
            coin_rect = pygame.Rect(coin_pos[0], coin_pos[1], new_size[0], new_size[1])
            
            self.coin_data = {
                'image': coin_img_scaled,
                'position': coin_pos,
                'rect': coin_rect,
                'name': 'greed_coin'
            }
            print(f"✅ Loaded coin at {coin_pos} (no collision)")
        except (pygame.error, FileNotFoundError) as e:
            print(f"⚠️  Could not load coin: {e}")
            self.coin_data = None
    
    def _load_npcs(self) -> None:
        """Loads 3 NPCs for interaction (no collision)."""
        npc_definitions = [
            {"name": "NPC_1", "pos": (100, 500), "color": (255, 100, 100)}
        ]
        
        for npc_def in npc_definitions:
            # Tạo NPC placeholder (hình tròn màu)
            npc_size = (60, 80)
            npc_surface = pygame.Surface(npc_size, pygame.SRCALPHA)
            # Vẽ hình người đơn giản
            pygame.draw.ellipse(npc_surface, npc_def["color"], (10, 10, 40, 50))  # Đầu
            pygame.draw.rect(npc_surface, npc_def["color"], (15, 55, 30, 25))  # Thân
            
            npc_rect = pygame.Rect(npc_def["pos"][0], npc_def["pos"][1], npc_size[0], npc_size[1])
            
            self.npcs.append({
                'image': npc_surface,
                'position': npc_def["pos"],
                'rect': npc_rect,
                'name': npc_def["name"],
                'color': npc_def["color"]
            })
        
        print(f"✅ Loaded {len(self.npcs)} NPCs (no collision)")

    def _setup_collision_rects(self) -> None:
        """Creates a list of pygame.Rects for efficient collision checking."""
        self.collision_rects.clear()
        for obj in self.obstacles:
            if 'rect' in obj:
                self.collision_rects.append(obj['rect'])
        # Coin KHÔNG được thêm vào collision rects
        print(f"✅ Built {len(self.collision_rects)} collision rects (coin excluded)")

    def _setup_interaction_areas(self) -> None:
        """Creates all interaction areas for this scene."""
        # Tạo interaction area cho coin
        if self.coin_data:
            # Mở rộng vùng tương tác 80 pixel xung quanh coin
            interaction_rect = self.coin_data['rect'].inflate(80, 80)
            self.coin_interaction_area = InteractionArea(rect=interaction_rect, callback=self._on_coin_pickup)
            self.interaction_areas.append(self.coin_interaction_area)
            print(f"✅ Created interaction area around coin at {self.coin_data['position']}")
        
        # Tạo interaction areas cho từng NPC
        for npc in self.npcs:
            interaction_rect = npc['rect'].inflate(100, 100)
            # Tạo callback riêng cho từng NPC
            callback = lambda npc_name=npc['name']: self._on_npc_interact(npc_name)
            npc_area = InteractionArea(rect=interaction_rect, callback=callback)
            self.npc_interaction_areas.append(npc_area)
            self.interaction_areas.append(npc_area)
            print(f"✅ Created interaction area for {npc['name']} at {npc['position']}")

    def _on_coin_pickup(self) -> None:
        """Callback giả khi người chơi nhặt coin."""
        if not self.coin_collected:
            self.coin_collected = True
            print("💰 Đã nhặt được đồng xu tham lam! (Coin collected)")
            
            # Xóa chính xác interaction area của coin (không ảnh hưởng các area khác)
            if self.coin_interaction_area in self.interaction_areas:
                self.interaction_areas.remove(self.coin_interaction_area)
                print("✅ Coin interaction area removed (other areas unaffected)")
    
    def _on_npc_interact(self, npc_name: str) -> None:
        """Callback giả khi người chơi tương tác với NPC."""
        print(f"💬 Đang nói chuyện với {npc_name}...")
        
        if npc_name == "NPC_1":
            print("Not done NPC_1")
            # to do, them call back
            
            # print("📝 TODO: Thêm coin vào inventory")
            # print("📝 TODO: Phát âm thanh nhặt vật phẩm")
            # print("📝 TODO: Hiệu ứng particle khi nhặt")
            # Sau này bạn sẽ thêm logic thực tế ở đây:
            # - Add coin to inventory
            # - Play sound effect
            # - Show particle effect
            # - Update quest/clue system

    def set_player(self, player: object) -> None:
        """Sets the player reference and positions them for this scene."""
        self.player = player
        if self.player:
            start_x, start_y = (900, 400)
            self.player.x, self.player.y = start_x, start_y
            self.player.rect.topleft = (start_x, start_y)
            print(f"✅ Player position set to ({start_x}, {start_y}) for OfficeScene.")

    def check_collision(self, rect: pygame.Rect) -> bool:
        """Checks if a rect collides with obstacle rects OR the wall mask."""
        # 1. Check against furniture rects
        for obstacle_rect in self.collision_rects:
            if rect.colliderect(obstacle_rect):
                return True
        
        # 2. Check against the wall mask
        if self.wall_mask:
            player_mask = pygame.mask.Mask(rect.size, fill=True)
            offset = (rect.x, rect.y)
            if self.wall_mask.overlap(player_mask, offset):
                return True

        return False
    
    def prevent_collision(self, player_rect: pygame.Rect, old_x: float, old_y: float) -> tuple:
        """Prevents the player from moving through obstacles using sliding collision."""
        if not self.check_collision(player_rect):
            return player_rect.x, player_rect.y
        
        test_rect = player_rect.copy()
        test_rect.x = int(old_x)
        if not self.check_collision(test_rect):
            return old_x, player_rect.y
        
        test_rect = player_rect.copy()
        test_rect.y = int(old_y)
        if not self.check_collision(test_rect):
            return player_rect.x, old_y
        
        return old_x, old_y
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handles scene-specific events."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                self.debug_mode = not self.debug_mode
                print(f"Debug mode: {'ON' if self.debug_mode else 'OFF'}")
        
        for area in self.interaction_areas:
            area.handle_event(event)
    
    def update(self) -> None:
        """Updates scene logic."""
        if self.player:
            for area in self.interaction_areas:
                area.update(self.player.rect)
    
    def draw(self, screen: pygame.Surface) -> None:
        """Renders the background and debug info."""
        screen.blit(self.background, (0, 0))
        if self.debug_mode:
            # Draw obstacle rects in RED
            for rect in self.collision_rects:
                debug_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
                debug_surface.fill((255, 0, 0, 100))
                screen.blit(debug_surface, rect.topleft)
                pygame.draw.rect(screen, (255, 0, 0), rect, 2)
            
            # Draw wall mask outline in BLUE
            if self.wall_mask:
                outline = self.wall_mask.outline()
                if outline:
                    pygame.draw.lines(screen, (0, 0, 255), True, outline, 2)

            # Draw interaction area rects in CYAN
            for area in self.interaction_areas:
                area.draw_debug(screen)

            font = pygame.font.Font(None, 24)
            debug_text = font.render(f"Rect Obstacles: {len(self.collision_rects)} | F3 to toggle", True, (255, 255, 0))
            screen.blit(debug_text, (10, 10))
    
    def draw_with_player(self, screen: pygame.Surface, player) -> None:
        """Draws the scene with the player, using Y-sorting for layering."""
        screen.blit(self.background, (0, 0))
        
        drawable_objects = []
        
        # Thêm obstacles (nếu có)
        for item in self.obstacles:
            if 'image' in item and 'position' in item:
                y_pos = item['position'][1] + item['rect'].height
                drawable_objects.append({'type': 'object', 'y': y_pos, 'item': item})
        
        # Thêm coin (nếu chưa nhặt)
        if self.coin_data and not self.coin_collected:
            coin_y = self.coin_data['position'][1] + self.coin_data['rect'].height
            drawable_objects.append({'type': 'coin', 'y': coin_y, 'item': self.coin_data})
        
        # Thêm NPCs
        for npc in self.npcs:
            npc_y = npc['position'][1] + npc['rect'].height
            drawable_objects.append({'type': 'npc', 'y': npc_y, 'item': npc})
        
        # Thêm player
        player_y = player.rect.y + player.rect.height
        drawable_objects.append({'type': 'player', 'y': player_y, 'item': player})
        
        # Sắp xếp theo Y để tạo hiệu ứng depth
        drawable_objects.sort(key=lambda obj: obj['y'])
        
        # Vẽ theo thứ tự
        for obj in drawable_objects:
            if obj['type'] == 'object':
                screen.blit(obj['item']['image'], obj['item']['position'])
            elif obj['type'] == 'coin':
                screen.blit(obj['item']['image'], obj['item']['position'])
            elif obj['type'] == 'npc':
                screen.blit(obj['item']['image'], obj['item']['position'])
            elif obj['type'] == 'player':
                player.draw(screen)

        for area in self.interaction_areas:
            area.draw(screen, player.rect)
        
        if self.debug_mode:
            # Draw RED rects for furniture obstacles
            for rect in self.collision_rects:
                debug_surface = pygame.Surface(rect.size, pygame.SRCALPHA)
                debug_surface.fill((255, 0, 0, 100))
                screen.blit(debug_surface, rect.topleft)
                pygame.draw.rect(screen, (255, 0, 0), rect, 2)
            
            # Draw BLUE outline for wall mask
            if self.wall_mask:
                outline = self.wall_mask.outline()
                if outline:
                    pygame.draw.lines(screen, (0, 0, 255), True, outline, 2)

            # Draw CYAN rects for interaction areas
            for area in self.interaction_areas:
                area.draw_debug(screen)
            for i in self.npc_interaction_areas :
                i.draw_debug(screen)

            font = pygame.font.Font(None, 24)
            text = f"Masks: ON | Rects: {len(self.collision_rects)} | Interact: {len(self.interaction_areas)} | F3"
            debug_text = font.render(text, True, (255, 255, 0))
            screen.blit(debug_text, (10, 10))
