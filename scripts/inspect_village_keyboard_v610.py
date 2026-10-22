"""Read-only keyboard focus/input inspection for ordinary controller navigation."""

import argparse
import json
import struct
from pathlib import Path

from PIL import Image


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("frame", type=int)
    args = parser.parse_args()
    folder = Path("E:/Rota Nova translations/Generated/work/emulation_v193/village_ui_v610_inuvik")
    image = Image.open(folder / f"frame_{args.frame:06d}_navigation.png").convert("RGB")
    raw = (folder / f"frame_{args.frame:06d}_arm9_ram.bin").read_bytes()
    marker = json.loads(Path("work/analysis/village_promised_words_plan.json").read_text(encoding="utf-8"))["keyboard_wrapper"]["provider_vtable"]
    needle = struct.pack("<I", marker)
    owners = [n - 4 for n in range(0x170000, len(raw) - 4, 4) if raw[n:n + 4] == needle]
    assert len(owners) == 1
    parent = owners[0]
    assert struct.unpack_from("<I", raw, parent + 0xD8)[0] == 18
    text = raw[parent + 0xB4:parent + 0xB4 + 19].split(b"\0", 1)[0].decode("ascii")
    title_present = any(min(image.getpixel((x, y))) > 100
                        for y in range(228, 237) for x in range(45, 55))
    print(json.dumps({"frame": args.frame, "parent": parent + 0x02000000,
                      "entry": text, "cursor": struct.unpack_from("<I", raw, parent + 0x78)[0],
                      "Latin_popup_visible": not title_present, "read_only": True}))


if __name__ == "__main__":
    main()
