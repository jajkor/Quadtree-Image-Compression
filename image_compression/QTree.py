import math
import cv2
import numpy as np


class Node:
    def __init__(self, x0, y0, w, h):
        self.x0 = x0
        self.y0 = y0
        self.width = w
        self.height = h
        self.children = []

    def get_width(self):
        return self.width

    def get_height(self):
        return self.height

    def get_points(self, img):
        return img[
            self.x0: self.x0 + self.get_width(), self.y0: self.y0 + self.get_height()
        ]

    def get_error(self, img):
        pixels = self.get_points(img)
        b_avg = np.mean(pixels[:, :, 0])
        b_mse = np.square(np.subtract(pixels[:, :, 0], b_avg)).mean()

        g_avg = np.mean(pixels[:, :, 1])
        g_mse = np.square(np.subtract(pixels[:, :, 1], g_avg)).mean()

        r_avg = np.mean(pixels[:, :, 2])
        r_mse = np.square(np.subtract(pixels[:, :, 2], r_avg)).mean()

        e = r_mse * 0.2989 + g_mse * 0.5870 + b_mse * 0.1140

        return (e * img.shape[0] * img.shape[1]) / 90000000


class QTree:
    def __init__(self, stdThreshold, minPixelSize, img):
        self.threshold = stdThreshold
        self.min_size = minPixelSize
        self.minPixelSize = minPixelSize
        self.img = img
        self.root = Node(0, 0, img.shape[0], img.shape[1])

    def get_points(self):
        return self.img[
            self.root.x0: self.root.x0 + self.root.get_width(),
            self.root.y0: self.root.y0 + self.root.get_height(),
        ]

    def subdivide(self):
        recursive_subdivide(self.root, self.threshold,
                            self.minPixelSize, self.img)

    def render_img(self, thickness=1, color=(0, 0, 255)):
        imgc = self.img.copy()
        c = find_children(self.root)
        for n in c:
            pixels = n.get_points(self.img)
            # grb
            gAvg = math.floor(np.mean(pixels[:, :, 0]))
            rAvg = math.floor(np.mean(pixels[:, :, 1]))
            bAvg = math.floor(np.mean(pixels[:, :, 2]))

            imgc[n.x0: n.x0 + n.get_width(), n.y0: n.y0 +
                 n.get_height(), 0] = gAvg
            imgc[n.x0: n.x0 + n.get_width(), n.y0: n.y0 +
                 n.get_height(), 1] = rAvg
            imgc[n.x0: n.x0 + n.get_width(), n.y0: n.y0 +
                 n.get_height(), 2] = bAvg

        if thickness > 0:
            for n in c:
                # Draw a rectangle
                imgc = cv2.rectangle(
                    imgc,
                    (n.y0, n.x0),
                    (n.y0 + n.get_height(), n.x0 + n.get_width()),
                    color,
                    thickness,
                )
        return imgc


def find_children(node):
    if not node.children:
        return [node]
    else:
        children = []
        for child in node.children:
            children += find_children(child)
    return children


def recursive_subdivide(node, k, minPixelSize, img):
    if node.get_error(img) <= k:
        return
    w_1 = int(math.floor(node.width / 2))
    w_2 = int(math.ceil(node.width / 2))
    h_1 = int(math.floor(node.height / 2))
    h_2 = int(math.ceil(node.height / 2))

    if w_1 <= minPixelSize or h_1 <= minPixelSize:
        return
    x1 = Node(node.x0, node.y0, w_1, h_1)  # top left
    recursive_subdivide(x1, k, minPixelSize, img)

    x2 = Node(node.x0, node.y0 + h_1, w_1, h_2)  # btm left
    recursive_subdivide(x2, k, minPixelSize, img)

    x3 = Node(node.x0 + w_1, node.y0, w_2, h_1)  # top right
    recursive_subdivide(x3, k, minPixelSize, img)

    x4 = Node(node.x0 + w_1, node.y0 + h_1, w_2, h_2)  # btm right
    recursive_subdivide(x4, k, minPixelSize, img)

    node.children = [x1, x2, x3, x4]
