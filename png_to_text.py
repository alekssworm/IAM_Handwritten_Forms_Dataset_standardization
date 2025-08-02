from PIL import Image
from pytesseract import pytesseract
from pathlib import Path
import os
from tqdm import tqdm
#tesseract placement folder
pytesseract.tesseract_cmd = r"H:\Tesseract\tesseract.exe"

def ocr_folder_images(input_folder, output_folder, lang="eng"):
    Path(output_folder).mkdir(parents=True, exist_ok=True)

    # Collect list of images
    image_files = [f for f in os.listdir(input_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    print(f"Total images for OCR: {len(image_files)}")

    for image_file in tqdm(image_files, desc="OCR processing", unit="file"):
        try:
            # Load image
            img_path = Path(input_folder) / image_file
            img = Image.open(img_path)

            # Perform OCR
            text = pytesseract.image_to_string(img, lang=lang)

            # Save as .txt
            txt_name = Path(image_file).stem + ".txt"
            txt_path = Path(output_folder) / txt_name
            with open(txt_path, "w", encoding="utf-8") as f:
                f.write(text.strip())

        except Exception as e:
            tqdm.write(f"[ERROR] Error processing {image_file}: {e}")

# Example run
ocr_folder_images(
    input_folder=r"H:\ma",        # Folder with machine-printed text images
    output_folder=r"H:\ma_txt",   # Folder to save txt files
    lang="eng"
)
