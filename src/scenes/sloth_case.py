"""\nSloth Case Scene\n===============\nScene điều tra vụ án lười biếng - scene top-down với hệ thống va chạm.\nNgười chơi có thể di chuyển tự do để khám phá hiện trường vụ án.\n\nCollision System:\n- Sử dụng AABB (Axis-Aligned Bounding Box) collision detection\n- Các vùng va chạm được định nghĩa dựa trên bố cục hiện trường\n- Obstacles bao gồm: tường, đồ vật bằng chứng, khu vực bị phong tỏa\n"""

import pygame
from typing import List, Optional, Tuple, Dict, Any
from .i_scene import IScene


from src.utils.interaction_area import InteractionArea


class SlothCaseScene(IScene):
    """
    Sloth Case scene using a collision mask for walls and rects for other obstacles.
    """
    
    def __init__(self, screen_width: int = 1280, screen_height: int = 720) -> None:
        """
        Initializes the Sloth Case Scene.
        """
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.obstacles: List[Dict[str, Any]] = []
        self.collision_rects: List[pygame.Rect] = []
        self.interaction_areas: List[InteractionArea] = []
        self.wall_mask: Optional[pygame.mask.Mask] = None
        
        # Clock state (vật thể có thể nhặt)
        self.clock_collected: bool = False
        self.clock_data: Optional[Dict[str, Any]] = None
        self.clock_interaction_area: Optional[InteractionArea] = None
        
        # NPCs data
        self.npcs: List[Dict[str, Any]] = []
        self.npc_interaction_areas: List[InteractionArea] = []

        self._load_background()
        self._load_wall_mask()
        self._load_obstacles()
        self._load_npcs()
        self._setup_collision_rects()
        self._setup_interaction_areas()
        
        self.player: Optional[object] = None
        self.debug_mode: bool = False

    def _load_background(self) -> None:
        """Loads the background image for the scene."""
        bg_paths = ["assets/images/scenes/sloth-bg.jpg", "assets/images/scenes/sloth-bg.png"]
        self.background = None
        for bg_path in bg_paths:
            try:
                self.background = pygame.image.load(bg_path).convert()
                self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
                print(f"✅ Loaded sloth background: {bg_path}")
                break
            except (pygame.error, FileNotFoundError):
                continue
        
        if self.background is None:
            print("⚠️  Could not load sloth background. Using placeholder.")
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((30, 30, 40))

    def _load_wall_mask(self) -> None:
        """Loads the wall collision mask from an image."""
        try:
            path = "assets/images/scenes/sloth-walls.png"
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
        """Loads obstacles with collision (all sloth items except clock)."""
        # Load sloth-item-book-shelf.png làm obstacle - Có COLLISION
        try:
            img = pygame.image.load("assets/images/scenes/sloth-item-book-shelf.png").convert_alpha()
            pos = (280, 200)
            scale = 1.2
            original_size = img.get_size()
            new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
            img_scaled = pygame.transform.scale(img, new_size)
            collision_rect = pygame.Rect(pos[0], pos[1] + 20, new_size[0] - 20, new_size[1] - 40)
            
            self.obstacles.append({
                'image': img_scaled,
                'position': pos,
                'rect': collision_rect,
                'name': 'book_shelf'
            })
            print(f"✅ Loaded book shelf obstacle at {pos} (WITH collision)")
        except (pygame.error, FileNotFoundError) as e:
            print(f"⚠️  Could not load book shelf: {e}")
        
        # Load sloth-item-lamp.png làm obstacle - Có COLLISION
        try:
            img = pygame.image.load("assets/images/scenes/sloth-item-lamp.png").convert_alpha()
            pos = (1100, 500)
            scale = 1.3
            original_size = img.get_size()
            new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
            img_scaled = pygame.transform.scale(img, new_size)
            collision_rect = pygame.Rect(pos[0], pos[1] + 20, new_size[0] - 20, new_size[1] - 40)
            
            self.obstacles.append({
                'image': img_scaled,
                'position': pos,
                'rect': collision_rect,
                'name': 'lamp'
            })
            print(f"✅ Loaded lamp obstacle at {pos} (WITH collision)")
        except (pygame.error, FileNotFoundError) as e:
            print(f"⚠️  Could not load lamp: {e}")
        
        # Load sloth-item-npc-death.png làm obstacle - Có COLLISION
        try:
            img = pygame.image.load("assets/images/scenes/sloth-item-npc-death.png").convert_alpha()
            pos = (550, 200)
            scale = 1.2
            original_size = img.get_size()
            new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
            img_scaled = pygame.transform.scale(img, new_size)
            collision_rect = pygame.Rect(pos[0], pos[1] + 20, new_size[0] - 20, new_size[1] - 40)
            
            self.obstacles.append({
                'image': img_scaled,
                'position': pos,
                'rect': collision_rect,
                'name': 'npc_death'
            })
            print(f"✅ Loaded npc death obstacle at {pos} (WITH collision)")
        except (pygame.error, FileNotFoundError) as e:
            print(f"⚠️  Could not load npc death: {e}")
        
        # Load sloth-item-clock.png - KHÔNG collision (có thể nhặt)
        try:
            clock_img = pygame.image.load("assets/images/scenes/sloth-item-clock.png").convert_alpha()
            clock_pos = (950, 200)
            clock_scale = 1
            original_size = clock_img.get_size()
            new_size = (int(original_size[0] * clock_scale), int(original_size[1] * clock_scale))
            clock_img_scaled = pygame.transform.scale(clock_img, new_size)
            
            clock_rect = pygame.Rect(clock_pos[0], clock_pos[1], new_size[0], new_size[1])
            
            self.clock_data = {
                'image': clock_img_scaled,
                'position': clock_pos,
                'rect': clock_rect,
                'name': 'sloth_clock'
            }
            print(f"✅ Loaded clock at {clock_pos} (no collision - can pickup)")
        except (pygame.error, FileNotFoundError) as e:
            print(f"⚠️  Could not load clock: {e}")
            self.clock_data = None
    
    def _load_npcs(self) -> None:
        """Loads NPCs for interaction (no collision)."""
        npc_definitions = [
            {"name": "NPC_Lazy_Witness", "pos": (100, 500), "color": (150, 150, 255)},
        ]
        
        for npc_def in npc_definitions:
            npc_size = (60, 80)
            npc_surface = pygame.Surface(npc_size, pygame.SRCALPHA)
            pygame.draw.ellipse(npc_surface, npc_def["color"], (10, 10, 40, 50))
            pygame.draw.rect(npc_surface, npc_def["color"], (15, 55, 30, 25))
            
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
        print(f"✅ Built {len(self.collision_rects)} collision rects from obstacles.")

    def _setup_interaction_areas(self) -> None:
        """Creates all interaction areas for this scene."""
        # Interaction area cho clock (vật phẩm nhặt được)
        if self.clock_data and not self.clock_collected:
            interaction_rect = self.clock_data['rect'].inflate(60, 60)
            self.clock_interaction_area = InteractionArea(
                rect=interaction_rect, 
                callback=self._on_clock_pickup
            )
            self.interaction_areas.append(self.clock_interaction_area)
            print(f"✅ Created interaction area for clock pickup")
        
        # Interaction areas cho NPCs
        for npc in self.npcs:
            interaction_rect = npc['rect'].inflate(60, 60)
            area = InteractionArea(
                rect=interaction_rect,
                callback=lambda n=npc: self._on_npc_interact(n)
            )
            self.interaction_areas.append(area)
            self.npc_interaction_areas.append(area)
        
        print(f"✅ Created {len(self.npc_interaction_areas)} NPC interaction areas")

    def _on_clock_pickup(self) -> None:
        """Callback khi nhặt đồng hồ."""
        if not self.clock_collected:
            self.clock_collected = True
            print("🕐 Nhặt được chiếc đồng hồ!")
            
            # Xóa interaction area của clock
            if self.clock_interaction_area in self.interaction_areas:
                self.interaction_areas.remove(self.clock_interaction_area)
                print("✅ Removed clock interaction area")
    
    def _on_npc_interact(self, npc: Dict[str, Any]) -> None:
        """Callback khi tương tác với NPC."""
        print(f"💬 Đang nói chuyện với {npc['name']}...")
        # TODO: Implement dialogue system

    def set_player(self, player: object) -> None:
        """Sets the player reference and positions them for this scene."""
        self.player = player
        if self.player:
            start_x, start_y = (900, 400)
            self.player.x, self.player.y = start_x, start_y
            self.player.rect.topleft = (start_x, start_y)
            print(f"✅ Player position set to ({start_x}, {start_y}) for SlothCaseScene.")

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
        
        # Thêm obstacles (book shelf, lamp, npc death) vào danh sách vẽ
        for item in self.obstacles:
            if 'image' in item and 'position' in item:
                y_pos = item['position'][1] + item['rect'].height
                drawable_objects.append({'type': 'object', 'y': y_pos, 'item': item})
        
        # Thêm clock nếu chưa nhặt
        if self.clock_data and not self.clock_collected:
            y_pos = self.clock_data['position'][1] + self.clock_data['rect'].height
            drawable_objects.append({'type': 'clock', 'y': y_pos, 'item': self.clock_data})
        
        # Thêm NPCs
        for npc in self.npcs:
            y_pos = npc['position'][1] + npc['rect'].height
            drawable_objects.append({'type': 'npc', 'y': y_pos, 'item': npc})
        
        # Thêm player
        player_y = player.rect.y + player.rect.height
        drawable_objects.append({'type': 'player', 'y': player_y, 'item': player})
        
        # Sắp xếp theo Y-coordinate
        drawable_objects.sort(key=lambda obj: obj['y'])
        
        # Vẽ tất cả theo thứ tự
        for obj in drawable_objects:
            if obj['type'] == 'object':
                screen.blit(obj['item']['image'], obj['item']['position'])
            elif obj['type'] == 'clock':
                screen.blit(obj['item']['image'], obj['item']['position'])
            elif obj['type'] == 'npc':
                screen.blit(obj['item']['image'], obj['item']['position'])
            elif obj['type'] == 'player':
                player.draw(screen)

        # Vẽ interaction areas
        for area in self.interaction_areas:
            area.draw(screen, player.rect)
        
        # Debug mode
        if self.debug_mode:
            # Draw RED rects for obstacles
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

            font = pygame.font.Font(None, 24)
            text = f"Sloth | Obstacles: {len(self.collision_rects)} | NPCs: {len(self.npcs)} | Clock: {'Collected' if self.clock_collected else 'Available'} | F3"
            debug_text = font.render(text, True, (255, 255, 0))
            screen.blit(debug_text, (10, 10))
