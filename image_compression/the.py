import os
import subprocess
import numpy as np
from PIL import Image, ImageDraw
from quadtree import QuadTree, Rectangle, Point


def compress_image_animation(
    image_path, output_dir="animation", max_depth=8, capacity=1
):
    """
    Compress an image using quadtree and create animation frames
    showing the progressive compression process

    Args:
        image_path: Path to the image file
        output_dir: Directory to save animation frames
        max_depth: Maximum depth of the quadtree
        capacity: Capacity of each quadtree node
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load the image and convert to grayscale
    img = Image.open(image_path).convert("L")
    img_array = np.array(img)
    width, height = img.size

    # Create the quadtree
    qt = QuadTree(Rectangle(0, 0, width, height), capacity=capacity)

    # Insert all pixels
    for y in range(height):
        for x in range(width):
            value = img_array[y, x]
            qt.insert(Point(x, y, value))

    # Generate animation frames at different depths
    print("Generating animation frames...")

    # Simple animation to visualize progressive compression
    frames = []

    # Use increasing error thresholds to simulate "uncompressing"
    error_thresholds = [1] + [int(2**i) for i in range(1, max_depth)]

    for frame_num, threshold in enumerate(error_thresholds):
        # Create a copy of the quadtree for this frame
        qt_copy = QuadTree(Rectangle(0, 0, width, height), capacity=capacity)

        # Reinsert all pixels
        for y in range(height):
            for x in range(width):
                value = img_array[y, x]
                qt_copy.insert(Point(x, y, value))

        # Compute average values with this threshold
        qt_copy.compute_average_value(threshold)

        # Create the compressed image for this frame
        compressed_img = Image.new("L", (width, height), color="white")
        qt_copy.draw_compressed_image(compressed_img)

        # Save this frame
        frame_path = os.path.join(output_dir, f"frame_{frame_num:03d}.jpg")
        compressed_img.save(frame_path, quality=95)

        print(f"  Frame {frame_num}: Error threshold = {threshold}")

    # Create a visualization of the final quadtree structure
    qt_viz = qt.visualize()
    qt_viz.save(os.path.join(output_dir, "quadtree_structure.png"))

    return len(error_thresholds)


def create_video_from_frames(input_pattern, output_file, framerate=2):
    """
    Create a video from image frames using ffmpeg

    Args:
        input_pattern: Input file pattern (e.g., "animation/frame_%03d.jpg")
        output_file: Output video file path
        framerate: Frames per second
    """
    print("Creating video from frames...")

    ffmpeg_cmd = [
        "ffmpeg",
        "-y",  # Overwrite output file if it exists
        "-framerate",
        str(framerate),
        "-i",
        input_pattern,
        # Ensure dimensions are even
        "-vf",
        "scale=trunc(iw/2)*2:trunc(ih/2)*2",
        "-c:v",
        "libx264",
        "-crf",
        "18",
        "-pix_fmt",
        "yuv420p",
        output_file,
    ]

    subprocess.run(ffmpeg_cmd, check=True)
    print(f"Video created: {output_file}")


def main():
    """
    Main function to demonstrate quadtree compression with animation
    """
    # Create output directory if it doesn't exist
    output_dir = "animation"
    os.makedirs(output_dir, exist_ok=True)

    # Sample image - replace with path to your image
    # If you don't have an image, this will create a test pattern
    image_path = "test_image.png"

    # Create a test image if no file exists
    if not os.path.exists(image_path):
        print(f"Creating test image at {image_path}")
        create_test_image(image_path)

    # Compress the image and create animation frames
    num_frames = compress_image_animation(
        image_path, output_dir=output_dir, max_depth=8, capacity=1
    )

    # Create video from frames
    create_video_from_frames(
        os.path.join(output_dir, "frame_%03d.jpg"),
        os.path.join(output_dir, "animation.mp4"),
        framerate=2,
    )

    # Play the video if ffplay is available
    try:
        print("Playing video...")
        subprocess.run(["ffplay", os.path.join(output_dir, "animation.mp4")])
    except FileNotFoundError:
        print(
            "ffplay not found. Video saved to:",
            os.path.join(output_dir, "animation.mp4"),
        )


def create_test_image(path, size=(256, 256)):
    """Create a test gradient image for demonstration purposes"""
    # Create a gradient pattern
    x = np.linspace(0, 255, size[0])
    y = np.linspace(0, 255, size[1])
    xx, yy = np.meshgrid(x, y)

    # Create a pattern with gradients and some features
    pattern = np.sin(xx / 20) * 128 + np.cos(yy / 10) * 64 + 127

    # Add some random noise
    noise = np.random.normal(0, 5, size)
    pattern += noise

    # Clip to valid range and convert to uint8
    pattern = np.clip(pattern, 0, 255).astype(np.uint8)

    # Create and save the image
    image = Image.fromarray(pattern, mode="L")
    image.save(path)

    return image


if __name__ == "__main__":
    main()
