import os
import hashlib
import logging
from typing import Dict, List

def remove_duplicate_images(folder: str) -> int:
    """
    Remove duplicate image files in a folder based on file content hash.
    Args:
        folder (str): Path to the folder containing images.
    Returns:
        int: Number of duplicates removed.
    """
    hashes: Dict[str, str] = {}
    duplicates: List[str] = []
    try:
        for filename in os.listdir(folder):
            path = os.path.join(folder, filename)
            if not os.path.isfile(path):
                continue
            try:
                with open(path, 'rb') as f:
                    filehash = hashlib.md5(f.read()).hexdigest()
            except Exception as e:
                logging.warning(f"Could not read file {path}: {e}")
                continue
            if filehash in hashes:
                duplicates.append(path)
            else:
                hashes[filehash] = path
        for dup in duplicates:
            try:
                os.remove(dup)
                logging.info(f"Removed: {dup}")
            except Exception as e:
                logging.error(f"Failed to remove {dup}: {e}")
        logging.info(f"Total duplicates removed: {len(duplicates)}")
        return len(duplicates)
    except Exception as e:
        logging.error(f"Error during duplicate removal: {e}")
        return 0

def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )
    folder = r"D:\01_Rahul_personal\01_Rahul_codes\04_AMR_Detection_Machine_learning\Dataset\Data"
    remove_duplicate_images(folder)

if __name__ == "__main__":
    main()
