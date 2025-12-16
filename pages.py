"""Travel Assistant - All Pages Combined"""
import tkinter as tk
from tkinter import messagebox, ttk, scrolledtext
from datetime import datetime, timedelta
from models import Activity, Accommodation, Trip
from helpers import generate_date_display, get_dates_in_range

# BASE PAGE
class BasePage:
    def __init__(self, root, bg_color):
        self.root = root
        self.frame = tk.Frame(root, bg=bg_color)
        self.bg_color = bg_color

    def show(self):
        self.frame.pack(fill="both", expand=True)

    def hide(self):
        self.frame.pack_forget()

    def refresh(self):
        pass

# ADD TRIP PAGE
class AddTripPage(BasePage):
    def __init__(self, root, storage, bg_color, frame_bg, button_bg, button_fg, title_bg, back_callback):
        super().__init__(root, bg_color)
        self.storage = storage
        self.back_callback = back_callback
        self._build_ui(frame_bg, button_bg, button_fg, title_bg)

    def _build_ui(self, frame_bg, button_bg, button_fg, title_bg):
        tk.Label(self.frame, text="🎭 Add Trip", font=("Arial", 20, "bold"), 
                 bg=title_bg, fg="white", padx=20, pady=10).pack(fill="x", pady=(0, 20))
        
        main = tk.Frame(self.frame, bg=frame_bg, relief="solid", bd=1)
        main.pack(fill="both", expand=True, padx=20, pady=10)
        
        left = tk.Frame(main, bg=frame_bg, padx=20, pady=20)
        left.pack(side="left", fill="both", expand=True)
        
        right = tk.Frame(main, bg=frame_bg, padx=20, pady=20)
        right.pack(side="right", fill="both", expand=True)

        tk.Label(left, text="Trip Name:", font=("Arial", 11, "bold"), bg=frame_bg).pack(anchor="w", pady=(0, 5))
        self._trip_name = tk.Entry(left, font=("Arial", 11))
        self._trip_name.pack(fill="x", pady=(0, 10))
        
        tk.Label(left, text="Destination:", font=("Arial", 11, "bold"), bg=frame_bg).pack(anchor="w", pady=(0, 5))
        self._destination = tk.Entry(left, font=("Arial", 11))
        self._destination.pack(fill="x", pady=(0, 10))
        
        tk.Label(left, text="Travel Style:", font=("Arial", 11, "bold"), bg=frame_bg).pack(anchor="w", pady=(0, 5))
        self._style = ttk.Combobox(left, values=["Leisure","Business","Adventure","Family","Romantic"], 
                                 font=("Arial", 11), state="readonly")
        self._style.set("Leisure")
        self._style.pack(fill="x", pady=(0, 10))

        tk.Label(left, text="Start Date (YYYY-MM-DD):", font=("Arial", 11, "bold"), bg=frame_bg).pack(anchor="w", pady=(0, 5))
        self._start = tk.Entry(left, font=("Arial", 11))
        self._start.pack(fill="x", pady=(0, 10))
        self._start.bind("<FocusOut>", lambda e: self._calculate_duration())

        tk.Label(left, text="End Date (YYYY-MM-DD):", font=("Arial", 11, "bold"), bg=frame_bg).pack(anchor="w", pady=(0, 5))
        self._end = tk.Entry(left, font=("Arial", 11))
        self._end.pack(fill="x", pady=(0, 10))
        self._end.bind("<FocusOut>", lambda e: self._calculate_duration())

        self._duration_label = tk.Label(left, text="Trip Duration: 0 day(s)", font=("Arial", 10, "italic"), bg=frame_bg, fg="#2c3e50")
        self._duration_label.pack(anchor="w", pady=(10, 5))

        quick_frame = tk.Frame(left, bg=frame_bg)
        quick_frame.pack(fill="x", pady=(10, 0))
        tk.Label(quick_frame, text="Quick Dates:", font=("Arial", 10), bg=frame_bg).pack(side="left", padx=(0, 10))
        
        quick_dates = [("Tomorrow", 1), ("In 3 days", 3), ("Next week", 7), ("In 2 weeks", 14)]
        for label, days in quick_dates:
            btn = tk.Button(quick_frame, text=label, font=("Arial", 9),
                           command=lambda d=days: self._set_quick_date(d))
            btn.pack(side="left", padx=2)

        tk.Button(left, text="💾 Save Trip", bg=button_bg, fg=button_fg,
                 font=("Arial", 10), command=self.save).pack(pady=20)

        tk.Label(right, text="Saved Trips:", font=("Arial", 12, "bold"), bg=frame_bg).pack(anchor="w", pady=(0, 10))
        self._listbox = tk.Listbox(right, font=("Arial", 10), height=15)
        self._listbox.pack(fill="both", expand=True)

        bframe = tk.Frame(right, bg=frame_bg)
        bframe.pack(fill="x", pady=(10, 0))
        
        tk.Button(bframe, text="🗑️ Delete Selected", bg="#d9534f", fg="white",
                 font=("Arial", 9), command=self.delete).pack(side="left", padx=5)

        tk.Button(self.frame, text="🔙 Back", bg=button_bg, fg=button_fg,
                 font=("Arial", 10), command=self.back_callback).pack(pady=10)

    def _calculate_duration(self):
        try:
            start = self._start.get().strip()
            end = self._end.get().strip()
            if start and end:
                s = datetime.strptime(start, "%Y-%m-%d")
                e = datetime.strptime(end, "%Y-%m-%d")
                if e >= s:
                    duration = (e - s).days + 1
                    self._duration_label.config(text=f"Trip Duration: {duration} day(s)")
                    return duration
                else:
                    self._duration_label.config(text="End date must be after start date")
                    return None
        except ValueError:
            self._duration_label.config(text="Invalid date format")
            return None
        return None

    def _set_quick_date(self, days_from_now):
        new_date = datetime.now() + timedelta(days=days_from_now)
        self._start.delete(0, tk.END)
        self._start.insert(0, new_date.strftime("%Y-%m-%d"))
        self._end.delete(0, tk.END)
        self._end.insert(0, (new_date + timedelta(days=2)).strftime("%Y-%m-%d"))
        self._calculate_duration()

    def clear(self):
        self._trip_name.delete(0, tk.END)
        self._destination.delete(0, tk.END)
        self._style.set("Leisure")
        self._start.delete(0, tk.END)
        self._end.delete(0, tk.END)
        self._duration_label.config(text="Trip Duration: 0 day(s)")

    def save(self):
        name = self._trip_name.get().strip()
        dest = self._destination.get().strip()
        style = self._style.get()
        start = self._start.get().strip()
        end = self._end.get().strip()
        
        if not name or not dest or not start or not end:
            messagebox.showerror("Error", "Please fill required fields")
            return
        
        try:
            s = datetime.strptime(start, "%Y-%m-%d")
            e = datetime.strptime(end, "%Y-%m-%d")
            if e < s:
                messagebox.showerror("Error", "End date must be after start date")
                return
            duration = (e - s).days + 1
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD")
            return
        
        trip = Trip(name=name, destination=dest, travel_style=style, 
                   start=start, end=end, duration=duration,
                   created=datetime.now().strftime("%Y-%m-%d %H:%M"))
        
        try:
            existing = self.storage.get_trip(name)
            if existing:
                if not messagebox.askyesno("Duplicate", f"Trip '{name}' already exists. Overwrite?"):
                    return
                self.storage.add_trip(trip, overwrite=True)
            else:
                self.storage.add_trip(trip)
            
            messagebox.showinfo("Success", f"Trip '{name}' saved successfully!")
            self.clear()
            self._update_trip_list()
            
        except ValueError as ex:
            messagebox.showerror("Error", str(ex))

    def delete(self):
        sel = self._listbox.curselection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select a trip to delete")
            return
        
        trip_name = self._listbox.get(sel[0])
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete trip '{trip_name}'?"):
            self.storage.remove_trip(trip_name)
            self._update_trip_list()

    def _update_trip_list(self):
        self._listbox.delete(0, tk.END)
        for trip in self.storage.list_trips():
            self._listbox.insert(tk.END, trip.name)

    def refresh(self):
        self._update_trip_list()

