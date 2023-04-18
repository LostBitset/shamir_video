#!/bin/bash

echo "RENDERING FULL VIDEO!"
echo "[render.sh] Settings: 1080p60 (-qh)"

echo "[render.sh] -delegate-> [manim]"
manim -qh -a scene.py
echo "[render.sh] <-return- [manim]"

echo "[render.sh] -delegate-> [compileall.sh]"
./compileall.sh
echo "[render.sh] <-return- [compileall.sh]"

echo "[render.sh] Output: output.mp4"
echo "RENDERING FULL VIDEO - ALL DONE!"
