import numpy as np

class AngleCalculator:
    @staticmethod
    def _xy(lms, idx):
        return np.array([lms[idx]["x"], lms[idx]["y"]], dtype=np.float32)

    @staticmethod
    def angle(a, b, c):
        ba = a - b
        bc = c - b
        denom = (np.linalg.norm(ba) * np.linalg.norm(bc)) + 1e-8
        cosang = np.dot(ba, bc) / denom
        cosang = np.clip(cosang, -1.0, 1.0)
        return float(np.degrees(np.arccos(cosang)))

    def compute(self, lms):
        if not lms:
            return {}

        # indices
        LS, LE, LW = 11, 13, 15
        RS, RE, RW = 12, 14, 16
        LH, LK, LA = 23, 25, 27
        RH, RK, RA = 24, 26, 28

        # Ensure we have enough landmarks
        max_idx = max(LS, LE, LW, RS, RE, RW, LH, LK, LA, RH, RK, RA)
        if len(lms) <= max_idx:
            return {}

        left_knee  = self.angle(self._xy(lms, LH), self._xy(lms, LK), self._xy(lms, LA))
        right_knee = self.angle(self._xy(lms, RH), self._xy(lms, RK), self._xy(lms, RA))

        left_elbow  = self.angle(self._xy(lms, LS), self._xy(lms, LE), self._xy(lms, LW))
        right_elbow = self.angle(self._xy(lms, RS), self._xy(lms, RE), self._xy(lms, RW))

        left_torso  = self.angle(self._xy(lms, LS), self._xy(lms, LH), self._xy(lms, LK))
        right_torso = self.angle(self._xy(lms, RS), self._xy(lms, RH), self._xy(lms, RK))

        # body alignment line: shoulder-hip-ankle (for plank & push-up straightness)
        left_body  = self.angle(self._xy(lms, LS), self._xy(lms, LH), self._xy(lms, LA))
        right_body = self.angle(self._xy(lms, RS), self._xy(lms, RH), self._xy(lms, RA))

        return {
            "knee": (left_knee + right_knee) / 2.0,
            "elbow": (left_elbow + right_elbow) / 2.0,
            "torso": (left_torso + right_torso) / 2.0,
            "body_line": (left_body + right_body) / 2.0
        }
