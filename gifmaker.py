import argparse
from PIL import Image
import glob
import sys
import os
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def create_gif(input_paths, output_path, new_width, frame_duration):
    # Load images and handle possible FileNotFoundError
    images = []
    for image_path in input_paths:
        cleaned_path = image_path.strip('\r\n')
        try:
            img = Image.open(cleaned_path)
            images.append(img)
        except FileNotFoundError:
            print(f"Warning: File not found and will be skipped: {cleaned_path}", file=sys.stderr)

    # Ensure there are images to process
    if not images:
        raise ValueError("No images could be loaded. Exiting.")

    # Resize images
    resized_images = []
    for img in images:
        w_percent = (new_width / float(img.size[0]))
        new_height = int((float(img.size[1]) * float(w_percent)))
        img = img.resize((new_width, new_height), Image.LANCZOS)
        resized_images.append(img)

    # Find the smallest width and height among the resized images
    min_width = min(img.size[0] for img in resized_images)
    min_height = min(img.size[1] for img in resized_images)

    # Crop images to the smallest width and height
    cropped_images = []
    for img in resized_images:
        left = (img.width - min_width) / 2
        top = (img.height - min_height) / 2
        right = (img.width + min_width) / 2
        bottom = (img.height + min_height) / 2
        img = img.crop((left, top, right, bottom))
        cropped_images.append(img)

    # Convert images to 'P' mode (palette-based color) for GIF compatibility
    images = [img.convert('P') for img in cropped_images]

    # Save images as a GIF
    images[0].save(output_path, save_all=True, append_images=images[1:], duration=frame_duration, loop=0, optimize=True)
    
def main():
    parser = argparse.ArgumentParser(description='Create a GIF from a series of images.')
    parser.add_argument('input_paths', type=str, nargs='+', help='Input file paths')
    parser.add_argument('-o', '--output', type=str, default='output.gif', help='Output file path')
    parser.add_argument('-w', '--width', type=int, default=640, help='New width for images')
    parser.add_argument('-d', '--duration', type=int, default=600, help='Frame duration in milliseconds')
    
    args = parser.parse_args()
    create_gif(args.input_paths, args.output, args.width, args.duration)

if __name__ == "__main__":
    main()