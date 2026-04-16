import cv2
import os
import logging

def extract_frames_from_video(
    video_path: str,
    output_folder: str,
    prefix: str = "AMR_",
    start_number: int = 1,
    frame_interval: int = 1
) -> int:
    """
    Extract frames from a video and save them as images.
    Args:
        video_path (str): Path to the video file.
        output_folder (str): Folder to save extracted frames.
        prefix (str): Filename prefix for saved images.
        start_number (int): Starting number for filenames.
        frame_interval (int): Interval for saving frames.
    Returns:
        int: Number of frames saved.
    """
    os.makedirs(output_folder, exist_ok=True)
    cap = cv2.VideoCapture(video_path)
    frame_count = 0
    save_count = start_number
    saved_frames = 0
    if not cap.isOpened():
        logging.error(f"Cannot open video: {video_path}")
        return 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if frame_count % frame_interval == 0:
            filename = f"{prefix}{save_count:03d}.jpg"
            filepath = os.path.join(output_folder, filename)
            try:
                cv2.imwrite(filepath, frame)
                logging.info(f"Saved: {filename}")
                save_count += 1
                saved_frames += 1
            except Exception as e:
                logging.error(f"Failed to save {filename}: {e}")
        frame_count += 1
    cap.release()
    logging.info(f"Frame extraction complete! Total frames saved: {saved_frames}")
    return saved_frames

def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    video_path = r"D:\01_Rahul_personal\01_Rahul_codes\04_AMR_Detection_Machine_learning\Dataset\Videos\AMR_Video2.mp4"
    output_folder = r"D:\01_Rahul_personal\01_Rahul_codes\04_AMR_Detection_Machine_learning\Dataset\Data"
    prefix = "AMR_"
    start_number = 19
    frame_interval = 20
    extract_frames_from_video(video_path, output_folder, prefix, start_number, frame_interval)

if __name__ == "__main__":
    main()
