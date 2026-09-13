import os
import json

BUILTIN_POSES = {
    "Casual Standing (Left Hand on Hip)": {
        "description": "Stand straight, place your left hand on your hip, and let your right arm hang casually down.",
        "angles": {"left_elbow":100.0,"right_elbow":170.0,"left_shoulder":35.0,"right_shoulder":15.0,"left_hip":175.0,"right_hip":175.0,"left_knee":175.0,"right_knee":175.0},
        "landmarks": [
            {"id":0,"x":.5,"y":.15},{"id":11,"x":.43,"y":.28},{"id":12,"x":.57,"y":.28},{"id":13,"x":.35,"y":.38},{"id":14,"x":.60,"y":.44},{"id":15,"x":.42,"y":.44},{"id":16,"x":.62,"y":.60},{"id":23,"x":.45,"y":.55},{"id":24,"x":.55,"y":.55},{"id":25,"x":.45,"y":.75},{"id":26,"x":.55,"y":.75},{"id":27,"x":.45,"y":.92},{"id":28,"x":.55,"y":.92}]},
    "Arms Crossed": {
        "description": "Cross your arms over your chest, stand tall with shoulder-width stance.",
        "angles": {"left_elbow":75.0,"right_elbow":75.0,"left_shoulder":40.0,"right_shoulder":40.0,"left_hip":175.0,"right_hip":175.0,"left_knee":175.0,"right_knee":175.0},
        "landmarks": [
            {"id":0,"x":.5,"y":.15},{"id":11,"x":.42,"y":.28},{"id":12,"x":.58,"y":.28},{"id":13,"x":.35,"y":.36},{"id":14,"x":.65,"y":.36},{"id":15,"x":.54,"y":.36},{"id":16,"x":.46,"y":.36},{"id":23,"x":.45,"y":.55},{"id":24,"x":.55,"y":.55},{"id":25,"x":.45,"y":.75},{"id":26,"x":.55,"y":.75},{"id":27,"x":.45,"y":.92},{"id":28,"x":.55,"y":.92}]},
    "Hand on Chin (The Thinker)": {
        "description": "Raise your right hand to touch your chin with your right elbow bent, resting on your crossed left arm.",
        "angles": {"left_elbow":80.0,"right_elbow":45.0,"left_shoulder":35.0,"right_shoulder":75.0,"left_hip":170.0,"right_hip":170.0,"left_knee":175.0,"right_knee":175.0},
        "landmarks": [
            {"id":0,"x":.5,"y":.15},{"id":11,"x":.42,"y":.28},{"id":12,"x":.58,"y":.28},{"id":13,"x":.35,"y":.38},{"id":14,"x":.55,"y":.38},{"id":15,"x":.48,"y":.38},{"id":16,"x":.50,"y":.20},{"id":23,"x":.45,"y":.55},{"id":24,"x":.55,"y":.55},{"id":25,"x":.45,"y":.75},{"id":26,"x":.55,"y":.75},{"id":27,"x":.45,"y":.92},{"id":28,"x":.55,"y":.92}]},
    "Model Pose (Hand in Pocket)": {
        "description": "Slightly tilt your body, slide your right hand into your pocket, bent at the elbow. Keep your left hand relaxed.",
        "angles": {"left_elbow":160.0,"right_elbow":115.0,"left_shoulder":15.0,"right_shoulder":25.0,"left_hip":175.0,"right_hip":165.0,"left_knee":175.0,"right_knee":165.0},
        "landmarks": [
            {"id":0,"x":.5,"y":.15},{"id":11,"x":.43,"y":.28},{"id":12,"x":.57,"y":.28},{"id":13,"x":.38,"y":.44},{"id":14,"x":.65,"y":.38},{"id":15,"x":.38,"y":.60},{"id":16,"x":.55,"y":.50},{"id":23,"x":.45,"y":.55},{"id":24,"x":.55,"y":.55},{"id":25,"x":.44,"y":.75},{"id":26,"x":.56,"y":.74},{"id":27,"x":.44,"y":.92},{"id":28,"x":.56,"y":.90}]},
    "Victory V-Sign (Hands Up)": {
        "description": "Raise both of your arms high, forming a 'V' shape, celebrating victory!",
        "angles": {"left_elbow":165.0,"right_elbow":165.0,"left_shoulder":140.0,"right_shoulder":140.0,"left_hip":175.0,"right_hip":175.0,"left_knee":175.0,"right_knee":175.0},
        "landmarks": [
            {"id":0,"x":.5,"y":.20},{"id":11,"x":.43,"y":.38},{"id":12,"x":.57,"y":.38},{"id":13,"x":.28,"y":.23},{"id":14,"x":.72,"y":.23},{"id":15,"x":.18,"y":.10},{"id":16,"x":.82,"y":.10},{"id":23,"x":.45,"y":.65},{"id":24,"x":.55,"y":.65},{"id":25,"x":.45,"y":.80},{"id":26,"x":.55,"y":.80},{"id":27,"x":.45,"y":.95},{"id":28,"x":.55,"y":.95}]}
}

def get_all_poses():
    all_poses = BUILTIN_POSES.copy()
    path = os.path.join("assets", "poses", "custom_poses.json")
    if os.path.exists(path):
        try:
            with open(path, "r") as f:
                all_poses.update(json.load(f))
        except Exception as e:
            print(f"Error loading custom poses: {e}")
    return all_poses

POSES_LIBRARY = BUILTIN_POSES