# ADD ACCOMMODATION PAGE
class AddAccommodationPage(BasePage):
    def __init__(self, root, storage, bg_color, frame_bg, button_bg, button_fg, title_bg, back_callback):
        super().__init__(root, bg_color)
        self.storage = storage
        self.back_callback = back_callback
        self.current_trip = None
        self._build_ui(frame_bg, button_bg, button_fg, title_bg)

    def _build_ui(self, frame_bg, button_bg, button_fg, title_bg):
        tk.Label(self.frame, text="🏨 Add Accommodation", font=("Arial", 20, "bold"), 
                 bg=title_bg, fg="white", padx=20, pady=10).pack(fill="x", pady=(0, 20))
        
        main = tk.Frame(self.frame, bg=frame_bg, relief="solid", bd=1)
        main.pack(fill="both", expand=True, padx=20, pady=10)
        
        left = tk.Frame(main, bg=frame_bg, padx=20, pady=20)
        left.pack(side="left", fill="both", expand=True)
        
        right = tk.Frame(main, bg=frame_bg, padx=20, pady=20)
        right.pack(side="right", fill="both", expand=True)

        tk.Label(left, text="Select Trip:", font=("Arial", 11, "bold"), bg=frame_bg).pack(anchor="w", pady=(0, 5))
        self._trip_combo = ttk.Combobox(left, state="readonly", font=("Arial", 11))
        self._trip_combo.pack(fill="x", pady=(0, 15))
        self._trip_combo.bind("<<ComboboxSelected>>", lambda e: self._on_trip_selected())

        tk.Label(left, text="Type:", font=("Arial", 11, "bold"), bg=frame_bg).pack(anchor="w", pady=(0, 5))
        self._type = ttk.Combobox(left, values=["Hotel","Hostel","Airbnb","Resort","Camping","Other"], 
                                font=("Arial", 11), state="readonly")
        self._type.set("Hotel")
        self._type.pack(fill="x", pady=(0, 10))
        
        tk.Label(left, text="Name:", font=("Arial", 11, "bold"), bg=frame_bg).pack(anchor="w", pady=(0, 5))
        self._name = tk.Entry(left, font=("Arial", 11))
        self._name.pack(fill="x", pady=(0, 10))
        
        tk.Label(left, text="Address:", font=("Arial", 11, "bold"), bg=frame_bg).pack(anchor="w", pady=(0, 5))
        self._address = tk.Entry(left, font=("Arial", 11))
        self._address.pack(fill="x", pady=(0, 10))
        
        tk.Label(left, text="Confirmation #:", font=("Arial", 11, "bold"), bg=frame_bg).pack(anchor="w", pady=(0, 5))
        self._confirmation = tk.Entry(left, font=("Arial", 11))
        self._confirmation.pack(fill="x", pady=(0, 10))
        
        # Date selection frame
        date_frame = tk.Frame(left, bg=frame_bg)
        date_frame.pack(fill="x", pady=(10, 0))
        
        tk.Label(date_frame, text="Trip Dates:", font=("Arial", 11, "bold"), bg=frame_bg).pack(anchor="w", pady=(0, 5))
        
        self._date_info_label = tk.Label(date_frame, text="No trip selected", 
                                       font=("Arial", 9), bg=frame_bg, fg="#666")
        self._date_info_label.pack(anchor="w", pady=(0, 10))
        
        # Check-in/out frame
        check_frame = tk.Frame(left, bg=frame_bg)
        check_frame.pack(fill="x", pady=(0, 10))
        
        # Check-in
        tk.Label(check_frame, text="Check-in:", font=("Arial", 11, "bold"), bg=frame_bg).grid(row=0, column=0, sticky="w", pady=(0, 5))
        self._cin_combo = ttk.Combobox(check_frame, state="readonly", font=("Arial", 10), width=15)
        self._cin_combo.grid(row=1, column=0, sticky="w", padx=(0, 10))
        
        # Check-out
        tk.Label(check_frame, text="Check-out:", font=("Arial", 11, "bold"), bg=frame_bg).grid(row=0, column=1, sticky="w", pady=(0, 5))
        self._cout_combo = ttk.Combobox(check_frame, state="readonly", font=("Arial", 10), width=15)
        self._cout_combo.grid(row=1, column=1, sticky="w")
        
        tk.Button(left, text="💾 Save Accommodation", bg=button_bg, fg=button_fg,
                 font=("Arial", 10), command=self.save).pack(pady=5)

        tk.Label(right, text="Saved Accommodations:", font=("Arial", 12, "bold"), bg=frame_bg).pack(anchor="w", pady=(0, 10))
        self._listbox = tk.Listbox(right, font=("Arial", 10), height=15)
        self._listbox.pack(fill="both", expand=True)

        bframe = tk.Frame(right, bg=frame_bg)
        bframe.pack(fill="x", pady=(10, 0))
        
        tk.Button(bframe, text="🗑️ Delete Selected", bg="#d9534f", fg="white",
                 font=("Arial", 9), command=self.delete).pack(side="left", padx=5)

        tk.Button(self.frame, text="🔙 Back", bg=button_bg, fg=button_fg,
                 font=("Arial", 10), command=self.back_callback).pack(pady=10)

    def _on_trip_selected(self):
        trip_name = self._trip_combo.get()
        if trip_name:
            self.current_trip = self.storage.get_trip(trip_name)
            if self.current_trip:
                self._update_date_info()
                self._populate_date_combos()
                self.load()
            else:
                self._date_info_label.config(text="Trip not found")
                self._cin_combo.set('')
                self._cout_combo.set('')
                self._cin_combo['values'] = []
                self._cout_combo['values'] = []

    def _update_date_info(self):
        if self.current_trip:
            start_display = generate_date_display(self.current_trip.start)
            end_display = generate_date_display(self.current_trip.end)
            self._date_info_label.config(
                text=f"{start_display} to {end_display} ({self.current_trip.duration} days)"
            )

    def _populate_date_combos(self):
        if self.current_trip:
            dates = get_dates_in_range(self.current_trip.start, self.current_trip.end)
            
            display_dates = []
            for date_str in dates:
                display = generate_date_display(date_str)
                display_dates.append(f"{date_str} - {display}")
            
            self._cin_combo['values'] = display_dates
            self._cout_combo['values'] = display_dates
            
            if dates:
                self._cin_combo.set(display_dates[0])
                if len(dates) > 1:
                    self._cout_combo.set(display_dates[-1])
                else:
                    self._cout_combo.set(display_dates[0])

    def _get_date_from_display(self, display_str):
        if display_str and " - " in display_str:
            return display_str.split(" - ")[0]
        return ""

    def refresh(self):
        names = self.storage.trip_names()
        self._trip_combo['values'] = names
        if names:
            self._trip_combo.set(names[0])
            self._on_trip_selected()
        else:
            self._trip_combo.set("")
            self._date_info_label.config(text="No trip selected")
            self._listbox.delete(0, tk.END)

    def load(self):
        self._listbox.delete(0, tk.END)
        trip = self._trip_combo.get()
        if not trip:
            return
        for acc in self.storage.list_accommodations(trip):
            display = f"{acc.type}: {acc.name} ({acc.check_in} to {acc.check_out})"
            self._listbox.insert(tk.END, display)

    def save(self):
        trip = self._trip_combo.get().strip()
        if not trip:
            messagebox.showerror("Error", "Please select a trip")
            return
        
        acc_type = self._type.get()
        name = self._name.get().strip()
        address = self._address.get().strip()
        
        cin_display = self._cin_combo.get()
        cout_display = self._cout_combo.get()
        
        cin = self._get_date_from_display(cin_display)
        cout = self._get_date_from_display(cout_display)
        
        confirmation = self._confirmation.get().strip()
        
        if not name:
            messagebox.showerror("Error", "Please enter accommodation name")
            return
        if not cin:
            messagebox.showerror("Error", "Please select check-in date")
            return
        if not cout:
            messagebox.showerror("Error", "Please select check-out date")
            return
        
        try:
            cin_date = datetime.strptime(cin, "%Y-%m-%d")
            cout_date = datetime.strptime(cout, "%Y-%m-%d")
            if cout_date < cin_date:
                messagebox.showerror("Error", "Check-out date must be after check-in date")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid date format")
            return
        
        acc = Accommodation(type=acc_type, name=name, address=address, 
                           check_in=cin, check_out=cout, confirmation=confirmation)
        
        try:
            self.storage.add_accommodation(trip, acc)
            messagebox.showinfo("Success", "Accommodation added successfully!")
            self._name.delete(0, tk.END)
            self._address.delete(0, tk.END)
            self._confirmation.delete(0, tk.END)
            self.load()
            
        except KeyError as e:
            messagebox.showerror("Error", str(e))

    def delete(self):
        sel = self._listbox.curselection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select an accommodation to delete")
            return
        
        trip = self._trip_combo.get().strip()
        if not trip:
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this accommodation?"):
            self.storage.remove_accommodation(trip, sel[0])
            self.load()

