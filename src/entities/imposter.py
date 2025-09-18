from npc import NPC

class Imposter(NPC):
    """
    Represents an imposter in a detective-style game.
    """

    def __init__(self, name: str, disguise: str):
        super().__init__(name, role="Imposter")
        self.disguise = disguise

    def interact(self, player):
        return f"{self.name} is pretending to be a {self.disguise}."