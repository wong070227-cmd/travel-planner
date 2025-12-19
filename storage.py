# storage.py
import os
from models import Trip, Accommodation, Activity
from helpers import get_dates_in_range

class StorageManager:
    def __init__(self):
        self._trips = []
        self.filename = "travel_data.txt"
        self.load_from_file()  # Auto-load on creation
    
    def auto_save(self):
        """Automatically save all data to file"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as file:
                trips = self.list_trips()
                
                if not trips:
                    file.write("No trips saved yet.\n")
                    return
                
                for trip in trips:
                    # Write trip info
                    file.write(f"TRIP|{trip.name}|{trip.destination}|{trip.travel_style}|"
                             f"{trip.start}|{trip.end}|{trip.duration}|{trip.created}\n")
                    
                    # Write accommodations
                    for acc in trip._accommodations:
                        file.write(f"ACC|{acc.type}|{acc.name}|{acc.address}|"
                                 f"{acc.check_in}|{acc.check_out}|{acc.confirmation}\n")
                    
                    # Write activities
                    for act in trip._activities:
                        file.write(f"ACT|{act.activity}|{act.date}|{act.time}|"
                                 f"{act.location}|{act.notes}\n")
                    
                    file.write("END\n")  # End marker for this trip
            
            print(f"Auto-saved {len(trips)} trip(s) to {self.filename}")
            
        except Exception as e:
            print(f"Auto-save error: {e}")
    
    def load_from_file(self):
        """Automatically load data from file on startup"""
        try:
            if not os.path.exists(self.filename):
                print(f"No save file found: {self.filename}")
                return
            
            with open(self.filename, 'r', encoding='utf-8') as file:
                lines = file.readlines()
            
            current_trip = None
            current_accommodations = []
            current_activities = []
            
            for line in lines:
                line = line.strip()
                if not line or line == "No trips saved yet.":
                    continue
                
                parts = line.split("|")
                
                if parts[0] == "TRIP" and len(parts) >= 8:
                    # Save previous trip if exists
                    if current_trip is not None:
                        current_trip._accommodations = current_accommodations
                        current_trip._activities = current_activities
                        self._trips.append(current_trip)
                    
                    # Create new trip
                    name = parts[1]
                    destination = parts[2]
                    travel_style = parts[3]
                    start = parts[4]
                    end = parts[5]
                    duration = int(parts[6])
                    created = parts[7]
                    
                    current_trip = Trip(name, destination, travel_style, start, end, duration, created)
                    current_accommodations = []
                    current_activities = []
                
                elif parts[0] == "ACC" and len(parts) >= 7:
                    acc_type = parts[1]
                    name = parts[2]
                    address = parts[3]
                    check_in = parts[4]
                    check_out = parts[5]
                    confirmation = parts[6] if len(parts) > 6 else ""
                    
                    acc = Accommodation(acc_type, name, address, check_in, check_out, confirmation)
                    current_accommodations.append(acc)
                
                elif parts[0] == "ACT" and len(parts) >= 6:
                    activity = parts[1]
                    date = parts[2]
                    time = parts[3]
                    location = parts[4]
                    notes = parts[5] if len(parts) > 5 else ""
                    
                    act = Activity(activity, date, time, location, notes)
                    current_activities.append(act)
                
                elif parts[0] == "END":
                    # Save the current trip
                    if current_trip is not None:
                        current_trip._accommodations = current_accommodations
                        current_trip._activities = current_activities
                        self._trips.append(current_trip)
                        current_trip = None
                        current_accommodations = []
                        current_activities = []
            
            # Save last trip if exists
            if current_trip is not None:
                current_trip._accommodations = current_accommodations
                current_trip._activities = current_activities
                self._trips.append(current_trip)
            
            print(f"Auto-loaded {len(self._trips)} trip(s) from {self.filename}")
            
        except Exception as e:
            print(f"Auto-load error: {e}")

    # Trip APIs
    def list_trips(self):
        return list(self._trips)

    def get_trip(self, name):
        for t in self._trips:
            if t.name.lower() == name.lower():
                return t
        return None

    def add_trip(self, trip, overwrite=False, allow_duplicate=False):
        if overwrite:
            # Remove any existing trip(s) with the same name
            self._trips = [t for t in self._trips if t.name != trip.name]
        elif not allow_duplicate:
            # Only block if duplicates not allowed
            existing = self.get_trip(trip.name)
            if existing:
                raise ValueError("Trip already exists")
        # Add trip
        self._trips.append(trip)
        self.auto_save()

    def update_trip(self, old_name, new_trip):
        """Update an existing trip"""
        old_trip = self.get_trip(old_name)
        if old_trip:
            # If name changed, we need to remove old and add new
            if old_name.lower() != new_trip.name.lower():
                self._trips.remove(old_trip)
                self._trips.append(new_trip)
            else:
                # Just update the existing trip's attributes
                idx = self._trips.index(old_trip)
                self._trips[idx] = new_trip
            self.auto_save()
            return True
        return False

    def remove_trip(self, name):
        t = self.get_trip(name)
        if t:
            self._trips.remove(t)
            self.auto_save()

    def trip_names(self):
        return [t.name for t in self._trips]

    # Accommodation delegates
    def add_accommodation(self, trip_name, acc):
        trip = self.get_trip(trip_name)
        if not trip:
            raise KeyError("Trip not found")
        trip.add_accommodation(acc)
        self.auto_save()
        
    def update_accommodation(self, trip_name, index, acc):
        """Update existing accommodation"""
        trip = self.get_trip(trip_name)
        if not trip:
            raise KeyError("Trip not found")
        trip.update_accommodation(index, acc)
        self.auto_save()

    def list_accommodations(self, trip_name):
        trip = self.get_trip(trip_name)
        return trip.list_accommodations() if trip else []

    def remove_accommodation(self, trip_name, index):
        trip = self.get_trip(trip_name)
        if trip:
            trip.remove_accommodation(index)
            self.auto_save()

    # Activity delegates
    def add_activity(self, trip_name, act):
        trip = self.get_trip(trip_name)
        if not trip:
            raise KeyError("Trip not found")
        trip.add_activity(act)
        self.auto_save()
        
    def update_activity(self, trip_name, index, act):
        """Update existing activity"""
        trip = self.get_trip(trip_name)
        if not trip:
            raise KeyError("Trip not found")
        trip.update_activity(index, act)
        self.auto_save()

    def list_activities(self, trip_name):
        trip = self.get_trip(trip_name)
        return trip.list_activities() if trip else []

    def remove_activity(self, trip_name, index):
        trip = self.get_trip(trip_name)
        if trip:
            trip.remove_activity(index)
            self.auto_save()