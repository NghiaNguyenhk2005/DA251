import pygame
from typing import List, Optional, Dict, Any
from .base_scene import BaseScene
from src.utils.interaction_area import InteractionArea

class PrideCaseScene(BaseScene):
    """
    Scene for the Pride case, set on a rainy city street.
    """
    
    def __init__(self, screen_width: int, screen_height: int):
        super().__init__(screen_width, screen_height)
        
        self.debug_mode = True

        # Setup standard assets
        self.setup_scene(
            background_path="assets/images/scenes/pride-bg.png",
            wall_mask_path="assets/images/scenes/pride-walls.png"
        )
        
        if self.background.get_at((0,0)) == (0,0,0,255):
            self.background.fill((70, 80, 90)) # Rainy city placeholder color

        # Load Scene Objects
        self._load_obstacles()
        self._load_npcs()
        
        # Build Standard Components
        self.rebuild_collision_rects()
        self._setup_interaction_areas()

    def _load_obstacles(self) -> None:
        """Loads drawable obstacles for the scene."""
        obstacle_definitions = [
            { "name": "car", "path": "assets/images/scenes/pride-item-car.png", "pos": (200, 620), "scale": 1.5, "rect_offset": (0, 40), "rect_modifier": (0, -80) },
            { "name": "npc_death", "path": "assets/images/scenes/pride-item-npc-death.png", "pos": (500, 630), "scale": 1.0, "rect_offset": (50, 50), "rect_modifier": (-100, -100) },
            { "name": "broken_image", "path": "assets/images/scenes/pride-item-broken-image.png", "pos": (800, 650), "rect_offset": (50, 50), "rect_modifier": (-100, -100) },
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
                print(f"✅ Loaded obstacle: {obs_def['name']} for PrideScene.")
            except (pygame.error, FileNotFoundError) as e:
                print(f"⚠️  Could not load obstacle {obs_def['name']}: {e}")
                continue

    def _load_npcs(self) -> None:
        """Loads NPCs."""
        npc_definitions = [
            {"name": "NPC_Pride_Witness", "pos": (600, 300), "color": (100, 100, 255)},
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
        # 1. Body
        npc_body = next((obs for obs in self.obstacles if obs['name'] == 'npc_death'), None)
        if npc_body:
            self.interaction_areas.append(
                InteractionArea(rect=npc_body['rect'].inflate(80, 80), callback=self._on_body_interact)
            )
            print("✅ Created interaction area around 'npc_death'.")
        
        # 2. Broken Image
        broken_image = next((obs for obs in self.obstacles if obs['name'] == 'broken_image'), None)
        if broken_image:
            self.interaction_areas.append(
                InteractionArea(rect=broken_image['rect'].inflate(60, 60), callback=self._on_image_interact)
            )
            print("✅ Created interaction area around 'broken_image'.")

        # 3. NPCs
        for npc in self.npcs:
            interaction_rect = npc['rect'].inflate(100, 100)
            callback = lambda npc_name=npc['name']: self._on_npc_interact(npc_name)
            self.interaction_areas.append(InteractionArea(rect=interaction_rect, callback=callback))

    def _on_body_interact(self) -> None:
        """Callback for when the player interacts with the body."""
        print("!! Player interacted with the body in the Pride scene!")

    def _on_image_interact(self) -> None:
        """Callback for when the player interacts with the broken image."""
        print("🖼️ Player interacted with the broken image.")

    def _on_npc_interact(self, npc_name: str) -> None:
        """Callback khi người chơi tương tác với NPC."""
        print(f"💬 Đang nói chuyện với {npc_name}...")

    def set_player(self, player: object) -> None:
        """Sets the player and their starting position for this scene."""
        start_x = self.screen_width - 200
        start_y = self.screen_height - 300
        super().set_player(player, start_pos=(start_x, start_y))
