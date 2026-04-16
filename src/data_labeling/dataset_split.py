import os
import random
import shutil
import logging
from typing import List

def copy_files(
    image_list: List[str],
    image_dest: str,
    label_dest: str,
    source_folder: str,
    output_folder: str
) -> None:
    for image in image_list:
        base_name = os.path.splitext(image)[0]
        image_src = os.path.join(source_folder, image)
        label_src = os.path.join(source_folder, base_name + ".txt")
        image_dst = os.path.join(output_folder, image_dest, image)
        label_dst = os.path.join(output_folder, label_dest, base_name + ".txt")
        try:
            shutil.copy(image_src, image_dst)
            if os.path.exists(label_src):
                shutil.copy(label_src, label_dst)
            else:
                logging.warning(f"Missing label for {image}")
        except Exception as e:
            logging.error(f"Failed to copy {image}: {e}")

def split_dataset(
    source_folder: str,
    output_folder: str,
    train_ratio: float = 0.8,
    random_seed: int = 42
) -> None:
    """
    Split dataset into train and validation sets, copying images and labels.
    Args:
        source_folder (str): Folder containing images and labels.
        output_folder (str): Output dataset folder.
        train_ratio (float): Ratio of training data.
        random_seed (int): Seed for reproducibility.
    """
    random.seed(random_seed)
    folders = [
        "images/train",
        "images/val",
        "labels/train",
        "labels/val"
    ]
    for folder in folders:
        os.makedirs(os.path.join(output_folder, folder), exist_ok=True)
    images = [f for f in os.listdir(source_folder) if f.lower().endswith(".jpg")]
    random.shuffle(images)
    split_index = int(len(images) * train_ratio)
    train_images = images[:split_index]
    val_images = images[split_index:]
    logging.info(f"Total images: {len(images)}")
    logging.info(f"Training images: {len(train_images)}")
    logging.info(f"Validation images: {len(val_images)}")
    copy_files(train_images, "images/train", "labels/train", source_folder, output_folder)
    copy_files(val_images, "images/val", "labels/val", source_folder, output_folder)
    logging.info("Dataset split complete!")

def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    source_folder = r"D:\01_Rahul_personal\01_Rahul_codes\04_AMR_Detection_Machine_learning\Dataset\Data"
    output_folder = "amr_dataset"
    train_ratio = 0.8
    random_seed = 42
    split_dataset(source_folder, output_folder, train_ratio, random_seed)

if __name__ == "__main__":
    main()
