class SimulationEngine:
    def __init__(self, root, model, controller, *, get_algo, get_density, get_emfreq, get_green, get_speed, on_paint, on_status):
        self.root = root
        self.m = model
        self.c = controller
        self.get_algo = get_algo
        self.get_density = get_density
        self.get_emfreq = get_emfreq
        self.get_green = get_green
        self.get_speed = get_speed
        self.on_paint = on_paint
        self.on_status = on_status

    def toggle(self):
        self.m.running = not self.m.running
        self.m.paused = False
        if self.m.running:
            self._loop()

    def pause_resume(self):
        if not self.m.running: return
        self.m.paused = not self.m.paused
        if not self.m.paused: self._loop()

    def _loop(self):
        if not self.m.running or self.m.paused: return
        self.m.tick()
        self.m.spawn_random(self.get_density(), self.get_emfreq())
        change = self.m.sync_emergency_flag()
        if change == "on":  self.on_status("Emergency vehicle detected - Priority mode activated!")
        if change == "off": self.on_status("Emergency cleared - Normal operation resumed")

        self.c.apply(self.get_algo(), self.m, self.get_green())
        self.m.process_current_lane()
        self.on_paint()

        delay = max(50, 1050 - (self.get_speed() * 10))
        self.root.after(delay, self._loop)
