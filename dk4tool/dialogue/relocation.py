from __future__ import annotations

import hashlib
import json
import struct
from dataclasses import dataclass
from pathlib import Path

from ..formats.ilnk import IlnkContainer
from .encoder import encode_relocatable_dialogue
from .profiles import DialogueProfile


class DialogueRelocationError(ValueError):
    """Raised when a dialogue block cannot be relocated with proven references."""


@dataclass(frozen=True)
class RecordLayout:
    segment_index: int
    old_offset: int
    old_length: int
    new_offset: int
    new_length: int


@dataclass(frozen=True)
class InteriorEntryPoint:
    name: str
    segment_index: int
    old_intra_record_offset: int = 0
    new_intra_record_offset: int | None = None


@dataclass(frozen=True)
class RelocatedEntryPoint:
    name: str
    segment_index: int
    old_offset: int
    new_offset: int


@dataclass(frozen=True)
class BlockEntryPointMap:
    block_index: int
    external_references_complete: bool
    entry_points: tuple[InteriorEntryPoint, ...]


@dataclass(frozen=True)
class BlockRelocationPlan:
    block_index: int
    old_size: int
    new_size: int
    records: tuple[RecordLayout, ...]
    entry_points: tuple[RelocatedEntryPoint, ...]


@dataclass(frozen=True)
class CsBlockRelocationResult:
    rebuilt_file: bytes
    old_block: bytes
    new_block: bytes
    changed_segments: tuple[int, ...]
    parity_padded_segments: tuple[int, ...]
    size_delta: int


def plan_block_relocation(
    block: bytes,
    replacement_lengths: dict[int, int],
    entry_point_map: BlockEntryPointMap,
) -> BlockRelocationPlan:
    """Plan new record starts without writing any bytes.

    ILNK's outer block offsets can be rebuilt mechanically, but event code may enter a
    block at an interior record or byte offset. Any size change is therefore rejected
    until reverse engineering declares the block's reference inventory complete.
    """

    segments = block.split(b"\0")
    if any(index < 0 or index >= len(segments) for index in replacement_lengths):
        raise DialogueRelocationError("replacement references an unknown segment")
    if any(length < 0 for length in replacement_lengths.values()):
        raise DialogueRelocationError("replacement lengths cannot be negative")

    changes_size = any(
        replacement_lengths[index] != len(segments[index])
        for index in replacement_lengths
    )
    if changes_size and not entry_point_map.external_references_complete:
        raise DialogueRelocationError(
            "block expansion is forbidden until external/interior references are complete"
        )

    old_cursor = 0
    new_cursor = 0
    layouts: list[RecordLayout] = []
    for index, segment in enumerate(segments):
        new_length = replacement_lengths.get(index, len(segment))
        layouts.append(RecordLayout(index, old_cursor, len(segment), new_cursor, new_length))
        separator = 1 if index < len(segments) - 1 else 0
        old_cursor += len(segment) + separator
        new_cursor += new_length + separator

    by_index = {record.segment_index: record for record in layouts}
    relocated: list[RelocatedEntryPoint] = []
    seen_names: set[str] = set()
    for entry in entry_point_map.entry_points:
        if not entry.name or entry.name in seen_names:
            raise DialogueRelocationError("entry-point names must be unique and nonempty")
        seen_names.add(entry.name)
        try:
            record = by_index[entry.segment_index]
        except KeyError as error:
            raise DialogueRelocationError(
                f"entry point {entry.name!r} references an unknown segment"
            ) from error
        old_intra = entry.old_intra_record_offset
        if old_intra < 0 or old_intra > record.old_length:
            raise DialogueRelocationError(
                f"entry point {entry.name!r} is outside its original record"
            )
        new_intra = entry.new_intra_record_offset if entry.new_intra_record_offset is not None else old_intra
        if record.old_length != record.new_length and old_intra != 0 and entry.new_intra_record_offset is None:
            raise DialogueRelocationError(
                f"entry point {entry.name!r} lies inside a resized record and needs an explicit new intra-record offset"
            )
        if new_intra < 0 or new_intra > record.new_length:
            raise DialogueRelocationError(
                f"entry point {entry.name!r} is outside its replacement record"
            )
        relocated.append(
            RelocatedEntryPoint(
                entry.name,
                entry.segment_index,
                record.old_offset + old_intra,
                record.new_offset + new_intra,
            )
        )

    return BlockRelocationPlan(
        entry_point_map.block_index,
        len(block),
        new_cursor,
        tuple(layouts),
        tuple(relocated),
    )


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_relocation_map(path: str | Path) -> dict[str, object]:
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value, dict) or value.get("format") != "dk4-cs-relocation-map-v1":
        raise DialogueRelocationError(f"{path}: unsupported relocation map")
    if value.get("external_references_complete") is not True:
        raise DialogueRelocationError(
            f"{path}: expansion is forbidden while external references are incomplete"
        )
    if value.get("preserve_record_parity") is not True:
        raise DialogueRelocationError(
            f"{path}: CS relocation requires source record parity preservation"
        )
    return value


