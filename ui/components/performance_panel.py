import tkinter as tk
from tkinter import ttk

class PerformancePanel(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Performance Dashboard", padding=15)
        self.grid_columnconfigure(0, weight=1); self.grid_columnconfigure(1, weight=1)
        self.labels = {}
        items = [("total_processed","Total Vehicles Processed","0","#4CAF50"),
                 ("avg_wait","Average Wait Time","0.0 cycles","#FF9800"),
                 ("throughput","Throughput Rate","0.0 vehicles/min","#2196F3"),
                 ("efficiency","System Efficiency","0.0%","#9C27B0"),
                 ("emergency_count","Emergency Vehicles","0","#F44336"),
                 ("best_lane","Most Efficient Lane","None","#795548")]
        for i,(k,lab,val,col) in enumerate(items):
            r,c = i//2, i%2
            box = tk.Frame(self, bg=col, relief="raised", bd=2); box.grid(row=r, column=c, padx=10, pady=5, sticky="ew")
            tk.Label(box, text=lab, fg="white", bg=col, font=("Arial",10,"bold")).pack()
            self.labels[k] = tk.Label(box, text=val, fg="white", bg=col, font=("Arial",14,"bold")); self.labels[k].pack()
