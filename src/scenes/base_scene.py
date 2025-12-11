import pygame
from typing import List, Optional, Dict, Any
from .i_scene import IScene
from src.utils.interaction_area import InteractionArea

class BaseScene(IScene):
    """
    Base generic scene for Case Scenes, handling common logic like:
    - Debug mode (F3)
    - Collision detection (Mask + Rects)
    - Asset loading (Background, Walls)
    - Object management (Obstacles, NPCs, Interaction Areas)
    - Rendering (Background, Y-sorted Entities, Debug info)
    """

    def __init__(self, screen_width: int = 1280, screen_height: int = 720):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # --- Asset Paths (Set these in subclass __init__ before super().__init__ if possible, or override _load methods) ---
        # Actually, standard practice: Subclass calls super().__init__, then loads specific things.
        # But for shared logic, we can have defaults or placeholders.
        
        # --- Core Data Structures ---
        self.obstacles: List[Dict[str, Any]] = []           # Visual objects with potential collision
        self.collision_rects: List[pygame.Rect] = []        # Pure collision rects (derived from obstacles or added manually)
        self.interaction_areas: List[InteractionArea] = []  # Interactive zones
        self.npcs: List[Dict[str, Any]] = []                # NPCs (visual only usually, interaction handled via areas)
        self.collectible_items: List[Dict[str, Any]] = []   # Items on ground (like woodpad, mask)
        
        self.wall_mask: Optional[pygame.mask.Mask] = None
        self.background: pygame.Surface = pygame.Surface((self.screen_width, self.screen_height))
        self.background.fill((0, 0, 0))

        self.player: Optional[object] = None
        self.debug_mode: bool = False

    # --- Loading Methods (Subclasses can override or extend) ---

    def setup_scene(self, background_path: Optional[str], wall_mask_path: Optional[str]):
        """
        Helper to load standard assets. Call this from subclass.
        """
        if background_path:
            self._load_background(background_path)
        
        if wall_mask_path:
            self._load_wall_mask(wall_mask_path)
            
    def _load_background(self, path: str) -> None:
        try:
            bg = pygame.image.load(path).convert()
            self.background = pygame.transform.scale(bg, (self.screen_width, self.screen_height))
            print(f"✅ Loaded background: {path}")
        except (pygame.error, FileNotFoundError) as e:
            print(f"⚠️  Could not load background {path}: {e}")
            # Keep default black/placeholder

    def _load_wall_mask(self, path: str) -> None:
        try:
            mask_image = pygame.image.load(path).convert()
            mask_image = pygame.transform.scale(mask_image, (self.screen_width, self.screen_height))
            mask_image.set_colorkey((0, 0, 0)) # Assuming black is transparent/walkable
            self.wall_mask = pygame.mask.from_surface(mask_image)
            print(f"✅ Loaded wall collision mask: {path}")
        except (pygame.error, FileNotFoundError) as e:
            print(f"⚠️  Could not load wall mask {path}: {e}")
            self.wall_mask = pygame.mask.Mask((self.screen_width, self.screen_height), fill=False)

    def rebuild_collision_rects(self) -> None:
        """Rebuilds self.collision_rects from self.obstacles."""
        self.collision_rects.clear()
        for obj in self.obstacles:
            if 'rect' in obj:
                self.collision_rects.append(obj['rect'])
        print(f"✅ Rebuilt {len(self.collision_rects)} collision rects from obstacles.")

    def set_player(self, player: object, start_pos: tuple = (100, 100)) -> None:
        self.player = player
        if self.player:
            self.player.x, self.player.y = start_pos
            self.player.rect.topleft = start_pos
            print(f"✅ Player set at {start_pos}")

    # --- Core Logic Implementation ---

    def check_collision(self, rect: pygame.Rect) -> bool:
        """
        Checks if the given rect collides with:
        1. Any rect in self.collision_rects
        2. The self.wall_mask (pixel perfect)
        """
        # 1. Obstacle Rects
        if rect.collidelist(self.collision_rects) != -1:
            return True
        
        # 2. Wall Mask
        if self.wall_mask:
            # Create a mask for the player/rect
            # Optimisation: We assume the player is roughly a filled box for mask check, or we could use player's actual mask if available.
            # Using a filled rect mask is safer and standard for top-down walking.
            player_mask = pygame.mask.Mask(rect.size, fill=True)
            offset = (rect.x, rect.y)
            if self.wall_mask.overlap(player_mask, offset):
                return True

        return False

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handles debug toggle and interaction areas."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                self.debug_mode = not self.debug_mode
                print(f"Debug mode: {'ON' if self.debug_mode else 'OFF'}")
        
        for area in self.interaction_areas:
            area.handle_event(event)

    def update(self) -> None:
        """Updates interaction areas with player position."""
        if self.player:
            for area in self.interaction_areas:
                area.update(self.player.rect)

    def draw(self, screen: pygame.Surface) -> None:
        """
        Draws the scene.
        Note: The game loop calls `draw(screen)`, but `WrathCaseScene` had `draw_with_player`.
        Usually `draw` is for background/static, and entities are drawn separately, OR `draw` handles everything.
        We will support `draw_with_player` as the primary render method if the game loop uses it.
        If the game loop calls `draw`, we will just draw background and debug.
        """
        screen.blit(self.background, (0, 0))
        if self.debug_mode:
            self._draw_debug(screen)

    def draw_with_player(self, screen: pygame.Surface, player: object) -> None:
        """
        Y-Sort rendering of all scene entities + player.
        """
        # 1. Background
        screen.blit(self.background, (0, 0))

        # 2. Collect All Drawable Objects
        drawable_objects = []

        # Player
        drawable_objects.append({
            'type': 'player', 
            'y': player.rect.bottom, 
            'item': player
        })

        # Obstacles
        for obj in self.obstacles:
            # Ensure object has image and position
            if 'image' in obj and 'position' in obj:
                # Use bottom of rect for sorting if available, else position + height
                y = obj['position'][1] + obj['image'].get_height()
                if 'rect' in obj:
                    y = obj['rect'].bottom
                drawable_objects.append({'type': 'object', 'y': y, 'item': obj})

        # NPCs
        for npc in self.npcs:
            y = npc['position'][1] + npc['image'].get_height()
            if 'rect' in npc:
                y = npc['rect'].bottom
            drawable_objects.append({'type': 'npc', 'y': y, 'item': npc})

        # Collectibles (Items on ground)
        for item in self.collectible_items:
            y = item['position'][1] + item['image'].get_height()
            if 'rect' in item:
                y = item['rect'].bottom
            drawable_objects.append({'type': 'collectible', 'y': y, 'item': item})

        # 3. Sort by Y
        drawable_objects.sort(key=lambda x: x['y'])

        # 4. Draw
        for obj in drawable_objects:
            t = obj['type']
            item = obj['item']
            if t == 'player':
                item.draw(screen)
            else:
                screen.blit(item['image'], item['position'])

        # 5. Overlays (Interaction Areas)
        for area in self.interaction_areas:
            area.draw(screen, player.rect)

        # 6. Debug
        if self.debug_mode:
            self._draw_debug(screen)

    def _draw_debug(self, screen: pygame.Surface):
        # Obstacles (Red)
        for rect in self.collision_rects:
            s = pygame.Surface(rect.size, pygame.SRCALPHA)
            s.fill((255, 0, 0, 100))
            screen.blit(s, rect.topleft)
            pygame.draw.rect(screen, (255, 0, 0), rect, 2)
        
        # Wall Mask (Blue Outline)
        if self.wall_mask:
            outline = self.wall_mask.outline()
            if outline:
                pygame.draw.lines(screen, (0, 0, 255), True, outline, 2)

        # Interaction Areas (Cyan/Green - handled by their own debug draw)
        for area in self.interaction_areas:
            area.draw_debug(screen)
            
        # Stats
        font = pygame.font.Font(None, 24)
        count_obs = len(self.collision_rects)
        count_int = len(self.interaction_areas)
        count_npc = len(self.npcs)
        
        text_str = f"BaseScene | Obs: {count_obs} | NPCs: {count_npc} | Interact: {count_int} | F3: Toggle Debug"
        text = font.render(text_str, True, (255, 255, 0))
        screen.blit(text, (10, 10))
