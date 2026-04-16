"""
AMR Detection System - Enhanced Streamlit Application
Automated detection of Antimicrobial Resistance from images and live camera streams.
Powered by YOLOv8 + Streamlit
"""

import sys
from pathlib import Path

# Add parent directories to path for imports to work with streamlit run
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image
import time
import datetime
import io
import os
import logging

# Import custom logger
try:
    from src.streaming.logger import get_logger, get_log_file_path
except ImportError:
    # Fallback for direct execution
    from streaming.logger import get_logger, get_log_file_path

logger = get_logger()
log_file = get_log_file_path()

# ═══════════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="AMR Detection System | YOLOv8",
    layout="wide",
    page_icon="🦠",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/yourusername/amr-detection',
        'Report a bug': "https://github.com/yourusername/amr-detection/issues",
        'About': "# AMR Detection System\nPowered by YOLOv8 • OpenCV • Streamlit"
    }
)

# ═══════════════════════════════════════════════════════════════════
# CUSTOM STYLING - MODERN DARK THEME
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto+Mono:wght@400;600&family=Roboto:wght@300;400;500;600;700&display=swap');

* {
    font-family: 'Roboto', sans-serif;
}

/* ── Main Background ── */
.stApp {
    background: linear-gradient(135deg, #0a0e27 0%, #1a1f4d 100%);
    color: #e6edf3;
}

/* ── Sidebar Styling ── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #161b22 0%, #0d1117 100%);
    border-right: 2px solid #30363d;
}

section[data-testid="stSidebar"] * {
    color: #c9d1d9 !important;
}

/* ── Headers ── */
h1 {
    font-family: 'Roboto', sans-serif !important;
    font-size: 2.5rem !important;
    color: #58a6ff !important;
    letter-spacing: -0.02em;
    font-weight: 700;
    text-shadow: 0 2px 12px rgba(88, 166, 255, 0.15);
}

h2 {
    color: #79c0ff !important;
    font-size: 1.3rem !important;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    border-bottom: 2px solid #30363d;
    padding-bottom: 12px;
    margin-top: 2.5rem !important;
    margin-bottom: 1.5rem !important;
    font-weight: 600;
}

h3 {
    color: #8b949e !important;
    font-size: 1rem !important;
    font-weight: 500;
}

/* ── Cards Container ── */
.amr-card {
    background: linear-gradient(135deg, rgba(22, 27, 34, 0.8) 0%, rgba(13, 17, 23, 0.8) 100%);
    border: 1px solid #30363d;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    backdrop-filter: blur(10px);
    box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    transition: all 0.3s ease;
}

.amr-card:hover {
    border-color: #58a6ff;
    box-shadow: 0 8px 24px rgba(88, 166, 255, 0.1);
    transform: translateY(-2px);
}

.amr-card-accent {
    border-left: 4px solid #58a6ff;
}

.amr-card-success {
    border-left: 4px solid #3fb950;
}

.amr-card-warning {
    border-left: 4px solid #d29922;
}

/* ── Metrics ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(31, 39, 46, 0.8), rgba(22, 27, 34, 0.8));
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 16px 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
}

[data-testid="stMetricValue"] {
    color: #58a6ff !important;
    font-family: 'Roboto Mono', monospace !important;
    font-size: 2rem !important;
    font-weight: 700;
}

[data-testid="stMetricLabel"] {
    color: #8b949e !important;
    font-size: 0.8rem !important;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    font-weight: 600;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #21262d 0%, #161b22 100%);
    color: #c9d1d9;
    border: 1.5px solid #30363d;
    border-radius: 8px;
    font-family: 'Roboto', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    transition: all 0.25s ease;
    padding: 0.6rem 1.2rem;
    text-transform: uppercase;
    cursor: pointer;
}

.stButton > button:hover {
    background: linear-gradient(135deg, #388bfd1a, #388bfd2a);
    border-color: #58a6ff;
    color: #58a6ff;
    box-shadow: 0 4px 12px rgba(88, 166, 255, 0.2);
}

.stButton > button:active {
    background: #1f6feb;
    color: #ffffff;
    border-color: #1f6feb;
}

/* ── Primary Button ── */
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg, #238636 0%, #2ea043 100%);
    border-color: #3fb950;
    color: #ffffff;
    font-weight: 700;
    box-shadow: 0 4px 12px rgba(48, 185, 61, 0.2);
}

