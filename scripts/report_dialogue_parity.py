from __future__ import annotations

import argparse
import json
from pathlib import Path

from dk4tool.dialogue.encoder import encode_relocatable_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.rom.nds import NdsImage
from dk4tool.script.translation_batch import read_translation_batch


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Report source and encoded byte parity for a dialogue batch."
    )
    parser.add_argument("rom", type=Path)
    parser.add_argument("batch", type=Path)
    args = parser.parse_args()

    header = json.loads(args.batch.read_text(encoding="utf-8"))
    source_file = NdsImage.open(args.rom).read_file(str(header["file_path"]))
    profile = get_dialogue_profile(str(header["dialogue_profile"]))
    for row in read_translation_batch(args.batch, source_file):
        source = bytes.fromhex(str(row["source_hex"]))
        target = encode_relocatable_dialogue(
            source, str(row["english"]), profile
        ).encoded
        print(
            f"{row['id']}: source={len(source)} ({len(source) % 2}) "
            f"target={len(target)} ({len(target) % 2}) delta={len(target) - len(source):+d}"
        )


if __name__ == "__main__":
    main()
