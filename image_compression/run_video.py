import subprocess
import os


def run():
    os.makedirs("output", exist_ok=True)

    print("Running image compression...")
    subprocess.run(
        ["poetry", "run", "python3", "image_compression/main.py", "--border", "0"]
    )

    print("Converting sequence to video...")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            "1",
            "-i",
            "output/frame_%04d.jpg",
            "output/animation.mp4",
        ]
    )

    print("Playing video")
    subprocess.run(["ffplay", "output/animation.mp4"])
