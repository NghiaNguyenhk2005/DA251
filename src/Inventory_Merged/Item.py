# items.py

class Item:
    def __init__(self, name, code, description, icon=None):
        self.name = name
        self.code = code
        self.description = description
        self.icon = icon  # Optional: path to image or sprite reference

    def __repr__(self):
        return f"Item({self.name}, {self.code})"

# Sample items
sticky_rice = Item(
    name="Sticky Rice Cake",
    code="4U4Y3",
    description=(
        "'T's side sticky rice cake. CT side always order this cake every round "
        "even if they got no money at all. 'T's good (t) but you'll need to add "
        "'k' ingredient before consume it. Also, be careful when eat it cuz "
        "some guy'll try fingers but hole..."
    )
)

flashbang = Item(
    name="Flashbang",
    code="FB01",
    description="Temporarily blinds enemies. Use with caution near teammates."
)

medkit = Item(
    name="Medkit",
    code="MED9",
    description="Restores health over time. Cannot be used while moving."
)

# Item registry
item_list = [sticky_rice, flashbang, medkit]