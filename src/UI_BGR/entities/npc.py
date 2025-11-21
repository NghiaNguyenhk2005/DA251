from abc import ABC, abstractmethod

class NPC(ABC):
    """
    Abstract base class for all NPCs in a detective-style game.
    """

    def __init__(self, name: str, role: str):
        self.name = name
        self.role = role
        self.invinsible = False

    @abstractmethod
    def interact(self, player):
        """
        Define how the NPC interacts with the player.
        """
        pass