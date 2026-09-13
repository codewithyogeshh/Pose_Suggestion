import cv2
import numpy as np
import streamlit as st
import os, time, glob, io, hashlib, json, base64
from PIL import Image
from pose_engine import PoseDetector, get_pose_angles, get_feedback, get_all_poses

st.set_page_config(page_title="AI Pose Suggestion & Camera", page_icon="📸", layout="wide")
os.makedirs("assets/captures", exist_ok=True)
os.makedirs("assets/poses", exist_ok=True)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap');
html, body, [class*="css"] {font-family:'Outfit',sans-serif;}
.main-header{font-size:3rem;font-weight:800;background:linear-gradient(45deg,#00FFCC,#0077FF);-webkit-background-clip:text;-webkit-text-fill-color:transparent;}
.card{background:#1E1E24;border-radius:12px;padding:1.5rem;border:1px solid #2D2D35;margin-bottom:1rem;}
</style>
""", unsafe_allow_html=True)

if "captured_image_info" not in st.session_state: st.session_state.captured_image_info = None
if "processed_state_key" not in st.session_state: st.session_state.processed_state_key = None

def generate_silhouette_preview(landmarks, transparent=False):
    from pose_engine.detector import POSE_CONNECTIONS
    canvas=np.zeros((480,640,4),dtype=np.uint8) if transparent else np.zeros((300,300,3),dtype=np.uint8)
    if not landmarks: return canvas
    h,w,_=canvas.shape
    pts={x["id"]:(int(x["x"]*w),int(x["y"]*h)) for x in landmarks}
    lc=(0,255,204,255) if transparent else (0,255,204)
    pc=(255,255,255,255) if transparent else (255,255,255)
    for a,b in POSE_CONNECTIONS:
        if a in pts and b in pts: cv2.line(canvas,pts[a],pts[b],lc,4 if transparent else 2,cv2.LINE_AA)
    for p in pts.values(): cv2.circle(canvas,p,6 if transparent else 3,pc,-1,cv2.LINE_AA)
    return canvas

def analyze_image(file_bytes, pose_data):
    image=Image.open(io.BytesIO(file_bytes)).convert("RGB")
    bgr=cv2.cvtColor(np.array(image),cv2.COLOR_RGB2BGR)
    detector=PoseDetector(); detector.process_frame(bgr); lm=detector.find_landmarks(bgr,draw=False)
    if lm:
        score,suggestions,status=get_feedback(get_pose_angles(lm),pose_data["angles"])
    else:
        score,suggestions,status=0,["No pose detected. Make sure your full body is visible."],{}
    clean=bgr.copy(); analysed=bgr.copy()
    detector.draw_guide_silhouette(analysed,pose_data.get("landmarks",[]),color=(150,150,150),thickness=2)
    if lm:
        color=(0,255,0) if score>=80 else ((0,255,255) if score>=50 else (0,0,255))
        detector.find_landmarks(analysed,draw=True,draw_connections=True,color=color)
    ts=int(time.time())
    raw=f"assets/captures/raw_{ts}.png"; out=f"assets/captures/analysed_{ts}.png"
    cv2.imwrite(raw,clean); cv2.imwrite(out,analysed)
    return ts,score,suggestions,status,raw,out

def main():
    st.markdown('<div class="main-header">PoseGenie AI 📸</div>',unsafe_allow_html=True)
    st.markdown("Strike the perfect pose with real-time AI guidance and feedback")
    poses=get_all_poses(); names=list(poses.keys())
    selected=st.sidebar.selectbox("Choose a target pose:",names)
    pose=poses[selected]
    st.sidebar.markdown("### Pose Details")
    st.sidebar.write(pose["description"])
    st.sidebar.image(generate_silhouette_preview(pose.get("landmarks",[])),channels="BGR",width="stretch")
    guide,gallery,custom=st.tabs(["🎯 Pose Guide & Camera","🖼️ My Photo Gallery","➕ Create Custom Pose"])
    with guide:
        c1,c2=st.columns(2)
        with c1:
            st.markdown('<div class="card"><h3>How it works</h3>1. Select a target pose.<br>2. Use the camera or upload a photo.<br>3. AI detects pose landmarks.<br>4. Get alignment score and feedback.</div>',unsafe_allow_html=True)
            method=st.radio("Input Method",["📷 Use Browser Camera","📤 Upload Photo"])
            f=st.camera_input("Strike your pose!") if method.startswith("📷") else st.file_uploader("Upload an image",type=["png","jpg","jpeg"])
            if f is not None:
                key=(hashlib.md5(f.getvalue()).hexdigest(),selected)
                if st.session_state.processed_state_key!=key:
                    with st.spinner("Analyzing pose..."):
                        try:
                            result=analyze_image(f.getvalue(),pose)
                            ts,score,suggestions,status,raw,out=result
                            st.session_state.captured_image_info={"timestamp":ts,"pose_name":selected,"score":score,"suggestions":suggestions,"status_dict":status,"raw_image":raw,"analysed_image":out}
                            st.session_state.processed_state_key=key
                            st.success("Pose analysis completed successfully!")
                        except Exception as e: st.error(f"Error processing image: {e}")
        with c2:
            info=st.session_state.captured_image_info
            if info:
                a,b=st.tabs(["✨ Final Photo","📊 AI Skeleton Analysis"])
                with a: st.image(info["raw_image"],width="stretch")
                with b: st.image(info["analysed_image"],width="stretch")
                st.markdown(f"### Alignment Accuracy: **{info['score']}%**")
                st.progress(info["score"]/100)
                for s in info["suggestions"]: st.write("📢",s)
            else: st.info("Capture or upload a photo to start analysis!")
    with gallery:
        photos=sorted(glob.glob("assets/captures/raw_*.png"),reverse=True)
        if not photos: st.info("No captured photos yet.")
        else:
            cols=st.columns(3)
            for i,p in enumerate(photos):
                with cols[i%3]:
                    st.image(p,width="stretch")
                    st.download_button("💾 Download",open(p,"rb").read(),file_name=os.path.basename(p),mime="image/png",key=f"dl_{i}")
    with custom:
        st.markdown("### ➕ Record & Create a Custom Pose")
        name=st.text_input("Pose Name"); desc=st.text_area("Pose Description")
        f=st.camera_input("Strike your custom pose!",key="custom_camera")
        if f is not None and name.strip():
            try:
                image=Image.open(io.BytesIO(f.getvalue())).convert("RGB"); bgr=cv2.cvtColor(np.array(image),cv2.COLOR_RGB2BGR)
                detector=PoseDetector(); detector.process_frame(bgr); lm=detector.find_landmarks(bgr,draw=False)
                if lm:
                    preview=bgr.copy(); detector.find_landmarks(preview,draw=True,draw_connections=True,color=(0,255,204)); st.image(preview,channels="BGR")
                    if st.button("💾 Save Custom Pose"):
                        path="assets/poses/custom_poses.json"; data={}
                        if os.path.exists(path):
                            with open(path) as x: data=json.load(x)
                        data[name.strip()]={"description":desc.strip() or f"Custom pose: {name.strip()}","angles":get_pose_angles(lm),"landmarks":[{"id":x[0],"x":x[3],"y":x[4],"vis":x[6]} for x in lm],"recorded_at":time.strftime("%Y-%m-%d %H:%M:%S")}
                        with open(path,"w") as x: json.dump(data,x,indent=4)
                        st.success("Custom pose saved!")
                else: st.error("No pose detected. Make sure your full body is visible.")
            except Exception as e: st.error(f"Error: {e}")

if __name__=="__main__": main()
