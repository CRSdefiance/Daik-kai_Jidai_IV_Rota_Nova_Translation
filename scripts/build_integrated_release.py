from __future__ import annotations

import argparse
import hashlib
import json
import struct
from collections import defaultdict
from datetime import UTC, datetime
from pathlib import Path

from dk4tool.dialogue.profiles import get_dialogue_profile
from dk4tool.dialogue.qa import (
    audit_fixed_dialogue_record,
    audit_relocatable_dialogue_record,
)
from dk4tool.dialogue.relocation import (
    load_relocation_map,
    rebuild_mapped_cs_dialogue,
)
from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage
from dk4tool.rom.nds import NdsImage
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import (
    materialize_translation_batch,
    read_translation_batch,
)

CANONICAL_BASELINE_SHA256 = (
    "c94e1fd7221c5e929c851a39f1e722c8b127992bea743dd9992ca1ff027afcdf"
)
REQUIRED_MENU_TEXT = (b"Continue", b"New Game", b"Opts", b"Grand Race", b"Extras", b"Gallery")
FORBIDDEN_PLACEHOLDERS = (b"see below",)
RELEASE_STACK_PATH = Path("translations/release_stack.json")
ARM9_LOAD_ADDRESS = 0x02000000
PROHIBITED_RUNTIME_DATA_START = 0x02171E48
PROHIBITED_RUNTIME_DATA_END = 0x02172464


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
    validate_natural_dialogue_batch(value)
    return value


def validate_playable_dialogue_header(path: Path, header: dict[str, object]) -> None:
    """Reject research-only newline profiles from playable story builds."""

    if header.get("encoder") not in {
        "dialogue-fixed-v1",
        "dialogue-relocatable-v1",
    }:
        return
    file_path = str(header.get("file_path", ""))
    if file_path not in {f"/data/SC{index}.DK4" for index in range(4)}:
        return
    profile_name = str(header.get("dialogue_profile", ""))
    profile = get_dialogue_profile(profile_name)
    if profile_name.endswith("-revoked") or not profile.guard_linebreaks:
        raise ValueError(
            f"{path}: playable progressive-story dialogue requires a live-safe "
            "guarded profile; research profile is forbidden"
        )


def validate_natural_dialogue_qa(
    path: Path, header: dict[str, object], source: bytes
) -> None:
    """Fail a playable build on every unwaived dialogue QA warning or error.

    This deliberately runs inside the release builder. A standalone audit is
    useful to translators, but it cannot protect a ROM when somebody forgets
    to run it before building.
    """

    if header.get("translation_policy") not in {
        "natural-dialogue-v1",
        "natural-dialogue-v2",
    }:
        return
    profile = get_dialogue_profile(str(header.get("dialogue_profile", "")))
    authored = {
        str(record.get("id", "")): record
        for record in header.get("records", [])
        if isinstance(record, dict)
    }
    failures: list[str] = []
    for row in materialize_translation_batch(header, source):
        row_id = str(row["id"])
        record = authored[row_id]
        waivers = (
            {str(value) for value in record.get("qa_waivers", [])}
            if isinstance(record.get("qa_waivers", []), list)
            else set()
        )
        if waivers and not str(
            record.get("qa_waiver_reason", record.get("localization_note", ""))
        ).strip():
            failures.append(f"{row_id}:error:undocumented-qa-waiver")
        audit_function = (
            audit_relocatable_dialogue_record
            if header.get("encoder") == "dialogue-relocatable-v1"
            else audit_fixed_dialogue_record
        )
        audit = audit_function(
            bytes.fromhex(str(row["source_hex"])),
            str(row["english"]),
            profile,
        )
        for issue in audit["issues"]:
            severity = str(issue["severity"])
            code = str(issue["code"])
            if severity == "error" or (severity == "warning" and code not in waivers):
                failures.append(f"{row_id}:{severity}:{code}")
    if failures:
        raise ValueError(
            f"{path}: natural-dialogue QA failed: " + ", ".join(failures)
        )


