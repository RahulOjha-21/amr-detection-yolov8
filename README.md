# 🦠 AMR Detection System

<div align="center">

**Real-time Automated Meter Reading (AMR) Detection using YOLOv8 and Computer Vision**

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Powered by YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-green)](https://github.com/ultralytics/ultralytics)

[Features](#features) • [Quick Start](#quick-start) • [Installation](#installation) • [Usage](#usage) • [Project Structure](#project-structure) • [Contributing](#contributing)

</div>

---

## 📋 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Documentation](#api-documentation)
- [Contributing](#contributing)
- [License](#license)
- [Author](#author)

---

## Overview

**AMR Detection System** is a comprehensive machine learning project for detecting and classifying Antimicrobial Resistance (AMR) patterns in medical samples using computer vision. This system leverages **YOLOv8**, one of the most advanced object detection models, combined with **Streamlit** for an intuitive real-time detection interface.

### Key Capabilities

- 🎥 **Real-time Detection**: Stream from webcams or IP cameras
- 📸 **Image Analysis**: Upload images for instant detection
- 🎯 **High Accuracy**: YOLOv8-based detection with configurable thresholds
- 📊 **Results Logging**: Track detection history and statistics
- ⚙️ **Configurable Parameters**: Adjust confidence, IoU, and detection limits
- 🔄 **Batch Processing**: Process multiple images programmatically
- 📈 **Performance Metrics**: View average confidence and detection counts

---

## Features

✨ **Core Features:**
- Multi-source detection (webcam, IP camera, uploaded images)
- Real-time video streaming with live inference
- Frame capture and analysis from video streams
- Batch image processing
- Export detection results with annotations
- Detailed detection logs and statistics
- Configurable detection parameters

📊 **Data Handling:**
- Automated frame extraction from videos
- Dataset splitting (train/validation)
- Duplicate image removal
- Batch image renaming

🛠️ **Developer Tools:**
- Python scripts for dataset preparation
- Jupyter notebooks for training and evaluation
- Easy model switching
- Modular, extensible codebase

---

## Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Detection Model** | YOLOv8 | Latest (Ultralytics) |
| **Computer Vision** | OpenCV | 4.8+ |
| **Web Framework** | Streamlit | 1.28+ |
| **ML Framework** | PyTorch | 2.0+ |
| **Image Processing** | Pillow | 10.0+ |
| **Language** | Python | 3.8+ |

---

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip or conda package manager
- 2GB+ RAM (4GB+ recommended)
- Webcam or IP camera (optional, for streaming)

### Setup (5 minutes)

```bash
# Clone the repository
git clone https://github.com/yourusername/amr-detection.git
cd amr-detection

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the web application
streamlit run src/app.py
```

---

## Installation

### Full Installation Guide

#### 1. **Clone Repository**
```bash
git clone https://github.com/yourusername/amr-detection.git
cd amr-detection
```

#### 2. **Create Virtual Environment**
```bash
# Using venv (recommended)
python -m venv venv
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# Using conda (alternative)
conda create -n amr-detection python=3.10
conda activate amr-detection
```

#### 3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

#### 4. **Download Pre-trained Model**
Place your trained YOLOv8 model at:
```
Models/best.pt
```

If you don't have a pre-trained model, the system will use YOLOv8's default weights.

#### 5. **Verify Installation**
```bash
python -c "import ultralytics; print(ultralytics.__version__)"
```

---

## Usage

### 🎬 Running the Web Application

```bash
streamlit run src/app.py
```

The application will open at `http://localhost:8501`

### 📊 Application Features

#### **Live Stream Tab**
- Connect to webcams or IP cameras
- Real-time video streaming
- Capture and analyze individual frames
- Adjustable stream resolution

#### **Upload Image Tab**
- Upload JPG, JPEG, or PNG images
- Instant detection and analysis
- Download annotated results
- Extract detection details

#### **Results & Logs Tab**
- View detection history
- Detailed per-detection statistics
- Real-time system logs
- Export results

### 🔧 Command-Line Usage

#### Extract Frames from Video
```python
from src.data_labeling.video_labeling import extract_frames_from_video

extract_frames_from_video(
    video_path="path/to/video.mp4",
    output_folder="output/frames",
    frame_interval=5  # Extract every 5th frame
)
```

#### Split Dataset
```python
from src.data_labeling.dataset_split import split_dataset

split_dataset(
    source_folder="data/labeled",
    output_folder="data/processed",
    train_ratio=0.8
)
```

#### Remove Duplicate Images
```python
from src.data_labeling.remove_duplicates import remove_duplicates

remove_duplicates(
    folder="data/images",
    threshold=0.95  # Similarity threshold
)
```

---

## Project Structure

```
amr-detection/
│
├── 📄 README.md                 # Project documentation
├── 📄 LICENSE                   # MIT License
├── 📄 requirements.txt          # Python dependencies
├── 📄 setup.py                  # Package setup configuration
├── 📄 .gitignore               # Git ignore rules
├── 📄 CONTRIBUTING.md          # Contribution guidelines
│
├── 📁 src/                      # Source code
│   ├── 📄 __init__.py
│   ├── 📄 config.py            # Configuration management
│   ├── 📄 constants.py         # Application constants
│   │
│   ├── 📁 data_labeling/       # Data preparation tools
│   │   ├── 📄 __init__.py
│   │   ├── 📄 image_labeling.py
│   │   ├── 📄 video_labeling.py
│   │   ├── 📄 dataset_split.py
│   │   └── 📄 remove_duplicates.py
│   │
│   └── 📁 streaming/           # Real-time detection
│       ├── 📄 __init__.py
│       ├── 📄 app.py           # Main Streamlit application
│       ├── 📄 model.py         # Model utilities
│       └── 📄 utils.py         # Helper utilities
│
├── 📁 notebooks/               # Jupyter notebooks
│   └── 📄 AMR_detect_code.ipynb    # Training & evaluation
│
├── 📁 Models/                  # Pre-trained models
│   └── 📄 best.pt             # YOLOv8 weights
│
├── 📁 AMR_Dataset/            # Labeled dataset
│   ├── 📁 images/
│   │   ├── 📁 train/          # Training images
│   │   └── 📁 val/            # Validation images
│   ├── 📁 labels/
│   │   ├── 📁 train/          # Training labels
│   │   └── 📁 val/            # Validation labels
│   └── 📁 Test_image/         # Test samples
│
└── 📁 Dataset/                # Raw data
    └── 📁 Data/               # Dataset files
```

---

## Configuration

### Environment Variables

Create a `.env` file in the project root:

```env
# Model Configuration
MODEL_PATH=Models/best.pt
CONFIDENCE_THRESHOLD=0.4
IOU_THRESHOLD=0.45
MAX_DETECTIONS=50

# Camera Configuration
DEFAULT_CAMERA_URL=0
ENABLE_STREAMING=true

# Application Settings
LOG_LEVEL=INFO
MAX_LOG_ENTRIES=50
```

---

## API Documentation

### Core Modules

#### `src.streaming.model`
```python
from src.streaming.model import load_model, run_detection

# Load model
model = load_model("Models/best.pt")

# Run detection
results = run_detection(
    image,
    model,
    conf=0.4,
    iou=0.45,
    max_det=50
)
```

#### `src.data_labeling.video_labeling`
```python
from src.data_labeling.video_labeling import extract_frames_from_video

frame_count = extract_frames_from_video(
    video_path="video.mp4",
    output_folder="frames/",
    frame_interval=1
)
```

#### `src.data_labeling.dataset_split`
```python
from src.data_labeling.dataset_split import split_dataset

split_dataset(
    source_folder="data/labeled",
    output_folder="data/processed",
    train_ratio=0.8
)
```

---

## Advanced Features

### 🔗 IP Camera Integration
Connect to any IP camera or stream URL:
- RTSP streams: `rtsp://camera-ip:554/stream`
- HTTP streams: `http://camera-ip:8080/video`
- Local camera: Use `0` for default webcam

### 📊 Batch Processing
Process multiple images programmatically:
```python
import os
from src.streaming.model import load_model, run_detection
import cv2

model = load_model("Models/best.pt")
for image_file in os.listdir("images/"):
    image = cv2.imread(f"images/{image_file}")
    results = run_detection(image, model)
    # Process results...
```

---

## Troubleshooting

### Common Issues

**"Model load failed"**
- Ensure `Models/best.pt` exists
- Check file permissions
- Verify model format compatibility

**"Cannot open stream"**
- Verify camera/stream URL is correct
- Check network connectivity
- Ensure port is not blocked by firewall

**"Low detection accuracy"**
- Ensure images are similar to training data
- Adjust confidence threshold lower
- Check model training status

### Getting Help
- 📖 Review [Ultralytics YOLOv8 docs](https://docs.ultralytics.com/)
- 🔍 Check GitHub Issues
- 💬 Create a detailed issue with logs

---

## Performance Optimization

### Tips for Better Results:
1. **Improve Image Quality**: Higher resolution = better detection
2. **Adjust Thresholds**: Lower confidence for more detections
3. **Model Training**: Train on your specific AMR dataset
4. **Hardware Acceleration**: Use GPU for faster inference
5. **Frame Rate**: Reduce video FPS for speed vs accuracy trade-off

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details.

### Development Setup
```bash
git clone https://github.com/yourusername/amr-detection.git
cd amr-detection
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

### Making Changes
1. Create a feature branch: `git checkout -b feature/amazing-feature`
2. Commit changes: `git commit -m 'Add amazing feature'`
3. Push to branch: `git push origin feature/amazing-feature`
4. Open a Pull Request

---

## Roadmap

- [x] Basic YOLOv8 detection
- [x] Streamlit web interface
- [x] Real-time streaming
- [ ] Advanced filtering algorithms
- [ ] Mobile app (React Native)
- [ ] Rest API (FastAPI)
- [ ] Multi-model support
- [ ] Cloud deployment guides
- [ ] Docker containerization

---

## License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details.

---

## Citation

If you use this project in your research, please cite:

```bibtex
@software{amr_detection_2024,
  title={AMR Detection System: Real-time Detection using YOLOv8},
  author={Rahul Ojha},
  year={2024},
  url={https://github.com/yourusername/amr-detection}
}
```

---

## Author & Maintainer

**Rahul Ojha**

- 🔗 [GitHub](https://github.com/yourusername)
- 📧 Email: your.email@example.com
- 💼 [LinkedIn](https://linkedin.com/in/yourusername)

---

## Acknowledgments

- **Ultralytics** - YOLOv8 framework
- **OpenCV** - Computer vision library
- **Streamlit** - Web app framework
- **PyTorch** - ML framework

---

## Support

If you found this project helpful, please consider:
- ⭐ Starring the repository
- 🐛 Reporting bugs via GitHub Issues
- 💡 Sharing feature ideas
- 🤝 Contributing improvements

---

<div align="center">

**Made with ❤️ by Rahul Ojha**

</div>
