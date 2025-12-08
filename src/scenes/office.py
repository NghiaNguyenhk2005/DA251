"""
Office Scene
============
Văn phòng chính - scene top-down với hệ thống va chạm.
Người chơi có thể di chuyển tự do nhưng không thể đi xuyên qua các vật cản.

Collision System:
- Sử dụng AABB (Axis-Aligned Bounding Box) collision detection
- Các vùng va chạm được định nghĩa trong một list để dễ dàng chỉnh sửa
- Obstacles bao gồm: tường, bàn làm việc, ghế, tủ hồ sơ, v.v.
"""

import pygame
from typing import List, Optional, Tuple, Dict, Any
from .i_scene import IScene


from src.utils.interaction_area import InteractionArea


class OfficeScene(IScene):
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

        self._load_background()
        self._load_wall_mask() # Load the new wall mask
        self._load_obstacles()
        self._setup_collision_rects()
        self._setup_interaction_areas()
        
        self.player: Optional[object] = None
        self.debug_mode: bool = True

    def _load_background(self) -> None:
        """Loads the background image for the scene."""
        bg_paths = ["assets/images/scenes/office-bg.jpg", "assets/images/scenes/office.png", "src/assets/images/scenes/office-bg.jpg"]
        self.background = None
        for bg_path in bg_paths:
            try:
                self.background = pygame.image.load(bg_path).convert()
                self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
                print(f"✅ Loaded office background: {bg_path}")
                break
            except (pygame.error, FileNotFoundError):
                continue
        
        if self.background is None:
            print("⚠️  Could not load office background. Using placeholder.")
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((40, 40, 50))

    def _load_wall_mask(self) -> None:
        """Loads the wall collision mask from an image."""
        try:
            path = "assets/images/scenes/office-walls.png"
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
        """Loads the drawable obstacle objects (chairs)."""
        obstacle_definitions = [
            {"path": "assets/images/scenes/office-chair1.png", "pos": (220, 300), "scale": 1.3},
            {"path": "assets/images/scenes/office-chair2.png", "pos": (self.screen_width//2-100, 240), "scale": 1.3},
            {"path": "assets/images/scenes/office-chair3.png", "pos": (self.screen_width//2, self.screen_height//2 + 150), "scale": 1.3},
        ]
        
        loaded_count = 0
        for i, obs_def in enumerate(obstacle_definitions):
            try:
                img = pygame.image.load(obs_def["path"]).convert_alpha()
                x, y = obs_def["pos"]
                scale = obs_def["scale"]
                original_size = img.get_size()
                new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
                img_scaled = pygame.transform.scale(img, new_size)
                collision_rect = pygame.Rect(x, y+50, new_size[0], new_size[1]-100)
                
                self.obstacles.append({
                    'image': img_scaled,
                    'position': (x, y),
                    'rect': collision_rect,
                    'name': f'chair{i+1}'
                })
                loaded_count += 1
            except (pygame.error, FileNotFoundError) as e:
                print(f"⚠️  Could not load {obs_def['path']}: {e}")
                continue
        print(f"✅ Loaded {loaded_count} rectangle-based obstacle objects.")

    def _setup_collision_rects(self) -> None:
        """Creates a list of pygame.Rects for efficient collision checking."""
        self.collision_rects.clear()
        for obj in self.obstacles:
            if 'rect' in obj:
                self.collision_rects.append(obj['rect'])
        print(f"✅ Built {len(self.collision_rects)} collision rects from obstacles.")

    def _setup_interaction_areas(self) -> None:
        """Creates all interaction areas for this scene."""
        target_obstacle_name = 'chair2'
        target_obstacle = next((obs for obs in self.obstacles if obs['name'] == target_obstacle_name), None)
        
        if target_obstacle:
            interaction_rect = target_obstacle['rect'].inflate(60, 60)
            self.interaction_areas.append(
                InteractionArea(rect=interaction_rect, callback=self._on_chair_interact)
            )
            print(f"✅ Created interaction area around '{target_obstacle_name}'")

    def _on_chair_interact(self) -> None:
        """Callback for when the player interacts with a chair."""
        print("💡 Player pressed [F] near the chair. Time to investigate!")

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
        for item in self.obstacles:
            if 'image' in item and 'position' in item:
                y_pos = item['position'][1] + item['rect'].height
                drawable_objects.append({'type': 'object', 'y': y_pos, 'item': item})
        
        player_y = player.rect.y + player.rect.height
        drawable_objects.append({'type': 'player', 'y': player_y, 'item': player})
        
        drawable_objects.sort(key=lambda obj: obj['y'])
        
        for obj in drawable_objects:
            if obj['type'] == 'object':
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

            font = pygame.font.Font(None, 24)
            text = f"Masks: ON | Rects: {len(self.collision_rects)} | Interact: {len(self.interaction_areas)} | F3"
            debug_text = font.render(text, True, (255, 255, 0))
            screen.blit(debug_text, (10, 10))

