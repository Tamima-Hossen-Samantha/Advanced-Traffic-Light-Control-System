import random
from collections import deque
from .constants import LANES, VEHICLE_WEIGHTS, SPAWN_WEIGHTS, DENSITY, EMERGENCY_FREQ

class TrafficState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.running = False
        self.paused = False
        self.queues = {l: deque() for l in LANES}
        self.current_green = None
        self.emergency_mode = False
        self.simulation_time = 0
        self.cycle_count = 0
        self.total_vehicles_processed = 0
        self.wait_times = []
        self.green_duration = {l: 0 for l in LANES}
        self.last_green_change = 0
        self.emergency_processed = 0

    def tick(self):
        self.simulation_time += 1
        self.cycle_count += 1
        if self.current_green:
            self.green_duration[self.current_green] += 1

    def spawn_random(self, density, em_freq):
        pd = DENSITY.get(density, 0.25)
        pe = EMERGENCY_FREQ.get(em_freq, 0.0)
        for lane in self.queues:
            if random.random() < pd:
                v = random.choices(list(SPAWN_WEIGHTS.keys()), weights=list(SPAWN_WEIGHTS.values()))[0]
                self.queues[lane].append(v)
            if random.random() < pe:
                self.queues[lane].appendleft("Emergency")
                self.emergency_mode = True

    def add_vehicle(self, lane=None):
        lane = random.choice(LANES) if lane is None else lane
        v = random.choices(list(VEHICLE_WEIGHTS.keys()), weights=list(VEHICLE_WEIGHTS.values()))[0]
        if v == "Emergency":
            self.queues[lane].appendleft(v); self.emergency_mode = True
        else:
            self.queues[lane].append(v)
        return lane, v

    def trigger_emergency(self):
        import random
        lane = random.choice(LANES)
        self.queues[lane].appendleft("Emergency")
        self.emergency_mode = True
        return lane

    def clear_queues(self):
        for l in LANES: self.queues[l].clear()

    def process_current_lane(self):
        q = self.queues.get(self.current_green, None)
        if not q: return
        if self.emergency_mode and q and q[0] == "Emergency":
            q.popleft(); self.total_vehicles_processed += 1; self.emergency_processed += 1; return
        import random
        for _ in range(min(random.randint(1,2), len(q))):
            q.popleft()
            self.total_vehicles_processed += 1
            self.wait_times.append(random.randint(1, 10))

    def sync_emergency_flag(self):
        active = any("Emergency" in q for q in self.queues.values())
        if active and not self.emergency_mode:
            self.emergency_mode = True; return "on"
        if not active and self.emergency_mode:
            self.emergency_mode = False; return "off"
        return None
