# Quick Start Guide

Get started with AMR Detection System in **5 minutes**! 🚀

## 1️⃣ Prerequisites

Before starting, ensure you have:

- **Python 3.8+** installed ([Download](https://www.python.org/downloads/))
- **pip** or **conda** (usually comes with Python)
- **Git** installed ([Download](https://git-scm.com/))

Check your Python version:
```bash
python --version
```

## 2️⃣ Installation (Choose One Method)

### Method A: Local Installation (Recommended for Development)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/amr-detection.git
cd amr-detection

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment
# On Windows:
venv\Scripts\activate

# On macOS/Linux:
source venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Get ready to run!
```

### Method B: Docker Installation (Recommended for Deployment)

```bash
# 1. Clone repository
git clone https://github.com/yourusername/amr-detection.git
cd amr-detection

# 2. Build and run with Docker Compose
docker-compose up -d

# 3. Open browser to http://localhost:8501
```

### Method C: Package Installation

```bash
pip install -e .
```

## 3️⃣ Running the Application

### Option 1: Using the Launcher Script

```bash
python run_app.py
```

The script will:
- ✅ Check dependencies
- ✅ Verify model file
- ✅ Launch Streamlit app
- 🌐 Open at `http://localhost:8501`

### Option 2: Direct Streamlit

```bash
streamlit run src/streaming/app.py
```

### Option 3: Docker

```bash
# If not already running
docker-compose up

# View logs
docker-compose logs -f amr-detection

# Stop
docker-compose down
```

## 4️⃣ Download Pre-trained Model

The system expects a trained YOLOv8 model at `Models/best.pt`

### Option A: Use Default YOLOv8 (Auto-downloaded)
The app will automatically use YOLOv8's pre-trained weights if your custom model isn't found.

### Option B: Use Your Trained Model
```bash
# Place your model file at:
Models/best.pt
```

## 5️⃣ Using the Web Interface

Once the app is running at `http://localhost:8501`:

### 📹 Live Stream Tab
1. Enter camera source:
   - `0` for local webcam
   - `http://camera-ip:8080/video` for IP camera
2. Click **Start Stream**
3. Click **Capture Frame** to analyze
4. View results instantly

### 🖼️ Upload Image Tab
1. Click **Select an image**
2. Choose JPG, JPEG, or PNG file
3. Click **Run Detection**
4. View results and download annotated image

### 📊 Results & Logs Tab
- View detection history
- See system logs
- Monitor performance metrics

---

## 🎯 Common Tasks

### Test with Sample Image

```bash
# The app includes test samples in: AMR_Dataset/Test_image/
# Just drag and drop into the Upload tab!
```

### Configure Detection Settings

In the **Settings** panel (left sidebar):
- **Confidence Threshold**: Lower = more detections (0.1-1.0)
- **IoU Threshold**: NMS setting (0.1-1.0)
- **Max Detections**: Maximum objects to detect (1-300)

### Change Camera/Stream

In **Camera Settings** (left sidebar):
- **Default**: `0` (local webcam)
- **IP Camera**: `http://192.168.1.100:8080/video`
- **RTSP Stream**: `rtsp://camera-ip:554/stream`

### Environment Configuration

Edit `.env` file (copy from `.env.example`):

```env
# Model settings
MODEL_PATH=Models/best.pt
CONFIDENCE_THRESHOLD=0.4
IOU_THRESHOLD=0.45

# Camera settings
DEFAULT_CAMERA_URL=0
STREAM_FPS=30
```

---

## 🔧 Troubleshooting

### "Model not found" Error

```bash
# Solution: Create Models directory and add model file
mkdir -p Models
# Place your best.pt file here
# Or download YOLOv8 weights automatically
```

### "Cannot open stream" Error

```bash
# Check camera/URL:
# - Webcam: Make sure no other app is using it
# - IP Camera: Verify URL and network connectivity
# - Firewall: Check if port is blocked
```

### Port 8501 Already in Use

```bash
# Option 1: Kill process using port
# On Windows:
netstat -ano | findstr :8501
taskkill /PID <PID> /F

# Option 2: Use different port
streamlit run src/streaming/app.py --server.port 8502
```

### Virtual Environment Issues

```bash
# Deactivate and reactivate
deactivate
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Or delete and recreate
rm -rf venv  # or rmdir /s venv on Windows
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Slow Inference

```bash
# Try these to speed up:
# 1. Lower confidence threshold in settings
# 2. Reduce image size in config
# 3. Use smaller YOLO model
# 4. Enable GPU (if available)
```

---

## 📚 Next Steps

### For Users
1. Upload your images
2. Adjust detection settings
3. View and export results
4. Check documentation for advanced features

### For Developers
1. Review [CONTRIBUTING.md](CONTRIBUTING.md) for contribution guidelines
2. Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment options
3. Read [STRUCTURE.md](STRUCTURE.md) for code organization
4. Explore `notebooks/AMR_detect_code.ipynb` for training

### For Training Your Own Model
See `notebooks/AMR_detect_code.ipynb` for:
- Data preparation
- Model training
- Evaluation
- Export

---

## 🚀 Deployment

### Local Network (LAN)

```bash
# After starting the app
streamlit run src/streaming/app.py \
  --server.address 0.0.0.0 \
  --server.port 8501
```

Access from other devices at: `http://your-machine-ip:8501`

### Docker (Production-Ready)

```bash
docker-compose up -d
# Available at: http://localhost:8501
```

See [DEPLOYMENT.md](DEPLOYMENT.md) for cloud options (AWS, Google Cloud, Heroku, etc.)

---

## 📖 Documentation

| Document | Purpose |
|----------|---------|
| [README.md](README_NEW.md) | Full project documentation |
| [CONTRIBUTING.md](CONTRIBUTING.md) | How to contribute |
| [DEPLOYMENT.md](DEPLOYMENT.md) | Deployment instructions |
| [STRUCTURE.md](STRUCTURE.md) | Code organization |
| [GITHUB_READY.md](GITHUB_READY.md) | GitHub launch checklist |

---

## ❓ FAQ

**Q: Can I use a different camera?**  
A: Yes! Enter any IP camera URL or camera index (0, 1, etc.) in Settings

**Q: How do I train my own model?**  
A: Use the Jupyter notebook at `notebooks/AMR_detect_code.ipynb`

**Q: Can I deploy to the cloud?**  
A: Yes! See [DEPLOYMENT.md](DEPLOYMENT.md) for AWS, Google Cloud, and Heroku

**Q: How do I improve detection accuracy?**  
A: Train with your dataset or adjust confidence threshold in settings

**Q: Is GPU support available?**  
A: Yes! Set `USE_GPU=true` in `.env` if you have CUDA-compatible GPU

---

## 🆘 Need Help?

1. Check **Logs** in Results & Logs tab
2. Review [Troubleshooting](README_NEW.md#troubleshooting) section
3. Check [GitHub Issues](https://github.com/yourusername/amr-detection/issues)
4. Create a new issue with details and logs

---

## ⭐ Tips & Tricks

- 💡 Lower confidence threshold to catch more objects
- 💡 Use GPU for 10x faster inference
- 💡 Docker for easy deployment
- 💡 Check logs to debug issues
- 💡 Export results for further analysis

---

**You're all set! Happy detecting! 🦠**

For more information, see the full [README](README_NEW.md)
