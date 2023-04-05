#!/bin/bash

# Subtitles hang around for no reason
rm media/videos/scene/*/*.srt || echo "[preview.sh] Leftover srt files not found."

# Caching breaks subcaptions for some reason
manim "-pq""$1" --disable_caching scene.py Top

echo "[preview.sh] Done."

