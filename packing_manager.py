from file_handler import save_data, load_data

# ---------- Encapsulation ----------
class PackingList:
    """
    Encapsulation: PackingList hides its internal data (_items) and exposes
    methods to interact with it safely. Users cannot directly modify _items
    from outside the class.
    """
    def __init__(self):
        # _items are private (conventionally, by leading underscore)
        # Load existing data from file when creating an instance
        self._items = load_data()  

    def add_item(self, trip, category, name):
        """Add a new item to the packing list"""
        self._items.append({
            "trip": trip,
            "category": category,
            "name": name,
            "packed": False # default status
        })
        self._save() # automatically save after modification

    def toggle_packed(self, index):
        """Toggle the packed status of an item by index"""
        self._items[index]["packed"] = not self._items[index]["packed"]
        self._save() # save changes

    def delete_item(self, index):
        """Remove an item by index"""
        self._items.pop(index)
        self._save() # save changes

    def get_items(self):
        """Return a copy of all items"""
        return self._items

    def calculate_progress(self):
        """Calculate percentage of packed items"""
        if self._items:
            packed = sum(1 for i in self._items if i["packed"])
            return int((packed / len(self._items)) * 100)
        return 0 # avoid division by zero if no items

    def _save(self):
         """
        Private method to save the current items to file.
        Users cannot call this directly (conventionally), ensuring
        controlled access to the data.
        """
        save_data(self._items) 


# ---------- Inheritance ----------
class TripPackingList(PackingList):
     """
    Inheritance: TripPackingList inherits all methods and attributes
    from PackingList, and adds extra functionality for trip-specific operations.
    """
    def get_items_for_trip(self, trip_name):
        """
        Return only the items belonging to a specific trip.
        Demonstrates extending functionality without rewriting base class.
        """
        return [i for i in self._items if i["trip"] == trip_name]
