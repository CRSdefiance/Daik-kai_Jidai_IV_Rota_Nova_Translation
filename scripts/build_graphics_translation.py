from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from dk4tool.graphics.fls import FlsArchive
from dk4tool.graphics.pxl import Box, PxlImage
from dk4tool.rom.nds import NdsImage


@dataclass(frozen=True)
class Label:
    box: Box
    text: str
    maximum_size: int = 13


TRANSPARENT_LABELS = {
    "/_pxl/charselect.pxl": [
        Label((0, 235, 48, 248), "Name"),
        Label((0, 251, 48, 264), "Middle", 11),
        Label((0, 267, 48, 280), "Last"),
        Label((0, 283, 48, 296), "Company", 10),
        Label((0, 299, 48, 312), "Born"),
    ],
}

PLAQUE_LABELS = {
    "/_pxl/towninfo.pxl": [
        # These four plaques share their rows with live values.  Keep the
        # captions deliberately compact so they cannot spill into City,
        # Normal, 6000, and 4200 at runtime.
        Label((7, 19, 51, 36), "Type", 8),
        Label((135, 19, 175, 36), "Growth", 7),
        Label((7, 39, 51, 56), "Status", 8),
        Label((135, 39, 175, 56), "Arms", 8),
        Label((39, 59, 89, 77), "Share"),
        Label((163, 59, 235, 77), "Specialty", 11),
    ],
    "/_pxl/chihofleetinfo.pxl": [
        Label((83, 72, 125, 90), "Level", 11),
        Label((3, 103, 49, 118), "Income", 11),
        Label((3, 123, 49, 138), "Expense", 10),
        Label((3, 143, 49, 158), "Invested", 9),
        Label((3, 163, 49, 178), "Mission", 10),
    ],
    "/_pxl/fleetinfo.pxl": [
        Label((83, 72, 125, 90), "Level", 11),
    ],
    "/_pxl/forceinfo.pxl": [
        Label((83, 72, 125, 90), "Level", 11),
        Label((3, 103, 49, 118), "Funds", 11),
        Label((3, 123, 49, 138), "Power", 11),
        Label((3, 143, 49, 158), "Home", 11),
        Label((3, 163, 49, 178), "Relations", 9),
    ],
    "/_pxl/dividecrewinfo.pxl": [
        Label((12, 14, 86, 36), "Fleet Crew", 10),
        Label((131, 14, 215, 36), "Unassigned", 9),
        Label((5, 37, 86, 60), "Range Days", 9),
        Label((5, 100, 68, 124), "Marines", 9),
        Label((84, 100, 124, 124), "Guns", 9),
        Label((5, 120, 68, 145), "Sail", 10),
        Label((132, 120, 196, 145), "Square", 9),
    ],
    "/_pxl/personinfo.pxl": [
        Label((3, 103, 49, 118), "Body", 11),
        Label((3, 123, 49, 138), "Mind", 11),
        Label((3, 143, 49, 158), "Level", 11),
        Label((3, 163, 49, 178), "HP", 11),
    ],
    "/_pxl/saveloadinfo.pxl": [
        Label((96, 39, 137, 57), "Level", 11),
        Label((96, 63, 137, 81), "Power", 11),
    ],
    "/_pxl/shipinfo.pxl": [
        Label((5, 37, 36, 60), "Water", 8),
        Label((69, 37, 102, 60), "Food", 9),
        Label((132, 37, 166, 60), "Crew", 9),
        Label((5, 57, 68, 81), "Cargo", 10),
        Label((132, 57, 182, 81), "Load", 10),
        Label((5, 77, 68, 101), "Sail", 10),
        Label((132, 77, 196, 101), "Square", 9),
        Label((5, 97, 68, 121), "Marines", 9),
        Label((132, 97, 196, 121), "Guns", 10),
        Label((5, 117, 68, 141), "Gun", 10),
        Label((5, 137, 68, 161), "Hull", 10),
    ],
    "/_pxl/goldsearoutediscovery.pxl": [
        Label((7, 16, 49, 35), "Goods", 11),
        Label((7, 48, 49, 67), "Profit", 11),
        Label((7, 80, 49, 99), "Reward", 10),
    ],
    "/_pxl/goldsearoutelog.pxl": [
        Label((63, 0, 113, 18), "Goods", 11),
        Label((167, 0, 209, 18), "Profit", 10),
        Label((215, 0, 249, 18), "Reward", 9),
    ],
    "/_pxl/goldsearoutelog2.pxl": [
        Label((63, 0, 113, 18), "Goods", 11),
        Label((175, 0, 241, 18), "Reward Total", 8),
    ],
}

FLS_LABELS = {
    "/FLS/logo.fls": {
        3: ["REKOEITION GAME"],
    },
    "/FLS/M22.fls": {
        1: ["Hey, don't!", "It's too dangerous!"],
        2: ["It's fine, it's fine.", "Leave it to me!"],
    },
    "/FLS/M24.fls": {
        3: ["The ship's here!", "Report to the captain!"],
        4: ["A foreign merchant ship!", "Admiral, your orders?"],
    },
}


def translate_pxl(data: bytes, path: str) -> tuple[bytes, PxlImage]:
    image = PxlImage.from_bytes(data)
    for label in TRANSPARENT_LABELS.get(path, []):
        image.clear(label.box)
        image.draw_text(
            label.box,
            label.text,
            255,
            outline_index=1,
            maximum_size=label.maximum_size,
        )
    for label in PLAQUE_LABELS.get(path, []):
        image.erase_dark_text(label.box)
        image.draw_text(
            label.box,
            label.text,
            1,
            maximum_size=label.maximum_size,
        )
    return image.to_bytes(), image


def main() -> None:
    parser = argparse.ArgumentParser(description="Apply the DK4 English graphics pass.")
    parser.add_argument("rom", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--preview-dir", type=Path)
    args = parser.parse_args()

    image = NdsImage.open(args.rom)
    paths = sorted(set(TRANSPARENT_LABELS) | set(PLAQUE_LABELS))
    for path in paths:
        rebuilt, preview = translate_pxl(image.read_file(path), path)
        image.replace_file(path, rebuilt)
        if args.preview_dir:
            destination = args.preview_dir / f"{Path(path).stem}.png"
            destination.parent.mkdir(parents=True, exist_ok=True)
            preview.render().save(destination)
        print(f"translated {path}")
    for path, assets in FLS_LABELS.items():
        archive = FlsArchive(image.read_file(path))
        for index, lines in assets.items():
            archive.texture(index).replace_with_lines(lines)
            if args.preview_dir:
                destination = args.preview_dir / f"{Path(path).stem}_{index:03d}.png"
                archive.texture(index).render().save(destination)
        image.replace_file(path, archive.to_bytes())
        print(f"translated {path}: {', '.join(map(str, assets))}")
    image.save(args.out)


if __name__ == "__main__":
    main()
