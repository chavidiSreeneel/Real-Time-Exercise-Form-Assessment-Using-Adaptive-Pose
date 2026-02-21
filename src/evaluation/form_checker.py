class SquatFormChecker:
    def __init__(self):
        self.depth_threshold = 90      # knee angle for good depth
        self.torso_threshold = 40      # torso lean limit

    def evaluate(self, knee_angle, torso_angle):
        feedback = []

        if knee_angle > self.depth_threshold:
            feedback.append("Go deeper")

        if torso_angle < self.torso_threshold:
            feedback.append("Keep chest up")

        if not feedback:
            feedback.append("Good form")

        return feedback
