#!/usr/bin/python3
import subprocess
import sys
import os
import collections

Stream = collections.namedtuple('Stream', ['width', 'bitrate'])

def verify_command(command):
    try:
        subprocess.run(
            args=[command, "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
        subprocess.run(
            args=[command, "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
    except subprocess.CalledProcessError:
        print(f"Error: ${command} not found.")
        sys.exit(1)


def get_video_width(file_path):
    try:
        result = subprocess.run(
            args=["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width", "-of", "csv=p=0", file_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True,
            text=True
        )
        return int(result.stdout.strip())
    except subprocess.CalledProcessError:
        print("Error: Failed to retrieve video width.")
        sys.exit(1)


if __name__ == "__main__":
    verify_command("ffmpeg")
    verify_command("ffprobe")

    if len(sys.argv) < 2:
        print("Usage: script.py input_file [output_folder]")
        sys.exit(1)

    input_file = sys.argv[1]
    if not os.path.isfile(input_file):
        print(f"Error: The first argument `{input_file}` is not a file.")
        sys.exit(1)

    output_folder = os.getcwd()
    if len(sys.argv) > 2:
        output_folder = sys.argv[2]
        if not os.path.isdir(output_folder):
            print(f"Error: Output folder not found: {output_folder}")
            sys.exit(1)

    video_width = get_video_width(input_file)

    streams = [
        Stream(480, '775k'),
        Stream(640, '1.2M'),
        Stream(768, '1.5M'),
        Stream(960, '2.5M'),
        Stream(1280, '3.5M'),
        Stream(1920, '5M'),
        Stream(1920, '6.5M'),
        Stream(1920, '8M'),
    ]

    filtered_streams = [stream for stream in streams if stream.width <= video_width]

    ffmpeg_command = f"""
    ffmpeg -hide_banner -i {input_file} \\
        -filter_complex \\
        " \\
            [0:a]aformat=channel_layouts=stereo[a1]; \\
            [0:v]split={len(filtered_streams)}"""
    
    # create a name for each stream that was created by the split filter
    ffmpeg_command += ''.join([f"[v{i+1}]" for i in range(len(filtered_streams))])

    # apply different aspect ratio for each stream
    for index, (width, bitrate) in enumerate(filtered_streams):
        ffmpeg_command += f"""; \\
            [v{index + 1}]scale={width}:-2[v{index + 1}scaled]"""

    # pass audio stream
    ffmpeg_command += f""" \\
        " \\
        -map "[a1]" \\"""

    # use high compression, remove audio, set max bitrate for each stream
    # also enable faststart for better web support
    for index, (width, bitrate) in enumerate(filtered_streams):
        ffmpeg_command += f"""
        -map "[v{index + 1}scaled]" -preset veryslow -movflags +faststart -an -maxrate {bitrate} \\"""

    # define audio stream for HLS
    ffmpeg_command += f"""
        -var_stream_map \\
        " \\
            a:0,agroup:audio,default:yes,name:a1"""

    # define video streams for HLS
    for index, (width, bitrate) in enumerate(filtered_streams):
        ffmpeg_command += f""" \\
            v:{index},agroup:audio,name:v{index + 1}"""

    # close bracket
    ffmpeg_command += ' \\\n        " \\'

    # apply HLS settings and naming conventions
    ffmpeg_command += f"""
        -threads 0 \\
        -f hls \\
        -hls_playlist_type vod \\
        -hls_segment_type fmp4 \\
        -hls_allow_cache 1 \\
        -hls_flags independent_segments+iframes_only \\
        -hls_segment_filename "{output_folder}/%v/fileSequence%d.ts" \\
        -master_pl_name "{output_folder}/prog_index.m3u8" \\
        "{output_folder}/%v/prog_index.m3u8"
    """

    print("Executing command:", ffmpeg_command)
    subprocess.run(ffmpeg_command, shell=True)
