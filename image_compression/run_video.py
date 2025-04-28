import subprocess
import os
import argparse


def run():
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default="input/Reflections.png")
    parser.add_argument("-b", "--border", default=1)
    args = parser.parse_args()

    os.makedirs("output", exist_ok=True)

    print("Running image compression...")
    subprocess.run(
        [
            "poetry",
            "run",
            "python3",
            "image_compression/main.py",
            "--file",
            f"{args.file}",
            "--border",
            f"{args.border}",
        ]
    )

    print("Converting sequence to video...")
    subprocess.run(
        [
            "ffmpeg",
            "-y",
            "-framerate",
            "1",
            "-i",
            "output/frame_%04d.png",
            "output/animation.mp4",
        ]
    )

    print("Playing video")
    subprocess.run(["ffplay", "output/animation.mp4"])
