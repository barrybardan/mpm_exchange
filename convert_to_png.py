import os
from PIL import Image

def convert_webp_to_png(directory):

    for root, dirs, files in os.walk(directory):
        for filename in files:
            # Check if the file has a .webp extension
            if filename.lower().endswith('.webp'):
                webp_path = os.path.join(root, filename)

                # Open the WebP image using Pillow (PIL)
                with Image.open(webp_path) as img:
                    # Get the path and name without the extension
                    name, _ = os.path.splitext(webp_path)

                    # Save the image as a PNG with the same name in the same directory
                    png_path = name + ".png"
                    img.save(png_path, 'PNG')

                    print(f"Converted {webp_path} to {png_path}")



def main():
    directory_path = 'pics/spb.metprommebel.ru/upload/webp'
    convert_webp_to_png(directory_path)

if __name__ == "__main__":
    main()