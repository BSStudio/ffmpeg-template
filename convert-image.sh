#!/bin/bash

# Use magick to generate image in the following formats:
# - AVIF
# - WebP
# - JPEG
# In the following sizes:
# - 1080
# - 720
# - 360

# This should generate 9 images in total keeping the original aspect ratio:
# image-lg.avif
# image-lg.webp
# image-lg.jpg
# image-md.avif
# image-md.webp
# image-md.jpg
# image-sm.avif
# image-sm.webp
# image-sm.jpg

# If the image is smaller than X size, don't generate the larger sizes

# Check if two arguments are provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <file> <folder>"
    exit 1
fi

file="$1"
# If the user provided a folder, use it. Otherwise, use the current directory
folder="${2:-.}"


magick "$file" -resize 1080x1080 "$folder/image-lg.avif"
magick "$file" -resize 1080x1080 "$folder/image-lg.webp"
magick "$file" -resize 1080x1080 "$folder/image-lg.jpeg"
magick "$file" -resize 720x720 "$folder/image-md.avif"
magick "$file" -resize 720x720 "$folder/image-md.webp"
magick "$file" -resize 720x720 "$folder/image-md.jpeg"
magick "$file" -resize 360x360 "$folder/image-sm.avif"
magick "$file" -resize 360x360 "$folder/image-sm.webp"
magick "$file" -resize 360x360 "$folder/image-sm.jpeg"

