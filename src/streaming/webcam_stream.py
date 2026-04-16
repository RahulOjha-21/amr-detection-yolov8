"""
AMR Detection System - app.py
Automated detection of Antimicrobial Resistance from images and live camera streams.
Developed by Rahul | Powered by YOLOv8 + Streamlit
"""

import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image
import time
import datetime
import io
import os

# ─────────────────────────────────────────
# Page Configuration
# ─────────────────────────────────────────
st.set_page_config(
    page_title="AMR Detection System",
    layout="wide",
    page_icon="🦠",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────
# Custom CSS — Industrial / Scientific Theme
# ─────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

/* ── Background ── */
.stApp {
    background-color: #0d1117;
    color: #e6edf3;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #161b22;
    border-right: 1px solid #30363d;
}
section[data-testid="stSidebar"] * {
    color: #c9d1d9 !important;
}
section[data-testid="stSidebar"] .stMarkdown h2 {
    color: #58a6ff !important;
    font-size: 14px;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}

/* ── Section Headers ── */
h1 { 
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 2rem !important;
    color: #58a6ff !important;
    letter-spacing: -0.02em;
}
h2 { 
    color: #79c0ff !important;
    font-size: 1.1rem !important;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border-bottom: 1px solid #21262d;
    padding-bottom: 8px;
    margin-top: 2rem !important;
}
h3 { color: #8b949e !important; font-size: 0.9rem !important; }

/* ── Cards ── */
.amr-card {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 1.25rem 1.5rem;
    margin-bottom: 1rem;
}
.amr-card-accent {
    border-left: 3px solid #58a6ff;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 8px;
    padding: 12px 16px;
}
[data-testid="stMetricValue"] {
    color: #58a6ff !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 1.8rem !important;
}
[data-testid="stMetricLabel"] {
    color: #8b949e !important;
    font-size: 0.75rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
}

/* ── Buttons ── */
.stButton > button {
    background-color: #21262d;
    color: #c9d1d9;
    border: 1px solid #30363d;
    border-radius: 6px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.85rem;
    letter-spacing: 0.04em;
    transition: all 0.15s ease;
    padding: 0.5rem 1rem;
}
.stButton > button:hover {
    background-color: #388bfd1a;
    border-color: #58a6ff;
    color: #58a6ff;
}
.stButton > button:active {
    background-color: #1f6feb;
    color: #ffffff;
    border-color: #1f6feb;
}

/* ── Primary action button ── */
.stButton > button[kind="primary"] {
    background-color: #238636;
    border-color: #2ea043;
    color: #ffffff;
    font-weight: 600;
}
.stButton > button[kind="primary"]:hover {
    background-color: #2ea043;
    border-color: #3fb950;
    color: #ffffff;
}

/* ── Inputs ── */
.stTextInput > div > div > input,
.stSelectbox > div > div,
.stSlider {
    background-color: #0d1117 !important;
    border: 1px solid #30363d !important;
    color: #c9d1d9 !important;
    border-radius: 6px !important;
    font-family: 'IBM Plex Mono', monospace !important;
}

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #161b22;
    border: 1px dashed #30363d;
    border-radius: 8px;
    padding: 1rem;
}

/* ── Alerts ── */
.stSuccess { background-color: #0f2d1a !important; border-color: #2ea043 !important; }
.stWarning { background-color: #2d1f00 !important; border-color: #d29922 !important; }
.stError   { background-color: #2d0f0f !important; border-color: #f85149 !important; }

/* ── Log panel ── */
.log-entry {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    line-height: 1.6;
    padding: 2px 0;
    border-bottom: 1px solid #21262d;
}
.log-info    { color: #8b949e; }
.log-success { color: #3fb950; }
.log-warning { color: #d29922; }
.log-error   { color: #f85149; }

/* ── Expander ── */
.streamlit-expanderHeader {
    background-color: #161b22 !important;
    border: 1px solid #30363d !important;
    border-radius: 6px !important;
    color: #8b949e !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.82rem !important;
}

/* ── Status badge ── */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 3px 10px;
    border-radius: 20px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem;
    font-weight: 600;
}
.status-ready { background: #0f2d1a; color: #3fb950; border: 1px solid #2ea043; }
.status-error { background: #2d0f0f; color: #f85149; border: 1px solid #f85149; }

/* ── Divider ── */
hr { border-color: #21262d !important; }

/* ── Tab styling ── */
.stTabs [data-baseweb="tab-list"] {
    background: #161b22;
    border-bottom: 1px solid #30363d;
    gap: 0;
}
.stTabs [data-baseweb="tab"] {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.82rem;
    color: #8b949e;
    padding: 8px 20px;
    border-bottom: 2px solid transparent;
}
.stTabs [aria-selected="true"] {
    color: #58a6ff !important;
    border-bottom: 2px solid #58a6ff !important;
    background: transparent !important;
}
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────
# Session State Initialization
# ─────────────────────────────────────────
defaults = {
    "captured_image": None,
    "uploaded_image": None,
    "last_frame": None,
    "live_logs": [],
    "stream_active": False,
    "prediction_result": None,
    "detection_count": 0,
    "confidence_scores": [],
    "class_names": [],
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ─────────────────────────────────────────
# Logging Utility
# ─────────────────────────────────────────
def log_event(msg: str, level: str = "INFO"):
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    st.session_state.live_logs.append({
        "text": f"[{timestamp}]  {msg}",
        "level": level,
    })
    if len(st.session_state.live_logs) > 50:
        st.session_state.live_logs = st.session_state.live_logs[-50:]


# ─────────────────────────────────────────
# Model Loader (cached)
# ─────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model(model_path: str) -> YOLO:
    return YOLO(model_path)


# ─────────────────────────────────────────
# Sidebar
# ─────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🦠 AMR Detection")
    st.markdown("---")

    # Model status
    MODEL_PATH = "Models/best.pt"
    model = None
    model_status_html = ""

    try:
        model = load_model(MODEL_PATH)
        model_status_html = "<span class='status-badge status-ready'>● Model Ready</span>"
        log_event(f"YOLO model loaded: {MODEL_PATH}", level="SUCCESS")
    except Exception as e:
        model_status_html = "<span class='status-badge status-error'>✕ Model Error</span>"
        log_event(f"Model load failed: {e}", level="ERROR")

    st.markdown(model_status_html, unsafe_allow_html=True)
    st.markdown("")

    # Detection settings
    st.markdown("## ⚙️ Detection Settings")
    conf_threshold = st.slider("Confidence Threshold", 0.1, 1.0, 0.4, 0.05,
                               help="Minimum confidence score to display a detection")
    iou_threshold = st.slider("IoU Threshold (NMS)", 0.1, 1.0, 0.45, 0.05,
                              help="Intersection-over-Union threshold for non-max suppression")
    max_det = st.number_input("Max Detections", 1, 300, 50,
                              help="Maximum number of detections per image")

    st.markdown("---")
    st.markdown("## 📡 Camera Settings")
    camera_url = st.text_input(
        "Stream URL",
        value="http://10.130.168.235:8080/video",
        help="IP camera stream URL, or enter 0 for local webcam",
        placeholder="http://<ip>:<port>/video or 0"
    )

    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.75rem; color:#484f58; line-height:1.8;'>
    Developed by <strong style='color:#8b949e'>Rahul</strong><br>
    YOLOv8 · OpenCV · Streamlit<br><br>
    <a href='https://github.com/' style='color:#58a6ff;'>GitHub ↗</a> &nbsp;·&nbsp;
    <a href='https://docs.ultralytics.com/' style='color:#58a6ff;'>YOLO Docs ↗</a>
    </div>
    """, unsafe_allow_html=True)


# ─────────────────────────────────────────
# Header
# ─────────────────────────────────────────
st.markdown("""
<div style='padding: 1.5rem 0 0.5rem 0;'>
  <h1>AMR Detection System</h1>
  <p style='color:#8b949e; font-size:0.95rem; margin-top: -0.5rem;'>
    Automated Antimicrobial Resistance detection · YOLOv8 · Real-time inference
  </p>
</div>
""", unsafe_allow_html=True)

if model is None:
    st.error("⚠️ YOLO model could not be loaded. Place `best.pt` inside the `Models/` directory and restart.")
    st.stop()

# ─────────────────────────────────────────
# Metrics Row
# ─────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Model", "YOLOv8", delta=None)
with m2:
    total_classes = len(model.names) if hasattr(model, "names") and model.names else "—"
    st.metric("Classes", total_classes)
with m3:
    st.metric("Last Detection Count", st.session_state.detection_count)
with m4:
    avg_conf = (
        f"{np.mean(st.session_state.confidence_scores):.2f}"
        if st.session_state.confidence_scores else "—"
    )
    st.metric("Avg Confidence", avg_conf)

st.markdown("---")

# ─────────────────────────────────────────
# Main Tabs
# ─────────────────────────────────────────
tab_stream, tab_upload, tab_results = st.tabs(["📹  Live Stream", "🖼️  Upload Image", "📊  Results & Logs"])


# ═══════════════════════════════════════════
# TAB 1 — Live Stream
# ═══════════════════════════════════════════
with tab_stream:
    st.markdown("## Live Camera Stream")
    st.markdown("""
    <div class='amr-card amr-card-accent'>
    Connect to a webcam or IP camera stream. Capture any frame for analysis.
    </div>
    """, unsafe_allow_html=True)

    col_a, col_b, col_c = st.columns([2, 1, 1])
    with col_a:
        st.markdown(f"**Stream URL:** `{camera_url}`")
    with col_b:
        start_btn = st.button("▶  Start Stream", use_container_width=True)
    with col_c:
        stop_btn = st.button("⏹  Stop Stream", use_container_width=True)

    if start_btn:
        st.session_state.stream_active = True
        log_event(f"Stream started → {camera_url}")

    if stop_btn:
        st.session_state.stream_active = False
        log_event("Stream stopped by user.")

    capture_col, _ = st.columns([1, 3])
    with capture_col:
        capture_btn = st.button("📸  Capture Frame", use_container_width=True,
                                disabled=not st.session_state.stream_active)

    if st.session_state.stream_active:
        stream_placeholder = st.empty()
        status_placeholder = st.empty()

        # Resolve URL (support integer for local webcam)
        raw_url = camera_url.strip()
        resolved_url = int(raw_url) if raw_url.isdigit() else raw_url

        cap = cv2.VideoCapture(resolved_url)
        if not cap.isOpened():
            st.error("Cannot open stream. Verify the URL or camera connection.")
            log_event("Failed to open video capture.", level="ERROR")
            st.session_state.stream_active = False
        else:
            error_count = 0
            while st.session_state.stream_active:
                ret, frame = cap.read()
                if not ret:
                    error_count += 1
                    if error_count > 15:
                        st.session_state.stream_active = False
                        st.error("Stream disconnected after repeated read failures.")
                        log_event("Stream disconnected (15 consecutive read failures).", level="ERROR")
                        break
                    time.sleep(0.05)
                    continue

                error_count = 0
                st.session_state.last_frame = frame.copy()

                # Show live feed
                display_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                stream_placeholder.image(display_frame, caption="Live Feed", use_container_width=True)
                status_placeholder.markdown(
                    f"<span style='color:#3fb950; font-family:monospace; font-size:0.8rem;'>● STREAMING</span>",
                    unsafe_allow_html=True
                )

                if capture_btn:
                    st.session_state.captured_image = frame.copy()
                    st.session_state.stream_active = False
                    log_event("Frame captured from live stream.")
                    break

                time.sleep(0.033)  # ~30 fps target

            cap.release()

    if st.session_state.captured_image is not None:
        st.markdown("### Captured Frame")
        preview = cv2.cvtColor(st.session_state.captured_image, cv2.COLOR_BGR2RGB)
        st.image(preview, use_container_width=True)
        st.info("Frame ready for prediction. Switch to **Upload Image** tab or run prediction below.")


# ═══════════════════════════════════════════
# TAB 2 — Upload Image
# ═══════════════════════════════════════════
with tab_upload:
    st.markdown("## Upload Image for Analysis")
    st.markdown("""
    <div class='amr-card amr-card-accent'>
    Supported formats: JPG, JPEG, PNG. Upload a microscopy or culture plate image for AMR detection.
    </div>
    """, unsafe_allow_html=True)

    uploaded_file = st.file_uploader(
        "Drop an image here or click to browse",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed",
    )

    if uploaded_file is not None:
        try:
            img = Image.open(uploaded_file).convert("RGB")
            st.session_state.uploaded_image = np.array(img)
            log_event(f"Image uploaded: {uploaded_file.name} ({img.size[0]}×{img.size[1]}px)")
            st.image(img, caption=f"{uploaded_file.name}  ·  {img.size[0]}×{img.size[1]} px",
                     use_container_width=True)
        except Exception as e:
            st.error(f"Failed to open image: {e}")
            log_event(f"Image open error: {e}", level="ERROR")

    # ── Prediction ────────────────────────
    st.markdown("## Run Prediction")

    # Resolve active image source (priority: upload > captured > last frame)
    def get_active_image():
        if st.session_state.uploaded_image is not None:
            return st.session_state.uploaded_image, "Uploaded image"
        if st.session_state.captured_image is not None:
            return cv2.cvtColor(st.session_state.captured_image, cv2.COLOR_BGR2RGB), "Captured frame"
        if st.session_state.last_frame is not None:
            return cv2.cvtColor(st.session_state.last_frame, cv2.COLOR_BGR2RGB), "Last stream frame"
        return None, None

    active_img, img_source = get_active_image()

    if active_img is not None:
        st.markdown(f"<small style='color:#8b949e;'>Source: {img_source}</small>", unsafe_allow_html=True)

    run_col, clear_col = st.columns([2, 1])
    with run_col:
        predict_btn = st.button(
            "🚀  Run Detection",
            use_container_width=True,
            type="primary",
            disabled=(active_img is None),
        )
    with clear_col:
        if st.button("🗑  Clear Image", use_container_width=True):
            st.session_state.uploaded_image = None
            st.session_state.captured_image = None
            st.session_state.prediction_result = None
            st.session_state.detection_count = 0
            st.session_state.confidence_scores = []
            st.session_state.class_names = []
            log_event("Session images cleared.")
            st.rerun()

    if active_img is None:
        st.warning("No image available. Upload an image or capture a frame from the live stream.")

    if predict_btn and active_img is not None:
        with st.spinner("Running inference…"):
            try:
                log_event(f"Prediction started  [conf={conf_threshold}  iou={iou_threshold}  max_det={max_det}]")
                results = model.predict(
                    active_img,
                    conf=conf_threshold,
                    iou=iou_threshold,
                    max_det=int(max_det),
                    verbose=False,
                )
                result = results[0]

                # Annotated frame (already RGB from model.predict on RGB input)
                annotated = result.plot()  # returns BGR
                annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
                st.session_state.prediction_result = annotated_rgb

                # Parse detections
                boxes = result.boxes
                if boxes is not None and len(boxes):
                    confs = boxes.conf.cpu().numpy().tolist()
                    cls_ids = boxes.cls.cpu().numpy().astype(int).tolist()
                    cls_names = [model.names[c] for c in cls_ids]
                    st.session_state.detection_count = len(confs)
                    st.session_state.confidence_scores = confs
                    st.session_state.class_names = cls_names
                else:
                    st.session_state.detection_count = 0
                    st.session_state.confidence_scores = []
                    st.session_state.class_names = []

                log_event(
                    f"Prediction complete — {st.session_state.detection_count} detection(s) found.",
                    level="SUCCESS"
                )

            except Exception as e:
                st.error(f"Prediction failed: {e}")
                log_event(f"Prediction error: {e}", level="ERROR")

    # Show quick result preview if available
    if st.session_state.prediction_result is not None:
        st.markdown("### Detection Output")
        st.image(st.session_state.prediction_result, use_container_width=True)

        # Download button
        result_pil = Image.fromarray(st.session_state.prediction_result)
        buf = io.BytesIO()
        result_pil.save(buf, format="PNG")
        st.download_button(
            label="⬇  Download Result",
            data=buf.getvalue(),
            file_name=f"amr_result_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
            mime="image/png",
        )


# ═══════════════════════════════════════════
# TAB 3 — Results & Logs
# ═══════════════════════════════════════════
with tab_results:
    st.markdown("## Detection Results")

    if st.session_state.prediction_result is not None:
        rc1, rc2 = st.columns([3, 2])
        with rc1:
            st.image(st.session_state.prediction_result,
                     caption="Latest Detection Result", use_container_width=True)

        with rc2:
            st.markdown("### Detection Summary")
            det_count = st.session_state.detection_count

            if det_count == 0:
                st.info("No detections found above the confidence threshold.")
            else:
                confs = st.session_state.confidence_scores
                names = st.session_state.class_names

                # Summary metrics
                sm1, sm2 = st.columns(2)
                sm1.metric("Detections", det_count)
                sm2.metric("Avg Confidence", f"{np.mean(confs):.2%}")

                # Per-detection table
                st.markdown("#### Individual Detections")
                rows = []
                for i, (name, conf) in enumerate(zip(names, confs), 1):
                    conf_bar = "█" * int(conf * 10) + "░" * (10 - int(conf * 10))
                    rows.append(f"`{i:02d}` **{name}** — `{conf:.2%}` `{conf_bar}`")
                st.markdown("\n\n".join(rows))
    else:
        st.info("No prediction has been run yet. Upload an image and click **Run Detection**.")

    st.markdown("---")
    st.markdown("## System Logs")

    log_col, btn_col = st.columns([5, 1])
    with btn_col:
        if st.button("Clear Logs", use_container_width=True):
            st.session_state.live_logs = []
            st.rerun()

    log_level_map = {
        "SUCCESS": ("log-success", "✓"),
        "WARNING": ("log-warning", "⚠"),
        "ERROR":   ("log-error",   "✕"),
        "INFO":    ("log-info",    "·"),
    }

    if st.session_state.live_logs:
        with st.container():
            log_html = "<div style='background:#0d1117; border:1px solid #21262d; border-radius:6px; padding:12px; max-height:350px; overflow-y:auto;'>"
            for entry in reversed(st.session_state.live_logs):
                level = entry.get("level", "INFO")
                css_class, icon = log_level_map.get(level, ("log-info", "·"))
                log_html += f"<div class='log-entry {css_class}'>{icon}  {entry['text']}</div>"
            log_html += "</div>"
            st.markdown(log_html, unsafe_allow_html=True)
    else:
        st.markdown("<span style='color:#484f58; font-size:0.85rem;'>No log entries yet.</span>",
                    unsafe_allow_html=True)