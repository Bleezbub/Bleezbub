#!/usr/bin/env python3
"""
prep_photo.py
Step 1 of Avi Vashishta's ASCII portrait pipeline.
1. Removes background with rembg
2. Composites onto pure white
3. Applies OpenCV CLAHE contrast enhancement
Output: source-prepped.png
"""
import io
import os
import sys
from pathlib import Path

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.join(HERE, "..")
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "photo.png")
OUT = os.path.join(ROOT, "source-prepped.png")

def main():
    if not os.path.exists(SRC):
        print(f"ERROR: {SRC} not found.")
        sys.exit(1)

    from rembg import remove
    import numpy as np
    import cv2
    from PIL import Image

    print(f"Prepping photo: {SRC}...")
    img_bytes = Path(SRC).read_bytes()

    # 1. Remove background
    removed = remove(img_bytes)
    img = Image.open(io.BytesIO(removed)).convert("RGBA")

    # 2. Composite onto pure white
    white_bg = Image.new("RGBA", img.size, (255, 255, 255, 255))
    white_bg.paste(img, mask=img.split()[3])
    img_gray = white_bg.convert("L")

    # 3. CLAHE local contrast enhancement
    arr = np.array(img_gray)
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    enhanced = clahe.apply(arr)

    out_img = Image.fromarray(enhanced)
    out_img.save(OUT)
    print(f"[OK] Saved {OUT} ({os.path.getsize(OUT):,} bytes)")

if __name__ == "__main__":
    main()
