"""
Configuration Management for AMR Detection System

This module handles loading and managing configuration settings
from environment variables or config files.
"""

import os
from pathlib import Path
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

# ═══════════════════════════════════════════════════════════════════
# LOGGING CONFIGURATION
# ═══════════════════════════════════════════════════════════════════
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)


# ═══════════════════════════════════════════════════════════════════
# MODEL CONFIGURATION
# ═══════════════════════════════════════════════════════════════════
class ModelConfig:
    """Configuration for YOLOv8 model."""
    
    # Model path
    MODEL_PATH = os.getenv("MODEL_PATH", "Models/best.pt")
    
    # Detection thresholds
    CONFIDENCE_THRESHOLD = float(os.getenv("CONFIDENCE_THRESHOLD", 0.4))
    IOU_THRESHOLD = float(os.getenv("IOU_THRESHOLD", 0.45))
    MAX_DETECTIONS = int(os.getenv("MAX_DETECTIONS", 50))
    
    # Model type
    MODEL_TYPE = os.getenv("MODEL_TYPE", "yolov8")
    USE_GPU = os.getenv("USE_GPU", "true").lower() == "true"
    
    # Validation
    @staticmethod
    def validate():
        """Validate model configuration."""
        if not Path(ModelConfig.MODEL_PATH).exists():
            logger.warning(f"Model not found at {ModelConfig.MODEL_PATH}")
        
        if not (0 < ModelConfig.CONFIDENCE_THRESHOLD < 1):
            logger.warning("Confidence threshold out of range [0, 1]")
        
        if not (0 < ModelConfig.IOU_THRESHOLD < 1):
            logger.warning("IoU threshold out of range [0, 1]")
        
        if ModelConfig.MAX_DETECTIONS < 1:
            logger.warning("Max detections must be positive")


# ═══════════════════════════════════════════════════════════════════
# CAMERA CONFIGURATION
# ═══════════════════════════════════════════════════════════════════
class CameraConfig:
    """Configuration for camera/stream inputs."""
    
    # Default camera source
    DEFAULT_CAMERA = os.getenv("DEFAULT_CAMERA_URL", "0")
    
    # Streaming settings
    ENABLE_STREAMING = os.getenv("ENABLE_STREAMING", "true").lower() == "true"
    STREAM_FPS = int(os.getenv("STREAM_FPS", 30))
    STREAM_TIMEOUT = int(os.getenv("STREAM_TIMEOUT", 5))
    
    # Frame settings
    FRAME_WIDTH = int(os.getenv("FRAME_WIDTH", 640))
    FRAME_HEIGHT = int(os.getenv("FRAME_HEIGHT", 480))


# ═══════════════════════════════════════════════════════════════════
# APPLICATION CONFIGURATION
# ═══════════════════════════════════════════════════════════════════
class AppConfig:
    """Application-wide configuration."""
    
    # Logging
    MAX_LOG_ENTRIES = int(os.getenv("MAX_LOG_ENTRIES", 100))
    
    # Data folders
    DATA_FOLDER = os.getenv("DATA_FOLDER", "Dataset/Data")
    MODELS_FOLDER = os.getenv("MODELS_FOLDER", "Models")
    OUTPUT_FOLDER = os.getenv("OUTPUT_FOLDER", "results")
    
    # File extensions
    SUPPORTED_IMAGE_FORMATS = [".jpg", ".jpeg", ".png", ".bmp"]
    SUPPORTED_VIDEO_FORMATS = [".mp4", ".avi", ".mov", ".mkv"]
    
    # UI Settings
    THEME = os.getenv("THEME", "dark")
    PAGE_TITLE = "AMR Detection System"
    PAGE_ICON = "🦠"


# ═══════════════════════════════════════════════════════════════════
# DATA CONFIGURATION
# ═══════════════════════════════════════════════════════════════════
class DataConfig:
    """Configuration for data processing."""
    
    # Dataset paths
    RAW_DATA_PATH = "Dataset/Data"
    PROCESSED_DATA_PATH = "AMR_Dataset"
    
    # Train/validation split
    TRAIN_RATIO = float(os.getenv("TRAIN_RATIO", 0.8))
    VALIDATION_RATIO = float(os.getenv("VALIDATION_RATIO", 0.2))
    
    # Data processing
    BATCH_SIZE = int(os.getenv("BATCH_SIZE", 8))
    NUM_WORKERS = int(os.getenv("NUM_WORKERS", 4))
    
    # Image processing
    IMAGE_SIZE = int(os.getenv("IMAGE_SIZE", 640))
    AUGMENTATION = os.getenv("AUGMENTATION", "true").lower() == "true"


# ═══════════════════════════════════════════════════════════════════
# VALIDATION
# ═══════════════════════════════════════════════════════════════════
def validate_config():
    """Validate all configuration settings."""
    ModelConfig.validate()
    logger.info("Configuration validated successfully")


if __name__ == "__main__":
    # Display configuration
    print("Model Configuration:")
    print(f"  Model Path: {ModelConfig.MODEL_PATH}")
    print(f"  Confidence Threshold: {ModelConfig.CONFIDENCE_THRESHOLD}")
    print(f"  IoU Threshold: {ModelConfig.IOU_THRESHOLD}")
    print(f"  Max Detections: {ModelConfig.MAX_DETECTIONS}")
    print()
    print("Camera Configuration:")
    print(f"  Default Camera: {CameraConfig.DEFAULT_CAMERA}")
    print(f"  Frame Size: {CameraConfig.FRAME_WIDTH}x{CameraConfig.FRAME_HEIGHT}")
    print()
    print("App Configuration:")
    print(f"  Data Folder: {AppConfig.DATA_FOLDER}")
    print(f"  Models Folder: {AppConfig.MODELS_FOLDER}")
    
    validate_config()
