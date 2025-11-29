from abc import ABC, abstractmethod

class Player(ABC):
    def __init__(self, name: str):
        self.name = name
        self.score = 0
        self.wallet = 0
        self.health = 3
        self.bag = []
        self.skin = "default"

    @abstractmethod
    def make_decision(self, choice):
        """Make a decision based on the player's choice."""
        pass

    @abstractmethod
    def update_score(self, points: int):
        """Update the player's score."""
        pass

    @abstractmethod
    def update_health(self, amount: int):
        """Update the player's health."""
        pass

    @abstractmethod
    def update_wallet(self, amount: int):
        """Update the player's wallet."""
        pass

    @abstractmethod
    def add_bag(self, item: str):
        """Add an item to the player's bag."""
        pass

    @abstractmethod
    def remove_bag(self, item: str):
        """Remove an item from the player's bag."""
        pass

    @abstractmethod
    def change_skin(self, skin: str):
        """Change the player's skin."""
        pass

    @abstractmethod
    def interact(self, entity):
        """Interact with another entity in the game."""
        pass
