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
        Label((7, 19, 67, 36), "Type"),
        Label((135, 19, 199, 36), "Growth"),
        Label((7, 39, 67, 56), "Status"),
        Label((135, 39, 199, 56), "Arms"),
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
        Label((16, 16, 82, 35), "Fleet Sailors", 10),
        Label((135, 16, 211, 35), "Unassigned", 10),
        Label((7, 39, 83, 58), "Range (Days)", 10),
        Label((7, 103, 65, 123), "Quarters", 10),
        Label((87, 103, 121, 123), "Cannon", 9),
        Label((7, 123, 65, 143), "Sail", 11),
        Label((135, 123, 193, 143), "Square Sail", 9),
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
        Label((7, 39, 33, 58), "Water", 9),
        Label((71, 39, 99, 58), "Food", 10),
        Label((135, 39, 163, 58), "Sailors", 8),
        Label((7, 59, 65, 79), "Cargo", 11),
        Label((135, 59, 179, 79), "Load", 11),
        Label((7, 79, 65, 99), "Sail", 11),
        Label((135, 79, 193, 99), "Square", 10),
        Label((7, 99, 65, 119), "Quarters", 10),
        Label((135, 99, 193, 119), "Cannons", 10),
        Label((7, 119, 65, 139), "Gun Type", 10),
        Label((7, 139, 65, 159), "Durability", 9),
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