# ADD ACTIVITIES PAGE
class AddActivitiesPage(BasePage):
    def __init__(self, root, storage, bg_color, frame_bg, button_bg, button_fg, title_bg, back_callback):
        super().__init__(root, bg_color)
        self.storage = storage
        self.back_callback = back_callback
        self.current_trip = None
        self._build_ui(frame_bg, button_bg, button_fg, title_bg)

    def _build_ui(self, frame_bg, button_bg, button_fg, title_bg):
        tk.Label(self.frame, text="🎭 Add Activities", font=("Arial", 20, "bold"), 
                 bg=title_bg, fg="white", padx=20, pady=10).pack(fill="x", pady=(0, 20))
        
        main = tk.Frame(self.frame, bg=frame_bg, relief="solid", bd=1)
        main.pack(fill="both", expand=True, padx=20, pady=10)
        
        left = tk.Frame(main, bg=frame_bg, padx=20, pady=20)
        left.pack(side="left", fill="both", expand=True)
        
        right = tk.Frame(main, bg=frame_bg, padx=20, pady=20)
        right.pack(side="right", fill="both", expand=True)

        tk.Label(left, text="Select Trip:", font=("Arial", 11, "bold"), bg=frame_bg).pack(anchor="w", pady=(0, 5))
        self._trip_combo = ttk.Combobox(left, state="readonly", font=("Arial", 11))
        self._trip_combo.pack(fill="x", pady=(0, 15))
        self._trip_combo.bind("<<ComboboxSelected>>", lambda e: self._on_trip_selected())

        tk.Label(left, text="Activity:", font=("Arial", 11, "bold"), bg=frame_bg).pack(anchor="w", pady=(0, 5))
        self._activity = tk.Entry(left, font=("Arial", 11))
        self._activity.pack(fill="x", pady=(0, 10))
        
        # Date selection area
        date_frame = tk.Frame(left, bg=frame_bg)
        date_frame.pack(fill="x", pady=(10, 0))
        
        tk.Label(date_frame, text="Select Date:", font=("Arial", 11, "bold"), bg=frame_bg).pack(anchor="w", pady=(0, 5))
        
        self._date_info_label = tk.Label(date_frame, text="No trip selected", 
                                       font=("Arial", 9), bg=frame_bg, fg="#666")
        self._date_info_label.pack(anchor="w", pady=(0, 10))
        
        # Date combo with display format
        self._date_combo = ttk.Combobox(left, state="readonly", font=("Arial", 10))
        self._date_combo.pack(fill="x", pady=(0, 10))
        
        # Day navigation buttons
        nav_frame = tk.Frame(left, bg=frame_bg)
        nav_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(nav_frame, text="Navigate:", font=("Arial", 10), bg=frame_bg).pack(side="left", padx=(0, 10))
        
        tk.Button(nav_frame, text="← Previous Day", font=("Arial", 8),
                 command=self._previous_day).pack(side="left", padx=2)
        tk.Button(nav_frame, text="Next Day →", font=("Arial", 8),
                 command=self._next_day).pack(side="left", padx=2)
        tk.Button(nav_frame, text="Today in Trip", font=("Arial", 8),
                 command=self._set_trip_start).pack(side="left", padx=2)
        
        tk.Label(left, text="Time (Optional):", font=("Arial", 11, "bold"), bg=frame_bg).pack(anchor="w", pady=(0, 5))
        self._time = tk.Entry(left, font=("Arial", 11), width=10)
        self._time.pack(fill="x", pady=(0, 10))
        
        # Time suggestions
        time_suggest_frame = tk.Frame(left, bg=frame_bg)
        time_suggest_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(time_suggest_frame, text="Quick Times:", font=("Arial", 9), bg=frame_bg).pack(side="left", padx=(0, 10))
        
        time_suggestions = ["09:00", "10:00", "12:00", "14:00", "16:00", "18:00", "20:00"]
        for time_str in time_suggestions:
            btn = tk.Button(time_suggest_frame, text=time_str, font=("Arial", 7),
                          command=lambda t=time_str: self._set_time(t))
            btn.pack(side="left", padx=1)
        
        tk.Label(left, text="Location (Optional):", font=("Arial", 11, "bold"), bg=frame_bg).pack(anchor="w", pady=(0, 5))
        self._location = tk.Entry(left, font=("Arial", 11))
        self._location.pack(fill="x", pady=(0, 10))
        
        tk.Label(left, text="Notes (Optional):", font=("Arial", 11, "bold"), bg=frame_bg).pack(anchor="w", pady=(0, 5))
        self._notes = tk.Entry(left, font=("Arial", 11))
        self._notes.pack(fill="x", pady=(0, 15))
        
        tk.Button(left, text="💾 Save Activity", bg=button_bg, fg=button_fg,
                 font=("Arial", 10), command=self.save).pack(pady=5)

        tk.Label(right, text="Saved Activities:", font=("Arial", 12, "bold"), bg=frame_bg).pack(anchor="w", pady=(0, 10))
        self._listbox = tk.Listbox(right, font=("Arial", 10), height=15)
        self._listbox.pack(fill="both", expand=True)

        bframe = tk.Frame(right, bg=frame_bg)
        bframe.pack(fill="x", pady=(10, 0))
        
        tk.Button(bframe, text="🗑️ Delete Selected", bg="#d9534f", fg="white",
                 font=("Arial", 9), command=self.delete).pack(side="left", padx=5)

        tk.Button(self.frame, text="🔙 Back", bg=button_bg, fg=button_fg,
                 font=("Arial", 10), command=self.back_callback).pack(pady=10)

    def _on_trip_selected(self):
        trip_name = self._trip_combo.get()
        if trip_name:
            self.current_trip = self.storage.get_trip(trip_name)
            if self.current_trip:
                self._update_date_info()
                self._populate_date_combo()
                self.load()
            else:
                self._date_info_label.config(text="Trip not found")
                self._date_combo.set('')
                self._date_combo['values'] = []

    def _update_date_info(self):
        if self.current_trip:
            start_display = generate_date_display(self.current_trip.start)
            end_display = generate_date_display(self.current_trip.end)
            self._date_info_label.config(
                text=f"Trip: {start_display} to {end_display}"
            )

    def _populate_date_combo(self):
        if self.current_trip:
            dates = get_dates_in_range(self.current_trip.start, self.current_trip.end)
            
            display_dates = []
            for i, date_str in enumerate(dates, 1):
                display = generate_date_display(date_str)
                display_dates.append(f"Day {i}: {date_str} - {display}")
            
            self._date_combo['values'] = display_dates
            
            if display_dates:
                self._date_combo.set(display_dates[0])

    def _get_date_from_display(self, display_str):
        if display_str and " - " in display_str:
            parts = display_str.split(" - ")
            if len(parts) > 1:
                date_part = parts[0].split(": ")[1] if ": " in parts[0] else parts[0]
                return date_part
        return ""

    def _previous_day(self):
        current = self._date_combo.get()
        if current and self._date_combo['values']:
            values = list(self._date_combo['values'])
            current_index = values.index(current) if current in values else -1
            if current_index > 0:
                self._date_combo.set(values[current_index - 1])

    def _next_day(self):
        current = self._date_combo.get()
        if current and self._date_combo['values']:
            values = list(self._date_combo['values'])
            current_index = values.index(current) if current in values else -1
            if current_index < len(values) - 1:
                self._date_combo.set(values[current_index + 1])

    def _set_trip_start(self):
        if self._date_combo['values']:
            self._date_combo.set(self._date_combo['values'][0])

    def _set_time(self, time_str):
        self._time.delete(0, tk.END)
        self._time.insert(0, time_str)

    def refresh(self):
        names = self.storage.trip_names()
        self._trip_combo['values'] = names
        if names:
            self._trip_combo.set(names[0])
            self._on_trip_selected()
        else:
            self._trip_combo.set("")
            self._date_info_label.config(text="No trip selected")
            self._listbox.delete(0, tk.END)

    def load(self):
        self._listbox.delete(0, tk.END)
        trip = self._trip_combo.get()
        if not trip:
            return
        for act in self.storage.list_activities(trip):
            time_str = f"{act.time} " if act.time else ""
            display = f"{act.date} {time_str}- {act.activity}"
            self._listbox.insert(tk.END, display)

    def save(self):
        trip = self._trip_combo.get().strip()
        activity = self._activity.get().strip()
        
        date_display = self._date_combo.get()
        date = self._get_date_from_display(date_display)
        
        time = self._time.get().strip()
        location = self._location.get().strip()
        notes = self._notes.get().strip()
        
        if not trip:
            messagebox.showerror("Error", "Please select a trip")
            return
        if not activity:
            messagebox.showerror("Error", "Please enter activity description")
            return
        if not date:
            messagebox.showerror("Error", "Please select activity date")
            return
        
        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Error", "Invalid date format")
            return
        
        act = Activity(activity=activity, date=date, time=time, location=location, notes=notes)
        
        try:
            self.storage.add_activity(trip, act)
            messagebox.showinfo("Success", "Activity added successfully!")
            self._activity.delete(0, tk.END)
            self._time.delete(0, tk.END)
            self._location.delete(0, tk.END)
            self._notes.delete(0, tk.END)
            self.load()
            
        except KeyError as e:
            messagebox.showerror("Error", str(e))

    def delete(self):
        sel = self._listbox.curselection()
        if not sel:
            messagebox.showwarning("No Selection", "Please select an activity to delete")
            return
        
        trip = self._trip_combo.get().strip()
        if not trip:
            return
        
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this activity?"):
            self.storage.remove_activity(trip, sel[0])
            self.load()

