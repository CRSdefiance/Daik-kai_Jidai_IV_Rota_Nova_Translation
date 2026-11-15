from __future__ import annotations

import argparse
import json
from pathlib import Path

from dk4tool.dialogue.encoder import encode_fixed_dialogue
from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import iter_mesfile_records
from dk4tool.script.translation_batch import materialize_translation_batch

ROUTE = "/data/SC2.DK4"


def main() -> None:
    parser = argparse.ArgumentParser(description="Check exact Lil batch bytes in an integrated ROM.")
    parser.add_argument("--base", type=Path, required=True)
    parser.add_argument("--candidate", type=Path, required=True)
    parser.add_argument("--batch", type=Path, required=True)
    parser.add_argument("--check-excluded", action="store_true")
    args = parser.parse_args()

    batch = json.loads(args.batch.read_text(encoding="utf-8"))
    if batch["file_path"] != ROUTE or batch["encoder"] != "dialogue-fixed-v1":
        raise ValueError("expected a fixed Lil SC2 dialogue batch")
    source = NdsImage.open(args.base).read_file(ROUTE)
    candidate = NdsImage.open(args.candidate).read_file(ROUTE)
    rows = materialize_translation_batch(batch, source)
    actual = {
        row.row_id: row.raw_bytes
        for row in iter_mesfile_records(candidate, include_non_japanese=True)
    }
    profile = get_dialogue_profile(batch["dialogue_profile"])
    for row in rows:
        expected = encode_fixed_dialogue(bytes.fromhex(row["source_hex"]), row["english"], profile)
        if actual.get(row["id"]) != expected.encoded:
            raise ValueError(f"candidate record differs from encoded batch: {row['id']}")
    if args.check_excluded:
        originals = {
            row.row_id: row.raw_bytes
            for row in iter_mesfile_records(source, include_non_japanese=True)
        }
        for row_id in batch.get("excluded_records", {}):
            if actual.get(row_id) != originals.get(row_id):
                raise ValueError(f"excluded record changed in candidate: {row_id}")
    print(f"verified {len(rows)} exact {ROUTE} records in {args.candidate}")
    if args.check_excluded:
        print(f"verified {len(batch.get('excluded_records', {}))} unchanged exclusions")


if __name__ == "__main__":
    main()
