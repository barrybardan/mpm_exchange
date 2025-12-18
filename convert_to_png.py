import os
from PIL import Image

def convert_webp_to_png(directory, pic_path_list=None):

    print(pic_path_list)

    if pic_path_list is not None:
        for pic_path in pic_path_list:
            root, filename = os.path.split(pic_path)
            convert_single_webp_to_png(root,filename)
        return    

    for root, dirs, files in os.walk(directory):
        for filename in files:
            convert_single_webp_to_png(root,filename)
            # Check if the file has a .webp extension

def convert_single_webp_to_png(root,filename):
    if filename.lower().endswith('.webp'):
        webp_path = os.path.join(root, filename)
        print(webp_path)
        name, _ = os.path.splitext(webp_path)
        png_path = name + ".png"
        if os.path.isfile(png_path):
            print("FOUND png, SKIPPING")
            return
        
        # Open the WebP image using Pillow (PIL)
        with Image.open(webp_path) as img:
            # Get the path and name without the extension

            # Save the image as a PNG with the same name in the same directory
            img.save(png_path, 'PNG')
            print(f"Converted {webp_path} to {png_path}")

def make_thumbnails(directory, new_size):
    thumb_size = (new_size,new_size)

    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.lower().endswith('.webp'):
                continue
            if filename.find("_"+str(new_size)) > 0:
                continue
            # Check if the file has a .webp extension
            webp_path = os.path.join(root, filename)

            # Open the WebP image using Pillow (PIL)
            with Image.open(webp_path) as img:
                # Get the path and name without the extension
                name, _ = os.path.splitext(webp_path)

                # Save the image as a PNG with the same name in the same directory
                thumb_path = name + "_"+str(new_size)+".png"
                try:
                    img = img.convert('RGBA')
                    img.thumbnail(thumb_size, Image.Resampling.LANCZOS)
                    img.save(thumb_path, 'PNG')
                    # print(f"Resized {webp_path} to {thumb_path}")
                except:
                    print('error converting' + webp_path)
                


def main():
    # convert_webp_to_png('pics/spb.metprommebel.ru/upload/webp')
    convert_webp_to_png('y:/temp/mpm_site_data/pics')


    
    # make_thumbnails('pics/spb.metprommebel.ru',180)

if __name__ == "__main__":
    main()