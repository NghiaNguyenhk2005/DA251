
"""
Sloth Case Scene
===============
Scene điều tra vụ án lười biếng - scene top-down với hệ thống va chạm.
Người chơi có thể di chuyển tự do để khám phá hiện trường vụ án.
"""

import pygame
from typing import List, Optional, Tuple, Dict, Any
from .base_scene import BaseScene
from src.utils.interaction_area import InteractionArea

class SlothCaseScene(BaseScene):
    """
    Sloth Case scene using BaseScene for core functionality.
    """
    
    def __init__(self, screen_width: int = 1280, screen_height: int = 720) -> None:
        """
        Initializes the Sloth Case Scene.
        """
        super().__init__(screen_width, screen_height)
        
        self.debug_mode = False

        # Clock state (vật thể có thể nhặt)
        self.clock_collected: bool = False
        
        # Setup standard assets
        self.setup_scene(
            background_path="assets/images/scenes/sloth-bg.jpg",
            wall_mask_path="assets/images/scenes/sloth-walls.png"
        )
        
        # Fallback background
        if self.background.get_at((0,0)) == (0,0,0,255):
             self.background.fill((30, 30, 40))

        # Load Scene Objects
        self._load_obstacles()
        self._load_npcs()
        
        # Build Standard Components
        self.rebuild_collision_rects()
        self._setup_interaction_areas()

    def _load_obstacles(self) -> None:
        """Loads obstacles with collision (all sloth items including clock as collectible)."""
        # Load obstacles
        obstacle_definitions = [
            {
                "name": "book_shelf",
                "path": "assets/images/scenes/sloth-item-book-shelf.png",
                "pos": (280, 200),
                "scale": 1.2,
                "rect_offset": (0, 20),
                "rect_modifier": (-20, -40)
            },
            {
                "name": "lamp",
                "path": "assets/images/scenes/sloth-item-lamp.png",
                "pos": (1100, 500),
                "scale": 1.3,
                "rect_offset": (0, 20),
                "rect_modifier": (-20, -40)
            },
            {
                "name": "npc_death",
                "path": "assets/images/scenes/sloth-item-npc-death.png",
                "pos": (550, 200),
                "scale": 1.2,
                "rect_offset": (0, 20),
                "rect_modifier": (-20, -40)
            }
        ]
        
        for obs_def in obstacle_definitions:
            try:
                img = pygame.image.load(obs_def["path"]).convert_alpha()
                scale = obs_def.get("scale", 1.0)
                original_size = img.get_size()
                new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
                img_scaled = pygame.transform.scale(img, new_size)
                
                # Check if position is center or topleft? Original code seemed to use topleft for these custom ones?
                # Actually original used pos directly as topleft for Rect, but pos as is for blitting/rect?
                # Original: collision_rect = pygame.Rect(pos[0], pos[1] + 20, new_size[0] - 20, new_size[1] - 40)
                # And stored position: pos. 
                # So pos was TOPLEFT of the image.
                
                img_rect = img_scaled.get_rect(topleft=obs_def["pos"])
                
                rect_offset = obs_def.get("rect_offset", (0, 0))
                rect_modifier = obs_def.get("rect_modifier", (0, 0))
                
                collision_rect = pygame.Rect(
                    img_rect.x + rect_offset[0],
                    img_rect.y + rect_offset[1],
                    img_rect.width + rect_modifier[0],
                    img_rect.height + rect_modifier[1]
                )
                
                self.obstacles.append({
                    'image': img_scaled,
                    'position': img_rect.topleft,
                    'rect': collision_rect,
                    'name': obs_def['name']
                })
                print(f"✅ Loaded obstacle: {obs_def['name']} with scale {scale}")
            except (pygame.error, FileNotFoundError) as e:
                print(f"⚠️  Could not load obstacle {obs_def['name']}: {e}")
                continue
        
        # Load sloth-item-clock.png - collectible
        try:
            clock_img = pygame.image.load("assets/images/scenes/sloth-item-clock.png").convert_alpha()
            clock_pos = (950, 200)
            clock_scale = 1
            original_size = clock_img.get_size()
            new_size = (int(original_size[0] * clock_scale), int(original_size[1] * clock_scale))
            clock_img_scaled = pygame.transform.scale(clock_img, new_size)
            
            clock_rect = pygame.Rect(clock_pos[0], clock_pos[1], new_size[0], new_size[1])
            
            self.collectible_items.append({
                'image': clock_img_scaled,
                'position': clock_pos,
                'rect': clock_rect,
                'name': 'sloth_clock'
            })
            print(f"✅ Loaded clock at {clock_pos} (collectible)")
        except (pygame.error, FileNotFoundError) as e:
            print(f"⚠️  Could not load clock: {e}")
    
    def _load_npcs(self) -> None:
        """Loads NPCs."""
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
        print(f"✅ Loaded {len(self.npcs)} NPCs")

    def _setup_interaction_areas(self) -> None:
        """Creates all interaction areas for this scene."""
        # 1. Clock Pickup
        clock = next((item for item in self.collectible_items if item['name'] == 'sloth_clock'), None)
        if clock:
            interaction_rect = clock['rect'].inflate(60, 60)
            self.clock_interaction_area = InteractionArea(
                rect=interaction_rect, 
                callback=self._on_clock_pickup
            )
            self.interaction_areas.append(self.clock_interaction_area)
            print(f"✅ Created interaction area for clock pickup")
        
        # 2. NPC Interaction
        for npc in self.npcs:
            interaction_rect = npc['rect'].inflate(60, 60)
            callback = lambda n=npc: self._on_npc_interact(n)
            self.interaction_areas.append(InteractionArea(rect=interaction_rect, callback=callback))

    def _on_clock_pickup(self) -> None:
        """Callback khi nhặt đồng hồ."""
        if not self.clock_collected:
            self.clock_collected = True
            print("🕐 Nhặt được chiếc đồng hồ!")
            
            # Remove interaction area
            if hasattr(self, 'clock_interaction_area') and self.clock_interaction_area in self.interaction_areas:
                self.interaction_areas.remove(self.clock_interaction_area)
            
            # Remove visual
            self.collectible_items = [item for item in self.collectible_items if item['name'] != 'sloth_clock']
    
    def _on_npc_interact(self, npc: Dict[str, Any]) -> None:
        """Callback khi tương tác với NPC."""
        print(f"💬 Đang nói chuyện với {npc['name']}...")
        # TODO: Implement dialogue system

    def set_player(self, player: object) -> None:
        """Sets the player reference and positions them for this scene."""
        super().set_player(player, start_pos=(900, 400))

    def handle_event(self, event: pygame.event.Event) -> None:
        """Handles scene-specific events."""
        super().handle_event(event) # Call BaseScene's event handler first
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F3:
                self.debug_mode = not self.debug_mode
                print(f"Debug mode: {'ON' if self.debug_mode else 'OFF'}")
    
    def update(self) -> None:
        """Updates scene logic."""
        super().update() # Call BaseScene's update
    
    def draw_with_player(self, screen: pygame.Surface, player) -> None:
        """Draws the scene with the player, using Y-sorting for layering."""
        super().draw_with_player(screen, player) # Call BaseScene's drawing logic
        
        # Draw interaction areas (BaseScene already draws them, but if you want custom drawing, do it here)
        # for area in self.interaction_areas:
        #     area.draw(screen, player.rect)
        
        # Debug mode
        if self.debug_mode:
            # BaseScene already draws collision rects and wall mask in debug mode
            # Draw CYAN rects for interaction areas
            for area in self.interaction_areas:
                area.draw_debug(screen)

            font = pygame.font.Font(None, 24)
            text = f"Sloth | Obstacles: {len(self.obstacles)} | NPCs: {len(self.npcs)} | Clock: {'Collected' if self.clock_collected else 'Available'} | F3"
            debug_text = font.render(text, True, (255, 255, 0))
            screen.blit(debug_text, (10, 10))