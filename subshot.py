import os
import cv2
import pytesseract
from PIL import Image
from pathlib import Path

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def get_subtitle(img_path):
    img = cv2.imread(str(img_path))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    sub = pytesseract.image_to_string(binary).strip()
    if len(sub) < 2:
        return None
    valid_characters = []
    for i in sub:
        if i.isalnum() or i in (' ', '-', '_'):
            valid_characters.append(i)
    clean_sub = "".join(valid_characters)
    clean_sub = clean_sub.replace(" ", "_")
    return clean_sub[:100]

def rename_files(path):
    folder = Path(path)

    renamed_folder = folder / 'renamed'
    renamed_folder.mkdir(exist_ok=True)
    
    supported_file_types = {'.png', '.jpg', '.jpeg'}
    
    for image_files in folder.iterdir():
        # Skip the renamed folder itself
        if image_files.name == 'renamed':
            continue
            
        if image_files.suffix.lower() in supported_file_types:
            try:
                sub = get_subtitle(image_files)
                if sub:
                    new_name = sub + image_files.suffix

                    new_path = renamed_folder / new_name

                    image_files.rename(new_path)
                    print(f"Renamed and moved: {image_files.name} -> {new_name}")
                else:
                    print(f"No sub found in: {image_files.name}")
            except Exception as e:
                print(f"Error processing {image_files.name}: {str(e)}")

if __name__ == "__main__":
    screenshots_folder = r'./sample1000'
    rename_files(screenshots_folder)