"""Extend exact contracts in the existing private128-byte table;gate unchanged."""

import struct

from dk4tool.patch import tavern_schemes_runtime as previous

SOURCE = 'f54d9d10c96edbebffbbab4d184550b2df1157827fe41ac9ffb1a60565c7f523'
CONTRACTS = previous.prior.CONTRACTS
GATE = previous.prior.GATE
CAPACITY = 128


def contract_rows():
    rows = []
    for parent, offset, high, ranges in previous.contract_rows():
        values = list(ranges)
        if parent == 0x02054014:
            values.append((972, 972))
        elif parent == 0x02053DB8:
            values.extend((n, n) for n in (0x81E0, 0x8220, 0x8240))
        elif parent == 0x02053D24:
            values.append((0x8200, 0x8200))
        values.sort()
        assert all(a[1] < b[0] for a, b in zip(values, values[1:]))
        rows.append((parent, offset, high, tuple(values)))
    assert len(rows) == 7
    return rows


def table():
    result = bytearray()
    for parent, offset, high, ranges in contract_rows():
        field = (offset + 24 - 0x180) // 4
        assert 0 <= field < 128 and high in (0, 0x0211)
        keys = []
        for lo, hi in ranges:
            if high:
                assert lo == hi and not lo & 15
                keys.append(lo >> 4)
            else:
                while lo <= hi:
                    end = min(lo + 15, hi)
                    assert 0 <= lo <= end < 4096
                    keys.append(lo | ((end - lo) << 12))
                    lo = end + 1
        result.extend(struct.pack('<HBB', parent & 65535, field | (128 if high else 0), len(keys)))
        result.extend(struct.pack('<' + 'H' * len(keys), *keys))
    assert len(result) == 110 <= CAPACITY
    return bytes(result)


def code():
    return {CONTRACTS: table()}
