#!/usr/bin/env python
"""
AMR Detection System - Application Launcher

This script launches the Streamlit web interface for the AMR Detection System.
It can be run with:
    python run_app.py
    streamlit run src/app.py
"""

import sys
import subprocess
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_dependencies():
    """Check if all required dependencies are installed."""
    required_packages = [
        'streamlit',
        'opencv-python',
        'ultralytics',
        'PIL',
        'numpy',
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package if package != 'PIL' else 'PIL')
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        logger.error(f"Missing packages: {', '.join(missing_packages)}")
        logger.error("Install with: pip install -r requirements.txt")
        return False
    
    logger.info("All dependencies are installed ✓")
    return True


def check_model():
    """Check if the model file exists."""
    model_path = Path("Models/best.pt")
    
    if not model_path.exists():
        logger.warning(f"Model file not found: {model_path}")
        logger.warning("The application will still run, but detection will fail.")
        logger.info("Place your trained model at: Models/best.pt")
    else:
        logger.info(f"Model found: {model_path} ✓")
    
    return True


def main():
    """Launch the Streamlit application."""
    logger.info("=" * 60)
    logger.info("AMR Detection System - Web Interface")
    logger.info("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check model
    check_model()
    
    logger.info("")
    logger.info("Starting Streamlit application...")
    logger.info("Opening at: http://localhost:8501")
    logger.info("")
    
    # Launch Streamlit
    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                "src/streaming/app.py",
                "--logger.level=info",
            ]
        )
    except KeyboardInterrupt:
        logger.info("Application stopped by user")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Error launching application: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
