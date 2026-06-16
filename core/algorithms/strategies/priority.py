from .base import Strategy

class Priority(Strategy):
    def step(self, model):
        if model.emergency_mode:
            for lane, q in model.queues.items():
                if q and q[0] == "Emergency" and lane != self.current:
                    return self._set(model, lane)
            return
        score, best = -1, self.current
        for lane, q in model.queues.items():
            s = len(q)*10 + (100 if "Emergency" in q else 0) + sum(15 if v=="Bus" else 5 if v=="Motorcycle" else 0 for v in q)
            if s > score: score, best = s, lane
        if best != self.current and (score > 20 or model.cycle_count - self.last_change >= 15):
            self._set(model, best)