def load_release_stack(path: Path = RELEASE_STACK_PATH) -> dict[str, object]:
    stack = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(stack, dict) or stack.get("format") != "dk4-release-stack-v1":
        raise ValueError(f"{path}: unsupported release-stack format")
    baseline = stack.get("canonical_baseline")
    if not isinstance(baseline, dict):
        raise TypeError(f"{path}: missing canonical_baseline")
    if str(baseline.get("sha256", "")).lower() != CANONICAL_BASELINE_SHA256:
        raise ValueError(f"{path}: canonical baseline hash disagrees with builder")
    accepted = stack.get("accepted_layers")
    profiles = stack.get("profiles")
    if not isinstance(accepted, list) or not isinstance(profiles, dict):
        raise TypeError(f"{path}: invalid accepted_layers or profiles")
    for layer in accepted:
        if (
            not isinstance(layer, dict)
            or layer.get("status") != "accepted"
            or not isinstance(layer.get("batch"), str)
            or not isinstance(layer.get("baked_into_baseline", False), bool)
        ):
            raise ValueError(f"{path}: invalid accepted layer")
    for name, value in profiles.items():
        if (
            not isinstance(name, str)
            or not isinstance(value, dict)
            or not isinstance(value.get("batches"), list)
            or not all(isinstance(item, str) for item in value["batches"])
        ):
            raise ValueError(f"{path}: invalid profile {name!r}")
    return stack


def accepted_batch_paths(stack: dict[str, object]) -> list[Path]:
    layers = stack["accepted_layers"]
    assert isinstance(layers, list)
    return [
        Path(str(layer["batch"]))
        for layer in layers
        if layer.get("baked_into_baseline") is not True
    ]


def profile_batch_paths(stack: dict[str, object], profile: str) -> list[Path]:
    profiles = stack["profiles"]
    assert isinstance(profiles, dict)
    value = profiles.get(profile)
    if not isinstance(value, dict):
        raise TypeError(f"unknown release profile: {profile}")
    if value.get("status") == "revoked":
        raise ValueError(f"release profile is revoked and cannot be built: {profile}")
    if value.get("status") != "experimental":
        raise ValueError(
            f"release profile is not buildable in status "
            f"{value.get('status')!r}: {profile}"
        )
    batches = value["batches"]
    assert isinstance(batches, list)
    return [Path(str(path)) for path in batches]


def resolve_release_batches(
    profile: str | None, requested: list[Path], stack: dict[str, object] | None = None
) -> list[Path]:
    """Return the complete ordered layer set for a playable release.

    Accepted layers are never optional. Named profiles add all mutually dependent
    batches for a feature, preventing a partial command from silently reverting UI.
    """
    stack = stack or load_release_stack()
    profiles = stack["profiles"]
    assert isinstance(profiles, dict)
    registered_owners: dict[str, set[str]] = defaultdict(set)
    for profile_name, value in profiles.items():
        assert isinstance(profile_name, str) and isinstance(value, dict)
        for path in value["batches"]:
            registered_owners[Path(str(path)).as_posix().casefold()].add(profile_name)
    for path in requested:
        owners = registered_owners.get(path.as_posix().casefold(), set())
        if not owners:
            raise ValueError(
                f"{path} is not registered in a release profile; add the complete "
                "feature layer to translations/release_stack.json first"
            )
        if profile not in owners:
            raise ValueError(
                f"{path} belongs to registered profile(s) {sorted(owners)}; "
                "select the matching --profile instead of applying it manually"
            )
    paths = accepted_batch_paths(stack)
    if profile is not None:
        paths.extend(profile_batch_paths(stack, profile))
    paths.extend(requested)
    unique: list[Path] = []
    seen: set[str] = set()
    for path in paths:
        key = path.as_posix().casefold()
        if key not in seen:
            seen.add(key)
            unique.append(path)
    return unique


