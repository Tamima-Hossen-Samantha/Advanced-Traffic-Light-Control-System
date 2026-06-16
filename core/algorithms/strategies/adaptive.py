from .base import Strategy

class Adaptive(Strategy):
    def step(self, model):
        if model.emergency_mode:
            for lane, q in model.queues.items():
                if q and q[0] == "Emergency" and lane != self.current:
                    return self._set(model, lane)
            return
        total = sum(len(q) for q in model.queues.values())
        if not total: return
        weights = {}
        for lane, q in model.queues.items():
            base = len(q)/total
            tg = sum(model.green_duration.values())
            fairness = min((tg/4)/max(model.green_duration[lane],1), 2.0) if tg else 1.0
            comp = 1 + sum(3.0 if v=="Emergency" else 0.8 if v=="Bus" else 0.3 if v=="Motorcycle" else 0 for v in q)
            timef = min(2.0, (model.cycle_count - self.last_change)/20) if lane != self.current else 0.5
            weights[lane] = base * fairness * comp * timef
        best = max(weights, key=weights.get)
        curr = weights.get(self.current, 0)
        if best != self.current and (weights[best] > curr*1.3 or model.cycle_count - self.last_change >= 10):
            self._set(model, best)
