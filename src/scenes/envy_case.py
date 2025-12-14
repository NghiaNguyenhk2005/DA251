"""
Envy Case Scene
===============
Scene điều tra vụ án ganh tỵ - scene top-down với hệ thống va chạm.
Người chơi có thể di chuyển tự do để khám phá hiện trường vụ án.
"""

import pygame
from typing import List, Optional, Tuple, Dict, Any
from .base_scene import BaseScene
from src.utils.interaction_area import InteractionArea
from src.tools.Inventory_Item import envy_mask, Item # <--- NEW IMPORT

class EnvyCaseScene(BaseScene):
    """
    Envy Case scene using BaseScene for core functionality.
    """
    
    def __init__(self, screen_width: int = 1280, screen_height: int = 720, game_system=None) -> None:
        """
        Initializes the Envy Case Scene.
        """
        super().__init__(screen_width, screen_height)
        self.game_system = game_system # <--- STORE REFERENCE
        # Mask state (collectible specific to this scene)
        self.mask_collected: bool = False
        
        # Initialise standard assets
        self.setup_scene(
            background_path="assets/images/scenes/envy-bg.png",
            wall_mask_path="assets/images/scenes/envy-walls.png"
        )
        
        # Load specific scene objects
        self._load_obstacles()
        self._load_npcs()
        
        # Build standard components
        self.rebuild_collision_rects()
        self._setup_interaction_areas()
        
        # Fallback background
        if self.background.get_at((0,0)) == (0,0,0,255): 
             # self.background.fill((25, 35, 25))
             pass

    def _load_obstacles(self) -> None:
        """Loads obstacles for Envy Case."""
        # 1. NPC Obstacle
        try:
            npc_obstacle_img = pygame.image.load("assets/images/scenes/envy-npc.png").convert_alpha()
            npc_obstacle_pos = (550, 380)
            npc_obstacle_scale = 0.4
            original_size = npc_obstacle_img.get_size()
            new_size = (int(original_size[0] * npc_obstacle_scale), int(original_size[1] * npc_obstacle_scale))
            npc_obstacle_img_scaled = pygame.transform.scale(npc_obstacle_img, new_size)
            
            npc_obstacle_rect = pygame.Rect(npc_obstacle_pos[0], npc_obstacle_pos[1] + 20, 
                                           new_size[0] - 20, new_size[1] - 40)
            
            self.obstacles.append({
                'image': npc_obstacle_img_scaled,
                'position': npc_obstacle_pos,
                'rect': npc_obstacle_rect,
                'name': 'envy_npc_obstacle'
            })
            print(f"✅ Loaded envy-npc obstacle at {npc_obstacle_pos}")
        except (pygame.error, FileNotFoundError) as e:
            print(f"⚠️  Could not load envy-npc obstacle: {e}")
        
        # 2. Mask (Collectible)
        try:
            mask_img = pygame.image.load("assets/images/scenes/envy-mask.png").convert_alpha()
            mask_pos = (700, 420)
            mask_scale = 0.3
            original_size = mask_img.get_size()
            new_size = (int(original_size[0] * mask_scale), int(original_size[1] * mask_scale))
            mask_img_scaled = pygame.transform.scale(mask_img, new_size)
            
            mask_rect = pygame.Rect(mask_pos[0], mask_pos[1], new_size[0], new_size[1])
            
            self.collectible_items.append({
                'image': mask_img_scaled,
                'position': mask_pos,
                'rect': mask_rect,
                'name': 'envy_mask'
            })
            print(f"✅ Loaded mask at {mask_pos}")
        except (pygame.error, FileNotFoundError) as e:
            print(f"⚠️  Could not load mask: {e}")
    
    def _load_npcs(self) -> None:
        """Loads NPCs."""
        npc_definitions = [
            {"name": "NPC_Jealous_Suspect", "pos": (700, 200), "color": (100, 255, 100)},
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
        """Creates interaction areas."""
        # 1. Mask
        mask = next((item for item in self.collectible_items if item['name'] == 'envy_mask'), None)
        if mask:
            interaction_rect = mask['rect'].inflate(60, 60)
            self.mask_interaction_area = InteractionArea(
                rect=interaction_rect, 
                callback=self._on_mask_pickup
            )
            self.interaction_areas.append(self.mask_interaction_area)
        
        # 2. NPCs
        for npc in self.npcs:
            interaction_rect = npc['rect'].inflate(60, 60)
            area = InteractionArea(
                rect=interaction_rect,
                callback=lambda n=npc: self._on_npc_interact(n)
            )
            self.interaction_areas.append(area)

    def _on_mask_pickup(self) -> None:
        """Callback khi nhặt mask."""
        
        if not self.mask_collected:
            
            # 1. Attempt to add the item to the central inventory
            if self.game_system and self.game_system.add_item_to_inventory(envy_mask):
                
                # 2. If collection was successful, remove the item from the scene
                self.mask_collected = True
                
                # Remove interaction area
                if hasattr(self, 'mask_interaction_area') and self.mask_interaction_area in self.interaction_areas:
                    self.interaction_areas.remove(self.mask_interaction_area)
                
                # Remove visual
                # Filter the item out of the list of visible/collectible items
                self.collectible_items = [item for item in self.collectible_items if item['name'] != 'envy_mask']
            
            else:
                # Optionally show a message that inventory is full
                print("❌ Cannot collect item. Inventory is full!")
    def _on_npc_interact(self, npc: Dict[str, Any]) -> None:
        """Callback khi tương tác với NPC."""
        print(f"💬 Đang nói chuyện với {npc['name']}...")
        # TODO: Implement dialogue system

    def set_player(self, player: object) -> None:
        """Sets the player reference and positions them."""
        super().set_player(player, start_pos=(900, 400))

