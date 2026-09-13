# Pose Suggestion

AI Pose Assistant is a Python-based ML project that analyzes a user's posture through the camera and provides real-time pose suggestions for better photographs. Using computer vision and pose estimation, it guides users to adjust their stance, hand placement, and body alignment to capture confident and visually appealing photos.

## Features
- Real-time camera or image upload
- MediaPipe pose landmark detection
- Pose angle comparison and alignment score
- Feedback for elbows, shoulders, hips and knees
- Built-in pose library
- Custom pose recording
- Captured-photo gallery

## Run locally
```bash
pip install -r requirements.txt
streamlit run app.py
```

The MediaPipe pose model is downloaded automatically when needed.

## Source
This project is based on the public `CAM_Pose_SuggestorAI` project by `SwastikBiswas26` and has been copied into this repository for development on `codewithyogeshh`.
