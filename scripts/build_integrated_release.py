from __future__ import annotations

import argparse
import hashlib
import json
import struct
import zlib
from collections import Counter, defaultdict
from datetime import UTC, datetime
from pathlib import Path

from dk4tool.dialogue.font_audit import GameAsciiFont
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
from dk4tool.graphics.compact_font import FONT_IDENTITIES as COMPACT_FONT_IDENTITIES
from dk4tool.graphics.compact_font import layout as compact_font_layout
from dk4tool.graphics.fls import FlsArchive
from dk4tool.graphics.obj_banked_sync import FORMAT as OBJ_BANKED_SYNC_FORMAT
from dk4tool.graphics.obj_banked_sync import apply_banked_sync
from dk4tool.graphics.pxl import PxlImage
from dk4tool.graphics.raw_bgr555_art import FORMAT as RAW_BGR555_ART_FORMAT
from dk4tool.graphics.raw_bgr555_art import apply_raw_bgr555_art
from dk4tool.patch.grand_race_help_release import validate_release_batch as validate_grand_race_help
from dk4tool.patch.grand_race_help_shared_titles import (
    MENU as SHARED_HELP_MENU_DEPENDENCY,
)
from dk4tool.patch.grand_race_help_shared_titles import (
    validate_release_batch as validate_shared_help_titles,
)
from dk4tool.patch.grand_race_menu_release import validate_release_batch as validate_grand_race_menu
from dk4tool.patch.grand_race_status_release import (
    validate_release_batch as validate_grand_race_status,
)
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_reblocking_release import apply_common_reblocking
from dk4tool.script.mesfile import rebuild_mesfile
from dk4tool.script.translation_batch import (
    materialize_translation_batch,
    read_translation_batch,
)

CANONICAL_BASELINE_SHA256 = (
    "3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe"
)
REQUIRED_MENU_TEXT = (b"Continue", b"New Game", b"Grand Race", b"Extras", b"Gallery")
REQUIRED_OPTIONS_TEXT = (b"Opts", b"Options")
FORBIDDEN_PLACEHOLDERS = (
    b"see below",
    b"The crew needs a marine captain to enforce the order.",
)
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
    """Require byte-modelled, pair-safe encoding for playable story dialogue."""

    if header.get("format") != "dk4-ilnk-translation-batch-v1":
        return
    file_path = str(header.get("file_path", ""))
    if file_path not in {f"/data/SC{index}.DK4" for index in range(4)}:
        return
    if header.get("encoder") not in {
        "dialogue-fixed-v1",
        "dialogue-relocatable-v1",
    }:
        raise ValueError(
            f"{path}: playable progressive-story dialogue requires the validated "
            "fixed or relocatable encoder; legacy raw translation is forbidden"
        )
    profile_name = str(header.get("dialogue_profile", ""))
    profile = get_dialogue_profile(profile_name)
    if profile.literal_prefix_policy != "forbid":
        raise ValueError(
            f"{path}: native literal-prefix dialogue requires a source-bound "
            "post-layer release with the proven runtime hash; direct story "
            "batching cannot establish that contract"
        )
    if (
        profile_name.endswith("-revoked")
        or not profile.guard_linebreaks
        or not profile.pair_phase_safe_breaks
    ):
        raise ValueError(
            f"{path}: playable progressive-story dialogue requires a live-safe "
            "guarded, pair-phase-aware profile; research profile is forbidden"
        )


def validate_ascii_guard_policy(path: Path, header: dict[str, object]) -> None:
    """Reject raw fixed text that can lose its first printable ASCII glyph.

    Packed COMMON records may have several independently addressed strings.
    Their entry points cannot be inferred from the byte stream, so guarded
    batches declare them explicitly. Every declared entry and every printable
    continuation after LF must begin with two sacrificial spaces.
    """

    policy = header.get("ascii_guard_policy")
    if policy is None:
        records = header.get("records", [])
        raw_english_ilnk = (
            header.get("format") == "dk4-ilnk-translation-batch-v1"
            and header.get("target_locale") == "en-US"
            and isinstance(records, list)
            and any(
                isinstance(record, dict) and bool(record.get("replacement_hex"))
                for record in records
            )
        )
        exemption = str(header.get("ascii_guard_exemption", "")).strip()
        if raw_english_ilnk and not exemption:
            raise ValueError(
                f"{path}: raw English ILNK text requires ascii_guard_policy or a "
                "documented ascii_guard_exemption"
            )
        return
    if policy != "two-byte-entry-and-line-v1":
        raise ValueError(f"{path}: unsupported ascii_guard_policy {policy!r}")
    if header.get("format") != "dk4-ilnk-translation-batch-v1":
        raise ValueError(f"{path}: ASCII guard policy is valid only for ILNK text")

    records = header.get("records")
    if not isinstance(records, list) or not records:
        raise ValueError(f"{path}: guarded batch has no records")
    for record in records:
        if not isinstance(record, dict):
            raise TypeError(f"{path}: guarded record must be an object")
        row_id = str(record.get("id", ""))
        replacement_hex = record.get("replacement_hex")
        if not isinstance(replacement_hex, str) or not replacement_hex:
            raise ValueError(f"{path}: {row_id} guarded record requires replacement_hex")
        replacement = bytes.fromhex(replacement_hex)
        record_exemption = str(record.get("ascii_guard_exemption", "")).strip()
        if record_exemption:
            # Some renderers display rather than consume their source indent.
            # A per-record exemption must be explicit so an observed layout can
            # be preserved without weakening the rest of a guarded batch.
            continue
        offsets = record.get("entry_offsets")
        if (
            not isinstance(offsets, list)
            or not offsets
            or not all(isinstance(value, int) for value in offsets)
            or offsets != sorted(set(offsets))
        ):
            raise ValueError(
                f"{path}: {row_id} requires sorted, unique entry_offsets"
            )
        if offsets[0] < 0 or offsets[-1] >= len(replacement):
            raise ValueError(f"{path}: {row_id} entry offset is outside the record")
        for index, start in enumerate(offsets):
            end = offsets[index + 1] if index + 1 < len(offsets) else len(replacement)
            segment = replacement[start:end]
            if not segment.startswith(b"  "):
                raise ValueError(
                    f"{path}: {row_id} entry at byte {start} lacks a two-byte guard"
                )
            for position, value in enumerate(segment[:-1]):
                if value != 0x0A or segment[position + 1] == 0x0A:
                    continue
                if segment[position + 1 : position + 3] != b"  ":
                    raise ValueError(
                        f"{path}: {row_id} LF at byte {start + position} lacks a "
                        "two-byte continuation guard"
                    )
            for line in segment.split(b"\n"):
                used = line.rstrip(b" \0")
                visible_limit = record.get("text_box_max_chars")
                if visible_limit is None:
                    if len(used) > 31:
                        raise ValueError(
                            f"{path}: {row_id} guarded line exceeds 31 bytes"
                        )
                elif len(used[2:]) > int(visible_limit):
                    raise ValueError(
                        f"{path}: {row_id} guarded line exceeds "
                        f"{int(visible_limit)} visible bytes"
                    )


def validate_fixed_text_layout_policy(path: Path, header: dict[str, object]) -> None:
    """Validate renderer-specific termination, indentation, and line limits.

    Fixed allocations are not interchangeable: some renderers consume a guard
    byte, while others display it. Records therefore declare the behavior that
    was verified for their actual screen instead of relying on a global leading
    space convention.
    """

    records = header.get("records")
    if not isinstance(records, list):
        return
    policy = header.get("fixed_text_policy", {})
    if policy is None:
        policy = {}
    if not isinstance(policy, dict):
        raise TypeError(f"{path}: fixed_text_policy must be an object")
    require_c_string = bool(policy.get("require_c_string_termination"))
    default_max = policy.get("maximum_prose_line_characters")
    default_no_indent = bool(policy.get("forbid_visible_leading_space"))
    default_line_guard = int(policy.get("linebreak_guard_bytes", 0))

    for record in records:
        if not isinstance(record, dict):
            continue
        row_id = str(record.get("id", ""))
        english = record.get("english")
        entries = record.get("display_entries")
        if entries is None:
            display_entries = [english] if isinstance(english, str) else []
        elif isinstance(entries, list) and all(isinstance(value, str) for value in entries):
            display_entries = entries
        else:
            raise ValueError(f"{path}: {row_id} display_entries must be strings")

        if require_c_string and record.get("string_kind") == "c-string":
            if not isinstance(english, str):
                raise ValueError(f"{path}: {row_id} C string requires English text")
            allocation = len(bytes.fromhex(str(record.get("source_hex", ""))))
            if len(english.encode(str(record.get("encoding", "ascii")))) >= allocation:
                raise ValueError(
                    f"{path}: {row_id} leaves no room for a C-string terminator"
                )

        max_chars = record.get("text_box_max_chars", default_max)
        line_guard = int(record.get("linebreak_guard_bytes", default_line_guard))
        if line_guard < 0:
            raise ValueError(f"{path}: {row_id} has a negative line-break guard")
        if max_chars is not None:
            width = int(max_chars)
            for entry in display_entries:
                for index, line in enumerate(entry.split("\n")):
                    visible = line[line_guard:] if index and line_guard else line
                    if index and line_guard and not line.startswith(" " * line_guard):
                        raise ValueError(
                            f"{path}: {row_id} line {index + 1} lacks its "
                            f"{line_guard}-byte renderer guard"
                        )
                    if len(visible) > width:
                        raise ValueError(
                            f"{path}: {row_id} line exceeds {width} characters: {visible!r}"
                        )

        no_indent = bool(record.get("forbid_visible_leading_space", default_no_indent))
        if no_indent:
            for entry in display_entries:
                for index, line in enumerate(entry.split("\n")):
                    visible = line[line_guard:] if index and line_guard else line
                    if visible.startswith((" ", "\t")):
                        raise ValueError(
                            f"{path}: {row_id} contains a visible leading indent"
                        )


