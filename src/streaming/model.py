"""
Model Loading and Management

Handles YOLO model initialization, caching, and prediction utilities.
"""

import os
import logging
from pathlib import Path
from typing import Optional, Tuple, List
import numpy as np
import cv2
from ultralytics import YOLO

logger = logging.getLogger(__name__)


class ModelManager:
    """Manages YOLO model loading and inference."""
    
    _instance = None  # For singleton pattern
    _model = None
    
    def __new__(cls):
        """Singleton pattern - one model instance."""
        if cls._instance is None:
            cls._instance = super(ModelManager, cls).__new__(cls)
        return cls._instance
    
    @classmethod
    def load_model(cls, model_path: str = "Models/best.pt") -> Optional[YOLO]:
        """
        Load YOLO model from file.
        
        Args:
            model_path: Path to the model weights file (.pt)
        
        Returns:
            YOLO model instance or None if loading fails
        """
        try:
            if not Path(model_path).exists():
                logger.error(f"Model file not found: {model_path}")
                return None
            
            logger.info(f"Loading model from {model_path}...")
            model = YOLO(model_path)
            logger.info("Model loaded successfully")
            cls._model = model
            return model
        
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            return None
    
    @classmethod
    def get_model(cls) -> Optional[YOLO]:
        """Get the currently loaded model."""
        return cls._model
    
    @staticmethod
    def is_model_loaded(model: Optional[YOLO]) -> bool:
        """Check if model is loaded."""
        return model is not None
    
    @staticmethod
    def get_class_names(model: YOLO) -> List[str]:
        """Get class names from model."""
        if hasattr(model, 'names') and model.names:
            return list(model.names.values())
        return []
    
    @staticmethod
    def run_inference(
        image: np.ndarray,
        model: YOLO,
        conf: float = 0.4,
        iou: float = 0.45,
        max_det: int = 50,
        verbose: bool = False
    ):
        """
        Run inference on an image.
        
        Args:
            image: Input image (numpy array)
            model: YOLO model instance
            conf: Confidence threshold
            iou: IoU threshold for NMS
            max_det: Maximum detections
            verbose: Print verbose output
        
        Returns:
            Detection results object
        """
        try:
            results = model.predict(
                image,
                conf=conf,
                iou=iou,
                max_det=int(max_det),
                verbose=verbose,
            )
            return results[0] if results else None
        
        except Exception as e:
            logger.error(f"Inference failed: {e}")
            return None
    
    @staticmethod
    def extract_detections(result) -> Tuple[List[str], List[float], np.ndarray]:
        """
        Extract detection information from results.
        
        Args:
            result: Detection result object
        
        Returns:
            Tuple of (class_names, confidences, bboxes)
        """
        try:
            if result is None or result.boxes is None:
                return [], [], np.array([])
            
            class_names = [result.names[int(cls_id)] 
                          for cls_id in result.boxes.cls.cpu().numpy()]
            confidences = result.boxes.conf.cpu().numpy().tolist()
            bboxes = result.boxes.xyxy.cpu().numpy()
            
            return class_names, confidences, bboxes
        
        except Exception as e:
            logger.error(f"Failed to extract detections: {e}")
            return [], [], np.array([])
    
    @staticmethod
    def draw_detections(
        image: np.ndarray,
        class_names: List[str],
        confidences: List[float],
        bboxes: np.ndarray,
        color: Tuple[int, int, int] = (0, 255, 0),
        thickness: int = 2
    ) -> np.ndarray:
        """
        Draw bounding boxes and labels on image.
        
        Args:
            image: Input image
            class_names: List of class names
            confidences: List of confidence scores
            bboxes: Bounding boxes array
            color: Box color (BGR)
            thickness: Line thickness
        
        Returns:
            Annotated image
        """
        annotated = image.copy()
        
        for (x1, y1, x2, y2), class_name, conf in zip(bboxes, class_names, confidences):
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            
            # Draw box
            cv2.rectangle(annotated, (x1, y1), (x2, y2), color, thickness)
            
            # Draw label
            label = f"{class_name}: {conf:.2%}"
            label_size, _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            
            cv2.rectangle(
                annotated,
                (x1, y1 - label_size[1] - 10),
                (x1 + label_size[0], y1),
                color,
                -1
            )
            
            cv2.putText(
                annotated,
                label,
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (255, 255, 255),
                2
            )
        
        return annotated


def load_model(model_path: str = "Models/best.pt") -> Optional[YOLO]:
    """Convenience function to load model."""
    return ModelManager.load_model(model_path)


def run_detection(
    image: np.ndarray,
    model: YOLO,
    conf: float = 0.4,
    iou: float = 0.45,
    max_det: int = 50
):
    """Convenience function to run detection."""
    return ModelManager.run_inference(image, model, conf, iou, max_det)


if __name__ == "__main__":
    # Test model loading
    import sys
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    model = load_model("Models/best.pt")
    if model:
        print(f"Classes: {ModelManager.get_class_names(model)}")
        print("Model loaded successfully!")
    else:
        print("Failed to load model")
        sys.exit(1)
