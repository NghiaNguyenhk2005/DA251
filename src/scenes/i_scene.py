from abc import ABC
import pygame

class IScene(ABC):
    def draw(self, screen: pygame.Surface):
        pass

    def update(self):
        pass

    def handle_event(self, event: pygame.event.Event):
        pass