def apply_arm9_fixed_batches(
    batch_paths: list[Path], source: bytes
) -> tuple[bytes, list[str]]:
    """Apply a source-locked, fixed-width ARM9 text batch.

    ARM9 labels are not ILNK records, but they still need the same parent and
    byte-preservation guarantees as dialogue batches. Each entry verifies the
    exact source bytes at its declared offset and can only shrink in place.
    """
    rebuilt = bytearray(source)
    record_ids: list[str] = []
    claimed: set[int] = set()
    actual_hash = sha256(source)
    for batch_path in batch_paths:
        batch = load_batch_header(batch_path)
        if batch.get("format") != "dk4-arm9-fixed-text-batch-v1":
            raise ValueError(f"{batch_path}: unsupported ARM9 batch format")
        inline_code = batch.get("content_type") == "arm9-inline-code-v1"
        expected_hash = str(batch.get("source_file_sha256", "")).lower()
        if expected_hash != actual_hash:
            raise ValueError(
                f"{batch_path}: ARM9 source SHA-256 mismatch "
                f"(expected {expected_hash}, got {actual_hash})"
            )
        records = batch.get("records")
        if not isinstance(records, list) or not records:
            raise ValueError(f"{batch_path}: ARM9 batch has no records")
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
            replacement_hex = str(record.get("replacement_hex", ""))
            if inline_code:
                runtime_address = int(record.get("runtime_address", -1))
                expected_runtime_address = ARM9_LOAD_ADDRESS + offset
                if runtime_address != expected_runtime_address:
                    raise ValueError(
                        f"{batch_path}: {row_id} runtime address does not match "
                        f"component offset (expected {expected_runtime_address:#010x})"
                    )
                runtime_end = runtime_address + len(expected)
                if (
                    runtime_address < PROHIBITED_RUNTIME_DATA_END
                    and runtime_end > PROHIBITED_RUNTIME_DATA_START
                ):
                    raise ValueError(
                        f"{batch_path}: {row_id} overlaps the prohibited runtime-owned "
                        "ARM9 data tail"
                    )
                if not replacement_hex:
                    raise ValueError(
                        f"{batch_path}: {row_id} inline code requires replacement_hex"
                    )
            if replacement_hex:
                replacement = bytes.fromhex(replacement_hex)
                if len(replacement) != len(expected):
                    raise ValueError(
                        f"{batch_path}: {row_id} raw replacement is {len(replacement)} bytes; "
                        f"exactly {len(expected)} bytes are required"
                    )
            else:
                encoding = str(record.get("encoding", "ascii"))
                replacement = str(record.get("english", "")).encode(encoding)
                if len(replacement) > len(expected):
                    raise ValueError(
                        f"{batch_path}: {row_id} replacement is {len(replacement)} bytes; "
                        f"slot is {len(expected)} bytes"
                    )
                replacement = replacement.ljust(len(expected), b"\0")
            rebuilt[offset : offset + len(expected)] = replacement
            claimed.update(range(offset, offset + len(expected)))
            record_ids.append(row_id)
    return bytes(rebuilt), record_ids


def apply_arm9_fixed_batch(batch_path: Path, source: bytes) -> tuple[bytes, list[str]]:
    return apply_arm9_fixed_batches([batch_path], source)


