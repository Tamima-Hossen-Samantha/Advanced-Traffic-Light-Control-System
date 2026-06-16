import tkinter as tk
from tkinter import ttk, messagebox, filedialog

from core.state import TrafficState
from core.algorithms import Controller
from core.sim import SimulationEngine
from services.stats import snapshot, long_report
from services.exporter import export_csv
from ui.intersection_view import IntersectionView
from ui.components.config_panel import ConfigPanel
from ui.components.control_panel import ControlPanel
from ui.components.quick_stats import QuickStats
from ui.components.performance_panel import PerformancePanel
from ui.components.details_log import DetailsLog
from ui.components.legend import add_legend
from ui.components.options import add_options
from ui.helptext import HELP_TEXT

class MainWindow:
    def __init__(self, root: tk.Tk):
        self.root = root
        self.root.title("🚦 Advanced Traffic Light Control System v2.0")
        self.root.geometry("1400x950")
        self.root.configure(bg="#f0f2f5")

        self.m = TrafficState()
        self.c = Controller()

        self.algorithm = tk.StringVar(value="Adaptive")
        self.density = tk.StringVar(value="Medium")
        self.emergency_freq = tk.StringVar(value="Rare")
        self.green_time = tk.IntVar(value=30)
        self.speed = tk.IntVar(value=50)

        self._menu(); self._tabs(); self._statusbar()

        self.engine = SimulationEngine(
            self.root, self.m, self.c,
            get_algo=lambda: self.algorithm.get(),
            get_density=lambda: self.density.get(),
            get_emfreq=lambda: self.emergency_freq.get(),
            get_green=lambda: self.green_time.get(),
            get_speed=lambda: self.speed.get(),
            on_paint=self._paint,
            on_status=lambda s: self.status.set(s),
        )
        self._center()
        messagebox.showinfo("Traffic Light Simulator v2.0",
            "Welcome to the Advanced Traffic Light Control System!\n\n"
            "Features:\n"
            "• 4 Different control algorithms\n"
            "• Real-time traffic visualization\n"
            "• Emergency vehicle handling\n"
            "• Comprehensive performance analytics\n"
            "• Interactive controls and testing\n\n"
            "Tip: Use the ▼ Lane menu next to “Add Vehicle” to add to a specific lane. "
            "The lane will flash yellow briefly.")

    # ---- UI build ----
    def _menu(self):
        m = tk.Menu(self.root); self.root.config(menu=m)
        filem = tk.Menu(m, tearoff=0); m.add_cascade(label="File", menu=filem)
        filem.add_command(label="Reset Simulation", command=self.reset)
        filem.add_command(label="Export Statistics", command=self._export)
        filem.add_separator(); filem.add_command(label="Exit", command=self.root.quit)
        viewm = tk.Menu(m, tearoff=0); m.add_cascade(label="View", menu=viewm)
        viewm.add_command(label="Show Help", command=self._help)
        toolsm = tk.Menu(m, tearoff=0); m.add_cascade(label="Tools", menu=toolsm)
        toolsm.add_command(label="Add 10 Vehicles", command=lambda: [self._add_random() for _ in range(10)])
        toolsm.add_command(label="Clear All Queues", command=self._clear)

    def _tabs(self):
        nb = ttk.Notebook(self.root); nb.pack(fill="both", expand=True, padx=10, pady=10)
        live, stats_tab, help_tab = ttk.Frame(nb), ttk.Frame(nb), ttk.Frame(nb)
        nb.add(live, text="🚦 Live Simulation"); nb.add(stats_tab, text="📊 Analytics"); nb.add(help_tab, text="❓ User Guide")

        left = ttk.Frame(live, width=400); left.pack(side="left", fill="y", padx=(0,10)); left.pack_propagate(False)
        right = ttk.Frame(live); right.pack(side="right", fill="both", expand=True)

        ConfigPanel(left, self.algorithm, self.density, self.emergency_freq, self.green_time)
        cp = ControlPanel(left, self._start_stop, self._pause_resume, self._add_random, self._add_lane, self._emergency, self.reset, self.speed)
        self.start_btn, self.pause_btn = cp.start_btn, cp.pause_btn

        self.quick = QuickStats(left)

        box = ttk.LabelFrame(right, text="🚦 Live Traffic Intersection", padding=10); box.pack(fill="both", expand=True)
        wrap = ttk.Frame(box); wrap.pack(fill="both", expand=True)
        self.view = IntersectionView(wrap)
        self.view.canvas.bind("<Button-1>", self._canvas_info)

        bar = ttk.Frame(box); bar.pack(fill="x", pady=5)
        add_legend(bar); add_options(bar)

        perf = PerformancePanel(stats_tab); perf.pack(fill="x", padx=10, pady=10)
        self.metrics = perf.labels
        detail = DetailsLog(stats_tab); detail.pack(fill="both", expand=True, padx=10, pady=10)
        self.log = detail.text
        btns = ttk.Frame(detail); btns.pack(fill="x", pady=(10,0))
        ttk.Button(btns, text="Refresh Stats", command=self._refresh_log).pack(side="left", padx=5)
        ttk.Button(btns, text="Clear Log", command=lambda: self._clear_text(self.log)).pack(side="left", padx=5)
        ttk.Button(btns, text="Export Stats", command=self._export).pack(side="left", padx=5)

        # map for quick labels
        self.quick_labels = self.quick.labels

        # help tab
        self._help_tab(help_tab)

    def _help_tab(self, parent):
        frame = ttk.Frame(parent); frame.pack(fill="both", expand=True, padx=10, pady=10)
        t = tk.Text(frame, wrap="word", font=("Segoe UI", 10), state="disabled", bg="#f8f9fa", fg="#2c3e50")
        sb = ttk.Scrollbar(frame, orient="vertical", command=t.yview); t.configure(yscrollcommand=sb.set)
        t.pack(side="left", fill="both", expand=True); sb.pack(side="right", fill="y")
        t.config(state="normal"); t.insert("1.0", HELP_TEXT); t.config(state="disabled")

    def _statusbar(self):
        bar = ttk.Frame(self.root); bar.pack(fill="x", padx=10, pady=(0,10))
        self.status = tk.StringVar(value="Ready to start simulation")
        ttk.Label(bar, textvariable=self.status, relief="sunken", background="#e8f4f8", font=("Arial", 10)).pack(side="left", fill="x", expand=True)
        self.time_lbl = ttk.Label(bar, text="Time: 0s", background="#e8f4f8", font=("Arial", 10)); self.time_lbl.pack(side="right", padx=10)

    # ---- actions ----
    def _start_stop(self):
        self.engine.toggle()
        self.start_btn.config(text="⏹ Stop" if self.m.running else "▶ Start", bg="#F44336" if self.m.running else "#4CAF50")
        self.status.set("Simulation running..." if self.m.running else "Simulation stopped")

    def _pause_resume(self):
        self.engine.pause_resume()
        if self.m.paused:
            self.pause_btn.config(text="▶ Resume", bg="#4CAF50"); self.status.set("Simulation paused")
        else:
            self.pause_btn.config(text="⏸ Pause", bg="#FF9800")
            if self.m.running: self.status.set("Simulation resumed...")

    def reset(self):
        self.m.reset(); self.c = Controller(); self.engine.c = self.c
        self.start_btn.config(text="▶ Start", bg="#4CAF50"); self.pause_btn.config(text="⏸ Pause", bg="#FF9800")
        self.status.set("Simulation reset - Ready to start"); self._paint()
        messagebox.showinfo("Reset Complete", "Simulation has been reset to initial state.")

    def _add_random(self):
        lane, v = self.m.add_vehicle(); self.view.flash_lane(lane); self._paint()
        self.status.set(("Emergency vehicle added to" if v=="Emergency" else f"{v} added to") + f" {lane} lane")

    def _add_lane(self, lane):
        lane, v = self.m.add_vehicle(lane); self.view.flash_lane(lane); self._paint()
        self.status.set(("Emergency vehicle added to" if v=="Emergency" else f"{v} added to") + f" {lane} lane")

    def _emergency(self):
        lane = self.m.trigger_emergency(); self.view.flash_lane(lane); self._paint()
        self.status.set(f"Emergency vehicle triggered in {lane} lane!")

    def _clear(self):
        self.m.clear_queues(); self._paint()
        messagebox.showinfo("Queues Cleared", "All vehicle queues have been cleared!")

    def _canvas_info(self, _):
        info = (f"Intersection Status:\nCurrent Green: {self.m.current_green or 'None'}\n"
                f"Emergency Mode: {'Active' if self.m.emergency_mode else 'Inactive'}\n"
                f"Total Waiting: {sum(len(q) for q in self.m.queues.values())} vehicles\n"
                f"Algorithm: {self.algorithm.get()}\nSimulation Time: {self.m.simulation_time}s")
        messagebox.showinfo("Intersection Info", info)

    # ---- repaint ----
    def _paint(self):
        self.view.set_lights(self.m.current_green); self.view.draw_queues(self.m.queues)
        snap = snapshot(self.m)
        self.quick_labels["vehicles_processed"].config(text=str(self.m.total_vehicles_processed))
        self.quick_labels["current_waiting"].config(text=str(snap["waiting"]))
        self.quick_labels["emergency_active"].config(text="Active" if self.m.emergency_mode else "Inactive")
        t = f"{self.m.simulation_time}s"; self.quick_labels["simulation_time"].config(text=t); self.time_lbl.config(text=f"Time: {t}")
        self.metrics["total_processed"].config(text=str(self.m.total_vehicles_processed))
        self.metrics["avg_wait"].config(text=f"{snap['avg']:.1f} cycles")
        self.metrics["throughput"].config(text=f"{snap['thr']:.1f} veh/min")
        self.metrics["efficiency"].config(text=f"{snap['eff']:.1f}%")
        self.metrics["emergency_count"].config(text=str(snap["emc"]))
        self.metrics["best_lane"].config(text=snap["best"])
        if self.m.cycle_count % 30 == 0: self._refresh_log()

    def _refresh_log(self):
        self.log.config(state="normal"); self.log.delete("1.0", "end")
        self.log.insert("end", long_report(self.m, self.algorithm.get(), self.density.get(),
                                           self.emergency_freq.get(), self.green_time.get(), self.speed.get()))
        self.log.config(state="disabled"); self.log.see("end")

    def _export(self):
        fn = filedialog.asksaveasfilename(defaultextension=".csv",
            filetypes=[("CSV files","*.csv"),("All files","*.*")], title="Export Statistics")
        if not fn: return
        s = snapshot(self.m)
        export_csv(fn, self.m, avg_wait=s["avg"], throughput=s["thr"],
                   conf=dict(algo=self.algorithm.get(), density=self.density.get(), emfreq=self.emergency_freq.get(), green=self.green_time.get()))
        messagebox.showinfo("Export Successful", f"Statistics exported to {fn}")

    def _help(self):
        win = tk.Toplevel(self.root); win.title("Traffic Simulator Quick Help"); win.geometry("600x400")
        tk.Label(win, text="""QUICK START
1) Configure: algorithm, density, emergency rate
2) Start ▶
3) Interact: add vehicles / emergencies
4) Analyze on the Analytics tab
""",
                 justify="left", font=("Segoe UI", 11), padx=20, pady=10).pack()
        txt = tk.Text(win, wrap="word"); txt.pack(fill="both", expand=True); txt.insert("1.0", HELP_TEXT); txt.config(state="disabled")
        ttk.Button(win, text="Close", command=win.destroy).pack(pady=8)

    def _status(self): pass  # legacy

    def _center(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth()//2) - (self.root.winfo_width()//2)
        y = (self.root.winfo_screenheight()//2) - (self.root.winfo_height()//2)
        self.root.geometry(f"+{x}+{y}")
