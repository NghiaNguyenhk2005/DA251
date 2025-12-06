from abc import abstractmethod
from typing import Protocol
import pygame

class Drawable(Protocol):
    @abstractmethod
    def draw(self, screen: pygame.Surface):
        pass

class Updatable(Protocol):

    @abstractmethod
    def update(self, delta_time: float = 0):
        pass

    @abstractmethod
    def handle_event(self, event: pygame.event.Event):
        pass

class DrawAndUpdateAble(Drawable, Updatable, Protocol):
    pass
