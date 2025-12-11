import pygame
from typing import List, Optional, Dict, Any
from .base_scene import BaseScene
from src.utils.interaction_area import InteractionArea

class GluttonyCaseScene(BaseScene):
    """
    Scene for the Gluttony case, featuring a dining hall.
    It uses a combination of a wall collision mask and rectangle-based obstacles.
    """
    
    def __init__(self, screen_width: int, screen_height: int):
        super().__init__(screen_width, screen_height)
        
        self.debug_mode = True # Original had this True by default? Or maybe just leftover debug. BaseScene defaults False.

        # Setup standard assets
        self.setup_scene(
            background_path="assets/images/scenes/gluttony-bg.jpg",
            wall_mask_path="assets/images/scenes/gluttony-walls.png"
        )
        
        # Fallback background colour
        if self.background.get_at((0,0)) == (0,0,0,255):
             self.background.fill((210, 105, 30)) # Brown/Orange placeholder

        # Load Scene Objects
        self._load_obstacles()
        self._load_npcs()
        
        # Build Standard Components
        self.rebuild_collision_rects()
        self._setup_interaction_areas()

    def _load_obstacles(self) -> None:
        """Loads drawable obstacles like the dining table and the cake evidence."""
        # Define obstacles with their assets, positions, and scale
        obstacle_definitions = [
            {
                "name": "dining_table",
                "path": "assets/images/scenes/gluttony-item-table.png",
                "pos": (self.screen_width // 2, self.screen_height // 2+70), # Centered
                "scale": 1.75,
                "rect_offset": (140, 100),       # (dx, dy)
                "rect_modifier": (-280, -160)     # (dw, dh)
            },
            {
                "name": "evidence_cake",
                "path": "assets/images/scenes/gluttony-item-vatchung.png",
                "pos": (self.screen_width // 2, self.screen_height // 2 + 170),
                "scale": 1,
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
                print(f"✅ Loaded obstacle: {obs_def['name']} with scale {scale}")
            except (pygame.error, FileNotFoundError) as e:
                print(f"⚠️  Could not load obstacle {obs_def['name']}: {e}")
                continue

    def _load_npcs(self) -> None:
        """Loads NPCs."""
        npc_definitions = [
            {"name": "NPC_Gluttony_Chef", "pos": (200, 400), "color": (150, 75, 0)},
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
        """Creates interaction areas, e.g., for the cake evidence."""
        # 1. Cake Evidence (Find in obstacles)
        cake = next((obs for obs in self.obstacles if obs['name'] == 'evidence_cake'), None)
        if cake:
            interaction_rect = cake['rect'].inflate(350, 40)
            self.interaction_areas.append(
                InteractionArea(rect=interaction_rect, callback=self._on_cake_interact)
            )
            print("✅ Created interaction area around 'evidence_cake'.")

        # 2. NPCs
        for npc in self.npcs:
            interaction_rect = npc['rect'].inflate(100, 100)
            callback = lambda npc_name=npc['name']: self._on_npc_interact(npc_name)
            self.interaction_areas.append(InteractionArea(rect=interaction_rect, callback=callback))

    def _on_npc_interact(self, npc_name: str) -> None:
        """Callback khi người chơi tương tác với NPC."""
        print(f"💬 Đang nói chuyện với {npc_name}...")

    def _on_cake_interact(self) -> None:
        """Callback for when the player interacts with the cake."""
        print("🍰 Player interacted with the cake evidence!")

    def set_player(self, player: object) -> None:
        """Sets the player and their starting position for this scene."""
        start_y = self.screen_height - 50
        super().set_player(player, start_pos=(0, start_y))
