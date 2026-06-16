import tkinter as tk
from tkinter import ttk

class ConfigPanel(ttk.LabelFrame):
    def __init__(self, parent, algorithm, density, emergency_freq, green_time):
        super().__init__(parent, text="🎛️ Control Configuration", padding=15)
        self.pack(fill="x", pady=5)
        ttk.Label(self, text="Control Algorithm:", font=("Segoe UI", 10, "bold")).grid(row=0, column=0, sticky="w", pady=5)
        for i, a in enumerate(["Fixed Time", "Priority Based", "Adaptive", "Round Robin"]):
            ttk.Radiobutton(self, text=a, variable=algorithm, value=a).grid(row=i+1, column=0, sticky="w", pady=2)
        ttk.Separator(self, orient="horizontal").grid(row=6, column=0, sticky="ew", pady=10)
        ttk.Label(self, text="Traffic Density:", font=("Segoe UI", 10, "bold")).grid(row=7, column=0, sticky="w", pady=5)
        for i, d in enumerate(["Low", "Medium", "High"]):
            ttk.Radiobutton(self, text=d, variable=density, value=d).grid(row=8, column=i, padx=5, sticky="w")
        ttk.Separator(self, orient="horizontal").grid(row=9, column=0, sticky="ew", pady=10)
        ttk.Label(self, text="Emergency Frequency:", font=("Segoe UI", 10, "bold")).grid(row=10, column=0, sticky="w", pady=5)
        for i, f in enumerate(["None", "Rare", "Occasional", "Frequent"]):
            ttk.Radiobutton(self, text=f, variable=emergency_freq, value=f).grid(row=11, column=i, padx=5, sticky="w")
        ttk.Separator(self, orient="horizontal").grid(row=12, column=0, sticky="ew", pady=10)
        frame = ttk.Frame(self); frame.grid(row=13, column=0, sticky="ew")
        ttk.Label(frame, text="Green Light Duration:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        row = ttk.Frame(frame); row.pack(fill="x", pady=5)
        ttk.Scale(row, from_=10, to=60, variable=green_time, orient="horizontal").pack(side="left", fill="x", expand=True)
        lbl = ttk.Label(row, text=f"{green_time.get()}s", font=("Arial", 10, "bold")); lbl.pack(side="right", padx=(10,0))
        green_time.trace("w", lambda *a: lbl.config(text=f"{green_time.get()}s"))
