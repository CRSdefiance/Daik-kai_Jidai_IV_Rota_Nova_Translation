from __future__ import annotations

import argparse
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.formats.ilnk import IlnkContainer


def render(input_path: Path, output: Path, width: int = 64) -> None:
    container = IlnkContainer.parse(input_path.read_bytes())
    tiles: list[Image.Image] = []
    for block in container.blocks:
        pixels = [nibble * 17 for value in block for nibble in (value & 0x0F, value >> 4)]
        height = math.ceil(len(pixels) / width)
        image = Image.new("L", (width, height), 0)
        image.putdata(pixels + [0] * (width * height - len(pixels)))
        tiles.append(image.resize((width * 2, height * 2), Image.Resampling.NEAREST))
    cell_width = 160
    cell_height = max(tile.height for tile in tiles) + 28
    sheet = Image.new("RGB", (cell_width * 4, cell_height * 4), "white")
    draw = ImageDraw.Draw(sheet)
    for index, tile in enumerate(tiles):
        x = index % 4 * cell_width
        y = index // 4 * cell_height
        draw.text((x + 4, y + 4), f"block {index:02d}: {len(container.blocks[index])} bytes", fill="black")
        sheet.paste(tile.convert("RGB"), (x + 4, y + 22))
    output.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(output)


def main() -> None:
    parser = argparse.ArgumentParser(description="Render DECKCHIP blocks as a raw 4bpp diagnostic")
    parser.add_argument("input", type=Path, nargs="?", default=Path("work/extracted_clean/data/DECKCHIP.DK4"))
    parser.add_argument("output", type=Path, nargs="?", default=Path("work/deckchip_raw_4bpp.png"))
    parser.add_argument("--width", type=int, default=64)
    args = parser.parse_args()
    render(args.input, args.output, args.width)
    print(args.output)


if __name__ == "__main__":
    main()
