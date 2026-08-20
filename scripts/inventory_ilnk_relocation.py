from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Create an incomplete ILNK block-layout inventory for Phase 4 mapping."
    )
    parser.add_argument("source", type=Path)
    parser.add_argument("--file-path", required=True)
    parser.add_argument("--block", type=int, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()

    source = (
        NdsImage.open(args.source).read_file(args.file_path)
        if args.source.suffix.lower() == ".nds"
        else args.source.read_bytes()
    )
    container = IlnkContainer.parse(source)
    try:
        block = container.blocks[args.block]
    except IndexError:
        raise SystemExit(f"block {args.block} is outside the ILNK container") from None

    records = []
    cursor = 0
    segments = block.split(b"\0")
    for index, segment in enumerate(segments):
        records.append(
            {
                "segment_index": index,
                "offset_in_block": cursor,
                "length": len(segment),
                "source_hex": segment.hex().upper(),
            }
        )
        cursor += len(segment) + (1 if index < len(segments) - 1 else 0)

    report = {
        "format": "dk4-ilnk-relocation-inventory-v1",
        "file_path": args.file_path,
        "source_file_sha256": hashlib.sha256(source).hexdigest(),
        "block_index": args.block,
        "block_size": len(block),
        "external_references_complete": False,
        "entry_points": [],
        "records": records,
        "warning": (
            "Record boundaries alone do not authorize expansion. Map every external "
            "and interior entry point before marking this inventory complete."
        ),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"wrote incomplete relocation inventory to {args.out}")


if __name__ == "__main__":
    main()
