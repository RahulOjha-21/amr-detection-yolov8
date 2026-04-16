"""
Utility Functions for Streaming and Detection

Helper functions for camera management, image processing, and logging.
"""

import logging
import cv2
import numpy as np
from pathlib import Path
from typing import Optional, Tuple, List
import datetime


logger = logging.getLogger(__name__)


# ═══════════════════════════════════════════════════════════════════
# CAMERA UTILITIES
# ═══════════════════════════════════════════════════════════════════
def open_camera(source: str = "0", timeout: int = 5) -> Optional[cv2.VideoCapture]:
    """
    Open camera or stream.
    
    Args:
        source: Camera index (0, 1...) or URL string
        timeout: Timeout in seconds
    
    Returns:
        VideoCapture object or None if failed
    """
    try:
        # Try to parse as integer (webcam index)
        if source.isdigit():
            source = int(source)
        
        cap = cv2.VideoCapture(source)
        
        # Set timeout
        if isinstance(source, int):
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        
        # Check if opened successfully
        if not cap.isOpened():
            logger.error(f"Cannot open camera/stream: {source}")
            return None
        
        logger.info(f"Camera opened successfully: {source}")
        return cap
    
    except Exception as e:
        logger.error(f"Error opening camera: {e}")
        return None


def read_frame(cap: cv2.VideoCapture) -> Tuple[bool, Optional[np.ndarray]]:
    """
    Read frame from camera.
    
    Args:
        cap: VideoCapture object
    
    Returns:
        Tuple of (success, frame)
    """
    if cap is None:
        return False, None
    
    try:
        ret, frame = cap.read()
        return ret, frame
    except Exception as e:
        logger.error(f"Error reading frame: {e}")
        return False, None


def close_camera(cap: Optional[cv2.VideoCapture]):
    """Close camera/stream."""
    if cap is not None:
        cap.release()
        logger.info("Camera closed")


# ═══════════════════════════════════════════════════════════════════
# IMAGE PROCESSING
# ═══════════════════════════════════════════════════════════════════
def resize_image(
    image: np.ndarray,
    width: Optional[int] = None,
    height: Optional[int] = None
) -> np.ndarray:
    """
    Resize image maintaining aspect ratio.
    
    Args:
        image: Input image
        width: Target width (keep aspect if height is None)
        height: Target height (keep aspect if width is None)
    
    Returns:
        Resized image
    """
    h, w = image.shape[:2]
    
    if width is None and height is None:
        return image
    
    if width is None:
        ratio = height / h
        width = int(w * ratio)
    elif height is None:
        ratio = width / w
        height = int(h * ratio)
    
    return cv2.resize(image, (width, height), interpolation=cv2.INTER_LINEAR)


def convert_color_space(
    image: np.ndarray,
    from_space: str = "BGR",
    to_space: str = "RGB"
) -> np.ndarray:
    """
    Convert image color space.
    
    Args:
        image: Input image
        from_space: Source color space
        to_space: Target color space
    
    Returns:
        Converted image
    """
    if from_space == to_space:
        return image
    
    if from_space == "BGR" and to_space == "RGB":
        return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    elif from_space == "RGB" and to_space == "BGR":
        return cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    elif from_space == "BGR" and to_space == "HSV":
        return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    elif from_space == "BGR" and to_space == "GRAY":
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    return image


def normalize_image(image: np.ndarray) -> np.ndarray:
    """Normalize image to [0, 1] range."""
    return image.astype(np.float32) / 255.0


# ═══════════════════════════════════════════════════════════════════
# FILE UTILITIES
# ═══════════════════════════════════════════════════════════════════
def save_image(
    image: np.ndarray,
    filepath: str,
    create_dirs: bool = True
) -> bool:
    """
    Save image to file.
    
    Args:
        image: Image to save
        filepath: Output path
        create_dirs: Create directories if needed
    
    Returns:
        Success status
    """
    try:
        if create_dirs:
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)
        
        success = cv2.imwrite(filepath, image)
        if success:
            logger.info(f"Image saved: {filepath}")
        else:
            logger.error(f"Failed to save image: {filepath}")
        
        return success
    
    except Exception as e:
        logger.error(f"Error saving image: {e}")
        return False


def get_image_files(
    folder: str,
    extensions: List[str] = None
) -> List[str]:
    """
    Get all image files in folder.
    
    Args:
        folder: Folder path
        extensions: File extensions to filter (default: .jpg, .png)
    
    Returns:
        List of image file paths
    """
    if extensions is None:
        extensions = [".jpg", ".jpeg", ".png", ".bmp"]
    
    try:
        folder_path = Path(folder)
        image_files = []
        
        for ext in extensions:
            image_files.extend(folder_path.glob(f"*{ext}"))
            image_files.extend(folder_path.glob(f"*{ext.upper()}"))
        
        return sorted([str(f) for f in set(image_files)])
    
    except Exception as e:
        logger.error(f"Error getting image files: {e}")
        return []


# ═══════════════════════════════════════════════════════════════════
# LOGGING & METRICS
# ═══════════════════════════════════════════════════════════════════
class PerformanceMetrics:
    """Track performance metrics."""
    
    def __init__(self):
        self.start_time = None
        self.frame_count = 0
        self.total_detections = 0
        self.avg_inference_time = 0.0
    
    def start(self):
        """Start timing."""
        self.start_time = datetime.datetime.now()
    
    def get_elapsed(self) -> float:
        """Get elapsed time in seconds."""
        if self.start_time is None:
            return 0.0
        return (datetime.datetime.now() - self.start_time).total_seconds()
    
    def get_fps(self) -> float:
        """Calculate FPS."""
        elapsed = self.get_elapsed()
        if elapsed > 0:
            return self.frame_count / elapsed
        return 0.0
    
    def reset(self):
        """Reset metrics."""
        self.start_time = None
        self.frame_count = 0
        self.total_detections = 0
        self.avg_inference_time = 0.0


def format_detection_summary(
    class_names: List[str],
    confidences: List[float]
) -> str:
    """Format detection summary as string."""
    if not class_names:
        return "No detections"
    
    summary = f"Found {len(class_names)} object(s):\n"
    for name, conf in zip(class_names, confidences):
        summary += f"  • {name}: {conf:.1%}\n"
    
    return summary


def log_detection_info(
    class_names: List[str],
    confidences: List[float],
    inference_time: float = 0.0
):
    """Log detection information."""
    if not class_names:
        logger.info("No detections found")
    else:
        logger.info(f"Detected {len(class_names)} object(s)")
        for name, conf in zip(class_names, confidences):
            logger.info(f"  - {name}: {conf:.1%}")
    
    if inference_time > 0:
        logger.info(f"Inference time: {inference_time:.3f}s")


if __name__ == "__main__":
    # Test logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    print("Utility functions loaded successfully")
