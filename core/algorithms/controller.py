from .strategies.fixed_time import FixedTime
from .strategies.priority import Priority
from .strategies.adaptive import Adaptive
from .strategies.round_robin import RoundRobin

class Controller:
    def __init__(self):
        self.fixed = FixedTime()
        self.priority = Priority()
        self.adaptive = Adaptive()
        self.round_robin = RoundRobin()

    def apply(self, algo_name, model, green_time):
        if   algo_name == "Fixed Time":    self.fixed.step(model, green_time)
        elif algo_name == "Priority Based": self.priority.step(model)
        elif algo_name == "Adaptive":      self.adaptive.step(model)
        else:                               self.round_robin.step(model, green_time)
