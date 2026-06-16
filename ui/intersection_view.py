# live traffic intersection ui


import tkinter as tk

class IntersectionView:
    def __init__(self, parent):
        self.canvas = tk.Canvas(parent, bg="#1a252f", highlightthickness=2, highlightbackground="#3498db")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", lambda e: self.canvas.after(50, self.draw))
        self.lights = {}
        self.vehicle_displays = {}
        self.queue_labels = {}
        self.lane_areas = {}
        self.lane_flash_rects = {}
        parent.after(100, self.draw)

    def draw(self):
        c = self.canvas
        w, h = c.winfo_width(), c.winfo_height()
        if w <= 1 or h <= 1:
            return
        c.delete("all")
        c.create_rectangle(0, 0, w, h, fill="#1a252f", outline="")
        rw = min(w, h) // 4
        c.create_rectangle(w//2 - rw//2, 0, w//2 + rw//2, h, fill="#34495e", outline="#2c3e50", width=3)
        c.create_rectangle(0, h//2 - rw//2, w, h//2 + rw//2, fill="#34495e", outline="#2c3e50", width=3)

        dash = (15, 10)
        y1, y2 = h//2 - rw//4, h//2 + rw//4
        c.create_line(0, y1, w, y1, fill="#f1c40f", width=2, dash=dash)
        c.create_line(0, y2, w, y2, fill="#f1c40f", width=2, dash=dash)
        x1, x2 = w//2 - rw//4, w//2 + rw//4
        c.create_line(x1, 0, x1, h, fill="#f1c40f", width=2, dash=dash)
        c.create_line(x2, 0, x2, h, fill="#f1c40f", width=2, dash=dash)

        cs = rw // 2
        c.create_rectangle(w//2 - cs//2, h//2 - cs//2, w//2 + cs//2, h//2 + cs//2,
                           fill="#2c3e50", outline="#3498db", width=4)

        for text, (x, y, col) in {
            "NORTH": (w//2, h//6, "#3498db"),
            "SOUTH": (w//2, 5*h//6, "#e74c3c"),
            "EAST": (5*w//6, h//2, "#2ecc71"),
            "WEST": (w//6, h//2, "#f39c12")
        }.items():
            c.create_text(x, y, text=text, font=("Arial", 14, "bold"), fill=col)

        self._lights(w, h)
        self._stacks_labels(w, h)
        self._lanes(w, h, rw)

    def _lights(self, w, h):
        c = self.canvas
        self.lights.clear()
        pos = {
            "North": (w//2 + 60, h//2 - 120),
            "South": (w//2 - 60, h//2 + 120),
            "East":  (w//2 + 120, h//2 + 60),
            "West":  (w//2 - 120, h//2 - 60)
        }
        for lane, (x, y) in pos.items():
            c.create_rectangle(x-25, y-50, x+25, y+50, fill="#2c3e50", outline="#34495e", width=3)
            self.lights[lane] = {
                "red":    c.create_oval(x-18, y-35, x+18, y-5,  fill="#444", outline="#666", width=2),
                "yellow": c.create_oval(x-18, y-15, x+18, y+15, fill="#444", outline="#666", width=2),
                "green":  c.create_oval(x-18, y+5,  x+18, y+35, fill="#444", outline="#666", width=2)
            }
            c.create_text(x, y+70, text=lane, font=("Arial", 10, "bold"), fill="#3498db")

    def _stacks_labels(self, w, h):
        c = self.canvas
        self.vehicle_displays.clear()
        self.queue_labels.clear()
        pos = {
            "North": (w//2 - 80, h//3),
            "South": (w//2 + 80, 2*h//3),
            "East":  (2*w//3, h//2 - 80),
            "West":  (w//3,   h//2 + 80)
        }
        labels = {
            "North": (pos["North"][0] + 50, pos["North"][1], "w"),
            "South": (pos["South"][0] + 50, pos["South"][1] + 40, "w"),  # moved downward
            "East":  (pos["East"][0], pos["East"][1] - 35, "s"),
            "West":  (pos["West"][0], pos["West"][1] + 35, "n")
        }
        for lane, (x, y) in pos.items():
            self.vehicle_displays[lane] = {"position": (x, y), "vehicles": []}
            lx, ly, anc = labels[lane]
            self.queue_labels[lane] = c.create_text(lx, ly, text=f"{lane}: 0",
                                                    font=("Arial", 11, "bold"),
                                                    fill="#3498db", anchor=anc)

    def _lanes(self, w, h, rw):
        c = self.canvas
        self.lane_areas.clear()
        self.lane_flash_rects.clear()
        cx, cy, bw, pad = w//2, h//2, rw//2, 8
        regs = {
            "North": (cx-bw+pad, 0, cx+bw-pad, cy-pad),
            "South": (cx-bw+pad, cy+pad, cx+bw-pad, h),
            "East":  (cx+pad, cy-bw+pad, w, cy+bw-pad),
            "West":  (0, cy-bw+pad, cx-pad, cy+bw-pad)
        }
        for lane, r in regs.items():
            self.lane_areas[lane] = r
            c.create_rectangle(*r, outline="#7f8c8d", width=1)
            self.lane_flash_rects[lane] = c.create_rectangle(*r, outline="#f4d03f", width=4, state="hidden")

    def set_lights(self, current):
        for lane, bulbs in self.lights.items():
            if lane == current:
                self.canvas.itemconfig(bulbs["green"], fill="#27ae60", outline="#2ecc71", width=3)
                self.canvas.itemconfig(bulbs["red"], fill="#444", outline="#666", width=2)
            else:
                self.canvas.itemconfig(bulbs["red"], fill="#e74c3c", outline="#c0392b", width=3)
                self.canvas.itemconfig(bulbs["green"], fill="#444", outline="#666", width=2)

    def draw_queues(self, queues):
        c = self.canvas
        for lane, disp in self.vehicle_displays.items():
            for rid in disp["vehicles"]:
                try:
                    c.delete(rid)
                except:
                    pass
            disp["vehicles"].clear()
        for lane, disp in self.vehicle_displays.items():
            q = queues[lane]
            color = "#3498db" if not q else "#2ecc71" if len(q) <= 3 else "#f39c12" if len(q) <= 6 else "#e74c3c"
            c.itemconfig(self.queue_labels[lane], text=f"{lane}: {len(q)}", fill=color)
            x, y = disp["position"]
            spacing = 25
            for i, v in enumerate(list(q)[:8]):
                if v == "Emergency":
                    fill, outline, wth = "#e74c3c", "#c0392b", 4
                elif v == "Bus":
                    fill, outline, wth = "#f39c12", "#e67e22", 3
                elif v == "Motorcycle":
                    fill, outline, wth = "#9b59b6", "#8e44ad", 2
                else:
                    fill, outline, wth = "#3498db", "#2980b9", 2
                if lane in ("North", "South"):
                    yy = y - i*spacing if lane == "North" else y + i*spacing
                    rid = c.create_rectangle(x-12, yy-10, x+12, yy+10, fill=fill, outline=outline, width=wth)
                else:
                    xx = x + i*spacing if lane == "East" else x - i*spacing
                    rid = c.create_rectangle(xx-10, y-12, xx+10, y+12, fill=fill, outline=outline, width=wth)
                disp["vehicles"].append(rid)

    def flash_lane(self, lane, ms=400):
        rid = self.lane_flash_rects.get(lane)
        if not rid:
            return
        self.canvas.itemconfigure(rid, state="normal")
        self.canvas.after(ms, lambda: self.canvas.itemconfigure(rid, state="hidden"))
