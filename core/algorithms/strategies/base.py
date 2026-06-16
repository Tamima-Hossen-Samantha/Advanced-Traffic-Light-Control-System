class Strategy:
    def __init__(self):
        self.current = None
        self.last_change = 0

    def _set(self, model, lane):
        self.current = lane
        self.last_change = model.cycle_count
        model.current_green = lane
        model.last_green_change = self.last_change
