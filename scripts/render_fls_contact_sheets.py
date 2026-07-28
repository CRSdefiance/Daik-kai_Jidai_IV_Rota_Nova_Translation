from __future__ import annotations

import argparse
import math
import struct
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.scan.compression_probe import decompress_lz10


def _bgr555(value: int) -> tuple[int, int, int, int]:
    red = (value & 0x1F) * 255 // 31
    green = ((value >> 5) & 0x1F) * 255 // 31
    blue = ((value >> 10) & 0x1F) * 255 // 31
    return red, green, blue, 255


def _next_power_of_two(value: int) -> int:
    return 1 << max(3, (value - 1).bit_length())


def _decode_texture(
    pixels: bytes, palette_data: bytes, visible_height: int
) -> Image.Image | None:
    palette = [
        _bgr555(value)
        for (value,) in struct.iter_unpack("<H", palette_data[: len(palette_data) & ~1])
    ]
    if len(palette) not in (16, 256):
        return None

    if len(palette) == 16:
        indices = bytearray(len(pixels) * 2)
        for position, value in enumerate(pixels):
            indices[position * 2] = value & 0x0F
            indices[position * 2 + 1] = value >> 4
    else:
        indices = bytearray(pixels)

    storage_height = min(256, _next_power_of_two(max(8, visible_height)))
    if len(indices) % storage_height:
        return None
    storage_width = len(indices) // storage_height
    if storage_width < 8 or storage_width > 256 or storage_width % 8:
        return None

    image = Image.new("RGBA", (storage_width, storage_height))
    output = image.load()
    for source, color_index in enumerate(indices):
        x = source % storage_width
        y = source // storage_width
        output[x, y] = palette[color_index]
    return image


def _assets(path: Path) -> list[tuple[int, int, Image.Image]]:
    data = path.read_bytes()
    table_offset, count, data_offset = struct.unpack_from("<III", data, 4)
    assets = []
    for index in range(count):
        flags, dimensions, palette_offset, _, pixels_offset, _ = struct.unpack_from(
            "<6I", data, table_offset + index * 24
        )
        try:
            palette = decompress_lz10(data[data_offset + palette_offset :])
            pixels = decompress_lz10(data[data_offset + pixels_offset :])
        except ValueError:
            continue
        visible_height = dimensions & 0xFFFF
        image = _decode_texture(pixels, palette, visible_height)
        if image is not None:
            assets.append((index, flags, image))
    return assets


def render(path: Path, output: Path, per_page: int = 24) -> list[Path]:
    assets = _assets(path)
    output.mkdir(parents=True, exist_ok=True)
    results = []
    cell_width, cell_height = 280, 292
    columns = 4
    for page_index in range(math.ceil(len(assets) / per_page)):
        page_assets = assets[page_index * per_page : (page_index + 1) * per_page]
        rows = math.ceil(len(page_assets) / columns)
        sheet = Image.new("RGB", (columns * cell_width, rows * cell_height), "white")
        draw = ImageDraw.Draw(sheet)
        for cell, (index, flags, image) in enumerate(page_assets):
            x = (cell % columns) * cell_width
            y = (cell // columns) * cell_height
            preview = image.copy()
            preview.thumbnail((256, 256), Image.Resampling.NEAREST)
            sheet.paste(preview.convert("RGB"), (x + 8, y + 24))
            draw.text(
                (x + 8, y + 5),
                f"asset {index:03d}  {image.width}x{image.height}  flags={flags:08X}",
                fill="black",
            )
        first = page_assets[0][0]
        last = page_assets[-1][0]
        destination = output / f"{path.stem}_{first:03d}_{last:03d}.png"
        sheet.save(destination)
        results.append(destination)
    return results


def main() -> None:
    parser = argparse.ArgumentParser(description="Render DK4 FLS tile archives as contact sheets.")
    parser.add_argument("fls", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--per-page", type=int, default=24)
    args = parser.parse_args()
    for result in render(args.fls, args.output, args.per_page):
        print(result)


if __name__ == "__main__":
    main()
