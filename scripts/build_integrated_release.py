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
            layout_width=(
                int(record["layout_width"])
                if record.get("layout_width") is not None
                else None
            ),
        )
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
            "fixed_text_two_byte_guards_enforced": True,
            "screen_entry_layout_enforced": True,
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
