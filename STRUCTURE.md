# Project Structure and Organization

## Directory Layout

```
amr-detection/
│
├── 📄 README_NEW.md                 ← Comprehensive project documentation
├── 📄 LICENSE                       ← MIT License
├── 📄 CONTRIBUTING.md               ← Contribution guidelines
├── 📄 DEPLOYMENT.md                 ← Deployment instructions
├── 📄 STRUCTURE.md                  ← This file
│
├── 📄 requirements.txt              ← Python dependencies with pinned versions
├── 📄 setup.py                      ← Package installation configuration
├── 📄 pyproject.toml                ← Modern Python project configuration
│
├── 📄 .gitignore                    ← Git ignore rules
├── 📄 .env.example                  ← Environment variables template
├── 📄 .dockerignore                 ← Docker build exclusions
│
├── 📄 Dockerfile                    ← Container image definition
├── 📄 docker-compose.yml            ← Docker Compose orchestration
│
├── 📄 run_app.py                    ← Application launcher script
│
├── 📁 src/                          ← Main source code directory
│   ├── 📄 __init__.py              ← Package initialization
│   ├── 📄 config.py                ← Configuration management
│   ├── 📄 constants.py             ← Application constants
│   │
│   ├── 📁 data_labeling/           ← Dataset preparation tools
│   │   ├── 📄 __init__.py
│   │   ├── 📄 image_labeling.py    ← Batch image renaming
│   │   ├── 📄 video_labeling.py    ← Frame extraction from videos
│   │   ├── 📄 dataset_split.py     ← Train/validation splitting
│   │   └── 📄 remove_duplicates.py ← Duplicate image removal
│   │
│   └── 📁 streaming/               ← Real-time detection module
│       ├── 📄 __init__.py
│       ├── 📄 app.py               ← Main Streamlit web application
│       ├── 📄 model.py             ← Model loading & inference utilities
│       └── 📄 utils.py             ← Helper utilities (camera, image processing)
│
├── 📁 notebooks/                    ← Jupyter notebooks
│   └── 📄 AMR_detect_code.ipynb    ← Model training & evaluation
│
├── 📁 Models/                       ← Pre-trained model weights
│   └── 📄 best.pt                 ← YOLOv8 model weights
│
├── 📁 AMR_Dataset/                 ← Organized labeled dataset
│   ├── 📁 images/
│   │   ├── 📁 train/              ← Training images (~80%)
│   │   └── 📁 val/                ← Validation images (~20%)
│   ├── 📁 labels/
│   │   ├── 📁 train/              ← Training labels (YOLO format)
│   │   └── 📁 val/                ← Validation labels
│   └── 📁 Test_image/             ← Test samples
│
├── 📁 Dataset/                      ← Raw dataset
│   └── 📁 Data/                    ← Raw image files (100+ samples)
│
└── 📁 results/                      ← Output directory (auto-created)
    ├── 📁 detections/              ← Detection results
    └── 📁 exports/                 ← Exported data
```

---

## Module Organization

### Core Modules

#### `src/config.py`
**Configuration Management**
- `ModelConfig`: YOLO model settings
- `CameraConfig`: Camera/stream settings
- `AppConfig`: Application settings
- `DataConfig`: Data processing settings
- Environment variable loading via `.env`

#### `src/constants.py`
**Application Constants**
- Detection thresholds
- Model paths
- File extensions
- Color definitions (BGR)
- Error and success messages
- API response formats

#### `src/data_labeling/`
**Dataset Preparation Tools**

- **`image_labeling.py`**: Batch rename images with custom prefixes
- **`video_labeling.py`**: Extract frames from videos at specified intervals
- **`dataset_split.py`**: Split dataset into train/validation sets
- **`remove_duplicates.py`**: Identify and remove similar images

#### `src/streaming/`
**Real-time Detection System**

- **`app.py`**: Main Streamlit web interface
  - Live stream tab
  - Image upload tab
  - Batch processing tab
  - Results & logs tab

- **`model.py`**: Model management
  - `ModelManager`: Singleton pattern model handling
  - Model loading and caching
  - Inference execution
  - Detection parsing

- **`utils.py`**: Helper utilities
  - Camera management
  - Image processing
  - File operations
  - Performance metrics
  - Logging utilities

---

## Data Flow

### Training Pipeline
```
Raw Dataset (Dataset/Data/)
    ↓
Dataset Preparation (src/data_labeling/)
    ├── Extract frames (video_labeling.py)
    ├── Remove duplicates (remove_duplicates.py)
    └── Split into train/val (dataset_split.py)
    ↓
Organized Dataset (AMR_Dataset/)
    ├── images/train/
    ├── images/val/
    ├── labels/train/
    └── labels/val/
    ↓
Model Training (notebooks/AMR_detect_code.ipynb)
    ↓
Trained Model (Models/best.pt)
```

