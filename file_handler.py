# This module handles file input and output operations for saving and loading packing list data.

# Name of the data file used to store packing items
DATA_FILE = "packing_data.txt"


def save_data(items):
    """
    Save packing items into a text file
    Format:
    trip,category,name,packed
    """
     # Open the file in write mode (overwrites existing data)
    with open(DATA_FILE, "w", encoding="utf-8") as f:
     # Write each packing item into the file
        for item in items:
            line = (
                f"{item['trip']},"
                f"{item['category']},"
                f"{item['name']},"
                f"{item['packed']}\n"
            )
            f.write(line)


def load_data():
    """
    Load packing items from text file
    Return: list of dictionary
    """
    items = [] # List to store loaded packing items


    try:
        # Open the file in read mode
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            for line in f:
                # Split the line into individual fields
                trip, category, name, packed = line.strip().split(",")
                # Convert string 'True' / 'False' back to boolean
                items.append({
                    "trip": trip,
                    "category": category,
                    "name": name,
                    "packed": packed == "True"
                })

    except FileNotFoundError:
        # If the file does not exist, return an empty list
        # File not found = no saved data yet
        pass

    return items
