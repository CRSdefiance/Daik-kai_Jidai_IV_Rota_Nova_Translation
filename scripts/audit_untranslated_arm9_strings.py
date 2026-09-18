from __future__ import annotations

import argparse
import json
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from dk4tool.script.arm9_profiles import PROFILES


def has_japanese(text: str) -> bool:
    return any(
        "\u3040" <= char <= "\u30ff" or "\u3400" <= char <= "\u9fff"
        for char in text
    )


def printable(text: str) -> bool:
    return bool(text) and all(char.isprintable() for char in text)


def known_ranges() -> list[tuple[int, int, str]]:
    return [
        (entry.offset, entry.offset + entry.source_length, entry.row_id)
        for entry in PROFILES["all"]
    ]


def scan(data: bytes, start: int = 0x110000) -> list[dict[str, object]]:
    known = known_ranges()
    rows: list[dict[str, object]] = []
    seen: set[tuple[int, int]] = set()
    for offset in range(start, len(data) - 2):
        # Runtime C-string pools are NUL-delimited. Requiring the preceding
        # terminator avoids reporting every four-byte suffix inside one string
        # and most accidental Shift-JIS decodes in executable code.
        if offset > start and data[offset - 1] != 0:
            continue
        end = data.find(b"\0", offset, min(len(data), offset + 65))
        if end < 0 or end - offset < 4:
            continue
        raw = data[offset:end]
        try:
            text = raw.decode("cp932")
        except UnicodeDecodeError:
            continue
        japanese_count = sum(
            "\u3040" <= char <= "\u30ff" or "\u3400" <= char <= "\u9fff"
            for char in text
        )
        if not printable(text) or not has_japanese(text) or japanese_count < 2:
            continue
        key = (offset, end)
        if key in seen:
            continue
        seen.add(key)
        owners = [row_id for lo, hi, row_id in known if lo <= offset < hi]
        rows.append(
            {
                "offset": offset,
                "length": len(raw),
                "text": text,
                "profile_owners": owners,
                "unprofiled": not owners,
            }
        )
    return rows


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Find printable Japanese C strings remaining in ARM9."
    )
    parser.add_argument("rom", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    arm9 = NdsImage.open(args.rom).read_file("/__arm9__.bin")
    rows = scan(arm9)
    report = {
        "format": "dk4-untranslated-arm9-audit-v1",
        "rom": str(args.rom),
        "remaining_count": len(rows),
        "unprofiled_count": sum(bool(row["unprofiled"]) for row in rows),
        "records": rows,
    }
    rendered = json.dumps(report, ensure_ascii=True, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(rendered, encoding="utf-8")
    print(rendered)


if __name__ == "__main__":
    main()
