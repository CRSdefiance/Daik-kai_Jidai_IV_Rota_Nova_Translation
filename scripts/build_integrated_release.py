from __future__ import annotations

import argparse
import hashlib
import json
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import read_translation_batch


CANONICAL_BASELINE_SHA256 = (
    "8e61fd4e8c444b25566cc273dd676b3e5bea5d683ad167db2f92444c10df9764"
)
REQUIRED_MENU_TEXT = (b"Continue", b"New Game", b"Opts", b"Grand Race", b"Extras", b"Gallery")
FORBIDDEN_PLACEHOLDERS = (b"see below",)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def rom_files(image: NdsImage) -> dict[str, bytes]:
    result = {path: data for _, path, data in image.iter_files()}
    result.update(dict(image.iter_components()))
    return result


def load_batch_header(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise TypeError(f"{path}: translation batch root must be an object")
    return value


def apply_arm9_fixed_batch(batch_path: Path, source: bytes) -> tuple[bytes, list[str]]:
    """Apply a source-locked, fixed-width ARM9 text batch.

    ARM9 labels are not ILNK records, but they still need the same parent and
    byte-preservation guarantees as dialogue batches. Each entry verifies the
    exact source bytes at its declared offset and can only shrink in place.
    """
    batch = load_batch_header(batch_path)
    if batch.get("format") != "dk4-arm9-fixed-text-batch-v1":
        raise ValueError(f"{batch_path}: unsupported ARM9 batch format")
    expected_hash = str(batch.get("source_file_sha256", "")).lower()
    actual_hash = sha256(source)
    if expected_hash != actual_hash:
        raise ValueError(
            f"{batch_path}: ARM9 source SHA-256 mismatch "
            f"(expected {expected_hash}, got {actual_hash})"
        )
    records = batch.get("records")
    if not isinstance(records, list) or not records:
        raise ValueError(f"{batch_path}: ARM9 batch has no records")

    rebuilt = bytearray(source)
    record_ids: list[str] = []
    claimed: set[int] = set()
    for record in records:
        if not isinstance(record, dict):
            raise TypeError(f"{batch_path}: ARM9 record must be an object")
        row_id = str(record.get("id", ""))
        if not row_id or row_id in record_ids:
            raise ValueError(f"{batch_path}: duplicate or missing ARM9 record id")
        offset = int(record.get("offset", -1))
        expected = bytes.fromhex(str(record.get("source_hex", "")))
        if offset < 0 or not expected or source[offset : offset + len(expected)] != expected:
            raise ValueError(f"{batch_path}: {row_id} source bytes do not match at {offset:#x}")
        if any(position in claimed for position in range(offset, offset + len(expected))):
            raise ValueError(f"{batch_path}: {row_id} overlaps another ARM9 record")
        encoding = str(record.get("encoding", "ascii"))
        replacement = str(record.get("english", "")).encode(encoding)
        if len(replacement) > len(expected):
            raise ValueError(
                f"{batch_path}: {row_id} replacement is {len(replacement)} bytes; "
                f"slot is {len(expected)} bytes"
            )
        rebuilt[offset : offset + len(expected)] = replacement.ljust(len(expected), b"\0")
        claimed.update(range(offset, offset + len(expected)))
        record_ids.append(row_id)
    return bytes(rebuilt), record_ids


def changed_segments(before: bytes, after: bytes) -> set[tuple[int, int]]:
    old = IlnkContainer.parse(before)
    new = IlnkContainer.parse(after)
    if len(old.blocks) != len(new.blocks):
        raise ValueError("ILNK block count changed")
    changed: set[tuple[int, int]] = set()
    for block_index, (old_block, new_block) in enumerate(zip(old.blocks, new.blocks, strict=True)):
        old_segments = old_block.split(b"\0")
        new_segments = new_block.split(b"\0")
        if len(old_segments) != len(new_segments):
            raise ValueError(f"ILNK segment count changed in block {block_index}")
        changed.update(
            (block_index, segment_index)
            for segment_index, (old_segment, new_segment) in enumerate(
                zip(old_segments, new_segments, strict=True)
            )
            if old_segment != new_segment
        )
    return changed


def parse_pointer_group(row: dict[str, object]) -> tuple[int, int]:
    parts = str(row.get("pointer_group", "")).split(":")
    if len(parts) != 3 or parts[0] != "ILNK":
        raise ValueError(f"{row.get('id')}: invalid ILNK pointer group")
    return int(parts[1]), int(parts[2])


def verify_golden_content(baseline: NdsImage, candidate: NdsImage) -> None:
    arm9 = candidate.read_file("/__arm9__.bin")
    missing = [value.decode("ascii") for value in REQUIRED_MENU_TEXT if value not in arm9]
    if missing:
        raise ValueError("required main-menu text missing: " + ", ".join(missing))

    baseline_files = rom_files(baseline)
    candidate_files = rom_files(candidate)
    for placeholder in FORBIDDEN_PLACEHOLDERS:
        old_count = sum(data.count(placeholder) for data in baseline_files.values())
        new_count = sum(data.count(placeholder) for data in candidate_files.values())
        if new_count > old_count:
            raise ValueError(
                f"forbidden placeholder {placeholder!r} increased from {old_count} to {new_count}"
            )


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a translation release only from the immutable accepted baseline."
    )
    parser.add_argument("--base", type=Path, default=Path("out/all_goods_roundtrip.nds"))
    parser.add_argument("--batch", action="append", type=Path, default=[])
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--manifest", type=Path)
    args = parser.parse_args()

    base_data = args.base.read_bytes()
    base_hash = sha256(base_data)
    if base_hash != CANONICAL_BASELINE_SHA256:
        raise SystemExit(
            "refusing noncanonical base ROM: "
            f"expected {CANONICAL_BASELINE_SHA256}, got {base_hash}"
        )
    if args.out.resolve() == args.base.resolve():
        raise SystemExit("refusing to overwrite the canonical baseline")

    baseline = NdsImage.open(args.base)
    candidate = NdsImage.open(args.base)
    grouped: dict[str, list[Path]] = defaultdict(list)
    for batch_path in args.batch:
        header = load_batch_header(batch_path)
        file_path = str(header.get("file_path", ""))
        if not file_path.startswith("/"):
            raise SystemExit(f"{batch_path}: invalid internal file path")
        grouped[file_path].append(batch_path)

    changed_records: dict[str, list[str]] = {}
    for file_path, batch_paths in grouped.items():
        source = candidate.read_file(file_path)
        if file_path == "/__arm9__.bin":
            if len(batch_paths) != 1:
                raise SystemExit("ARM9 release builds accept exactly one fixed-text batch")
            rebuilt, record_ids = apply_arm9_fixed_batch(batch_paths[0], source)
            if rebuilt == source:
                raise SystemExit("ARM9 fixed-text batch made no changes")
            candidate.replace_file(file_path, rebuilt)
            changed_records[file_path] = record_ids
            continue
        rows: list[dict[str, object]] = []
        for batch_path in batch_paths:
            rows.extend(read_translation_batch(batch_path, source))
        if file_path == "/data/SC2.DK4" and any(
            parse_pointer_group(row)[0] == 22 for row in rows
        ):
            raise SystemExit(
                "SC2 block 22 is blocked: its portrait/name control preamble is unmapped. "
                "Use only a disposable live-tested research probe until that format is documented."
            )
        record_ids = [str(row["id"]) for row in rows]
        if len(record_ids) != len(set(record_ids)):
            raise SystemExit(f"{file_path}: duplicate record appears across translation batches")

        expected_segments = {parse_pointer_group(row) for row in rows}
        rebuilt = rebuild_mesfile(source, rows)
        actual_segments = changed_segments(source, rebuilt)
        unexpected = actual_segments - expected_segments
        if unexpected:
            raise SystemExit(
                f"{file_path}: unrequested ILNK segments changed: {sorted(unexpected)}"
            )
        unchanged_requested = expected_segments - actual_segments
        if unchanged_requested:
            raise SystemExit(
                f"{file_path}: requested records did not change: {sorted(unchanged_requested)}"
            )
        candidate.replace_file(file_path, rebuilt)
        changed_records[file_path] = record_ids

    verify_golden_content(baseline, candidate)
    before_files = rom_files(baseline)
    after_files = rom_files(candidate)
    changed_paths = sorted(
        path
        for path in before_files.keys() | after_files.keys()
        if before_files.get(path) != after_files.get(path)
    )
    undeclared = sorted(set(changed_paths) - set(grouped))
    if undeclared:
        raise SystemExit("undeclared ROM files changed: " + ", ".join(undeclared))
    missing_changes = sorted(set(grouped) - set(changed_paths))
    if missing_changes:
        raise SystemExit("declared ROM files did not change: " + ", ".join(missing_changes))

    candidate.save(args.out)
    saved = NdsImage.open(args.out)
    saved_files = rom_files(saved)
    if saved_files != after_files:
        raise SystemExit("saved ROM does not round-trip to the verified internal-file set")

    manifest_path = args.manifest or args.out.with_suffix(".manifest.json")
    manifest = {
        "format": "dk4-integrated-release-v1",
        "created_at": datetime.now(UTC).isoformat(),
        "base_rom": str(args.base),
        "base_sha256": base_hash,
        "candidate_rom": str(args.out),
        "candidate_sha256": sha256(args.out.read_bytes()),
        "changed_paths": changed_paths,
        "changed_records": changed_records,
        "batches": [str(path) for path in args.batch],
        "checks": {
            "canonical_base": True,
            "undeclared_files_unchanged": True,
            "untouched_ilnk_segments_unchanged": True,
            "main_menu_anchors_present": True,
            "unmapped_story_control_records_rejected": True,
            "no_new_placeholder_fallbacks": True,
            "saved_rom_roundtrip": True,
        },
    }
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except (KeyError, OSError, TypeError, ValueError) as error:
        raise SystemExit(f"build rejected: {error}") from None
