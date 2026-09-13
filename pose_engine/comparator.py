import numpy as np

def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    if angle > 180.0:
        angle = 360.0 - angle
    return angle

def get_pose_angles(lm_list):
    if not lm_list or len(lm_list) < 33:
        return {}
    points = {item[0]: [item[3], item[4]] for item in lm_list}
    angles = {}
    try:
        angles['left_elbow'] = calculate_angle(points[11], points[13], points[15])
        angles['right_elbow'] = calculate_angle(points[12], points[14], points[16])
        angles['left_shoulder'] = calculate_angle(points[23], points[11], points[13])
        angles['right_shoulder'] = calculate_angle(points[24], points[12], points[14])
        angles['left_hip'] = calculate_angle(points[11], points[23], points[25])
        angles['right_hip'] = calculate_angle(points[12], points[24], points[26])
        angles['left_knee'] = calculate_angle(points[23], points[25], points[27])
        angles['right_knee'] = calculate_angle(points[24], points[26], points[28])
    except KeyError:
        pass
    return angles

def get_feedback(user_angles, target_angles, tolerance=20.0):
    feedback_list = []
    status_dict = {}
    total_score = 0.0
    joints_compared = 0
    joint_names = {
        'left_elbow': 'left elbow', 'right_elbow': 'right elbow',
        'left_shoulder': 'left shoulder', 'right_shoulder': 'right shoulder',
        'left_hip': 'left hip', 'right_hip': 'right hip',
        'left_knee': 'left knee', 'right_knee': 'right knee'
    }
    for joint, target_val in target_angles.items():
        if joint not in user_angles:
            continue
        user_val = user_angles[joint]
        diff = user_val - target_val
        abs_diff = abs(diff)
        joint_score = max(0.0, 100.0 - (abs_diff / 45.0) * 100.0)
        total_score += joint_score
        joints_compared += 1
        if abs_diff <= tolerance:
            status_dict[joint] = 'GOOD'
        elif abs_diff <= tolerance * 2:
            status_dict[joint] = 'CLOSE'
            feedback_list.append(f"Adjust your {joint_names[joint]} slightly")
        else:
            status_dict[joint] = 'ADJUST'
            if 'elbow' in joint or 'knee' in joint or 'hip' in joint:
                feedback_list.append(f"{'Bend' if diff > 0 else 'Straighten'} your {joint_names[joint]} more")
            elif 'shoulder' in joint:
                feedback_list.append(f"{'Lower' if diff > 0 else 'Raise'} your {joint_names[joint]} arm")
    overall_score = (total_score / joints_compared) if joints_compared > 0 else 0.0
    if not feedback_list and overall_score >= 85:
        feedback_list.append("Pose matches perfectly! Click the photo now!")
    return int(overall_score), feedback_list, status_dict
