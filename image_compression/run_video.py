import subprocess
import os


def run():
    os.makedirs("animation", exist_ok=True)

    print("Running image compression...")
    subprocess.run(["poetry", "run", "python3", "image_compression/main.py"])

    print("Converting sequence to video...")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            "2",
            "-i",
            "animation/frame_%04d.jpg",
            "animation/animation.mp4",
        ]
    )

    print("Playing video")
    subprocess.run(["ffplay", "animation/animation.mp4"])
