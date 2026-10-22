"""Add the reviewed direct31-message range in the existing private table."""

import struct

from dk4tool.patch import scheme_followup_runtime as previous
from dk4tool.patch import recruitment_editorial_runtime as base

SOURCE = 'd7f302ed2b142f675006ecf3b94ff14b2921dc6d43706cf4e867dfec882baa49'
CONTRACTS, GATE, CAPACITY = base.CONTRACTS, base.GATE, 128


def contract_rows():
    rows = []
    for parent, offset, high, ranges in previous.contract_rows():
        values = list(ranges)
        if parent == 0x02054014:
            values.append((989, 1019))
        values.sort()
        assert all(a[1] < b[0] for a, b in zip(values, values[1:]))
        rows.append((parent, offset, high, tuple(values)))
    return rows


def table():
    result = bytearray()
    for parent, offset, high, ranges in contract_rows():
        field = (offset+24-0x180)//4
        assert 0 <= field < 128 and high in (0, 0x0211)
        keys = []
        for lo, hi in ranges:
            if high:
                assert lo == hi and not lo & 15
                keys.append(lo >> 4)
            else:
                while lo <= hi:
                    end = min(lo+15, hi)
                    assert 0 <= lo <= end < 4096
                    keys.append(lo | ((end-lo) << 12))
                    lo = end+1
        result.extend(struct.pack('<HBB', parent & 65535, field | (128 if high else 0), len(keys)))
        result.extend(struct.pack('<'+'H'*len(keys), *keys))
    assert len(result) == 114 <= CAPACITY
    return bytes(result)


def code():
    return {CONTRACTS: table()}
