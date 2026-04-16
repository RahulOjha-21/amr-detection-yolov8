import os
import logging
from typing import List

def rename_images(
    folder: str,
    prefix: str = "AMR_",
    start_number: int = 1,
    extension: str = ".jpg"
) -> None:
    """
    Rename image files in a folder with a custom prefix and sequential numbering.
    Args:
        folder (str): Path to the folder containing images.
        prefix (str): Prefix for renamed files.
        start_number (int): Starting number for renaming.
        extension (str): File extension to filter (default: ".jpg").
    """
    try:
        files: List[str] = [f for f in os.listdir(folder) if f.lower().endswith(extension)]
        files.sort()
        count = start_number
        for file in files:
            old_path = os.path.join(folder, file)
            new_name = f"{prefix}{count:03d}{extension}"
            new_path = os.path.join(folder, new_name)
            if os.path.exists(new_path):
                logging.warning(f"Target file already exists: {new_name}. Skipping.")
                count += 1
                continue
            os.rename(old_path, new_path)
            logging.info(f"Renamed: {file} → {new_name}")
            count += 1
        logging.info("Renaming completed.")
    except Exception as e:
        logging.error(f"Error during renaming: {e}")

def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    folder = r"D:\01_Rahul_personal\01_Rahul_codes\04_AMR_Detection_Machine_learning\Dataset\Data"
    rename_images(folder)

if __name__ == "__main__":
    main()
