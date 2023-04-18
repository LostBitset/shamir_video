#!/bin/bash

echo "Please note that this script does actually render anything. "
echo "It just concatenates generated scenes together in the correct order. "

python makesceneorder.py
ffmpeg -f concat -i sceneorder.txt -c copy output.mp4