### Inference Pipeline
```
Input Source
├── Option 1: Live Camera (src/streaming/app.py - Stream tab)
├── Option 2: Image Upload (src/streaming/app.py - Upload tab)
└── Option 3: Batch Processing (src/streaming/app.py - Batch tab)
    ↓
Image Preprocessing (src/streaming/utils.py)
    ↓
Model Loading (src/streaming/model.py)
    ↓
YOLO Inference
    ↓
Detection Parsing (src/streaming/model.py)
    ↓
Result Visualization & Export (src/streaming/app.py)
```

---

## File Type Organization

### Python Files (`.py`)
- Source code modules
- Utilities and helpers
- Application entry points

### Configuration Files
- `.env.example`: Environment variable template
- `pyproject.toml`: Modern Python packaging
- `setup.py`: Installation configuration
- `requirements.txt`: Python dependencies

### Jupyter Notebooks (`.ipynb`)
- `AMR_detect_code.ipynb`: Model training and evaluation
- Interactive environment for development

### Docker Files
- `Dockerfile`: Container image definition
- `docker-compose.yml`: Multi-container orchestration
- `.dockerignore`: Build context exclusions

### Documentation (`.md`)
- `README_NEW.md`: Main documentation
- `CONTRIBUTING.md`: Contribution guidelines
- `DEPLOYMENT.md`: Deployment instructions
- `STRUCTURE.md`: This file

### Dataset
- Images: JPG/PNG format
- Labels: YOLO format (.txt files)
- Structure: Train/validation split

### Models
- `.pt` files: PyTorch/YOLOv8 model weights
- Pre-trained weights storage

---

## Development Workflow

### 1. Setup Environment
```bash
git clone <repo>
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### 2. Add/Modify Code
```bash
# Edit files in src/
# Follow Python conventions
# Add docstrings
# Test changes
```

### 3. Prepare Dataset
```bash
# Place raw data in Dataset/Data/
python -c "from src.data_labeling.video_labeling import extract_frames_from_video; ..."
python -c "from src.data_labeling.dataset_split import split_dataset; ..."
```

### 4. Train Model
```bash
# Use notebooks/AMR_detect_code.ipynb
# Or run training script
jupyter notebook notebooks/AMR_detect_code.ipynb
```

### 5. Test & Deploy
```bash
# Test locally
python run_app.py

# Deploy with Docker
docker-compose up -d
```

---

## Configuration Hierarchy

Configuration is loaded in this order (highest priority first):

1. **Environment Variables** (`.env` file)
   - Production settings
   - Secrets and credentials

2. **Command-line Arguments**
   - Runtime overrides

3. **Configuration Classes** (`src/config.py`)
   - Application defaults

4. **Constants** (`src/constants.py`)
   - Hard-coded defaults

### Example
```python
# Constants (lowest priority)
DEFAULT_CONFIDENCE = 0.4

# Config class (higher priority)
class ModelConfig:
    CONFIDENCE_THRESHOLD = os.getenv("CONFIDENCE_THRESHOLD", 0.4)

# Environment variable (highest priority)
CONFIDENCE_THRESHOLD=0.6  # in .env file
```

---

## Extension Points

### Adding New Detection Features
1. Add utilities to `src/streaming/utils.py`
2. Extend `ModelManager` in `src/streaming/model.py`
3. Add UI components to `src/streaming/app.py`

### Adding Data Processing
1. Create new script in `src/data_labeling/`
2. Add to `__init__.py` exports
3. Document usage in README

### Adding Configuration
1. Add to appropriate `Config` class in `src/config.py`
2. Add to `.env.example`
3. Update documentation

### Adding Models
1. Train model using notebook
2. Place in `Models/` directory
3. Update `MODEL_PATH` in configuration

---

## Best Practices

### Code Quality
- ✅ Follow PEP 8 style guide
- ✅ Write docstrings for all functions
- ✅ Use type hints
- ✅ Keep functions small and focused
- ✅ Use meaningful variable names

### Documentation
- ✅ Document configuration options
- ✅ Add examples in docstrings
- ✅ Keep README updated
- ✅ Document API changes

### Testing
- ✅ Test with sample images
- ✅ Verify with different input sources
- ✅ Check error handling
- ✅ Test in Docker container

### Security
- ✅ Never commit `.env` files
- ✅ Use environment variables for secrets
- ✅ Validate user inputs
- ✅ Keep dependencies updated

---

## Performance Optimization

### Memory
- Cache model in singleton
- Limit log entries (100 max)
- Stream frames instead of buffering

### Speed
- Use smaller YOLO model for faster inference
- Adjust detect-write detection threshold
- Reduce input image size
- Use GPU if available

### Scalability
- Docker for easy deployment
- Load balancing via reverse proxy
- Database for results storage (future)
- Queue system for batch processing (future)

---

## Maintenance

### Dependency Updates
```bash
pip install --upgrade -r requirements.txt
# Test thoroughly after updates
```

### Model Updates
```bash
# Train new model
# Replace Models/best.pt
# Test with sample images
# Update documentation
```

### Backup Strategy
```bash
# Backup models and results
tar -czf backup.tar.gz Models/ results/
# Upload to cloud storage
```

---

**Last Updated:** March 2024
**Maintained by:** Rahul Ojha
