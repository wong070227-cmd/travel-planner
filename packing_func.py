from packing_manager import TripPackingList

# Initialize the packing list manager
# This object manages all packing items and handles data operations
manager = TripPackingList()

def add_item(trip, category, name):
    """
    Add a new item to the packing list.

    Parameters:
        trip (str): Name of the trip
        category (str): Category of the item
        name (str): Name of the packing item
    """
    manager.add_item(trip, category, name)

def toggle_packed(index):
    """
    Toggle the packed status of an item.

    Parameters:
        index (int): Index of the selected item in the list
    """
    manager.toggle_packed(index)

def delete_item(index):
    """
    Remove an item from the packing list.

    Parameters:
        index (int): Index of the item to be deleted
    """
    manager.delete_item(index)

def get_items():
    """
    Retrieve all packing items.

    Returns:
        list: A list of packing item dictionaries
    """
    return manager.get_items()

def calculate_progress():
    """
    Calculate the packing progress.

    Returns:
        int: Percentage of items marked as packed
    """
    return manager.calculate_progress()
