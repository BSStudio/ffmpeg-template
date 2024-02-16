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

ffmpeg -hide_banner -i $file \
  -filter_complex \
  "
    [0:v]split=8[v1][v2][v3][v4][v5][v6][v7][v8]; \
    [v1]scale=480:-1[v1scaled]; \
    [v2]scale=640:-1[v2scaled]; \
    [v3]scale=768:-1[v3scaled]; \
    [v4]scale=960:-1[v4scaled]; \
    [v5]scale=1280:-1[v5scaled]; \
    [v6]scale=1920:-1[v6scaled]; \
    [v7]scale=1920:-1[v7scaled]; \
    [v8]scale=1920:-1[v8scaled]; \
    [0:a]aformat=channel_layouts=stereo[a1] \
    " \
  -map "[v1scaled]" -maxrate 775k \
  -map "[v2scaled]" -maxrate 1.2M \
  -map "[v3scaled]" -maxrate 1.5M \
  -map "[v4scaled]" -maxrate 2.5M \
  -map "[v5scaled]" -maxrate 3.5M \
  -map "[v6scaled]" -maxrate 5M   \
  -map "[v7scaled]" -maxrate 6.5M \
  -map "[v8scaled]" -maxrate 8M   \
  -map "[a1]" \
  -var_stream_map \
  " \
    a:0,agroup:audio,default:yes,name:a1 \
    v:0,agroup:audio,name:v1 \
    v:1,agroup:audio,name:v2 \
    v:2,agroup:audio,name:v3 \
    v:3,agroup:audio,name:v4 \
    v:4,agroup:audio,name:v5 \
    v:5,agroup:audio,name:v6 \
    v:6,agroup:audio,name:v7 \
    v:7,agroup:audio,name:v8" \
  -threads 0 \
  -f hls \
  -hls_playlist_type vod \
  -hls_segment_type fmp4 \
  -hls_allow_cache 1 \
  -hls_flags independent_segments+iframes_only \
  -hls_segment_filename "%v/fileSequence%d.ts" \
  -master_pl_name "prog_index.m3u8" \
  "%v/prog_index.m3u8"
