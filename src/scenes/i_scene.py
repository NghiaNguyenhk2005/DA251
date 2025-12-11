from abc import ABC
import pygame

class IScene(ABC):
    def draw(self, screen: pygame.Surface):
        pass

    def update(self):
        pass

    def handle_event(self, event: pygame.event.Event):
        pass

    def check_collision(self, rect: pygame.Rect) -> bool:
        """
        Check if the given rect collides with any obstacles in the scene.
        Must be implemented by concrete classes.
        """
        return False

    def prevent_collision(self, player_rect: pygame.Rect, old_x: float, old_y: float) -> tuple:
        """
        Prevents player from passing through obstacles using sliding and deflection.
        Returns the safe (x, y) coordinates.
        """
        # 1. If no collision at target, all good.
        if not self.check_collision(player_rect):
            return player_rect.x, player_rect.y

        target_x = player_rect.x
        target_y = player_rect.y
        dx = target_x - old_x
        dy = target_y - old_y

        # Helper to check if a position is free
        def is_free(x, y):
            test_rect = player_rect.copy()
            test_rect.x = int(x)
            test_rect.y = int(y)
            return not self.check_collision(test_rect)

        # 2. Axis Separation (Standard Sliding)
        # Determine if we can move along X-only or Y-only
        can_move_x = False
        if abs(dx) > 0 and is_free(target_x, old_y):
            can_move_x = True

        can_move_y = False
        if abs(dy) > 0 and is_free(old_x, target_y):
            can_move_y = True

        # If we can move in one axis (slide), do it.
        # If both are possible (diagonal into void corner?), favor X for consistency or just return one.
        if can_move_x and can_move_y:
            return target_x, old_y # Favor X slide, or could use (target_x, target_y) but that was collision? No, is_free checks separate.
        
        if can_move_x:
            return target_x, old_y
        
        if can_move_y:
            return old_x, target_y

        # 3. Deflection (Diagonal Sliding against Walls)
        # If we are here, direct movement and single-axis movement failed (or wasn't attempted due to 0 delta).
        # This solves the "sticking" when moving straight into a diagonal wall.
        
        slide_step = 3 # pixels to nudge
        
        # If blocked on X (we tried to move X, but failed)
        if abs(dx) > 0:
            # Try sliding Y+ or Y- while damping X progress
            reduced_x = old_x + (dx * 0.5) # Allow half-step into the "wall" direction (will be corrected if blocked, but helps visual) -> Actually better to stay at old_x or slight push
            # Let's try pure slide at old_x first? No, we want to move ALONG wall.
            
            # Try sliding UP
            if is_free(old_x + (dx * 0.2), old_y - slide_step):
                return old_x + (dx * 0.2), old_y - slide_step
            # Try sliding DOWN
            if is_free(old_x + (dx * 0.2), old_y + slide_step):
                return old_x + (dx * 0.2), old_y + slide_step

        # If blocked on Y
        if abs(dy) > 0:
            # Try sliding LEFT
            if is_free(old_x - slide_step, old_y + (dy * 0.2)):
                return old_x - slide_step, old_y + (dy * 0.2)
            # Try sliding RIGHT
            if is_free(old_x + slide_step, old_y + (dy * 0.2)):
                return old_x + slide_step, old_y + (dy * 0.2)

        # 4. Fallback: Full Stop
        return old_x, old_y