.stButton > button[kind="primary"]:hover {
    background: linear-gradient(135deg, #2ea043 0%, #3fb950 100%);
    border-color: #3fb950;
    box-shadow: 0 6px 16px rgba(48, 185, 61, 0.3);
}

/* ── Input Fields ── */
.stTextInput > div > div > input,
.stSelectbox > div > div > div,
.stSlider,
.stNumberInput {
    background-color: rgba(30, 30, 46, 0.8) !important;
    border: 1.5px solid #30363d !important;
    color: #c9d1d9 !important;
    border-radius: 8px !important;
    font-family: 'Roboto', sans-serif !important;
    padding: 10px 12px !important;
}

.stTextInput > div > div > input:focus,
.stSelectbox > div > div > div:focus,
.stNumberInput:focus {
    border-color: #58a6ff !important;
    box-shadow: 0 0 0 2px rgba(88, 166, 255, 0.15) !important;
}

/* ── File Uploader ── */
[data-testid="stFileUploader"] {
    background: linear-gradient(135deg, rgba(31, 39, 46, 0.6), rgba(22, 27, 34, 0.6));
    border: 2px dashed #30363d;
    border-radius: 12px;
    padding: 2rem;
    transition: all 0.3s ease;
}

[data-testid="stFileUploader"]:hover {
    border-color: #58a6ff;
    background: linear-gradient(135deg, rgba(31, 39, 46, 0.8), rgba(22, 27, 34, 0.8));
}

/* ── Alerts ── */
.stSuccess {
    background-color: rgba(15, 45, 26, 0.8) !important;
    border: 1px solid #2ea043 !important;
    border-radius: 8px !important;
    color: #3fb950 !important;
}

.stWarning {
    background-color: rgba(45, 31, 0, 0.8) !important;
    border: 1px solid #d29922 !important;
    border-radius: 8px !important;
    color: #d29922 !important;
}

.stError {
    background-color: rgba(45, 15, 15, 0.8) !important;
    border: 1px solid #f85149 !important;
    border-radius: 8px !important;
    color: #f85149 !important;
}

.stInfo {
    background-color: rgba(15, 32, 60, 0.8) !important;
    border: 1px solid #58a6ff !important;
    border-radius: 8px !important;
    color: #79c0ff !important;
}

/* ── Expanders ── */
.streamlit-expanderHeader {
    background-color: rgba(31, 39, 46, 0.6) !important;
    border: 1px solid #30363d !important;
    border-radius: 8px !important;
    color: #8b949e !important;
    font-weight: 600 !important;
    padding: 12px 16px !important;
}

.streamlit-expanderHeader:hover {
    background-color: rgba(31, 39, 46, 0.9) !important;
    border-color: #58a6ff !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: transparent;
    border-bottom: 2px solid #30363d;
    gap: 0;
    padding-bottom: 0;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'Roboto', sans-serif;
    font-size: 0.95rem;
    color: #8b949e;
    padding: 12px 24px;
    border-bottom: 3px solid transparent;
    font-weight: 600;
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 0.05em;
}

.stTabs [data-baseweb="tab"]:hover {
    color: #79c0ff;
}

.stTabs [aria-selected="true"] {
    color: #58a6ff !important;
    border-bottom: 3px solid #58a6ff !important;
}

/* ── Status Badge ── */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 14px;
    border-radius: 20px;
    font-family: 'Roboto Mono', monospace;
    font-size: 0.8rem;
    font-weight: 700;
    letter-spacing: 0.04em;
    text-transform: uppercase;
}

.status-ready {
    background: rgba(15, 45, 26, 0.9);
    color: #3fb950;
    border: 1px solid #2ea043;
}

.status-loading {
    background: rgba(45, 60, 111, 0.9);
    color: #58a6ff;
    border: 1px solid #58a6ff;
    animation: pulse 2s infinite;
}

