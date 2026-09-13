import numpy as np
from pose_engine import PoseDetector, get_pose_angles, get_feedback, POSES_LIBRARY

def test_pipeline():
    print("Testing imports and classes...")
    try:
        detector = PoseDetector()
        print("[SUCCESS] PoseDetector initialized successfully.")
    except Exception as e:
        print(f"[FAILURE] PoseDetector initialization failed: {e}")
        return False
    if not POSES_LIBRARY:
        return False
    dummy_img = np.zeros((480, 640, 3), dtype=np.uint8)
    try:
        detector.process_frame(dummy_img)
        lm_list = detector.find_landmarks(dummy_img, draw=True)
        user_angles = get_pose_angles(lm_list)
        target = POSES_LIBRARY[list(POSES_LIBRARY.keys())[0]]["angles"]
        score, feedback, status = get_feedback(user_angles, target)
        print(f"[SUCCESS] Comparator run. Score: {score}")
    except Exception as e:
        print(f"[FAILURE] {e}")
        return False
    return True

if __name__ == "__main__":
    print("All backend components are working correctly and ready!" if test_pipeline() else "Some tests failed. Check dependencies.")
