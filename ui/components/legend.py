import tkinter as tk
from tkinter import ttk

def add_legend(parent):
    legend = ttk.LabelFrame(parent, text="Legend"); legend.pack(side="left", padx=5)
    for label, col in [("Car", "#3498db"), ("Bus", "#f39c12"), ("Motorcycle", "#9b59b6"), ("Emergency", "#e74c3c")]:
        f = tk.Frame(legend); f.pack(side="left", padx=5)
        tk.Label(f, text="●", fg=col, font=("Arial", 12)).pack()
        tk.Label(f, text=label, font=("Arial", 8)).pack()
    return legend