.status-error {
    background: rgba(45, 15, 15, 0.9);
    color: #f85149;
    border: 1px solid #f85149;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

/* ── Divider ── */
hr {
    border-color: #30363d !important;
    border-top: 2px solid #30363d !important;
    margin: 2rem 0 !important;
}

/* ── Log Panel ── */
.log-container {
    background: rgba(13, 17, 23, 0.9);
    border: 1px solid #21262d;
    border-radius: 10px;
    padding: 16px;
    max-height: 400px;
    overflow-y: auto;
    font-family: 'Roboto Mono', monospace;
    font-size: 0.85rem;
    line-height: 1.8;
}

.log-entry {
    padding: 6px 0;
    border-bottom: 1px solid #21262d;
    word-wrap: break-word;
}

.log-entry:last-child {
    border-bottom: none;
}

.log-info { color: #8b949e; }
.log-success { color: #3fb950; font-weight: 600; }
.log-warning { color: #d29922; font-weight: 600; }
.log-error { color: #f85149; font-weight: 600; }

/* ── Scrollbar Styling ── */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: rgba(30, 30, 46, 0.5);
}

::-webkit-scrollbar-thumb {
    background: #30363d;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #58a6ff;
}

/* ── Image Container ── */
.image-container {
    border: 1px solid #30363d;
    border-radius: 10px;
    overflow: hidden;
    background: rgba(30, 30, 46, 0.5);
    padding: 8px;
}

/* ── Footer ── */
.footer {
    text-align: center;
    padding: 20px 0;
    margin-top: 40px;
    border-top: 1px solid #30363d;
    font-size: 0.85rem;
    color: #8b949e;
}

.footer a {
    color: #58a6ff;
    text-decoration: none;
    transition: color 0.3s ease;
}

.footer a:hover {
    color: #79c0ff;
    text-decoration: underline;
}
</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# SESSION STATE INITIALIZATION
# ═══════════════════════════════════════════════════════════════════
session_defaults = {
    "captured_image": None,
    "uploaded_image": None,
    "last_frame": None,
    "live_logs": [],
    "stream_active": False,
    "prediction_result": None,
    "detection_count": 0,
    "confidence_scores": [],
    "class_names": [],
    "bounding_boxes": [],
}

for key, value in session_defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# ═══════════════════════════════════════════════════════════════════
# UTILITY FUNCTIONS
# ═══════════════════════════════════════════════════════════════════
def log_event(msg: str, level: str = "INFO"):
    """Log an event with timestamp and level."""
    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
    st.session_state.live_logs.append({
        "text": f"[{timestamp}] {msg}",
        "level": level,
    })
    # Keep only recent logs
    if len(st.session_state.live_logs) > 100:
        st.session_state.live_logs = st.session_state.live_logs[-100:]
    
    # Also log to file
    log_level_map = {
        "INFO": logging.INFO,
        "SUCCESS": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
    }
    
    log_func = {
        "INFO": logger.info,
        "SUCCESS": logger.info,
        "WARNING": logger.warning,
        "ERROR": logger.error,
    }
    
    log_message = f"[{level}] {msg}"
    if level in log_func:
        log_func[level](log_message)
    else:
        logger.info(log_message)


@st.cache_resource(show_spinner=False)
def load_model(model_path: str = "Models/best.pt") -> YOLO:
    """Load YOLO model with caching."""
    try:
        return YOLO(model_path)
    except Exception as e:
        st.error(f"Failed to load model: {e}")
        return None


def perform_detection(image, model, conf, iou, max_det):
    """Run detection on image with comprehensive error handling."""
    if model is None:
        log_event("Model is None - cannot run detection", level="ERROR")
        logger.error("Model is None")
        return None
    
    try:
        logger.info(f"Starting detection with conf={conf}, iou={iou}, max_det={max_det}")
        
        # Ensure image is in correct format
        if isinstance(image, np.ndarray):
            if image.dtype != np.uint8:
                image = (image * 255).astype(np.uint8) if image.max() <= 1 else image.astype(np.uint8)
        
        logger.debug(f"Image shape: {image.shape}, dtype: {image.dtype}")
        
        # Run prediction
        results = model.predict(
            image,
            conf=conf,
            iou=iou,
            max_det=int(max_det),
            verbose=False,
        )
        
        if not results:
            logger.warning("Prediction returned empty results")
            return None
        
        result = results[0]
        logger.info(f"Prediction successful. Boxes: {len(result.boxes) if result.boxes else 0}")
        
        return result
    
    except Exception as e:
        error_msg = f"Detection error: {str(e)}"
        log_event(error_msg, level="ERROR")
        logger.error(error_msg, exc_info=True)
        return None


def draw_detection_boxes(image, boxes_xyxy, confidence_scores, class_ids, class_names_dict):
    """Draw bounding boxes and labels on image
    
    Args:
        image: Input image (numpy array)
        boxes_xyxy: Bounding boxes as [[x1,y1,x2,y2], ...]
        confidence_scores: Confidence scores for each box
        class_ids: Class IDs for each box
        class_names_dict: Dictionary mapping class IDs to class names
    
    Returns:
        Annotated image with boxes drawn
    """
    if image is None:
        logger.warning("draw_detection_boxes called with None image")
        return None
    
    if not isinstance(boxes_xyxy, (list, tuple)) or len(boxes_xyxy) == 0:
        logger.info("No boxes to draw")
        return image.copy() if isinstance(image, np.ndarray) else image
    
    try:
        annotated = image.copy()
        
        # Ensure boxes are in correct format
        if isinstance(boxes_xyxy, np.ndarray):
            boxes = boxes_xyxy.astype(int)
        else:
            boxes = np.array(boxes_xyxy, dtype=int)
        
        # Ensure confidence scores and class_ids are arrays
        if isinstance(confidence_scores, np.ndarray):
            confs = confidence_scores
        else:
            confs = np.array(confidence_scores) if confidence_scores else np.array([])
        
        if isinstance(class_ids, np.ndarray):
            cls_ids = class_ids.astype(int)
        else:
            cls_ids = np.array(class_ids, dtype=int) if class_ids else np.array([])
        
        logger.info(f"Drawing {len(boxes)} boxes on image of shape {annotated.shape}")
        
        for i, (box, conf) in enumerate(zip(boxes, confs)):
            x1, y1, x2, y2 = box
            
            # Clamp coordinates to image bounds
            h, w = annotated.shape[:2]
            x1 = max(0, min(x1, w-1))
            y1 = max(0, min(y1, h-1))
            x2 = max(0, min(x2, w-1))
            y2 = max(0, min(y2, h-1))
            
            # Draw box
            cv2.rectangle(annotated, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)
            
            # Get class name if available
            if i < len(cls_ids):
                cls_id = int(cls_ids[i])
                if isinstance(class_names_dict, dict):
                    class_name = class_names_dict.get(cls_id, f"Class {cls_id}")
                else:
                    class_name = f"Class {cls_id}"
            else:
                class_name = "Unknown"
            
            # Draw label
            label = f"{class_name}: {float(conf):.1%}"
            label_size, baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            
            cv2.rectangle(
                annotated,
                (int(x1), int(y1) - label_size[1] - 10),
                (int(x1) + label_size[0], int(y1)),
                (0, 255, 0),
                -1
            )
            
            cv2.putText(
                annotated,
                label,
                (int(x1), int(y1) - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )
        
        logger.info(f"Successfully drew {len(boxes)} bounding boxes")
        return annotated
    
    except Exception as e:
        logger.error(f"Error drawing boxes: {e}", exc_info=True)
        return image.copy() if isinstance(image, np.ndarray) else image



# ═══════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## 🦠 AMR Detection System")
    
    # Model Status
    st.markdown("---")
    MODEL_PATH = "Models/best.pt"
    
    logger.info("="*60)
    logger.info("Application started")
    logger.info(f"Log file: {log_file}")
    logger.info("="*60)
    
    # Check if model exists
    model_exists = Path(MODEL_PATH).exists()
    
    logger.info(f"Model path: {MODEL_PATH}")
    logger.info(f"Model exists: {model_exists}")
    
    if model_exists:
        try:
            logger.info("Loading YOLO model...")
            model = load_model(MODEL_PATH)
            if model:
                status_html = "<span class='status-badge status-ready'>● Ready</span>"
                log_event("YOLO model loaded successfully", level="SUCCESS")
                logger.info("Model loaded successfully")
            else:
                status_html = "<span class='status-badge status-error'>✕ Load Failed</span>"
                log_event("Failed to load model", level="ERROR")
                logger.error("Model loading returned None")
                model = None
        except Exception as e:
            status_html = "<span class='status-badge status-error'>✕ Error</span>"
            log_event(f"Model loading error: {e}", level="ERROR")
            logger.error(f"Model loading exception: {e}", exc_info=True)
            model = None
    else:
        model = None
        status_html = "<span class='status-badge status-error'>✕ Not Found</span>"
        log_event(f"Model not found at {MODEL_PATH}", level="ERROR")
        logger.warning(f"Model file not found: {MODEL_PATH}")
    
    st.markdown("**Model Status:**")
    st.markdown(status_html, unsafe_allow_html=True)
    
    # Detection Settings
    st.markdown("---")
    st.markdown("## 🎯 Detection Settings")
    
    col1, col2 = st.columns(2)
    with col1:
        conf_threshold = st.slider(
            "Confidence",
            0.1, 1.0, 0.4, 0.05,
            help="Minimum confidence score"
        )
    with col2:
        iou_threshold = st.slider(
            "IoU Threshold",
            0.1, 1.0, 0.45, 0.05,
            help="NMS threshold"
        )
    
    max_det = st.number_input(
        "Max Detections",
        1, 300, 50,
        help="Maximum detections per image"
    )
    
    # Camera Settings
    st.markdown("---")
    st.markdown("## 📡 Camera Settings")
    
    camera_url = st.text_input(
        "Stream URL",
        value="0",
        help="0 for webcam or camera URL"
    )
    
    # Log file viewer
    st.markdown("---")
    st.markdown("## 📋 System Information")
    if st.checkbox("Show log file path"):
        st.code(log_file, language="text")
    
    # About & Links
    st.markdown("---")
    st.markdown("""
    <div style='font-size:0.8rem; color:#8b949e; line-height:1.8;'>
    <strong>Version:</strong> 1.0.0<br>
    <strong>Powered by:</strong> YOLOv8<br><br>
    <a href='https://github.com/yourusername' style='color:#58a6ff;'>🔗 GitHub</a> • 
    <a href='https://docs.ultralytics.com/' style='color:#58a6ff;'>📖 Docs</a>
    </div>
    """, unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════
col1, col2 = st.columns([3, 1])

with col1:
    st.markdown("""
    <div style='margin-bottom: 1.5rem;'>
        <h1>🦠 AMR Detection System</h1>
        <p style='color:#8b949e; font-size:1.05rem; margin-top: -1rem;'>
            Real-time Detection • YOLOv8 • Computer Vision
        </p>
    </div>
    """, unsafe_allow_html=True)

if model is None:
    st.error("⚠️ Model not found! Place `best.pt` in the `Models/` directory.")
    st.stop()

# ─────────────────────────────────────────
# METRICS ROW
# ─────────────────────────────────────────
m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("🤖 Model", "YOLOv8")

with m2:
    class_count = len(model.names) if hasattr(model, "names") and model.names else 0
    st.metric("📂 Classes", class_count)

with m3:
    st.metric("🎯 Detections", st.session_state.detection_count)

with m4:
    if st.session_state.confidence_scores:
        avg_conf = np.mean(st.session_state.confidence_scores)
        st.metric("💯 Avg Conf", f"{avg_conf:.1%}")
    else:
        st.metric("💯 Avg Conf", "—")

st.markdown("---")

# ═══════════════════════════════════════════════════════════════════
# MAIN TABS
# ═══════════════════════════════════════════════════════════════════
tab_stream, tab_upload, tab_batch, tab_results = st.tabs(
    ["📹 Live Stream", "🖼️  Upload Image", "📦 Batch Process", "📊 Results & Logs"]
)

# ───────────────────────────────────────────────────────────────────
# TAB 1: LIVE STREAM
# ───────────────────────────────────────────────────────────────────
with tab_stream:
    st.markdown("## Live Camera Stream")
    
    st.markdown("""
    <div class='amr-card amr-card-accent'>
    🎥 Connect to webcam or IP camera for real-time detection.
    </div>
    """, unsafe_allow_html=True)
    
    col_start, col_stop, col_capture = st.columns(3)
    
    with col_start:
        if st.button("▶ Start Stream", use_container_width=True, key="start_btn"):
            st.session_state.stream_active = True
            log_event(f"Stream started: {camera_url}")
    
    with col_stop:
        if st.button("⏹ Stop Stream", use_container_width=True, key="stop_btn"):
            st.session_state.stream_active = False
            log_event("Stream stopped")
    
    with col_capture:
        st.button("📸 Capture Frame", use_container_width=True, 
                 disabled=not st.session_state.stream_active, key="capture_btn")
    
    if st.session_state.stream_active:
        stream_placeholder = st.empty()
        status_placeholder = st.empty()
        
        # Resolve URL
        raw_url = camera_url.strip()
        resolved_url = int(raw_url) if raw_url.isdigit() else raw_url
        
        cap = cv2.VideoCapture(resolved_url)
        
        if not cap.isOpened():
            st.error("❌ Cannot open stream")
            log_event("Failed to open camera", level="ERROR")
            st.session_state.stream_active = False
        else:
            error_count = 0
            frame_count = 0
            
            while st.session_state.stream_active:
                ret, frame = cap.read()
                
                if not ret:
                    error_count += 1
                    if error_count > 20:
                        st.session_state.stream_active = False
                        st.error("❌ Stream disconnected")
                        break
                    time.sleep(0.05)
                    continue
                
                error_count = 0
                frame_count += 1
                
                # Display frame
                display_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                stream_placeholder.image(display_frame, use_container_width=True)
                
                status_placeholder.markdown(
                    f"<span style='color:#3fb950; font-family:monospace;'>● LIVE • Frames: {frame_count}</span>",
                    unsafe_allow_html=True
                )
                
                st.session_state.last_frame = frame.copy()
                time.sleep(0.033)  # ~30 fps
            
            cap.release()

# ───────────────────────────────────────────────────────────────────
# TAB 2: UPLOAD IMAGE
# ───────────────────────────────────────────────────────────────────
with tab_upload:
    st.markdown("## Upload Image for Analysis")
    
    st.markdown("""
    <div class='amr-card amr-card-accent'>
    📷 Upload JPG, JPEG, or PNG images for instant detection.
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Select an image",
        type=["jpg", "jpeg", "png"],
        label_visibility="collapsed"
    )
    
    if uploaded_file:
        try:
            img = Image.open(uploaded_file).convert("RGB")
            st.session_state.uploaded_image = np.array(img)
            log_event(f"Image uploaded: {uploaded_file.name}")
            
            st.markdown(f"**📷 {uploaded_file.name}** ({img.size[0]}×{img.size[1]}px)")
            st.image(img, use_container_width=True)
        except Exception as e:
            st.error(f"Error loading image: {e}")
            log_event(f"Image load error: {e}", level="ERROR")
    
    st.markdown("---")
    st.markdown("## Run Detection")
    
    # Get active image
    def get_active_image():
        if st.session_state.uploaded_image is not None:
            return st.session_state.uploaded_image, "Uploaded"
        if st.session_state.captured_image is not None:
            return cv2.cvtColor(st.session_state.captured_image, cv2.COLOR_BGR2RGB), "Captured"
        if st.session_state.last_frame is not None:
            return cv2.cvtColor(st.session_state.last_frame, cv2.COLOR_BGR2RGB), "Last Stream"
        return None, None
    
    active_img, img_source = get_active_image()
    
    if active_img is not None:
        st.markdown(f"<small>Source: **{img_source}**</small>", unsafe_allow_html=True)
    
    col_predict, col_clear = st.columns([2, 1])
    
    with col_predict:
        predict_btn = st.button(
            "🚀 Run Detection",
            use_container_width=True,
            type="primary",
            disabled=(active_img is None)
        )
    
    with col_clear:
        clear_btn = st.button("🗑️ Clear", use_container_width=True)
    
    if clear_btn:
        st.session_state.uploaded_image = None
        st.session_state.captured_image = None
        st.session_state.prediction_result = None
        st.rerun()
    
    if active_img is None:
        st.info("No image available. Upload or capture one.")
    
    if predict_btn and active_img is not None:
        logger.info("-" * 60)
        logger.info("Starting detection...")
        logger.info(f"Image shape: {active_img.shape}")
        logger.info(f"Image dtype: {active_img.dtype}")
        logger.info(f"Model: {model}")
        
        with st.spinner("🔍 Running inference..."):
            try:
                result = perform_detection(
                    active_img, 
                    model, 
                    conf_threshold, 
                    iou_threshold, 
                    max_det
                )
                
                if result is None:
                    logger.error("perform_detection returned None")
                    st.error("❌ Detection failed - returned None result")
                    log_event("Detection returned None result", level="ERROR")
                else:
                    logger.info(f"Detection result received: {type(result)}")
                    
                    # Check if result has boxes
                    if hasattr(result, 'boxes') and result.boxes is not None:
                        logger.info(f"Boxes detected: {len(result.boxes)}")
                        
                        # Try to plot annotated image
                        try:
                            annotated = result.plot()
                            annotated_rgb = cv2.cvtColor(annotated, cv2.COLOR_BGR2RGB)
                            st.session_state.prediction_result = annotated_rgb
                            logger.info("Annotated image generated successfully")
                        except Exception as e:
                            logger.warning(f"Could not use result.plot(), falling back to manual annotation: {e}")
                            # Fallback to manual annotation
                            annotated_rgb = draw_detection_boxes(
                                active_img,
                                result.boxes.xyxy.cpu().numpy() if hasattr(result.boxes, 'xyxy') else [],
                                result.boxes.conf.cpu().numpy() if hasattr(result.boxes, 'conf') else [],
                                result.boxes.cls.cpu().numpy() if hasattr(result.boxes, 'cls') else [],
                                model.names if hasattr(model, 'names') else {}
                            )
                            st.session_state.prediction_result = annotated_rgb
                            logger.info("Manual annotation fallback successful")
                        
                        # Parse detections
                        try:
                            if hasattr(result.boxes, 'conf'):
                                st.session_state.confidence_scores = result.boxes.conf.cpu().numpy().tolist()
                            else:
                                st.session_state.confidence_scores = []
                            
                            if hasattr(result.boxes, 'cls'):
                                cls_ids = result.boxes.cls.cpu().numpy().astype(int).tolist()
                                st.session_state.class_names = [model.names[c] for c in cls_ids] if hasattr(model, 'names') else []
                            else:
                                st.session_state.class_names = []
                            
                            if hasattr(result.boxes, 'xyxy'):
                                st.session_state.bounding_boxes = result.boxes.xyxy.cpu().numpy().tolist()
                            else:
                                st.session_state.bounding_boxes = []
                            
                            st.session_state.detection_count = len(st.session_state.confidence_scores)
                            
                            logger.info(f"Detection stats: {st.session_state.detection_count} objects")
                            logger.info(f"Confidence scores: {st.session_state.confidence_scores}")
                            logger.info(f"Class names: {st.session_state.class_names}")
                            
                            log_event(
                                f"Detection complete: {st.session_state.detection_count} object(s)",
                                level="SUCCESS"
                            )
                            logger.info("Detection processing complete - rerunning UI")
                            st.success(f"✅ Detection complete: {st.session_state.detection_count} object(s) detected")
                            st.rerun()
                        except Exception as e:
                            logger.error(f"Error parsing detection results: {e}", exc_info=True)
                            st.error(f"❌ Error parsing results: {e}")
                            log_event(f"Result parsing error: {e}", level="ERROR")
                    else:
                        # No boxes detected
                        logger.info("No objects detected in image")
                        st.session_state.detection_count = 0
                        st.session_state.confidence_scores = []
                        st.session_state.class_names = []
                        st.session_state.bounding_boxes = []
                        st.session_state.prediction_result = active_img
                        log_event("Detection complete: No objects detected", level="INFO")
                        st.info("✅ Detection complete: No objects detected")
                        st.rerun()
            except Exception as e:
                logger.error(f"Detection exception: {e}", exc_info=True)
                st.error(f"❌ Detection failed with error: {e}")
                log_event(f"Detection error: {e}", level="ERROR")
                logger.info("-" * 60)
    
    # Show results
    if st.session_state.prediction_result is not None:
        st.markdown("### Detection Output")
        st.image(st.session_state.prediction_result, use_container_width=True)
        
        # Download button
        from io import BytesIO
        result_pil = Image.fromarray(st.session_state.prediction_result)
        buf = BytesIO()
        result_pil.save(buf, format="PNG")
        st.download_button(
            "⬇️ Download Result",
            buf.getvalue(),
            f"amr_result_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png",
            "image/png"
        )

# ───────────────────────────────────────────────────────────────────
# TAB 3: BATCH PROCESSING
# ───────────────────────────────────────────────────────────────────
with tab_batch:
    st.markdown("## Batch Process Images")
    
    st.markdown("""
    <div class='amr-card amr-card-accent'>
    🔄 Process multiple images at once and export results.
    </div>
    """, unsafe_allow_html=True)
    
    st.info("ℹ️ Feature coming soon - Process entire folders with detection results export")

# ───────────────────────────────────────────────────────────────────
# TAB 4: RESULTS & LOGS
# ───────────────────────────────────────────────────────────────────
with tab_results:
    st.markdown("## Detection Results")
    
    if st.session_state.prediction_result is not None:
        rc1, rc2 = st.columns([3, 2])
        
        with rc1:
            st.image(st.session_state.prediction_result, use_container_width=True)
        
        with rc2:
            st.markdown("### Summary")
            
            det_count = st.session_state.detection_count
            
            if det_count == 0:
                st.info("No detections found")
            else:
                sm1, sm2 = st.columns(2)
                sm1.metric("Total", det_count)
                sm2.metric("Avg Conf", f"{np.mean(st.session_state.confidence_scores):.1%}")
                
                # Detections table
                st.markdown("#### Detections")
                for i, (name, conf) in enumerate(zip(st.session_state.class_names, st.session_state.confidence_scores), 1):
                    conf_pct = conf * 100
                    bar_len = int(conf * 10)
                    bar = "█" * bar_len + "░" * (10 - bar_len)
                    st.markdown(f"`{i:02d}` **{name}** — `{conf_pct:.1f}%` `{bar}`")
    else:
        st.info("No predictions yet")
    
    st.markdown("---")
    st.markdown("## Monitoring & Logs")
    
    log_tab1, log_tab2 = st.tabs(["📋 Live Logs", "📄 File Logs"])
    
    # Live Logs
    with log_tab1:
        col_clear, col_export = st.columns([1, 1])
        
        with col_clear:
            if st.button("Clear Live Logs", use_container_width=True):
                st.session_state.live_logs = []
                st.rerun()
        
        with col_export:
            if st.button("Export Live Logs", use_container_width=True):
                log_text = "\n".join([f"{entry['level']}: {entry['text']}" for entry in st.session_state.live_logs])
                st.download_button(
                    "⬇️ Download Logs",
                    log_text,
                    f"logs_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                )
        
        if st.session_state.live_logs:
            log_html = "<div class='log-container' style='max-height:500px; overflow-y:auto;'>"
            for entry in reversed(st.session_state.live_logs):
                level = entry.get("level", "INFO")
                level_class = f"log-{level.lower()}"
                icons = {"SUCCESS": "✓", "WARNING": "⚠", "ERROR": "✕", "INFO": "·"}
                icon = icons.get(level, "·")
                log_html += f"<div class='log-entry {level_class}'>{icon} {entry['text']}</div>"
            log_html += "</div>"
            st.markdown(log_html, unsafe_allow_html=True)
        else:
            st.markdown("<p style='color:#8b949e;'>No logs yet</p>", unsafe_allow_html=True)
    
    # File Logs
    with log_tab2:
        try:
            log_file_path = Path(log_file)
            
            if log_file_path.exists():
                st.success(f"✅ Log file: {log_file}")
                
                # Read and display log contents
                with open(log_file_path, 'r') as f:
                    log_contents = f.read()
                
                # Show with line numbers and syntax highlighting
                if log_contents.strip():
                    col_view, col_download = st.columns([1, 1])
                    
                    with col_view:
                        st.markdown("### Log Contents")
                    
                    with col_download:
                        if st.button("⬇️ Download File Log", use_container_width=True):
                            st.download_button(
                                "📥 Save Log File",
                                log_contents,
                                f"amr_detection_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
                                "text/plain"
                            )
                    
                    # Display logs with scrollable area
                    st.text_area(
                        "Log Output",
                        value=log_contents,
                        height=400,
                        disabled=True,
                        label_visibility="collapsed"
                    )
                    
                    # Log statistics
                    lines = log_contents.strip().split('\n')
                    error_count = sum(1 for l in lines if 'ERROR' in l)
                    warning_count = sum(1 for l in lines if 'WARNING' in l)
                    info_count = sum(1 for l in lines if 'INFO' in l)
                    
                    st.markdown("### Log Statistics")
                    stat1, stat2, stat3 = st.columns(3)
                    stat1.metric("Total Lines", len(lines))
                    stat2.metric("Warnings", warning_count)
                    stat3.metric("Errors", error_count)
                else:
                    st.info("Log file exists but is empty")
            else:
                st.warning(f"⚠️ Log file not found: {log_file}")
                st.info("Logs will be created when you run detection")
        
        except Exception as e:
            st.error(f"❌ Error reading log file: {e}")
            logger.error(f"Failed to read log file: {e}", exc_info=True)

# ═══════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════
st.markdown("""
<div class='footer'>
Made with ❤️ by <strong>Rahul Ojha</strong> | 
<a href='https://github.com/yourusername/amr-detection'>GitHub</a> | 
<a href='https://docs.ultralytics.com/'>YOLOv8 Docs</a><br>
<small>© 2024 AMR Detection System • Powered by YOLOv8 & Streamlit</small>
</div>
""", unsafe_allow_html=True)


def main():
    """Main entry point for the application."""
    pass


if __name__ == "__main__":
    main()
