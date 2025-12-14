"""
Wrath Case Scene
================
Scene điều tra vụ án thịnh nộ - scene top-down với hệ thống va chạm.
Người chơi có thể di chuyển tự do để khám phá hiện trường vụ án.
"""

import pygame
from typing import List, Optional, Tuple, Dict, Any
from .base_scene import BaseScene
from src.utils.interaction_area import InteractionArea
from src.tools.Inventory_Item import wrath_woodpad, Item # <--- NEW IMPORT

class WrathCaseScene(BaseScene):
    """
    Wrath Case scene using BaseScene for core functionality.
    """
    
    def __init__(self, screen_width: int = 1280, screen_height: int = 720, game_system=None) -> None:
        """
        Initializes the Wrath Case Scene.
        """
        super().__init__(screen_width, screen_height)
        self.game_system = game_system # <--- STORE REFERENCE
        # Woodpad state (collectible specific to this scene)
        self.woodpad_collected: bool = False
        
        # Initialise standard assets
        self.setup_scene(
            background_path="assets/images/scenes/wrath-bg.png",
            wall_mask_path="assets/images/scenes/wrath-walls.png"
        )
        
        # Load specific scene objects
        self._load_obstacles()
        self._load_npcs()
        
        # Build standard components
        self.rebuild_collision_rects()
        self._setup_interaction_areas()
        
        # Fallback background if load failed (BaseScene handles placeholder, but we can customise colour)
        if self.background.get_at((0,0)) == (0,0,0,255): # Simple check if black default
             # Optional: set custom placeholder color if desired, e.g.
             # self.background.fill((40, 20, 20)) 
             pass

    def _load_obstacles(self) -> None:
        """Loads specific obstacles for Wrath Case."""
        # 1. NPC Obstacle
        try:
            npc_obstacle_img = pygame.image.load("assets/images/scenes/wrath-npc.png").convert_alpha()
            npc_obstacle_pos = (500, 500)
            original_size = npc_obstacle_img.get_size()
            new_size = original_size # Scale 1
            # Explicit scaling if needed, based on original code
            
            # Rect logic from original
            npc_obstacle_rect = pygame.Rect(npc_obstacle_pos[0], npc_obstacle_pos[1] + 20, 
                                           new_size[0] - 20, new_size[1] - 40)
            
            self.obstacles.append({
                'image': npc_obstacle_img,
                'position': npc_obstacle_pos,
                'rect': npc_obstacle_rect,
                'name': 'wrath_npc_obstacle'
            })
            print(f"✅ Loaded wrath-npc obstacle at {npc_obstacle_pos}")
        except (pygame.error, FileNotFoundError) as e:
            print(f"⚠️  Could not load wrath-npc obstacle: {e}")
        
        # 2. Woodpad (Collectible) - Added to collectible_items used in BaseScene if we want automatic drawing
        # OR we can keep it in a separate list if logic demands it, but BaseScene draw_with_player supports self.collectible_items
        try:
            woodpad_img = pygame.image.load("assets/images/scenes/wrath-woodpad.png").convert_alpha()
            woodpad_pos = (700, 500)
            woodpad_scale = 0.5
            original_size = woodpad_img.get_size()
            new_size = (int(original_size[0] * woodpad_scale), int(original_size[1] * woodpad_scale))
            woodpad_img_scaled = pygame.transform.scale(woodpad_img, new_size)
            
            woodpad_rect = pygame.Rect(woodpad_pos[0], woodpad_pos[1], new_size[0], new_size[1])
            
            self.collectible_items.append({
                'image': woodpad_img_scaled,
                'position': woodpad_pos,
                'rect': woodpad_rect,
                'name': 'wrath_woodpad'
            })
            print(f"✅ Loaded woodpad at {woodpad_pos}")
        except (pygame.error, FileNotFoundError) as e:
             print(f"⚠️  Could not load woodpad: {e}")
    
    def _load_npcs(self) -> None:
        """Loads NPCs for interaction."""
        npc_definitions = [
            {"name": "NPC_Angry_Victim", "pos": (100, 500), "color": (255, 100, 100)},
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
        # 1. Woodpad Area
        # Find woodpad in collectibles
        woodpad = next((item for item in self.collectible_items if item['name'] == 'wrath_woodpad'), None)
        if woodpad:
            interaction_rect = woodpad['rect'].inflate(80, 80)
            # We must use a separate variable or ID to know WHICH item to remove.
            # Using a simplified callback wrapper.
            self.woodpad_interaction_area = InteractionArea(rect=interaction_rect, callback=self._on_woodpad_pickup)
            self.interaction_areas.append(self.woodpad_interaction_area)
        
        # 2. NPC Areas
        for npc in self.npcs:
            interaction_rect = npc['rect'].inflate(100, 100)
            callback = lambda npc_name=npc['name']: self._on_npc_interact(npc_name)
            self.interaction_areas.append(InteractionArea(rect=interaction_rect, callback=callback))

    def _on_woodpad_pickup(self) -> None:
            """Callback khi người chơi nhặt woodpad."""
            if not self.woodpad_collected:
                
                # 1. Attempt to add the item to the central inventory
                # Thử thêm tấm gỗ vào kho đồ qua game_system
                if self.game_system and self.game_system.add_item_to_inventory(wrath_woodpad):
                    
                    # 2. If collection was successful, remove the item from the scene
                    self.woodpad_collected = True
                    print("🪵 Đã nhặt được tấm gỗ! (Woodpad collected)")

                    # Remove from scene
                    # A. Remove interaction area
                    if hasattr(self, 'woodpad_interaction_area') and self.woodpad_interaction_area in self.interaction_areas:
                        self.interaction_areas.remove(self.woodpad_interaction_area)
                    
                    # B. Remove visual item
                    # Filter the item out of the list of visible/collectible items
                    self.collectible_items = [item for item in self.collectible_items if item['name'] != 'wrath_woodpad']
                
                else:
                    # Optionally show a message that inventory is full
                    # In thông báo nếu không thể nhặt (ví dụ: kho đồ đầy)
                    print("❌ Cannot collect item. Inventory is full!")
    def _on_npc_interact(self, npc_name: str) -> None:
        """Callback khi người chơi tương tác với NPC."""
        print(f"💬 Đang nói chuyện với {npc_name}...")
        
        if npc_name == "NPC_Angry_Victim":
            print("   😡 Angry Victim: 'Hắn ta đã phá hủy mọi thứ của tôi! Tôi sẽ không tha thứ!'")
            print("   📝 TODO: Mở dialogue về nạn nhân và động cơ")
        elif npc_name == "NPC_Witness":
            print("   👁️ Witness: 'Tôi đã thấy một người đàn ông rất tức giận ở đây...'")

    def set_player(self, player: object) -> None:
        """Specific set_player override to set start position."""
        super().set_player(player, start_pos=(900, 400))


