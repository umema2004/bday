import os
from PIL import Image
import pillow_heif

# Register HEIC support
pillow_heif.register_heif_opener()

# Folder where secret.html lives (same folder as this script)
folder_path = r"."

image_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".gif", ".tiff", ".webp",
                    ".heic", ".jfif", ".avif", ".apng")

image_files = sorted(
    [f for f in os.listdir(folder_path) if f.lower().endswith(image_extensions)
     and not f.lower().startswith("photo")],
    key=lambda f: f.lower()
)

if not image_files:
    # All files already named photo*.* — just convert any non-jpg ones
    image_files = sorted(
        [f for f in os.listdir(folder_path) if f.lower().endswith(image_extensions)],
        key=lambda f: f.lower()
    )

converted = 0
for i, filename in enumerate(image_files, start=1):
    src = os.path.join(folder_path, filename)
    dst = os.path.join(folder_path, f"photo{i}.jpg")
    if os.path.abspath(src) == os.path.abspath(dst):
        print(f"Skipping {filename} (already correct)")
        continue
    try:
        img = Image.open(src).convert("RGB")
        img.save(dst, "JPEG", quality=90)
        print(f"Converted {filename} → photo{i}.jpg")
        converted += 1
    except Exception as e:
        print(f"ERROR on {filename}: {e}")

print(f"\nDone — {converted} files converted to JPG.")