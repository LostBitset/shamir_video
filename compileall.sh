#!/bin/bash

echo "Please note that this script does actually render anything. "
echo "It just concatenates generated scenes together in the correct order. "

rm output.mp4 2>/dev/null || echo "(No previous copy to delete.)"
python makesceneorder.py
ffmpeg -f concat -i sceneorder.txt -c copy output.mp4
