import tkinter as tk
from tkinter import ttk

class ControlPanel(ttk.LabelFrame):
    def __init__(self, parent, on_start, on_pause, on_add_random, on_add_lane, on_emergency, on_reset, speed_var):
        super().__init__(parent, text="🎮 Simulation Controls", padding=15)
        self.pack(fill="x", pady=10)

        r1 = ttk.Frame(self); r1.pack(fill="x", pady=5)
        self.start_btn = tk.Button(r1, text="▶ Start", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
                                   command=on_start, relief="raised", bd=2)
        self.start_btn.pack(side="left", fill="x", expand=True, padx=2)
        self.pause_btn = tk.Button(r1, text="⏸ Pause", bg="#FF9800", fg="white", font=("Arial", 10, "bold"),
                                   command=on_pause, relief="raised", bd=2)
        self.pause_btn.pack(side="left", fill="x", expand=True, padx=2)

        r2 = ttk.Frame(self); r2.pack(fill="x", pady=5)
        tk.Button(r2, text="🚗 Add Vehicle", bg="#2196F3", fg="white", font=("Arial", 9, "bold"),
                  command=on_add_random, relief="raised", bd=2).pack(side="left", fill="x", expand=True, padx=2)

        style = ttk.Style(); style.configure("Green.TMenubutton", background="#3d6164", foreground="white")
        style.map("Green.TMenubutton", background=[("active", "#161817")], foreground=[("active", "white")])
        lane_btn = ttk.Menubutton(r2, text="▼ Lane", style="Green.TMenubutton")
        menu = tk.Menu(lane_btn, tearoff=0)
        for lane in ["North", "East", "South", "West", "Random Lane"]:
            menu.add_command(label=lane, command=lambda L=lane: on_add_lane(None if L=="Random Lane" else L))
        lane_btn["menu"] = menu; lane_btn.pack(side="left", padx=2)

        tk.Button(r2, text="🚨 Emergency", bg="#F44336", fg="white", font=("Arial", 9, "bold"),
                  command=on_emergency, relief="raised", bd=2).pack(side="left", fill="x", expand=True, padx=2)

        r3 = ttk.Frame(self); r3.pack(fill="x", pady=5)
        tk.Button(r3, text="🔄 Reset", bg="#9C27B0", fg="white", font=("Arial", 9, "bold"),
                  command=on_reset, relief="raised", bd=2).pack(fill="x")

        ttk.Separator(self, orient="horizontal").pack(fill="x", pady=10)
        row = ttk.Frame(self); row.pack(fill="x")
        ttk.Label(row, text="Simulation Speed:", font=("Segoe UI", 10, "bold")).pack(anchor="w")
        line = ttk.Frame(row); line.pack(fill="x", pady=5)
        ttk.Scale(line, from_=10, to=100, variable=speed_var, orient="horizontal").pack(side="left", fill="x", expand=True)
        speed_lbl = ttk.Label(line, text="Normal", font=("Arial", 10, "bold")); speed_lbl.pack(side="right", padx=(10,0))
        speed_var.trace("w", lambda *a: speed_lbl.config(text=("Slow" if speed_var.get()<30 else "Normal" if speed_var.get()<70 else "Fast")))
