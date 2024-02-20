# web-media-converter-scripts

This repo stores a template for
 * generating VOD (Video On Demand) files for the bsstudio.hu project
 * generating optimised images for the bsstudio.hu web project

# Usage

## Convert image
```bash
./convert_image.py ./sample/original.jpeg ./docs
```
1. The first argument is the path to the original image.
2. The second (optional) argument is the path to the output directory.
   It's the current directory by default.

## Convert video
```bash
./convert_video.py ./sample/original.mp4 ./docs
```
1. The first argument is the path to the original video.
2. The second (optional) argument is the path to the output directory.
   It's the current directory by default.

# Sample media file

## Video
The sample media file is a copy of the Big Buck Bunny movie,
which is licensed under the Creative Commons Attribution 3.0 license.
The original file can be found at https://peach.blender.org/download/

I used the following ffmpeg command to keep only the first 30 seconds of the movie
```bash
curl -O http://distribution.bbb3d.renderfarming.net/video/mp4/bbb_sunflower_1080p_30fps_normal.mp4
ffmpeg -i bbb_sunflower_1080p_30fps_normal.mp4 -t 30 -c copy ./media/original.mp4
rm bbb_sunflower_1080p_30fps_normal.mp4
```

## Photo
An image I took with my phone in Connemara, Ireland.  
![Original photo](./sample/original.jpeg)
`iPhone 15 Pro f/1.8 1/7092 6.86mm ISO80`

# Generated formats
The attempts to follow Apple's recommendations for HTTP Live Streaming (HLS) format.
https://developer.apple.com/streaming/examples/

 * 8 video variants
   * Gear 1 - 480x270 @ 775 kbps
   * Gear 2 - 640x360 @ 1.2 Mbps
   * Gear 3 - 768x432 @ 1.5 Mbps
   * Gear 4 - 960x540 @ 2.5 Mbps
   * Gear 5 - 1280x720 @ 3.5 Mbps
   * Gear 6 - 1920x1080 @ 5 Mbps
   * Gear 7 - 1920x1080 @ 6.5 Mbps
   * Gear 8 - 1920x1080 @ 8 Mbps
 * 1 audio variant
   * original audio (this will change)

# Generated files
## Video
A HSL (HTTP Live Streaming) web player should be pointed at the ./prog_index.m3u8 file.  
After that the web player can figure out what format the client can play and start streaming the video.
```
📁 ./
├─ 📄️ prog_index.m3u8
├─ 📁️ a1/
│  ├─ 📄️ prog_index.m3u8
│  ├─ 🎵️ int0.mp4
│  ├─ 🎵️ fileSequence0.aac
│  ├─ 🎵️ fileSequence1.aac
│  ├─ [...]
├─ 📁️ v1/
│  ├─ 📄️ prog_index.m3u8
│  ├─ 🎞️ int1.mp4
│  ├─ 🎞️ fileSequence0.ts
│  ├─ 🎞️ fileSequence1.ts
│  ├─ [...]
├─ 📁️ v2/
│  ├─ 📄️ prog_index.m3u8
│  ├─ 🎞️ int2.mp4
│  ├─ 🎞️ fileSequence0.ts
│  ├─ 🎞️ fileSequence1.ts
│  ├─ [...]
├─ 📁️ v3/
│  ├─ 📄️ prog_index.m3u8
│  ├─ 🎞️ int1.mp4
│  ├─ 🎞️ fileSequence0.ts
│  ├─ 🎞️ fileSequence1.ts
│  ├─ [...]
├─ 📁️ v4/
│  ├─ 📄️ prog_index.m3u8
│  ├─ 🎞️ int4.mp4
│  ├─ 🎞️ fileSequence0.ts
│  ├─ 🎞️ fileSequence1.ts
│  ├─ [...]
├─ 📁️ v5/
│  ├─ 📄️ prog_index.m3u8
│  ├─ 🎞️ int5.mp4
│  ├─ 🎞️ fileSequence0.ts
│  ├─ 🎞️ fileSequence1.ts
│  ├─ [...]
├─ 📁️ v6/
│  ├─ 📄️ prog_index.m3u8
│  ├─ 🎞️ int6.mp4
│  ├─ 🎞️ fileSequence0.ts
│  ├─ 🎞️ fileSequence1.ts
│  ├─ [...]
├─ 📁️ v7/
│  ├─ 📄️ prog_index.m3u8
│  ├─ 🎞️ int7.mp4
│  ├─ 🎞️ fileSequence0.ts
│  ├─ 🎞️ fileSequence1.ts
│  ├─ [...]
├─ 📁️ v8/
│  ├─ 📄️ prog_index.m3u8
│  ├─ 🎞️ int8.mp4
│  ├─ 🎞️ fileSequence0.ts
│  ├─ 🎞️ fileSequence1.ts
│  ├─ [...]
```

## Photo
```
📁 ./
├─ 🖼️️ image-lg.avif
├─ 🖼️️ image-lg.webp
├─ 🖼️️ image-lg.jpeg
├─ 🖼️️ image-md.avif
├─ 🖼️️ image-md.webp
├─ 🖼️️ image-md.jpeg
├─ 🖼️️ image-sm.avif
├─ 🖼️️ image-sm.webp
├─ 🖼️️ image-sm.jpeg
```
