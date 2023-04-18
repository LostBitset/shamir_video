import re

scene_re = re.compile(r"^class (\w+)\((Voiceover)?Scene\)\:")

scenes = []
with open("scene.py", "r") as f:
    for line in f.readlines():
        matches = scene_re.match(line)
        if matches is not None:
            name, _ = matches.groups()
            scenes.append(name)

def makeFfmpegInput(name):
    return f"-i 'media/videos/scene/1080p60/{name}.mp4'"

print("Scene List:")
for name in scenes:
    ch = "├"
    if name == scenes[len(scenes)-1]:
        ch = "└"
    print(f"{ch} {name}")

inputs = " ".join(map(makeFfmpegInput, scenes))

ffmpeg_filter_text = ""
for i in range(len(scenes)):
    ffmpeg_filter_text += f"[{i}:v] "
    if not scenes[i].startswith("SceneCard"):
        ffmpeg_filter_text += f"[{i}:a] "
ffmpeg_filter_text += f"concat=n={len(scenes)}:v=1:a=1 [v] [a]"

filterpart = f"-filter_complex \"{ffmpeg_filter_text}\""

mappings = "-map \"[v]\" -map \"[a]\""

ffmpeg_command = f"ffmpeg {inputs} {filterpart} {mappings} output.mp4"
print("FFmpeg Command:")
print(f">>> {ffmpeg_command}")
