from __future__ import annotations

import argparse
import struct
from pathlib import Path

from PIL import Image


def _bgr555(value: int) -> tuple[int, int, int, int]:
    red = (value & 0x1F) * 255 // 31
    green = ((value >> 5) & 0x1F) * 255 // 31
    blue = ((value >> 10) & 0x1F) * 255 // 31
    return red, green, blue, 255


def decode(path: Path) -> Image.Image:
    data = path.read_bytes()
    depth, width_words, height, palette_offset, pixels_offset = struct.unpack_from(
        "<5I", data
    )
    bits_per_pixel = depth & 0xFF
    if bits_per_pixel not in (4, 8):
        raise ValueError(f"unsupported PXL depth: {bits_per_pixel}")

    palette_size = 32 if bits_per_pixel == 4 else 512
    palette_data = data[palette_offset : palette_offset + palette_size]
    palette = [_bgr555(value) for (value,) in struct.iter_unpack("<H", palette_data)]
    packed = data[pixels_offset:]

    if bits_per_pixel == 4:
        width = width_words * 4
        indices = bytearray(len(packed) * 2)
        for position, value in enumerate(packed):
            indices[position * 2] = value & 0x0F
            indices[position * 2 + 1] = value >> 4
    else:
        width = width_words * 2
        indices = bytearray(packed)

    expected = width * height
    if len(indices) != expected:
        raise ValueError(f"pixel size mismatch: expected {expected}, found {len(indices)}")

    image = Image.new("RGBA", (width, height))
    output = image.load()
    for source, color_index in enumerate(indices):
        output[source % width, source // width] = palette[color_index]
    return image


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a DK4 PXL image atlas.")
    parser.add_argument("pxl", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--scale", type=int, default=1)
    args = parser.parse_args()
    image = decode(args.pxl)
    if args.scale < 1:
        raise ValueError("scale must be at least one")
    if args.scale != 1:
        image = image.resize(
            (image.width * args.scale, image.height * args.scale),
            resample=Image.Resampling.NEAREST,
        )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    image.save(args.output)
    print(f"{args.output} ({image.width}x{image.height})")


if __name__ == "__main__":
    main()
