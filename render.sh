#!/bin/bash

echo "RENDERING FULL VIDEO!"
echo "[render.sh] Settings: 1080p60 (-qh)"

echo "[render.sh] PURGING EXISTING MEDIA"
rm -rf media 2>/dev/null || echo "(No previous media to purge.)"
echo "[render.sh] PURGING EXISTING MEDIA - STEP DONE"

echo "[render.sh] -delegate-> [manim]"
manim -qh -a scene.py
echo "[render.sh] <-return- [manim]"

echo "[render.sh] -delegate-> [compileall.sh]"
./compileall.sh
echo "[render.sh] <-return- [compileall.sh]"

echo "[render.sh] Output: output.mp4"
echo "RENDERING FULL VIDEO - ALL DONE!"
