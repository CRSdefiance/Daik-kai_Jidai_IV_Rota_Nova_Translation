"""Source-locked native entry mapping for COMMON item descriptions."""
from __future__ import annotations

import struct
from dataclasses import dataclass
from hashlib import sha256

from dk4tool.formats.ilnk import IlnkContainer

B32_TABLE_OFFSET = 0x142FE0
B32_ENTRY_COUNT = 46
B32_TABLE_SHA256 = "9c8ee0fa0269b4d7e3f52ecd45675332c423c96097b629db5904a77acac2df6a"
CLEAN_COMMON_SHA256 = "4ba2b09e6c4032d6466ab1ec77f6ce2eea2edf58ae50a6b2f0dcb91037e269bc"
ITEM_TABLES = {
    29: (0x142F0E, 10, 0, "eb7344fab50ee4e678a6a221f085f21d7d2b8c6414a2251a325a26262166b202", 8),
    30: (0x142F22, 49, 10, "422f4a2ab07bd9fe70b666a05fa2a1463e2dbb9e0f99dba8950d86b5b5951db9", 22),
    31: (0x142F84, 46, 59, "a5cd04acfd105543e84d21b6a21b7999e2e26ef85467135231de1b0ae796b217", 23),
    32: (B32_TABLE_OFFSET, B32_ENTRY_COUNT, 105, B32_TABLE_SHA256, 23),
}


@dataclass(frozen=True)
class CommonItemEntry:
    item_index: int
    table_offset: int
    block_offset: int
    record_index: int
    start: int
    end: int
    source: bytes


def b32_item_entries(clean_common: bytes, clean_arm9: bytes) -> list[CommonItemEntry]:
    return native_item_entries(clean_common, clean_arm9, 32)


def native_item_entries(clean_common: bytes, clean_arm9: bytes, block_index: int) -> list[CommonItemEntry]:
    """Resolve every table offset against the clean NUL record allocations.

    Source offsets are authoritative: leading alignment bytes outside the
    native entry are not interchangeable with text guards or visible glyphs.
    """
    table_offset, count, first_item, table_hash, record_count = ITEM_TABLES[block_index]
    table = clean_arm9[table_offset:table_offset + count * 2]
    if sha256(clean_common).hexdigest() != CLEAN_COMMON_SHA256 or sha256(table).hexdigest() != table_hash:
        raise ValueError(f"B{block_index} mapping requires the exact clean COMMON and native table")
    block = IlnkContainer.parse(clean_common).blocks[block_index]
    starts = list(struct.unpack_from(f"<{count}H", clean_arm9, table_offset))
    expected_first = 3136 if block_index == 29 else 0
    if starts[0] != expected_first or starts != sorted(set(starts)) or starts[-1] >= len(block):
        raise ValueError(f"B{block_index} native entry table is not strictly ordered/in bounds")
    records = []
    position = 0
    for index, raw in enumerate(block.split(b"\0")):
        if raw:
            records.append((index, position, position + len(raw)))
        position += len(raw) + 1
    entries = []
    for i, start in enumerate(starts):
        owners = [(index, lo, hi) for index, lo, hi in records if lo <= start < hi]
        if len(owners) != 1:
            raise ValueError(f"native entry {i} lands outside a source record")
        index, lo, hi = owners[0]
        end = min(starts[i + 1] if i + 1 < len(starts) else len(block), hi)
        source = block[start:end]
        source.decode("cp932")
        if start % 2 or not source or b"\0" in source:
            raise ValueError(f"native entry {i} has invalid source alignment/span")
        entries.append(CommonItemEntry(first_item + i, table_offset + i * 2, start, index, start - lo, end - lo, source))
    expected_records = set(range(53, 61)) if block_index == 29 else set(range(record_count))
    if {entry.record_index for entry in entries} != expected_records:
        raise ValueError(f"B{block_index} entry table does not account for every source record")
    return entries
