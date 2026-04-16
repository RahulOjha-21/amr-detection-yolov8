"""
Application Constants

Defines all constant values used throughout the AMR Detection System.
"""

# ═══════════════════════════════════════════════════════════════════
# DEFAULT THRESHOLDS
# ═══════════════════════════════════════════════════════════════════
DEFAULT_CONFIDENCE_THRESHOLD = 0.4
DEFAULT_IOU_THRESHOLD = 0.45
DEFAULT_MAX_DETECTIONS = 50

CONFIDENCE_THRESHOLD_MIN = 0.1
CONFIDENCE_THRESHOLD_MAX = 1.0

IOU_THRESHOLD_MIN = 0.1
IOU_THRESHOLD_MAX = 1.0

# ═══════════════════════════════════════════════════════════════════
# MODEL CONFIGURATION
# ═══════════════════════════════════════════════════════════════════
MODEL_PATH = "Models/best.pt"
YOLO_MODEL_SIZE = "n"  # nano, small, medium, large, x-large
YOLO_DEVICE = "cpu"  # cpu, 0 (GPU index), or cuda

# ═══════════════════════════════════════════════════════════════════
# CAMERA/STREAM SETTINGS
# ═══════════════════════════════════════════════════════════════════
DEFAULT_CAMERA_INDEX = 0
DEFAULT_CAMERA_FPS = 30
DEFAULT_CAMERA_WIDTH = 640
DEFAULT_CAMERA_HEIGHT = 480

# Stream timeout (seconds)
STREAM_TIMEOUT = 5
MAX_STREAM_ERRORS = 20

# ═══════════════════════════════════════════════════════════════════
# FILE EXTENSIONS
# ═══════════════════════════════════════════════════════════════════
SUPPORTED_IMAGE_FORMATS = ("jpg", "jpeg", "png", "bmp", "tiff")
SUPPORTED_VIDEO_FORMATS = ("mp4", "avi", "mov", "mkv", "flv", "wmv")

# ═══════════════════════════════════════════════════════════════════
# LOGGING
# ═══════════════════════════════════════════════════════════════════
LOG_LEVEL = "INFO"
MAX_LOG_ENTRIES = 100
LOG_FORMAT = "[%(asctime)s] [%(levelname)s] %(message)s"
LOG_DATE_FORMAT = "%H:%M:%S"

# ═══════════════════════════════════════════════════════════════════
# COLORS (BGR for OpenCV)
# ═══════════════════════════════════════════════════════════════════
COLOR_GREEN = (0, 255, 0)
COLOR_RED = (0, 0, 255)
COLOR_BLUE = (255, 0, 0)
COLOR_YELLOW = (0, 255, 255)
COLOR_CYAN = (255, 255, 0)
COLOR_MAGENTA = (255, 0, 255)
COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)

# ═══════════════════════════════════════════════════════════════════
# APPLICATION TEXT
# ═══════════════════════════════════════════════════════════════════
APP_TITLE = "🦠 AMR Detection System"
APP_DESCRIPTION = "Real-time Automated Meter Reading Detection using YOLOv8"
APP_VERSION = "1.0.0"
APP_AUTHOR = "Rahul Ojha"

# ═══════════════════════════════════════════════════════════════════
# DATA PROCESSING
# ═══════════════════════════════════════════════════════════════════
DEFAULT_TRAIN_RATIO = 0.8
DEFAULT_VAL_RATIO = 0.2
RANDOM_SEED = 42

FRAME_EXTRACTION_INTERVAL = 1  # Extract every nth frame
DUPLICATE_DETECTION_THRESHOLD = 0.95

# ═══════════════════════════════════════════════════════════════════
# BATCH PROCESSING
# ═══════════════════════════════════════════════════════════════════
BATCH_SIZE = 8
NUM_WORKERS = 4

# ═══════════════════════════════════════════════════════════════════
# ERROR MESSAGES
# ═══════════════════════════════════════════════════════════════════
ERROR_MODEL_NOT_FOUND = "Model file not found. Place best.pt in Models/ directory."
ERROR_CANNOT_OPEN_CAMERA = "Cannot open camera/stream. Verify URL or camera connection."
ERROR_INVALID_IMAGE_FORMAT = "Invalid image format. Supported: jpg, jpeg, png, bmp"
ERROR_INVALID_VIDEO_FORMAT = "Invalid video format. Supported: mp4, avi, mov, mkv"
ERROR_PREDICTION_FAILED = "Prediction failed. Check model and input image."

# ═══════════════════════════════════════════════════════════════════
# SUCCESS MESSAGES
# ═══════════════════════════════════════════════════════════════════
SUCCESS_MODEL_LOADED = "Model loaded successfully"
SUCCESS_PREDICTION_COMPLETE = "Prediction complete"
SUCCESS_FRAMES_EXTRACTED = "Frames extracted successfully"
SUCCESS_DATASET_SPLIT = "Dataset split successfully"

# ═══════════════════════════════════════════════════════════════════
# API RESPONSE FORMATS
# ═══════════════════════════════════════════════════════════════════
RESPONSE_SUCCESS = {
    "status": "success",
    "code": 200,
}

RESPONSE_ERROR = {
    "status": "error",
    "code": 400,
}

# ═══════════════════════════════════════════════════════════════════
# PATHS
# ═══════════════════════════════════════════════════════════════════
MODELS_DIR = "Models"
DATA_DIR = "Dataset"
RESULTS_DIR = "results"
NOTEBOOKS_DIR = "notebooks"