def apply_pxl_label_batches(
    batch_paths: list[Path], source: bytes
) -> tuple[bytes, list[str]]:
    """Redraw source-locked labels inside an existing fixed-size PXL atlas."""

    actual_hash = sha256(source)
    image = PxlImage.from_bytes(source)
    record_ids: list[str] = []
    claimed_boxes: list[tuple[int, int, int, int]] = []
    for batch_path in batch_paths:
        batch = load_batch_header(batch_path)
        if batch.get("format") != "dk4-pxl-label-batch-v1":
            raise ValueError(f"{batch_path}: unsupported PXL batch format")
        if str(batch.get("source_file_sha256", "")).lower() != actual_hash:
            raise ValueError(f"{batch_path}: PXL source SHA-256 mismatch")
        records = batch.get("records")
        if not isinstance(records, list) or not records:
            raise ValueError(f"{batch_path}: PXL batch has no records")
        for record in records:
            if not isinstance(record, dict):
                raise TypeError(f"{batch_path}: PXL record must be an object")
            row_id = str(record.get("id", ""))
            if not row_id or row_id in record_ids:
                raise ValueError(f"{batch_path}: duplicate or missing PXL record id")
            raw_box = record.get("box")
            if not isinstance(raw_box, list) or len(raw_box) != 4:
                raise ValueError(f"{batch_path}: {row_id} requires a four-value box")
            box = tuple(int(value) for value in raw_box)
            left, top, right, bottom = box
            if not (0 <= left < right <= image.width and 0 <= top < bottom <= image.height):
                raise ValueError(f"{batch_path}: {row_id} box is outside the PXL atlas")
            if any(
                left < old_right
                and right > old_left
                and top < old_bottom
                and bottom > old_top
                for old_left, old_top, old_right, old_bottom in claimed_boxes
            ):
                raise ValueError(f"{batch_path}: {row_id} overlaps another PXL label")
            erase = str(record.get("erase", "dark-text"))
            if erase == "dark-text":
                image.erase_dark_text(box, threshold=int(record.get("threshold", 135)))
            elif erase == "palette-indices":
                raw_indices = record.get("palette_indices")
                if not isinstance(raw_indices, list) or not raw_indices:
                    raise ValueError(
                        f"{batch_path}: {row_id} requires palette_indices"
                    )
                extra_indices = batch.get("additional_palette_indices", [])
                if not isinstance(extra_indices, list):
                    raise ValueError(
                        f"{batch_path}: additional_palette_indices must be a list"
                    )
                image.erase_palette_indices(
                    box,
                    {
                        int(value)
                        for value in [*raw_indices, *extra_indices]
                    },
                )
            else:
                raise ValueError(f"{batch_path}: {row_id} has unsupported erase mode {erase!r}")
            image.draw_text(
                box,
                str(record.get("text", "")),
                int(record.get("color_index", 1)),
                outline_index=(
                    int(record["outline_index"])
                    if record.get("outline_index") is not None
                    else None
                ),
                maximum_size=int(record.get("maximum_size", 13)),
            )
            claimed_boxes.append(box)
            record_ids.append(row_id)
    rebuilt = image.to_bytes()
    if len(rebuilt) != len(source):
        raise ValueError("PXL label rebuild changed the resource allocation")
    return rebuilt, record_ids


def changed_segments(before: bytes, after: bytes) -> set[tuple[int, int]]:
    def logical_segments(block: bytes, block_index: int) -> list[bytes]:
        if block[:4] != b"CS\0\x01":
            return block.split(b"\0")
        logical_end = 8 + struct.unpack_from("<H", block, 4)[0]
        if logical_end > len(block) or any(block[logical_end:]):
            raise ValueError(f"invalid CS length in block {block_index}")
        return block[:logical_end].split(b"\0")

    old = IlnkContainer.parse(before)
    new = IlnkContainer.parse(after)
    if len(old.blocks) != len(new.blocks):
        raise ValueError("ILNK block count changed")
    changed: set[tuple[int, int]] = set()
    for block_index, (old_block, new_block) in enumerate(zip(old.blocks, new.blocks, strict=True)):
        old_segments = logical_segments(old_block, block_index)
        new_segments = logical_segments(new_block, block_index)
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


