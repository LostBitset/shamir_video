#!/bin/bash

echo "Please note that this script does actually render anything. "
echo "It just concatenates generated scenes together in the correct order. "

rm output.mp4
python makesceneorder.py
ffmpeg -i sceneorder.txt -c copy output.mp4
