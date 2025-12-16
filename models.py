"""Data models for the Travel Assistant"""
class Activity:
    def __init__(self, activity, date, time="", location="", notes=""):
        self.activity = activity
        self.date = date
        self.time = time
        self.location = location
        self.notes = notes

class Accommodation:
    def __init__(self, type, name, address="", check_in="", check_out="", confirmation=""):
        self.type = type
        self.name = name
        self.address = address
        self.check_in = check_in
        self.check_out = check_out
        self.confirmation = confirmation

class Trip:
    def __init__(self, name, destination, travel_style, start, end, duration=0, created=""):
        self.name = name
        self.destination = destination
        self.travel_style = travel_style
        self.start = start
        self.end = end
        self.duration = duration
        self.created = created
        self._accommodations = []
        self._activities = []
        self._packing_items = []
        self._emergency_contacts = []

    def add_accommodation(self, acc):
        self._accommodations.append(acc)

    def list_accommodations(self):
        return list(self._accommodations)

    def remove_accommodation(self, index):
        if 0 <= index < len(self._accommodations):
            del self._accommodations[index]

    def add_activity(self, act):
        self._activities.append(act)

    def list_activities(self):
        return list(self._activities)

    def remove_activity(self, index):
        if 0 <= index < len(self._activities):
            del self._activities[index]