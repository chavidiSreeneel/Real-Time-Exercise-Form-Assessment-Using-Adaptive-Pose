import pandas as pd
import matplotlib.pyplot as plt
import glob
import os
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

def plot_video_results(csv_path):
    df = pd.read_csv(csv_path)
    video_name = os.path.basename(csv_path).replace('.csv', '')
    
    # Create the graphics directory if it doesn't exist
    graphics_dir = os.path.join("outputs", "graphics")
    os.makedirs(graphics_dir, exist_ok=True)

    # Convert timestamps to relative time in seconds
    df['time_rel'] = df['timestamp'] - df['timestamp'].iloc[0]

    # 1. Joint Angle Plot (Knee & Torso for squats)
    plt.figure(figsize=(12, 6))
    if 'squat' in video_name:
        plt.plot(df['time_rel'], df['knee'], label='Knee Angle', color='blue')
        plt.plot(df['time_rel'], df['torso'], label='Torso Angle', color='green', alpha=0.5)
        plt.ylabel('Angle (Degrees)')
    elif 'pushup' in csv_path:
        plt.plot(df['time_rel'], df['elbow'], label='Elbow Angle', color='red')
        plt.plot(df['time_rel'], df['body_line'], label='Body Alignment', color='purple', alpha=0.5)
        plt.ylabel('Angle (Degrees)')
    
    plt.title(f'Joint Angles Over Time - {video_name}')
    plt.xlabel('Time (seconds)')
    plt.legend()
    plt.grid(True)
    plt.savefig(os.path.join(graphics_dir, f'{video_name}_angles.png'))
    plt.close()

    # 2. FPS Analysis
    plt.figure(figsize=(10, 4))
    plt.plot(df['time_rel'], df['fps'], color='orange')
    plt.title(f'Processing FPS - {video_name}')
    plt.xlabel('Time (seconds)')
    plt.ylabel('FPS')
    plt.grid(True)
    plt.savefig(os.path.join(graphics_dir, f'{video_name}_fps.png'))
    plt.close()

    print(f"Generated graphs for: {video_name}")

def main():
    logs = glob.glob("outputs/logs/*.csv")
    if not logs:
        print("No log files found in outputs/logs/")
        return
    
    for log in logs:
        plot_video_results(log)

if __name__ == "__main__":
    main()
