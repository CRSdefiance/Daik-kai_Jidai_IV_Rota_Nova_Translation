from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image, ImageDraw


def main() -> None:
    parser = argparse.ArgumentParser(description="Build labeled contact sheets for dialogue QA.")
    parser.add_argument("preview_dir", type=Path)
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--columns", type=int, default=2)
    parser.add_argument("--rows", type=int, default=5)
    args = parser.parse_args()

    files = sorted(args.preview_dir.glob("*.png"))
    if not files:
        raise SystemExit(f"no PNG previews found in {args.preview_dir}")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    with Image.open(files[0]) as first:
        width, height = first.size
    label_height = 22
    page_size = args.columns * args.rows
    for page_index in range(0, len(files), page_size):
        subset = files[page_index : page_index + page_size]
        sheet = Image.new(
            "RGB",
            (args.columns * width, args.rows * (height + label_height)),
            "white",
        )
        draw = ImageDraw.Draw(sheet)
        for index, path in enumerate(subset):
            column = index % args.columns
            row = index // args.columns
            x = column * width
            y = row * (height + label_height)
            draw.text((x + 4, y + 2), path.stem, fill="black")
            with Image.open(path) as preview:
                sheet.paste(preview.convert("RGB"), (x, y + label_height))
        output = args.output_dir / f"sheet_{page_index // page_size + 1}.png"
        sheet.save(output)
        print(output)


if __name__ == "__main__":
    main()
