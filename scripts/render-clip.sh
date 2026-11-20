#!/usr/bin/env bash
# Render the gta6-clipper-01 Short from the original stills.
#   bash scripts/render-clip.sh [output.mp4]
# Produces a 24 s vertical 1080x1920 30 fps H.264 Short:
#   0-8s   neon sunset hook      ("GTA 6 IS HERE / VICE CITY IS CALLING")
#   8-16s  night skyline middle  ("13 YEARS OF WAITING. ONE CITY.")
#   16-24s make.fun pitch card   ("MAKE CLIPS LIKE THIS WITH AI / AND EARN MONEY ON MAKE.FUN")
# Audio is an original low synth pad generated with ffmpeg's sine source.
# No Rockstar footage, audio, or artwork is used.
set -euo pipefail
cd "$(dirname "$0")/.."

OUT="${1:-gta6-clipper-01-short.mp4}"
FRAMES="${FRAMES:-clip/frames}"

python3 scripts/render-clip.py "$FRAMES"

# One slow zoom-in per still, then concat. Each still is a single image:
# zoompan turns one input frame into 240 frames (8 s at 30 fps).
# (Do NOT -loop the stills: zoompan's d= applies per input frame, so a
# looped still would make the first segment fill the whole clip.)
ffmpeg -y -v error \
  -i "$FRAMES/sunset.png" \
  -i "$FRAMES/skyline.png" \
  -i "$FRAMES/pitch.png" \
  -f lavfi -t 24 -i "sine=frequency=55:duration=24" \
  -f lavfi -t 24 -i "sine=frequency=110:duration=24" \
  -f lavfi -t 24 -i "sine=frequency=165:duration=24" \
  -filter_complex "\
[0:v]scale=1080:1920,zoompan=z='min(zoom+0.00045,1.09)':d=240:s=1080x1920:fps=30[v0]; \
[1:v]scale=1080:1920,zoompan=z='min(zoom+0.00045,1.09)':d=240:s=1080x1920:fps=30[v1]; \
[2:v]scale=1080:1920,zoompan=z='min(zoom+0.00030,1.06)':d=240:s=1080x1920:fps=30[v2]; \
[v0][v1][v2]concat=n=3:v=1:a=0,format=yuv420p[v]; \
[3:a][4:a][5:a]amix=inputs=3:normalize=0,volume=0.10,tremolo=f=0.25:d=0.6[a]" \
  -map "[v]" -map "[a]" -c:v libx264 -preset medium -crf 20 \
  -c:a aac -b:a 96k -movflags +faststart -shortest "$OUT"

ffprobe -v error -show_entries format=duration,size \
  -show_entries stream=width,height,r_frame_rate,codec_name -of default=nw=1 "$OUT"
echo "rendered $OUT"
