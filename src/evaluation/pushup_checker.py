class PushupFormChecker:
    def __init__(self):
        self.straight_threshold = 165
        self.depth_threshold = 95

    def evaluate(self, elbow_angle, body_line_angle):
        feedback = []
        if elbow_angle > self.depth_threshold:
            feedback.append("Go lower")
        if body_line_angle < self.straight_threshold:
            feedback.append("Keep body straight")
        if not feedback:
            feedback.append("Good push-up form")
        return feedback
