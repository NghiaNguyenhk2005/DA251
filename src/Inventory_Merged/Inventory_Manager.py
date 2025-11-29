# inventory_manager.py

class InventoryManager:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.max_slots = rows * cols
        self.items = [None] * self.max_slots

    def add_item(self, item, index=None):
        """Add item to a specific slot or first available slot."""
        if index is not None and 0 <= index < self.max_slots:
            self.items[index] = item
            return True
        for i in range(self.max_slots):
            if self.items[i] is None:
                self.items[i] = item
                return True
        return False  # Inventory full

    def remove_item(self, index):
        """Remove item from a specific slot."""
        if 0 <= index < self.max_slots:
            self.items[index] = None
            return True
        return False

    def get_item(self, index):
        """Get item from a specific slot."""
        if 0 <= index < self.max_slots:
            return self.items[index]
        return None

    def clear_inventory(self):
        """Remove all items."""
        self.items = [None] * self.max_slots

    def get_all_items(self):
        """Return all items in inventory."""
        return self.items