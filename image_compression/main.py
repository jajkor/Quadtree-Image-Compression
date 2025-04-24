from PIL import Image
import numpy as np
from numpy.core.multiarray import ndarray
from quadtree import QTree, Point, Node


def animate_subdivision(image_path: str, iteration_counts: list):
    image = Image.open(image_path)
    image_data = np.array(image, dtype=np.uint8)

    last_iteration_count = 0
    frame = 0
    for iteration_count in iteration_counts:
        frame += 1
        last_iteration_count = iteration_count
        subdivide_image(image, image_data)
        # Image.fromarray(image_data).save(f"animation/frame_{frame:0>4}.jpg")


def subdivide_image(image, image_data):
    print()


if __name__ == "__main__":
    iteration_counts = [
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

    # https://jrtechs.net/data-science/implementing-a-quadtree-in-python
    tree = QTree(1, 100)
    tree.subdivide()
    tree.graph()
