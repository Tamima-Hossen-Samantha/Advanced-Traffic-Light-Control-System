import tkinter as tk
from tkinter import ttk

class StatusBar(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.status = tk.StringVar(value="Ready to start simulation")
        self.time_lbl = ttk.Label(self, text="Time: 0s", background="#e8f4f8", font=("Arial", 10))
        ttk.Label(self, textvariable=self.status, relief="sunken", background="#e8f4f8", font=("Arial", 10)).pack(side="left", fill="x", expand=True)
        self.time_lbl.pack(side="right", padx=10)
        self.pack(fill="x", padx=10, pady=(0,10))
