"""
Office Scene
============
Văn phòng chính - scene top-down với hệ thống va chạm.
Người chơi có thể di chuyển tự do nhưng không thể đi xuyên qua các vật cản.
"""

import pygame
from typing import List, Optional, Tuple, Dict, Any
from .base_scene import BaseScene
from src.utils.interaction_area import InteractionArea

class OfficeScene(BaseScene):
    """
    Office scene using BaseScene for core functionality.
    """
    
    def __init__(self, screen_width: int = 1280, screen_height: int = 720) -> None:
        """
        Initializes the Office Scene.
        """
        super().__init__(screen_width, screen_height)
        
        self.debug_mode = True

        # Setup standard assets
        self.setup_scene(
            background_path="assets/images/scenes/office-bg.jpg",
            wall_mask_path="assets/images/scenes/office-walls.png"
        )
        
        # Fallback background
        if self.background.get_at((0,0)) == (0,0,0,255):
             self.background.fill((40, 40, 50))

        # Load Scene Objects
        self._load_obstacles()
        
        # Build Standard Components
        self.rebuild_collision_rects()
        self._setup_interaction_areas()

    def _load_obstacles(self) -> None:
        """Loads the drawable obstacle objects (chairs)."""
        obstacle_definitions = [
            {"path": "assets/images/scenes/office-chair1.png", "pos": (220, 300), "scale": 1.3},
            {"path": "assets/images/scenes/office-chair2.png", "pos": (self.screen_width//2-100, 240), "scale": 1.3},
            {"path": "assets/images/scenes/office-chair3.png", "pos": (self.screen_width//2, self.screen_height//2 + 150), "scale": 1.3},
        ]
        
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
                print(f"✅ Loaded obstacle: {obs_def['path']}")
            except (pygame.error, FileNotFoundError) as e:
                print(f"⚠️  Could not load {obs_def['path']}: {e}")
                continue

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
        super().set_player(player, start_pos=(900, 400))
