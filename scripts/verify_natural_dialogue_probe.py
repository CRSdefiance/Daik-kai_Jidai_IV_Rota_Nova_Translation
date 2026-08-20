from __future__ import annotations

import argparse
import json
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import materialize_translation_batch

BATCHES = (
    Path("translations/raphael_natural_dialogue_probe.json"),
    Path("translations/raphael_pre_tutorial_natural.json"),
    Path("translations/raphael_tutorial_choice_v2.json"),
)
FILE_PATH = "/data/SC0.DK4"
TARGET_BLOCK = 44


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify the fixed-size Raphael natural-dialogue probe."
    )
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    args = parser.parse_args()

    baseline = NdsImage.open(args.baseline)
    candidate = NdsImage.open(args.candidate)
    source = baseline.read_file(FILE_PATH)
    actual = candidate.read_file(FILE_PATH)
    rows = []
    for batch_path in BATCHES:
        batch = json.loads(batch_path.read_text(encoding="utf-8"))
        rows.extend(materialize_translation_batch(batch, source))
    expected = rebuild_mesfile(source, rows)
    target_records = sorted(
        int(str(row["pointer_group"]).split(":")[2]) for row in rows
    )

    if actual != expected:
        raise SystemExit("candidate SC0 does not exactly match the declared probe rebuild")
    if len(actual) != len(source):
        raise SystemExit("SC0 size changed")

    before = IlnkContainer.parse(source)
    after = IlnkContainer.parse(actual)
    if [len(block) for block in before.blocks] != [len(block) for block in after.blocks]:
        raise SystemExit("an ILNK block size changed")
    changed = [
        index
        for index, pair in enumerate(zip(before.blocks, after.blocks, strict=True))
        if pair[0] != pair[1]
    ]
    if changed != [TARGET_BLOCK]:
        raise SystemExit(f"unexpected changed ILNK blocks: {changed}")

    before_segments = before.blocks[TARGET_BLOCK].split(b"\0")
    after_segments = after.blocks[TARGET_BLOCK].split(b"\0")
    changed_segments = [
        index
        for index, pair in enumerate(zip(before_segments, after_segments, strict=True))
        if pair[0] != pair[1]
    ]
    if changed_segments != target_records:
        raise SystemExit(f"unexpected changed records: {changed_segments}")

    print(
        "natural-dialogue probe verified: SC0 and every ILNK block retain their "
        "original size; only the declared Raphael opening/tutorial records changed"
    )


if __name__ == "__main__":
    main()
