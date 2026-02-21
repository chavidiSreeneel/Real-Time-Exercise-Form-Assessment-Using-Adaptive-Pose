import os
import sys
import glob

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.pose.pose_detector import PoseDetector

def run_batch(exercise, folder):
    print(f"\n--- Starting Batch Processing for {exercise} in {folder} ---")
    videos = glob.glob(os.path.join(folder, "*.mp4"))
    if not videos:
        print("No videos found in:", folder)
        return

    # Process each video
    for v in videos:
        print(f"Processing: {os.path.basename(v)}")
        # Initialize a new detector per video to reset states (reps/phase)
        detector = PoseDetector(exercise=exercise, display=False)
        detector.run_video(v)
    
    print(f"--- Finished Batch Processing for {exercise} ---")

if __name__ == "__main__":
    # Run squats batch
    # run_batch("squat", "data/selected/squat")
    run_batch("push-up", "data/selected/push-up")
    run_batch("plank", "data/selected/plank")
    
    # Run pushups batch
    # run_batch("pushup", "data/selected/pushup")
    
    # Run planks batch
    # run_batch("plank", "data/selected/plank")
