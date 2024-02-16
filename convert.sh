#!/bin/bash

# Check if ffmpeg is installed
if ! command -v ffmpeg &> /dev/null; then
    echo "Error: ffmpeg is not installed. Please install ffmpeg."
    exit 1
fi

# Check if two arguments are provided
if [ $# -ne 2 ]; then
    echo "Usage: $0 <file> <folder>"
    exit 1
fi

file="$1"
folder="$2"

ffmpeg -i $file \
  -map 0:v:0 \
  -filter:v:0 scale=480:-1  -maxrate:v:0 775k \
  -map 0:v:0 \
  -filter:v:1 scale=640:-1  -maxrate:v:1 1.2M \
  -map 0:v:0 \
  -filter:v:2 scale=768:-1  -maxrate:v:2 1.5M \
  -map 0:v:0 \
  -filter:v:3 scale=960:-1  -maxrate:v:3 2.5M \
  -map 0:v:0 \
  -filter:v:4 scale=1280:-1 -maxrate:v:4 3.5M \
  -map 0:v:0 \
  -filter:v:5 scale=1920:-1 -maxrate:v:5 5M \
  -map 0:v:0 \
  -filter:v:6 scale=1920:-1 -maxrate:v:6 6.5M \
  -map 0:v:0 \
  -filter:v:7 scale=1920:-1 -maxrate:v:7 8M \
  -var_stream_map "v:0,name:v1
                   v:1,name:v2
                   v:2,name:v3
                   v:3,name:v4
                   v:4,name:v5
                   v:5,name:v6
                   v:6,name:v7
                   v:7,name:v8" \
  -threads 0 \
  -f hls \
  -hls_playlist_type vod \
  -hls_segment_type fmp4 \
  -hls_allow_cache 1 \
  -hls_flags independent_segments+iframes_only \
  -hls_segment_filename "%v/fileSequence%d.ts" \
  -master_pl_name "prog_index.m3u8" \
  "%v/prog_index.m3u8"
