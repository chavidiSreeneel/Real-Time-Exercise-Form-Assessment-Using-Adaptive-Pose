class SquatPhaseDetector:
    def __init__(self):
        self.prev_angle = None
        self.phase = "start"
        self.rep_count = 0
        self.bottom_threshold = 80  # adjust if needed
        self.standing_threshold = 160

    def update(self, knee_angle):
        if self.prev_angle is None:
            self.prev_angle = knee_angle
            return self.phase, self.rep_count

        # Detect descent
        if knee_angle < self.prev_angle - 2:
            self.phase = "descent"

        # Detect bottom
        elif knee_angle <= self.bottom_threshold:
            self.phase = "bottom"

        # Detect ascent
        elif knee_angle > self.prev_angle + 2:
            if self.phase == "bottom":
                self.rep_count += 1
            self.phase = "ascent"

        self.prev_angle = knee_angle
        return self.phase, self.rep_count
