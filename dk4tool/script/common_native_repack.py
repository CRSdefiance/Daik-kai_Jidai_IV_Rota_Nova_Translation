"""Reallocate mapped COMMON records within their original native cache blocks."""
from __future__ import annotations

import struct
from collections import defaultdict
from dataclasses import dataclass

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.script.common_message_table import CommonMessageEntry, common_message_entries


@dataclass(frozen=True)
class NativeCommonRepack:
    common: bytes
    arm9: bytes
    changed_records: set[tuple[int, int]]
    changed_offsets: set[int]
    entries: list[CommonMessageEntry]


def repack_native_records(common: bytes, arm9: bytes, authored: dict[int, bytes],
                          prefixes: dict[tuple[int, int], bytes], *,
                          preserved_packed_neighbors: dict[int, bytes] | None = None,
                          spare_padding_before_first_entry: bool = False) -> NativeCommonRepack:
    """Fund full translations with terminal padding; preserve all global IDs.

    Every entry in an authored packed record must be supplied. Only terminal
    spaces in other mapped records can fund expansion. NUL counts and block
    sizes remain exact; all affected uint16 native offsets are recalculated.
    An explicitly reviewed consumer may keep spare bytes before an owner's first
    mapped entry, advancing every entry offset so the bytes are never selected.
    """
    original = IlnkContainer.parse(common)
    before = common_message_entries(common, arm9, clean=False)
    by_id = {entry.message_id: entry for entry in before}
    preserved = preserved_packed_neighbors or {}
    if not authored or not authored.keys() <= by_id.keys():
        raise ValueError("Authored messages must name verified native IDs")
    if (authored.keys() & preserved.keys() or not preserved.keys() <= by_id.keys()
            or any(raw != by_id[mid].text for mid, raw in preserved.items())):
        raise ValueError("Preserved packed neighbors must match exact current selections")
    owners = defaultdict(list)
    for entry in before:
        owners[entry.block, entry.record_index].append(entry)
    targets = {(by_id[message_id].block, by_id[message_id].record_index) for message_id in authored}
    if any((by_id[mid].block, by_id[mid].record_index) not in targets for mid in preserved):
        raise ValueError("Preserved packed neighbors must belong to an authored owner")
    for owner in targets:
        if {entry.message_id for entry in owners[owner]} - authored.keys() - preserved.keys():
            raise ValueError("An authored packed record requires every native entry")
        if owner not in prefixes or any(byte != 32 for byte in prefixes[owner]):
            raise ValueError("Authored record requires a verified alignment prefix")
    for raw in authored.values():
        if not raw or b"\0" in raw or b"\n" in raw or b"\r" in raw:
            raise ValueError("Authored native entries require one nonempty paragraph")
        raw.decode("cp932")
    rebuilt_blocks = list(original.blocks)
    local_starts = {entry.message_id: entry.start for entry in before}
    patched_arm9 = bytearray(arm9)
    changed_records, changed_offsets = set(), set()
    for block_index in sorted({block for block, _ in targets}):
        old_rows = original.blocks[block_index].split(b"\0")
        rows = list(old_rows)
        for owner in sorted(targets):
            block, record = owner
            if block != block_index:
                continue
            packed = bytearray(prefixes[owner])
            for entry in owners[owner]:
                local_starts[entry.message_id] = len(packed)
                packed.extend(authored[entry.message_id] if entry.message_id in authored
                              else preserved[entry.message_id])
            rows[record] = bytes(packed)
        needed = sum(len(row) for row in rows) - sum(len(row) for row in old_rows)
        if needed < 0:
            record = max(record for block, record in targets if block == block_index)
            if spare_padding_before_first_entry:
                rows[record] = b" " * -needed + rows[record]
                for entry in owners[block_index, record]:
                    local_starts[entry.message_id] += -needed
            else:
                rows[record] += b" " * -needed
            needed = 0
        donors = []
        for record, raw in enumerate(rows):
            owner = (block_index, record)
            if owner in targets or len(owners[owner]) != 1:
                continue
            if not owners[owner][0].text.strip(b" \n\r"):
                continue
            padding = len(raw) - len(raw.rstrip(b" "))
            # A trailing LF still needs its protective following bytes. They
            # are controls, not spare allocation, even at the end of a record.
            guard = 2 if raw.rstrip(b" ").endswith(b"\n") else 0
            available = min(max(0, padding - guard), len(raw) - owners[owner][-1].start - 1)
            if available > 0:
                donors.append((available, record))
        for available, record in sorted(donors, reverse=True):
            remove = min(needed, available)
            if remove:
                rows[record] = rows[record][:-remove]
                needed -= remove
            if not needed:
                break
        if needed:
            raise ValueError(f"B{block_index}: lacks {needed} terminal padding bytes for faithful prose")
        rebuilt = b"\0".join(rows)
        if len(rebuilt) != len(original.blocks[block_index]):
            raise ValueError("Native cache block allocation changed")
        rebuilt_blocks[block_index] = rebuilt
        position = 0
        for record, raw in enumerate(rows):
            if raw != old_rows[record]:
                changed_records.add((block_index, record))
            for entry in owners[block_index, record]:
                target = position + local_starts[entry.message_id]
                if target != entry.block_offset:
                    struct.pack_into("<H", patched_arm9, entry.table_offset, target)
                    changed_offsets.add(entry.table_offset)
            position += len(raw) + 1
    rebuilt_common = IlnkContainer(rebuilt_blocks).to_bytes()
    after = common_message_entries(rebuilt_common, bytes(patched_arm9), clean=False)
    for old, new in zip(before, after, strict=True):
        if new.message_id in preserved and new.text != preserved[new.message_id]:
            raise ValueError("Preserved packed neighbor changed")
        expected = authored.get(new.message_id, old.text)
        if new.text.rstrip(b" ") != expected.rstrip(b" "):
            raise ValueError(f"Message {new.message_id}: repack changes or truncates native selection")
        if (old.message_id, old.block, old.record_index) != (new.message_id, new.block, new.record_index):
            raise ValueError("Native message/NUL-record identity changed")
    return NativeCommonRepack(rebuilt_common, bytes(patched_arm9), changed_records, changed_offsets, after)
