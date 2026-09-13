import cv2
import numpy as np
import os
import urllib.request
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

POSE_CONNECTIONS = [
    (0, 1), (1, 2), (2, 3), (0, 4), (4, 5), (5, 6),
    (11, 12), (11, 23), (12, 24), (23, 24),
    (11, 13), (13, 15), (12, 14), (14, 16),
    (23, 25), (25, 27), (27, 31), (27, 29), (29, 31),
    (24, 26), (26, 28), (28, 32), (28, 30), (30, 32)
]

class PoseDetector:
    def __init__(self, model_name="pose_landmarker_full.task", detection_con=0.5, tracking_con=0.5):
        self.model_path = os.path.join(os.path.dirname(__file__), model_name)
        self.download_model_if_missing(model_name)
        base_options = python.BaseOptions(model_asset_path=self.model_path)
        options = vision.PoseLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.IMAGE,
            output_segmentation_masks=False,
            min_pose_detection_confidence=detection_con,
            min_pose_presence_confidence=tracking_con
        )
        self.landmarker = vision.PoseLandmarker.create_from_options(options)
        self.results = None

    def download_model_if_missing(self, model_name):
        if not os.path.exists(self.model_path):
            print(f"Downloading {model_name} from Google APIs...")
            os.makedirs(os.path.dirname(self.model_path), exist_ok=True)
            url = f"https://storage.googleapis.com/mediapipe-models/pose_landmarker/pose_landmarker_full/float16/1/{model_name}"
            try:
                urllib.request.urlretrieve(url, self.model_path)
                print("Model downloaded successfully.")
            except Exception as e:
                print(f"Error downloading model: {e}")
                self.model_path = model_name
                if not os.path.exists(self.model_path):
                    urllib.request.urlretrieve(url, self.model_path)

    def process_frame(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=img_rgb)
        self.results = self.landmarker.detect(mp_image)
        return self.results

    def find_landmarks(self, img, draw=False, draw_connections=True, color=(0, 255, 0)):
        lm_list = []
        if not self.results or not self.results.pose_landmarks:
            return lm_list
        h, w, c = img.shape
        landmarks = self.results.pose_landmarks[0]
        for idx, lm in enumerate(landmarks):
            cx, cy = int(lm.x * w), int(lm.y * h)
            lm_list.append([idx, cx, cy, lm.x, lm.y, lm.z, lm.visibility])
        if draw:
            if draw_connections:
                for start_idx, end_idx in POSE_CONNECTIONS:
                    if start_idx < len(lm_list) and end_idx < len(lm_list):
                        if lm_list[start_idx][6] > 0.4 and lm_list[end_idx][6] > 0.4:
                            cv2.line(img, (lm_list[start_idx][1], lm_list[start_idx][2]), (lm_list[end_idx][1], lm_list[end_idx][2]), color, 3)
            for item in lm_list:
                idx, cx, cy, _, _, _, vis = item
                if vis > 0.4:
                    cv2.circle(img, (cx, cy), 5, (255, 255, 255), cv2.FILLED)
                    cv2.circle(img, (cx, cy), 7, color, 2)
        return lm_list

    def draw_guide_silhouette(self, img, landmarks_template, color=(180, 180, 180), thickness=2):
        if not landmarks_template:
            return
        h, w, c = img.shape
        pts = {lm["id"]: (int(lm["x"] * w), int(lm["y"] * h)) for lm in landmarks_template}
        for start_idx, end_idx in POSE_CONNECTIONS:
            if start_idx in pts and end_idx in pts:
                cv2.line(img, pts[start_idx], pts[end_idx], color, thickness, lineType=cv2.LINE_AA)
        for pt in pts.values():
            cv2.circle(img, pt, 4, color, -1, lineType=cv2.LINE_AA)