# PACKING LIST PAGE (Placeholder)
class PackingListPage(BasePage):
    def __init__(self, root, storage, bg_color, frame_bg, button_bg, button_fg, title_bg, back_callback):
        super().__init__(root, bg_color)
        self.storage = storage
        self.back_callback = back_callback
        self._build_ui(frame_bg, button_bg, button_fg, title_bg)

    def _build_ui(self, frame_bg, button_bg, button_fg, title_bg):
        tk.Label(self.frame, text="🎒 Packing List Generator", font=("Arial", 20, "bold"),
                 bg=title_bg, fg="white", padx=20, pady=10).pack(fill="x", pady=(0, 20))

        tk.Button(self.frame, text="🔙 Back", bg=button_bg, fg=button_fg,
                 font=("Arial", 10), command=self.back_callback).pack(pady=10)

# EMERGENCY CONTACT PAGE (Placeholder)
class EmergencyContactPage(BasePage):
    def __init__(self, root, storage, bg_color, frame_bg, button_bg, button_fg, title_bg, back_callback):
        super().__init__(root, bg_color)
        self.storage = storage
        self.back_callback = back_callback
        self._build_ui(frame_bg, button_bg, button_fg, title_bg)

    def _build_ui(self, frame_bg, button_bg, button_fg, title_bg):
        tk.Label(self.frame, text="📞 Emergency Contact Manager", font=("Arial", 20, "bold"),
                 bg=title_bg, fg="white", padx=20, pady=10).pack(fill="x", pady=(0, 20))
        

        tk.Button(self.frame, text="🔙 Back", bg=button_bg, fg=button_fg,
                 font=("Arial", 10), command=self.back_callback).pack(pady=10)

