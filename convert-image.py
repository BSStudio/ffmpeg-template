#!/usr/bin/python3

import subprocess
import sys
import os


def check_installed(command):
    try:
        subprocess.run(
            args=[command, "-version"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False


def get_image_height(image_file):
    result = subprocess.run(
        args=["identify", "-format", "%h", image_file],
        stdout=subprocess.PIPE,
        text=True
    )
    return int(result.stdout.strip())


def generate_image(image_file, size, dimension, image_format, output_folder):
    output_file = os.path.join(output_folder, f"image-{size}.{image_format}")
    subprocess.run(
        ["magick", image_file, "-resize", dimension, output_file]
    )


if __name__ == "__main__":
    # Use subprocess to determine if `identify` is installed
    if not check_installed("identify"):
        print("Error: 'identify' command not found. Please install ImageMagick.")
        sys.exit(1)

    # Use subprocess to determine if `magick` is installed
    if not check_installed("magick"):
        print("Error: 'magick' command not found. Please install ImageMagick.")
        sys.exit(1)

    # Verify there's an argument for the image file
    if len(sys.argv) < 2:
        print("Usage: python script.py <image_file> [output_folder]")
        sys.exit(1)

    # Save the argument as a variable `image_file`
    image_file = sys.argv[1]

    # Verify if the image file exists
    if not os.path.isfile(image_file):
        print(f"Error: Image file not found: {image_file}")
        sys.exit(1)

    # Verify if there's an optional argument for the output folder
    # Otherwise, use the current working directory
    output_folder = os.getcwd()
    if len(sys.argv) > 2:
        output_folder = sys.argv[2]
        if not os.path.isdir(output_folder):
            print(f"Error: Output folder not found: {output_folder}")
            sys.exit(1)

    # Verify if the output folder exists
    if not os.path.isdir(output_folder):
        print(f"Error: Output folder not found: {output_folder}")
        sys.exit(1)

    # Generate different sizes of the image
    sizes = {
        "xlg": (2160, "2160x2160"),
        "lg": (1080, "1080x1080"),
        "md": (720, "720x720"),
        "sm": (360, "360x360")
    }

    # Use subprocess to determine the height of the image using `identify`
    image_height = get_image_height(image_file)
    print(f"Image height: {image_height}")

    for size, dimensions in sizes.items():
        # Don't generate images for sizes
        # that are larger than the original image
        if dimensions[0] <= image_height:
            for image_format in ["avif", "webp", "jpeg"]:
                generate_image(image_file, size, dimensions[1], image_format, output_folder)
    print("Images generated successfully.")
