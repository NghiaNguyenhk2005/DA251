import pygame
from typing import List, Optional, Dict, Any
from .i_scene import IScene
from src.utils.interaction_area import InteractionArea

class GluttonyScene(IScene):
    """
    Scene for the Gluttony case, featuring a dining hall.
    It uses a combination of a wall collision mask and rectangle-based obstacles.
    """
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Data structures for scene elements
        self.obstacles: List[Dict[str, Any]] = []
        self.collision_rects: List[pygame.Rect] = []
        self.interaction_areas: List[InteractionArea] = []
        self.wall_mask: Optional[pygame.mask.Mask] = None
        
        self.player: Optional[object] = None
        self.debug_mode = True

        # Load all assets and set up the scene
        self._load_background()
        self._load_wall_mask()
        self._load_obstacles()
        self._setup_collision_rects()
        self._setup_interaction_areas()

    def _load_background(self) -> None:
        """Loads the background image for the dining hall."""
        try:
            path = "assets/images/scenes/gluttony-bg.jpg"
            self.background = pygame.image.load(path).convert()
            self.background = pygame.transform.scale(self.background, (self.screen_width, self.screen_height))
            print(f"✅ Loaded background: {path} for GluttonyScene.")
        except (pygame.error, FileNotFoundError) as e:
            print(f"⚠️  Could not load background for GluttonyScene: {e}. Using placeholder.")
            self.background = pygame.Surface((self.screen_width, self.screen_height))
            self.background.fill((210, 105, 30)) # Brown/Orange placeholder

    def _load_wall_mask(self) -> None:
        """Loads the wall collision mask from the corresponding image."""
        try:
            path = "assets/images/scenes/gluttony-walls.png"
            mask_image = pygame.image.load(path).convert()
            mask_image = pygame.transform.scale(mask_image, (self.screen_width, self.screen_height))
            mask_image.set_colorkey((0, 0, 0)) # Black pixels are walkable
            self.wall_mask = pygame.mask.from_surface(mask_image)
            print(f"✅ Loaded wall collision mask from {path} for GluttonyScene.")
        except (pygame.error, FileNotFoundError) as e:
            print(f"⚠️  Could not load wall collision mask for GluttonyScene: {e}")
            self.wall_mask = pygame.mask.Mask((self.screen_width, self.screen_height), fill=False)

    def _load_obstacles(self) -> None:
        """Loads drawable obstacles like the dining table and the cake evidence."""
        # Define obstacles with their assets, positions, and scale
        obstacle_definitions = [
            {
                "name": "dining_table",
                "path": "assets/images/scenes/gluttony-item-table.png",
                "pos": (self.screen_width // 2, self.screen_height // 2 - 50), # Centered
                "scale": 1.0,
                "rect_offset": (50, 100),       # (dx, dy)
                "rect_modifier": (-100, -160)     # (dw, dh)
            },
            {
                "name": "evidence_cake",
                "path": "assets/images/scenes/gluttony-item-vatchung.png",
                "pos": (self.screen_width // 2 - 10, self.screen_height // 2 + 30),
                "scale": 0.5,
                "rect_offset": (0, 0),
                "rect_modifier": (0, 0)
            }
        ]
        
        for obs_def in obstacle_definitions:
            try:
                img = pygame.image.load(obs_def["path"]).convert_alpha()
                
                # Apply scaling
                scale = obs_def.get("scale", 1.0)
                original_size = img.get_size()
                new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
                img_scaled = pygame.transform.scale(img, new_size)
                
                # Position the center of the image at the defined pos
                img_rect = img_scaled.get_rect(center=obs_def["pos"])

                # Get new flexible rect parameters
                rect_offset = obs_def.get("rect_offset", (0, 0))
                rect_modifier = obs_def.get("rect_modifier", (0, 0))
                
                # Define a collision rect using the new flexible parameters
                collision_rect = pygame.Rect(
                    img_rect.x + rect_offset[0],
                    img_rect.y + rect_offset[1],
                    img_rect.width + rect_modifier[0],
                    img_rect.height + rect_modifier[1]
                )
                
                self.obstacles.append({
                    'image': img_scaled, # Store the scaled image
                    'position': img_rect.topleft,
                    'rect': collision_rect,
                    'name': obs_def['name']
                })
                print(f"✅ Loaded obstacle: {obs_def['name']} with scale {scale} for GluttonyScene.")
            except (pygame.error, FileNotFoundError) as e:
                print(f"⚠️  Could not load obstacle {obs_def['name']}: {e}")
                continue

    def _setup_collision_rects(self) -> None:
        """Builds a simple list of rects for collision checking."""
        self.collision_rects.clear()
        for obj in self.obstacles:
            self.collision_rects.append(obj['rect'])
        print(f"✅ Built {len(self.collision_rects)} collision rects for GluttonyScene.")

    def _setup_interaction_areas(self) -> None:
        """Creates interaction areas, e.g., for the cake evidence."""
        cake = next((obs for obs in self.obstacles if obs['name'] == 'evidence_cake'), None)
        if cake:
            interaction_rect = cake['rect'].inflate(40, 40)
            self.interaction_areas.append(
                InteractionArea(rect=interaction_rect, callback=self._on_cake_interact)
            )
            print("✅ Created interaction area around 'evidence_cake'.")

    def _on_cake_interact(self) -> None:
        """Callback for when the player interacts with the cake."""
        print("🍰 Player interacted with the cake evidence!")

    def set_player(self, player: object) -> None:
        """Sets the player and their starting position for this scene."""
        self.player = player
        if self.player:
            start_x = self.screen_width // 2
            start_y = self.screen_height - 150
            self.player.x, self.player.y = start_x, start_y
            self.player.rect.topleft = (start_x, start_y)
            print(f"✅ Player position set to ({start_x}, {start_y}) for GluttonyScene.")

    def check_collision(self, rect: pygame.Rect) -> bool:
        """Checks for collision with both rect obstacles and the wall mask."""
        if rect.collidelist(self.collision_rects) != -1:
            return True
        if self.wall_mask and self.wall_mask.overlap(pygame.mask.Mask(rect.size, fill=True), rect.topleft):
            return True
        return False

    def prevent_collision(self, player_rect: pygame.Rect, old_x: float, old_y: float) -> tuple:
        """Prevents player from passing through obstacles using sliding."""
        if not self.check_collision(player_rect):
            return player_rect.x, player_rect.y
        
        test_rect = player_rect.copy()
        test_rect.x = int(old_x)
        if not self.check_collision(test_rect):
            return old_x, player_rect.y
        
        test_rect.y = int(old_y)
        if not self.check_collision(test_rect):
            return player_rect.x, old_y
            
        return old_x, old_y

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handles scene-specific events."""
        if event.type == pygame.KEYDOWN and event.key == pygame.K_F3:
            self.debug_mode = not self.debug_mode
        for area in self.interaction_areas:
            area.handle_event(event)

    def update(self) -> None:
        """Updates scene logic."""
        if self.player:
            for area in self.interaction_areas:
                area.update(self.player.rect)

    def draw(self, screen: pygame.Surface) -> None:
        """Draws the background and debug info."""
        screen.blit(self.background, (0, 0))
        if self.debug_mode:
            self._draw_debug_info(screen)
            
    def draw_with_player(self, screen: pygame.Surface, player) -> None:
        """Draws the scene with all objects and the player, sorted by layer."""
        screen.blit(self.background, (0, 0))
        
        drawable_objects = [{'type': 'player', 'y': player.rect.bottom, 'item': player}]
        for item in self.obstacles:
            drawable_objects.append({'type': 'object', 'y': item['rect'].bottom, 'item': item})
        
        drawable_objects.sort(key=lambda obj: obj['y'])
        
        for obj in drawable_objects:
            if obj['type'] == 'object':
                screen.blit(obj['item']['image'], obj['item']['position'])
            elif obj['type'] == 'player':
                player.draw(screen)

        for area in self.interaction_areas:
            area.draw(screen, player.rect)
        
        if self.debug_mode:
            self._draw_debug_info(screen)

    def _draw_debug_info(self, screen: pygame.Surface):
        """Helper function to draw all debug visuals."""
        # Draw RED rects for obstacles
        for rect in self.collision_rects:
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
        text = f"GluttonyScene | Rects: {len(self.collision_rects)} | Interact: {len(self.interaction_areas)} | F3"
        debug_text = font.render(text, True, (255, 255, 0))
        screen.blit(debug_text, (10, 10))