# SUMMARY PAGE
class SummaryPage(BasePage):
    def __init__(self, root, storage, bg_color, frame_bg, button_bg, button_fg, title_bg, back_callback):
        super().__init__(root, bg_color)
        self.storage = storage
        self.back_callback = back_callback
        self._build_ui(frame_bg, button_bg, button_fg, title_bg)

    def _build_ui(self, frame_bg, button_bg, button_fg, title_bg):
        tk.Label(self.frame, text="📋 Itinerary Summary", font=("Arial", 20, "bold"),
                 bg=title_bg, fg="white", padx=20, pady=10).pack(fill="x", pady=(0, 20))

        main = tk.Frame(self.frame, bg=frame_bg, relief="solid", bd=1)
        main.pack(fill="both", expand=True, padx=20, pady=10)

        control_frame = tk.Frame(main, bg=frame_bg)
        control_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(control_frame, text="Select Trip:", font=("Arial", 11, "bold"), bg=frame_bg).pack(side="left", padx=(0, 10))
        self._trip_combo = ttk.Combobox(control_frame, state="readonly", font=("Arial", 11), width=30)
        self._trip_combo.pack(side="left", padx=(0, 20))
        self._trip_combo.bind("<<ComboboxSelected>>", lambda e: self._load_summary())
        
        tk.Button(control_frame, text="🔄 Refresh", bg=button_bg, fg=button_fg,
                 font=("Arial", 10), command=self._load_summary).pack(side="left")

        self._summary_text = scrolledtext.ScrolledText(main, font=("Consolas", 10), 
                                                      wrap=tk.WORD, height=20)
        self._summary_text.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        tk.Button(self.frame, text="🔙 Back", bg=button_bg, fg=button_fg,
                 font=("Arial", 10), command=self.back_callback).pack(pady=10)

    def refresh(self):
        names = self.storage.trip_names()
        self._trip_combo['values'] = names
        if names:
            self._trip_combo.set(names[0])
            self._load_summary()
        else:
            self._trip_combo.set("")
            self._summary_text.delete(1.0, tk.END)

    def _load_summary(self):
        self._summary_text.delete(1.0, tk.END)
        trip_name = self._trip_combo.get()
        
        if not trip_name:
            self._summary_text.insert(tk.END, "No trip selected.\n")
            return
        
        trip = self.storage.get_trip(trip_name)
        if not trip:
            self._summary_text.insert(tk.END, f"No trip found: {trip_name}\n")
            return
        
        self._summary_text.insert(tk.END, f"{'='*60}\n")
        self._summary_text.insert(tk.END, f"TRIP SUMMARY: {trip.name}\n")
        self._summary_text.insert(tk.END, f"{'='*60}\n\n")
        
        self._summary_text.insert(tk.END, f"Destination: {trip.destination}\n")
        self._summary_text.insert(tk.END, f"Travel Style: {trip.travel_style}\n")
        self._summary_text.insert(tk.END, f"Dates: {trip.start} to {trip.end} ({trip.duration} days)\n")
        self._summary_text.insert(tk.END, f"Created: {trip.created}\n\n")
        
        accommodations = self.storage.list_accommodations(trip_name)
        if accommodations:
            self._summary_text.insert(tk.END, f"{'-'*40}\n")
            self._summary_text.insert(tk.END, "ACCOMMODATIONS:\n")
            self._summary_text.insert(tk.END, f"{'-'*40}\n")
            for i, acc in enumerate(accommodations, 1):
                self._summary_text.insert(tk.END, f"\n{i}. {acc.type}: {acc.name}\n")
                if acc.address:
                    self._summary_text.insert(tk.END, f"   Address: {acc.address}\n")
                self._summary_text.insert(tk.END, f"   Dates: {acc.check_in} to {acc.check_out}\n")
                if acc.confirmation:
                    self._summary_text.insert(tk.END, f"   Confirmation: {acc.confirmation}\n")
            self._summary_text.insert(tk.END, "\n")
        
        activities = self.storage.list_activities(trip_name)
        if activities:
            self._summary_text.insert(tk.END, f"{'-'*40}\n")
            self._summary_text.insert(tk.END, "ACTIVITIES:\n")
            self._summary_text.insert(tk.END, f"{'-'*40}\n")
            
            activities_by_date = {}
            for act in activities:
                if act.date not in activities_by_date:
                    activities_by_date[act.date] = []
                activities_by_date[act.date].append(act)
            
            for date in sorted(activities_by_date.keys()):
                self._summary_text.insert(tk.END, f"\n{date}:\n")
                for act in activities_by_date[date]:
                    time_str = f" at {act.time}" if act.time else ""
                    location_str = f" ({act.location})" if act.location else ""
                    self._summary_text.insert(tk.END, f"  • {act.activity}{time_str}{location_str}\n")
            self._summary_text.insert(tk.END, "\n")