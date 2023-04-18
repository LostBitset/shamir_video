import re

scene_re = re.compile(r"^class (\w+)\((Voiceover)?Scene\)\:")

scenes = []
with open("scene.py", "r") as f:
    for line in f.readlines():
        matches = scene_re.match(line)
        if matches is not None:
            name, _ = matches.groups()
            scenes.append(name)

def makeFfmpegLine(name):
    ch = "├"
    if name == scenes[len(scenes)-1]:
        ch = "└"
    print(f"{ch} {name}")
    return f"file 'media/videos/scene/1080p60/{name}.mp4'"

with open("sceneorder.txt", "w") as f:
    print("Scene List:")
    f.writelines([
        makeFfmpegLine(name) + "\n" for name in scenes
    ])
