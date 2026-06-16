from .base import Strategy
from ...constants import LANES

class FixedTime(Strategy):
    def step(self, model, green_time):
        if self.current is None:
            return self._set(model, LANES[0])
        if model.cycle_count - self.last_change >= green_time:
            i = LANES.index(self.current)
            self._set(model, LANES[(i+1) % 4])
