import cv2
import mediapipe as mp
import time
import csv
import os
from typing import Optional, Tuple, Dict, Any, List
from src.angles.angle_calculator import AngleCalculator
from src.temporal.smoother import TemporalSmoother
from src.evaluation.phase_detector import SquatPhaseDetector
from src.evaluation.form_checker import SquatFormChecker
from src.evaluation.pushup_phase_detector import PushupPhaseDetector
from src.evaluation.pushup_checker import PushupFormChecker
from src.evaluation.plank_checker import PlankFormChecker


class PoseDetector:
    """
    MediaPipe Pose wrapper:
    - reads webcam/video
    - extracts landmarks
    - draws skeleton
    - returns landmark list per frame
    - logs metrics to CSV
    """

    def __init__(
        self,
        static_image_mode: bool = False,
        model_complexity: int = 1,
        enable_segmentation: bool = False,
        min_detection_confidence: float = 0.5,
        min_tracking_confidence: float = 0.5,
        exercise: str = "squat",
        display: bool = True
    ):
        self.exercise = exercise
        self.display = display
        self.mp_pose = mp.solutions.pose
        self.mp_draw = mp.solutions.drawing_utils

        self.pose = self.mp_pose.Pose(
            static_image_mode=static_image_mode,
            model_complexity=model_complexity,
            enable_segmentation=enable_segmentation,
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
        )
        self.angle_calc = AngleCalculator()
        self.smoother = TemporalSmoother(window_size=7)
        
        # Initialize detectors/checkers
        self.squat_phase = SquatPhaseDetector()
        self.squat_checker = SquatFormChecker()
        
        self.pushup_phase = PushupPhaseDetector()
        self.pushup_checker = PushupFormChecker()
        
        self.plank_checker = PlankFormChecker()

    def process_frame(self, frame) -> Tuple[Any, Optional[List[Dict[str, float]]]]:
        """
        Returns:
          - annotated_frame
          - landmarks_list: list of dicts with x,y,z,visibility (normalized coords)
        """
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.pose.process(image_rgb)

        landmarks_list = None
        if results.pose_landmarks:
            if self.display:
                self.mp_draw.draw_landmarks(
                    frame,
                    results.pose_landmarks,
                    self.mp_pose.POSE_CONNECTIONS,
                )
            landmarks_list = []
            for lm in results.pose_landmarks.landmark:
                landmarks_list.append(
                    {"x": lm.x, "y": lm.y, "z": lm.z, "v": lm.visibility}
                )

        return frame, landmarks_list

    def run_video(self, source=0, window_name: str = "PoseDetector"):
        """
        source:
          - 0 for webcam
          - "path/to/video.mp4" for video
        """
        cap = cv2.VideoCapture(source)
        if not cap.isOpened():
            raise RuntimeError(f"Could not open video source: {source}")

        # Logging Setup
        log_file = None
        writer = None
        if isinstance(source, str):
            video_name = os.path.basename(source).split('.')[0]
            log_dir = os.path.join("outputs", "logs")
            os.makedirs(log_dir, exist_ok=True)
            log_path = os.path.join(log_dir, f"{self.exercise}_{video_name}.csv")
            log_file = open(log_path, 'w', newline='')
            writer = csv.writer(log_file)
            writer.writerow(["timestamp", "knee", "torso", "elbow", "body_line", "phase", "reps", "feedback", "fps"])

        start_time = time.time()
        frame_count = 0

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            frame_count += 1
            curr_time = time.time()
            elapsed = curr_time - start_time
            fps = frame_count / elapsed if elapsed > 0 else 0

            frame, landmarks = self.process_frame(frame)

            angles = self.angle_calc.compute(landmarks)
            if angles:
                # Smooth all necessary angles
                knee = self.smoother.smooth("knee", angles["knee"])
                torso = self.smoother.smooth("torso", angles["torso"])
                elbow = self.smoother.smooth("elbow", angles["elbow"])
                body_line = self.smoother.smooth("body_line", angles["body_line"])

                # Exercise logic
                phase, reps, feedback = "hold", 0, []
                
                if self.exercise == "squat":
                    phase, reps = self.squat_phase.update(knee)
                    feedback = self.squat_checker.evaluate(knee, torso)

                elif self.exercise == "pushup":
                    phase, reps = self.pushup_phase.update(elbow)
                    feedback = self.pushup_checker.evaluate(elbow, body_line)

                elif self.exercise == "plank":
                    phase, reps = "hold", 0
                    feedback = self.plank_checker.evaluate(body_line)

                # Log data
                if writer:
                    writer.writerow([
                        curr_time, knee, torso, elbow, body_line, 
                        phase, reps, "|".join(feedback), fps
                    ])

                # Overlay Results if display is enabled
                if self.display:
                    cv2.putText(frame, f"Knee: {knee:.1f}", (20, 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    cv2.putText(frame, f"Torso: {torso:.1f}", (20, 75),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    cv2.putText(frame, f"Elbow: {elbow:.1f}", (20, 110),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                    cv2.putText(frame, f"Phase: {phase}", (20, 150),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
                    cv2.putText(frame, f"Reps: {reps}", (20, 185),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 0), 2)

                    y_offset = 220
                    for msg in feedback:
                        cv2.putText(frame, msg, (20, y_offset),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)
                        y_offset += 30

            if self.display:
                cv2.imshow(window_name, frame)
                key = cv2.waitKey(1) & 0xFF
                if key == 27:  # ESC
                    break

        cap.release()
        if self.display:
            cv2.destroyAllWindows()
        if log_file:
            log_file.close()
