import json
import sys
from pathlib import Path
from PIL import Image

def load_image_as_binary_matrix(path, threshold=128):
    img = Image.open(path).convert("RGBA")
    width, height = img.size
    pixels = img.load()

    matrix = []
    for y in range(height):
        row = []
        for x in range(width):
            r, g, b, a = pixels[x, y]
            if a < 128:
                row.append(0)
            else:
                brightness = (r + g + b) / 3
                row.append(1 if brightness < threshold else 0)
        matrix.append(row)
    return matrix

def save_matrix_to_json(matrix, json_path):
    with open(json_path, "w") as f:
        json.dump(matrix, f)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python save_binary_image.py <image.png>")
        sys.exit(1)

    image_path = Path(sys.argv[1])
    if not image_path.is_file():
        print(f"File not found: {image_path}")
        sys.exit(1)

    output_path = image_path.with_suffix('.json')

    matrix = load_image_as_binary_matrix(str(image_path))
    save_matrix_to_json(matrix, str(output_path))
    print(f"Saved binary pixel matrix to {output_path}")
