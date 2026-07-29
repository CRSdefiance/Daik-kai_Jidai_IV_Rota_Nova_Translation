from __future__ import annotations

# The repository root is intentionally added before importing the local package.
# ruff: noqa: I001

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.input_calendar import patch_nds_bytes
from dk4tool.rom.nds import NdsImage


EXPECTED_RECORDS = {
    (0, 64): " Range: about %s days.",
    (0, 65): " %s/%s\n %s\n Departed %s.",
    (14, 36): "  %s! You aid this city's defense\n without a contract?\n How generous\n of you.",
    (14, 43): " Hmm. Admirable resolve.\n Well done.",
    (14, 59): " One coin per night.\n How many nights?",
    (14, 60): "  Stay %s nights?\n Rest.",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the dedicated input/calendar build.")
    parser.add_argument("rom", type=Path)
    arguments = parser.parse_args()

    rom_bytes = arguments.rom.read_bytes()
    idempotent, changes = patch_nds_bytes(rom_bytes)
    if idempotent != rom_bytes:
        raise SystemExit("ARM9 input/calendar patch is not fully applied")

    image = NdsImage.open(arguments.rom)
    mesfile = IlnkContainer.parse(image.read_file("/COMMON/MESFILE.DK4"))
    for (block_index, record_index), expected in EXPECTED_RECORDS.items():
        records = mesfile.blocks[block_index].split(b"\0")
        actual = records[record_index].rstrip(b" ").decode("cp932")
        if actual != expected:
            raise SystemExit(
                f"record {block_index}:{record_index} is {actual!r}; expected {expected!r}"
            )

    # Record 38 has a second live entry point at byte 56.  The palace can jump
    # directly here, so the translated first sentence must not move it.
    palace_record = mesfile.blocks[14].split(b"\0")[38]
    second_entry = palace_record[56:].rstrip(b" ").decode("cp932")
    expected_second_entry = "%s! You will aid\n the city's defense?"
    if second_entry != expected_second_entry:
        raise SystemExit(
            f"record 14:38 secondary entry is {second_entry!r}; "
            f"expected {expected_second_entry!r}"
        )

    print(
        f"Verified {len(changes)} ARM9 changes and "
        f"{len(EXPECTED_RECORDS)} shared date/inn records."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
