import cv2

import argparse
from QTree import QTree


def displayQuadTree(
    img_name,
    threshold=7,
    minCell=3,
    line_border=1,
    line_color=(0, 0, 255),
):
    imgT = cv2.imread(img_name)
    qt = QTree(threshold, minCell, imgT)
    qt.subdivide()
    qtImg = qt.render_img(thickness=line_border, color=line_color)
    file_name = "output/" + f"frame_{frame:0>4}.png"
    print(file_name)
    cv2.imwrite(file_name, qtImg)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", default="input/Reflections.png")
    parser.add_argument("-b", "--border", default=1)
    args = parser.parse_args()

    threshold_counts = [2**x for x in range(7, -7, -1)]

    frame = 0
    for i in threshold_counts:
        frame += 1
        displayQuadTree(
            args.file,
            threshold=i,
            line_color=(0, 0, 0),
            line_border=int(args.border),
        )
