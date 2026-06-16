from tkinter import ttk
def add_options(parent):
    box = ttk.LabelFrame(parent, text="View Options"); box.pack(side="right", padx=5)
    var = ttk.BooleanVar(value=True) if hasattr(ttk, 'BooleanVar') else None
    ttk.Checkbutton(box, text="Animations").pack(side="left", padx=5)
    return box
