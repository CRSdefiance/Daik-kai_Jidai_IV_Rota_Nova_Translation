"""Exact shared-dialogue contracts within the existing table and gate banks."""

import struct

from keystone import KS_ARCH_ARM, KS_MODE_THUMB, Ks

from dk4tool.patch import barmaid_editorial_runtime as previous
from dk4tool.patch import tavern_schemes_runtime as previous_gate

SOURCE = 'd2d2670bfbbb8ce1c3433b0c1a6220f385ef8beba5678bea9e9d4bb612b57abb'
CONTRACTS, GATE = previous.CONTRACTS, previous.GATE
TABLE_CAPACITY, GATE_CAPACITY = 128, 144


def contract_rows():
    rows = []
    for parent, offset, high, ranges in previous.contract_rows():
        values = list(ranges)
        if parent == 0x02054014:
            values.extend(((1028, 1034), (1049, 1069)))
        elif parent == 0x02053D24:
            values.extend((n, n) for n in (0x8180, 0x81A0, 0x81C0))
        elif parent == 0x02053E38:
            values.append((1020, 1020))
        values.sort()
        assert all(a[1] < b[0] for a, b in zip(values, values[1:]))
        rows.append((parent, offset, high, tuple(values)))
    return rows


def assemble():
    table = bytearray()
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
        table.extend(struct.pack('<HBB', parent & 65535, field | (128 if high else 0), len(keys)))
        table.extend(struct.pack('<' + 'H' * len(keys), *keys))
    assert len(table) == TABLE_CAPACITY
    _, _, assembly = previous_gate.assemble()
    old = f'bls status\nblx {previous.base.LITERAL_EXIT}'
    new = f'bls status\nsubs r4,#123\ncmp r4,#1\nbls coordinate\nblx {previous.base.LITERAL_EXIT}'
    assert assembly.count(old) == 1
    assembly = assembly.replace(old, new)
    # Every row lives in the same existing 0x0214 bank. Derive 0x0211
    # from that row address instead of storing another literal in the gate.
    assert CONTRACTS >> 16 == (CONTRACTS + TABLE_CAPACITY - 1) >> 16 == 0x0214
    assert assembly.count('ldr r7,field_high') == 1
    assert assembly.count('field_high: .word 0x0211') == 1
    assembly = assembly.replace('ldr r7,field_high', 'lsrs r7,r4,#16\nsubs r7,#3')
    assembly = assembly.replace('field_high: .word 0x0211', '')
    gate = bytes(Ks(KS_ARCH_ARM, KS_MODE_THUMB).asm(assembly, GATE)[0])
    assert len(gate) == GATE_CAPACITY
    return bytes(table), gate, assembly


def code():
    table, gate, _ = assemble()
    return {CONTRACTS: table, GATE: gate}
