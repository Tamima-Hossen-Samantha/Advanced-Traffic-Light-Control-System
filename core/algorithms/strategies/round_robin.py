from .base import Strategy
from ...constants import LANES

class RoundRobin(Strategy):
    def step(self, model, green_time):
        t = max(10, green_time//4)
        if self.current is None:
            return self._set(model, LANES[0])
        if model.cycle_count - self.last_change >= t:
            i = LANES.index(self.current)
            self._set(model, LANES[(i+1) % 4])
