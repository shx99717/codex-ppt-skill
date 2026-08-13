"""Shared slide-image ratio checks, gpt-image-2 size table, and uniform contain placement."""

from __future__ import annotations

RATIO_RELATIVE_TOLERANCE = 0.02
RATIO_BY_LABEL = {"16:9": 16 / 9, "4:3": 4 / 3, "3:2": 3 / 2}
GPT_IMAGE_SIZE = {"16:9": "2560x1440", "4:3": "2560x1920", "3:2": "2400x1600"}


def is_ratio(width, height, expected, relative_tolerance=RATIO_RELATIVE_TOLERANCE) -> bool:
    if height <= 0 or width <= 0 or expected <= 0:
        return False
    return abs((width / height) / expected - 1.0) <= relative_tolerance


def is_16_9(width, height, relative_tolerance=RATIO_RELATIVE_TOLERANCE) -> bool:
    return is_ratio(width, height, 16 / 9, relative_tolerance)


def gpt_image_size(label: str) -> str:
    if label not in GPT_IMAGE_SIZE:
        raise KeyError(label)
    return GPT_IMAGE_SIZE[label]


def image_size(path: str) -> tuple[int, int]:
    from PIL import Image

    with Image.open(path) as im:
        return im.size


def require_image_ratio(path, expected, label, relative_tolerance=RATIO_RELATIVE_TOLERANCE):
    width, height = image_size(path)
    if not is_ratio(width, height, expected, relative_tolerance):
        ratio = (width / height) if height else 0.0
        raise ValueError(
            f"Slide image must be {label} (2% relative): {path} is {width}x{height} "
            f"(ratio {ratio:.4f}, expected {expected:.4f}). Do not stretch."
        )
    return width, height


def uniform_picture_box(image_w, image_h, box_w, box_h):
    scale = min(box_w / image_w, box_h / image_h)
    width = int(image_w * scale)
    height = int(image_h * scale)
    left = (box_w - width) // 2
    top = (box_h - height) // 2
    return left, top, width, height
