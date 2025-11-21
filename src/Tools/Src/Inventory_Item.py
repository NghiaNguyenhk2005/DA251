# Inventory_Item.py

# Item only stores data — no pygame image loading here.
# InventoryUI will load the sprite sheet and extract icons.

class Item:
    def __init__(self, name, code, description, icon_id):
        self.name = name
        self.code = code
        self.description = description
        self.icon_id = icon_id   # used later by InventoryUI

    def __repr__(self):
        return f"Item({self.name}, {self.code})"


# ---- DETECTIVE GAME ITEMS (9 total) ---------------------------------------

magnifying_glass = Item(
    name="Magnifying Glass",
    code="MAG2",
    description="Useful for spotting small details others overlook.",
    icon_id=0
)

crime_scene_tape = Item(
    name="Crime Scene Tape",
    code="CST3",
    description="Bright yellow tape used to secure areas. Smells like cheap plastic.",
    icon_id=1
)

evidence_bag = Item(
    name="Evidence Bag",
    code="EVD4",
    description="A sealed bag containing an unidentified object. Do not tamper.",
    icon_id=2
)

fingerprint_duster = Item(
    name="Fingerprint Duster",
    code="FPD5",
    description="Used to reveal fingerprints. Leaves black powder everywhere.",
    icon_id=3
)

voice_recorder = Item(
    name="Voice Recorder",
    code="REC6",
    description="Used to interview suspects. Battery life: unpredictable.",
    icon_id=4
)

old_key = Item(
    name="Rusty Key",
    code="KEY7",
    description="Found at a crime scene. Belongs to a lock long forgotten.",
    icon_id=5
)

pocket_watch = Item(
    name="Stopped Pocket Watch",
    code="PW8",
    description="Stopped at 11:47 PM. Possible time of crime?",
    icon_id=6
)

cigarette_butt = Item(
    name="Cigarette Butt",
    code="CB9",
    description="Left behind by someone at the scene. Menthol — unusual choice.",
    icon_id=7
)

mysterious_letter = Item(
    name="Mysterious Letter",
    code="LTRX",
    description="A handwritten note with no signature. The ink is still wet.",
    icon_id=8
)

# ---- Registry --------------------------------------------------------------

item_list = [
    magnifying_glass,
    crime_scene_tape,
    evidence_bag,
    fingerprint_duster,
    voice_recorder,
    old_key,
    pocket_watch,
    cigarette_butt,
    mysterious_letter
]
