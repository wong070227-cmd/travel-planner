import tkinter as tk
from tkinter import ttk, messagebox
from constant import TRIPS, CATEGORIES
from packing_func import (
    add_item, toggle_packed, delete_item,
    get_items, calculate_progress 
)


def launch_gui():
    # ---------- Create Main Window ----------
    root = tk.Tk()
    root.title("Packing List Generator")
    root.geometry("1000x620")

    # ---------- Header ----------
    tk.Label(
        root, text="🧳 Packing List Generator",
        font=("Arial", 18, "bold"),
        bg="#2c3e50", fg="white", pady=15
    ).pack(fill="x")

    # ---------- Main Frames ----------
    main = tk.Frame(root, padx=20, pady=20)
    main.pack(fill="both", expand=True)

     # Left frame for input controls
    left = tk.Frame(main, bd=2, relief="groove", padx=15, pady=15)
    left.pack(side="left", fill="both", expand=True, padx=10)

    # Right frame for list display
    right = tk.Frame(main, bd=2, relief="groove", padx=15, pady=15)
    right.pack(side="right", fill="both", expand=True, padx=10)

    # ---------- Left Frame Inputs ----------
    label_font = ("Arial", 12)
    input_font = ("Arial", 12)

    # Trip selection dropdown
    tk.Label(left,text="Select Trip",font=label_font).pack(anchor="w", pady=(0, 4))
    trip_cb = ttk.Combobox(left,values=TRIPS,state="readonly",font=input_font,height=12)
    trip_cb.pack(fill="x", ipady=6, pady=(0, 12))

    # Category selection dropdown
    tk.Label(left,text="Category",font=label_font).pack(anchor="w", pady=(0, 4))
    cat_cb = ttk.Combobox(left,values=CATEGORIES,state="readonly",font=input_font)
    cat_cb.current(0)
    cat_cb.pack(fill="x", ipady=6, pady=(0, 12))

    # Item name entry
    tk.Label(left,text="Item Name",font=label_font).pack(anchor="w", pady=(0, 4))
    item_entry = tk.Entry(left,font=input_font)
    item_entry.pack(fill="x", ipady=6, pady=(0, 15))

    # ---------- Right Frame List ----------
    tk.Label(right,text="Packing List:",font=("Arial", 12, "bold")).pack(anchor="w", pady=(0, 5))
    
    listbox = tk.Listbox(right,height=18,bd=2,relief="solid")
    listbox.pack(fill="both", expand=True, pady=5)

    # ---------- Functions ----------
    def refresh():
        """
        Refresh the Listbox with current items
        and update the progress bar.
        """
        listbox.delete(0, tk.END)
        for i in get_items():
            status = "✔ Packed" if i["packed"] else "❌ Not Packed"
            listbox.insert(
                tk.END,
                f"{i['trip']}      {i['category']} : {i['name'].lower()}   - > {status}"
            )

        # Update progress
        progress = calculate_progress()
        progress_bar["value"] = progress
        progress_label.config(text=f"Packing Progress: {progress}%")

    def add():
         """Add a new item to the packing list"""
        if trip_cb.get() and item_entry.get():
            add_item(trip_cb.get(), cat_cb.get(), item_entry.get())
            item_entry.delete(0, tk.END)
            refresh()
        else:
            messagebox.showwarning("Error", "Missing data") # Alert if input missing


    def toggle():
        """Toggle the packed status of the selected item"""
        if listbox.curselection():
            toggle_packed(listbox.curselection()[0])
            refresh()

    def delete():
        """Delete the selected item from the list"""
        if listbox.curselection():
            delete_item(listbox.curselection()[0])
            refresh()

    # ---------- Left Frame Buttons ----------
    tk.Button(left, text="➕ Add Item", command=add).pack(pady=10)

    # ---------- Right Frame Buttons ----------
    btns = tk.Frame(right)
    btns.pack(pady=10)
    tk.Button(btns, text="✔ Toggle Packed", command=toggle).pack(side="left", padx=5)
    tk.Button(btns, text="🗑 Delete Item", command=delete).pack(side="left", padx=5)

    # ---------- Progress Bar ----------
    progress_label = tk.Label(right,text="Packing Progress: 0%")
    progress_label.pack(anchor="w", pady=(10, 2))

    progress_bar = ttk.Progressbar(right,orient="horizontal",length=400)
    progress_bar.pack(anchor="w")

     # ---------- Start Main Loop ----------
    root.mainloop()
