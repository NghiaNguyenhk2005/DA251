# Inventory_Item.py

# Item only stores data — no pygame image loading here.
# InventoryUI will load the sprite sheet and extract icons.

class Item:
    def __init__(self, name, code, description, item_icon_path):
        self.name = name
        self.code = code
        self.description = description
        #self.icon_id = icon_id   # used later by InventoryUI
        self.item_icon_path = item_icon_path
    def __repr__(self):
        return f"Item({self.name}, {self.code})"

envy_mask = Item(
    name="Envy Mask",
    code="EMASK1",
    description="A distinctive green mask found at the crime scene. A key piece of evidence.",
    #icon_id=1 # Use an available icon ID (assuming one is available)
    item_icon_path="assets/inventory/UI_Item_Icon/envy-mask.png"
)

greed_coin = Item(
    name="Greed Coin",
    code="GCOIN1",
    description="A shiny gold coin symbolizing greed. Found in the Greed Case scene.",
    #icon_id=2 # Use an available icon ID (assuming one is available)
    item_icon_path="assets/inventory/UI_Item_Icon/greed-coin.png"
)

wrath_woodpad = Item(
    name="Woodpad",
    code="WDPAD1",
    description="A wooden notepad used by the victim to jot down clues. Found in the Wrath Case scene.",
    #icon_id=3 # Use an available icon ID (assuming one is available)    
    item_icon_path="assets/inventory/UI_Item_Icon/wrath-woodpad.png"
)

# ---- Registry --------------------------------------------------------------

item_list = []
