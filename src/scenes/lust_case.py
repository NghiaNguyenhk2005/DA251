import pygame
from typing import List, Optional, Dict, Any
from .base_scene import BaseScene
from src.utils.interaction_area import InteractionArea

class LustCaseScene(BaseScene):
    """
    Scene for the Lust case.
    Uses a combination of a wall collision mask and rectangle-based obstacles.
    """
    
    def __init__(self, screen_width: int, screen_height: int):
        super().__init__(screen_width, screen_height)
        
        self.debug_mode = True

        # Setup standard assets
        self.setup_scene(
            background_path="assets/images/scenes/lust-bg.png",
            wall_mask_path="assets/images/scenes/lust-walls.png"
        )
        
        if self.background.get_at((0,0)) == (0,0,0,255):
            self.background.fill((255, 105, 180)) # Pink placeholder

        # Load Scene Objects
        self._load_obstacles()
        self._load_npcs()
        
        # Build Standard Components
        self.rebuild_collision_rects()
        self._setup_interaction_areas()

    def _load_obstacles(self) -> None:
        """Loads drawable obstacles for the scene."""
        # Positions are approximate, based on the background image.
        obstacle_definitions = [
            { "name": "sofa1", "path": "assets/images/scenes/lust-item-sofa1.png", "pos": (self.screen_width//2, 250), "scale": 2, "rect_offset": (0, 20), "rect_modifier": (0, -40) },
            { "name": "sofa2", "path": "assets/images/scenes/lust-item-sofa2.png", "pos": (self.screen_width//2+300, 350), "scale": 2, "rect_offset": (0, 20), "rect_modifier": (0, -40) },
            { "name": "table1", "path": "assets/images/scenes/lust-item-table1.png", "pos": (250, 400), "scale": 2, "rect_offset": (50, 50), "rect_modifier": (-100, -100) },
            { "name": "table2", "path": "assets/images/scenes/lust-item-table2.png", "pos": (self.screen_width//2, 350), "scale": 2, "rect_offset": (25, 25), "rect_modifier": (-50, -50) },
            { "name": "chair", "path": "assets/images/scenes/lust-item-chair.png", "pos": (150, 350), "scale": 2, "rect_offset": (50, 50), "rect_modifier": (-100, -100) },
            { "name": "npc_death", "path": "assets/images/scenes/lust-item-npc-death.png", "pos": (640, 450), "scale": 2, "rect_offset": (50, 50), "rect_modifier": (-100,-100) },
        ]
        
        for obs_def in obstacle_definitions:
            try:
                img = pygame.image.load(obs_def["path"]).convert_alpha()
                scale = obs_def.get("scale", 1.0)
                original_size = img.get_size()
                new_size = (int(original_size[0] * scale), int(original_size[1] * scale))
                img_scaled = pygame.transform.scale(img, new_size)
                
                img_rect = img_scaled.get_rect(center=obs_def["pos"])
                
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
                print(f"✅ Loaded obstacle: {obs_def['name']} for LustScene.")
            except (pygame.error, FileNotFoundError) as e:
                print(f"⚠️  Could not load obstacle {obs_def['name']}: {e}")
                continue

    def _load_npcs(self) -> None:
        """Loads NPCs."""
        npc_definitions = [
            {"name": "NPC_Lust_Witness", "pos": (800, 250), "color": (255, 100, 180)},
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
        """Creates interaction areas for key objects."""
        # Body (Find in obstacles)
        npc_body = next((obs for obs in self.obstacles if obs['name'] == 'npc_death'), None)
        if npc_body:
            interaction_rect = npc_body['rect'].inflate(50, 50)
            self.interaction_areas.append(
                InteractionArea(rect=interaction_rect, callback=self._on_body_interact)
            )
            print("✅ Created interaction area around 'npc_death'.")

        # NPCs
        for npc in self.npcs:
            interaction_rect = npc['rect'].inflate(100, 100)
            callback = lambda npc_name=npc['name']: self._on_npc_interact(npc_name)
            self.interaction_areas.append(InteractionArea(rect=interaction_rect, callback=callback))

    def _on_body_interact(self) -> None:
        """Callback for when the player interacts with the body."""
        print("!! Player interacted with the body in the Lust scene!")
    
    def _on_npc_interact(self, npc_name: str) -> None:
        """Callback khi người chơi tương tác với NPC."""
        print(f"💬 Đang nói chuyện với {npc_name}...")

    def set_player(self, player: object) -> None:
        """Sets the player and their starting position for this scene."""
        start_x = self.screen_width // 2
        start_y = self.screen_height - 150
        super().set_player(player, start_pos=(start_x, start_y))
