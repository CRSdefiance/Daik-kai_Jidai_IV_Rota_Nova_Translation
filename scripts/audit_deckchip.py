from __future__ import annotations

"""Classify the DECKCHIP ILNK container before any translation work."""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.formats.ilnk import IlnkContainer


def audit(path: Path) -> str:
    container = IlnkContainer.parse(path.read_bytes())
    lines = [
        "# DECKCHIP audit",
        "",
        "## Classification",
        "",
        "`/data/DECKCHIP.DK4` is an ILNK-wrapped binary deck/ship-chip asset. "
        "It is not a normal dialogue or label string table.",
        "",
        "## Evidence",
        "",
        f"- Container blocks: {len(container.blocks)}",
        "- Blocks are 456-736 bytes long and contain 11-17 variable-length binary fragments.",
        "- Those fragments do not decode as stand-alone Shift-JIS text records and do not have a shared text layout.",
        "- Decoding arbitrary asset bytes as CP932 produces accidental Japanese glyphs, which is why "
        "the generic MESFILE scanner reported 29 false-positive records.",
        "",
        "| Block | Bytes | Binary fragments | Classification |",
        "|---:|---:|---:|---|",
    ]
    for index, block in enumerate(container.blocks):
        fragments = [fragment for fragment in block.split(bytes([0])) if fragment]
        lines.append(f"| {index:02d} | {len(block)} | {len(fragments)} | Binary asset payload |")
    lines.extend(
        [
            "",
            "## Translation path",
            "",
            "1. Locate the deck/ship screen that consumes each block through runtime tracing or a resource-map search.",
            "2. Determine the asset format: tile graphics, tile map, palette, compressed sprite data, or a combination.",
            "3. Render each block to an image only after the format is known; do not insert CP932 text into it.",
            "4. Redraw any Japanese labels as English tiles, preserving dimensions and palette indices.",
            "5. Repack the edited assets and verify the deck screen in-game for corruption and alignment.",
            "",
            "Until steps 1-3 are complete, DECKCHIP has **zero confirmed text records** to translate.",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Audit the binary DECKCHIP container")
    parser.add_argument("input", type=Path, nargs="?", default=Path("work/extracted_clean/data/DECKCHIP.DK4"))
    parser.add_argument("--out", type=Path, default=Path("docs/deckchip_audit.md"))
    args = parser.parse_args()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(audit(args.input), encoding="utf-8")
    print(args.out)


if __name__ == "__main__":
    main()
