from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from dk4tool.patch.input_calendar import patch_nds_bytes


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Apply the shared English naming-input and calendar patch."
    )
    parser.add_argument("rom", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    arguments = parser.parse_args()

    patched, changes = patch_nds_bytes(arguments.rom.read_bytes())
    arguments.out.parent.mkdir(parents=True, exist_ok=True)
    arguments.out.write_bytes(patched)
    print(f"Wrote {arguments.out} with {len(changes)} verified ARM9 changes.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
