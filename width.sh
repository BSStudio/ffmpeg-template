#!/bin/bash

# Check if the user provided a video file path
if [ $# -ne 1 ]; then
    echo "Usage: $0 <video_file>"
    exit 1
fi

# Check if ffprobe is installed
if ! command -v ffprobe &> /dev/null; then
    echo "Error: ffprobe is not installed. Please install ffmpeg."
    exit 1
fi

video_file="$1"

# Use ffprobe to get video width
ffprobe -v error -select_streams v:0 -show_entries stream=width -of csv=s=x:p=0 "$video_file"
