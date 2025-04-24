from PIL import Image
import numpy as np


def animate_subdivision(image_path: str, iteration_counts: list):
    image = Image.open(image_path)
    image_data = np.array(image, dtype=np.uint8)

    last_iteration_count = 0
    frame = 0
    for iteration_count in iteration_counts:
        frame += 1
        last_iteration_count = iteration_count

        Image.fromarray(image_data).save(f"animation/frame_{frame:0>4}.jpg")


iteration_counts = [
    0,
    *range(10),
    *range(20, 100, 10),
    200,
    300,
    500,
    1000,
    *range(2000, 20000, 1000),
    80000,
    80000,
]
animate_subdivision("input/mount.jpg", iteration_counts)
