import tkinter as tk
from tkinter import ttk

class QuickStats(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="📊 Quick Statistics", padding=15)
        self.pack(fill="x", pady=10)
        self.labels = {}
        for key, label, value, color in [
            ("vehicles_processed", "Vehicles Processed", "0", "#4CAF50"),
            ("current_waiting", "Currently Waiting", "0", "#FF9800"),
            ("emergency_active", "Emergency Mode", "Inactive", "#F44336"),
            ("simulation_time", "Running Time", "0s", "#2196F3"),
        ]:
            f = tk.Frame(self, bg=color, relief="raised", bd=2); f.pack(fill="x", pady=2)
            tk.Label(f, text=label, fg="white", bg=color, font=("Arial", 9, "bold")).pack()
            self.labels[key] = tk.Label(f, text=value, fg="white", bg=color, font=("Arial", 12, "bold"))
            self.labels[key].pack()
