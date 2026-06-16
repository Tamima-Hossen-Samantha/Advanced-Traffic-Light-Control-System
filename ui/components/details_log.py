from tkinter import ttk, Text

class DetailsLog(ttk.LabelFrame):
    def __init__(self, parent):
        super().__init__(parent, text="Detailed Log", padding=10)
        tf = ttk.Frame(self); tf.pack(fill="both", expand=True)
        self.text = Text(tf, height=15, wrap="word", font=("Consolas", 9), state="disabled", bg="#f8f9fa", fg="#2c3e50")
        sb = ttk.Scrollbar(tf, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=sb.set); self.text.pack(side="left", fill="both", expand=True); sb.pack(side="right", fill="y")
