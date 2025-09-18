from npc import NPC

class Mentor(NPC):
    """
    Represents a mentor for an intern detective.
    """

    def __init__(self, name: str, expertise: str):
        super().__init__(name)
        self.expertise = expertise

    def guide(self, intern_name: str):
        return (
            f"{self.name}, an expert in {self.expertise}, "
            f"is guiding {intern_name} on their detective career path."
        )