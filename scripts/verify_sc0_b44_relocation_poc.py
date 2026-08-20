from __future__ import annotations

import argparse
import hashlib
import json
import struct
from pathlib import Path

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.relocation import (
    load_relocation_map,
    rebuild_mapped_cs_dialogue,
)
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import read_translation_batch

FILE_PATH = "/data/SC0.DK4"
TARGET_BLOCK = 44
PROTECTED_START = 0x02171E48 - 0x02000000
PROTECTED_END = 0x02172464 - 0x02000000
DEFAULT_BATCH_PATH = Path("translations/raphael_b44_long_dialogue_parity_poc.json")
DEFAULT_MAP_PATH = Path("translations/sc0_b44_parity_relocation_probe_map.json")
EXPECTED_BASE_SHA256 = (
    "8e61fd4e8c444b25566cc273dd676b3e5bea5d683ad167db2f92444c10df9764"
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rom_files(image: NdsImage) -> dict[str, bytes]:
    files = {path: data for _, path, data in image.iter_files()}
    files.update(dict(image.iter_components()))
    return files


def block_offsets(container: IlnkContainer) -> list[int]:
    cursor = 8 + (len(container.blocks) + 1) * 4
    offsets = [cursor]
    for block in container.blocks:
        cursor += len(block)
        offsets.append(cursor)
    return offsets


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Verify the guarded SC0 block-44 dialogue relocation proof."
    )
    parser.add_argument("baseline", type=Path)
    parser.add_argument("candidate", type=Path)
    parser.add_argument("--batch", type=Path, default=DEFAULT_BATCH_PATH)
    parser.add_argument("--map", type=Path, default=DEFAULT_MAP_PATH)
    parser.add_argument("--fixed-batch", type=Path, action="append", default=[])
    args = parser.parse_args()

    baseline_bytes = args.baseline.read_bytes()
    if sha256(baseline_bytes) != EXPECTED_BASE_SHA256:
        raise SystemExit("baseline is not the canonical all-goods ROM")
    baseline = NdsImage.open(args.baseline)
    candidate = NdsImage.open(args.candidate)
    before_files = rom_files(baseline)
    after_files = rom_files(candidate)
    changed_paths = sorted(
        path
        for path in before_files.keys() | after_files.keys()
        if before_files.get(path) != after_files.get(path)
    )
    if changed_paths != ["/__arm9__.bin", FILE_PATH]:
        raise SystemExit(f"unexpected changed ROM paths: {changed_paths}")

    source = before_files[FILE_PATH]
    batch_header = json.loads(args.batch.read_text(encoding="utf-8"))
    rows = read_translation_batch(args.batch, source)
    relocation_map = load_relocation_map(args.map)
    expected = rebuild_mapped_cs_dialogue(
        source,
        rows,
        get_dialogue_profile(str(batch_header["dialogue_profile"])),
        relocation_map,
    )
    relocated_segments = {
        tuple(int(value) for value in str(row["pointer_group"]).split(":")[1:])
        for row in rows
    }
    fixed_rows = []
    for fixed_path in args.fixed_batch:
        fixed_rows.extend(
            row
            for row in read_translation_batch(fixed_path, source)
            if tuple(
                int(value) for value in str(row["pointer_group"]).split(":")[1:]
            )
            not in relocated_segments
        )
    expected_file = (
        rebuild_mesfile(expected.rebuilt_file, fixed_rows)
        if fixed_rows
        else expected.rebuilt_file
    )
    if after_files[FILE_PATH] != expected_file:
        raise SystemExit("candidate SC0 is not the exact declared relocation rebuild")

    before = IlnkContainer.parse(source)
    after = IlnkContainer.parse(after_files[FILE_PATH])
    changed_blocks = [
        index
        for index, pair in enumerate(zip(before.blocks, after.blocks, strict=True))
        if pair[0] != pair[1]
    ]
    if TARGET_BLOCK not in changed_blocks:
        raise SystemExit("target ILNK block did not change")
    delta = len(after.blocks[TARGET_BLOCK]) - len(before.blocks[TARGET_BLOCK])
    if delta != expected.size_delta:
        raise SystemExit("block size delta disagrees with guarded rebuild")
    before_offsets = block_offsets(before)
    after_offsets = block_offsets(after)
    if before_offsets[: TARGET_BLOCK + 1] != after_offsets[: TARGET_BLOCK + 1]:
        raise SystemExit("an ILNK offset before block 44 moved")
    if any(
        new - old != delta
        for old, new in zip(
            before_offsets[TARGET_BLOCK + 1 :],
            after_offsets[TARGET_BLOCK + 1 :],
            strict=True,
        )
    ):
        raise SystemExit("a post-block-44 ILNK offset did not move by the exact delta")

    rebuilt_block = after.blocks[TARGET_BLOCK]
    body_size = struct.unpack_from("<H", rebuilt_block, 4)[0]
    logical_end = 8 + body_size
    if any(rebuilt_block[logical_end:]) or len(rebuilt_block) % 4:
        raise SystemExit("rebuilt CS length or alignment padding is invalid")
    if expected.changed_segments != (13, 17, 21, 25, 29):
        raise SystemExit("unexpected changed CS dialogue segments")

    before_arm9 = before_files["/__arm9__.bin"]
    after_arm9 = after_files["/__arm9__.bin"]
    if before_arm9[PROTECTED_START:PROTECTED_END] != after_arm9[
        PROTECTED_START:PROTECTED_END
    ]:
        raise SystemExit("protected ARM9 runtime-owned data changed")

    print(
        json.dumps(
            {
                "candidate_sha256": sha256(args.candidate.read_bytes()),
                "changed_paths": changed_paths,
                "changed_block": TARGET_BLOCK,
                "changed_block_count": len(changed_blocks),
                "hybrid_fixed_record_count": len(fixed_rows),
                "changed_segments": list(expected.changed_segments),
                "parity_padded_segments": list(expected.parity_padded_segments),
                "block_size_delta": delta,
                "protected_arm9_range_unchanged": True,
                "post_block_offsets_shifted_by_exact_delta": True,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