def validate_fixed_allocation_policy(path: Path, header: dict[str, object]) -> None:
    """Validate screen-specific guards and translated byte ranges.

    This policy is intentionally opt-in.  It gives new fixed-allocation work a
    stronger contract without pretending that every historical COMMON batch
    used the same renderer.  Each translated range must be English-only, every
    independently addressed entry must retain its declared consumed guard, and
    every manual line break must carry the renderer's continuation guard.
    """

    policy = header.get("fixed_allocation_policy")
    if policy is None:
        return
    if policy != "screen-entry-layout-v1":
        raise ValueError(f"{path}: unsupported fixed_allocation_policy {policy!r}")
    records = header.get("records")
    if not isinstance(records, list) or not records:
        raise ValueError(f"{path}: fixed-allocation batch has no records")

    for record in records:
        if not isinstance(record, dict):
            raise TypeError(f"{path}: fixed-allocation record must be an object")
        row_id = str(record.get("id", ""))
        raw_hex = record.get("replacement_hex")
        if not isinstance(raw_hex, str) or not raw_hex:
            raise ValueError(f"{path}: {row_id} requires replacement_hex")
        replacement = bytes.fromhex(raw_hex)
        ranges = record.get("translated_ranges")
        if not (
            isinstance(ranges, list)
            and ranges
            and all(
                isinstance(pair, list)
                and len(pair) == 2
                and all(isinstance(value, int) for value in pair)
                for pair in ranges
            )
        ):
            raise ValueError(f"{path}: {row_id} requires translated_ranges")
        for start, end in ranges:
            if not 0 <= start < end <= len(replacement):
                raise ValueError(f"{path}: {row_id} has an invalid translated range")
            translated = replacement[start:end]
            safe_latin = record.get("safe_literal_latin_glyphs", [])
            if not isinstance(safe_latin, list) or any(character not in {"Ｆ", "Ｉ"} for character in safe_latin):
                raise ValueError(f"{path}: {row_id} declares an unsupported literal Latin glyph")
            try:
                text = translated.decode("cp932" if safe_latin else "ascii")
            except UnicodeDecodeError as exc:
                raise ValueError(
                    f"{path}: {row_id} translated range contains non-ASCII text"
                ) from exc
            if any(ord(character) > 127 and character not in safe_latin for character in text):
                raise ValueError(f"{path}: {row_id} contains an undeclared non-ASCII glyph")
            if any("\u3040" <= char <= "\u30ff" or "\u3400" <= char <= "\u9fff" for char in text):
                raise ValueError(f"{path}: {row_id} translated range mixes Japanese text")

        starts = record.get("entry_offsets")
        if not (
            isinstance(starts, list)
            and starts
            and all(isinstance(value, int) for value in starts)
            and starts == sorted(set(starts))
        ):
            raise ValueError(f"{path}: {row_id} requires sorted entry_offsets")
        declared_ends = record.get("entry_ends")
        if declared_ends is not None and not (
            isinstance(declared_ends, list)
            and len(declared_ends) == len(starts)
            and all(isinstance(value, int) for value in declared_ends)
        ):
            raise ValueError(f"{path}: {row_id} has invalid entry_ends")
        entry_guard = int(record.get("entry_guard_bytes", 0))
        line_guard = int(record.get("linebreak_guard_bytes", 0))
        width = int(record.get("text_box_max_chars", 40))
        for position, start in enumerate(starts):
            end = (
                declared_ends[position]
                if isinstance(declared_ends, list)
                else starts[position + 1]
                if position + 1 < len(starts)
                else len(replacement)
            )
            if not start < end <= len(replacement):
                raise ValueError(f"{path}: {row_id} has an invalid entry end")
            segment = replacement[start:end]
            if not segment.startswith(b" " * entry_guard):
                raise ValueError(f"{path}: {row_id} entry at {start} lacks its guard")
            for line_index, line in enumerate(segment.rstrip(b" \0\n").split(b"\n")):
                guard = entry_guard if line_index == 0 else line_guard
                if not line.startswith(b" " * guard):
                    raise ValueError(
                        f"{path}: {row_id} line {line_index + 1} lacks its guard"
                    )
                visible = line[guard:]
                if len(visible) > width:
                    raise ValueError(
                        f"{path}: {row_id} line exceeds {width} visible characters"
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
        if batch.get("native_text_repack"):
            validate_grand_race_help(batch, source)
        if batch.get("native_shared_help_titles"):
            if Path(SHARED_HELP_MENU_DEPENDENCY) not in batch_paths:
                raise ValueError("Shared help titles require the complete native menu batch")
            validate_shared_help_titles(batch, source)
        if batch.get("native_menu_labels"):
            validate_grand_race_menu(batch, source)
        if batch.get("native_wireless_status"):
            validate_grand_race_status(batch, source)
        if batch.get("native_complete_race_ui"):
            from dk4tool.patch.grand_race_complete_release import validate_release_batch

            validate_release_batch(batch, source, batch_paths)
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
            elif erase == "solid":
                image.clear(box, int(record.get("erase_color_index", 0)))
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


def apply_fls_label_batch(
    batch_path: Path, source: bytes
) -> tuple[bytes, list[str]]:
    """Redraw source-locked subtitle cards inside one fixed-size FLS archive."""

    batch = load_batch_header(batch_path)
    if batch.get("format") != "dk4-fls-label-batch-v1":
        raise ValueError(f"{batch_path}: unsupported FLS label format")
    if str(batch.get("source_file_sha256", "")).lower() != sha256(source):
        raise ValueError(f"{batch_path}: FLS source SHA-256 mismatch")
    records = batch.get("records")
    if not isinstance(records, list) or not records:
        raise ValueError(f"{batch_path}: FLS label batch has no records")

    archive = FlsArchive(source)
    record_ids: list[str] = []
    claimed_assets: set[int] = set()
    for record in records:
        if not isinstance(record, dict):
            raise TypeError(f"{batch_path}: FLS label record must be an object")
        row_id = str(record.get("id", ""))
        asset_index = int(record.get("asset_index", -1))
        lines = record.get("lines")
        if not row_id or row_id in record_ids:
            raise ValueError(f"{batch_path}: duplicate or missing FLS label id")
        if asset_index < 0 or asset_index >= archive.count:
            raise ValueError(f"{batch_path}: {row_id} asset index is out of range")
        if asset_index in claimed_assets:
            raise ValueError(f"{batch_path}: duplicate FLS asset {asset_index}")
        if not isinstance(lines, list) or not lines or not all(
            isinstance(line, str) and line for line in lines
        ):
            raise ValueError(f"{batch_path}: {row_id} requires nonempty text lines")
        viewport_policy = batch.get("native_viewport_policy")
        if viewport_policy not in (None, "header-width-v1", "header-size-v2"):
            raise ValueError(f"{batch_path}: unknown native FLS viewport policy")
        layout_width = int(record["layout_width"]) if record.get("layout_width") is not None else None
        layout_height = int(record["layout_height"]) if record.get("layout_height") is not None else None
        if viewport_policy in ("header-width-v1", "header-size-v2"):
            native_width = archive.records[asset_index][0] >> 16
            if not 1 <= native_width <= archive.texture(asset_index).width:
                raise ValueError(f"{batch_path}: {row_id} invalid native FLS width")
            if layout_width is not None and layout_width != native_width:
                raise ValueError(f"{batch_path}: {row_id} text layout differs from native FLS viewport")
            layout_width = native_width
        if viewport_policy == "header-size-v2":
            native_height = archive.records[asset_index][1] & 0xFFFF
            if not 1 <= native_height <= archive.texture(asset_index).height:
                raise ValueError(f"{batch_path}: {row_id} invalid native FLS height")
            if layout_height is not None and layout_height != native_height:
                raise ValueError(f"{batch_path}: {row_id} text layout differs from native FLS height")
            layout_height = native_height
        archive.texture(asset_index).replace_with_lines(
            lines,
            maximum_size=int(record.get("maximum_size", 12)),
            background_index=int(record.get("background_index", 0)),
            color_index=int(record.get("color_index", 1)),
            outline_index=(
                int(record["outline_index"])
                if record.get("outline_index") is not None
                else None
            ),
            layout_width=layout_width,
            layout_height=layout_height,
        )
        if viewport_policy in ("header-width-v1", "header-size-v2"):
            texture = archive.texture(asset_index)
            background = int(record.get("background_index", 0))
            if any(value != background and (index % texture.width >= layout_width
                                           or (viewport_policy == "header-size-v2" and index // texture.width >= layout_height))
                   for index, value in enumerate(texture.indices)):
                raise ValueError(f"{batch_path}: {row_id} subtitle ink or outline escapes native viewport")
        claimed_assets.add(asset_index)
        record_ids.append(row_id)

    rebuilt = archive.to_bytes()
    if len(rebuilt) != len(source):
        raise ValueError("FLS label rebuild changed the resource allocation")
    return rebuilt, record_ids


def apply_pxl_indexed_region_batch(batch_path: Path, source: bytes) -> tuple[bytes, list[str]]:
    """Apply reviewed indexed artwork while preserving PXL metadata and unowned cells."""
    batch = load_batch_header(batch_path)
    if batch.get('format') != 'dk4-pxl-indexed-region-batch-v1':
        raise ValueError('Unsupported indexed PXL artwork format')
    if batch.get('source_file_sha256') != sha256(source):
        raise ValueError('PXL source SHA-256 mismatch')
    records = batch.get('records')
    if not isinstance(records, list) or not records:
        raise ValueError('Indexed PXL artwork requires records')
    image = PxlImage.from_bytes(source)
    original = bytes(image.indices)
    ids: list[str] = []
    owned: set[int] = set()
    for row in records:
        record_id = str(row['id'])
        box = row['box']
        if not record_id or record_id in ids or not isinstance(box, list) or len(box) != 4:
            raise ValueError('Duplicate or invalid indexed PXL artwork record')
        x0, y0, x1, y1 = (int(v) for v in box)
        if not 0 <= x0 < x1 <= image.width or not 0 <= y0 < y1 <= image.height:
            raise ValueError('Indexed PXL artwork escapes original image')
        offsets = [y * image.width + x for y in range(y0, y1) for x in range(x0, x1)]
        if owned.intersection(offsets):
            raise ValueError('Overlapping indexed PXL artwork regions')
        if row['source_region_sha256'] != sha256(bytes(original[i] for i in offsets)):
            raise ValueError('PXL source region identity differs')
        pixels = zlib.decompress(bytes.fromhex(row['indices_zlib_hex']))
        if len(pixels) != len(offsets) or row['indices_sha256'] != sha256(pixels):
            raise ValueError('Indexed PXL artwork extent or identity differs')
        if any(v >= len(image.palette) for v in pixels):
            raise ValueError('Indexed PXL artwork palette index out of range')
        for offset, value in zip(offsets, pixels, strict=True):
            image.indices[offset] = value
        owned.update(offsets)
        ids.append(record_id)
    rebuilt = image.to_bytes()
    if len(rebuilt) != len(source) or rebuilt[:image.pixels_offset] != source[:image.pixels_offset]:
        raise ValueError('Indexed PXL artwork changed metadata or allocation')
    return rebuilt, ids


def apply_ilnk_indexed_region_batch(batch_path: Path, source: bytes) -> tuple[bytes, list[str]]:
    """Apply reviewed regions in exact type-16 single-bank 8-bit legacy images."""
    batch = load_batch_header(batch_path)
    if batch.get('format') != 'dk4-ilnk-indexed-region-batch-v1':
        raise ValueError('Unsupported indexed ILNK artwork format')
    if batch.get('source_file_sha256') != sha256(source):
        raise ValueError('ILNK source SHA-256 mismatch')
    records = batch.get('records')
    if not isinstance(records, list) or not records:
        raise ValueError('Indexed ILNK artwork requires records')
    original = IlnkContainer.parse(source)
    rebuilt = IlnkContainer.parse(source)
    owned: dict[int, set[int]] = {}
    ids: list[str] = []
    for row in records:
        index, record_id = int(row['block_index']), str(row['id'])
        if not record_id or record_id in ids or not 0 <= index < len(original.blocks):
            raise ValueError('Duplicate or invalid indexed ILNK artwork record')
        raw = original.blocks[index]
        if row['source_block_sha256'] != sha256(raw):
            raise ValueError('ILNK source block identity differs')
        if struct.unpack_from('<3I', raw) != (16, 9, 524):
            raise ValueError('Exact type-16 single-bank 8-bit image required')
        extent, _flags, width_words, height = struct.unpack_from('<IIHH', raw, 532)
        width, pixel_start = width_words * 2, 544
        if extent != width * height + 12 or len(raw) < pixel_start + width * height:
            raise ValueError('ILNK indexed image extent differs')
        box = row['box']
        if not isinstance(box, list) or len(box) != 4:
            raise ValueError('Invalid indexed ILNK artwork box')
        x0, y0, x1, y1 = (int(v) for v in box)
        if not 0 <= x0 < x1 <= width or not 0 <= y0 < y1 <= height:
            raise ValueError('Indexed ILNK artwork escapes original image')
        offsets = [pixel_start + y * width + x for y in range(y0, y1) for x in range(x0, x1)]
        if owned.get(index, set()).intersection(offsets):
            raise ValueError('Overlapping indexed ILNK artwork regions')
        if row['source_region_sha256'] != sha256(bytes(raw[i] for i in offsets)):
            raise ValueError('ILNK source region identity differs')
        pixels = zlib.decompress(bytes.fromhex(row['indices_zlib_hex']))
        if len(pixels) != len(offsets) or row['indices_sha256'] != sha256(pixels):
            raise ValueError('Indexed ILNK artwork extent or identity differs')
        block = bytearray(rebuilt.blocks[index])
        for offset, value in zip(offsets, pixels, strict=True):
            block[offset] = value
        rebuilt.blocks[index] = bytes(block)
        owned.setdefault(index, set()).update(offsets)
        ids.append(record_id)
    result = rebuilt.to_bytes()
    if len(result) != len(source):
        raise ValueError('Indexed ILNK artwork changed allocation')
    for index, (a, b) in enumerate(zip(original.blocks, rebuilt.blocks, strict=True)):
        if any(x != y for offset, (x, y) in enumerate(zip(a, b, strict=True))
               if offset not in owned.get(index, set())):
            raise ValueError('Indexed ILNK artwork changed unowned metadata/pixels')
    return result, ids


def apply_fls_indexed_region_batch(batch_path: Path, source: bytes) -> tuple[bytes, list[str]]:
    """Apply reviewed indexed artwork inside locked FLS texture rectangles."""
    batch = load_batch_header(batch_path)
    if batch.get('format') != 'dk4-fls-indexed-region-batch-v1':
        raise ValueError('Unsupported indexed FLS artwork format')
    if batch.get('source_file_sha256') != sha256(source):
        raise ValueError('FLS source SHA-256 mismatch')
    records = batch.get('records')
    if not isinstance(records, list) or not records:
        raise ValueError('Indexed FLS artwork requires records')
    archive = FlsArchive(source)
    ids: list[str] = []
    owned: set[int] = set()
    # Opt-in mapping may reclaim only zero alignment bytes before a texture's
    # original compressed-pixel slot. Protect every declared native stream.
    protected_streams = [(record[2], record[2] + record[3]) for record in archive.records]
    protected_streams += [(record[4], record[4] + record[5]) for record in archive.records]
    reclaimed: set[int] = set()
    prefix_ranges: list[tuple[int, int]] = []
    for row in records:
        index = int(row['asset_index'])
        record_id = str(row['id'])
        if not record_id or record_id in ids or index in owned or not 0 <= index < archive.count:
            raise ValueError('Duplicate or invalid indexed FLS artwork ownership')
        texture = archive.texture(index)
        if (row['source_texture_sha256'] != sha256(bytes(texture.indices))
                or row['source_record'] != archive.records[index]):
            raise ValueError('FLS texture pixels or native record differ')
        box = row['box']
        if not isinstance(box, list) or len(box) != 4:
            raise ValueError('Invalid indexed FLS artwork box')
        x0, y0, x1, y1 = (int(v) for v in box)
        if not 0 <= x0 < x1 <= texture.width or not 0 <= y0 < y1 <= texture.height:
            raise ValueError('Indexed FLS artwork escapes original texture')
        pixels = zlib.decompress(bytes.fromhex(row['indices_zlib_hex']))
        if len(pixels) != (x1 - x0) * (y1 - y0) or row['indices_sha256'] != sha256(pixels):
            raise ValueError('Indexed FLS artwork extent or identity differs')
        if any(v >= len(texture.palette) for v in pixels):
            raise ValueError('Indexed FLS artwork palette index out of range')
        prefix = row.get('pixel_slot_prefix_bytes', 0)
        if not isinstance(prefix, int) or isinstance(prefix, bool) or prefix < 0 or prefix % 16:
            raise ValueError('FLS pixel-prefix reclaim must be a nonnegative aligned integer')
        if prefix:
            record = archive.records[index]
            start, end = record[4] - prefix, record[4]
            if start < record[2] + record[3] or any(start < hi and lo < end for lo, hi in protected_streams):
                raise ValueError('FLS pixel-prefix reclaim overlaps a native palette/pixel stream')
            absolute_start, absolute_end = archive.data_offset + start, archive.data_offset + end
            if not 0 <= absolute_start < absolute_end <= len(source) or any(source[absolute_start:absolute_end]):
                raise ValueError('FLS pixel-prefix reclaim is not locked zero alignment padding')
            if any(start < hi and lo < end for lo, hi in prefix_ranges):
                raise ValueError('FLS pixel-prefix reclaims overlap')
            record[4] -= prefix
            record[5] += prefix
            reclaimed.add(index)
            prefix_ranges.append((start, end))
        for y in range(y0, y1):
            start = (y - y0) * (x1 - x0)
            texture.indices[y * texture.width + x0:y * texture.width + x1] = pixels[start:start + x1 - x0]
        owned.add(index)
        ids.append(record_id)
    if reclaimed:
        mapped_source = bytearray(archive.source)
        for index in reclaimed:
            struct.pack_into('<2I', mapped_source, archive.table_offset + index * 24 + 16,
                             archive.records[index][4], archive.records[index][5])
        archive.source = bytes(mapped_source)
    rebuilt = archive.to_bytes()
    if len(rebuilt) != len(source):
        raise ValueError('Indexed FLS artwork changed allocation')
    return rebuilt, ids


def apply_ilnk_pxl_sync_batch(
    batch_path: Path, source: bytes, reference_pxl: bytes
) -> tuple[bytes, list[str]]:
    """Copy a translated PXL atlas into one fixed-size region of an ILNK block."""

    batch = load_batch_header(batch_path)
    if batch.get("format") != "dk4-ilnk-pxl-sync-v1":
        raise ValueError(f"{batch_path}: unsupported ILNK/PXL sync format")
    if str(batch.get("source_file_sha256", "")).lower() != sha256(source):
        raise ValueError(f"{batch_path}: ILNK source SHA-256 mismatch")
    if str(batch.get("source_image_sha256", "")).lower() != sha256(reference_pxl):
        raise ValueError(f"{batch_path}: reference PXL SHA-256 mismatch")

    block_index = int(batch.get("block_index", -1))
    header_size = int(batch.get("block_header_size", -1))
    target_width = int(batch.get("target_width", -1))
    target_height = int(batch.get("target_height", -1))
    target_x = int(batch.get("target_x", -1))
    target_y = int(batch.get("target_y", -1))
    record_id = str(batch.get("id", ""))
    if not record_id:
        raise ValueError(f"{batch_path}: missing record id")
    if target_width <= 0 or target_width % 2 or target_height <= 0:
        raise ValueError(f"{batch_path}: invalid packed 4bpp target dimensions")

    container = IlnkContainer.parse(source)
    if not 0 <= block_index < len(container.blocks):
        raise ValueError(f"{batch_path}: ILNK block index is out of range")
    block = bytearray(container.blocks[block_index])
    if str(batch.get("source_block_sha256", "")).lower() != sha256(block):
        raise ValueError(f"{batch_path}: ILNK block source SHA-256 mismatch")
    expected_payload = target_width * target_height // 2
    if header_size < 0 or len(block) - header_size != expected_payload:
        raise ValueError(f"{batch_path}: ILNK packed-pixel dimensions do not match")

    marker = PxlImage.from_bytes(reference_pxl)
    if marker.bits_per_pixel != 4:
        raise ValueError(f"{batch_path}: reference PXL must be 4bpp")
    if target_x < 0 or target_y < 0:
        raise ValueError(f"{batch_path}: negative atlas destination")
    if target_x + marker.width > target_width or target_y + marker.height > target_height:
        raise ValueError(f"{batch_path}: reference PXL does not fit target atlas")
    if target_x % 2 or marker.width % 2:
        raise ValueError(f"{batch_path}: 4bpp x coordinates and width must be even")

    row_stride = target_width // 2
    marker_stride = marker.width // 2
    for y in range(marker.height):
        destination = header_size + (target_y + y) * row_stride + target_x // 2
        source_row = y * marker.width
        packed = bytearray(marker_stride)
        for x in range(0, marker.width, 2):
            packed[x // 2] = (
                marker.indices[source_row + x]
                | marker.indices[source_row + x + 1] << 4
            )
        block[destination : destination + marker_stride] = packed

    original_blocks = list(container.blocks)
    container.blocks[block_index] = bytes(block)
    rebuilt = container.to_bytes()
    if len(rebuilt) != len(source):
        raise ValueError(f"{batch_path}: ILNK sync changed file size")
    rebuilt_blocks = IlnkContainer.parse(rebuilt).blocks
    if any(
        before != after
        for index, (before, after) in enumerate(
            zip(original_blocks, rebuilt_blocks, strict=True)
        )
        if index != block_index
    ):
        raise ValueError(f"{batch_path}: ILNK sync changed an unrelated block")
    return rebuilt, [record_id]


def apply_ilnk_pxl_sync_batches(
    batch_paths: list[Path], source: bytes, reference_images: dict[str, bytes]
) -> tuple[bytes, list[str]]:
    """Merge disjoint source-locked packed regions without rebasing any batch."""
    original = IlnkContainer.parse(source)
    combined = IlnkContainer.parse(source)
    owned: dict[int, set[int]] = {}
    geometries: dict[int, tuple[int, int, int]] = {}
    record_ids: list[str] = []
    for batch_path in batch_paths:
        header = load_batch_header(batch_path)
        reference = str(header.get("source_image_path", ""))
        if reference not in reference_images or not reference.startswith("/"):
            raise ValueError(f"{batch_path}: missing translated reference PXL")
        block_index = int(header.get("block_index", -1))
        rebuilt, ids = apply_ilnk_pxl_sync_batch(batch_path, source, reference_images[reference])
        image = PxlImage.from_bytes(reference_images[reference])
        header_size = int(header['block_header_size'])
        width, height = int(header['target_width']), int(header['target_height'])
        geometry = (header_size, width, height)
        if block_index in geometries and geometries[block_index] != geometry:
            raise ValueError(f"{batch_path}: inconsistent ILNK/PXL sync block geometry")
        geometries[block_index] = geometry
        x, y = int(header['target_x']), int(header['target_y'])
        region = {header_size + row * (width // 2) + column
                  for row in range(y, y + image.height)
                  for column in range(x // 2, (x + image.width) // 2)}
        if region & owned.get(block_index, set()):
            raise ValueError(f"{batch_path}: overlapping ILNK/PXL sync region ownership")
        if any(record_id in record_ids for record_id in ids):
            raise ValueError(f"{batch_path}: duplicate ILNK/PXL sync record id")
        result = IlnkContainer.parse(rebuilt)
        target = bytearray(combined.blocks[block_index])
        for offset in region:
            target[offset] = result.blocks[block_index][offset]
        combined.blocks[block_index] = bytes(target)
        owned.setdefault(block_index, set()).update(region)
        record_ids.extend(ids)
    rebuilt = combined.to_bytes()
    if len(rebuilt) != len(source) or any(
        before != after for index, (before, after) in enumerate(
            zip(original.blocks, IlnkContainer.parse(rebuilt).blocks, strict=True)
        ) if index not in owned
    ):
        raise ValueError("Combined ILNK/PXL sync changed unrelated blocks or file size")
    for index, offsets in owned.items():
        if any(a != b for offset, (a, b) in enumerate(zip(
                original.blocks[index], combined.blocks[index], strict=True))
               if offset not in offsets):
            raise ValueError("Combined ILNK/PXL sync changed unowned pixels or header")
    return rebuilt, record_ids


def order_graphics_sync_groups(grouped: dict[str, list[Path]]) -> list[tuple[str, list[Path]]]:
    """Resolve translated PXL inputs before their archive sync groups."""
    return sorted(grouped.items(), key=lambda item: any(
        load_batch_header(path).get("format") == "dk4-ilnk-pxl-sync-v1" for path in item[1]
    ))


def apply_ilnk_mixed_art_batches(batch_paths: list[Path], source: bytes,
                                 reference_images: dict[str, bytes]) -> tuple[bytes, list[str]]:
    """Merge reviewed raw art and legacy PXL syncs from one canonical source."""
    syncs = [p for p in batch_paths if load_batch_header(p).get("format") == "dk4-ilnk-pxl-sync-v1"]
    raws = [p for p in batch_paths if load_batch_header(p).get("format") == RAW_BGR555_ART_FORMAT]
    if len(syncs) + len(raws) != len(batch_paths) or len(raws) != 1:
        raise ValueError("Mixed ILNK artwork requires one raw batch and only declared syncs")
    sync_blocks = {int(load_batch_header(p)["block_index"]) for p in syncs}
    if 19 in sync_blocks:
        raise ValueError("Mixed ILNK artwork overlaps sync block")
    result, ids = apply_ilnk_pxl_sync_batches(syncs, source, reference_images) if syncs else (source, [])
    combined = IlnkContainer.parse(result)
    raw_result, raw_ids = apply_raw_bgr555_art(raws[0], source)
    if 19 in sync_blocks or set(ids).intersection(raw_ids):
        raise ValueError("Mixed ILNK artwork overlaps sync block or record IDs")
    raw_archive = IlnkContainer.parse(raw_result)
    original = IlnkContainer.parse(source)
    if any(a != b for i, (a, b) in enumerate(zip(original.blocks, raw_archive.blocks, strict=True)) if i != 19):
        raise ValueError("Raw artwork changed unrelated sync/archive blocks")
    combined.blocks[19] = raw_archive.blocks[19]
    return combined.to_bytes(), ids + raw_ids


def apply_obj_tile_pxl_sync_batch(
    batch_path: Path, source: bytes, reference_pxl: bytes
) -> tuple[bytes, list[str]]:
    """Copy rectangular PXL tile regions into a raw DS 4-bpp OBJ tile bank."""

    batch = load_batch_header(batch_path)
    if batch.get("format") != "dk4-obj-tile-pxl-sync-v1":
        raise ValueError(f"{batch_path}: unsupported OBJ/PXL sync format")
    if str(batch.get("source_file_sha256", "")).lower() != sha256(source):
        raise ValueError(f"{batch_path}: OBJ source SHA-256 mismatch")
    if str(batch.get("source_image_sha256", "")).lower() != sha256(reference_pxl):
        raise ValueError(f"{batch_path}: reference PXL SHA-256 mismatch")
    if len(source) % 32:
        raise ValueError(f"{batch_path}: OBJ bank is not composed of 32-byte 4bpp tiles")

    marker = PxlImage.from_bytes(reference_pxl)
    if marker.bits_per_pixel != 4 or marker.width % 8 or marker.height % 8:
        raise ValueError(f"{batch_path}: reference PXL must be an 8x8-aligned 4bpp atlas")
    records = batch.get("records")
    if not isinstance(records, list) or not records:
        raise ValueError(f"{batch_path}: OBJ/PXL sync batch has no records")

    rebuilt = bytearray(source)
    claimed_tiles: set[int] = set()
    record_ids: list[str] = []
    tile_count = len(source) // 32
    for record in records:
        if not isinstance(record, dict):
            raise TypeError(f"{batch_path}: OBJ/PXL record must be an object")
        record_id = str(record.get("id", ""))
        raw_box = record.get("source_tile_box")
        if not record_id or record_id in record_ids:
            raise ValueError(f"{batch_path}: duplicate or missing OBJ/PXL record id")
        if not isinstance(raw_box, list) or len(raw_box) != 4:
            raise ValueError(f"{batch_path}: {record_id} requires a source tile box")
        left, top, right, bottom = (int(value) for value in raw_box)
        target_tile = int(record.get("target_tile", -1))
        target_row_tiles = int(record.get("target_row_tiles", -1))
        if not (
            0 <= left < right <= marker.width // 8
            and 0 <= top < bottom <= marker.height // 8
            and target_tile >= 0
            and target_row_tiles >= right - left
        ):
            raise ValueError(f"{batch_path}: {record_id} has invalid tile geometry")

        for row in range(bottom - top):
            for column in range(right - left):
                destination_tile = target_tile + row * target_row_tiles + column
                if destination_tile >= tile_count or destination_tile in claimed_tiles:
                    raise ValueError(f"{batch_path}: {record_id} has an invalid OBJ target")
                source_x = (left + column) * 8
                source_y = (top + row) * 8
                packed = bytearray()
                for y in range(8):
                    row_start = (source_y + y) * marker.width + source_x
                    for x in range(0, 8, 2):
                        packed.append(
                            marker.indices[row_start + x]
                            | marker.indices[row_start + x + 1] << 4
                        )
                destination = destination_tile * 32
                rebuilt[destination : destination + 32] = packed
                claimed_tiles.add(destination_tile)
        record_ids.append(record_id)

    if len(rebuilt) != len(source):
        raise ValueError(f"{batch_path}: OBJ/PXL sync changed file size")
    return bytes(rebuilt), record_ids


def apply_obj_label_batch(
    batch_path: Path, source: bytes, arm9: bytes
) -> tuple[bytes, list[str]]:
    """Clean and redraw fixed OBJ labels with DK4's native ASCII bitmap font."""

    batch = load_batch_header(batch_path)
    if batch.get("format") != "dk4-obj-label-batch-v1":
        raise ValueError(f"{batch_path}: unsupported OBJ label format")
    if str(batch.get("source_file_sha256", "")).lower() != sha256(source):
        raise ValueError(f"{batch_path}: OBJ source SHA-256 mismatch")
    if len(source) % 32:
        raise ValueError(f"{batch_path}: OBJ bank is not composed of 32-byte 4bpp tiles")

    font = GameAsciiFont.from_arm9(arm9)
    if str(batch.get("font_sha256", "")).lower() != sha256(font.glyphs):
        raise ValueError(f"{batch_path}: ASCII font SHA-256 mismatch")
    records = batch.get("records")
    if not isinstance(records, list) or not records:
        raise ValueError(f"{batch_path}: OBJ label batch has no records")

    bank_width = int(batch.get("bank_width", 64))
    bank_height = int(batch.get("bank_height", 32))
    if bank_width % 8 or bank_height % 8:
        raise ValueError(f"{batch_path}: OBJ bank geometry must be 8x8-aligned")
    tiles_per_row = bank_width // 8
    tiles_per_bank = tiles_per_row * (bank_height // 8)
    tile_count = len(source) // 32

    def decode_region(start_tile: int) -> list[list[int]]:
        pixels = [[0] * bank_width for _ in range(bank_height)]
        for tile_y in range(bank_height // 8):
            for tile_x in range(tiles_per_row):
                tile = start_tile + tile_y * tiles_per_row + tile_x
                packed = source[tile * 32 : tile * 32 + 32]
                for y in range(8):
                    for pair, value in enumerate(packed[y * 4 : y * 4 + 4]):
                        x = tile_x * 8 + pair * 2
                        pixels[tile_y * 8 + y][x] = value & 0x0F
                        pixels[tile_y * 8 + y][x + 1] = value >> 4
        return pixels

    parsed: list[tuple[str, int, str]] = []
    seen_ids: set[str] = set()
    seen_regions: set[int] = set()
    for record in records:
        if not isinstance(record, dict):
            raise TypeError(f"{batch_path}: OBJ label record must be an object")
        record_id = str(record.get("id", ""))
        bank = int(record.get("bank", -1))
        start_tile = int(record.get("target_tile", bank * tiles_per_bank))
        text = str(record.get("text", ""))
        if not record_id or record_id in seen_ids:
            raise ValueError(f"{batch_path}: duplicate or missing OBJ label id")
        if (
            start_tile < 0
            or start_tile + tiles_per_bank > tile_count
            or start_tile in seen_regions
            or not text
        ):
            raise ValueError(f"{batch_path}: {record_id} has an invalid target")
        seen_ids.add(record_id)
        seen_regions.add(start_tile)
        parsed.append((record_id, start_tile, text))

    raw_box = batch.get("erase_box")
    if not isinstance(raw_box, list) or len(raw_box) != 4:
        raise ValueError(f"{batch_path}: OBJ label batch requires an erase box")
    left, top, right, bottom = (int(value) for value in raw_box)
    if not (0 <= left < right <= bank_width and 0 <= top < bottom <= bank_height):
        raise ValueError(f"{batch_path}: invalid OBJ label erase box")
    erase_index = int(batch.get("erase_index", 15))
    raw_erase_indices = batch.get("erase_indices", [erase_index])
    if not isinstance(raw_erase_indices, list) or not raw_erase_indices:
        raise ValueError(f"{batch_path}: OBJ erase_indices must be a nonempty list")
    erase_indices = {int(value) for value in raw_erase_indices}
    color_index = int(batch.get("color_index", 15))
    fallback_index = int(batch.get("background_fallback_index", 0))
    glyph_width = int(batch.get("glyph_width", 5))
    advance = int(batch.get("advance", glyph_width))
    text_y = int(batch.get("text_y", top))
    if not all(
        0 <= value <= 15 for value in erase_indices | {color_index, fallback_index}
    ):
        raise ValueError(f"{batch_path}: OBJ palette indices must be 0..15")
    if not (1 <= glyph_width <= 6 and advance >= glyph_width and text_y >= 0):
        raise ValueError(f"{batch_path}: invalid OBJ font geometry")

    pixels_by_bank = {start_tile: decode_region(start_tile) for _, start_tile, _ in parsed}
    background: dict[tuple[int, int], int] = {}
    for y in range(top, bottom):
        for x in range(left, right):
            candidates = [
                pixels[y][x]
                for pixels in pixels_by_bank.values()
                if pixels[y][x] not in erase_indices
            ]
            background[x, y] = (
                Counter(candidates).most_common(1)[0][0] if candidates else fallback_index
            )

    for _, start_tile, text in parsed:
        pixels = pixels_by_bank[start_tile]
        for (x, y), value in background.items():
            if pixels[y][x] in erase_indices:
                pixels[y][x] = value

        text_width = len(text) * advance
        text_x = (bank_width - text_width) // 2
        if text_x < left or text_x + text_width > right or text_y + 11 > bottom:
            raise ValueError(f"{batch_path}: label does not fit tile region {start_tile}: {text!r}")
        for index, character in enumerate(text):
            glyph = font.decode(character)
            bounds = glyph.getbbox()
            if bounds is not None and bounds[2] > glyph_width:
                raise ValueError(f"{batch_path}: cropped glyph in label {text!r}")
            glyph_pixels = glyph.load()
            for y in range(11):
                for x in range(glyph_width):
                    if glyph_pixels[x, y]:
                        pixels[text_y + y][text_x + index * advance + x] = color_index

    rebuilt = bytearray(source)
    for _, start_tile, _ in parsed:
        pixels = pixels_by_bank[start_tile]
        for tile_y in range(bank_height // 8):
            for tile_x in range(tiles_per_row):
                packed = bytearray()
                for y in range(8):
                    row = pixels[tile_y * 8 + y]
                    for x in range(0, 8, 2):
                        source_x = tile_x * 8 + x
                        packed.append(row[source_x] | row[source_x + 1] << 4)
                tile = start_tile + tile_y * tiles_per_row + tile_x
                rebuilt[tile * 32 : tile * 32 + 32] = packed

    return bytes(rebuilt), [record_id for record_id, _, _ in parsed]


def apply_pxl_native_label_batch(
    batch_path: Path, source: bytes, arm9: bytes
) -> tuple[bytes, list[str]]:
    """Redraw source-locked PXL labels with native or opt-in compact bitmap ink."""

    batch = load_batch_header(batch_path)
    if batch.get("format") != "dk4-pxl-native-label-batch-v1":
        raise ValueError(f"{batch_path}: unsupported native PXL label format")
    if str(batch.get("source_file_sha256", "")).lower() != sha256(source):
        raise ValueError(f"{batch_path}: PXL source SHA-256 mismatch")
    font = GameAsciiFont.from_arm9(arm9)
    if str(batch.get("font_sha256", "")).lower() != sha256(font.glyphs):
        raise ValueError(f"{batch_path}: ASCII font SHA-256 mismatch")

    image = PxlImage.from_bytes(source)
    records = batch.get("records")
    if not isinstance(records, list) or not records:
        raise ValueError(f"{batch_path}: native PXL label batch has no records")
    glyph_width = int(batch.get("glyph_width", 5))
    advance = int(batch.get("advance", glyph_width))
    color_index = int(batch.get("color_index", 1))
    erased = {int(value) for value in batch.get("erase_palette_indices", [color_index])}
    trim_top = int(batch.get("trim_blank_top_rows", 0))
    if not 0 <= trim_top < 11:
        raise ValueError(f"{batch_path}: invalid native font blank-row trim")
    glyph_height = 11 - trim_top
    if not (1 <= glyph_width <= 6 and advance >= glyph_width):
        raise ValueError(f"{batch_path}: invalid native PXL font geometry")
    if not all(0 <= value < len(image.palette) for value in erased | {color_index}):
        raise ValueError(f"{batch_path}: native PXL palette index is out of range")

    parsed: list[
        tuple[
            str,
            tuple[int, int, int, int],
            tuple[int, int, int, int],
            bytes | None,
            str,
            str,
            int,
            set[int],
            str,
            int,
        ]
    ] = []
    record_ids: list[str] = []
    for record in records:
        if not isinstance(record, dict):
            raise TypeError(f"{batch_path}: native PXL label record must be an object")
        record_id = str(record.get("id", ""))
        raw_box = record.get("box")
        raw_draw_box = record.get("draw_box", raw_box)
        raw_background = record.get("background_indices_zlib_hex")
        text = str(record.get("text", ""))
        glyph_spacing = str(record.get("glyph_spacing", "fixed"))
        row_color = int(record.get("color_index", color_index))
        row_erased = {int(value) for value in record.get("erase_palette_indices", erased)}
        font_face = str(record.get("font_face", "native-ascii"))
        word_space_width = int(record.get("compact_word_space_width", 2))
        if font_face != "native-ascii" and font_face not in COMPACT_FONT_IDENTITIES:
            raise ValueError(f"{batch_path}: unsupported bitmap font face")
        if font_face in COMPACT_FONT_IDENTITIES and (
            record.get("compact_font_sha256") != COMPACT_FONT_IDENTITIES[font_face]
            or glyph_spacing != "fixed"
        ):
            raise ValueError(f"{batch_path}: compact font identity or spacing differs")
        if font_face in COMPACT_FONT_IDENTITIES and word_space_width not in (1, 2, 3):
            raise ValueError(f"{batch_path}: invalid compact word space")
        if not all(0 <= value < len(image.palette) for value in row_erased | {row_color}):
            raise ValueError(f"{batch_path}: {record_id} native palette index is out of range")
        if glyph_spacing not in ("fixed", "native-ink-v1"):
            raise ValueError(f"{batch_path}: {record_id} has invalid native glyph spacing")
        if not record_id or record_id in record_ids or not text:
            raise ValueError(f"{batch_path}: duplicate or incomplete native PXL label")
        if not isinstance(raw_box, list) or len(raw_box) != 4:
            raise ValueError(f"{batch_path}: {record_id} requires a label box")
        if not isinstance(raw_draw_box, list) or len(raw_draw_box) != 4:
            raise ValueError(f"{batch_path}: {record_id} has an invalid draw box")
        left, top, right, bottom = (int(value) for value in raw_box)
        draw_left, draw_top, draw_right, draw_bottom = (
            int(value) for value in raw_draw_box
        )
        background = (
            zlib.decompress(bytes.fromhex(str(raw_background)))
            if raw_background is not None
            else None
        )
        if not (0 <= left < right <= image.width and 0 <= top < bottom <= image.height):
            raise ValueError(f"{batch_path}: {record_id} has an invalid label box")
        if not (
            left <= draw_left < draw_right <= right
            and top <= draw_top < draw_bottom <= bottom
        ):
            raise ValueError(f"{batch_path}: {record_id} draw box escapes its label box")
        if background is not None:
            expected_background_size = (right - left) * (bottom - top)
            if len(background) != expected_background_size:
                raise ValueError(
                    f"{batch_path}: {record_id} background has {len(background)} "
                    f"indices; expected {expected_background_size}"
                )
            if any(value >= len(image.palette) for value in background):
                raise ValueError(f"{batch_path}: {record_id} background index is invalid")
        parsed.append(
            (
                record_id,
                (left, top, right, bottom),
                (draw_left, draw_top, draw_right, draw_bottom),
                background,
                text,
                glyph_spacing,
                row_color,
                row_erased,
                font_face,
                word_space_width,
            )
        )
        record_ids.append(record_id)

    # Erase every old label before drawing any replacement. Some original
    # plaque boxes overlap by a few background-only rows.
    for _, (left, top, right, bottom), _, background, _, _, _, row_erased, _, _ in parsed:
        if background is not None:
            width = right - left
            for y in range(top, bottom):
                source_start = (y - top) * width
                destination_start = y * image.width + left
                image.indices[destination_start : destination_start + width] = background[
                    source_start : source_start + width
                ]
        else:
            image.erase_palette_indices((left, top, right, bottom), row_erased)

    drawn: list[tuple[int, int, int, int]] = []
    for record_id, _, (left, top, right, bottom), _, text, glyph_spacing, row_color, _, font_face, word_space_width in parsed:
        if font_face in COMPACT_FONT_IDENTITIES:
            mask, text_box, _ = compact_font_layout(
                text, (left, top, right, bottom), word_space_width=word_space_width,
                font_face=font_face,
            )
            if any(
                text_box[0] < old_right and text_box[2] > old_left
                and text_box[1] < old_bottom and text_box[3] > old_top
                for old_left, old_top, old_right, old_bottom in drawn
            ):
                raise ValueError(f"{batch_path}: {record_id} overlaps another rendered label")
            image._paste_mask((left, top, right, bottom), mask.convert("L"), row_color)
            drawn.append(text_box)
            continue
        glyphs = [font.decode(character) for character in text]
        offsets = []
        text_width = 0
        for character, glyph in zip(text, glyphs, strict=True):
            bounds = glyph.getbbox()
            if glyph_spacing == "native-ink-v1":
                # Remove blank side bearings, never ink. Thin native letters
                # retain every pixel, one clear separating column, and the
                # space retains three blank columns. Fixed labels stay exact.
                if bounds is None and character != " ":
                    raise ValueError(f"{batch_path}: unknown blank native glyph")
                offsets.append(text_width - bounds[0] if bounds else text_width)
                text_width += bounds[2] - bounds[0] + 1 if bounds else 3
            else:
                offsets.append(text_width)
                text_width += advance
        text_x = left + (right - left - text_width) // 2
        text_y = top + (bottom - top - glyph_height) // 2
        if text_x < left or text_x + text_width > right or text_y < top:
            raise ValueError(f"{batch_path}: label does not fit: {text!r}")
        text_box = (text_x, text_y, text_x + text_width, text_y + glyph_height)
        if any(
            text_box[0] < old_right
            and text_box[2] > old_left
            and text_box[1] < old_bottom
            and text_box[3] > old_top
            for old_left, old_top, old_right, old_bottom in drawn
        ):
            raise ValueError(f"{batch_path}: {record_id} overlaps another rendered label")
        for offset, glyph in zip(offsets, glyphs, strict=True):
            if trim_top:
                if glyph.crop((0, 0, 6, trim_top)).getbbox() is not None:
                    raise ValueError(f"{batch_path}: font trim would drop visible glyph pixels")
                glyph = glyph.crop((0, trim_top, 6, 11))
            bounds = glyph.getbbox()
            if bounds is not None and bounds[2] > glyph_width:
                raise ValueError(f"{batch_path}: cropped glyph in label {text!r}")
            glyph_pixels = glyph.load()
            for y in range(glyph_height):
                for x in range(glyph_width):
                    if glyph_pixels[x, y]:
                        image.indices[
                            (text_y + y) * image.width
                            + text_x
                            + offset
                            + x
                        ] = row_color
        drawn.append(text_box)

    rebuilt = image.to_bytes()
    if len(rebuilt) != len(source):
        raise ValueError(f"{batch_path}: native PXL labels changed file size")
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
    if not any(value in arm9 for value in REQUIRED_OPTIONS_TEXT):
        raise ValueError("required main-menu text missing: Opts or Options")

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
    profile_config = profiles.get(args.profile, {}) if args.profile else {}
    require_screen_layout = bool(
        isinstance(profile_config, dict)
        and profile_config.get("require_screen_entry_layout")
    )

    baseline = NdsImage.open(args.base)
    candidate = NdsImage.open(args.base)
    grouped: dict[str, list[Path]] = defaultdict(list)
    for batch_path in release_batches:
        header = load_batch_header(batch_path)
        try:
            validate_playable_dialogue_header(batch_path, header)
        except ValueError as error:
            raise SystemExit(str(error)) from None
        if require_screen_layout and header.get("format") == "dk4-ilnk-translation-batch-v1":
            records = header.get("records", [])
            has_raw_fixed_text = isinstance(records, list) and any(
                isinstance(record, dict) and bool(record.get("replacement_hex"))
                for record in records
            )
            if has_raw_fixed_text and header.get("fixed_allocation_policy") != "screen-entry-layout-v1":
                raise SystemExit(
                    f"{batch_path}: profile requires screen-entry-layout-v1 for "
                    "every raw fixed-allocation COMMON batch"
                )
        file_path = str(header.get("file_path", ""))
        if not file_path.startswith("/"):
            raise SystemExit(f"{batch_path}: invalid internal file path")
        grouped[file_path].append(batch_path)

    changed_records: dict[str, list[str]] = {}
    relocation_checks: dict[str, object] = {}
    for file_path, file_batch_paths in order_graphics_sync_groups(grouped):
        source = candidate.read_file(file_path)
        for batch_path in file_batch_paths:
            try:
                batch_header = load_batch_header(batch_path)
                validate_ascii_guard_policy(batch_path, batch_header)
                validate_fixed_text_layout_policy(batch_path, batch_header)
                validate_fixed_allocation_policy(batch_path, batch_header)
            except (TypeError, ValueError) as error:
                raise SystemExit(str(error)) from None
        formats = {str(load_batch_header(path).get("format", "")) for path in file_batch_paths}
        if formats == {'dk4-ilnk-indexed-region-batch-v1'}:
            if len(file_batch_paths) != 1:
                raise SystemExit('Exactly one indexed ILNK artwork batch is allowed')
            rebuilt, record_ids = apply_ilnk_indexed_region_batch(file_batch_paths[0], source)
            if rebuilt == source:
                raise SystemExit('Indexed ILNK artwork made no changes')
            candidate.replace_file(file_path, rebuilt)
            changed_records[file_path] = record_ids
            continue
        if formats == {'dk4-pxl-indexed-region-batch-v1'}:
            if len(file_batch_paths) != 1:
                raise SystemExit('Exactly one indexed PXL artwork batch is allowed')
            rebuilt, record_ids = apply_pxl_indexed_region_batch(file_batch_paths[0], source)
            if rebuilt == source:
                raise SystemExit('Indexed PXL artwork made no changes')
            candidate.replace_file(file_path, rebuilt)
            changed_records[file_path] = record_ids
            continue
        if formats == {'dk4-fls-indexed-region-batch-v1'}:
            if len(file_batch_paths) != 1:
                raise SystemExit('Exactly one indexed FLS artwork batch is allowed')
            rebuilt, record_ids = apply_fls_indexed_region_batch(file_batch_paths[0], source)
            if rebuilt == source:
                raise SystemExit('Indexed FLS artwork made no changes')
            candidate.replace_file(file_path, rebuilt)
            changed_records[file_path] = record_ids
            continue
        if formats == {"dk4-fls-label-batch-v1"}:
            if len(file_batch_paths) != 1:
                raise SystemExit(f"{file_path}: exactly one FLS label batch is allowed")
            rebuilt, record_ids = apply_fls_label_batch(file_batch_paths[0], source)
            if rebuilt == source:
                raise SystemExit(f"{file_path}: FLS label batch made no changes")
            candidate.replace_file(file_path, rebuilt)
            changed_records[file_path] = record_ids
            continue
        if formats == {"dk4-pxl-label-batch-v1"}:
            rebuilt, record_ids = apply_pxl_label_batches(file_batch_paths, source)
            if rebuilt == source:
                raise SystemExit(f"{file_path}: PXL label batch made no changes")
            candidate.replace_file(file_path, rebuilt)
            changed_records[file_path] = record_ids
            continue
        if RAW_BGR555_ART_FORMAT in formats:
            references = {str(load_batch_header(p)["source_image_path"]): candidate.read_file(str(load_batch_header(p)["source_image_path"]))
                          for p in file_batch_paths if load_batch_header(p).get("format") == "dk4-ilnk-pxl-sync-v1"}
            rebuilt, record_ids = apply_ilnk_mixed_art_batches(file_batch_paths, source, references)
            if rebuilt == source:
                raise SystemExit("Mixed raw ILNK artwork made no changes")
            candidate.replace_file(file_path, rebuilt)
            changed_records[file_path] = record_ids
            continue
        if formats == {"dk4-ilnk-pxl-sync-v1"}:
            reference_paths = [str(load_batch_header(path).get("source_image_path", ""))
                               for path in file_batch_paths]
            if any(not path.startswith("/") for path in reference_paths):
                raise SystemExit(f"{file_path}: invalid reference PXL path")
            rebuilt, record_ids = apply_ilnk_pxl_sync_batches(
                file_batch_paths, source, {path: candidate.read_file(path) for path in reference_paths}
            )
            if rebuilt == source:
                raise SystemExit(f"{file_path}: ILNK/PXL sync made no changes")
            candidate.replace_file(file_path, rebuilt)
            changed_records[file_path] = record_ids
            continue
        if formats == {OBJ_BANKED_SYNC_FORMAT}:
            if len(file_batch_paths) != 1:
                raise SystemExit(f"{file_path}: exactly one banked OBJ sync batch is allowed")
            header = load_batch_header(file_batch_paths[0])
            reference_path = str(header.get("source_image_path", ""))
            if not reference_path.startswith("/"):
                raise SystemExit("Invalid banked OBJ reference path")
            rebuilt, record_ids = apply_banked_sync(header, source, candidate.read_file(reference_path))
            if rebuilt == source:
                raise SystemExit("Banked OBJ sync made no changes")
            candidate.replace_file(file_path, rebuilt)
            changed_records[file_path] = record_ids
            continue
        if formats == {"dk4-obj-tile-pxl-sync-v1"}:
            if len(file_batch_paths) != 1:
                raise SystemExit(f"{file_path}: exactly one OBJ/PXL sync batch is allowed")
            batch_path = file_batch_paths[0]
            header = load_batch_header(batch_path)
            reference_path = str(header.get("source_image_path", ""))
            if not reference_path.startswith("/"):
                raise SystemExit(f"{batch_path}: invalid reference PXL path")
            rebuilt, record_ids = apply_obj_tile_pxl_sync_batch(
                batch_path, source, candidate.read_file(reference_path)
            )
            if rebuilt == source:
                raise SystemExit(f"{file_path}: OBJ/PXL sync made no changes")
            candidate.replace_file(file_path, rebuilt)
            changed_records[file_path] = record_ids
            continue
        if formats == {"dk4-obj-label-batch-v1"}:
            if len(file_batch_paths) != 1:
                raise SystemExit(f"{file_path}: exactly one OBJ label batch is allowed")
            batch_path = file_batch_paths[0]
            header = load_batch_header(batch_path)
            font_path = str(header.get("font_file_path", ""))
            if font_path != "/__arm9__.bin":
                raise SystemExit(f"{batch_path}: invalid OBJ label font path")
            rebuilt, record_ids = apply_obj_label_batch(
                batch_path, source, candidate.read_file(font_path)
            )
            if rebuilt == source:
                raise SystemExit(f"{file_path}: OBJ label batch made no changes")
            candidate.replace_file(file_path, rebuilt)
            changed_records[file_path] = record_ids
            continue
        if formats == {"dk4-pxl-native-label-batch-v1"}:
            if len(file_batch_paths) != 1:
                raise SystemExit(f"{file_path}: exactly one native PXL batch is allowed")
            batch_path = file_batch_paths[0]
            header = load_batch_header(batch_path)
            font_path = str(header.get("font_file_path", ""))
            if font_path != "/__arm9__.bin":
                raise SystemExit(f"{batch_path}: invalid native PXL font path")
            rebuilt, record_ids = apply_pxl_native_label_batch(
                batch_path, source, candidate.read_file(font_path)
            )
            if rebuilt == source:
                raise SystemExit(f"{file_path}: native PXL batch made no changes")
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
            allowed_lil_b22_profiles = {
                "lil-b22-first-screen-probe",
                "lil-b22-intro-probe",
                "lil-b22-intro-shared-data-v2",
                "lil-b22-intro-guild-inn-v3",
                "lil-b22-intro-guild-inn-v4",
                "lil-b22-intro-all-items-v5",
                "lil-hodram-unified-v1",
                "main-menu-birthday-v1",
                "main-menu-character-crew-wrap-v2",
                "main-menu-character-square-repair-v3",
                "main-menu-character-placeholder-cleanup-v4",
                "main-menu-character-placeholder-english-v5",
            }
            if args.profile not in allowed_lil_b22_profiles:
                raise SystemExit(
                    "SC2 block 22 is blocked: its portrait/name control preamble is unmapped. "
                    "Use only a named source-locked Lil B22 research probe until that "
                    "format is documented."
                )
            if len(file_batch_paths) != 1 or not bool(
                load_batch_header(file_batch_paths[0]).get("research_only")
            ):
                raise SystemExit(
                    "Lil B22 probes require exactly one research-only batch"
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

    common_reblock = profile_config.get("common_native_reblocking")
    if common_reblock:
        common_path, arm9_path = "/COMMON/MESFILE.DK4", "/__arm9__.bin"
        reblocked, mapped_arm9, reblock_report = apply_common_reblocking(
            candidate.read_file(common_path), candidate.read_file(arm9_path), Path(common_reblock)
        )
        candidate.replace_file(common_path, reblocked)
        candidate.replace_file(arm9_path, mapped_arm9)
        relocation_checks[common_path] = reblock_report
        changed_records[common_path].extend(
            f"COMMON_NATIVE_MESSAGE_{i}" for i in reblock_report["authored_ids"]
        )
        changed_records[arm9_path].append("COMMON_NATIVE_REBLOCK_DIRECTORY_AND_OFFSETS")

    caption_release = profile_config.get("scene_caption_release")
    if caption_release:
        if not common_reblock:
            raise ValueError("Complete captions require the preceding COMMON rebuild")
        from dk4tool.patch.scene_caption_release import apply_release as apply_scene_captions

        arm9_path = "/__arm9__.bin"
        caption_arm9, caption_report = apply_scene_captions(candidate.read_file(arm9_path), Path(caption_release))
        candidate.replace_file(arm9_path, caption_arm9)
        caption_report["release_config"] = str(caption_release)
        caption_report["release_config_sha256"] = sha256(Path(caption_release).read_bytes())
        relocation_checks[arm9_path] = caption_report
        changed_records[arm9_path].extend(
            f"SCENE_CAPTION_ROUTE_{route}_{index:02d}"
            for route, count in enumerate((46, 41, 39, 38)) for index in range(count)
        )
        changed_records[arm9_path].append("SCENE_CAPTION_NATIVE_TRACKING_CLASS_DISPATCH_AND_GUARDED_POOL")

    golden_viewer_release = profile_config.get("golden_route_viewer_release")
    if golden_viewer_release:
        if not caption_release:
            raise ValueError("Complete Golden Route viewer requires the preceding caption release")
        from dk4tool.patch.golden_route_viewer_release import apply_release as apply_golden_viewer

        arm9_path = "/__arm9__.bin"
        golden_arm9, golden_report = apply_golden_viewer(candidate.read_file(arm9_path), Path(golden_viewer_release))
        candidate.replace_file(arm9_path, golden_arm9)
        golden_report["release_config"] = str(golden_viewer_release)
        golden_report["release_config_sha256"] = sha256(Path(golden_viewer_release).read_bytes())
        relocation_checks[arm9_path]["golden_route_viewer"] = golden_report
        changed_records[arm9_path].extend(
            f"GOLDEN_ROUTE_VIEWER_{key}" for key in ("PREVIOUS", "NEXT", "SWITCH", "FOUND", "RECORDS", "EMPTY")
        )

    map_tooltip_release = profile_config.get("map_tooltip_release")
    if map_tooltip_release:
        if not golden_viewer_release:
            raise ValueError("Complete map tooltips require the preceding Golden Route viewer release")
        from dk4tool.patch.map_tooltip_release import apply_release as apply_map_tooltips

        arm9_path = "/__arm9__.bin"
        tooltip_arm9, tooltip_report = apply_map_tooltips(candidate.read_file(arm9_path), Path(map_tooltip_release))
        candidate.replace_file(arm9_path, tooltip_arm9)
        tooltip_report["release_config"] = str(map_tooltip_release)
        tooltip_report["release_config_sha256"] = sha256(Path(map_tooltip_release).read_bytes())
        relocation_checks[arm9_path]["map_tooltips"] = tooltip_report
        changed_records[arm9_path].extend(
            ["MAP_ENTITY_TOOLTIP_" + key for key in ("PIRATES", "MONSTER", "UNKNOWN", "CLASS", "ARMAMENT")]
            + ["MAP_CREATURE_CLASS_" + str(index) for index in range(34, 38)]
            + ["MAP_TOOLTIP_SHARED_POOL_AND_GOLDEN_ROUTE_HEADING_TABLE_RELOCATION"]
        )

    blizzard_release = profile_config.get("common_blizzard_release")
    if blizzard_release:
        if not map_tooltip_release:
            raise ValueError("Blizzard repair requires the complete preceding V140 stack")
        from dk4tool.patch.common_blizzard_release import apply_release as apply_blizzard

        common_path, arm9_path = "/COMMON/MESFILE.DK4", "/__arm9__.bin"
        repaired_common, repaired_arm9, repair_report = apply_blizzard(
            candidate.read_file(common_path), candidate.read_file(arm9_path), Path(blizzard_release)
        )
        candidate.replace_file(common_path, repaired_common)
        candidate.replace_file(arm9_path, repaired_arm9)
        repair_report["release_config"] = str(blizzard_release)
        repair_report["release_config_sha256"] = sha256(Path(blizzard_release).read_bytes())
        relocation_checks[common_path]["blizzard_repair"] = repair_report
        changed_records[common_path].extend(["COMMON_MESSAGE_" + str(i) for i in repair_report["authored_ids"]])
        changed_records[arm9_path].extend(["BLIZZARD_NATIVE_OFFSET_" + str(i) for i in repair_report["changed_offsets"]])

    placeholder_release = profile_config.get("common_placeholder_release")
    if placeholder_release:
        if not blizzard_release:
            raise ValueError("Placeholder repair requires the complete preceding V141 stack")
        from dk4tool.patch.common_placeholder_release import apply_release as apply_placeholders

        common_path, arm9_path = "/COMMON/MESFILE.DK4", "/__arm9__.bin"
        repaired_common, repaired_arm9, repair_report = apply_placeholders(
            candidate.read_file(common_path), candidate.read_file(arm9_path), Path(placeholder_release)
        )
        candidate.replace_file(common_path, repaired_common)
        candidate.replace_file(arm9_path, repaired_arm9)
        repair_report["release_config"] = str(placeholder_release)
        repair_report["release_config_sha256"] = sha256(Path(placeholder_release).read_bytes())
        relocation_checks[common_path]["placeholder_repair"] = repair_report
        changed_records[common_path].extend(["COMMON_MESSAGE_" + str(i) for i in repair_report["authored_ids"]])
        changed_records[arm9_path].extend(["PLACEHOLDER_NATIVE_OFFSET_" + str(i) for i in repair_report["changed_offsets"]])

    tribute_release = profile_config.get("common_tribute_release")
    if tribute_release:
        if not placeholder_release:
            raise ValueError("Tribute repair requires the complete preceding V142 stack")
        from dk4tool.patch.common_tribute_release import apply_release as apply_tribute

        common_path, arm9_path = "/COMMON/MESFILE.DK4", "/__arm9__.bin"
        repaired_common, repaired_arm9, repair_report = apply_tribute(
            candidate.read_file(common_path), candidate.read_file(arm9_path), Path(tribute_release)
        )
        candidate.replace_file(common_path, repaired_common)
        candidate.replace_file(arm9_path, repaired_arm9)
        repair_report["release_config"] = str(tribute_release)
        repair_report["release_config_sha256"] = sha256(Path(tribute_release).read_bytes())
        relocation_checks[common_path]["tribute_repair"] = repair_report
        changed_records[common_path].extend(["COMMON_MESSAGE_" + str(i) for i in repair_report["authored_ids"]])
        changed_records[arm9_path].extend(["TRIBUTE_NATIVE_OFFSET_" + str(i) for i in repair_report["changed_offsets"]])
        changed_records[arm9_path].extend(["TRIBUTE_RUNTIME_NAME_HOOK", "TRIBUTE_RUNTIME_TOWN_WRAP",
                                           "TRIBUTE_RUNTIME_MONTHLY_WRAP", "TRIBUTE_RESIDENT_ARENA_RESERVATION"])

    options_narrow_release = profile_config.get("options_narrow_release")
    if options_narrow_release:
        if not tribute_release:
            raise ValueError("Narrow Options requires complete V143 tribute stack")
        from dk4tool.patch.options_narrow_release import apply_release as apply_options_narrow

        arm9_path = "/__arm9__.bin"
        repaired_arm9, options_report = apply_options_narrow(candidate.read_file(arm9_path), Path(options_narrow_release))
        candidate.replace_file(arm9_path, repaired_arm9)
        options_report["release_config"] = str(options_narrow_release)
        options_report["release_config_sha256"] = sha256(Path(options_narrow_release).read_bytes())
        relocation_checks[arm9_path]["options_narrow"] = options_report
        changed_records[arm9_path].extend(["OPTIONS_NARROW_" + str(at) for at in options_report["authored_offsets"]])

    damaged_save_release = profile_config.get("damaged_save_release")
    if damaged_save_release:
        if not options_narrow_release:
            raise ValueError("Damaged-save release requires complete V144 Options stack")
        from dk4tool.patch.damaged_save_release import apply_release as apply_damaged_save

        arm9_path = "/__arm9__.bin"
        repaired_arm9, damaged_report = apply_damaged_save(candidate.read_file(arm9_path), damaged_save_release)
        candidate.replace_file(arm9_path, repaired_arm9)
        damaged_report["release_config"] = damaged_save_release
        damaged_report["release_config_sha256"] = sha256(Path(damaged_save_release).read_bytes())
        relocation_checks[arm9_path]["damaged_save"] = damaged_report
        changed_records[arm9_path].append("DAMAGED_SAVE_MESSAGE_SUFFIX")

    deck_explanation_release = profile_config.get("deck_explanation_release")
    if deck_explanation_release:
        if not damaged_save_release:
            raise ValueError("Deck explanations require complete V145 damaged-save stack")
        from dk4tool.patch.deck_explanation_release import apply_release as apply_deck_explanations

        arm9_path = "/__arm9__.bin"
        repaired_arm9, deck_report = apply_deck_explanations(candidate.read_file(arm9_path), deck_explanation_release)
        candidate.replace_file(arm9_path, repaired_arm9)
        deck_report["release_config"] = deck_explanation_release
        deck_report["release_config_sha256"] = sha256(Path(deck_explanation_release).read_bytes())
        relocation_checks[arm9_path]["deck_explanations"] = deck_report
        changed_records[arm9_path].extend(["DECK_EXPLANATION_" + str(at) for at in deck_report["authored_offsets"]])
        changed_records[arm9_path].append("DECK_EXPLANATION_POOL_RELOCATION")

    available_companions_release = profile_config.get("available_companions_release")
    if available_companions_release:
        if not deck_explanation_release:
            raise ValueError("Companion message requires complete V146 Deck stack")
        from dk4tool.patch.available_companions_release import apply_release as apply_companions

        arm9_path = "/__arm9__.bin"
        repaired_arm9, companion_report = apply_companions(candidate.read_file(arm9_path), available_companions_release)
        candidate.replace_file(arm9_path, repaired_arm9)
        companion_report["release_config"] = available_companions_release
        companion_report["release_config_sha256"] = sha256(Path(available_companions_release).read_bytes())
        relocation_checks[arm9_path]["available_companions"] = companion_report
        changed_records[arm9_path].append("AVAILABLE_COMPANIONS_POOL_RELOCATION")

    persistent_name_release = profile_config.get("persistent_name_release")
    if persistent_name_release:
        if not available_companions_release:
            raise ValueError("Persistent names require the complete V147 stack")
        from dk4tool.patch.persistent_name_release import apply_release as apply_persistent_names

        arm9_path = "/__arm9__.bin"
        repaired_arm9, name_report = apply_persistent_names(candidate.read_file(arm9_path), persistent_name_release)
        candidate.replace_file(arm9_path, repaired_arm9)
        name_report["release_config"] = persistent_name_release
        name_report["release_config_sha256"] = sha256(Path(persistent_name_release).read_bytes())
        relocation_checks[arm9_path]["persistent_names"] = name_report
        changed_records[arm9_path].append("PERSISTENT_NAME_SECTION_AND_COMPLETE_SHOPKEEPER_NAMES")

    fleet_name_release = profile_config.get("fleet_name_release")
    if fleet_name_release:
        if not persistent_name_release:
            raise ValueError("Fleet labels require the complete V148 persistent-name stack")
        from dk4tool.patch.fleet_name_release import apply_release as apply_fleet_names

        arm9_path = "/__arm9__.bin"
        repaired_arm9, fleet_report = apply_fleet_names(candidate.read_file(arm9_path), fleet_name_release)
        candidate.replace_file(arm9_path, repaired_arm9)
        fleet_report["release_config"] = fleet_name_release
        fleet_report["release_config_sha256"] = sha256(Path(fleet_name_release).read_bytes())
        relocation_checks[arm9_path]["fleet_names"] = fleet_report
        changed_records[arm9_path].extend(["FLEET_NAME_PIRATE", "FLEET_NAME_UNIDENTIFIED"])

    residual_character_names_release = profile_config.get("residual_character_names_release")
    if residual_character_names_release:
        if not fleet_name_release:
            raise ValueError("Residual character names require the complete V149 fleet-label stack")
        from dk4tool.patch.residual_character_name_release import (
            apply_release as apply_residual_names,
        )

        arm9_path = "/__arm9__.bin"
        repaired_arm9, residual_report = apply_residual_names(candidate.read_file(arm9_path), residual_character_names_release)
        candidate.replace_file(arm9_path, repaired_arm9)
        residual_report["release_config"] = residual_character_names_release
        residual_report["release_config_sha256"] = sha256(Path(residual_character_names_release).read_bytes())
        relocation_checks[arm9_path]["residual_character_names"] = residual_report
        changed_records[arm9_path].extend(["ORDINARY_GIVEN_NAME_61", "ORDINARY_GIVEN_NAME_77"])

    persistent_name_boot_release = profile_config.get("persistent_name_boot_release")
    if persistent_name_boot_release:
        if not residual_character_names_release:
            raise ValueError("Staged boot repair requires the complete V150 translation stack")
        from dk4tool.patch.persistent_name_boot_release import apply_release as apply_name_boot

        arm9_path = "/__arm9__.bin"
        repaired_arm9, boot_report = apply_name_boot(
            candidate.read_file(arm9_path), persistent_name_boot_release,
            bytes(candidate.rom.arm7), candidate.rom.arm7RamAddress)
        candidate.replace_file(arm9_path, repaired_arm9)
        boot_report["release_config"] = persistent_name_boot_release
        boot_report["release_config_sha256"] = sha256(Path(persistent_name_boot_release).read_bytes())
        relocation_checks[arm9_path]["persistent_name_boot"] = boot_report
        changed_records[arm9_path].append("PERSISTENT_NAME_STAGED_BOOT_COPY")

    common_copy_alignment_release = profile_config.get("common_copy_alignment_release")
    if common_copy_alignment_release:
        if not persistent_name_boot_release:
            raise ValueError("Shared copy repair requires the complete staged V151 stack")
        from dk4tool.patch.common_copy_alignment_release import (
            apply_release as apply_copy_alignment,
        )

        arm9_path = "/__arm9__.bin"
        repaired_arm9, copy_report = apply_copy_alignment(
            candidate.read_file(arm9_path), common_copy_alignment_release)
        candidate.replace_file(arm9_path, repaired_arm9)
        copy_report["release_config"] = common_copy_alignment_release
        copy_report["release_config_sha256"] = sha256(Path(common_copy_alignment_release).read_bytes())
        relocation_checks[arm9_path]["common_copy_alignment"] = copy_report
        changed_records[arm9_path].append("SHARED_COPY_ARM946_ALIGNMENT_GUARD")

    raphael_system_panel_release = profile_config.get("raphael_system_panel_release")
    if raphael_system_panel_release:
        if not common_copy_alignment_release:
            raise ValueError("Tutorial repair requires the complete shared-copy repair stack")
        from dk4tool.patch.raphael_system_panel_release import PATH as panel_path
        from dk4tool.patch.raphael_system_panel_release import apply_release as apply_system_panels

        clean_reference = NdsImage.open("work/clean.nds")
        repaired_panels, panel_report = apply_system_panels(
            candidate.read_file(panel_path), baseline.read_file(panel_path),
            clean_reference.read_file(panel_path), raphael_system_panel_release)
        candidate.replace_file(panel_path, repaired_panels)
        panel_report["release_config"] = raphael_system_panel_release
        panel_report["release_config_sha256"] = sha256(Path(raphael_system_panel_release).read_bytes())
        relocation_checks.setdefault(panel_path, {})["system_panels"] = panel_report
        changed_records[panel_path].extend(panel_report["changed_records"])

    ordinary_name_fidelity_release = profile_config.get("ordinary_name_fidelity_release")
    if ordinary_name_fidelity_release:
        if not raphael_system_panel_release:
            raise ValueError("Name fidelity corrections require the complete V153 repair stack")
        from dk4tool.patch.ordinary_name_fidelity_release import (
            apply_release as apply_name_fidelity,
        )

        arm9_path = "/__arm9__.bin"
        repaired_names, name_report = apply_name_fidelity(
            candidate.read_file(arm9_path), NdsImage.open("work/clean.nds").read_file(arm9_path),
            ordinary_name_fidelity_release)
        candidate.replace_file(arm9_path, repaired_names)
        name_report["release_config"] = ordinary_name_fidelity_release
        name_report["release_config_sha256"] = sha256(Path(ordinary_name_fidelity_release).read_bytes())
        relocation_checks[arm9_path]["ordinary_name_fidelity"] = name_report
        changed_records[arm9_path].extend(name_report["changed_records"])

    village_release = profile_config.get("village_promised_words_release")
    if village_release:
        if not ordinary_name_fidelity_release:
            raise ValueError("Village localization requires the complete V154 stack")
        from dk4tool.patch.village_promised_words_release import apply_release as apply_village

        arm9_path = "/__arm9__.bin"
        village_arm9, village_report = apply_village(
            candidate, NdsImage.open("work/clean.nds").read_file(arm9_path), village_release)
        candidate.replace_file(arm9_path, village_arm9)
        village_report["release_config"] = village_release
        village_report["release_config_sha256"] = sha256(Path(village_release).read_bytes())
        relocation_checks[arm9_path]["village_promised_words"] = village_report
        changed_records[arm9_path].extend(village_report["changed_records"])

    movement_release = profile_config.get("movement_notice_release")
    if movement_release:
        if not village_release:
            raise ValueError("Movement localization requires the complete V155 stack")
        from dk4tool.patch.movement_notice_release import apply_release as apply_movement

        arm9_path, common_path = "/__arm9__.bin", "/COMMON/MESFILE.DK4"
        movement_arm9, movement_common, movement_report = apply_movement(
            candidate, NdsImage.open("work/clean.nds"), movement_release)
        candidate.replace_file(arm9_path, movement_arm9)
        candidate.replace_file(common_path, movement_common)
        movement_report["release_config"] = movement_release
        movement_report["release_config_sha256"] = sha256(Path(movement_release).read_bytes())
        relocation_checks[arm9_path]["movement_notices"] = movement_report
        changed_records[arm9_path].extend(movement_report["arm9_changed_records"])
        changed_records[common_path].extend(
            "COMMON_MESSAGE_" + str(mid) for mid in movement_report["common_changed_ids"])

    duel_release = profile_config.get("swordsmanship_status_release")
    if duel_release:
        if not movement_release:
            raise ValueError("Duel localization requires the complete V156 stack")
        from dk4tool.patch.swordsmanship_status_release import apply_release as apply_duel

        arm9_path = "/__arm9__.bin"
        duel_arm9, duel_report = apply_duel(candidate, NdsImage.open("work/clean.nds"), duel_release)
        candidate.replace_file(arm9_path, duel_arm9)
        duel_report["release_config"] = duel_release
        duel_report["release_config_sha256"] = sha256(Path(duel_release).read_bytes())
        relocation_checks[arm9_path]["swordsmanship_status"] = duel_report
        changed_records[arm9_path].extend(duel_report["changed_records"])

    gallery_release = profile_config.get("gallery_description_release")
    if gallery_release:
        if not duel_release:
            raise ValueError("Gallery localization requires the complete V157 stack")
        from dk4tool.patch.gallery_description_release import apply_release as apply_gallery

        arm9_path = "/__arm9__.bin"
        gallery_arm9, gallery_report = apply_gallery(candidate, NdsImage.open("work/clean.nds"), gallery_release)
        candidate.replace_file(arm9_path, gallery_arm9)
        gallery_report["release_config"] = gallery_release
        gallery_report["release_config_sha256"] = sha256(Path(gallery_release).read_bytes())
        relocation_checks[arm9_path]["gallery_descriptions"] = gallery_report
        changed_records[arm9_path].extend(gallery_report["changed_records"])

    item_release = profile_config.get("item_interface_release")
    if item_release:
        if not gallery_release:
            raise ValueError("Item localization requires the complete V158 stack")
        from dk4tool.patch.item_interface_release import apply_release as apply_items

        arm9_path = "/__arm9__.bin"
        item_arm9, item_report = apply_items(candidate, NdsImage.open("work/clean.nds"), item_release)
        candidate.replace_file(arm9_path, item_arm9)
        item_report["release_config"] = item_release
        item_report["release_config_sha256"] = sha256(Path(item_release).read_bytes())
        relocation_checks[arm9_path]["item_interface"] = item_report
        changed_records[arm9_path].extend(item_report["changed_records"])

    online_banner_release = profile_config.get("online_title_banner_release")
    if online_banner_release:
        if not item_release:
            raise ValueError("Online banner correction requires the complete current integration stack")
        from dk4tool.patch.online_title_banner_release import apply_release as apply_online_banner

        arm9_path = "/__arm9__.bin"
        banner_arm9, banner_report = apply_online_banner(
            candidate.read_file(arm9_path), baseline.read_file(arm9_path), online_banner_release)
        candidate.replace_file(arm9_path, banner_arm9)
        banner_report["release_config"] = online_banner_release
        banner_report["release_config_sha256"] = sha256(Path(online_banner_release).read_bytes())
        relocation_checks[arm9_path]["online_title_banner"] = banner_report
        changed_records[arm9_path].extend(banner_report["changed_records"])

    sailing_graphics_release = profile_config.get("sailing_panel_graphics_release")
    if sailing_graphics_release is not None:
        if not online_banner_release:
            raise ValueError("Sailing graphics requires the complete V211 stack")
        from dk4tool.patch.sailing_panel_graphics import apply_release as apply_sailing_graphics

        arm9_path = "/__arm9__.bin"
        sailing_arm9, sailing_report = apply_sailing_graphics(
            candidate.read_file(arm9_path), baseline.read_file(arm9_path), sailing_graphics_release)
        candidate.replace_file(arm9_path, sailing_arm9)
        sailing_report["release_config"] = sailing_graphics_release
        sailing_report["release_config_sha256"] = sha256(Path(sailing_graphics_release).read_bytes())
        relocation_checks[arm9_path]["sailing_panel_graphics"] = sailing_report
        changed_records[arm9_path].extend(sailing_report["changed_records"])

    sailing_no_target_release = profile_config.get("sailing_no_target_release")
    if sailing_no_target_release is not None:
        if not sailing_graphics_release:
            raise ValueError("No-target graphics requires the complete V217 sailing stack")
        from dk4tool.patch.sailing_no_target import apply_release as apply_no_target

        arm9_path = "/__arm9__.bin"
        notice_arm9, notice_report = apply_no_target(
            candidate.read_file(arm9_path), baseline.read_file(arm9_path), sailing_no_target_release)
        candidate.replace_file(arm9_path, notice_arm9)
        notice_report["release_config"] = sailing_no_target_release
        notice_report["release_config_sha256"] = sha256(Path(sailing_no_target_release).read_bytes())
        relocation_checks[arm9_path]["sailing_no_target"] = notice_report
        changed_records[arm9_path].extend(notice_report["changed_records"])

    navigator_popup_release = profile_config.get("navigator_selection_menu_release")
    if navigator_popup_release is not None:
        if not sailing_no_target_release:
            raise ValueError("Navigator popup localization requires the complete V218 stack")
        from dk4tool.patch.navigator_selection_menu import apply_release as apply_navigator_popup

        arm9_path = "/__arm9__.bin"
        popup_arm9, popup_report = apply_navigator_popup(
            candidate.read_file(arm9_path), baseline.read_file(arm9_path), navigator_popup_release)
        candidate.replace_file(arm9_path, popup_arm9)
        popup_report["release_config"] = navigator_popup_release
        popup_report["release_config_sha256"] = sha256(Path(navigator_popup_release).read_bytes())
        relocation_checks[arm9_path]["navigator_selection_menu"] = popup_report
        changed_records[arm9_path].extend(popup_report["changed_records"])

    two_screen_layout_release = profile_config.get("two_screen_layout_release")
    if two_screen_layout_release is not None:
        if not navigator_popup_release:
            raise ValueError("Two-screen layout requires the complete V245 runtime stack")
        from dk4tool.patch.two_screen_layout import apply_release as apply_two_screen_layout

        arm9_path = "/__arm9__.bin"
        layout_arm9, layout_report = apply_two_screen_layout(
            candidate.read_file(arm9_path), baseline.read_file(arm9_path), two_screen_layout_release)
        candidate.replace_file(arm9_path, layout_arm9)
        layout_report["release_config"] = two_screen_layout_release
        layout_report["release_config_sha256"] = sha256(Path(two_screen_layout_release).read_bytes())
        relocation_checks[arm9_path]["two_screen_layout"] = layout_report
        changed_records[arm9_path].extend(layout_report["changed_records"])

    plaque_style_release = profile_config.get("plaque_style_release")
    if plaque_style_release is not None:
        if not two_screen_layout_release:
            raise ValueError("Plaque style requires the complete V246 layout")
        from dk4tool.patch.plaque_style import apply_release as apply_plaque_style

        arm9_path = "/__arm9__.bin"
        styled_arm9, style_report = apply_plaque_style(
            candidate.read_file(arm9_path), plaque_style_release)
        candidate.replace_file(arm9_path, styled_arm9)
        style_report["release_config"] = plaque_style_release
        style_report["release_config_sha256"] = sha256(Path(plaque_style_release).read_bytes())
        relocation_checks[arm9_path]["plaque_style"] = style_report
        changed_records[arm9_path].extend(style_report["changed_records"])

    short_equipment_paper_release = profile_config.get("short_equipment_paper_release")
    if short_equipment_paper_release is not None:
        if not plaque_style_release:
            raise ValueError("Short equipment paper requires the complete V251 stack")
        from dk4tool.patch.short_equipment_paper import apply_release as apply_short_equipment_paper

        arm9_path = "/__arm9__.bin"
        styled_arm9, short_report = apply_short_equipment_paper(
            candidate.read_file(arm9_path), short_equipment_paper_release)
        candidate.replace_file(arm9_path, styled_arm9)
        short_report["release_config"] = short_equipment_paper_release
        short_report["release_config_sha256"] = sha256(Path(short_equipment_paper_release).read_bytes())
        relocation_checks[arm9_path]["short_equipment_paper"] = short_report
        changed_records[arm9_path].extend(short_report["changed_records"])

    square_shop_labels_release = profile_config.get("square_shop_labels_release")
    if square_shop_labels_release is not None:
        if not short_equipment_paper_release:
            raise ValueError("Square captions require the complete V252 stack")
        from dk4tool.patch.square_shop_labels import apply_release as apply_square_shop_labels

        arm9_path = "/__arm9__.bin"
        labelled_arm9, square_report = apply_square_shop_labels(
            candidate.read_file(arm9_path), square_shop_labels_release)
        candidate.replace_file(arm9_path, labelled_arm9)
        square_report["release_config"] = square_shop_labels_release
        square_report["release_config_sha256"] = sha256(Path(square_shop_labels_release).read_bytes())
        relocation_checks[arm9_path]["square_shop_labels"] = square_report
        changed_records[arm9_path].extend(square_report["changed_records"])

    square_sign_bounds_release = profile_config.get("square_sign_bounds_release")
    if square_sign_bounds_release is not None:
        if not square_shop_labels_release:
            raise ValueError("Square sign bounds require the complete V253 stack")
        from dk4tool.patch.square_sign_bounds import apply_release as apply_square_sign_bounds

        arm9_path = "/__arm9__.bin"
        bounded_arm9, bounds_report = apply_square_sign_bounds(
            candidate.read_file(arm9_path), square_sign_bounds_release)
        candidate.replace_file(arm9_path, bounded_arm9)
        bounds_report["release_config"] = square_sign_bounds_release
        bounds_report["release_config_sha256"] = sha256(Path(square_sign_bounds_release).read_bytes())
        relocation_checks[arm9_path]["square_sign_bounds"] = bounds_report
        changed_records[arm9_path].extend(bounds_report["changed_records"])

    common_literal_prefix_release = profile_config.get("common_literal_prefix_release")
    if common_literal_prefix_release is not None:
        if not square_sign_bounds_release:
            raise ValueError("Literal-prefix repair requires the complete V254 stack")
        from dk4tool.patch.common_literal_prefix import apply_release as apply_common_literal_prefix

        arm9_path = "/__arm9__.bin"
        literal_arm9, literal_report = apply_common_literal_prefix(
            candidate.read_file(arm9_path), common_literal_prefix_release)
        candidate.replace_file(arm9_path, literal_arm9)
        literal_report["release_config"] = common_literal_prefix_release
        literal_report["release_config_sha256"] = sha256(Path(common_literal_prefix_release).read_bytes())
        relocation_checks[arm9_path]["common_literal_prefix"] = literal_report
        changed_records[arm9_path].extend(literal_report["changed_records"])

    common_dialogue_alignment_release = profile_config.get("common_dialogue_alignment_release")
    if common_dialogue_alignment_release is not None:
        if not common_literal_prefix_release:
            raise ValueError("Dialogue alignment requires the complete V255 stack")
        from dk4tool.patch.common_dialogue_alignment import (
            apply_release as apply_common_dialogue_alignment,
        )

        arm9_path = "/__arm9__.bin"
        aligned_arm9, alignment_report = apply_common_dialogue_alignment(
            candidate.read_file(arm9_path), common_dialogue_alignment_release)
        candidate.replace_file(arm9_path, aligned_arm9)
        alignment_report["release_config"] = common_dialogue_alignment_release
        alignment_report["release_config_sha256"] = sha256(Path(common_dialogue_alignment_release).read_bytes())
        relocation_checks[arm9_path]["common_dialogue_alignment"] = alignment_report
        changed_records[arm9_path].extend(alignment_report["changed_records"])

    fleet_rank_labels_release = profile_config.get("fleet_rank_labels_release")
    if fleet_rank_labels_release is not None:
        if not common_dialogue_alignment_release:
            raise ValueError("Fleet rank labels require the complete V258 stack")
        from dk4tool.patch.fleet_rank_labels import apply_release as apply_fleet_rank_labels

        arm9_path = "/__arm9__.bin"
        ranked_arm9, rank_report = apply_fleet_rank_labels(
            candidate.read_file(arm9_path), NdsImage.open("work/clean.nds").read_file(arm9_path), fleet_rank_labels_release)
        candidate.replace_file(arm9_path, ranked_arm9)
        rank_report["release_config"] = fleet_rank_labels_release
        rank_report["release_config_sha256"] = sha256(Path(fleet_rank_labels_release).read_bytes())
        relocation_checks[arm9_path]["fleet_rank_labels"] = rank_report
        changed_records[arm9_path].extend(rank_report["changed_records"])

    world_map_headers_release = profile_config.get("world_map_headers_release")
    if world_map_headers_release is not None:
        if not fleet_rank_labels_release:
            raise ValueError("World Map headers require the complete V260 stack")
        from dk4tool.patch.world_map_headers import apply_release as apply_world_map_headers

        arm9_path = "/__arm9__.bin"
        mapped_arm9, map_report = apply_world_map_headers(
            candidate.read_file(arm9_path), NdsImage.open("work/clean.nds").read_file(arm9_path), world_map_headers_release)
        candidate.replace_file(arm9_path, mapped_arm9)
        map_report["release_config"] = world_map_headers_release
        map_report["release_config_sha256"] = sha256(Path(world_map_headers_release).read_bytes())
        relocation_checks[arm9_path]["world_map_headers"] = map_report
        changed_records[arm9_path].extend(map_report["changed_records"])

    deck_filter_help_release = profile_config.get("deck_filter_help_release")
    if deck_filter_help_release is not None:
        if not world_map_headers_release:
            raise ValueError("Deck filter/help requires the complete V261 stack")
        from dk4tool.patch.deck_filter_help import apply_release as apply_deck_filter_help

        arm9_path = "/__arm9__.bin"
        helped_arm9, help_report = apply_deck_filter_help(
            candidate.read_file(arm9_path), NdsImage.open("work/clean.nds").read_file(arm9_path), deck_filter_help_release)
        candidate.replace_file(arm9_path, helped_arm9)
        help_report["release_config"] = deck_filter_help_release
        help_report["release_config_sha256"] = sha256(Path(deck_filter_help_release).read_bytes())
        relocation_checks[arm9_path]["deck_filter_help"] = help_report
        changed_records[arm9_path].extend(help_report["changed_records"])

    sail_angle_caption_release = profile_config.get("sail_angle_caption_release")
    if sail_angle_caption_release is not None:
        if not deck_filter_help_release:
            raise ValueError("Sail-angle caption requires the complete V263 stack")
        from dk4tool.patch.sail_angle_caption import apply_release as apply_sail_angle_caption

        arm9_path = "/__arm9__.bin"
        captioned_arm9, caption_report = apply_sail_angle_caption(
            candidate.read_file(arm9_path), NdsImage.open("work/clean.nds").read_file(arm9_path), sail_angle_caption_release)
        candidate.replace_file(arm9_path, captioned_arm9)
        caption_report["release_config"] = sail_angle_caption_release
        caption_report["release_config_sha256"] = sha256(Path(sail_angle_caption_release).read_bytes())
        relocation_checks[arm9_path]["sail_angle_caption"] = caption_report
        changed_records[arm9_path].extend(caption_report["changed_records"])

    variable_equipment_paper_release = profile_config.get("variable_equipment_paper_release")
    if variable_equipment_paper_release is not None:
        if not sail_angle_caption_release:
            raise ValueError("Variable equipment paper requires the complete V267 stack")
        from dk4tool.patch.variable_equipment_paper import (
            apply_release as apply_variable_equipment_paper,
        )

        arm9_path = "/__arm9__.bin"
        papered_arm9, paper_report = apply_variable_equipment_paper(
            candidate.read_file(arm9_path), variable_equipment_paper_release)
        candidate.replace_file(arm9_path, papered_arm9)
        paper_report["release_config"] = variable_equipment_paper_release
        paper_report["release_config_sha256"] = sha256(Path(variable_equipment_paper_release).read_bytes())
        relocation_checks[arm9_path]["variable_equipment_paper"] = paper_report
        changed_records[arm9_path].extend(paper_report["changed_records"])

    direct_equipment_paper_release = profile_config.get("direct_equipment_paper_release")
    if direct_equipment_paper_release is not None:
        if not sail_angle_caption_release or variable_equipment_paper_release:
            raise ValueError("Direct paper requires V267 and excludes the failed slow renderer")
        from dk4tool.patch.direct_equipment_paper import (
            apply_release as apply_direct_equipment_paper,
        )

        arm9_path = "/__arm9__.bin"
        papered_arm9, paper_report = apply_direct_equipment_paper(
            candidate.read_file(arm9_path), direct_equipment_paper_release)
        candidate.replace_file(arm9_path, papered_arm9)
        paper_report["release_config"] = direct_equipment_paper_release
        paper_report["release_config_sha256"] = sha256(Path(direct_equipment_paper_release).read_bytes())
        relocation_checks[arm9_path]["direct_equipment_paper"] = paper_report
        changed_records[arm9_path].extend(paper_report["changed_records"])

    modal_cursor_guard_release = profile_config.get("modal_cursor_guard_release")
    if modal_cursor_guard_release is not None:
        if not direct_equipment_paper_release:
            raise ValueError("Modal cursor repair requires the complete V270 stack")
        from dk4tool.patch.modal_cursor_guard import apply_release as apply_modal_cursor_guard

        arm9_path = "/__arm9__.bin"
        guarded_arm9, cursor_report = apply_modal_cursor_guard(
            candidate.read_file(arm9_path), modal_cursor_guard_release)
        candidate.replace_file(arm9_path, guarded_arm9)
        cursor_report["release_config"] = modal_cursor_guard_release
        cursor_report["release_config_sha256"] = sha256(Path(modal_cursor_guard_release).read_bytes())
        relocation_checks[arm9_path]["modal_cursor_guard"] = cursor_report
        changed_records[arm9_path].extend(cursor_report["changed_records"])

    sailor_mood_caption_release = profile_config.get("sailor_mood_caption_release")
    if sailor_mood_caption_release is not None:
        if not modal_cursor_guard_release:
            raise ValueError("Sailor Mood caption requires the complete V272 stack")
        from dk4tool.patch.sailor_mood_caption import apply_release as apply_sailor_mood_caption

        arm9_path = "/__arm9__.bin"
        mood_arm9, mood_report = apply_sailor_mood_caption(
            candidate.read_file(arm9_path), NdsImage.open("work/clean.nds").read_file(arm9_path), sailor_mood_caption_release)
        candidate.replace_file(arm9_path, mood_arm9)
        mood_report["release_config"] = sailor_mood_caption_release
        mood_report["release_config_sha256"] = sha256(Path(sailor_mood_caption_release).read_bytes())
        relocation_checks[arm9_path]["sailor_mood_caption"] = mood_report
        changed_records[arm9_path].extend(mood_report["changed_records"])

    actor_integrity_release = profile_config.get("message_actor_integrity_release")
    if actor_integrity_release is not None:
        if not sailor_mood_caption_release:
            raise ValueError("Message actor integrity requires the complete V275 stack")
        from dk4tool.patch.message_actor_integrity import apply_release as apply_actor_integrity

        actor_report = apply_actor_integrity(
            candidate, NdsImage.open("work/clean.nds"), actor_integrity_release)
        for path in actor_report["target_file_sha256"]:
            scoped = [row for row in actor_report["records"] if row["file_path"] == path]
            relocation_checks.setdefault(path, {})["message_actor_integrity"] = {
                **actor_report, "records": scoped, "release_config": actor_integrity_release,
                "release_config_sha256": sha256(Path(actor_integrity_release).read_bytes()),
            }
            changed_records[path].extend(row["id"] for row in scoped)

    artwork_name_captions_release = profile_config.get("artwork_name_captions_release")
    if artwork_name_captions_release is not None:
        if not actor_integrity_release:
            raise ValueError("Artwork name captions require the complete V296 stack")
        from dk4tool.patch.artwork_name_captions import apply_release as apply_artwork_name_captions

        arm9_path = "/__arm9__.bin"
        captions_arm9, captions_report = apply_artwork_name_captions(
            candidate.read_file(arm9_path), NdsImage.open("work/clean.nds").read_file(arm9_path),
            artwork_name_captions_release)
        candidate.replace_file(arm9_path, captions_arm9)
        captions_report["release_config"] = artwork_name_captions_release
        captions_report["release_config_sha256"] = sha256(Path(artwork_name_captions_release).read_bytes())
        relocation_checks[arm9_path]["artwork_name_captions"] = captions_report
        changed_records[arm9_path].extend(captions_report["changed_records"])

    reviewed_name_integration_release = profile_config.get("reviewed_name_integration_release")
    if reviewed_name_integration_release is not None:
        if not artwork_name_captions_release:
            raise ValueError("Reviewed name integration requires the complete V298 caption stack")
        from dk4tool.patch.reviewed_name_integration import (
            apply_release as apply_reviewed_name_integration,
        )

        names_report = apply_reviewed_name_integration(
            candidate, NdsImage.open("work/clean.nds"), baseline, reviewed_name_integration_release)
        names_report["release_config"] = reviewed_name_integration_release
        names_report["release_config_sha256"] = sha256(Path(reviewed_name_integration_release).read_bytes())
        relocation_checks["/__arm9__.bin"]["reviewed_name_integration"] = names_report
        changed_records["/__arm9__.bin"].extend(row["id"] for row in names_report["catalog"]["name_fields"])
        changed_records["/__arm9__.bin"].append("REVIEWED_ROUTE_NAME_CATALOG_467_KEYS")
        for row in names_report["route"]["fixed_records"]:
            changed_records[row["file_path"]].append(row["id"])
        for row in names_report["catalog"]["records"]:
            for request in row["requests"]:
                path, ident = request["owner"]
                if ident not in changed_records[path]:
                    changed_records[path].append(ident)
        changed_records["/COMMON/MESFILE.DK4"].extend(
            f"COMMON_MESSAGE_{index:04d}" for index in names_report["COMMON"]["message_IDs"])
        changed_records["/COMMON/HELP.DK4"].extend(
            f"HELP_TOPIC_{index:03d}" for index in names_report["HELP"]["topic_IDs"])

    gallery_menu_labels_release = profile_config.get("gallery_menu_labels_release")
    if gallery_menu_labels_release is not None:
        if not reviewed_name_integration_release:
            raise ValueError("Gallery labels require the complete V305 naming/art stack")
        from dk4tool.patch.gallery_menu_labels import apply_release as apply_gallery_menu_labels

        arm9_path = "/__arm9__.bin"
        gallery_arm9, gallery_report = apply_gallery_menu_labels(
            candidate.read_file(arm9_path), NdsImage.open("work/clean.nds").read_file(arm9_path),
            baseline.read_file(arm9_path), gallery_menu_labels_release)
        candidate.replace_file(arm9_path, gallery_arm9)
        gallery_report["release_config"] = gallery_menu_labels_release
        gallery_report["release_config_sha256"] = sha256(Path(gallery_menu_labels_release).read_bytes())
        relocation_checks[arm9_path]["gallery_menu_labels"] = gallery_report
        changed_records[arm9_path].extend(gallery_report["changed_records"])

    sailing_condition_names_release = profile_config.get("sailing_condition_names_release")
    if sailing_condition_names_release is not None:
        if not gallery_menu_labels_release:
            raise ValueError("Sailing condition names require the complete V307 stack")
        from dk4tool.patch.sailing_condition_names import (
            apply_release as apply_sailing_condition_names,
        )

        arm9_path = "/__arm9__.bin"
        conditions_arm9, conditions_report = apply_sailing_condition_names(
            candidate.read_file(arm9_path), NdsImage.open("work/clean.nds").read_file(arm9_path),
            baseline.read_file(arm9_path), sailing_condition_names_release)
        candidate.replace_file(arm9_path, conditions_arm9)
        conditions_report["release_config"] = sailing_condition_names_release
        conditions_report["release_config_sha256"] = sha256(Path(sailing_condition_names_release).read_bytes())
        relocation_checks[arm9_path]["sailing_condition_names"] = conditions_report
        changed_records[arm9_path].extend(conditions_report["changed_records"])

    auto_move_caption_release = profile_config.get("auto_move_caption_release")
    if auto_move_caption_release is not None:
        if not sailing_condition_names_release:
            raise ValueError("Auto Move caption requires the complete V309 stack")
        from dk4tool.patch.auto_move_caption import apply_release as apply_auto_move_caption

        arm9_path = "/__arm9__.bin"
        auto_arm9, auto_report = apply_auto_move_caption(
            candidate.read_file(arm9_path), NdsImage.open("work/clean.nds").read_file(arm9_path),
            baseline.read_file(arm9_path), auto_move_caption_release)
        candidate.replace_file(arm9_path, auto_arm9)
        auto_report["release_config"] = auto_move_caption_release
        auto_report["release_config_sha256"] = sha256(Path(auto_move_caption_release).read_bytes())
        relocation_checks[arm9_path]["auto_move_caption"] = auto_report
        changed_records[arm9_path].extend(auto_report["changed_records"])

    footer_measurement_release = profile_config.get("footer_measurement_release")
    if footer_measurement_release is not None:
        if not auto_move_caption_release:
            raise ValueError("Footer measurement requires the complete V316 stack")
        from dk4tool.patch.footer_measurement import apply_release as apply_footer_measurement

        arm9_path = "/__arm9__.bin"
        footer_arm9, footer_report = apply_footer_measurement(
            candidate.read_file(arm9_path), NdsImage.open("work/clean.nds").read_file(arm9_path),
            baseline.read_file(arm9_path), footer_measurement_release)
        candidate.replace_file(arm9_path, footer_arm9)
        footer_report["release_config"] = footer_measurement_release
        footer_report["release_config_sha256"] = sha256(Path(footer_measurement_release).read_bytes())
        relocation_checks[arm9_path]["footer_measurement"] = footer_report
        changed_records[arm9_path].extend(footer_report["changed_records"])

    sea_inspect_caption_release = profile_config.get("sea_inspect_caption_release")
    if sea_inspect_caption_release is not None:
        if not footer_measurement_release:
            raise ValueError("Inspect caption requires the complete V318 stack")
        from dk4tool.patch.sea_inspect_caption import apply_release as apply_sea_inspect_caption

        arm9_path = "/__arm9__.bin"
        inspect_arm9, inspect_report = apply_sea_inspect_caption(
            candidate.read_file(arm9_path), NdsImage.open("work/clean.nds").read_file(arm9_path),
            baseline.read_file(arm9_path), sea_inspect_caption_release)
        candidate.replace_file(arm9_path, inspect_arm9)
        inspect_report["release_config"] = sea_inspect_caption_release
        inspect_report["release_config_sha256"] = sha256(Path(sea_inspect_caption_release).read_bytes())
        relocation_checks[arm9_path]["sea_inspect_caption"] = inspect_report
        changed_records[arm9_path].extend(inspect_report["changed_records"])

    sail_rotation_caption_release = profile_config.get("sail_rotation_caption_release")
    if sail_rotation_caption_release is not None:
        if not sea_inspect_caption_release:
            raise ValueError("Rotate caption requires the complete V322 stack")
        from dk4tool.patch.sail_rotation_caption import apply_release as apply_sail_rotation_caption

        arm9_path = "/__arm9__.bin"
        rotate_arm9, rotate_report = apply_sail_rotation_caption(
            candidate.read_file(arm9_path), NdsImage.open("work/clean.nds").read_file(arm9_path),
            baseline.read_file(arm9_path), sail_rotation_caption_release)
        candidate.replace_file(arm9_path, rotate_arm9)
        rotate_report["release_config"] = sail_rotation_caption_release
        rotate_report["release_config_sha256"] = sha256(Path(sail_rotation_caption_release).read_bytes())
        relocation_checks[arm9_path]["sail_rotation_caption"] = rotate_report
        changed_records[arm9_path].extend(rotate_report["changed_records"])

    crew_role_labels_release = profile_config.get("crew_role_labels_release")
    if crew_role_labels_release is not None:
        if not sail_rotation_caption_release:
            raise ValueError("Crew roles require the complete V324 stack")
        from dk4tool.patch.crew_role_labels import apply_release as apply_crew_role_labels

        arm9_path = "/__arm9__.bin"
        roles_arm9, roles_report = apply_crew_role_labels(
            candidate.read_file(arm9_path), NdsImage.open("work/clean.nds").read_file(arm9_path),
            baseline.read_file(arm9_path), crew_role_labels_release)
        candidate.replace_file(arm9_path, roles_arm9)
        roles_report["release_config"] = crew_role_labels_release
        roles_report["release_config_sha256"] = sha256(Path(crew_role_labels_release).read_bytes())
        relocation_checks[arm9_path]["crew_role_labels"] = roles_report
        changed_records[arm9_path].extend(roles_report["changed_records"])

    legacy_saved_item_names_release = profile_config.get("legacy_saved_item_names_release")
    if legacy_saved_item_names_release is not None:
        from dk4tool.patch.legacy_saved_item_names import apply_release as apply_legacy_saved_names

        arm9_path = "/__arm9__.bin"
        names_arm9, names_report = apply_legacy_saved_names(
            candidate.read_file(arm9_path), NdsImage.open("work/clean.nds").read_file(arm9_path),
            legacy_saved_item_names_release)
        candidate.replace_file(arm9_path, names_arm9)
        names_report["release_config"] = legacy_saved_item_names_release
        names_report["release_config_sha256"] = sha256(Path(legacy_saved_item_names_release).read_bytes())
        relocation_checks[arm9_path]["legacy_saved_item_names"] = names_report
        changed_records[arm9_path].extend(names_report["changed_records"])

    guild_diplomacy_labels_release = profile_config.get("guild_diplomacy_labels_release")
    if guild_diplomacy_labels_release is not None:
        from dk4tool.patch.guild_diplomacy_labels import apply_release as apply_guild_diplomacy

        arm9_path = "/__arm9__.bin"
        guild_arm9, guild_report = apply_guild_diplomacy(
            candidate.read_file(arm9_path), NdsImage.open("work/clean.nds").read_file(arm9_path),
            baseline.read_file(arm9_path), guild_diplomacy_labels_release)
        candidate.replace_file(arm9_path, guild_arm9)
        guild_report["release_config"] = guild_diplomacy_labels_release
        guild_report["release_config_sha256"] = sha256(Path(guild_diplomacy_labels_release).read_bytes())
        relocation_checks[arm9_path]["guild_diplomacy_labels"] = guild_report
        changed_records[arm9_path].extend(guild_report["changed_records"])

    roster_role_crop_release = profile_config.get("roster_role_crop_release")
    if roster_role_crop_release is not None:
        from dk4tool.patch.roster_role_crop import apply_release as apply_roster_role_crop

        arm9_path = "/__arm9__.bin"
        roster_arm9, roster_report = apply_roster_role_crop(
            candidate.read_file(arm9_path), NdsImage.open("work/clean.nds").read_file(arm9_path),
            baseline.read_file(arm9_path), roster_role_crop_release)
        candidate.replace_file(arm9_path, roster_arm9)
        roster_report["release_config"] = roster_role_crop_release
        roster_report["release_config_sha256"] = sha256(Path(roster_role_crop_release).read_bytes())
        relocation_checks[arm9_path]["roster_role_crop"] = roster_report
        changed_records[arm9_path].extend(roster_report["changed_records"])

    endurance_approximation_release = profile_config.get("endurance_approximation_release")
    if endurance_approximation_release is not None:
        from dk4tool.patch.endurance_approximation import (
            apply_release as apply_endurance_approximation,
        )

        arm9_path = "/__arm9__.bin"
        endurance_arm9, endurance_report = apply_endurance_approximation(
            candidate.read_file(arm9_path), NdsImage.open("work/clean.nds").read_file(arm9_path),
            baseline.read_file(arm9_path), endurance_approximation_release)
        candidate.replace_file(arm9_path, endurance_arm9)
        endurance_report["release_config"] = endurance_approximation_release
        endurance_report["release_config_sha256"] = sha256(Path(endurance_approximation_release).read_bytes())
        relocation_checks[arm9_path]["endurance_approximation"] = endurance_report
        changed_records[arm9_path].extend(endurance_report["changed_records"])

    commodity_ui_release = profile_config.get("commodity_ui_release")
    if commodity_ui_release is not None:
        from dk4tool.patch.commodity_ui_release import apply_release as apply_commodity_ui

        arm9_path = "/__arm9__.bin"
        commodity_arm9, commodity_report = apply_commodity_ui(
            candidate.read_file(arm9_path), NdsImage.open("work/clean.nds").read_file(arm9_path),
            commodity_ui_release)
        candidate.replace_file(arm9_path, commodity_arm9)
        commodity_report["release_config"] = commodity_ui_release
        commodity_report["release_config_sha256"] = sha256(Path(commodity_ui_release).read_bytes())
        relocation_checks[arm9_path]["commodity_ui"] = commodity_report
        changed_records[arm9_path].extend(commodity_report["changed_records"])

    equipment_confirmation_wrap = profile_config.get("equipment_confirmation_wrap")
    if equipment_confirmation_wrap is not None:
        from dk4tool.patch.equipment_confirmation_wrap import apply_release as apply_equipment_wrap

        arm9_path = "/__arm9__.bin"
        equipment_arm9, equipment_report = apply_equipment_wrap(
            candidate.read_file(arm9_path), equipment_confirmation_wrap)
        candidate.replace_file(arm9_path, equipment_arm9)
        equipment_report["release_config"] = equipment_confirmation_wrap
        equipment_report["release_config_sha256"] = sha256(Path(equipment_confirmation_wrap).read_bytes())
        relocation_checks[arm9_path]["equipment_confirmation_wrap"] = equipment_report
        changed_records[arm9_path].extend(equipment_report["changed_records"])

    fleet_detail_release = profile_config.get("fleet_detail_release")
    if fleet_detail_release is not None:
        from dk4tool.patch.fleet_detail_release import apply_release as apply_fleet_detail

        arm9_path = "/__arm9__.bin"
        fleet_arm9, fleet_report = apply_fleet_detail(
            candidate.read_file(arm9_path), NdsImage.open("work/clean.nds").read_file(arm9_path),
            fleet_detail_release)
        candidate.replace_file(arm9_path, fleet_arm9)
        fleet_report["release_config"] = fleet_detail_release
        fleet_report["release_config_sha256"] = sha256(Path(fleet_detail_release).read_bytes())
        relocation_checks[arm9_path]["fleet_detail"] = fleet_report
        changed_records[arm9_path].extend(fleet_report["changed_records"])

    unguarded_dialogue_alignment = profile_config.get("unguarded_dialogue_alignment")
    if unguarded_dialogue_alignment is not None:
        from dk4tool.patch.unguarded_dialogue_alignment import (
            apply_release as apply_unguarded_alignment,
        )

        arm9_path = "/__arm9__.bin"
        aligned_arm9, aligned_report = apply_unguarded_alignment(
            candidate.read_file(arm9_path), unguarded_dialogue_alignment)
        candidate.replace_file(arm9_path, aligned_arm9)
        aligned_report["release_config"] = unguarded_dialogue_alignment
        aligned_report["release_config_sha256"] = sha256(Path(unguarded_dialogue_alignment).read_bytes())
        relocation_checks[arm9_path]["unguarded_dialogue_alignment"] = aligned_report
        changed_records[arm9_path].extend(aligned_report["changed_records"])

    tavern_round_announcement = profile_config.get("tavern_round_announcement")
    if tavern_round_announcement is not None:
        from dk4tool.patch.tavern_round_announcement import apply_release as apply_tavern_round

        common_path, arm9_path = "/COMMON/MESFILE.DK4", "/__arm9__.bin"
        round_common, round_report = apply_tavern_round(
            candidate.read_file(common_path), candidate.read_file(arm9_path), tavern_round_announcement)
        candidate.replace_file(common_path, round_common)
        round_report["release_config"] = tavern_round_announcement
        round_report["release_config_sha256"] = sha256(Path(tavern_round_announcement).read_bytes())
        relocation_checks[common_path]["tavern_round_announcement"] = round_report
        changed_records[common_path].extend(round_report["changed_records"])

    condition_labels = profile_config.get("condition_labels")
    if condition_labels is not None:
        from dk4tool.patch.condition_labels import apply_release as apply_condition_labels

        arm9_path = "/__arm9__.bin"
        conditions_arm9, conditions_report = apply_condition_labels(
            candidate.read_file(arm9_path), condition_labels)
        candidate.replace_file(arm9_path, conditions_arm9)
        conditions_report["release_config"] = condition_labels
        conditions_report["release_config_sha256"] = sha256(Path(condition_labels).read_bytes())
        relocation_checks[arm9_path]["condition_labels"] = conditions_report
        changed_records[arm9_path].extend(conditions_report["changed_records"])

    local_reputation_rumors = profile_config.get("local_reputation_rumors")
    if local_reputation_rumors is not None:
        from dk4tool.patch.local_reputation_rumors import apply_release as apply_reputation_rumors

        common_path, arm9_path = "/COMMON/MESFILE.DK4", "/__arm9__.bin"
        rumors_common, rumors_arm9, rumors_report = apply_reputation_rumors(
            candidate.read_file(common_path), candidate.read_file(arm9_path), local_reputation_rumors)
        candidate.replace_file(common_path, rumors_common)
        candidate.replace_file(arm9_path, rumors_arm9)
        rumors_report["release_config"] = local_reputation_rumors
        rumors_report["release_config_sha256"] = sha256(Path(local_reputation_rumors).read_bytes())
        relocation_checks[common_path]["local_reputation_rumors"] = rumors_report
        changed_records[common_path].extend(rumors_report["changed_records"])
        changed_records[arm9_path].extend(["COMMON_RUMOR_OFFSET_822", "COMMON_RUMOR_OFFSET_823"])

    tavern_addresses = profile_config.get("tavern_addresses")
    if tavern_addresses is not None:
        from dk4tool.patch.tavern_address_release import apply_release as apply_tavern_addresses

        common_path, arm9_path = "/COMMON/MESFILE.DK4", "/__arm9__.bin"
        address_common, address_arm9, address_report = apply_tavern_addresses(
            candidate.read_file(common_path), candidate.read_file(arm9_path), tavern_addresses)
        candidate.replace_file(common_path, address_common)
        candidate.replace_file(arm9_path, address_arm9)
        address_report["release_config"] = tavern_addresses
        address_report["release_config_sha256"] = sha256(Path(tavern_addresses).read_bytes())
        relocation_checks[common_path]["tavern_addresses"] = address_report
        changed_records[common_path].extend(address_report["changed_records"])
        changed_records[arm9_path].extend(["TAVERN_SHARED_ADDRESSES", "TAVERN_PORTRAIT_WORD_WRAP"])

    trade_help = profile_config.get("trade_help_release")
    if trade_help is not None:
        from dk4tool.patch.trade_help_release import apply_release as apply_trade_help

        help_path = "/COMMON/HELP.DK4"
        translated_help, trade_report = apply_trade_help(
            candidate.read_file(help_path),
            NdsImage.open("work/clean.nds").read_file(help_path),
            baseline.read_file(help_path), trade_help)
        candidate.replace_file(help_path, translated_help)
        trade_report["release_config"] = trade_help
        trade_report["release_config_sha256"] = sha256(Path(trade_help).read_bytes())
        relocation_checks.setdefault(help_path, {})["trade_help_release"] = trade_report
        changed_records[help_path].extend(trade_report["changed_records"])

    general_help = profile_config.get("general_help_release")
    if general_help is not None:
        from dk4tool.patch.general_help_release import apply_release as apply_general_help

        help_path = "/COMMON/HELP.DK4"
        translated_help, general_report = apply_general_help(
            candidate.read_file(help_path),
            NdsImage.open("work/clean.nds").read_file(help_path),
            baseline.read_file(help_path), general_help)
        candidate.replace_file(help_path, translated_help)
        general_report["release_config"] = general_help
        general_report["release_config_sha256"] = sha256(Path(general_help).read_bytes())
        relocation_checks.setdefault(help_path, {})["general_help_release"] = general_report
        changed_records[help_path].extend(general_report["changed_records"])

    city_help = profile_config.get("city_help_release")
    if city_help is not None:
        from dk4tool.patch.city_help_release import apply_release as apply_city_help

        help_path = "/COMMON/HELP.DK4"
        translated_help, city_report = apply_city_help(
            candidate.read_file(help_path),
            NdsImage.open("work/clean.nds").read_file(help_path),
            baseline.read_file(help_path), city_help)
        candidate.replace_file(help_path, translated_help)
        city_report["release_config"] = city_help
        city_report["release_config_sha256"] = sha256(Path(city_help).read_bytes())
        relocation_checks.setdefault(help_path, {})["city_help_release"] = city_report
        changed_records[help_path].extend(city_report["changed_records"])

    city_status = profile_config.get("city_status_labels")
    if city_status is not None:
        from dk4tool.patch.city_status_labels import apply_release as apply_city_status

        arm9_path = "/__arm9__.bin"
        status_arm9, status_report = apply_city_status(candidate.read_file(arm9_path), city_status)
        candidate.replace_file(arm9_path, status_arm9)
        status_report["release_config"] = city_status
        status_report["release_config_sha256"] = sha256(Path(city_status).read_bytes())
        relocation_checks[arm9_path]["city_status_labels"] = status_report
        changed_records[arm9_path].extend(status_report["changed_records"])

    faction_help = profile_config.get("faction_help_release")
    if faction_help is not None:
        from dk4tool.patch.faction_help_release import apply_release as apply_faction_help

        help_path = "/COMMON/HELP.DK4"
        translated_help, faction_report = apply_faction_help(
            candidate.read_file(help_path),
            NdsImage.open("work/clean.nds").read_file(help_path),
            baseline.read_file(help_path), faction_help)
        candidate.replace_file(help_path, translated_help)
        faction_report["release_config"] = faction_help
        faction_report["release_config_sha256"] = sha256(Path(faction_help).read_bytes())
        relocation_checks.setdefault(help_path, {})["faction_help_release"] = faction_report
        changed_records[help_path].extend(faction_report["changed_records"])

    guild_descriptions = profile_config.get("guild_description_wrap")
    if guild_descriptions is not None:
        from dk4tool.patch.guild_description_wrap import apply_release as apply_guild_descriptions

        common_path, arm9_path = "/COMMON/MESFILE.DK4", "/__arm9__.bin"
        guild_common, guild_arm9, guild_report = apply_guild_descriptions(
            candidate.read_file(common_path), candidate.read_file(arm9_path), guild_descriptions)
        candidate.replace_file(common_path, guild_common)
        candidate.replace_file(arm9_path, guild_arm9)
        guild_report["release_config"] = guild_descriptions
        guild_report["release_config_sha256"] = sha256(Path(guild_descriptions).read_bytes())
        relocation_checks[common_path]["guild_description_wrap"] = guild_report
        changed_records[common_path].extend(["COMMON_MESSAGE_3665"])
        changed_records[arm9_path].extend(["GUILD_TREASURE_DESCRIPTION_WORD_WRAP"])

    sailor_data_help = profile_config.get("sailor_data_help_release")
    if sailor_data_help is not None:
        from dk4tool.patch.sailor_data_help_release import apply_release as apply_sailor_data_help

        help_path = "/COMMON/HELP.DK4"
        translated_help, sailor_report = apply_sailor_data_help(
            candidate.read_file(help_path),
            NdsImage.open("work/clean.nds").read_file(help_path),
            baseline.read_file(help_path), sailor_data_help)
        candidate.replace_file(help_path, translated_help)
        sailor_report["release_config"] = sailor_data_help
        sailor_report["release_config_sha256"] = sha256(Path(sailor_data_help).read_bytes())
        relocation_checks.setdefault(help_path, {})["sailor_data_help_release"] = sailor_report
        changed_records[help_path].extend(sailor_report["changed_records"])

    crew_help = profile_config.get("crew_help_release")
    if crew_help is not None:
        from dk4tool.patch.crew_help_release import apply_release as apply_crew_help

        help_path = "/COMMON/HELP.DK4"
        translated_help, crew_help_report = apply_crew_help(
            candidate.read_file(help_path),
            NdsImage.open("work/clean.nds").read_file(help_path),
            baseline.read_file(help_path), crew_help)
        candidate.replace_file(help_path, translated_help)
        crew_help_report["release_config"] = crew_help
        crew_help_report["release_config_sha256"] = sha256(Path(crew_help).read_bytes())
        relocation_checks.setdefault(help_path, {})["crew_help_release"] = crew_help_report
        changed_records[help_path].extend(crew_help_report["changed_records"])

    help_footer = profile_config.get("help_footer_release")
    if help_footer is not None:
        if profile_config.get("help_footer_release_version", 1) == 3:
            from dk4tool.patch.help_footer_release_v3 import apply_release as apply_help_footer
        elif profile_config.get("help_footer_release_version", 1) == 2:
            from dk4tool.patch.help_footer_release_v2 import apply_release as apply_help_footer
        else:
            from dk4tool.patch.help_footer_release import apply_release as apply_help_footer

        arm9_path = "/__arm9__.bin"
        footer_arm, footer_report = apply_help_footer(candidate.read_file(arm9_path), help_footer)
        candidate.replace_file(arm9_path, footer_arm)
        footer_report["release_config"] = help_footer
        footer_report["release_config_sha256"] = sha256(Path(help_footer).read_bytes())
        relocation_checks[arm9_path]["help_footer_release"] = footer_report
        changed_records[arm9_path].extend(footer_report["changed_records"])

    interface_help = profile_config.get("interface_help_release")
    if interface_help is not None:
        from dk4tool.patch.interface_help_release import apply_release as apply_interface_help

        help_path = "/COMMON/HELP.DK4"
        translated_help, interface_report = apply_interface_help(
            candidate.read_file(help_path),
            NdsImage.open("work/clean.nds").read_file(help_path),
            baseline.read_file(help_path), interface_help)
        candidate.replace_file(help_path, translated_help)
        interface_report["release_config"] = interface_help
        interface_report["release_config_sha256"] = sha256(Path(interface_help).read_bytes())
        relocation_checks.setdefault(help_path, {})["interface_help_release"] = interface_report
        changed_records[help_path].extend(interface_report["changed_records"])

    navigation_help = profile_config.get("navigation_help_release")
    if navigation_help is not None:
        if profile_config.get("navigation_help_release_version", 1) == 2:
            from dk4tool.patch.navigation_help_release_v2 import (
                apply_release as apply_navigation_help,
            )
        else:
            from dk4tool.patch.navigation_help_release import apply_release as apply_navigation_help

        help_path = "/COMMON/HELP.DK4"
        translated_help, navigation_report = apply_navigation_help(
            candidate.read_file(help_path),
            NdsImage.open("work/clean.nds").read_file(help_path),
            baseline.read_file(help_path), navigation_help)
        candidate.replace_file(help_path, translated_help)
        navigation_report["release_config"] = navigation_help
        navigation_report["release_config_sha256"] = sha256(Path(navigation_help).read_bytes())
        relocation_checks.setdefault(help_path, {})["navigation_help_release"] = navigation_report
        changed_records[help_path].extend(navigation_report["changed_records"])

    skill_terms_help = profile_config.get("skill_terms_help_release")
    if skill_terms_help is not None:
        from dk4tool.patch.skill_terms_help_release import apply_release as apply_skill_terms_help

        help_path = "/COMMON/HELP.DK4"
        translated_help, skill_terms_report = apply_skill_terms_help(
            candidate.read_file(help_path),
            NdsImage.open("work/clean.nds").read_file(help_path),
            baseline.read_file(help_path), skill_terms_help)
        candidate.replace_file(help_path, translated_help)
        skill_terms_report["release_config"] = skill_terms_help
        skill_terms_report["release_config_sha256"] = sha256(Path(skill_terms_help).read_bytes())
        relocation_checks.setdefault(help_path, {})["skill_terms_help_release"] = skill_terms_report
        changed_records[help_path].extend(skill_terms_report["changed_records"])

    crew_columns = profile_config.get("crew_column_alignment")
    if crew_columns is not None:
        from dk4tool.patch.crew_column_alignment import apply_release as apply_crew_columns

        arm_path = "/__arm9__.bin"
        aligned_arm, crew_columns_report = apply_crew_columns(candidate.read_file(arm_path), crew_columns)
        candidate.replace_file(arm_path, aligned_arm)
        crew_columns_report["release_config"] = crew_columns
        crew_columns_report["release_config_sha256"] = sha256(Path(crew_columns).read_bytes())
        relocation_checks.setdefault(arm_path, {})["crew_column_alignment"] = crew_columns_report
        changed_records[arm_path].extend(crew_columns_report["changed_records"])

    repair_wait = profile_config.get("repair_wait_wrap")
    if repair_wait is not None:
        from dk4tool.patch.repair_wait_wrap import apply_release as apply_repair_wait

        arm_path = "/__arm9__.bin"
        repaired_arm, repair_wait_report = apply_repair_wait(candidate.read_file(arm_path), repair_wait)
        candidate.replace_file(arm_path, repaired_arm)
        repair_wait_report["release_config"] = repair_wait
        repair_wait_report["release_config_sha256"] = sha256(Path(repair_wait).read_bytes())
        relocation_checks.setdefault(arm_path, {})["repair_wait_wrap"] = repair_wait_report
        changed_records[arm_path].extend(repair_wait_report["changed_records"])

    square_cells = profile_config.get("square_caption_cells")
    if square_cells is not None:
        from dk4tool.patch.square_caption_cells import apply_release as apply_square_cells

        arm_path = "/__arm9__.bin"
        square_arm, square_report = apply_square_cells(candidate.read_file(arm_path), square_cells)
        candidate.replace_file(arm_path, square_arm)
        square_report["release_config"] = square_cells
        square_report["release_config_sha256"] = sha256(Path(square_cells).read_bytes())
        relocation_checks.setdefault(arm_path, {})["square_caption_cells"] = square_report
        changed_records[arm_path].extend(square_report["changed_records"])

    town_lifetime = profile_config.get("town_canvas_lifetime")
    if town_lifetime is not None:
        from dk4tool.patch.town_canvas_lifetime import apply_release as apply_town_lifetime

        arm_path = "/__arm9__.bin"
        private_arm, lifetime_report = apply_town_lifetime(candidate.read_file(arm_path), town_lifetime)
        candidate.replace_file(arm_path, private_arm)
        lifetime_report["release_config"] = town_lifetime
        lifetime_report["release_config_sha256"] = sha256(Path(town_lifetime).read_bytes())
        relocation_checks.setdefault(arm_path, {})["town_canvas_lifetime"] = lifetime_report
        changed_records[arm_path].extend(lifetime_report["changed_records"])

    town_rows = profile_config.get("town_stock_rows")
    if town_rows is not None:
        from dk4tool.patch.town_stock_rows import apply_release as apply_town_rows

        arm_path = "/__arm9__.bin"
        rows_arm, rows_report = apply_town_rows(candidate.read_file(arm_path), town_rows)
        candidate.replace_file(arm_path, rows_arm)
        rows_report["release_config"] = town_rows
        rows_report["release_config_sha256"] = sha256(Path(town_rows).read_bytes())
        relocation_checks.setdefault(arm_path, {})["town_stock_rows"] = rows_report
        changed_records[arm_path].extend(rows_report["changed_records"])

    tavern_family = profile_config.get("tavern_family_wrap")
    if tavern_family is not None:
        if not town_rows:
            raise ValueError("Tavern family wrapping requires the complete V502 stack")
        from dk4tool.patch.tavern_family_wrap import apply_release as apply_tavern_family

        common_path, arm_path = "/COMMON/MESFILE.DK4", "/__arm9__.bin"
        family_common, family_arm, family_report = apply_tavern_family(
            candidate.read_file(common_path), candidate.read_file(arm_path), tavern_family)
        candidate.replace_file(common_path, family_common)
        candidate.replace_file(arm_path, family_arm)
        family_report["release_config"] = tavern_family
        family_report["release_config_sha256"] = sha256(Path(tavern_family).read_bytes())
        relocation_checks.setdefault(common_path, {})["tavern_family_wrap"] = family_report
        relocation_checks.setdefault(arm_path, {})["tavern_family_wrap"] = family_report
        changed_records[common_path].append("COMMON_MESSAGE_827")
        changed_records[arm_path].append("COMMON_TAVERN_FAMILY_PORTRAIT_WORD_WRAP")

    sea_foam = profile_config.get("sea_foam_family")
    if sea_foam is not None:
        if not tavern_family:
            raise ValueError("Sea-foam dialogue requires the complete V508 stack")
        from dk4tool.patch.sea_foam_family import apply_release as apply_sea_foam

        common_path, arm_path = "/COMMON/MESFILE.DK4", "/__arm9__.bin"
        foam_common, foam_arm, foam_report = apply_sea_foam(
            candidate.read_file(common_path), candidate.read_file(arm_path), sea_foam)
        candidate.replace_file(common_path, foam_common)
        candidate.replace_file(arm_path, foam_arm)
        foam_report["release_config"] = sea_foam
        foam_report["release_config_sha256"] = sha256(Path(sea_foam).read_bytes())
        relocation_checks.setdefault(common_path, {})["sea_foam_family"] = foam_report
        relocation_checks.setdefault(arm_path, {})["sea_foam_family"] = foam_report
        changed_records[common_path].extend([f"COMMON_MESSAGE_{i}" for i in range(457, 481)])
        changed_records[arm_path].append("SEA_FOAM_PORTRAIT_WRAP_457_480")

    surname_completion = profile_config.get("shiraki_surname")
    if surname_completion is not None:
        if not sea_foam:
            raise ValueError("Surname completion requires the complete V514 stack")
        from dk4tool.patch.shiraki_surname import apply_release as apply_surname

        arm_path = "/__arm9__.bin"
        surname_arm, surname_report = apply_surname(candidate.read_file(arm_path), surname_completion)
        candidate.replace_file(arm_path, surname_arm)
        surname_report["release_config"] = surname_completion
        surname_report["release_config_sha256"] = sha256(Path(surname_completion).read_bytes())
        relocation_checks.setdefault(arm_path, {})["shiraki_surname"] = surname_report
        changed_records[arm_path].append("NPC_SURNAME_SHIRAKI")

    gallery_bounds = profile_config.get('gallery_caption_bounds')
    if gallery_bounds is not None:
        if not surname_completion:
            raise ValueError('Gallery caption bounds requires the complete V518 stack')
        from dk4tool.patch.gallery_caption_bounds import apply_release as apply_gallery_bounds

        arm_path = '/__arm9__.bin'
        bounded_arm, bounded_report = apply_gallery_bounds(candidate.read_file(arm_path), gallery_bounds)
        candidate.replace_file(arm_path, bounded_arm)
        bounded_report['release_config'] = gallery_bounds
        bounded_report['release_config_sha256'] = sha256(Path(gallery_bounds).read_bytes())
        relocation_checks.setdefault(arm_path, {})['gallery_caption_bounds'] = bounded_report
        changed_records[arm_path].append('SCENE_CAPTION_ROUTE_3_35')

    characters_text = profile_config.get('characters_gallery_text')
    if characters_text is not None:
        if not gallery_bounds:
            raise ValueError('Characters gallery requires the complete V523 stack')
        from dk4tool.patch.characters_gallery_text import apply_release as apply_characters_text

        arm_path = '/__arm9__.bin'
        characters_arm, characters_report = apply_characters_text(candidate.read_file(arm_path), characters_text)
        candidate.replace_file(arm_path, characters_arm)
        characters_report['release_config'] = characters_text
        characters_report['release_config_sha256'] = sha256(Path(characters_text).read_bytes())
        relocation_checks.setdefault(arm_path, {})['characters_gallery_text'] = characters_report
        changed_records[arm_path].extend(characters_report['changed_records'])

    historic_names = profile_config.get('historic_site_names')
    if historic_names is not None:
        if not characters_text:
            raise ValueError('Historic site names require the complete V525 stack')
        from dk4tool.patch.historic_site_names import apply_release as apply_historic_names

        arm_path = '/__arm9__.bin'
        historic_arm, historic_report = apply_historic_names(candidate.read_file(arm_path), historic_names)
        candidate.replace_file(arm_path, historic_arm)
        historic_report['release_config'] = historic_names
        historic_report['release_config_sha256'] = sha256(Path(historic_names).read_bytes())
        relocation_checks.setdefault(arm_path, {})['historic_site_names'] = historic_report
        changed_records[arm_path].extend(historic_report['changed_records'])

    site_descriptions = profile_config.get('site_descriptions')
    if site_descriptions is not None:
        if not historic_names:
            raise ValueError('Site descriptions require the complete V528 site-name stack')
        from dk4tool.patch.site_descriptions import apply_release as apply_site_descriptions

        arm_path = '/__arm9__.bin'
        site_arm, site_report = apply_site_descriptions(candidate.read_file(arm_path), site_descriptions)
        candidate.replace_file(arm_path, site_arm)
        site_report['release_config'] = site_descriptions
        site_report['release_config_sha256'] = sha256(Path(site_descriptions).read_bytes())
        relocation_checks.setdefault(arm_path, {})['site_descriptions'] = site_report
        changed_records[arm_path].extend(site_report['changed_records'])

    coin_prompts = profile_config.get('coin_game_prompts')
    if coin_prompts is not None:
        if not site_descriptions:
            raise ValueError('Coin-game prompts require the complete V534 integration stack')
        from dk4tool.patch.coin_game_prompts import apply_release as apply_coin_prompts

        arm_path = '/__arm9__.bin'
        coin_arm, coin_report = apply_coin_prompts(candidate.read_file(arm_path), coin_prompts)
        candidate.replace_file(arm_path, coin_arm)
        coin_report['release_config'] = coin_prompts
        coin_report['release_config_sha256'] = sha256(Path(coin_prompts).read_bytes())
        relocation_checks.setdefault(arm_path, {})['coin_game_prompts'] = coin_report
        changed_records[arm_path].extend(coin_report['changed_records'])

    source_grain = profile_config.get('source_plaque_grain')
    if source_grain is not None:
        if not coin_prompts:
            raise ValueError('Original plaque grain requires the complete V540 stack')
        from dk4tool.patch.source_plaque_grain import apply_release as apply_source_grain

        grain_files, grain_report = apply_source_grain(
            candidate, NdsImage.open('work/clean.nds'), source_grain)
        for path, data in grain_files.items():
            candidate.replace_file(path, data)
            file_report = next(r for r in grain_report['files'] if r['file_path'] == path)
            file_report['release_config'] = source_grain
            file_report['release_config_sha256'] = sha256(Path(source_grain).read_bytes())
            file_report['donor_file'] = grain_report['donor_file']
            file_report['source_blank_bounds'] = grain_report['source_blank_bounds']
            relocation_checks.setdefault(path, {})['source_plaque_grain'] = file_report
            changed_records[path].extend(file_report['changed_records'])

    equipment_grain = profile_config.get('equipment_source_grain')
    if equipment_grain is not None:
        if not source_grain:
            raise ValueError('Equipment source grain requires the complete V542 stack')
        from dk4tool.patch.equipment_source_grain import apply_release as apply_equipment_grain

        arm_path = '/__arm9__.bin'
        grain_arm, equipment_report = apply_equipment_grain(
            candidate.read_file(arm_path), NdsImage.open('work/clean.nds'), equipment_grain)
        candidate.replace_file(arm_path, grain_arm)
        equipment_report['release_config'] = equipment_grain
        equipment_report['release_config_sha256'] = sha256(Path(equipment_grain).read_bytes())
        relocation_checks.setdefault(arm_path, {})['equipment_source_grain'] = equipment_report
        changed_records[arm_path].extend(equipment_report['changed_records'])

    original_frames = profile_config.get('original_plaque_frames')
    if original_frames is not None:
        if not equipment_grain:
            raise ValueError('Original plaque frames require the complete V543 stack')
        from dk4tool.patch.original_plaque_frames import apply_release as apply_original_frames

        frame_files, frame_reports = apply_original_frames(
            candidate, NdsImage.open('work/clean.nds'), original_frames)
        for path, data in frame_files.items():
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            file_report = next(r for r in frame_reports if r['file_path'] == path)
            file_report['release_config'] = original_frames
            file_report['release_config_sha256'] = sha256(Path(original_frames).read_bytes())
            relocation_checks.setdefault(path, {})['original_plaque_frames'] = file_report
            changed_records.setdefault(path, []).extend(file_report['changed_records'])

    treasure_grain = profile_config.get('treasure_source_grain')
    if treasure_grain is not None:
        if not original_frames:
            raise ValueError('Treasure source grain requires the complete V544 stack')
        from dk4tool.patch.treasure_source_grain import PATH as treasure_path
        from dk4tool.patch.treasure_source_grain import apply_release as apply_treasure_grain

        treasure_data, treasure_report = apply_treasure_grain(
            candidate, NdsImage.open('work/clean.nds'), treasure_grain)
        candidate.replace_file(treasure_path, treasure_data)
        grouped.setdefault(treasure_path, [])
        treasure_report['release_config'] = treasure_grain
        treasure_report['release_config_sha256'] = sha256(Path(treasure_grain).read_bytes())
        relocation_checks.setdefault(treasure_path, {})['treasure_source_grain'] = treasure_report
        changed_records.setdefault(treasure_path, []).extend(treasure_report['changed_records'])

    source_bevels = profile_config.get('source_plaque_bevels')
    if source_bevels is not None:
        if not treasure_grain:
            raise ValueError('Clean source bevels require the complete V545 stack')
        from dk4tool.patch.source_plaque_bevels import apply_release as apply_source_bevels

        bevel_files, bevel_reports = apply_source_bevels(
            candidate, NdsImage.open('work/clean.nds'), source_bevels)
        for path, data in bevel_files.items():
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            file_report = next(r for r in bevel_reports if r['file_path'] == path)
            file_report['release_config'] = source_bevels
            file_report['release_config_sha256'] = sha256(Path(source_bevels).read_bytes())
            relocation_checks.setdefault(path, {})['source_plaque_bevels'] = file_report
            changed_records.setdefault(path, []).extend(file_report['changed_records'])

    local_texture = profile_config.get('local_plaque_texture')
    if local_texture is not None:
        if not source_bevels:
            raise ValueError('Local plaque margins require the complete source bevel stack')
        from dk4tool.patch.local_plaque_texture import apply_release as apply_local_texture

        texture_files, texture_reports = apply_local_texture(
            candidate, NdsImage.open('work/clean.nds'), local_texture)
        for path, data in texture_files.items():
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            file_report = next(r for r in texture_reports if r['file_path'] == path)
            file_report['release_config'] = local_texture
            file_report['release_config_sha256'] = sha256(Path(local_texture).read_bytes())
            relocation_checks.setdefault(path, {})['local_plaque_texture'] = file_report
            changed_records.setdefault(path, []).extend(file_report['changed_records'])

    ship_texture = profile_config.get('ship_plaque_texture')
    if ship_texture is not None:
        if not local_texture:
            raise ValueError('Ship texture requires the complete V555 stack')
        from dk4tool.patch.ship_plaque_texture import apply_release as apply_ship_texture

        ship_path, ship_data, ship_report = apply_ship_texture(
            candidate, NdsImage.open('work/clean.nds'), ship_texture)
        candidate.replace_file(ship_path, ship_data)
        grouped.setdefault(ship_path, [])
        ship_report['release_config'] = ship_texture
        ship_report['release_config_sha256'] = sha256(Path(ship_texture).read_bytes())
        relocation_checks.setdefault(ship_path, {})['ship_plaque_texture'] = ship_report
        changed_records.setdefault(ship_path, []).extend(ship_report['changed_records'])

    name_gradients = profile_config.get('name_plaque_gradients')
    if name_gradients is not None:
        if not ship_texture:
            raise ValueError('Name gradients require the complete V557 stack')
        from dk4tool.patch.name_plaque_gradients import apply_release as apply_name_gradients

        gradient_files, gradient_reports = apply_name_gradients(
            candidate, NdsImage.open('work/clean.nds'), name_gradients)
        for path, data in gradient_files.items():
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            file_report = next(r for r in gradient_reports if r['file_path'] == path)
            file_report['release_config'] = name_gradients
            file_report['release_config_sha256'] = sha256(Path(name_gradients).read_bytes())
            relocation_checks.setdefault(path, {})['name_plaque_gradients'] = file_report
            changed_records.setdefault(path, []).extend(file_report['changed_records'])

    cargo_texture = profile_config.get('cargo_banner_texture')
    if cargo_texture is not None:
        if not name_gradients:
            raise ValueError('Cargo banner repair requires the complete V558 stack')
        from dk4tool.patch.cargo_banner_texture import apply_release as apply_cargo_texture

        cargo_path = '/_pxl/tempcargo.pxl'
        cargo_data, cargo_report = apply_cargo_texture(
            candidate, NdsImage.open('work/clean.nds'), cargo_texture)
        candidate.replace_file(cargo_path, cargo_data)
        grouped.setdefault(cargo_path, [])
        cargo_report['release_config'] = cargo_texture
        cargo_report['release_config_sha256'] = sha256(Path(cargo_texture).read_bytes())
        relocation_checks.setdefault(cargo_path, {})['cargo_banner_texture'] = cargo_report
        changed_records.setdefault(cargo_path, []).extend(cargo_report['changed_records'])

    header_textures = profile_config.get('header_wood_textures')
    if header_textures is not None:
        if not cargo_texture:
            raise ValueError('Wooden headers require the complete V564 stack')
        from dk4tool.patch.cargo_banner_texture import apply_header_release

        header_files, header_reports = apply_header_release(
            candidate, NdsImage.open('work/clean.nds'), header_textures)
        for path, data in header_files.items():
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            header_report = next(r for r in header_reports if r['file_path'] == path)
            header_report['release_config'] = header_textures
            header_report['release_config_sha256'] = sha256(Path(header_textures).read_bytes())
            relocation_checks.setdefault(path, {})['header_wood_textures'] = header_report
            changed_records.setdefault(path, []).extend(header_report['changed_records'])

    marker_ownership = profile_config.get('marker_price_ownership')
    if marker_ownership is not None:
        if not header_textures:
            raise ValueError('Marker ownership requires the complete V566 stack')
        from dk4tool.patch.marker_price_ownership import apply_release as apply_marker_ownership

        marker_files, marker_reports = apply_marker_ownership(
            candidate, NdsImage.open('work/clean.nds'), marker_ownership)
        for path, data in marker_files.items():
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            marker_report = next(r for r in marker_reports if r['file_path'] == path)
            marker_report['release_config'] = marker_ownership
            marker_report['release_config_sha256'] = sha256(Path(marker_ownership).read_bytes())
            relocation_checks.setdefault(path, {})['marker_price_ownership'] = marker_report
            changed_records.setdefault(path, []).extend(marker_report['changed_records'])

    marker_headers = profile_config.get('marker_header_materials')
    if marker_headers is not None:
        if not marker_ownership:
            raise ValueError('Marker headers require the complete V569 stack')
        from dk4tool.patch.marker_header_materials import apply_release as apply_marker_headers

        header_files, header_reports = apply_marker_headers(
            candidate, NdsImage.open('work/clean.nds'), marker_headers)
        for path, data in header_files.items():
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            header_report = next(r for r in header_reports if r['file_path'] == path)
            header_report['release_config'] = marker_headers
            header_report['release_config_sha256'] = sha256(Path(marker_headers).read_bytes())
            relocation_checks.setdefault(path, {})['marker_header_materials'] = header_report
            changed_records.setdefault(path, []).extend(header_report['changed_records'])

    confirm_material = profile_config.get('confirm_button_material')
    if confirm_material is not None:
        if not marker_headers:
            raise ValueError('Confirm material requires the complete V571 stack')
        from dk4tool.patch.confirm_material import apply_release as apply_confirm_material

        confirm_path = '/_pxl/kakutei.pxl'
        confirm_data, confirm_report = apply_confirm_material(
            candidate, NdsImage.open('work/clean.nds'), confirm_material)
        candidate.replace_file(confirm_path, confirm_data)
        grouped.setdefault(confirm_path, [])
        confirm_report['release_config'] = confirm_material
        confirm_report['release_config_sha256'] = sha256(Path(confirm_material).read_bytes())
        relocation_checks.setdefault(confirm_path, {})['confirm_button_material'] = confirm_report
        changed_records.setdefault(confirm_path, []).extend(confirm_report['changed_records'])

    equipment_join = profile_config.get('equipment_grain_join')
    if equipment_join is not None:
        if not confirm_material:
            raise ValueError('Equipment wood join requires the complete V573 stack')
        from dk4tool.patch.equipment_grain_join import apply_release as apply_equipment_join

        arm_path = '/__arm9__.bin'
        arm_data, join_report = apply_equipment_join(
            candidate.read_file(arm_path), NdsImage.open('work/clean.nds'), equipment_join)
        candidate.replace_file(arm_path, arm_data)
        grouped.setdefault(arm_path, [])
        join_report['release_config'] = equipment_join
        join_report['release_config_sha256'] = sha256(Path(equipment_join).read_bytes())
        relocation_checks.setdefault(arm_path, {})['equipment_grain_join'] = join_report
        changed_records.setdefault(arm_path, []).extend(join_report['changed_records'])

    ship_quarters = profile_config.get('ship_quarters_label')
    if ship_quarters is not None:
        if not equipment_join:
            raise ValueError('Ship Quarters label requires the complete V581 stack')
        from dk4tool.patch.ship_quarters_label import apply_release as apply_ship_quarters

        quarters_path, quarters_data, quarters_report = apply_ship_quarters(
            candidate, NdsImage.open('work/clean.nds'), ship_quarters)
        candidate.replace_file(quarters_path, quarters_data)
        grouped.setdefault(quarters_path, [])
        quarters_report['release_config'] = ship_quarters
        quarters_report['release_config_sha256'] = sha256(Path(ship_quarters).read_bytes())
        relocation_checks.setdefault(quarters_path, {})['ship_quarters_label'] = quarters_report
        changed_records.setdefault(quarters_path, []).extend(quarters_report['changed_records'])

    battery_labels = profile_config.get('ship_battery_labels')
    if battery_labels is not None:
        if not ship_quarters:
            raise ValueError('Ship battery labels require the complete V591 stack')
        from dk4tool.patch.ship_battery_labels import apply_release as apply_battery_labels

        battery_files, battery_reports = apply_battery_labels(
            candidate, NdsImage.open('work/clean.nds'), battery_labels)
        for battery_path, battery_data in battery_files.items():
            battery_report = battery_reports[battery_path]
            candidate.replace_file(battery_path, battery_data)
            grouped.setdefault(battery_path, [])
            battery_report['release_config'] = battery_labels
            battery_report['release_config_sha256'] = sha256(Path(battery_labels).read_bytes())
            relocation_checks.setdefault(battery_path, {})['ship_battery_labels'] = battery_report
            changed_records.setdefault(battery_path, []).extend(battery_report['changed_records'])

    keyboard_labels = profile_config.get('keyboard_page_labels')
    if keyboard_labels is not None:
        if not battery_labels:
            raise ValueError('Keyboard page labels require the complete V593 stack')
        from dk4tool.patch.keyboard_page_labels import apply_release as apply_keyboard_labels

        keyboard_path = '/__arm9__.bin'
        keyboard_data, keyboard_report = apply_keyboard_labels(candidate.read_file(keyboard_path), keyboard_labels)
        candidate.replace_file(keyboard_path, keyboard_data)
        grouped.setdefault(keyboard_path, [])
        keyboard_report['release_config'] = keyboard_labels
        keyboard_report['release_config_sha256'] = sha256(Path(keyboard_labels).read_bytes())
        relocation_checks.setdefault(keyboard_path, {})['keyboard_page_labels'] = keyboard_report
        changed_records.setdefault(keyboard_path, []).extend(keyboard_report['changed_records'])

    race_waiting_label = profile_config.get('race_waiting_label')
    if race_waiting_label is not None:
        if not keyboard_labels:
            raise ValueError('Race waiting label requires the complete V599 stack')
        from dk4tool.patch.race_waiting_label import apply_release as apply_race_waiting_label

        waiting_path = '/__arm9__.bin'
        waiting_data, waiting_report = apply_race_waiting_label(candidate.read_file(waiting_path), race_waiting_label)
        candidate.replace_file(waiting_path, waiting_data)
        grouped.setdefault(waiting_path, [])
        waiting_report['release_config'] = race_waiting_label
        waiting_report['release_config_sha256'] = sha256(Path(race_waiting_label).read_bytes())
        relocation_checks.setdefault(waiting_path, {})['race_waiting_label'] = waiting_report
        changed_records.setdefault(waiting_path, []).extend(waiting_report['changed_records'])

    village_portrait_wrap = profile_config.get('village_portrait_wrap')
    if village_portrait_wrap is not None:
        if not race_waiting_label:
            raise ValueError('Village portrait wrapping requires the complete V604 stack')
        from dk4tool.patch.village_portrait_wrap import apply_release as apply_village_portrait_wrap

        village_path = '/__arm9__.bin'
        village_data, village_report = apply_village_portrait_wrap(candidate.read_file(village_path), village_portrait_wrap)
        candidate.replace_file(village_path, village_data)
        grouped.setdefault(village_path, [])
        village_report['release_config'] = village_portrait_wrap
        village_report['release_config_sha256'] = sha256(Path(village_portrait_wrap).read_bytes())
        relocation_checks.setdefault(village_path, {})['village_portrait_wrap'] = village_report
        changed_records.setdefault(village_path, []).extend(village_report['changed_records'])

    village_ui_text = profile_config.get('village_ui_text')
    if village_ui_text is not None:
        if not village_portrait_wrap:
            raise ValueError('Village UI text requires the complete V608 stack')
        village_ui_version = profile_config.get('village_ui_text_version', 1)
        if village_ui_version == 1:
            from dk4tool.patch.village_ui_text import apply_release as apply_village_ui_text
        elif village_ui_version == 2:
            from dk4tool.patch.village_ui_compact import apply_release as apply_village_ui_text
        else:
            raise ValueError('Unknown village UI text layout version')

        village_arm_path, village_route_path = '/__arm9__.bin', '/data/SC2.DK4'
        village_arm, village_route, village_ui_report = apply_village_ui_text(
            candidate.read_file(village_arm_path), candidate.read_file(village_route_path), village_ui_text)
        candidate.replace_file(village_arm_path, village_arm)
        candidate.replace_file(village_route_path, village_route)
        village_ui_report['release_config'] = village_ui_text
        village_ui_report['release_config_sha256'] = sha256(Path(village_ui_text).read_bytes())
        for village_path in (village_arm_path, village_route_path):
            grouped.setdefault(village_path, [])
            relocation_checks.setdefault(village_path, {})['village_ui_text'] = village_ui_report
        changed_records.setdefault(village_arm_path, []).extend(r['id'] for r in village_ui_report['placements'])
        changed_records.setdefault(village_route_path, []).extend(r['id'] for r in village_ui_report['same_width_name_corrections'])

    regional_plaques = profile_config.get('regional_fleet_plaques')
    if regional_plaques is not None:
        if not village_ui_text or village_ui_version != 2:
            raise ValueError('Regional fleet plaques require the complete compact V610 stack')
        from dk4tool.patch.regional_fleet_plaques import apply_release as apply_regional_plaques

        regional_outputs, regional_report = apply_regional_plaques(
            candidate, NdsImage.open('work/clean.nds'), regional_plaques)
        regional_report['release_config'] = regional_plaques
        regional_report['release_config_sha256'] = sha256(Path(regional_plaques).read_bytes())
        for regional_path, regional_data in regional_outputs.items():
            candidate.replace_file(regional_path, regional_data)
            grouped.setdefault(regional_path, [])
            relocation_checks.setdefault(regional_path, {})['regional_fleet_plaques'] = regional_report
            changed_records.setdefault(regional_path, []).extend(r['id'] for r in regional_report['records'])

    save_load_plaques = profile_config.get('save_load_plaques')
    if save_load_plaques is not None:
        if not regional_plaques:
            raise ValueError('Save/Load plaques require the complete V611 stack')
        from dk4tool.patch.save_load_plaques import apply_release as apply_save_load_plaques

        save_outputs, save_report = apply_save_load_plaques(
            candidate, NdsImage.open('work/clean.nds'), save_load_plaques)
        save_report['release_config'] = save_load_plaques
        save_report['release_config_sha256'] = sha256(Path(save_load_plaques).read_bytes())
        for save_path, save_data in save_outputs.items():
            candidate.replace_file(save_path, save_data)
            grouped.setdefault(save_path, [])
            relocation_checks.setdefault(save_path, {})['save_load_plaques'] = save_report
            changed_records.setdefault(save_path, []).extend(r['id'] for r in save_report['records'])

    golden_plaques = profile_config.get('golden_route_plaques')
    if golden_plaques is not None:
        if not save_load_plaques:
            raise ValueError('Golden Route plaques require the complete V612 stack')
        from dk4tool.patch.golden_route_plaques import apply_release as apply_golden_plaques

        golden_outputs, golden_report = apply_golden_plaques(
            candidate, NdsImage.open('work/clean.nds'), golden_plaques)
        for golden_path, golden_data in golden_outputs.items():
            candidate.replace_file(golden_path, golden_data)
            grouped.setdefault(golden_path, [])
            relocation_checks.setdefault(golden_path, {})['golden_route_plaques'] = {
                'release_config': golden_plaques,
                'release_config_sha256': sha256(Path(golden_plaques).read_bytes()),
                'files': golden_report,
            }
            changed_records.setdefault(golden_path, []).extend(
                r['id'] for report in golden_report if report['file_path'] == golden_path
                for r in report['records'])

    ship_name_heading = profile_config.get('ship_name_heading')
    if ship_name_heading is not None:
        if not golden_plaques:
            raise ValueError('Ship Name headings require the complete V613 stack')
        from dk4tool.patch.ship_name_heading import apply_release as apply_ship_name_heading

        name_arm, name_report = apply_ship_name_heading(
            candidate.read_file('/__arm9__.bin'), ship_name_heading)
        name_report['release_config'] = ship_name_heading
        name_report['release_config_sha256'] = sha256(Path(ship_name_heading).read_bytes())
        candidate.replace_file('/__arm9__.bin', name_arm)
        grouped.setdefault('/__arm9__.bin', [])
        relocation_checks.setdefault('/__arm9__.bin', {})['ship_name_heading'] = name_report
        changed_records.setdefault('/__arm9__.bin', []).extend(name_report['changed_records'])

    shipyard_ui_labels = profile_config.get('shipyard_ui_labels')
    regional_policy_prompts = profile_config.get('regional_policy_prompts')
    if bool(shipyard_ui_labels) != bool(regional_policy_prompts):
        raise ValueError('Shipyard and regional policy labels/prompts require their complete coordinated family')
    if shipyard_ui_labels:
        if not golden_plaques or ship_name_heading:
            raise ValueError('Complete Shipyard UI requires the full V613 stack and replaces the narrow heading stage')
        from dk4tool.patch.regional_policy_prompts import (
            apply_release as apply_regional_policy_prompts,
        )
        from dk4tool.patch.shipyard_ui_labels import apply_release as apply_shipyard_ui_labels

        ship_arm, ship_report = apply_shipyard_ui_labels(candidate.read_file('/__arm9__.bin'), shipyard_ui_labels)
        regional_common, regional_arm, regional_report = apply_regional_policy_prompts(
            candidate.read_file('/COMMON/MESFILE.DK4'), ship_arm, regional_policy_prompts)
        for internal_path, data in (('/__arm9__.bin', regional_arm), ('/COMMON/MESFILE.DK4', regional_common)):
            candidate.replace_file(internal_path, data)
            grouped.setdefault(internal_path, [])
            relocation_checks.setdefault(internal_path, {})['regional_policy_prompts'] = {
                'release_config': regional_policy_prompts,
                'release_config_sha256': sha256(Path(regional_policy_prompts).read_bytes()), 'proof': regional_report}
            changed_records.setdefault(internal_path, []).extend(regional_report['changed_records'])
        relocation_checks['/__arm9__.bin']['shipyard_ui_labels'] = {
            'release_config': shipyard_ui_labels,
            'release_config_sha256': sha256(Path(shipyard_ui_labels).read_bytes()), 'proof': ship_report}
        changed_records['/__arm9__.bin'].extend(ship_report['changed_records'])

    regional_policy_wrap = profile_config.get('regional_policy_wrap')
    if regional_policy_wrap is not None:
        if not regional_policy_prompts or not shipyard_ui_labels:
            raise ValueError('Regional policy wrapping requires the complete V615 UI/message family')
        from dk4tool.patch.regional_policy_wrap import apply_release as apply_regional_policy_wrap

        wrap_arm, wrap_report = apply_regional_policy_wrap(candidate.read_file('/__arm9__.bin'), regional_policy_wrap)
        candidate.replace_file('/__arm9__.bin', wrap_arm)
        grouped.setdefault('/__arm9__.bin', [])
        relocation_checks.setdefault('/__arm9__.bin', {})['regional_policy_wrap'] = {
            'release_config': regional_policy_wrap,
            'release_config_sha256': sha256(Path(regional_policy_wrap).read_bytes()), 'proof': wrap_report}
        changed_records.setdefault('/__arm9__.bin', []).extend(wrap_report['changed_records'])

    regional_assignment_wrap = profile_config.get('regional_assignment_wrap')
    regional_fleet_ordinal_label = profile_config.get('regional_fleet_ordinal_label')
    if bool(regional_assignment_wrap) != bool(regional_fleet_ordinal_label):
        raise ValueError('Regional assignment guards and numbered-fleet label require their complete coordinated family')
    if regional_assignment_wrap:
        if not regional_policy_wrap:
            raise ValueError('Regional assignment repair requires the complete V616 stack')
        from dk4tool.patch.regional_assignment_wrap import (
            apply_release as apply_regional_assignment_wrap,
        )
        from dk4tool.patch.regional_fleet_ordinal_label import (
            apply_release as apply_regional_fleet_ordinal_label,
        )

        assignment_arm, assignment_report = apply_regional_assignment_wrap(
            candidate.read_file('/__arm9__.bin'), regional_assignment_wrap)
        ordinal_arm, ordinal_report = apply_regional_fleet_ordinal_label(assignment_arm, regional_fleet_ordinal_label)
        candidate.replace_file('/__arm9__.bin', ordinal_arm)
        grouped.setdefault('/__arm9__.bin', [])
        for stage, config_path, stage_report in (('regional_assignment_wrap', regional_assignment_wrap, assignment_report),
                                                 ('regional_fleet_ordinal_label', regional_fleet_ordinal_label, ordinal_report)):
            relocation_checks.setdefault('/__arm9__.bin', {})[stage] = {
                'release_config': config_path, 'release_config_sha256': sha256(Path(config_path).read_bytes()), 'proof': stage_report}
            changed_records.setdefault('/__arm9__.bin', []).extend(stage_report['changed_records'])

    compact_bitmap_origin = profile_config.get('compact_bitmap_origin')
    if compact_bitmap_origin:
        if not regional_assignment_wrap or not regional_fleet_ordinal_label:
            raise ValueError('Compact bitmap origins require the complete V617 stack')
        from dk4tool.patch.compact_bitmap_origin import apply_release as apply_compact_bitmap_origin

        origin_arm, origin_report = apply_compact_bitmap_origin(
            candidate.read_file('/__arm9__.bin'), compact_bitmap_origin)
        candidate.replace_file('/__arm9__.bin', origin_arm)
        grouped.setdefault('/__arm9__.bin', [])
        relocation_checks.setdefault('/__arm9__.bin', {})['compact_bitmap_origin'] = {
            'release_config': compact_bitmap_origin,
            'release_config_sha256': sha256(Path(compact_bitmap_origin).read_bytes()),
            'proof': origin_report}
        changed_records.setdefault('/__arm9__.bin', []).extend(origin_report['changed_records'])

    plaza_distribution_label = profile_config.get('plaza_distribution_label')
    if plaza_distribution_label:
        if not compact_bitmap_origin:
            raise ValueError('Square distribution labels require complete V621')
        from dk4tool.patch.plaza_distribution_label import (
            apply_release as apply_plaza_distribution_label,
        )

        plaza_arm, plaza_report = apply_plaza_distribution_label(
            candidate.read_file('/__arm9__.bin'), plaza_distribution_label)
        candidate.replace_file('/__arm9__.bin', plaza_arm)
        grouped.setdefault('/__arm9__.bin', [])
        relocation_checks.setdefault('/__arm9__.bin', {})['plaza_distribution_label'] = {
            'release_config': plaza_distribution_label,
            'release_config_sha256': sha256(Path(plaza_distribution_label).read_bytes()),
            'proof': plaza_report}
        changed_records.setdefault('/__arm9__.bin', []).extend(plaza_report['changed_records'])

    tavern_scheme_labels = profile_config.get('tavern_scheme_labels')
    if tavern_scheme_labels:
        if not plaza_distribution_label:
            raise ValueError('Tavern scheme labels require complete V623')
        from dk4tool.patch.tavern_scheme_labels import apply_release as apply_tavern_scheme_labels

        tavern_arm, tavern_report = apply_tavern_scheme_labels(
            candidate.read_file('/__arm9__.bin'), tavern_scheme_labels)
        candidate.replace_file('/__arm9__.bin', tavern_arm)
        grouped.setdefault('/__arm9__.bin', [])
        relocation_checks.setdefault('/__arm9__.bin', {})['tavern_scheme_labels'] = {
            'release_config': tavern_scheme_labels,
            'release_config_sha256': sha256(Path(tavern_scheme_labels).read_bytes()),
            'proof': tavern_report}
        changed_records.setdefault('/__arm9__.bin', []).extend(tavern_report['changed_records'])

    tavern_scheme_context = profile_config.get('tavern_scheme_context')
    if tavern_scheme_context:
        if not tavern_scheme_labels:
            raise ValueError('Scheme contexts require complete V624')
        from dk4tool.patch.tavern_scheme_context import apply_release as apply_tavern_scheme_context

        scheme_common, scheme_arm, scheme_report = apply_tavern_scheme_context(
            candidate.read_file('/COMMON/MESFILE.DK4'), candidate.read_file('/__arm9__.bin'),
            tavern_scheme_context)
        candidate.replace_file('/COMMON/MESFILE.DK4', scheme_common)
        candidate.replace_file('/__arm9__.bin', scheme_arm)
        for component in ('/COMMON/MESFILE.DK4', '/__arm9__.bin'):
            grouped.setdefault(component, [])
            relocation_checks.setdefault(component, {})['tavern_scheme_context'] = {
                'release_config': tavern_scheme_context,
                'release_config_sha256': sha256(Path(tavern_scheme_context).read_bytes()),
                'proof': scheme_report}
            changed_records.setdefault(component, []).extend(scheme_report['changed_records'])

    tavern_strategist_wrap = profile_config.get('tavern_strategist_wrap')
    if tavern_strategist_wrap:
        if not tavern_scheme_context:
            raise ValueError('Queued Strategist wrapping requires complete V625')
        from dk4tool.patch.tavern_strategist_wrap import (
            apply_release as apply_tavern_strategist_wrap,
        )

        strategist_arm, strategist_report = apply_tavern_strategist_wrap(
            candidate.read_file('/__arm9__.bin'), tavern_strategist_wrap)
        candidate.replace_file('/__arm9__.bin', strategist_arm)
        grouped.setdefault('/__arm9__.bin', [])
        relocation_checks.setdefault('/__arm9__.bin', {})['tavern_strategist_wrap'] = {
            'release_config': tavern_strategist_wrap,
            'release_config_sha256': sha256(Path(tavern_strategist_wrap).read_bytes()),
            'proof': strategist_report}
        changed_records.setdefault('/__arm9__.bin', []).extend(strategist_report['changed_records'])

    tavern_recruitment = profile_config.get('tavern_recruitment')
    if tavern_recruitment:
        if not tavern_strategist_wrap:
            raise ValueError('Recruitment voice repair requires complete V626')
        from dk4tool.patch.tavern_recruitment import apply_release as apply_tavern_recruitment

        recruit_common, recruit_arm, recruit_report = apply_tavern_recruitment(
            candidate.read_file('/COMMON/MESFILE.DK4'), candidate.read_file('/__arm9__.bin'),
            tavern_recruitment)
        candidate.replace_file('/COMMON/MESFILE.DK4', recruit_common)
        candidate.replace_file('/__arm9__.bin', recruit_arm)
        for component in ('/COMMON/MESFILE.DK4', '/__arm9__.bin'):
            grouped.setdefault(component, [])
            relocation_checks.setdefault(component, {})['tavern_recruitment'] = {
                'release_config': tavern_recruitment,
                'release_config_sha256': sha256(Path(tavern_recruitment).read_bytes()),
                'proof': recruit_report}
            changed_records.setdefault(component, []).extend(recruit_report['changed_records'])

    ship_info_title_crop = profile_config.get('ship_info_title_crop')
    if ship_info_title_crop:
        if not tavern_recruitment:
            raise ValueError('Ship Info title cropping requires complete V627')
        from dk4tool.patch.ship_info_title_crop import apply_release as apply_ship_info_title_crop

        title_arm, title_report = apply_ship_info_title_crop(
            candidate.read_file('/__arm9__.bin'), ship_info_title_crop)
        candidate.replace_file('/__arm9__.bin', title_arm)
        grouped.setdefault('/__arm9__.bin', [])
        relocation_checks.setdefault('/__arm9__.bin', {})['ship_info_title_crop'] = {
            'release_config': ship_info_title_crop,
            'release_config_sha256': sha256(Path(ship_info_title_crop).read_bytes()),
            'proof': title_report}
        changed_records.setdefault('/__arm9__.bin', []).extend(title_report['changed_records'])

    commodity_fidelity = profile_config.get('commodity_fidelity')
    if commodity_fidelity:
        if not ship_info_title_crop:
            raise ValueError('Complete commodity meanings require the complete V633 stack')
        from dk4tool.patch.commodity_fidelity import apply_release as apply_commodity_fidelity

        commodity_arm, commodity_report = apply_commodity_fidelity(
            candidate.read_file('/__arm9__.bin'), NdsImage.open('work/clean.nds').read_file('/__arm9__.bin'),
            commodity_fidelity)
        candidate.replace_file('/__arm9__.bin', commodity_arm)
        grouped.setdefault('/__arm9__.bin', [])
        relocation_checks.setdefault('/__arm9__.bin', {})['commodity_fidelity'] = {
            'release_config': commodity_fidelity,
            'release_config_sha256': sha256(Path(commodity_fidelity).read_bytes()),
            'proof': commodity_report}
        changed_records.setdefault('/__arm9__.bin', []).extend(commodity_report['changed_records'])

    region_name_boundaries = profile_config.get('region_name_boundaries')
    if region_name_boundaries:
        if not commodity_fidelity:
            raise ValueError('Region-name boundary repair requires the complete V636 stack')
        from dk4tool.patch.region_name_boundaries import (
            apply_release as apply_region_name_boundaries,
        )

        region_arm, region_report = apply_region_name_boundaries(
            candidate.read_file('/__arm9__.bin'), NdsImage.open('work/clean.nds').read_file('/__arm9__.bin'),
            region_name_boundaries)
        candidate.replace_file('/__arm9__.bin', region_arm)
        grouped.setdefault('/__arm9__.bin', [])
        relocation_checks.setdefault('/__arm9__.bin', {})['region_name_boundaries'] = {
            'release_config': region_name_boundaries,
            'release_config_sha256': sha256(Path(region_name_boundaries).read_bytes()),
            'proof': region_report}
        changed_records.setdefault('/__arm9__.bin', []).extend(region_report['changed_records'])

    captain_prompt_wrap = profile_config.get('captain_prompt_wrap')
    if captain_prompt_wrap:
        if not region_name_boundaries:
            raise ValueError('Captain instruction wrapping requires the complete V640 stack')
        from dk4tool.patch.captain_prompt_wrap import apply_release as apply_captain_prompt_wrap

        captain_arm, captain_report = apply_captain_prompt_wrap(
            candidate.read_file('/__arm9__.bin'), captain_prompt_wrap)
        candidate.replace_file('/__arm9__.bin', captain_arm)
        grouped.setdefault('/__arm9__.bin', [])
        relocation_checks.setdefault('/__arm9__.bin', {})['captain_prompt_wrap'] = {
            'release_config': captain_prompt_wrap,
            'release_config_sha256': sha256(Path(captain_prompt_wrap).read_bytes()),
            'proof': captain_report}
        changed_records.setdefault('/__arm9__.bin', []).extend(captain_report['changed_records'])

    queued_portrait_wrap = profile_config.get('queued_portrait_wrap')
    if queued_portrait_wrap:
        if not captain_prompt_wrap:
            raise ValueError('Shared queued portrait wrapping requires the complete V651 stack')
        from dk4tool.patch.queued_portrait_wrap import apply_release as apply_queued_portrait_wrap

        queued_arm, queued_report = apply_queued_portrait_wrap(
            candidate.read_file('/__arm9__.bin'), queued_portrait_wrap)
        candidate.replace_file('/__arm9__.bin', queued_arm)
        grouped.setdefault('/__arm9__.bin', [])
        relocation_checks.setdefault('/__arm9__.bin', {})['queued_portrait_wrap'] = {
            'release_config': queued_portrait_wrap,
            'release_config_sha256': sha256(Path(queued_portrait_wrap).read_bytes()),
            'proof': queued_report}
        changed_records.setdefault('/__arm9__.bin', []).extend(queued_report['changed_records'])

    village_port_consistency = profile_config.get('village_port_consistency')
    if village_port_consistency:
        if not queued_portrait_wrap:
            raise ValueError('Village port consistency requires the complete V653 stack')
        from dk4tool.patch.village_port_consistency import (
            apply_release as apply_village_port_consistency,
        )

        village_arm, village_report = apply_village_port_consistency(
            candidate.read_file('/__arm9__.bin'), village_port_consistency)
        candidate.replace_file('/__arm9__.bin', village_arm)
        grouped.setdefault('/__arm9__.bin', [])
        relocation_checks.setdefault('/__arm9__.bin', {})['village_port_consistency'] = {
            'release_config': village_port_consistency,
            'release_config_sha256': sha256(Path(village_port_consistency).read_bytes()),
            'proof': village_report}
        changed_records.setdefault('/__arm9__.bin', []).extend(
            [f"Town metadata name {row['town']}" for row in village_report['five_original_Town_name_pointer_aliases']]
            + [f"Village clue {row['index']}" for row in village_report['two_reflowed_clues']])

    wedding_dialogue_cleanup = profile_config.get('wedding_dialogue_cleanup')
    if wedding_dialogue_cleanup:
        if not village_port_consistency:
            raise ValueError('Wedding dialogue cleanup requires the complete V666 stack')
        from dk4tool.patch.wedding_dialogue_cleanup import (
            apply_release as apply_wedding_dialogue_cleanup,
        )

        wedding_sc2, wedding_report = apply_wedding_dialogue_cleanup(
            candidate.read_file('/data/SC2.DK4'), baseline.read_file('/data/SC2.DK4'),
            wedding_dialogue_cleanup)
        candidate.replace_file('/data/SC2.DK4', wedding_sc2)
        grouped.setdefault('/data/SC2.DK4', [])
        relocation_checks.setdefault('/data/SC2.DK4', {})['wedding_dialogue_cleanup'] = {
            'release_config': wedding_dialogue_cleanup,
            'release_config_sha256': sha256(Path(wedding_dialogue_cleanup).read_bytes()),
            'proof': wedding_report}
        existing = changed_records.setdefault('/data/SC2.DK4', [])
        existing.extend(record for record in wedding_report['changed_records'] if record not in existing)

    story_literal_percent_safety = profile_config.get('story_literal_percent_safety')
    if story_literal_percent_safety:
        if not wedding_dialogue_cleanup:
            raise ValueError('Story percent repair requires the complete V678 stack')
        from dk4tool.patch.story_literal_percent import apply_release as apply_story_literal_percent

        percent_config = json.loads(Path(story_literal_percent_safety).read_text(encoding='utf-8'))
        percent_paths = tuple(percent_config['files'])
        percent_files, percent_report = apply_story_literal_percent(
            {p: candidate.read_file(p) for p in percent_paths},
            {p: baseline.read_file(p) for p in percent_paths}, story_literal_percent_safety)
        for path, data in percent_files.items():
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            relocation_checks.setdefault(path, {})['story_literal_percent_safety'] = {
                'release_config': story_literal_percent_safety,
                'release_config_sha256': sha256(Path(story_literal_percent_safety).read_bytes()),
                'proof': percent_report[path]}
            existing = changed_records.setdefault(path, [])
            existing.extend(r for r in percent_report[path]['changed_records'] if r not in existing)

    navigator_captain_filter = profile_config.get('navigator_captain_filter')
    if navigator_captain_filter:
        from dk4tool.patch.navigator_captain_filter import apply_release as apply_captain_filter

        path = '/__arm9__.bin'
        filter_arm9, filter_report = apply_captain_filter(
            candidate.read_file(path), NdsImage.open('work/clean.nds').read_file(path),
            navigator_captain_filter)
        candidate.replace_file(path, filter_arm9)
        grouped.setdefault(path, [])
        relocation_checks.setdefault(path, {})['navigator_captain_filter'] = {
            'release_config': navigator_captain_filter,
            'release_config_sha256': sha256(Path(navigator_captain_filter).read_bytes()),
            'proof': filter_report}
        existing = changed_records.setdefault(path, [])
        existing.extend(r for r in filter_report['changed_records'] if r not in existing)

    refit_help_release = profile_config.get('refit_help_release')
    if refit_help_release:
        from dk4tool.patch.refit_help_release import apply_release as apply_refit_help

        path = '/__arm9__.bin'
        refit_arm, refit_report = apply_refit_help(candidate.read_file(path), refit_help_release)
        candidate.replace_file(path, refit_arm)
        grouped.setdefault(path, [])
        relocation_checks.setdefault(path, {})['refit_help_release'] = {
            'release_config': refit_help_release,
            'release_config_sha256': sha256(Path(refit_help_release).read_bytes()),
            'proof': refit_report}
        existing = changed_records.setdefault(path, [])
        existing.extend(r for r in refit_report['changed_records'] if r not in existing)

    refit_help_repack = profile_config.get('refit_help_repack')
    if refit_help_repack:
        from dk4tool.patch.refit_help_repack import apply_release as apply_refit_help_repack

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        common_data, arm_data, refit_report = apply_refit_help_repack(
            candidate.read_file(common_path), candidate.read_file(arm_path), refit_help_repack)
        for path, data in ((common_path, common_data), (arm_path, arm_data)):
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            relocation_checks.setdefault(path, {})['refit_help_repack'] = {
                'release_config': refit_help_repack,
                'release_config_sha256': sha256(Path(refit_help_repack).read_bytes()),
                'proof': refit_report}
            existing = changed_records.setdefault(path, [])
            existing.extend(r for r in refit_report['changed_records'] if r not in existing)

    refit_help_layout = profile_config.get('refit_help_layout')
    if refit_help_layout:
        from dk4tool.patch.refit_help_layout_v2 import apply_release as apply_refit_help_layout

        path = '/__arm9__.bin'
        layout_arm, layout_report = apply_refit_help_layout(candidate.read_file(path), refit_help_layout)
        candidate.replace_file(path, layout_arm)
        grouped.setdefault(path, [])
        relocation_checks.setdefault(path, {})['refit_help_layout'] = {
            'release_config': refit_help_layout,
            'release_config_sha256': sha256(Path(refit_help_layout).read_bytes()),
            'proof': layout_report}
        existing = changed_records.setdefault(path, [])
        existing.extend(r for r in layout_report['changed_records'] if r not in existing)

    shop_business_editorial = profile_config.get('shop_business_editorial')
    if shop_business_editorial:
        from dk4tool.patch.shop_business_editorial import (
            apply_release as apply_shop_business_editorial,
        )

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        shop_common, shop_arm, shop_report = apply_shop_business_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), shop_business_editorial)
        for path, data in ((common_path, shop_common), (arm_path, shop_arm)):
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            relocation_checks.setdefault(path, {})['shop_business_editorial'] = {
                'release_config': shop_business_editorial,
                'release_config_sha256': sha256(Path(shop_business_editorial).read_bytes()),
                'proof': shop_report}
        changed_records.setdefault(common_path, []).extend(shop_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('COMMON_SHOP_BUSINESS_NATIVE_OFFSET_FIELDS')

    giveaway_editorial = profile_config.get('giveaway_editorial')
    if giveaway_editorial:
        from dk4tool.patch.giveaway_editorial import apply_release as apply_giveaway_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        giveaway_common, giveaway_arm, giveaway_report = apply_giveaway_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), giveaway_editorial)
        for path, data in ((common_path, giveaway_common), (arm_path, giveaway_arm)):
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            relocation_checks.setdefault(path, {})['giveaway_editorial'] = {
                'release_config': giveaway_editorial,
                'release_config_sha256': sha256(Path(giveaway_editorial).read_bytes()),
                'proof': giveaway_report}
        changed_records.setdefault(common_path, []).extend(giveaway_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('COMMON_GIVEAWAY_NATIVE_OFFSET_FIELDS')

    product_pitches_editorial = profile_config.get('product_pitches_editorial')
    if product_pitches_editorial:
        from dk4tool.patch.product_pitches_editorial import apply_release as apply_product_pitches

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        pitches_common, pitches_arm, pitches_report = apply_product_pitches(
            candidate.read_file(common_path), candidate.read_file(arm_path), product_pitches_editorial)
        for path, data in ((common_path, pitches_common), (arm_path, pitches_arm)):
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            relocation_checks.setdefault(path, {})['product_pitches_editorial'] = {
                'release_config': product_pitches_editorial,
                'release_config_sha256': sha256(Path(product_pitches_editorial).read_bytes()),
                'proof': pitches_report}
        changed_records.setdefault(common_path, []).extend(pitches_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend([
            'COMMON_PRODUCT_PITCH_NATIVE_OFFSET_FIELDS', 'COMMON_PRODUCT_PITCH_SCOPED_RUNTIME_WRAP'])

    country_editorial = profile_config.get('country_editorial')
    if country_editorial:
        from dk4tool.patch.country_editorial import apply_release as apply_country_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        country_common, country_arm, country_report = apply_country_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), country_editorial)
        for path, data in ((common_path, country_common), (arm_path, country_arm)):
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            relocation_checks.setdefault(path, {})['country_editorial'] = {
                'release_config': country_editorial,
                'release_config_sha256': sha256(Path(country_editorial).read_bytes()),
                'proof': country_report}
        changed_records.setdefault(common_path, []).extend(country_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend([
            'COMMON_COUNTRY_NATIVE_OFFSET_FIELDS', 'COMMON_COUNTRY_SCOPED_RUNTIME_WRAP'])

    regional_rumors = profile_config.get('regional_rumors')
    if regional_rumors:
        from dk4tool.patch.regional_rumors import apply_release as apply_regional_rumors

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        rumor_common, rumor_arm, rumor_report = apply_regional_rumors(
            candidate.read_file(common_path), candidate.read_file(arm_path), regional_rumors)
        for path, data in ((common_path, rumor_common), (arm_path, rumor_arm)):
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            relocation_checks.setdefault(path, {})['regional_rumors'] = {
                'release_config': regional_rumors,
                'release_config_sha256': sha256(Path(regional_rumors).read_bytes()),
                'proof': rumor_report}
        changed_records.setdefault(common_path, []).extend(rumor_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend([
            'COMMON_REGIONAL_RUMOR_NATIVE_OFFSET_FIELDS', 'COMMON_REGIONAL_RUMOR_SCOPED_RUNTIME_WRAP'])

    town_events_editorial = profile_config.get('town_events_editorial')
    if town_events_editorial:
        from dk4tool.patch.town_events_editorial import apply_release as apply_town_events

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        event_common, event_arm, event_report = apply_town_events(
            candidate.read_file(common_path), candidate.read_file(arm_path), town_events_editorial)
        for path, data in ((common_path, event_common), (arm_path, event_arm)):
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            relocation_checks.setdefault(path, {})['town_events_editorial'] = {
                'release_config': town_events_editorial,
                'release_config_sha256': sha256(Path(town_events_editorial).read_bytes()),
                'proof': event_report}
        changed_records.setdefault(common_path, []).extend(event_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend([
            'COMMON_TOWN_EVENT_NATIVE_OFFSETS', 'COMMON_TOWN_EVENT_SCOPED_RUNTIME_WRAP'])

    town_responses_editorial = profile_config.get('town_responses_editorial')
    if town_responses_editorial:
        from dk4tool.patch.town_responses_editorial import apply_release as apply_town_responses

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        response_common, response_arm, response_report = apply_town_responses(
            candidate.read_file(common_path), candidate.read_file(arm_path), town_responses_editorial)
        for path, data in ((common_path, response_common), (arm_path, response_arm)):
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            relocation_checks.setdefault(path, {})['town_responses_editorial'] = {
                'release_config': town_responses_editorial,
                'release_config_sha256': sha256(Path(town_responses_editorial).read_bytes()),
                'proof': response_report}
        changed_records.setdefault(common_path, []).extend(response_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend([
            'COMMON_TOWN_RESPONSE_NATIVE_OFFSETS', 'COMMON_TOWN_RESPONSE_SCOPED_RUNTIME_WRAP'])

    specialty_question_editorial = profile_config.get('specialty_question_editorial')
    if specialty_question_editorial:
        from dk4tool.patch.specialty_question_editorial import apply_release as apply_specialty_question

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        specialty_common, specialty_arm, specialty_report = apply_specialty_question(
            candidate.read_file(common_path), candidate.read_file(arm_path), specialty_question_editorial)
        for path, data in ((common_path, specialty_common), (arm_path, specialty_arm)):
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            relocation_checks.setdefault(path, {})['specialty_question_editorial'] = {
                'release_config': specialty_question_editorial,
                'release_config_sha256': sha256(Path(specialty_question_editorial).read_bytes()),
                'proof': specialty_report}
        changed_records.setdefault(common_path, []).extend(specialty_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend([
            'COMMON_SPECIALTY_QUESTION_NATIVE_OFFSETS', 'COMMON_SPECIALTY_QUESTION_SCOPED_WRAP'])

    market_replies_editorial = profile_config.get('market_replies_editorial')
    if market_replies_editorial:
        from dk4tool.patch.market_replies_editorial import apply_release as apply_market_replies

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        market_common, market_arm, market_report = apply_market_replies(
            candidate.read_file(common_path), candidate.read_file(arm_path), market_replies_editorial)
        for path, data in ((common_path, market_common), (arm_path, market_arm)):
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            relocation_checks.setdefault(path, {})['market_replies_editorial'] = {
                'release_config': market_replies_editorial,
                'release_config_sha256': sha256(Path(market_replies_editorial).read_bytes()),
                'proof': market_report}
        changed_records.setdefault(common_path, []).extend(market_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('COMMON_MARKET_REPLIES_COMPLETE_SELECTION_MAP')

    category_dialogue_editorial = profile_config.get('category_dialogue_editorial')
    if category_dialogue_editorial:
        from dk4tool.patch.category_dialogue_editorial import apply_release as apply_category_dialogue

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        category_common, category_arm, category_report = apply_category_dialogue(
            candidate.read_file(common_path), candidate.read_file(arm_path), category_dialogue_editorial)
        for path, data in ((common_path, category_common), (arm_path, category_arm)):
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            relocation_checks.setdefault(path, {})['category_dialogue_editorial'] = {
                'release_config': category_dialogue_editorial,
                'release_config_sha256': sha256(Path(category_dialogue_editorial).read_bytes()),
                'proof': category_report}
        changed_records.setdefault(common_path, []).extend(category_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend([
            'COMMON_CATEGORY730_NATIVE_OFFSET', 'FULL_CATEGORY730_COMPACT_MENU_LOOKUP'])

    market_stock_editorial_v2 = profile_config.get('market_stock_editorial_v2')
    assert not (market_stock_editorial_v2 and profile_config.get('market_stock_editorial'))
    market_stock_editorial = market_stock_editorial_v2 or profile_config.get('market_stock_editorial')
    if market_stock_editorial:
        if market_stock_editorial_v2:
            from dk4tool.patch.market_stock_editorial_v2 import apply_release as apply_market_stock
        else:
            from dk4tool.patch.market_stock_editorial import apply_release as apply_market_stock

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        stock_common, stock_arm, stock_report = apply_market_stock(
            candidate.read_file(common_path), candidate.read_file(arm_path), market_stock_editorial)
        for path, data in ((common_path, stock_common), (arm_path, stock_arm)):
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            relocation_checks.setdefault(path, {})['market_stock_editorial'] = {
                'release_config': market_stock_editorial,
                'release_config_sha256': sha256(Path(market_stock_editorial).read_bytes()),
                'proof': stock_report}
        changed_records.setdefault(common_path, []).extend(stock_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend([
            'COMMON_MARKET_STOCK_COMPLETE_SELECTION_MAP', 'SCOPED_MARKET_RUNTIME_BALANCED_WRAP'])

    market_contract_editorial = profile_config.get('market_contract_editorial')
    if market_contract_editorial:
        from dk4tool.patch.market_contract_editorial import apply_release as apply_market_contract

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        contract_common, contract_arm, contract_report = apply_market_contract(
            candidate.read_file(common_path), candidate.read_file(arm_path), market_contract_editorial)
        for path, data in ((common_path, contract_common), (arm_path, contract_arm)):
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            relocation_checks.setdefault(path, {})['market_contract_editorial'] = {
                'release_config': market_contract_editorial,
                'release_config_sha256': sha256(Path(market_contract_editorial).read_bytes()),
                'proof': contract_report}
        changed_records.setdefault(common_path, []).extend(contract_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend([
            'COMMON_MARKET_ADVICE_CONTRACT_SELECTION_MAP', 'EXACT761_BALANCED_WRAP',
            'FULL_GOVERNOR_OFFICE_PROVIDER_AND_EXACT_OTHER_LABELS'])

    shipyard_editorial = profile_config.get('shipyard_editorial')
    if shipyard_editorial:
        from dk4tool.patch.shipyard_editorial_release import apply_release as apply_shipyard

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        yard_common, yard_arm, yard_report = apply_shipyard(
            candidate.read_file(common_path), candidate.read_file(arm_path), shipyard_editorial)
        for path, data in ((common_path, yard_common), (arm_path, yard_arm)):
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            relocation_checks.setdefault(path, {})['shipyard_editorial'] = {
                'release_config': shipyard_editorial,
                'release_config_sha256': sha256(Path(shipyard_editorial).read_bytes()),
                'proof': yard_report}
        changed_records.setdefault(common_path, []).extend(yard_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend([
            'COMMON_SHIPYARD_COMPLETE_SELECTION_MAP', 'SCOPED_TYPED_GOLD_AND_DAYS',
            'SCOPED_LITERAL_SHIP_NAMES_AND_BALANCED_WRAP_IN_OWNED_CONST_SLOTS'])

    port_services_editorial = profile_config.get('port_services_editorial')
    if port_services_editorial:
        from dk4tool.patch.port_services_editorial import apply_release as apply_port_services

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        service_common, service_arm, service_report = apply_port_services(
            candidate.read_file(common_path), candidate.read_file(arm_path), port_services_editorial)
        for path, data in ((common_path, service_common), (arm_path, service_arm)):
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            relocation_checks.setdefault(path, {})['port_services_editorial'] = {
                'release_config': port_services_editorial,
                'release_config_sha256': sha256(Path(port_services_editorial).read_bytes()),
                'proof': service_report}
        changed_records.setdefault(common_path, []).extend(service_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend([
            'COMMON_PORT_SERVICE_COMPLETE_SELECTION_MAP', 'EXACT808_1245_1246_LITERAL_BALANCING'])

    tavern_editorial = profile_config.get('tavern_conversations_editorial')
    if tavern_editorial:
        from dk4tool.patch.tavern_conversations_editorial import apply_release as apply_tavern_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        tavern_common, tavern_arm, tavern_report = apply_tavern_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), tavern_editorial)
        for path, data in ((common_path, tavern_common), (arm_path, tavern_arm)):
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            relocation_checks.setdefault(path, {})['tavern_conversations_editorial'] = {
                'release_config': tavern_editorial,
                'release_config_sha256': sha256(Path(tavern_editorial).read_bytes()),
                'proof': tavern_report}
        changed_records.setdefault(common_path, []).extend(tavern_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend([
            'COMMON_TAVERN_COMPLETE_SELECTION_MAP', 'PRIVATE_ENGLISH_DIRECTION_AND_PROFESSION_PROVIDERS',
            'SCOPED_LITERAL_GIFT_NAMES_AND_TYPED_COORDINATE_PAIRS'])

    tavern_continuation = profile_config.get('tavern_continuation_editorial')
    if tavern_continuation:
        from dk4tool.patch.tavern_continuation_editorial import apply_release as apply_tavern_continuation

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        new_common, new_arm, new_report = apply_tavern_continuation(
            candidate.read_file(common_path), candidate.read_file(arm_path), tavern_continuation)
        for path, data in ((common_path, new_common), (arm_path, new_arm)):
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            relocation_checks.setdefault(path, {})['tavern_continuation_editorial'] = {
                'release_config': tavern_continuation,
                'release_config_sha256': sha256(Path(tavern_continuation).read_bytes()),
                'proof': new_report}
        changed_records.setdefault(common_path, []).extend(new_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend([
            'COMMON_TAVERN_CONTINUATION_COMPLETE_SELECTION_MAP', 'PRIVATE_FULL_REGION_PHRASES',
            'SCOPED_TAVERN_COST_AND_ROUND_CALLERS', 'PLAYER_VOCATIVE_TARGET_ORDER_878'])

    recruitment = profile_config.get('recruitment_editorial')
    if recruitment:
        from dk4tool.patch.recruitment_editorial import apply_release as apply_recruitment

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        new_common, new_arm, new_report = apply_recruitment(
            candidate.read_file(common_path), candidate.read_file(arm_path), recruitment)
        for path, data in ((common_path, new_common), (arm_path, new_arm)):
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            relocation_checks.setdefault(path, {})['recruitment_editorial'] = {
                'release_config': recruitment,
                'release_config_sha256': sha256(Path(recruitment).read_bytes()),
                'proof': new_report}
        changed_records.setdefault(common_path, []).extend(new_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend([
            'COMMON_RECRUITMENT_COMPLETE_SELECTION_MAP', 'PRIVATE_TYPED_CONDITION_PHRASES',
            'EXACT_ROLE_TABLE_AND_ID_DISPATCH', 'SEVEN_CALLER_QUANTITY_HELPER'])

    schemes = profile_config.get('tavern_schemes_editorial')
    if schemes:
        from dk4tool.patch.tavern_schemes_editorial import apply_release as apply_schemes

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        new_common, new_arm, new_report = apply_schemes(
            candidate.read_file(common_path), candidate.read_file(arm_path), schemes)
        for path, data in ((common_path, new_common), (arm_path, new_arm)):
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            relocation_checks.setdefault(path, {})['tavern_schemes_editorial'] = {
                'release_config': schemes,
                'release_config_sha256': sha256(Path(schemes).read_bytes()),
                'proof': new_report}
        changed_records.setdefault(common_path, []).extend(new_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend([
            'COMMON_SCHEMES_COMPLETE_SELECTION_MAP', 'EXACT_SCHEME_TABLE_DISPATCH',
            'EXISTING_PRIVATE_ROUTING_BANKS_NO_GROWTH'])

    followup = profile_config.get('scheme_followup_editorial')
    if followup:
        from dk4tool.patch.scheme_followup_editorial import apply_release as apply_followup

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        new_common, new_arm, new_report = apply_followup(
            candidate.read_file(common_path), candidate.read_file(arm_path), followup)
        for path, data in ((common_path, new_common), (arm_path, new_arm)):
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            relocation_checks.setdefault(path, {})['scheme_followup_editorial'] = {
                'release_config': followup,
                'release_config_sha256': sha256(Path(followup).read_bytes()),
                'proof': new_report}
        changed_records.setdefault(common_path, []).extend(new_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend([
            'COMMON_FOLLOWUP_COMPLETE_SELECTION_MAP', 'EXACT_FOLLOWUP_TABLE_AND_972_DISPATCH',
            'EXISTING_PRIVATE_CONTRACT_TABLE_NO_GROWTH'])

    barmaid = profile_config.get('barmaid_editorial')
    if barmaid:
        from dk4tool.patch.barmaid_editorial import apply_release as apply_barmaid

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        new_common, new_arm, new_report = apply_barmaid(
            candidate.read_file(common_path), candidate.read_file(arm_path), barmaid)
        for path, data in ((common_path, new_common), (arm_path, new_arm)):
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            relocation_checks.setdefault(path, {})['barmaid_editorial'] = {
                'release_config': barmaid,
                'release_config_sha256': sha256(Path(barmaid).read_bytes()),
                'proof': new_report}
        changed_records.setdefault(common_path, []).extend(new_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend([
            'COMMON_BARMAID_COMPLETE_SELECTION_MAP', 'EXACT_DIRECT_BARMAID_ID_DISPATCH',
            'EXISTING_PRIVATE_CONTRACT_TABLE_NO_GROWTH'])

    shared_dialogue = profile_config.get('shared_dialogue_editorial')
    if shared_dialogue:
        from dk4tool.patch.shared_dialogue_editorial import apply_release as apply_shared_dialogue

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        new_common, new_arm, new_report = apply_shared_dialogue(
            candidate.read_file(common_path), candidate.read_file(arm_path), shared_dialogue)
        for path, data in ((common_path, new_common), (arm_path, new_arm)):
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            relocation_checks.setdefault(path, {})['shared_dialogue_editorial'] = {
                'release_config': shared_dialogue,
                'release_config_sha256': sha256(Path(shared_dialogue).read_bytes()),
                'proof': new_report}
        changed_records.setdefault(common_path, []).extend(new_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend([
            'COMMON_SHARED_COMPLETE_SELECTION_MAP', 'EXACT_SHARED_ROLE_VOICE_AND_COORDINATE_DISPATCH',
            'EXISTING_PRIVATE_TABLE_AND_GATE_NO_GROWTH'])

    item_diplomacy = profile_config.get('item_diplomacy_editorial')
    if item_diplomacy:
        from dk4tool.patch.item_diplomacy_editorial import apply_release as apply_item_diplomacy

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        new_common, new_arm, new_report = apply_item_diplomacy(
            candidate.read_file(common_path), candidate.read_file(arm_path), item_diplomacy)
        for path, data in ((common_path, new_common), (arm_path, new_arm)):
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            relocation_checks.setdefault(path, {})['item_diplomacy_editorial'] = {
                'release_config': item_diplomacy,
                'release_config_sha256': sha256(Path(item_diplomacy).read_bytes()),
                'proof': new_report}
        changed_records.setdefault(common_path, []).extend(new_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend([
            'COMMON_ITEM_DIPLOMACY_COMPLETE_SELECTION_MAP', 'SCOPED_ITEM_DIPLOMACY_DISPATCH',
            'SIX_COMPLETE_NOMINAL_DOCUMENT_NAMES', 'SHARED_SCHEME_NAME_WIDTH_24_CELLS_NO_GROWTH'])

    arrival_notices = profile_config.get('arrival_notices_editorial')
    if arrival_notices:
        from dk4tool.patch.arrival_notices_editorial import apply_release as apply_arrival_notices

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        new_common, new_arm, new_report = apply_arrival_notices(
            candidate.read_file(common_path), candidate.read_file(arm_path), arrival_notices)
        for path, data in ((common_path, new_common), (arm_path, new_arm)):
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            relocation_checks.setdefault(path, {})['arrival_notices_editorial'] = {
                'release_config': arrival_notices,
                'release_config_sha256': sha256(Path(arrival_notices).read_bytes()),
                'proof': new_report}
        changed_records.setdefault(common_path, []).extend(new_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend([
            'COMMON_ARRIVAL_COMPLETE_SELECTION_MAP', 'THREE_SOURCE_BOUND_MODAL_NOTICES',
            'EXISTING_128_BYTE_MODAL_WRAPPER_NO_GROWTH'])

    palace_editorial = profile_config.get('palace_editorial')
    if palace_editorial:
        from dk4tool.patch.palace_editorial import apply_release as apply_palace_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        new_common, new_arm, new_report = apply_palace_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), palace_editorial)
        for path, data in ((common_path, new_common), (arm_path, new_arm)):
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            relocation_checks.setdefault(path, {})['palace_editorial'] = {
                'release_config': palace_editorial,
                'release_config_sha256': sha256(Path(palace_editorial).read_bytes()),
                'proof': new_report}
        changed_records.setdefault(common_path, []).extend(new_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend([
            'COMMON_PALACE_COMPLETE_SELECTION_MAP', 'EXACT_PARENT_PALACE_PARAGRAPHS',
            'EXISTING_168_BYTE_PRIVATE_DATA_REPACK_NO_GROWTH'])

    palace_label_contract = {'applicable': False}
    palace_labels = profile_config.get('palace_label_boundaries')
    if palace_labels:
        from dk4tool.patch.palace_label_boundaries import apply_release as apply_palace_labels, verify_final as verify_palace_labels

        arm_path = '/__arm9__.bin'
        new_arm, new_report = apply_palace_labels(candidate.read_file(arm_path), palace_labels)
        candidate.replace_file(arm_path, new_arm)
        grouped.setdefault(arm_path, [])
        relocation_checks.setdefault(arm_path, {})['palace_label_boundaries'] = {
            'release_config': palace_labels,
            'release_config_sha256': sha256(Path(palace_labels).read_bytes()),
            'proof': new_report}
        changed_records.setdefault(arm_path, []).extend(new_report['changed_records'])
        palace_label_contract = {'applicable': True, **verify_palace_labels(new_arm)}

    inn_editorial = profile_config.get('inn_editorial')
    if inn_editorial:
        from dk4tool.patch.inn_editorial import apply_release as apply_inn_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        new_common, new_arm, new_report = apply_inn_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), inn_editorial)
        for path, data in ((common_path, new_common), (arm_path, new_arm)):
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            relocation_checks.setdefault(path, {})['inn_editorial'] = {
                'release_config': inn_editorial,
                'release_config_sha256': sha256(Path(inn_editorial).read_bytes()),
                'proof': new_report}
        changed_records.setdefault(common_path, []).extend(new_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend([
            'COMMON_INN_COMPLETE_SELECTION_MAP', 'EXACT_PARENT_INN_PARAGRAPHS',
            'COMPLETE_RELATIVE_MONTH_PHRASES_IN_SOURCE_OWNED_STRINGS',
            'EXISTING_168_BYTE_PRIVATE_DATA_REPACK_NO_GROWTH'])
        if palace_labels:
            palace_label_contract = {'applicable': True, **verify_palace_labels(new_arm)}

    ceremony_editorial = profile_config.get('ceremony_editorial')
    if ceremony_editorial:
        from dk4tool.patch.ceremony_editorial import apply_release as apply_ceremony_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        new_common, new_arm, new_report = apply_ceremony_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), ceremony_editorial)
        for path, data in ((common_path, new_common), (arm_path, new_arm)):
            candidate.replace_file(path, data)
            grouped.setdefault(path, [])
            relocation_checks.setdefault(path, {})['ceremony_editorial'] = {
                'release_config': ceremony_editorial,
                'release_config_sha256': sha256(Path(ceremony_editorial).read_bytes()),
                'proof': new_report}
        changed_records.setdefault(common_path, []).extend(new_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend([
            'COMMON_CEREMONY_COMPLETE_SELECTION_MAP', 'EXACT_PARENT_CEREMONY_PARAGRAPHS',
            'SIX_SOURCE_BOUND_CEREMONY_MODAL_NOTICES',
            'EXISTING_384_BYTE_RUNTIME_BANK_REPACK_NO_GROWTH'])
        if palace_labels:
            palace_label_contract = {'applicable': True, **verify_palace_labels(new_arm)}

    levelup_stat_format = profile_config.get('levelup_stat_format')
    if levelup_stat_format:
        from dk4tool.patch.levelup_stat_format import apply_release as apply_levelup_stat_format
        arm_path, common_path = '/__arm9__.bin', '/COMMON/MESFILE.DK4'
        new_arm, new_report = apply_levelup_stat_format(
            candidate.read_file(common_path), candidate.read_file(arm_path), levelup_stat_format)
        candidate.replace_file(arm_path, new_arm)
        grouped.setdefault(arm_path, [])
        relocation_checks.setdefault(arm_path, {})['levelup_stat_format'] = {
            'release_config': levelup_stat_format,
            'release_config_sha256': sha256(Path(levelup_stat_format).read_bytes()),
            'proof': new_report}
        changed_records.setdefault(arm_path, []).extend([
            'SOURCE_OWNED_LEVELUP_HEADER_INSTRUCTION_SET_REPACK',
            'SCOPED_COMPOUND_STAT_LINE_GUARDS_AND_NATIVE_PAGINATION'])

    late_story_editorial = profile_config.get('late_story_editorial_release')
    if late_story_editorial:
        from dk4tool.patch.late_story_editorial import apply_release as apply_late_story_editorial

        late_config = json.loads(Path(late_story_editorial).read_text(encoding='utf-8'))
        for spec in late_config['batches']:
            late_path = Path(spec['path'])
            if late_path in release_batches:
                raise ValueError('Late story batch must not run before frozen historical stages')
            late_header = load_batch_header(late_path)
            validate_playable_dialogue_header(late_path, late_header)
            validate_natural_dialogue_qa(late_path, late_header, baseline.read_file(late_header['file_path']))
        late_report = apply_late_story_editorial(candidate, baseline, late_story_editorial)
        for row in late_report['changed_records']:
            file_path = row['file_path']
            grouped.setdefault(file_path, [])
            changed_records.setdefault(file_path, []).append(row['id'])
            relocation_checks.setdefault(file_path, {})['late_story_editorial'] = {
                'release_config': late_story_editorial,
                'release_config_sha256': sha256(Path(late_story_editorial).read_bytes()),
                'proof': late_report}
        release_batches.extend(Path(p) for p in late_report['batches'])

    refit_help_editorial = profile_config.get('refit_help_editorial')
    if refit_help_editorial:
        from dk4tool.patch.refit_help_editorial import apply_release as apply_refit_help_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, refit_report = apply_refit_help_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), refit_help_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['refit_help_editorial'] = {
                'release_config': refit_help_editorial,
                'release_config_sha256': sha256(Path(refit_help_editorial).read_bytes()),
                'proof': refit_report}
        changed_records.setdefault(common_path, []).extend(refit_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('REFIT_EDITORIAL_COMPLETE_NATIVE_SELECTION_METADATA')

    refit_dialogue_editorial = profile_config.get('refit_dialogue_editorial')
    if refit_dialogue_editorial:
        from dk4tool.patch.refit_dialogue_editorial import apply_release as apply_refit_dialogue_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, refit_dialogue_report = apply_refit_dialogue_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), refit_dialogue_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['refit_dialogue_editorial'] = {
                'release_config': refit_dialogue_editorial,
                'release_config_sha256': sha256(Path(refit_dialogue_editorial).read_bytes()),
                'proof': refit_dialogue_report}
        changed_records.setdefault(common_path, []).extend(refit_dialogue_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('REFIT_DIALOGUE_EXACT_SCOPES_DURATION_UNIT_AND_NATIVE_SELECTION_METADATA')

    personal_chatter_editorial = profile_config.get('personal_chatter_editorial')
    if personal_chatter_editorial:
        from dk4tool.patch.personal_chatter_editorial import apply_release as apply_personal_chatter_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, personal_chatter_report = apply_personal_chatter_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), personal_chatter_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['personal_chatter_editorial'] = {
                'release_config': personal_chatter_editorial,
                'release_config_sha256': sha256(Path(personal_chatter_editorial).read_bytes()),
                'proof': personal_chatter_report}
        changed_records.setdefault(common_path, []).extend(personal_chatter_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('DECK_PERSONAL_COMMENT_NATIVE_METADATA_AND_VISIBLE_CROP')

    work_comments_editorial = profile_config.get('work_comments_editorial')
    if work_comments_editorial:
        from dk4tool.patch.work_comments_editorial import apply_release as apply_work_comments_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, work_comments_report = apply_work_comments_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), work_comments_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['work_comments_editorial'] = {
                'release_config': work_comments_editorial,
                'release_config_sha256': sha256(Path(work_comments_editorial).read_bytes()),
                'proof': work_comments_report}
        changed_records.setdefault(common_path, []).extend(work_comments_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('WORK_COMMENTS_NATIVE_SELECTION_METADATA')

    cooking_comments_editorial = profile_config.get('cooking_comments_editorial')
    if cooking_comments_editorial:
        from dk4tool.patch.cooking_comments_editorial import apply_release as apply_cooking_comments_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, cooking_comments_report = apply_cooking_comments_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), cooking_comments_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['cooking_comments_editorial'] = {
                'release_config': cooking_comments_editorial,
                'release_config_sha256': sha256(Path(cooking_comments_editorial).read_bytes()),
                'proof': cooking_comments_report}
        changed_records.setdefault(common_path, []).extend(cooking_comments_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('COOKING_COMMENTS_NATIVE_SELECTION_METADATA')

    livestock_prayer_editorial = profile_config.get('livestock_prayer_editorial')
    if livestock_prayer_editorial:
        from dk4tool.patch.livestock_prayer_editorial import apply_release as apply_livestock_prayer_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, livestock_prayer_report = apply_livestock_prayer_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), livestock_prayer_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['livestock_prayer_editorial'] = {
                'release_config': livestock_prayer_editorial,
                'release_config_sha256': sha256(Path(livestock_prayer_editorial).read_bytes()),
                'proof': livestock_prayer_report}
        changed_records.setdefault(common_path, []).extend(livestock_prayer_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('LIVESTOCK_PRAYER_NATIVE_SELECTION_METADATA')

    planning_finance_editorial = profile_config.get('planning_finance_editorial')
    if planning_finance_editorial:
        from dk4tool.patch.planning_finance_editorial_v2 import apply_release as apply_planning_finance_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, planning_finance_report = apply_planning_finance_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), planning_finance_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['planning_finance_editorial'] = {
                'release_config': planning_finance_editorial,
                'release_config_sha256': sha256(Path(planning_finance_editorial).read_bytes()),
                'proof': planning_finance_report}
        changed_records.setdefault(common_path, []).extend(planning_finance_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend([
            'PLANNING_FINANCE_NATIVE_SELECTION_METADATA', 'COMMON_SINGLE8192_CACHE_IN_ORIGINAL_ALLOCATION'])

    bridge_duties_editorial = profile_config.get('bridge_duties_editorial')
    if bridge_duties_editorial:
        from dk4tool.patch.bridge_duties_editorial import apply_release as apply_bridge_duties_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, bridge_duties_report = apply_bridge_duties_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), bridge_duties_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['bridge_duties_editorial'] = {
                'release_config': bridge_duties_editorial,
                'release_config_sha256': sha256(Path(bridge_duties_editorial).read_bytes()),
                'proof': bridge_duties_report}
        changed_records.setdefault(common_path, []).extend(bridge_duties_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('BRIDGE_DUTIES_NATIVE_SELECTION_METADATA')

    survey_lookout_editorial = profile_config.get('survey_lookout_editorial')
    if survey_lookout_editorial:
        from dk4tool.patch.survey_lookout_editorial import apply_release as apply_survey_lookout_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, survey_lookout_report = apply_survey_lookout_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), survey_lookout_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['survey_lookout_editorial'] = {
                'release_config': survey_lookout_editorial,
                'release_config_sha256': sha256(Path(survey_lookout_editorial).read_bytes()),
                'proof': survey_lookout_report}
        changed_records.setdefault(common_path, []).extend(survey_lookout_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('SURVEY_LOOKOUT_NATIVE_SELECTION_METADATA')

    sails_boarding_editorial = profile_config.get('sails_boarding_editorial')
    if sails_boarding_editorial:
        from dk4tool.patch.sails_boarding_editorial import apply_release as apply_sails_boarding_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, sails_boarding_report = apply_sails_boarding_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), sails_boarding_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['sails_boarding_editorial'] = {
                'release_config': sails_boarding_editorial,
                'release_config_sha256': sha256(Path(sails_boarding_editorial).read_bytes()),
                'proof': sails_boarding_report}
        changed_records.setdefault(common_path, []).extend(sails_boarding_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('SAILS_BOARDING_NATIVE_SELECTION_METADATA')

    gunnery_deck_editorial = profile_config.get('gunnery_deck_editorial')
    if gunnery_deck_editorial:
        from dk4tool.patch.gunnery_deck_editorial import apply_release as apply_gunnery_deck_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, gunnery_deck_report = apply_gunnery_deck_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), gunnery_deck_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['gunnery_deck_editorial'] = {
                'release_config': gunnery_deck_editorial,
                'release_config_sha256': sha256(Path(gunnery_deck_editorial).read_bytes()),
                'proof': gunnery_deck_report}
        changed_records.setdefault(common_path, []).extend(gunnery_deck_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('GUNNERY_DECK_NATIVE_SELECTION_METADATA')

    battle_personal_editorial = profile_config.get('battle_personal_editorial')
    if battle_personal_editorial:
        from dk4tool.patch.battle_personal_editorial import apply_release as apply_battle_personal_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, battle_personal_report = apply_battle_personal_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), battle_personal_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['battle_personal_editorial'] = {
                'release_config': battle_personal_editorial,
                'release_config_sha256': sha256(Path(battle_personal_editorial).read_bytes()),
                'proof': battle_personal_report}
        changed_records.setdefault(common_path, []).extend(battle_personal_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('BATTLE_PERSONAL_NATIVE_SELECTION_METADATA')

    battle_repair_medical_editorial = profile_config.get('battle_repair_medical_editorial')
    if battle_repair_medical_editorial:
        from dk4tool.patch.battle_repair_medical_editorial import apply_release as apply_battle_repair_medical_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, battle_repair_medical_report = apply_battle_repair_medical_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), battle_repair_medical_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['battle_repair_medical_editorial'] = {
                'release_config': battle_repair_medical_editorial,
                'release_config_sha256': sha256(Path(battle_repair_medical_editorial).read_bytes()),
                'proof': battle_repair_medical_report}
        changed_records.setdefault(common_path, []).extend(battle_repair_medical_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('BATTLE_REPAIR_MEDICAL_NATIVE_SELECTION_METADATA')

    battle_cooking_livestock_editorial = profile_config.get('battle_cooking_livestock_editorial')
    if battle_cooking_livestock_editorial:
        from dk4tool.patch.battle_cooking_livestock_editorial import apply_release as apply_battle_cooking_livestock_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, battle_cooking_livestock_report = apply_battle_cooking_livestock_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), battle_cooking_livestock_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['battle_cooking_livestock_editorial'] = {
                'release_config': battle_cooking_livestock_editorial,
                'release_config_sha256': sha256(Path(battle_cooking_livestock_editorial).read_bytes()),
                'proof': battle_cooking_livestock_report}
        changed_records.setdefault(common_path, []).extend(battle_cooking_livestock_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('BATTLE_COOKING_LIVESTOCK_NATIVE_SELECTION_METADATA')

    battle_chapel_planning_editorial = profile_config.get('battle_chapel_planning_editorial')
    if battle_chapel_planning_editorial:
        from dk4tool.patch.battle_chapel_planning_editorial import apply_release as apply_battle_chapel_planning_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, battle_chapel_planning_report = apply_battle_chapel_planning_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), battle_chapel_planning_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['battle_chapel_planning_editorial'] = {
                'release_config': battle_chapel_planning_editorial,
                'release_config_sha256': sha256(Path(battle_chapel_planning_editorial).read_bytes()),
                'proof': battle_chapel_planning_report}
        changed_records.setdefault(common_path, []).extend(battle_chapel_planning_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('BATTLE_CHAPEL_PLANNING_NATIVE_SELECTION_METADATA')

    battle_finance_editorial = profile_config.get('battle_finance_editorial')
    if battle_finance_editorial:
        from dk4tool.patch.battle_finance_editorial import apply_release as apply_battle_finance_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, battle_finance_report = apply_battle_finance_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), battle_finance_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['battle_finance_editorial'] = {
                'release_config': battle_finance_editorial,
                'release_config_sha256': sha256(Path(battle_finance_editorial).read_bytes()),
                'proof': battle_finance_report}
        changed_records.setdefault(common_path, []).extend(battle_finance_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('BATTLE_FINANCE_NATIVE_SELECTION_METADATA')

    battle_bridge_editorial = profile_config.get('battle_bridge_editorial')
    if battle_bridge_editorial:
        from dk4tool.patch.battle_bridge_editorial import apply_release as apply_battle_bridge_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, battle_bridge_report = apply_battle_bridge_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), battle_bridge_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['battle_bridge_editorial'] = {
                'release_config': battle_bridge_editorial,
                'release_config_sha256': sha256(Path(battle_bridge_editorial).read_bytes()),
                'proof': battle_bridge_report}
        changed_records.setdefault(common_path, []).extend(battle_bridge_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('BATTLE_BRIDGE_NATIVE_SELECTION_METADATA')

    battle_survey_lookout_editorial = profile_config.get('battle_survey_lookout_editorial')
    if battle_survey_lookout_editorial:
        from dk4tool.patch.battle_survey_lookout_editorial import apply_release as apply_battle_survey_lookout_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, battle_survey_lookout_report = apply_battle_survey_lookout_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), battle_survey_lookout_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['battle_survey_lookout_editorial'] = {
                'release_config': battle_survey_lookout_editorial,
                'release_config_sha256': sha256(Path(battle_survey_lookout_editorial).read_bytes()),
                'proof': battle_survey_lookout_report}
        changed_records.setdefault(common_path, []).extend(battle_survey_lookout_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('BATTLE_SURVEY_LOOKOUT_NATIVE_SELECTION_METADATA')

    battle_sails_boarding_editorial = profile_config.get('battle_sails_boarding_editorial')
    if battle_sails_boarding_editorial:
        from dk4tool.patch.battle_sails_boarding_editorial import apply_release as apply_battle_sails_boarding_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, battle_sails_boarding_report = apply_battle_sails_boarding_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), battle_sails_boarding_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['battle_sails_boarding_editorial'] = {
                'release_config': battle_sails_boarding_editorial,
                'release_config_sha256': sha256(Path(battle_sails_boarding_editorial).read_bytes()),
                'proof': battle_sails_boarding_report}
        changed_records.setdefault(common_path, []).extend(battle_sails_boarding_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('BATTLE_SAILS_BOARDING_NATIVE_SELECTION_METADATA')

    battle_gunnery_deck_editorial = profile_config.get('battle_gunnery_deck_editorial')
    if battle_gunnery_deck_editorial:
        from dk4tool.patch.battle_gunnery_deck_editorial import apply_release as apply_battle_gunnery_deck_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, battle_gunnery_deck_report = apply_battle_gunnery_deck_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), battle_gunnery_deck_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['battle_gunnery_deck_editorial'] = {
                'release_config': battle_gunnery_deck_editorial,
                'release_config_sha256': sha256(Path(battle_gunnery_deck_editorial).read_bytes()),
                'proof': battle_gunnery_deck_report}
        changed_records.setdefault(common_path, []).extend(battle_gunnery_deck_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('BATTLE_GUNNERY_DECK_NATIVE_SELECTION_METADATA')

    physical_fatigue_editorial = profile_config.get('physical_fatigue_editorial')
    if physical_fatigue_editorial:
        from dk4tool.patch.physical_fatigue_editorial import apply_release as apply_physical_fatigue_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, physical_fatigue_report = apply_physical_fatigue_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), physical_fatigue_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['physical_fatigue_editorial'] = {
                'release_config': physical_fatigue_editorial,
                'release_config_sha256': sha256(Path(physical_fatigue_editorial).read_bytes()),
                'proof': physical_fatigue_report}
        changed_records.setdefault(common_path, []).extend(physical_fatigue_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('PHYSICAL_FATIGUE_NATIVE_SELECTION_METADATA')

    physical_wounds_editorial = profile_config.get('physical_wounds_editorial')
    if physical_wounds_editorial:
        from dk4tool.patch.physical_wounds_editorial import apply_release as apply_physical_wounds_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, physical_wounds_report = apply_physical_wounds_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), physical_wounds_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['physical_wounds_editorial'] = {
                'release_config': physical_wounds_editorial,
                'release_config_sha256': sha256(Path(physical_wounds_editorial).read_bytes()),
                'proof': physical_wounds_report}
        changed_records.setdefault(common_path, []).extend(physical_wounds_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('PHYSICAL_WOUNDS_NATIVE_SELECTION_METADATA')

    illness_critical_editorial = profile_config.get('illness_critical_editorial')
    if illness_critical_editorial:
        from dk4tool.patch.illness_critical_editorial import apply_release as apply_illness_critical_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, illness_critical_report = apply_illness_critical_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), illness_critical_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['illness_critical_editorial'] = {
                'release_config': illness_critical_editorial,
                'release_config_sha256': sha256(Path(illness_critical_editorial).read_bytes()),
                'proof': illness_critical_report}
        changed_records.setdefault(common_path, []).extend(illness_critical_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('ILLNESS_CRITICAL_NATIVE_SELECTION_METADATA')

    mood_comments_editorial = profile_config.get('mood_comments_editorial')
    if mood_comments_editorial:
        from dk4tool.patch.mood_comments_editorial_v981b import apply_release as apply_mood_comments_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, mood_comments_report = apply_mood_comments_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), mood_comments_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['mood_comments_editorial'] = {
                'release_config': mood_comments_editorial,
                'release_config_sha256': sha256(Path(mood_comments_editorial).read_bytes()),
                'proof': mood_comments_report}
        changed_records.setdefault(common_path, []).extend(mood_comments_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('MOOD_COMMENTS_NATIVE_SELECTION_METADATA')

    activity_special_editorial = profile_config.get('activity_special_editorial')
    if activity_special_editorial:
        from dk4tool.patch.activity_special_editorial_v987b import apply_release as apply_activity_special_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, activity_special_report = apply_activity_special_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), activity_special_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['activity_special_editorial'] = {
                'release_config': activity_special_editorial,
                'release_config_sha256': sha256(Path(activity_special_editorial).read_bytes()),
                'proof': activity_special_report}
        changed_records.setdefault(common_path, []).extend(activity_special_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('ACTIVITY_SPECIAL_NATIVE_SELECTION_METADATA')

    battle_declaration_editorial = profile_config.get('battle_declaration_editorial')
    if battle_declaration_editorial:
        from dk4tool.patch.battle_declaration_editorial import apply_release as apply_battle_declaration_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, battle_declaration_report = apply_battle_declaration_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), battle_declaration_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['battle_declaration_editorial'] = {
                'release_config': battle_declaration_editorial,
                'release_config_sha256': sha256(Path(battle_declaration_editorial).read_bytes()),
                'proof': battle_declaration_report}
        changed_records.setdefault(common_path, []).extend(battle_declaration_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('BATTLE_DECLARATION_NATIVE_SELECTION_METADATA')

    reinforcement_sniping_editorial = profile_config.get('reinforcement_sniping_editorial')
    if reinforcement_sniping_editorial:
        from dk4tool.patch.reinforcement_sniping_editorial import apply_release as apply_reinforcement_sniping_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, reinforcement_sniping_report = apply_reinforcement_sniping_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), reinforcement_sniping_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['reinforcement_sniping_editorial'] = {
                'release_config': reinforcement_sniping_editorial,
                'release_config_sha256': sha256(Path(reinforcement_sniping_editorial).read_bytes()),
                'proof': reinforcement_sniping_report}
        changed_records.setdefault(common_path, []).extend(reinforcement_sniping_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('REINFORCEMENT_SNIPING_NATIVE_SELECTION_METADATA')

    sighting_editorial = profile_config.get('sighting_editorial')
    if sighting_editorial:
        from dk4tool.patch.sighting_editorial import apply_release as apply_sighting_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, sighting_report = apply_sighting_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), sighting_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['sighting_editorial'] = {
                'release_config': sighting_editorial,
                'release_config_sha256': sha256(Path(sighting_editorial).read_bytes()),
                'proof': sighting_report}
        changed_records.setdefault(common_path, []).extend(sighting_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend(['SIGHTING_NATIVE_SELECTION_METADATA', 'CLOSE_RANGE_BEARING_LABEL', 'ARMED_LATINA_DEFAULT_SHIP_LABEL'])

    sighting_grammar_editorial = profile_config.get('sighting_grammar_editorial')
    if sighting_grammar_editorial:
        from dk4tool.patch.sighting_grammar_editorial import apply_release as apply_sighting_grammar_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, sighting_grammar_report = apply_sighting_grammar_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), sighting_grammar_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['sighting_grammar_editorial'] = {
                'release_config': sighting_grammar_editorial,
                'release_config_sha256': sha256(Path(sighting_grammar_editorial).read_bytes()),
                'proof': sighting_grammar_report}
        changed_records.setdefault(common_path, []).extend(sighting_grammar_report['changed_records'])
        changed_records.setdefault(arm_path, []).append('SIGHTING_GRAMMAR_NATIVE_SELECTION_METADATA')

    duel_editorial = profile_config.get('duel_editorial')
    if duel_editorial:
        from dk4tool.patch.duel_editorial import apply_release as apply_duel_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, duel_report = apply_duel_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), duel_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['duel_editorial'] = {
                'release_config': duel_editorial,
                'release_config_sha256': sha256(Path(duel_editorial).read_bytes()),
                'proof': duel_report}
        changed_records.setdefault(common_path, []).extend(duel_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend(['DUEL_NATIVE_SELECTION_METADATA', 'DUEL_OWNED_RENDERER_AND_ESCAPE_SCOPE'])

    escape_direct_formatting = profile_config.get('escape_direct_formatting')
    if escape_direct_formatting:
        from dk4tool.patch.escape_direct_formatting import apply_release as apply_escape_direct_formatting

        arm_path = '/__arm9__.bin'
        final_arm, escape_direct_report = apply_escape_direct_formatting(
            candidate.read_file(arm_path), escape_direct_formatting)
        candidate.replace_file(arm_path, final_arm)
        grouped.setdefault(arm_path, [])
        relocation_checks.setdefault(arm_path, {})['escape_direct_formatting'] = {
            'release_config': escape_direct_formatting,
            'release_config_sha256': sha256(Path(escape_direct_formatting).read_bytes()),
            'proof': escape_direct_report}
        changed_records.setdefault(arm_path, []).append('DIRECT_ESCAPE_PORTRAIT_SCOPE_AND_PRESERVED_STATUS_LITERAL')

    duel_bark_editorial = profile_config.get('duel_bark_editorial')
    if duel_bark_editorial:
        from dk4tool.patch.duel_bark_editorial import apply_release as apply_duel_bark_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, duel_report = apply_duel_bark_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), duel_bark_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['duel_bark_editorial'] = {
                'release_config': duel_bark_editorial,
                'release_config_sha256': sha256(Path(duel_bark_editorial).read_bytes()),
                'proof': duel_report}
        changed_records.setdefault(common_path, []).extend(duel_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend(['DUEL_BARK_NATIVE_SELECTION_METADATA', 'DUEL_BARK_FIVE_TABLE_FRONT_SAME_OWNED108'])

    duel_special_editorial = profile_config.get('duel_special_editorial')
    if duel_special_editorial:
        from dk4tool.patch.duel_special_editorial import apply_release as apply_duel_special_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, duel_report = apply_duel_special_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), duel_special_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['duel_special_editorial'] = {
                'release_config': duel_special_editorial,
                'release_config_sha256': sha256(Path(duel_special_editorial).read_bytes()),
                'proof': duel_report}
        changed_records.setdefault(common_path, []).extend(duel_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend(['DUEL_SPECIAL_NATIVE_SELECTION_METADATA', 'DUEL_SPECIAL_SOURCE_OWNED_HELPER64_AND_FRONT108'])

    battle_aftermath_editorial = profile_config.get('battle_aftermath_editorial')
    if battle_aftermath_editorial:
        from dk4tool.patch.battle_aftermath_editorial import apply_release as apply_battle_aftermath_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, duel_report = apply_battle_aftermath_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), battle_aftermath_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['battle_aftermath_editorial'] = {
                'release_config': battle_aftermath_editorial,
                'release_config_sha256': sha256(Path(battle_aftermath_editorial).read_bytes()),
                'proof': duel_report}
        changed_records.setdefault(common_path, []).extend(duel_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend(['BATTLE_AFTERMATH_NATIVE_SELECTION_METADATA', 'BATTLE_AFTERMATH_SELECTOR_SAME_OWNED188_AND172'])

    powder_fire_editorial = profile_config.get('powder_fire_editorial')
    if powder_fire_editorial:
        from dk4tool.patch.powder_fire_editorial import apply_release as apply_powder_fire_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, duel_report = apply_powder_fire_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), powder_fire_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['powder_fire_editorial'] = {
                'release_config': powder_fire_editorial,
                'release_config_sha256': sha256(Path(powder_fire_editorial).read_bytes()),
                'proof': duel_report}
        changed_records.setdefault(common_path, []).extend(duel_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend(['POWDER_FIRE_NATIVE_SELECTION_METADATA', 'POWDER_FIRE_TABLE_SAME_OWNED188_GATE_CODE_UNCHANGED'])

    ship_sinking_editorial = profile_config.get('ship_sinking_editorial')
    if ship_sinking_editorial:
        from dk4tool.patch.ship_sinking_editorial import apply_release as apply_ship_sinking_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, duel_report = apply_ship_sinking_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), ship_sinking_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['ship_sinking_editorial'] = {
                'release_config': ship_sinking_editorial,
                'release_config_sha256': sha256(Path(ship_sinking_editorial).read_bytes()),
                'proof': duel_report}
        changed_records.setdefault(common_path, []).extend(duel_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend(['SHIP_SINKING_NATIVE_SELECTION_METADATA', 'SHIP_SINKING_TABLE_SAME_OWNED188_GATE_CODE_UNCHANGED'])

    flagship_capture_precision = profile_config.get('flagship_capture_precision')
    if flagship_capture_precision:
        from dk4tool.patch.flagship_capture_precision import apply_release as apply_flagship_capture_precision

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, duel_report = apply_flagship_capture_precision(
            candidate.read_file(common_path), candidate.read_file(arm_path), flagship_capture_precision)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['flagship_capture_precision'] = {
                'release_config': flagship_capture_precision,
                'release_config_sha256': sha256(Path(flagship_capture_precision).read_bytes()),
                'proof': duel_report}
        changed_records.setdefault(common_path, []).extend(duel_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend(['FLAGSHIP_CAPTURE_PRECISION_NATIVE_SELECTION_METADATA', 'FLAGSHIP_CAPTURE_PRECISION_ENTIRE_RUNTIME_UNCHANGED'])

    battle_victory_editorial = profile_config.get('battle_victory_editorial')
    if battle_victory_editorial:
        from dk4tool.patch.battle_victory_editorial import apply_release as apply_battle_victory_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, duel_report = apply_battle_victory_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), battle_victory_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['battle_victory_editorial'] = {
                'release_config': battle_victory_editorial,
                'release_config_sha256': sha256(Path(battle_victory_editorial).read_bytes()),
                'proof': duel_report}
        changed_records.setdefault(common_path, []).extend(duel_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend(['BATTLE_VICTORY_NATIVE_SELECTION_METADATA', 'BATTLE_VICTORY_ENTIRE_RUNTIME_UNCHANGED'])

    enemy_capture_editorial = profile_config.get('enemy_capture_editorial')
    if enemy_capture_editorial:
        from dk4tool.patch.enemy_capture_editorial import apply_release as apply_enemy_capture_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, duel_report = apply_enemy_capture_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), enemy_capture_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['enemy_capture_editorial'] = {
                'release_config': enemy_capture_editorial,
                'release_config_sha256': sha256(Path(enemy_capture_editorial).read_bytes()),
                'proof': duel_report}
        changed_records.setdefault(common_path, []).extend(duel_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend(['ENEMY_CAPTURE_NATIVE_SELECTION_METADATA', 'ENEMY_CAPTURE_EXACT_DIRECT_CALLER_NAME_PROTECTION_AND_WRAP'])

    ship_loss_surrender_editorial = profile_config.get('ship_loss_surrender_editorial')
    if ship_loss_surrender_editorial:
        from dk4tool.patch.ship_loss_surrender_editorial import apply_release as apply_ship_loss_surrender_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, duel_report = apply_ship_loss_surrender_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), ship_loss_surrender_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['ship_loss_surrender_editorial'] = {
                'release_config': ship_loss_surrender_editorial,
                'release_config_sha256': sha256(Path(ship_loss_surrender_editorial).read_bytes()),
                'proof': duel_report}
        changed_records.setdefault(common_path, []).extend(duel_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend(['SHIP_LOSS_SURRENDER_NATIVE_SELECTION_METADATA', 'SHIP_LOSS_SURRENDER_THREE_EXACT_ROLE_CALLERS_NAME_PROTECTION_AND_WRAP'])

    battle_reaction_editorial = profile_config.get('battle_reaction_editorial')
    if battle_reaction_editorial:
        from dk4tool.patch.battle_reaction_editorial import apply_release as apply_battle_reaction_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, duel_report = apply_battle_reaction_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), battle_reaction_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['battle_reaction_editorial'] = {
                'release_config': battle_reaction_editorial,
                'release_config_sha256': sha256(Path(battle_reaction_editorial).read_bytes()),
                'proof': duel_report}
        changed_records.setdefault(common_path, []).extend(duel_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend(['BATTLE_REACTION_NATIVE_SELECTION_METADATA', 'BATTLE_REACTION_FOUR_EXACT_ACTOR_TABLES_AND_POSTMACRO_WRAP'])

    retreat_transfer_editorial = profile_config.get('retreat_transfer_editorial')
    if retreat_transfer_editorial:
        from dk4tool.patch.retreat_transfer_editorial import apply_release as apply_retreat_transfer_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, duel_report = apply_retreat_transfer_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), retreat_transfer_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['retreat_transfer_editorial'] = {
                'release_config': retreat_transfer_editorial,
                'release_config_sha256': sha256(Path(retreat_transfer_editorial).read_bytes()),
                'proof': duel_report}
        changed_records.setdefault(common_path, []).extend(duel_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend(['RETREAT_TRANSFER_NATIVE_SELECTION_METADATA', 'RETREAT_TRANSFER_EXACT_ROLE_TABLE_LITERAL_NAMES_AND_POSTMACRO_WRAP'])

    declaration_responses_editorial = profile_config.get('declaration_responses_editorial')
    if declaration_responses_editorial:
        from dk4tool.patch.declaration_responses_editorial import apply_release as apply_declaration_responses_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, duel_report = apply_declaration_responses_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), declaration_responses_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['declaration_responses_editorial'] = {
                'release_config': declaration_responses_editorial,
                'release_config_sha256': sha256(Path(declaration_responses_editorial).read_bytes()),
                'proof': duel_report}
        changed_records.setdefault(common_path, []).extend(duel_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend(['NPC_DECLARATION_NATIVE_SELECTION_METADATA', 'NPC_DECLARATION_EXACT_ACTOR_TABLE_AND_POSTMACRO_WRAP'])

    sea_responses_editorial = profile_config.get('sea_responses_editorial')
    if sea_responses_editorial:
        from dk4tool.patch.sea_responses_editorial import apply_release as apply_sea_responses_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, duel_report = apply_sea_responses_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), sea_responses_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['sea_responses_editorial'] = {
                'release_config': sea_responses_editorial,
                'release_config_sha256': sha256(Path(sea_responses_editorial).read_bytes()),
                'proof': duel_report}
        changed_records.setdefault(common_path, []).extend(duel_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend(['SEA_INSPECTION_NATIVE_SELECTION_METADATA', 'SEA_INSPECTION_EXACT_ROLE_TABLE_AND_POSTMACRO_WRAP'])

    inspection_status_editorial = profile_config.get('inspection_status_editorial')
    if inspection_status_editorial:
        from dk4tool.patch.inspection_status_editorial import apply_release as apply_inspection_status_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, duel_report = apply_inspection_status_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), inspection_status_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['inspection_status_editorial'] = {
                'release_config': inspection_status_editorial,
                'release_config_sha256': sha256(Path(inspection_status_editorial).read_bytes()),
                'proof': duel_report}
        changed_records.setdefault(common_path, []).extend(duel_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend(['INSPECTION_STATUS_NATIVE_METADATA', 'INSPECTION_STATUS_LITERAL_SYSTEM_MODAL_TEXT'])

    fatigue_status_editorial = profile_config.get('fatigue_status_editorial')
    if fatigue_status_editorial:
        from dk4tool.patch.fatigue_status_editorial import apply_release as apply_fatigue_status_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, duel_report = apply_fatigue_status_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), fatigue_status_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['fatigue_status_editorial'] = {
                'release_config': fatigue_status_editorial,
                'release_config_sha256': sha256(Path(fatigue_status_editorial).read_bytes()),
                'proof': duel_report}
        changed_records.setdefault(common_path, []).extend(duel_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend(['FATIGUE_STATUS_NATIVE_METADATA', 'FATIGUE_STATUS_SOURCE_NUMERIC_SYSTEM_MODAL_TEXT'])

    screenshot_repairs = profile_config.get('screenshot_text_repairs')
    if screenshot_repairs:
        from dk4tool.patch.screenshot_text_repairs import apply_release as apply_screenshot_repairs

        repair_report = apply_screenshot_repairs(candidate, baseline, screenshot_repairs)
        release_batches.extend(Path(p) for p in repair_report['batches'])
        for file_path in repair_report['target_file_sha256']:
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['screenshot_text_repairs'] = {
                'release_config': screenshot_repairs,
                'release_config_sha256': sha256(Path(screenshot_repairs).read_bytes()),
                'proof': repair_report}
            changed_records.setdefault(file_path, []).extend(
                r['id'] for r in repair_report['changed_records'] if r['file_path'] == file_path)

    choice_centering = profile_config.get('ship_advice_choice_centering')
    if choice_centering:
        from dk4tool.patch.ship_advice_choice_centering import apply_release as apply_choice_centering

        choice_report = apply_choice_centering(candidate, baseline, choice_centering)
        release_batches.extend(Path(p) for p in choice_report['batches'])
        file_path = '/data/SC0.DK4'
        grouped.setdefault(file_path, [])
        relocation_checks.setdefault(file_path, {})['ship_advice_choice_centering'] = {
            'release_config': choice_centering,
            'release_config_sha256': sha256(Path(choice_centering).read_bytes()),
            'proof': choice_report}
        changed_records.setdefault(file_path, []).extend(choice_report['changed_records'])

    hot_spring_editorial = profile_config.get('hot_spring_editorial')
    if hot_spring_editorial:
        from dk4tool.patch.hot_spring_editorial import apply_release as apply_hot_spring_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, duel_report = apply_hot_spring_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), hot_spring_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['hot_spring_editorial'] = {
                'release_config': hot_spring_editorial,
                'release_config_sha256': sha256(Path(hot_spring_editorial).read_bytes()),
                'proof': duel_report}
        changed_records.setdefault(common_path, []).extend(duel_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend(['HOT_SPRING_NATIVE_METADATA_AND_SELECTOR_KEYS', 'HOT_SPRING_ROLE1_SOURCE_DIALOGUE'])

    hot_spring_notice_editorial = profile_config.get('hot_spring_notice_editorial')
    if hot_spring_notice_editorial:
        from dk4tool.patch.hot_spring_notice_editorial import apply_release as apply_hot_spring_notice_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, duel_report = apply_hot_spring_notice_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), hot_spring_notice_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['hot_spring_notice_editorial'] = {
                'release_config': hot_spring_notice_editorial,
                'release_config_sha256': sha256(Path(hot_spring_notice_editorial).read_bytes()),
                'proof': duel_report}
        changed_records.setdefault(common_path, []).extend(duel_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend(['HOT_SPRING_NOTICE_NATIVE_METADATA', 'HOT_SPRING_OPTIONAL_EXPERIENCE_MODAL_TEXT'])

    search_reports_editorial = profile_config.get('search_reports_editorial')
    if search_reports_editorial:
        from dk4tool.patch.search_reports_editorial import apply_release as apply_search_reports_editorial

        common_path, arm_path = '/COMMON/MESFILE.DK4', '/__arm9__.bin'
        final_common, final_arm, duel_report = apply_search_reports_editorial(
            candidate.read_file(common_path), candidate.read_file(arm_path), search_reports_editorial)
        for file_path, data in ((common_path, final_common), (arm_path, final_arm)):
            candidate.replace_file(file_path, data)
            grouped.setdefault(file_path, [])
            relocation_checks.setdefault(file_path, {})['search_reports_editorial'] = {
                'release_config': search_reports_editorial,
                'release_config_sha256': sha256(Path(search_reports_editorial).read_bytes()),
                'proof': duel_report}
        changed_records.setdefault(common_path, []).extend(duel_report['changed_records'])
        changed_records.setdefault(arm_path, []).extend(['SEARCH_REPORTS_NATIVE_METADATA_AND_EXACT_TABLE_KEYS', 'SEARCH_ROLE1_ROLE7_AND_LOSS_MODAL_SOURCE_TEXT'])

    lil_opening_editorial = profile_config.get('lil_opening_editorial')
    if lil_opening_editorial:
        from dk4tool.patch.lil_opening_editorial import apply_release as apply_lil_opening_editorial

        opening_report = apply_lil_opening_editorial(candidate, baseline, lil_opening_editorial)
        file_path = '/data/SC2.DK4'
        grouped.setdefault(file_path, [])
        changed_records.setdefault(file_path, []).extend(row['id'] for row in opening_report['changed_records'])
        relocation_checks.setdefault(file_path, {})['lil_opening_editorial'] = {
            'release_config': lil_opening_editorial,
            'release_config_sha256': sha256(Path(lil_opening_editorial).read_bytes()),
            'proof': opening_report}
        opening_batch = Path(opening_report['manuscript'])
        if opening_batch in release_batches:
            raise ValueError('Lil opening must run only after the frozen cumulative stages')
        release_batches.append(opening_batch)

    lil_lessons_editorial = profile_config.get('lil_lessons_editorial')
    if lil_lessons_editorial:
        from dk4tool.patch.lil_lessons_editorial import apply_release as apply_lil_lessons_editorial

        lesson_report = apply_lil_lessons_editorial(candidate, baseline, lil_lessons_editorial)
        file_path = '/data/SC2.DK4'
        grouped.setdefault(file_path, [])
        changed_records.setdefault(file_path, []).extend(row['id'] for row in lesson_report['changed_records'])
        relocation_checks.setdefault(file_path, {})['lil_lessons_editorial'] = {
            'release_config': lil_lessons_editorial,
            'release_config_sha256': sha256(Path(lil_lessons_editorial).read_bytes()),
            'proof': lesson_report}
        for name in ('manuscript', 'choices'):
            lesson_batch = Path(lesson_report[name])
            if lesson_batch in release_batches:
                raise ValueError('Lil lessons must run only after the frozen cumulative stages')
            release_batches.append(lesson_batch)

    reinforcement_faction_prose = profile_config.get('reinforcement_faction_prose')
    if reinforcement_faction_prose:
        from dk4tool.patch.reinforcement_faction_prose import apply_release as apply_reinforcement_faction_prose

        faction_report = apply_reinforcement_faction_prose(candidate, baseline, reinforcement_faction_prose)
        file_path = '/COMMON/MESFILE.DK4'
        grouped.setdefault(file_path, [])
        changed_records.setdefault(file_path, []).extend(row['id'] for row in faction_report['changed_records'])
        relocation_checks.setdefault(file_path, {})['reinforcement_faction_prose'] = {
            'release_config': reinforcement_faction_prose,
            'release_config_sha256': sha256(Path(reinforcement_faction_prose).read_bytes()),
            'proof': faction_report}
        faction_batch = Path(faction_report['manuscript'])
        if faction_batch in release_batches:
            raise ValueError('Faction prose must run only after the frozen cumulative stages')
        release_batches.append(faction_batch)

    lil_trade_routes_editorial = profile_config.get('lil_trade_routes_editorial')
    if lil_trade_routes_editorial:
        from dk4tool.patch.lil_trade_routes_editorial import apply_release as apply_lil_trade_routes_editorial

        trade_report = apply_lil_trade_routes_editorial(candidate, baseline, lil_trade_routes_editorial)
        file_path = '/data/SC2.DK4'
        grouped.setdefault(file_path, [])
        changed_records.setdefault(file_path, []).extend(row['id'] for row in trade_report['changed_records'])
        relocation_checks.setdefault(file_path, {})['lil_trade_routes_editorial'] = {
            'release_config': lil_trade_routes_editorial,
            'release_config_sha256': sha256(Path(lil_trade_routes_editorial).read_bytes()),
            'proof': trade_report}
        trade_batch = Path(trade_report['manuscript'])
        if trade_batch in release_batches:
            raise ValueError('Lil trade routes must run only after the frozen cumulative stages')
        release_batches.append(trade_batch)

    lil_stockholm_editorial = profile_config.get('lil_stockholm_editorial')
    if lil_stockholm_editorial:
        from dk4tool.patch.lil_stockholm_editorial import apply_release as apply_lil_stockholm_editorial

        stockholm_report = apply_lil_stockholm_editorial(candidate, baseline, lil_stockholm_editorial)
        file_path = '/data/SC2.DK4'
        grouped.setdefault(file_path, [])
        changed_records.setdefault(file_path, []).extend(row['id'] for row in stockholm_report['changed_records'])
        relocation_checks.setdefault(file_path, {})['lil_stockholm_editorial'] = {
            'release_config': lil_stockholm_editorial,
            'release_config_sha256': sha256(Path(lil_stockholm_editorial).read_bytes()),
            'proof': stockholm_report}
        stockholm_batch = Path(stockholm_report['manuscript'])
        if stockholm_batch in release_batches:
            raise ValueError('Stockholm must run after the complete frozen cumulative stages')
        release_batches.append(stockholm_batch)

    lil_london_editorial = profile_config.get('lil_london_editorial')
    if lil_london_editorial:
        from dk4tool.patch.lil_london_editorial import apply_release as apply_lil_london_editorial

        london_report = apply_lil_london_editorial(candidate, baseline, lil_london_editorial)
        file_path = '/data/SC2.DK4'
        grouped.setdefault(file_path, [])
        changed_records.setdefault(file_path, []).extend(row['id'] for row in london_report['changed_records'])
        relocation_checks.setdefault(file_path, {})['lil_london_editorial'] = {
            'release_config': lil_london_editorial,
            'release_config_sha256': sha256(Path(lil_london_editorial).read_bytes()),
            'proof': london_report}
        london_batch = Path(london_report['manuscript'])
        if london_batch in release_batches:
            raise ValueError('London must run after the complete frozen cumulative stages')
        release_batches.append(london_batch)

    lil_speyer_editorial = profile_config.get('lil_speyer_editorial')
    if lil_speyer_editorial:
        from dk4tool.patch.lil_speyer_editorial import apply_release as apply_lil_speyer_editorial

        speyer_report = apply_lil_speyer_editorial(candidate, baseline, lil_speyer_editorial)
        file_path = '/data/SC2.DK4'
        grouped.setdefault(file_path, [])
        changed_records.setdefault(file_path, []).extend(row['id'] for row in speyer_report['changed_records'])
        relocation_checks.setdefault(file_path, {})['lil_speyer_editorial'] = {
            'release_config': lil_speyer_editorial,
            'release_config_sha256': sha256(Path(lil_speyer_editorial).read_bytes()),
            'proof': speyer_report}
        for batch_name in ('manuscript', 'choices'):
            speyer_batch = Path(speyer_report[batch_name])
            if speyer_batch in release_batches:
                raise ValueError('Speyer must run after the complete frozen cumulative stages')
            release_batches.append(speyer_batch)

    lil_hamburg_editorial = profile_config.get('lil_hamburg_editorial')
    if lil_hamburg_editorial:
        from dk4tool.patch.lil_hamburg_editorial import apply_release as apply_lil_hamburg_editorial

        hamburg_report = apply_lil_hamburg_editorial(candidate, baseline, lil_hamburg_editorial)
        file_path = '/data/SC2.DK4'
        grouped.setdefault(file_path, [])
        changed_records.setdefault(file_path, []).extend(row['id'] for row in hamburg_report['changed_records'])
        relocation_checks.setdefault(file_path, {})['lil_hamburg_editorial'] = {
            'release_config': lil_hamburg_editorial,
            'release_config_sha256': sha256(Path(lil_hamburg_editorial).read_bytes()),
            'proof': hamburg_report}
        for batch_name in ('manuscript', 'choices'):
            hamburg_batch = Path(hamburg_report[batch_name])
            if hamburg_batch in release_batches:
                raise ValueError('Hamburg must run after the complete frozen cumulative stages')
            release_batches.append(hamburg_batch)

    lil_lookout_affiliation = profile_config.get('lil_lookout_affiliation')
    if lil_lookout_affiliation:
        from dk4tool.patch.lil_lookout_affiliation import apply_release as apply_lil_lookout_affiliation

        lookout_report = apply_lil_lookout_affiliation(candidate, baseline, lil_lookout_affiliation)
        file_path = '/data/SC2.DK4'
        grouped.setdefault(file_path, [])
        changed_records.setdefault(file_path, []).extend(row['id'] for row in lookout_report['changed_records'])
        relocation_checks.setdefault(file_path, {})['lil_lookout_affiliation'] = {
            'release_config': lil_lookout_affiliation,
            'release_config_sha256': sha256(Path(lil_lookout_affiliation).read_bytes()),
            'proof': lookout_report}
        lookout_batch = Path(lookout_report['manuscript'])
        if lookout_batch in release_batches:
            raise ValueError('Lookout correction must run after the complete frozen cumulative stages')
        release_batches.append(lookout_batch)

    rafael_opening_editorial = profile_config.get('rafael_opening_editorial')
    if rafael_opening_editorial:
        from dk4tool.patch.rafael_opening_editorial import apply_release as apply_rafael_opening_editorial

        rafael_report = apply_rafael_opening_editorial(candidate, baseline, rafael_opening_editorial)
        file_path = '/data/SC0.DK4'
        grouped.setdefault(file_path, [])
        changed_records.setdefault(file_path, []).extend(row['id'] for row in rafael_report['changed_records'])
        relocation_checks.setdefault(file_path, {})['rafael_opening_editorial'] = {
            'release_config': rafael_opening_editorial,
            'release_config_sha256': sha256(Path(rafael_opening_editorial).read_bytes()),
            'proof': rafael_report}
        for batch_name in ('manuscript', 'choices'):
            rafael_batch = Path(rafael_report[batch_name])
            if rafael_batch in release_batches:
                raise ValueError('Rafael opening must run after the complete frozen cumulative stages')
            release_batches.append(rafael_batch)

    hodram_opening_editorial = profile_config.get('hodram_opening_editorial')
    if hodram_opening_editorial:
        from dk4tool.patch.hodram_opening_editorial_v2 import apply_release as apply_hodram_opening_editorial

        hodram_report = apply_hodram_opening_editorial(candidate, baseline, hodram_opening_editorial)
        file_path = '/data/SC1.DK4'
        grouped.setdefault(file_path, [])
        changed_records.setdefault(file_path, []).extend(row['id'] for row in hodram_report['changed_records'])
        relocation_checks.setdefault(file_path, {})['hodram_opening_editorial'] = {
            'release_config': hodram_opening_editorial,
            'release_config_sha256': sha256(Path(hodram_opening_editorial).read_bytes()),
            'proof': hodram_report}
        hodram_batch = Path(hodram_report['manuscript'])
        if hodram_batch in release_batches:
            raise ValueError('Hodram opening must run after the complete frozen cumulative stages')
        release_batches.append(hodram_batch)

    maria_opening_editorial = profile_config.get('maria_opening_editorial')
    if maria_opening_editorial:
        from dk4tool.patch.maria_opening_editorial import apply_release as apply_maria_opening_editorial

        maria_report = apply_maria_opening_editorial(candidate, baseline, maria_opening_editorial)
        file_path = '/data/SC3.DK4'
        grouped.setdefault(file_path, [])
        changed_records.setdefault(file_path, []).extend(row['id'] for row in maria_report['changed_records'])
        relocation_checks.setdefault(file_path, {})['maria_opening_editorial'] = {
            'release_config': maria_opening_editorial,
            'release_config_sha256': sha256(Path(maria_opening_editorial).read_bytes()),
            'proof': maria_report}
        maria_batch = Path(maria_report['manuscript'])
        if maria_batch in release_batches:
            raise ValueError('Maria opening must run after the complete frozen cumulative stages')
        release_batches.append(maria_batch)

    primary_town_services = profile_config.get('primary_town_services_editorial')
    if primary_town_services:
        from dk4tool.patch.primary_town_services_editorial import apply_release as apply_primary_town_services

        town_report = apply_primary_town_services(candidate, baseline, primary_town_services)
        for town_path in ('/COMMON/MESFILE.DK4', '/__arm9__.bin'):
            grouped.setdefault(town_path, [])
            relocation_checks.setdefault(town_path, {})['primary_town_services_editorial'] = {
                'release_config': primary_town_services,
                'release_config_sha256': sha256(Path(primary_town_services).read_bytes()),
                'proof': town_report}
        changed_records.setdefault('/COMMON/MESFILE.DK4', []).extend(row['id'] for row in town_report['changed_records'])
        changed_records.setdefault('/__arm9__.bin', []).append('PRIMARY_TOWN84_SOURCE_BOUND_LITERAL_ROUTES_AND_COMMON0_DIRECTORY')
        town_batch = Path(town_report['manuscript'])
        if town_batch in release_batches:
            raise ValueError('Primary town layer must run after all frozen cumulative stages')
        release_batches.append(town_batch)

    square_context = profile_config.get('square_contextual_editorial')
    if square_context:
        from dk4tool.patch.square_contextual_editorial import apply_release as apply_square_context

        square_report = apply_square_context(candidate, baseline, square_context)
        for square_path in ('/COMMON/MESFILE.DK4', '/__arm9__.bin'):
            grouped.setdefault(square_path, [])
            relocation_checks.setdefault(square_path, {})['square_contextual_editorial'] = {
                'release_config': square_context,
                'release_config_sha256': sha256(Path(square_context).read_bytes()),
                'proof': square_report}
        changed_records.setdefault('/COMMON/MESFILE.DK4', []).extend(row['id'] for row in square_report['changed_records'])
        changed_records.setdefault('/__arm9__.bin', []).append('SQUARE_FOUR_PARAGRAPHS_COMMON8_9_METADATA_ONLY')
        square_batch = Path(square_report['manuscript'])
        if square_batch in release_batches:
            raise ValueError('Square layer must run after all frozen cumulative stages')
        release_batches.append(square_batch)

    town_trade_port = profile_config.get('town_trade_port_contextual_editorial')
    if town_trade_port:
        from dk4tool.patch.town_trade_port_contextual_editorial import apply_release as apply_town_trade_port

        trade_report = apply_town_trade_port(candidate, baseline, town_trade_port)
        for trade_path in ('/COMMON/MESFILE.DK4', '/__arm9__.bin'):
            grouped.setdefault(trade_path, [])
            relocation_checks.setdefault(trade_path, {})['town_trade_port_contextual_editorial'] = {
                'release_config': town_trade_port,
                'release_config_sha256': sha256(Path(town_trade_port).read_bytes()),
                'proof': trade_report}
        changed_records.setdefault('/COMMON/MESFILE.DK4', []).extend(row['id'] for row in trade_report['changed_records'])
        changed_records.setdefault('/__arm9__.bin', []).append('TREND654655_OWNED_SELECTOR_CODEC_STACK_BRIDGES_AND_COMMON7_METADATA')
        trade_batch = Path(trade_report['manuscript'])
        if trade_batch in release_batches:
            raise ValueError('Shared trade and Port layer must run after frozen cumulative stages')
        release_batches.append(trade_batch)

    refit_context = profile_config.get('refit_contextual_spritsail')
    if refit_context:
        from dk4tool.patch.refit_contextual_spritsail_v1 import apply_release as apply_refit_context

        refit_context_report = apply_refit_context(candidate, baseline, refit_context)
        for refit_path in ('/COMMON/MESFILE.DK4', '/__arm9__.bin'):
            grouped.setdefault(refit_path, [])
            relocation_checks.setdefault(refit_path, {})['refit_contextual_spritsail'] = {
                'release_config': refit_context,
                'release_config_sha256': sha256(Path(refit_context).read_bytes()),
                'proof': refit_context_report}
        changed_records.setdefault('/COMMON/MESFILE.DK4', []).extend(row['id'] for row in refit_context_report['changed_records'])
        changed_records.setdefault('/__arm9__.bin', []).append('REFIT_SPRITSAIL_OWNED_COMPONENT_LABEL_133234_133240')
        refit_context_batch = Path(refit_context_report['manuscript'])
        if refit_context_batch in release_batches:
            raise ValueError('Refit terminology successor must run after the complete cumulative stack')
        release_batches.append(refit_context_batch)

    surrender_advice = profile_config.get('surrender_advice_contextual')
    if surrender_advice:
        from dk4tool.patch.surrender_advice_contextual_v1 import apply_release as apply_surrender_advice

        surrender_advice_report = apply_surrender_advice(candidate, baseline, surrender_advice)
        for advice_path in ('/COMMON/MESFILE.DK4', '/__arm9__.bin'):
            grouped.setdefault(advice_path, [])
            relocation_checks.setdefault(advice_path, {})['surrender_advice_contextual'] = {
                'release_config': surrender_advice,
                'release_config_sha256': sha256(Path(surrender_advice).read_bytes()),
                'proof': surrender_advice_report}
        changed_records.setdefault('/COMMON/MESFILE.DK4', []).extend(row['id'] for row in surrender_advice_report['changed_records'])
        changed_records.setdefault('/__arm9__.bin', []).append('SURRENDER_ADVICE_COMMON22_DIRECTORY_AND_OFFSETS')
        advice_batch = Path(surrender_advice_report['manuscript'])
        if advice_batch in release_batches:
            raise ValueError('Surrender advice must run after the complete cumulative stack')
        release_batches.append(advice_batch)

    lil_seville = profile_config.get('lil_seville_editorial')
    if lil_seville:
        from dk4tool.patch.lil_seville_editorial import apply_release as apply_lil_seville

        lil_seville_report = apply_lil_seville(candidate, baseline, lil_seville)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_seville_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_seville_editorial'] = {
            'release_config': lil_seville,
            'release_config_sha256': sha256(Path(lil_seville).read_bytes()),
            'proof': lil_seville_report}
        for seville_key in ('manuscript', 'choices'):
            seville_batch = Path(lil_seville_report[seville_key])
            if seville_batch in release_batches:
                raise ValueError('Seville must run once after the complete V2674 stack')
            release_batches.append(seville_batch)

    lil_post_seville = profile_config.get('lil_post_seville_editorial')
    if lil_post_seville:
        from dk4tool.patch.lil_post_seville_editorial import apply_release as apply_lil_post_seville

        lil_post_seville_report = apply_lil_post_seville(candidate, baseline, lil_post_seville)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_post_seville_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_post_seville_editorial'] = {
            'release_config': lil_post_seville,
            'release_config_sha256': sha256(Path(lil_post_seville).read_bytes()),
            'proof': lil_post_seville_report}
        post_seville_batch = Path(lil_post_seville_report['manuscript'])
        if post_seville_batch in release_batches:
            raise ValueError('Post-Seville must run once after the complete V2724 stack')
        release_batches.append(post_seville_batch)

    lil_mediterranean_africa = profile_config.get('lil_mediterranean_africa_editorial')
    if lil_mediterranean_africa:
        from dk4tool.patch.lil_mediterranean_africa_editorial import apply_release as apply_lil_mediterranean_africa

        lil_mediterranean_africa_report = apply_lil_mediterranean_africa(candidate, baseline, lil_mediterranean_africa)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_mediterranean_africa_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_mediterranean_africa_editorial'] = {
            'release_config': lil_mediterranean_africa,
            'release_config_sha256': sha256(Path(lil_mediterranean_africa).read_bytes()),
            'proof': lil_mediterranean_africa_report}
        for mediterranean_africa_key in ('manuscript', 'choices'):
            mediterranean_africa_batch = Path(lil_mediterranean_africa_report[mediterranean_africa_key])
            if mediterranean_africa_batch in release_batches:
                raise ValueError('Mediterranean/Africa must run once after the complete V2750 stack')
            release_batches.append(mediterranean_africa_batch)

    lil_india_polder = profile_config.get('lil_india_polder_editorial')
    if lil_india_polder:
        from dk4tool.patch.lil_india_polder_editorial import apply_release as apply_lil_india_polder

        lil_india_polder_report = apply_lil_india_polder(candidate, baseline, lil_india_polder)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_india_polder_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_india_polder_editorial'] = {
            'release_config': lil_india_polder,
            'release_config_sha256': sha256(Path(lil_india_polder).read_bytes()),
            'proof': lil_india_polder_report}
        india_polder_batch = Path(lil_india_polder_report['manuscript'])
        if india_polder_batch in release_batches:
            raise ValueError('India/polder must run once after the complete V2783 stack')
        release_batches.append(india_polder_batch)

    lil_goods_mediterranean = profile_config.get('lil_goods_mediterranean_editorial')
    if lil_goods_mediterranean:
        from dk4tool.patch.lil_goods_mediterranean_editorial import apply_release as apply_lil_goods_mediterranean

        lil_goods_mediterranean_report = apply_lil_goods_mediterranean(candidate, baseline, lil_goods_mediterranean)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_goods_mediterranean_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_goods_mediterranean_editorial'] = {
            'release_config': lil_goods_mediterranean,
            'release_config_sha256': sha256(Path(lil_goods_mediterranean).read_bytes()),
            'proof': lil_goods_mediterranean_report}
        goods_mediterranean_batch = Path(lil_goods_mediterranean_report['manuscript'])
        if goods_mediterranean_batch in release_batches:
            raise ValueError('goods/Mediterranean must run once after the complete V2814 stack')
        release_batches.append(goods_mediterranean_batch)

    lil_kuhn_alliance = profile_config.get('lil_kuhn_alliance_editorial')
    if lil_kuhn_alliance:
        from dk4tool.patch.lil_kuhn_alliance_editorial import apply_release as apply_lil_kuhn_alliance

        lil_kuhn_alliance_report = apply_lil_kuhn_alliance(candidate, baseline, lil_kuhn_alliance)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_kuhn_alliance_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_kuhn_alliance_editorial'] = {
            'release_config': lil_kuhn_alliance,
            'release_config_sha256': sha256(Path(lil_kuhn_alliance).read_bytes()),
            'proof': lil_kuhn_alliance_report}
        goods_mediterranean_batch = Path(lil_kuhn_alliance_report['manuscript'])
        if goods_mediterranean_batch in release_batches:
            raise ValueError('goods/Mediterranean must run once after the complete V2840 stack')
        release_batches.append(goods_mediterranean_batch)

    lil_kuhn_china = profile_config.get('lil_kuhn_china_editorial')
    if lil_kuhn_china:
        from dk4tool.patch.lil_kuhn_china_editorial import apply_release as apply_lil_kuhn_china

        lil_kuhn_china_report = apply_lil_kuhn_china(candidate, baseline, lil_kuhn_china)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_kuhn_china_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_kuhn_china_editorial'] = {
            'release_config': lil_kuhn_china,
            'release_config_sha256': sha256(Path(lil_kuhn_china).read_bytes()),
            'proof': lil_kuhn_china_report}
        kuhn_china_batch = Path(lil_kuhn_china_report['manuscript'])
        if kuhn_china_batch in release_batches:
            raise ValueError('Kuhn/China must run once after the complete V2883 stack')
        release_batches.append(kuhn_china_batch)

    lil_kuhn_resolution = profile_config.get('lil_kuhn_resolution_editorial')
    if lil_kuhn_resolution:
        from dk4tool.patch.lil_kuhn_resolution_editorial import apply_release as apply_lil_kuhn_resolution

        lil_kuhn_resolution_report = apply_lil_kuhn_resolution(candidate, baseline, lil_kuhn_resolution)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_kuhn_resolution_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_kuhn_resolution_editorial'] = {
            'release_config': lil_kuhn_resolution,
            'release_config_sha256': sha256(Path(lil_kuhn_resolution).read_bytes()),
            'proof': lil_kuhn_resolution_report}
        for kuhn_resolution_key in ('manuscript', 'choices'):
            kuhn_resolution_batch = Path(lil_kuhn_resolution_report[kuhn_resolution_key])
            if kuhn_resolution_batch in release_batches:
                raise ValueError('Kuhn-resolution must run once after the complete V2916 stack')
            release_batches.append(kuhn_resolution_batch)

    lil_clifford_north_new_world = profile_config.get('lil_clifford_north_new_world_editorial')
    if lil_clifford_north_new_world:
        from dk4tool.patch.lil_clifford_north_new_world_editorial import apply_release as apply_lil_clifford_north_new_world

        lil_clifford_north_new_world_report = apply_lil_clifford_north_new_world(candidate, baseline, lil_clifford_north_new_world)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_clifford_north_new_world_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_clifford_north_new_world_editorial'] = {
            'release_config': lil_clifford_north_new_world,
            'release_config_sha256': sha256(Path(lil_clifford_north_new_world).read_bytes()),
            'proof': lil_clifford_north_new_world_report}
        clifford_north_new_world_batch = Path(lil_clifford_north_new_world_report['manuscript'])
        if clifford_north_new_world_batch in release_batches:
            raise ValueError('Clifford/north/NewWorld must run once after the complete V2958 stack')
        release_batches.append(clifford_north_new_world_batch)

    lil_homecoming_ian = profile_config.get('lil_homecoming_ian_editorial')
    if lil_homecoming_ian:
        from dk4tool.patch.lil_homecoming_ian_editorial import apply_release as apply_lil_homecoming_ian

        lil_homecoming_ian_report = apply_lil_homecoming_ian(candidate, baseline, lil_homecoming_ian)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_homecoming_ian_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_homecoming_ian_editorial'] = {
            'release_config': lil_homecoming_ian,
            'release_config_sha256': sha256(Path(lil_homecoming_ian).read_bytes()),
            'proof': lil_homecoming_ian_report}
        homecoming_ian_batch = Path(lil_homecoming_ian_report['manuscript'])
        if homecoming_ian_batch in release_batches:
            raise ValueError('Homecoming/Ian must run once after the complete V2996 stack')
        release_batches.append(homecoming_ian_batch)

    lil_christina_mivor = profile_config.get('lil_christina_mivor_editorial')
    if lil_christina_mivor:
        from dk4tool.patch.lil_christina_mivor_editorial_v2 import apply_release as apply_lil_christina_mivor

        lil_christina_mivor_report = apply_lil_christina_mivor(candidate, baseline, lil_christina_mivor)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_christina_mivor_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_christina_mivor_editorial'] = {
            'release_config': lil_christina_mivor,
            'release_config_sha256': sha256(Path(lil_christina_mivor).read_bytes()),
            'proof': lil_christina_mivor_report}
        christina_mivor_batch = Path(lil_christina_mivor_report['manuscript'])
        if christina_mivor_batch in release_batches:
            raise ValueError('Christina/Mivor must run once after the complete V3029 stack')
        release_batches.append(christina_mivor_batch)

    lil_recruits_julian = profile_config.get('lil_recruits_julian_editorial')
    if lil_recruits_julian:
        from dk4tool.patch.lil_recruits_julian_editorial import apply_release as apply_lil_recruits_julian

        lil_recruits_julian_report = apply_lil_recruits_julian(candidate, baseline, lil_recruits_julian)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_recruits_julian_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_recruits_julian_editorial'] = {
            'release_config': lil_recruits_julian,
            'release_config_sha256': sha256(Path(lil_recruits_julian).read_bytes()),
            'proof': lil_recruits_julian_report}
        for recruits_julian_key in ('manuscript', 'choices'):
            recruits_julian_batch = Path(lil_recruits_julian_report[recruits_julian_key])
            if recruits_julian_batch in release_batches:
                raise ValueError('Recruits/Julian must run once after the complete V3066 stack')
            release_batches.append(recruits_julian_batch)

    lil_crew_items = profile_config.get('lil_crew_items_editorial')
    if lil_crew_items:
        from dk4tool.patch.lil_crew_items_editorial import apply_release as apply_lil_crew_items

        lil_crew_items_report = apply_lil_crew_items(candidate, baseline, lil_crew_items)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_crew_items_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_crew_items_editorial'] = {
            'release_config': lil_crew_items,
            'release_config_sha256': sha256(Path(lil_crew_items).read_bytes()),
            'proof': lil_crew_items_report}
        for crew_items_key in ('manuscript', 'choices'):
            crew_items_batch = Path(lil_crew_items_report[crew_items_key])
            if crew_items_batch in release_batches:
                raise ValueError('Crew/Items must run once after the complete V3103 stack')
            release_batches.append(crew_items_batch)

    lil_shrines = profile_config.get('lil_shrines_temples_editorial')
    if lil_shrines:
        from dk4tool.patch.lil_shrines_temples_editorial import apply_release as apply_lil_shrines

        lil_shrines_report = apply_lil_shrines(candidate, baseline, lil_shrines)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_shrines_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_shrines_temples_editorial'] = {
            'release_config': lil_shrines,
            'release_config_sha256': sha256(Path(lil_shrines).read_bytes()),
            'proof': lil_shrines_report}
        for shrines_key in ('manuscript', 'actor_styles', 'choices'):
            shrines_batch = Path(lil_shrines_report[shrines_key])
            if shrines_batch in release_batches:
                raise ValueError('Shrines/Temples must run once after the complete V3144 stack')
            release_batches.append(shrines_batch)

    lil_cultural = profile_config.get('lil_B111_B119_editorial')
    if lil_cultural:
        from dk4tool.patch.lil_B111_B119_editorial import apply_release as apply_lil_cultural

        lil_cultural_report = apply_lil_cultural(candidate, baseline, lil_cultural)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_cultural_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B111_B119_editorial'] = {
            'release_config': lil_cultural,
            'release_config_sha256': sha256(Path(lil_cultural).read_bytes()),
            'proof': lil_cultural_report}
        for cultural_key in ('manuscript', 'actor_styles'):
            cultural_batch = Path(lil_cultural_report[cultural_key])
            if cultural_batch in release_batches:
                raise ValueError('B111-B119 must run once after the complete V3204 stack')
            release_batches.append(cultural_batch)

    lil_more = profile_config.get('lil_B122_B127_editorial')
    if lil_more:
        from dk4tool.patch.lil_B122_B127_editorial_v2 import apply_release as apply_lil_more

        lil_more_report = apply_lil_more(candidate, baseline, lil_more)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_more_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B122_B127_editorial'] = {
            'release_config': lil_more,
            'release_config_sha256': sha256(Path(lil_more).read_bytes()),
            'proof': lil_more_report}
        for more_key in ('manuscript', 'choices'):
            more_batch = Path(lil_more_report[more_key])
            if more_batch in release_batches:
                raise ValueError('B122-B127 must run once after the complete V3251 stack')
            release_batches.append(more_batch)

    lil_more = profile_config.get('lil_B131_B133_editorial')
    if lil_more:
        from dk4tool.patch.lil_B131_B133_editorial_v1 import apply_release as apply_lil_more

        lil_more_report = apply_lil_more(candidate, baseline, lil_more)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_more_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B131_B133_editorial'] = {
            'release_config': lil_more,
            'release_config_sha256': sha256(Path(lil_more).read_bytes()),
            'proof': lil_more_report}
        for more_key in ('manuscript', 'choices'):
            more_batch = Path(lil_more_report[more_key])
            if more_batch in release_batches:
                raise ValueError('B131/B133 must run once after the complete V3300 stack')
            release_batches.append(more_batch)

    lil_more = profile_config.get('lil_B135_B136_editorial')
    if lil_more:
        from dk4tool.patch.lil_B135_B136_editorial_v1 import apply_release as apply_lil_more

        lil_more_report = apply_lil_more(candidate, baseline, lil_more)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_more_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B135_B136_editorial'] = {
            'release_config': lil_more,
            'release_config_sha256': sha256(Path(lil_more).read_bytes()),
            'proof': lil_more_report}
        for more_key in ('manuscript',):
            more_batch = Path(lil_more_report[more_key])
            if more_batch in release_batches:
                raise ValueError('B135/B136 must run once after the complete V3338 stack')
            release_batches.append(more_batch)

    lil_more = profile_config.get('lil_B137_editorial')
    if lil_more:
        from dk4tool.patch.lil_B137_editorial_v1 import apply_release as apply_lil_more

        lil_more_report = apply_lil_more(candidate, baseline, lil_more)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_more_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B137_editorial'] = {
            'release_config': lil_more,
            'release_config_sha256': sha256(Path(lil_more).read_bytes()),
            'proof': lil_more_report}
        for more_key in ('manuscript',):
            more_batch = Path(lil_more_report[more_key])
            if more_batch in release_batches:
                raise ValueError('B137 must run once after the complete V3372 stack')
            release_batches.append(more_batch)

    lil_more = profile_config.get('lil_B137_editorial_v2')
    if lil_more:
        from dk4tool.patch.lil_B137_editorial_v2 import apply_release as apply_lil_more

        lil_more_report = apply_lil_more(candidate, baseline, lil_more)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_more_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B137_editorial_v2'] = {
            'release_config': lil_more,
            'release_config_sha256': sha256(Path(lil_more).read_bytes()),
            'proof': lil_more_report}
        for more_key in ('manuscript',):
            more_batch = Path(lil_more_report[more_key])
            if more_batch in release_batches:
                raise ValueError('B137 must run once after the complete V3372 stack')
            release_batches.append(more_batch)

    lil_more = profile_config.get('lil_B138_editorial')
    if lil_more:
        from dk4tool.patch.lil_B138_editorial_v1 import apply_release as apply_lil_more

        lil_more_report = apply_lil_more(candidate, baseline, lil_more)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_more_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B138_editorial'] = {
            'release_config': lil_more,
            'release_config_sha256': sha256(Path(lil_more).read_bytes()),
            'proof': lil_more_report}
        for more_key in ('manuscript',):
            more_batch = Path(lil_more_report[more_key])
            if more_batch in release_batches:
                raise ValueError('B138 must run once after the complete V3416 stack')
            release_batches.append(more_batch)

    lil_more = profile_config.get('lil_B139_B140_editorial')
    if lil_more:
        from dk4tool.patch.lil_B139_B140_editorial_v2 import apply_release as apply_lil_more

        lil_more_report = apply_lil_more(candidate, baseline, lil_more)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_more_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B139_B140_editorial'] = {
            'release_config': lil_more,
            'release_config_sha256': sha256(Path(lil_more).read_bytes()),
            'proof': lil_more_report}
        for more_key in ('manuscript',):
            more_batch = Path(lil_more_report[more_key])
            if more_batch in release_batches:
                raise ValueError('B139/B140 must run once after the complete V3450 stack')
            release_batches.append(more_batch)

    maria_more = profile_config.get('maria_B109_editorial')
    if maria_more:
        from dk4tool.patch.maria_B109_editorial_v1 import apply_release as apply_maria_more

        maria_more_report = apply_maria_more(candidate, baseline, maria_more)
        grouped.setdefault('/data/SC3.DK4', [])
        changed_records.setdefault('/data/SC3.DK4', []).extend(row['id'] for row in maria_more_report['changed_records'])
        relocation_checks.setdefault('/data/SC3.DK4', {})['maria_B109_editorial'] = {
            'release_config': maria_more,
            'release_config_sha256': sha256(Path(maria_more).read_bytes()),
            'proof': maria_more_report}
        more_batch = Path(maria_more_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('Maria B109 must run once after the complete V3487 stack')
        release_batches.append(more_batch)

    lil_funding = profile_config.get('lil_B141_editorial')
    if lil_funding:
        from dk4tool.patch.lil_B141_editorial_v1 import apply_release as apply_lil_funding

        lil_funding_report = apply_lil_funding(candidate, baseline, lil_funding)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_funding_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B141_editorial'] = {
            'release_config': lil_funding,
            'release_config_sha256': sha256(Path(lil_funding).read_bytes()),
            'proof': lil_funding_report}
        more_batch = Path(lil_funding_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B141 must run once after the complete V3526 stack')
        release_batches.append(more_batch)

    lil_polder_armor_map = profile_config.get('lil_B142_B145_editorial')
    if lil_polder_armor_map:
        from dk4tool.patch.lil_B142_B145_editorial_v1 import apply_release as apply_lil_polder_armor_map

        lil_polder_armor_map_report = apply_lil_polder_armor_map(candidate, baseline, lil_polder_armor_map)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_polder_armor_map_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B142_B145_editorial'] = {
            'release_config': lil_polder_armor_map,
            'release_config_sha256': sha256(Path(lil_polder_armor_map).read_bytes()),
            'proof': lil_polder_armor_map_report}
        more_batch = Path(lil_polder_armor_map_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B142-B145 must run once after the complete V3561 stack')
        release_batches.append(more_batch)

    lil_coin_al = profile_config.get('lil_B152_B154_editorial')
    if lil_coin_al:
        from dk4tool.patch.lil_B152_B154_editorial_v1 import apply_release as apply_lil_coin_al

        lil_coin_al_report = apply_lil_coin_al(candidate, baseline, lil_coin_al)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_coin_al_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B152_B154_editorial'] = {
            'release_config': lil_coin_al,
            'release_config_sha256': sha256(Path(lil_coin_al).read_bytes()),
            'proof': lil_coin_al_report}
        more_batch = Path(lil_coin_al_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B152-B154 must run once after the complete V3607 stack')
        release_batches.append(more_batch)

    lil_angelo = profile_config.get('lil_B155_editorial')
    if lil_angelo:
        from dk4tool.patch.lil_B155_editorial_v1 import apply_release as apply_lil_angelo

        lil_angelo_report = apply_lil_angelo(candidate, baseline, lil_angelo)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_angelo_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B155_editorial'] = {
            'release_config': lil_angelo,
            'release_config_sha256': sha256(Path(lil_angelo).read_bytes()),
            'proof': lil_angelo_report}
        more_batch = Path(lil_angelo_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B155 must run once after the complete V3650 stack')
        release_batches.append(more_batch)

    lil_ian = profile_config.get('lil_B156_editorial')
    if lil_ian:
        from dk4tool.patch.lil_B156_editorial_v1 import apply_release as apply_lil_ian

        lil_ian_report = apply_lil_ian(candidate, baseline, lil_ian)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_ian_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B156_editorial'] = {
            'release_config': lil_ian,
            'release_config_sha256': sha256(Path(lil_ian).read_bytes()),
            'proof': lil_ian_report}
        more_batch = Path(lil_ian_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B156 must run once after the complete V3692 stack')
        release_batches.append(more_batch)

    lil_carlo = profile_config.get('lil_B157_editorial')
    if lil_carlo:
        from dk4tool.patch.lil_B157_editorial_v1 import apply_release as apply_lil_carlo

        lil_carlo_report = apply_lil_carlo(candidate, baseline, lil_carlo)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_carlo_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B157_editorial'] = {
            'release_config': lil_carlo,
            'release_config_sha256': sha256(Path(lil_carlo).read_bytes()),
            'proof': lil_carlo_report}
        more_batch = Path(lil_carlo_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B157 must run once after the complete V3738 stack')
        release_batches.append(more_batch)

    lil_dance = profile_config.get('lil_B158_editorial')
    if lil_dance:
        from dk4tool.patch.lil_B158_editorial_v1 import apply_release as apply_lil_dance

        lil_dance_report = apply_lil_dance(candidate, baseline, lil_dance)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_dance_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B158_editorial'] = {
            'release_config': lil_dance,
            'release_config_sha256': sha256(Path(lil_dance).read_bytes()),
            'proof': lil_dance_report}
        more_batch = Path(lil_dance_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B158 must run once after the complete V3778 stack')
        release_batches.append(more_batch)

    lil_samwell = profile_config.get('lil_B159_editorial')
    if lil_samwell:
        from dk4tool.patch.lil_B159_editorial_v2 import apply_release as apply_lil_samwell

        lil_samwell_report = apply_lil_samwell(candidate, baseline, lil_samwell)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_samwell_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B159_editorial'] = {
            'release_config': lil_samwell,
            'release_config_sha256': sha256(Path(lil_samwell).read_bytes()),
            'proof': lil_samwell_report}
        more_batch = Path(lil_samwell_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B159 must run once after the complete V3819 stack')
        release_batches.append(more_batch)

    lil_missing_ship = profile_config.get('lil_B160_editorial')
    if lil_missing_ship:
        from dk4tool.patch.lil_B160_editorial_v1 import apply_release as apply_lil_missing_ship

        lil_missing_ship_report = apply_lil_missing_ship(candidate, baseline, lil_missing_ship)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_missing_ship_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B160_editorial'] = {
            'release_config': lil_missing_ship,
            'release_config_sha256': sha256(Path(lil_missing_ship).read_bytes()),
            'proof': lil_missing_ship_report}
        more_batch = Path(lil_missing_ship_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B160 must run once after the complete V3862 stack')
        release_batches.append(more_batch)

    lil_jam_return = profile_config.get('lil_B161_B163_editorial')
    if lil_jam_return:
        from dk4tool.patch.lil_B161_B163_editorial_v1 import apply_release as apply_lil_jam_return

        lil_jam_return_report = apply_lil_jam_return(candidate, baseline, lil_jam_return)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_jam_return_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B161_B163_editorial'] = {
            'release_config': lil_jam_return,
            'release_config_sha256': sha256(Path(lil_jam_return).read_bytes()),
            'proof': lil_jam_return_report}
        more_batch = Path(lil_jam_return_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B161-B163 must run once after the complete V3904 stack')
        release_batches.append(more_batch)

    lil_cesare_advice = profile_config.get('lil_B164_editorial')
    if lil_cesare_advice:
        from dk4tool.patch.lil_B164_editorial_v2 import apply_release as apply_lil_cesare_advice

        lil_cesare_advice_report = apply_lil_cesare_advice(candidate, baseline, lil_cesare_advice)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_cesare_advice_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B164_editorial'] = {
            'release_config': lil_cesare_advice,
            'release_config_sha256': sha256(Path(lil_cesare_advice).read_bytes()),
            'proof': lil_cesare_advice_report}
        for more_batch in [Path(lil_cesare_advice_report['manuscript']), Path(lil_cesare_advice_report['choices'])]:
            if more_batch in release_batches:
                raise ValueError('B164 must run once after the complete V3954 stack')
            release_batches.append(more_batch)

    lil_julio_argument = profile_config.get('lil_B165_editorial')
    if lil_julio_argument:
        from dk4tool.patch.lil_B165_editorial_v1 import apply_release as apply_lil_julio_argument

        lil_julio_argument_report = apply_lil_julio_argument(candidate, baseline, lil_julio_argument)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_julio_argument_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B165_editorial'] = {
            'release_config': lil_julio_argument,
            'release_config_sha256': sha256(Path(lil_julio_argument).read_bytes()),
            'proof': lil_julio_argument_report}
        more_batch = Path(lil_julio_argument_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B165 must run once after the complete V4002 stack')
        release_batches.append(more_batch)

    lil_manuel_advice = profile_config.get('lil_B166_editorial')
    if lil_manuel_advice:
        from dk4tool.patch.lil_B166_editorial_v1 import apply_release as apply_lil_manuel_advice

        lil_manuel_advice_report = apply_lil_manuel_advice(candidate, baseline, lil_manuel_advice)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_manuel_advice_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B166_editorial'] = {
            'release_config': lil_manuel_advice,
            'release_config_sha256': sha256(Path(lil_manuel_advice).read_bytes()),
            'proof': lil_manuel_advice_report}
        for more_batch in [Path(lil_manuel_advice_report['manuscript']), Path(lil_manuel_advice_report['choices'])]:
            if more_batch in release_batches:
                raise ValueError('B166 must run once after the complete V4046 stack')
            release_batches.append(more_batch)

    lil_sail_lesson = profile_config.get('lil_B167_editorial')
    if lil_sail_lesson:
        from dk4tool.patch.lil_B167_editorial_v2 import apply_release as apply_lil_sail_lesson

        lil_sail_lesson_report = apply_lil_sail_lesson(candidate, baseline, lil_sail_lesson)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_sail_lesson_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B167_editorial'] = {
            'release_config': lil_sail_lesson,
            'release_config_sha256': sha256(Path(lil_sail_lesson).read_bytes()),
            'proof': lil_sail_lesson_report}
        for more_batch in [Path(lil_sail_lesson_report['manuscript']), Path(lil_sail_lesson_report['choices'])]:
            if more_batch in release_batches:
                raise ValueError('B167 must run once after the complete V4110 stack')
            release_batches.append(more_batch)

    lil_mikhail = profile_config.get('lil_B168_editorial')
    if lil_mikhail:
        from dk4tool.patch.lil_B168_editorial_v1 import apply_release as apply_lil_mikhail

        lil_mikhail_report = apply_lil_mikhail(candidate, baseline, lil_mikhail)
        grouped.setdefault('/data/SC2.DK4', [])
        changed_records.setdefault('/data/SC2.DK4', []).extend(row['id'] for row in lil_mikhail_report['changed_records'])
        relocation_checks.setdefault('/data/SC2.DK4', {})['lil_B168_editorial'] = {
            'release_config': lil_mikhail,
            'release_config_sha256': sha256(Path(lil_mikhail).read_bytes()),
            'proof': lil_mikhail_report}
        more_batch = Path(lil_mikhail_report['manuscript'])
        if more_batch in release_batches:
            raise ValueError('B168 must run once after the complete V4160 stack')
        release_batches.append(more_batch)

    # Lexically valid "% o" and "% s" in translated prose still consume native
    # arguments absent from the Japanese source. Check final files, including
    # all post-batch stages, instead of accepting syntax alone as safety proof.
    from dk4tool.script.format_safety import reject_story_percent_commands

    percent_clean_path = Path('work/clean.nds')
    if sha256(percent_clean_path.read_bytes()) != 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d':
        raise ValueError('Exact clean Japanese source required for final story format contracts')
    percent_clean = NdsImage.open(percent_clean_path)
    percent_story_paths = [f'/data/SC{i}.DK4' for i in range(4)]
    story_percent_contract = reject_story_percent_commands(
        {p: percent_clean.read_file(p) for p in percent_story_paths},
        {p: candidate.read_file(p) for p in percent_story_paths})

    # A later stage must not overwrite the review-pending plaque material after
    # its own repair-stage checks have passed. This final check changes no bytes.
    from dk4tool.graphics.plaque_contract import verify_final_plaque_material

    final_plaque_contract = verify_final_plaque_material(candidate, percent_clean, profile_config)

    # Raw captions are merged early alongside archive sync layers. Recheck the
    # complete reviewed block after later stages, including preserved source art.
    from dk4tool.graphics.raw_art_contract import verify_final_raw_art

    final_raw_art_contract = verify_final_raw_art(candidate, baseline, percent_clean, release_batches)

    # Embedded copies are produced early. A later stage must not desynchronize
    # their letters, symbols, native tile banks, palettes or source metadata.
    from dk4tool.graphics.copy_contract import verify_final_graphics_copies

    final_graphics_copy_contract = verify_final_graphics_copies(candidate, baseline, release_batches, profile_config)

    # Source FE is an executable selector. Its CP932 re-encoding is never prose.
    # Reject the known corruption in every future playable profile, even when
    # a profile omits the repair stage or introduces it through a new batch.
    from dk4tool.patch.raphael_system_panel_release import reject_corrupt_panel_selectors

    reject_corrupt_panel_selectors(rom_files(candidate))
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
            "playable_story_pair_phase_enforced": True,
            "source_bound_story_printf_contracts_enforced": True,
            "final_reviewed_plaque_material_contract_enforced": final_plaque_contract['applicable'],
            "final_reviewed_raw_art_contract_enforced": final_raw_art_contract['applicable'],
            "final_registered_graphics_copy_contract_enforced": final_graphics_copy_contract['applicable'],
            "final_palace_menu_boundaries_enforced": not palace_label_contract['applicable'] or palace_label_contract['all_six_complete_labels_NUL_terminated_inside_owned_strings'],
            "fixed_text_two_byte_guards_enforced": True,
            "screen_entry_layout_enforced": True,
            "no_new_placeholder_fallbacks": True,
            "saved_rom_roundtrip": True,
            "mapped_ilnk_relocation_enforced": bool(relocation_checks)
            if relocation_checks
            else True,
        },
        "relocations": relocation_checks,
        "story_percent_contract": story_percent_contract,
        "final_plaque_contract": final_plaque_contract,
        "final_raw_art_contract": final_raw_art_contract,
        "final_graphics_copy_contract": final_graphics_copy_contract,
        "final_palace_menu_contract": palace_label_contract,
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
