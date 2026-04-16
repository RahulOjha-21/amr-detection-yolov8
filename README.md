# AMR Detection Machine Learning Project

## Project Overview
This project focuses on Automated Meter Reading (AMR) using machine learning and computer vision. It includes scripts for data labeling, dataset preparation, model training, and real-time streaming.

## Folder Structure
```
notebooks/
    AMR_detection.ipynb         # Main notebook for detection, training, evaluation
src/
    data_labeling/
        image_labeling.py       # Script for labeling images
        video_labeling.py       # Script for extracting frames and labeling videos
        remove_duplicates.py    # Script for removing duplicate images
        dataset_split.py        # Script for splitting dataset into train/val
    streaming/
        webcam_stream.py        # Real-time webcam streaming and capture
models/
    best_model.pt              # Trained model weights
requirements.txt               # Python dependencies
README.md                      # Project documentation

# Data
 data/
    raw/
        images/                # Raw images
        videos/                # Raw videos
        labels/                # Raw label files
    processed/
        train/
            images/            # Training images
            labels/            # Training labels
        val/
            images/            # Validation images
            labels/            # Validation labels
```

## Usage
- Use scripts in `src/data_labeling/` to prepare and clean your dataset.
- Use `notebooks/AMR_detection.ipynb` for model training, evaluation, and inference.
- Store trained models in `models/`.
- Use `src/streaming/webcam_stream.py` for real-time image capture and streaming.

## Requirements
Install dependencies:
```
pip install -r requirements.txt
```

## Data Preparation
- Place raw images, videos, and labels in `data/raw/`.
- Use `dataset_split.py` to organize data into train/val splits.

## Model Training
- Run the notebook for training and evaluation.
- Save best model weights in `models/best_model.pt`.

## License
MIT License

## Author
Rahul Ojha