def validate_unchanged_segments(
    file_path: str,
    expected: set[tuple[int, int]],
    actual: set[tuple[int, int]],
    declared: set[tuple[int, int]],
) -> set[tuple[int, int]]:
    """Allow audited no-op records only when their exact segments are declared."""

    unchanged = expected - actual
    undeclared = unchanged - declared
    if undeclared:
        raise ValueError(
            f"{file_path}: requested records did not change without an explicit "
            f"declaration: {sorted(undeclared)}"
        )
    declared_but_changed = declared - unchanged
    if declared_but_changed:
        raise ValueError(
            f"{file_path}: records declared unchanged actually changed: "
            f"{sorted(declared_but_changed)}"
        )
    return unchanged


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
    try:
        release_stack = load_release_stack()
    except (OSError, TypeError, ValueError, json.JSONDecodeError) as error:
        raise SystemExit(f"invalid release stack: {error}") from None
    profiles = release_stack["profiles"]
    assert isinstance(profiles, dict)
    parser = argparse.ArgumentParser(
        description="Build a translation release only from the immutable accepted baseline."
    )
    parser.add_argument(
        "--base", type=Path, default=Path("out/raphael_natural_v2_accepted_base.nds")
    )
    parser.add_argument("--profile", choices=sorted(profiles))
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

    try:
        release_batches = resolve_release_batches(args.profile, args.batch, release_stack)
    except ValueError as error:
        raise SystemExit(str(error)) from None

    baseline = NdsImage.open(args.base)
    candidate = NdsImage.open(args.base)
    grouped: dict[str, list[Path]] = defaultdict(list)
    for batch_path in release_batches:
        header = load_batch_header(batch_path)
        try:
            validate_playable_dialogue_header(batch_path, header)
        except ValueError as error:
            raise SystemExit(str(error)) from None
        file_path = str(header.get("file_path", ""))
        if not file_path.startswith("/"):
            raise SystemExit(f"{batch_path}: invalid internal file path")
        grouped[file_path].append(batch_path)

    changed_records: dict[str, list[str]] = {}
    relocation_checks: dict[str, object] = {}
    for file_path, file_batch_paths in grouped.items():
        source = candidate.read_file(file_path)
        formats = {str(load_batch_header(path).get("format", "")) for path in file_batch_paths}
        if formats == {"dk4-pxl-label-batch-v1"}:
            rebuilt, record_ids = apply_pxl_label_batches(file_batch_paths, source)
            if rebuilt == source:
                raise SystemExit(f"{file_path}: PXL label batch made no changes")
            candidate.replace_file(file_path, rebuilt)
            changed_records[file_path] = record_ids
            continue
        if file_path == "/__arm9__.bin":
            rebuilt, record_ids = apply_arm9_fixed_batches(file_batch_paths, source)
            if rebuilt == source:
                raise SystemExit("ARM9 fixed-text batch made no changes")
            candidate.replace_file(file_path, rebuilt)
            changed_records[file_path] = record_ids
            continue
        relocation_paths = [
            batch_path
            for batch_path in file_batch_paths
            if load_batch_header(batch_path).get("encoder")
            == "dialogue-relocatable-v1"
        ]
        if relocation_paths:
            if len(relocation_paths) != 1:
                raise SystemExit(
                    f"{file_path}: exactly one relocation batch may target a file"
                )
            batch_path = relocation_paths[0]
            header = load_batch_header(batch_path)
            try:
                validate_natural_dialogue_qa(batch_path, header, source)
                map_path_value = str(header.get("relocation_map", ""))
                if not map_path_value:
                    raise ValueError("relocatable dialogue requires relocation_map")
                map_path = Path(map_path_value)
                relocation_map = load_relocation_map(map_path)
                rows = read_translation_batch(batch_path, source)
                profile = get_dialogue_profile(
                    str(header.get("dialogue_profile", ""))
                )
                result = rebuild_mapped_cs_dialogue(
                    source, rows, profile, relocation_map
                )
            except ValueError as error:
                raise SystemExit(f"{batch_path}: {error}") from None

            relocated_segments = {parse_pointer_group(row) for row in rows}
            fixed_rows: list[dict[str, object]] = []
            fixed_ids: set[str] = set()
            for fixed_path in file_batch_paths:
                if fixed_path == batch_path:
                    continue
                fixed_header = load_batch_header(fixed_path)
                if fixed_header.get("encoder") != "dialogue-fixed-v1":
                    raise SystemExit(
                        f"{file_path}: relocation may be combined only with "
                        "dialogue-fixed-v1 batches"
                    )
                try:
                    validate_natural_dialogue_qa(fixed_path, fixed_header, source)
                except ValueError as error:
                    raise SystemExit(str(error)) from None
                for row in read_translation_batch(fixed_path, source):
                    row_id = str(row["id"])
                    if row_id in fixed_ids:
                        raise SystemExit(
                            f"{file_path}: duplicate fixed record across hybrid batches: "
                            f"{row_id}"
                        )
                    fixed_ids.add(row_id)
                    if parse_pointer_group(row) in relocated_segments:
                        if header.get("override_fixed_records") is not True:
                            raise SystemExit(
                                f"{batch_path}: overlapping fixed record requires "
                                "override_fixed_records"
                            )
                        continue
                    fixed_rows.append(row)

            rebuilt = (
                rebuild_mesfile(result.rebuilt_file, fixed_rows)
                if fixed_rows
                else result.rebuilt_file
            )
            actual_segments = changed_segments(source, rebuilt)
            expected_segments = relocated_segments | {
                parse_pointer_group(row) for row in fixed_rows
            }
            block_index = int(relocation_map["block_index"])
            unexpected = actual_segments - expected_segments - {(block_index, 1)}
            if unexpected:
                raise SystemExit(
                    f"{file_path}: hybrid relocation changed undeclared segments: "
                    f"{sorted(unexpected)}"
                )
            segment_to_id = {
                parse_pointer_group(row): str(row["id"])
                for row in [*fixed_rows, *rows]
            }
            candidate.replace_file(file_path, rebuilt)
            changed_records[file_path] = [
                segment_to_id[segment]
                for segment in sorted(actual_segments - {(block_index, 1)})
                if segment in segment_to_id
            ]
            final_block = IlnkContainer.parse(rebuilt).blocks[block_index]
            relocation_checks[file_path] = {
                "map": map_path.as_posix(),
                "map_sha256": sha256(map_path.read_bytes()),
                "block_index": block_index,
                "source_block_sha256": sha256(result.old_block),
                "rebuilt_block_sha256": sha256(final_block),
                "changed_segments": list(result.changed_segments),
                "parity_padded_segments": list(result.parity_padded_segments),
                "block_size_delta": result.size_delta,
                "external_references_complete": True,
                "hybrid_fixed_record_count": len(fixed_rows),
                "relocation_overrides_fixed_records": sorted(
                    str(row["id"])
                    for row in rows
                    if str(row["id"]) in fixed_ids
                ),
            }
            continue
        rows: list[dict[str, object]] = []
        declared_unchanged_ids: set[str] = set()
        for batch_path in file_batch_paths:
            header = load_batch_header(batch_path)
            try:
                validate_natural_dialogue_qa(batch_path, header, source)
            except ValueError as error:
                raise SystemExit(str(error)) from None
            batch_rows = read_translation_batch(batch_path, source)
            batch_ids = {str(row["id"]) for row in batch_rows}
            unchanged_ids = {
                str(value) for value in header.get("unchanged_records", [])
            }
            if unchanged_ids and not str(
                header.get("unchanged_record_reason", "")
            ).strip():
                raise SystemExit(
                    f"{batch_path}: unchanged_records requires unchanged_record_reason"
                )
            unknown_unchanged = unchanged_ids - batch_ids
            if unknown_unchanged:
                raise SystemExit(
                    f"{batch_path}: unchanged_records contains IDs outside the batch: "
                    f"{sorted(unknown_unchanged)}"
                )
            declared_unchanged_ids.update(unchanged_ids)
            rows.extend(batch_rows)
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
        segment_by_id = {
            str(row["id"]): parse_pointer_group(row) for row in rows
        }
        declared_unchanged = {
            segment_by_id[row_id] for row_id in declared_unchanged_ids
        }
        rebuilt = rebuild_mesfile(source, rows)
        actual_segments = changed_segments(source, rebuilt)
        unexpected = actual_segments - expected_segments
        if unexpected:
            raise SystemExit(
                f"{file_path}: unrequested ILNK segments changed: {sorted(unexpected)}"
            )
        try:
            validate_unchanged_segments(
                file_path, expected_segments, actual_segments, declared_unchanged
            )
        except ValueError as error:
            raise SystemExit(str(error)) from None
        candidate.replace_file(file_path, rebuilt)
        changed_records[file_path] = [
            row_id
            for row_id in record_ids
            if segment_by_id[row_id] in actual_segments
        ]

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
        "profile": args.profile,
        "release_stack": str(RELEASE_STACK_PATH),
        "release_stack_sha256": sha256(RELEASE_STACK_PATH.read_bytes()),
        "required_batches": [
            str(path) for path in accepted_batch_paths(release_stack)
        ],
        "batches": [str(path) for path in release_batches],
        "checks": {
            "canonical_base": True,
            "release_stack_enforced": True,
            "undeclared_files_unchanged": True,
            "untouched_ilnk_segments_unchanged": True,
            "main_menu_anchors_present": True,
            "unmapped_story_control_records_rejected": True,
            "natural_dialogue_qa_enforced": True,
            "no_new_placeholder_fallbacks": True,
            "saved_rom_roundtrip": True,
            "mapped_ilnk_relocation_enforced": bool(relocation_checks)
            if relocation_checks
            else True,
        },
        "relocations": relocation_checks,
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
