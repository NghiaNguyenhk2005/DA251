from npc import NPC
class Witness(NPC):
    """
    Represents a witness in a detective-style game.
    """

    def __init__(self, name: str, testimony: str):
        super().__init__(name, role="Witness")
        self.testimony = testimony

    def interact(self, player):
        return f"{self.name} says: '{self.testimony}'"