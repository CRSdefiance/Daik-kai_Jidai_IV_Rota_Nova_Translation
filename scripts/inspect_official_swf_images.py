"""Extract static image tags from saved official SWFs; never execute ActionScript."""

import io
import json
import struct
import zlib
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from scripts.fleet_row_graphics_v162 import save

ROOT = Path("work/research/online_official_sources")
OUT = ROOT / "swf_images"


def tags(raw):
    if raw[:3] == b"CWS":
        raw = raw[:8] + zlib.decompress(raw[8:])
    elif raw[:3] != b"FWS":
        raise ValueError("Unsupported SWF compression")
    if len(raw) != struct.unpack_from("<I", raw, 4)[0]:
        raise ValueError("SWF declared extent differs")
    rect_bits = raw[8] >> 3
    offset = 8 + (5 + rect_bits * 4 + 7) // 8 + 4
    while offset < len(raw):
        start = offset
        code = struct.unpack_from("<H", raw, offset)[0]
        kind, length = code >> 6, code & 63
        offset += 2
        if length == 63:
            length = struct.unpack_from("<I", raw, offset)[0]
            offset += 4
        if offset + length > len(raw):
            raise ValueError("SWF tag crosses declared allocation")
        yield kind, start, raw[offset : offset + length]
        offset += length
        if kind == 0:
            break


def bitmap(kind, data):
    if kind in (21, 35):
        offset = 2 if kind == 21 else 6
        length = len(data) - offset if kind == 21 else struct.unpack_from("<I", data, 2)[0]
        encoded = data[offset : offset + length].replace(b"\xff\xd9\xff\xd8", b"")
        return Image.open(io.BytesIO(encoded)).convert("RGBA")
    if kind not in (20, 36):
        return None
    fmt, width, height = struct.unpack_from("<BHH", data, 2)
    alpha = kind == 36
    if fmt == 3:
        count = data[7] + 1
        raw = zlib.decompress(data[8:])
        channels = 4 if alpha else 3
        palette = [tuple(raw[i * channels : (i + 1) * channels]) for i in range(count)]
        if not alpha:
            palette = [c + (255,) for c in palette]
        stride = (width + 3) // 4 * 4
        pixels = raw[count * channels :]
        if len(pixels) != stride * height:
            raise ValueError("SWF indexed bitmap allocation differs")
        image = Image.new("RGBA", (width, height))
        image.putdata(
            [palette[pixels[y * stride + x]] for y in range(height) for x in range(width)]
        )
        return image
    if fmt == 5:
        raw = zlib.decompress(data[7:])
        if len(raw) != width * height * 4:
            raise ValueError("SWF RGB bitmap allocation differs")
        # Lossless2 uses ARGB; lossless1 uses reserved/RGB.
        pixels = [
            (raw[i + 1], raw[i + 2], raw[i + 3], raw[i] if alpha else 255)
            for i in range(0, len(raw), 4)
        ]
        image = Image.new("RGBA", (width, height))
        image.putdata(pixels)
        return image
    raise ValueError("Unsupported SWF bitmap type")


def main():
    OUT.mkdir(exist_ok=True)
    rows, errors = [], []
    for file in [ROOT / "main.swf", *sorted((ROOT / "d4_sections").glob("*.swf"))]:
        raw = file.read_bytes()
        for kind, offset, data in tags(raw):
            if kind not in (20, 21, 35, 36):
                continue
            try:
                image = bitmap(kind, data)
                ident = struct.unpack_from("<H", data)[0]
                output = OUT / f"{file.stem}_{ident}_{kind}.png"
                image.save(output)
                rows.append(
                    {
                        "source": str(file),
                        "source_sha256": sha(raw),
                        "tag_offset": offset,
                        "tag_kind": kind,
                        "character_id": ident,
                        "dimensions": list(image.size),
                        "preview": str(output),
                        "preview_sha256": sha(output.read_bytes()),
                    }
                )
            except (ValueError, OSError, IndexError, struct.error) as error:
                errors.append({"source": str(file), "tag_offset": offset, "error": str(error)})
    selected = [r for r in rows if r["dimensions"][0] >= 120 and r["dimensions"][1] >= 70]
    for start in range(0, len(selected), 12):
        sheet = Image.new("RGB", (1000, 630), "#343434")
        draw = ImageDraw.Draw(sheet)
        for i, row in enumerate(selected[start : start + 12]):
            image = Image.open(row["preview"]).convert("RGB")
            image.thumbnail((245, 175))
            x, y = i % 4 * 250, i // 4 * 210
            draw.text((x + 4, y + 4), Path(row["preview"]).name, fill="white")
            draw.text((x + 4, y + 17), str(row["dimensions"]), fill="white")
            sheet.paste(image, (x + 4, y + 30))
        sheet.save(OUT / f"sheet_{start // 12}.png")
    save(
        OUT / "inventory.json",
        {
            "images": rows,
            "errors": errors,
            "selected_previews": selected,
            "flash_code_executed": False,
        },
    )
    print(json.dumps({"images": len(rows), "selected": len(selected), "errors": errors}))


if __name__ == "__main__":
    main()
