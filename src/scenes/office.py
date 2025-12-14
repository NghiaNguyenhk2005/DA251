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
from src.ui.suspect_selection_popup import SuspectSelectionPopup

class OfficeScene(BaseScene):
    """
    Office scene using BaseScene for core functionality.
    """
    
    def __init__(self, screen_width: int = 1280, screen_height: int = 720, on_scene_change=None) -> None:
        """
        Initializes the Office Scene.
        
        Args:
            screen_width: Width of the screen
            screen_height: Height of the screen
            on_scene_change: Callback function to change scenes (receives scene_id: str)
        """
        super().__init__(screen_width, screen_height)
        
        self.debug_mode = True
        self.on_scene_change = on_scene_change  # Store callback for scene changes

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
        
        # Suspect selection popup
        self.suspect_popup = SuspectSelectionPopup(screen_width, screen_height, self._on_suspect_selected)

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
        print("💡 Player pressed [F] near the chair. Showing suspect selection...")
        self.suspect_popup.show()
    
    def _on_suspect_selected(self, bg_scene: str) -> None:
        """Callback when a suspect is selected from the popup."""
        print(f"✅ Suspect selected with background: {bg_scene}")
        # Store the selected background to pass to interrogation
        self.selected_interrogation_bg = bg_scene
        if self.on_scene_change:
            self.on_scene_change("interrogation_room")

    def set_player(self, player: object) -> None:
        """Sets the player reference and positions them for this scene."""
        super().set_player(player, start_pos=(900, 400))
    
    def handle_event(self, event: pygame.event.Event) -> None:
        """Handle events, including popup."""
        # If popup is visible, let it handle events first
        if self.suspect_popup.visible:
            if self.suspect_popup.handle_event(event):
                return  # Event consumed by popup
        
        # Otherwise, handle normal scene events
        super().handle_event(event)
    
    def draw_with_player(self, screen: pygame.Surface, player: object) -> None:
        """Draw scene and popup."""
        # Draw normal scene
        super().draw_with_player(screen, player)
        
        # Draw popup on top
        self.suspect_popup.draw(screen)
