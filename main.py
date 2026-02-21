from src.pose.pose_detector import PoseDetector

# EXERCISE = "squat"      # "squat" | "pushup" | "plank"
# SOURCE = 0             # 0 for webcam, or "path/to/video.mp4" for video file

# For demonstration, we'll keep it flexible
EXERCISE = "plank"
SOURCE = "data/selected/plank/plank_7.mp4"# Default to your video

detector = PoseDetector(exercise=EXERCISE)
detector.run_video(SOURCE)
