import os
from PIL import Image
import time

def convert_png_to_bmp(directory):
    print(f"Converting PNG files in {directory} to BMP")
    time.sleep(5)
    for subdir in ["day", "night"]:
        subdir_path = os.path.join(directory, subdir)
        if os.path.exists(subdir_path):
            for filename in os.listdir(subdir_path):
                if filename.endswith(".png"):
                    prefix = 'd' if subdir == "day" else 'n'
                    new_filename = prefix + filename.replace(".png", "")
                    png_path = os.path.join(subdir_path, filename)
                    bmp_path = os.path.join(subdir_path, new_filename.replace(".png", ".bmp"))
                    with Image.open(png_path) as img:
                        img.save(bmp_path, "BMP")
                    print(f"Converted {png_path} to {bmp_path}")

directory = "/Users/shrey/Downloads/Coding/Neon/icon"  
convert_png_to_bmp(directory)