def rebuild_mapped_cs_dialogue(
    source_file: bytes,
    rows: list[dict[str, object]],
    profile: DialogueProfile,
    relocation_map: dict[str, object],
) -> CsBlockRelocationResult:
    """Expand explicitly mapped CS dialogue while preserving all other script bytes."""

    expected_file_hash = str(relocation_map.get("source_file_sha256", "")).lower()
    if _sha256(source_file) != expected_file_hash:
        raise DialogueRelocationError("relocation source file SHA-256 mismatch")
    block_index = int(relocation_map.get("block_index", -1))
    container = IlnkContainer.parse(source_file)
    try:
        old_block = container.blocks[block_index]
    except IndexError as error:
        raise DialogueRelocationError("relocation block is outside the ILNK file") from error
    if _sha256(old_block) != str(relocation_map.get("source_block_sha256", "")).lower():
        raise DialogueRelocationError("relocation source block SHA-256 mismatch")
    if old_block[:4] != b"CS\0\x01":
        raise DialogueRelocationError("mapped block is not a CS v1 script")

    declared_size = struct.unpack_from("<H", old_block, 4)[0]
    logical_end = 8 + declared_size
    if logical_end > len(old_block) or any(old_block[logical_end:]):
        raise DialogueRelocationError("CS logical length or alignment padding is invalid")
    if declared_size != int(relocation_map.get("source_cs_body_size", -1)):
        raise DialogueRelocationError("CS body length disagrees with relocation map")

    logical = old_block[:logical_end]
    segments = logical.split(b"\0")
    original_segments = list(segments)
    allowed = {int(value) for value in relocation_map.get("movable_segments", [])}
    replacements: dict[int, bytes] = {}
    parity_padded: set[int] = set()
    seen: set[int] = set()
    for row in rows:
        parts = str(row.get("pointer_group", "")).split(":")
        if len(parts) != 3 or parts[0] != "ILNK":
            raise DialogueRelocationError(f"{row.get('id')}: invalid ILNK pointer group")
        row_block, segment_index = int(parts[1]), int(parts[2])
        if row_block != block_index or segment_index not in allowed:
            raise DialogueRelocationError(
                f"{row.get('id')}: segment is not authorized by the relocation map"
            )
        if segment_index in seen:
            raise DialogueRelocationError(f"{row.get('id')}: duplicate relocated segment")
        seen.add(segment_index)
        expected = bytes.fromhex(str(row.get("source_hex", "")))
        if segments[segment_index] != expected:
            raise DialogueRelocationError(f"{row.get('id')}: source segment does not match")
        replacements[segment_index] = encode_relocatable_dialogue(
            expected, str(row.get("english", "")), profile
        ).encoded
        if len(replacements[segment_index]) % 2 != len(expected) % 2:
            if relocation_map.get("parity_mismatch_policy") != "append-single-space":
                raise DialogueRelocationError(
                    f"{row.get('id')}: relocated CS record changed byte parity"
                )
            replacements[segment_index] += b" "
            parity_padded.add(segment_index)

    required = {int(value) for value in relocation_map.get("required_segments", [])}
    if seen != required:
        raise DialogueRelocationError(
            f"relocation batch must contain exactly mapped proof segments {sorted(required)}"
        )
    for segment_index, replacement in replacements.items():
        segments[segment_index] = replacement

    new_logical = bytearray(b"\0".join(segments))
    if len(new_logical) - 8 > 0xFFFF:
        raise DialogueRelocationError("relocated CS body exceeds its 16-bit length field")
    struct.pack_into("<H", new_logical, 4, len(new_logical) - 8)
    new_block = bytes(new_logical) + b"\0" * (-len(new_logical) % 4)

    new_segments = bytes(new_logical).split(b"\0")
    if len(new_segments) != len(original_segments):
        raise DialogueRelocationError("relocation changed the CS segment count")
    changed = {
        index
        for index, (old, new) in enumerate(
            zip(original_segments, new_segments, strict=True)
        )
        if old != new
    }
    # Segment 1 contains the CS length field. No other unrequested script segment
    # may change.
    unexpected = changed - seen - {1}
    if unexpected:
        raise DialogueRelocationError(
            f"relocation changed unrequested CS segments: {sorted(unexpected)}"
        )
    container.blocks[block_index] = new_block
    rebuilt_file = container.to_bytes()
    reparsed = IlnkContainer.parse(rebuilt_file)
    if any(
        before != after
        for index, (before, after) in enumerate(
            zip(container.blocks, reparsed.blocks, strict=True)
        )
        if index != block_index
    ):
        raise DialogueRelocationError("relocation changed another ILNK block")
    return CsBlockRelocationResult(
        rebuilt_file,
        old_block,
        new_block,
        tuple(sorted(changed - {1})),
        tuple(sorted(parity_padded)),
        len(new_block) - len(old_block),
    )
