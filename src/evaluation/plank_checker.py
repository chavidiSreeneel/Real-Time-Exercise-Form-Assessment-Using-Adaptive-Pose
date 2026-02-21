class PlankFormChecker:
    def __init__(self):
        self.straight_threshold = 165   # closer to 180 = straighter
        self.min_hold_seconds = 10      # optional for scoring

    def evaluate(self, body_line_angle):
        feedback = []
        if body_line_angle < self.straight_threshold:
            feedback.append("Keep body straight (hips down/up)")
        else:
            feedback.append("Good plank form")
        return feedback
