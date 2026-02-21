class PushupPhaseDetector:
    def __init__(self):
        self.prev = None
        self.phase = "start"
        self.rep_count = 0
        self.bottom_threshold = 85      # elbow angle for "down" (tune)
        self.top_threshold = 160        # elbow angle for "up" (tune)

    def update(self, elbow_angle):
        if self.prev is None:
            self.prev = elbow_angle
            return self.phase, self.rep_count

        if elbow_angle < self.prev - 2:
            self.phase = "descent"

        if elbow_angle <= self.bottom_threshold:
            self.phase = "bottom"

        if elbow_angle > self.prev + 2:
            if self.phase == "bottom" and elbow_angle >= self.top_threshold:
                self.rep_count += 1
            self.phase = "ascent"

        self.prev = elbow_angle
        return self.phase, self.rep_count
