import cv2
import numpy as np
from pathlib import Path
import os
from tqdm import tqdm

# ---- functions for line detection and splitting ----
def find_lines_template_scaled(image_path, template_path, thresholds=[0.6, 0.7, 0.8]):
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    lines_y = []

    for scale in [0.8, 0.9, 1.0, 1.1, 1.2]:
        scaled_template = cv2.resize(template, None, fx=scale, fy=scale, interpolation=cv2.INTER_LINEAR)
        result = cv2.matchTemplate(img, scaled_template, cv2.TM_CCOEFF_NORMED)

        for thresh in thresholds:
            loc = np.where(result >= thresh)
            for pt in zip(*loc[::-1]):
                lines_y.append(pt[1])

    return lines_y

def merge_line_clusters(lines, tolerance=20):
    if not lines:
        return []
    lines = sorted([int(y) for y in lines])
    merged = []
    current_cluster_start = lines[0]
    for y in lines[1:]:
        if y - current_cluster_start > tolerance:
            merged.append(current_cluster_start)
            current_cluster_start = y
    merged.append(current_cluster_start)
    return merged

def split_image_save(image_path, template_path, output_ma, output_hw):
    lines = find_lines_template_scaled(image_path, template_path)
    merged_lines = merge_line_clusters(lines)

    if len(merged_lines) < 3:
        print(f"[WARN] Failed to find 3 lines for {image_path}")
        return

    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    y1, y2, y3 = merged_lines[0], merged_lines[1], merged_lines[2]

    # Save printed
    printed = img[y1:y2, :]
    printed_path = Path(output_ma) / (Path(image_path).stem + "_printed.png")
    cv2.imwrite(str(printed_path), printed)

    # Save handwritten
    handwritten = img[y2:y3, :]
    handwritten_path = Path(output_hw) / (Path(image_path).stem + "_handwritten.png")
    cv2.imwrite(str(handwritten_path), handwritten)

# ---- batch processing with tqdm ----
def process_dataset(data_folder, template_path, output_ma, output_hw):
    Path(output_ma).mkdir(parents=True, exist_ok=True)
    Path(output_hw).mkdir(parents=True, exist_ok=True)

    # List of all images
    image_files = []
    for root, dirs, files in os.walk(data_folder):
        for file in files:
            if file.lower().endswith(('.png', '.jpg', '.jpeg')):
                image_files.append(os.path.join(root, file))

    total = len(image_files)
    print(f"Total files to process: {total}")

    # tqdm progress
    for image_path in tqdm(image_files, desc="Processing images", unit="file"):
        try:
            split_image_save(image_path, template_path, output_ma, output_hw)

            # Output folder name + file name
            folder_name = Path(image_path).parent.name
            file_name = Path(image_path).name
            tqdm.write(f"Done: {folder_name}/{file_name}")

        except Exception as e:
            tqdm.write(f"[ERROR] Error while processing {image_path}: {e}")

# Example run
process_dataset(
     data_folder=r"H:\archive\data",
     template_path=r"E:\cut_image_to_dataset\test.png",
     output_ma=r"H:\ma",
     output_hw=r"H:\hw"
)
