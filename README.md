# Real-Time Exercise Form Assessment Using Adaptive Pose


Real-time exercise form assessment using adaptive pose-based joint angle analysis under unconstrained environments.
This project implements a system for real-time exercise form assessment using adaptive pose estimation.

## Project Structure

- `src/`: Core source code for pose detection and exercise evaluation.
  - `pose/`: Pose detection modules.
  - `evaluation/`: Form checking and exercise-specific logic (Push-ups, Squats, Planks, etc.).
  - `utils/`: Utility functions.
- `configs/`: Configuration files for the models and exercises.
- `experiments/`: Scripts for running experiments and plotting results.
- `main.py`: Entry point for the application.
- `requirements.txt`: Python dependencies.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the application:
   ```bash
   python main.py
   ```

## Note on Data

The large `data/` and `outputs/` directories are currently not included in the repository due to size constraints.
