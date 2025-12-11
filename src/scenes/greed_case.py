"""
Greed Case Scene
================
Scene điều tra vụ án tham lam - scene top-down với hệ thống va chạm.
Người chơi có thể di chuyển tự do để khám phá hiện trường vụ án.
"""

import pygame
from typing import List, Optional, Tuple, Dict, Any
from .base_scene import BaseScene


from src.utils.interaction_area import InteractionArea


class GreedCaseScene(BaseScene):
    """
    Greed Case scene using BaseScene for core functionality.
    """
    
    def __init__(self, screen_width: int = 1280, screen_height: int = 720) -> None:
        """
        Initializes the Greed Case Scene.
        """
        super().__init__(screen_width, screen_height)
        
        self.debug_mode = True # Keep preference
        
        # Coin state
        self.coin_collected: bool = False
        
        # Setup standard assets
        self.setup_scene(
            background_path="assets/images/scenes/greed-bg.png",
            wall_mask_path="assets/images/scenes/greed-walls.png"
        )
        
        # Fallback background
        if self.background.get_at((0,0)) == (0,0,0,255):
             self.background.fill((40, 40, 50))

        # Load Scene Objects
        self._load_obstacles() 
        self._load_npcs()
        
        # Build Standard Components
        self.rebuild_collision_rects()
        self._setup_interaction_areas()
        
    def _load_obstacles(self) -> None:
        """Loads (collectible) coin."""
        # Load coin - không tạo collision, chỉ hiển thị (collectible)
        try:
            coin_img = pygame.image.load("assets/images/scenes/greed-coin.png").convert_alpha()
            coin_pos = (600, 250)
            coin_scale = 0.5
            original_size = coin_img.get_size()
            new_size = (int(original_size[0] * coin_scale), int(original_size[1] * coin_scale))
            coin_img_scaled = pygame.transform.scale(coin_img, new_size)
            
            coin_rect = pygame.Rect(coin_pos[0], coin_pos[1], new_size[0], new_size[1])
            
            self.collectible_items.append({
                'image': coin_img_scaled,
                'position': coin_pos,
                'rect': coin_rect,
                'name': 'greed_coin'
            })
            print(f"✅ Loaded coin at {coin_pos}")
        except (pygame.error, FileNotFoundError) as e:
            print(f"⚠️  Could not load coin: {e}")
    
    def _load_npcs(self) -> None:
        """Loads NPCs."""
        npc_definitions = [
            {"name": "NPC_1", "pos": (100, 500), "color": (255, 100, 100)}
        ]
        
        for npc_def in npc_definitions:
            npc_size = (60, 80)
            npc_surface = pygame.Surface(npc_size, pygame.SRCALPHA)
            pygame.draw.ellipse(npc_surface, npc_def["color"], (10, 10, 40, 50))  # Head
            pygame.draw.rect(npc_surface, npc_def["color"], (15, 55, 30, 25))  # Body
            
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
        # 1. Coin Interaction
        coin = next((item for item in self.collectible_items if item['name'] == 'greed_coin'), None)
        if coin:
            interaction_rect = coin['rect'].inflate(80, 80)
            self.coin_interaction_area = InteractionArea(rect=interaction_rect, callback=self._on_coin_pickup)
            self.interaction_areas.append(self.coin_interaction_area)
            print(f"✅ Created interaction area around coin at {coin['position']}")
        
        # 2. NPC Interaction
        for npc in self.npcs:
            interaction_rect = npc['rect'].inflate(100, 100)
            callback = lambda npc_name=npc['name']: self._on_npc_interact(npc_name)
            self.interaction_areas.append(InteractionArea(rect=interaction_rect, callback=callback))

    def _on_coin_pickup(self) -> None:
        """Callback giả khi người chơi nhặt coin."""
        if not self.coin_collected:
            self.coin_collected = True
            print("💰 Đã nhặt được đồng xu tham lam! (Coin collected)")
            
            # Remove interaction area
            if hasattr(self, 'coin_interaction_area') and self.coin_interaction_area in self.interaction_areas:
                self.interaction_areas.remove(self.coin_interaction_area)
            
            # Remove visual
            self.collectible_items = [item for item in self.collectible_items if item['name'] != 'greed_coin']
    
    def _on_npc_interact(self, npc_name: str) -> None:
        """Callback giả khi người chơi tương tác với NPC."""
        print(f"💬 Đang nói chuyện với {npc_name}...")
        
        if npc_name == "NPC_1":
            print("Not done NPC_1")

    def set_player(self, player: object) -> None:
        """Sets the player reference and positions them for this scene."""
        super().set_player(player, start_pos=(900, 400))
