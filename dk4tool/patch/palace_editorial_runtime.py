"""Palace selectors packed in the existing 168-byte private data allocation.

No parent normalization or permissive range bridging is used. The existing
gate, its seven exact parent contracts and all code bytes remain unchanged.
"""

import struct

from dk4tool.patch import item_diplomacy_runtime as previous

bank = previous.bank
BASE = bank.BASE
LUXURY_GOODS = bank.CONTRACTS
# A C string needs its NUL: luxury goods occupies 13 bytes, then one byte
# aligns the halfword table. Its 130 bytes end on a word boundary.
CONTRACTS = LUXURY_GOODS+14
TABLE_BYTES = 130
PACKED_PHRASES = CONTRACTS+TABLE_BYTES
END = 0x02147A24


def contract_rows():
    rows = []
    for parent, offset, high, values in previous.contract_rows():
        values = set(values)
        if parent == 0x02054014:
            values.update(range(1146,1177))
        elif parent == 0x02053FCC:
            values.add(1166)
        rows.append((parent,offset,high,tuple(sorted(values))))
    return rows


def table():
    data = bytearray()
    for parent, offset, high, values in contract_rows():
        shift = (4 if parent == 0x02053C14 else 5) if high else 0
        assert all(not n & ((1<<shift)-1) for n in values)
        keys = sorted((n>>shift)-512 if high else n for n in values)
        ranges = []
        for key in keys:
            if ranges and key == ranges[-1][1]+1:
                ranges[-1] = (ranges[-1][0],key)
            else:
                ranges.append((key,key))
        encoded = []
        for lo, hi in ranges:
            while lo <= hi:
                end = min(lo+31,hi)
                assert 0 <= lo <= end < 2048
                encoded.append(lo | ((end-lo)<<11))
                lo = end+1
        field = (offset+24-0x180)//4
        data.extend(struct.pack('<HBB',parent&65535,field|(128 if high else 0),len(encoded)))
        data.extend(struct.pack('<'+'H'*len(encoded),*encoded))
    assert len(data) == 130
    return bytes(data)+bytes(TABLE_BYTES-len(data))


def patches(arm):
    assert arm[bank.CONTRACTS-BASE:bank.CONTRACTS-BASE+128] == previous.table()
    old = previous.code()[bank.PACKED_PHRASES]
    assert arm[bank.PACKED_PHRASES-BASE:bank.PACKED_PHRASES-BASE+24] == old
    words = list(struct.unpack('<12H',old))
    assert words[7]*4+bank.DATA_BASE == bank.DATA_ADDRESSES[7]
    words[7] = (LUXURY_GOODS-bank.DATA_BASE)//4
    data = b'luxury goods\0\0'+table()+struct.pack('<12H',*words)
    assert LUXURY_GOODS+len(data) == END and LUXURY_GOODS%4 == 0
    assert CONTRACTS%2 == 0 and PACKED_PHRASES%4 == 0
    status = arm[bank.STATUS-BASE:bank.STATUS-BASE+80]
    literal = struct.pack('<I',bank.PACKED_PHRASES)
    assert status.count(literal) == 1
    at = status.index(literal)
    assert at%4 == 0
    gate = arm[bank.GATE-BASE:bank.GATE-BASE+164]
    old_contracts = struct.pack('<I',bank.CONTRACTS)
    assert gate.count(old_contracts) == 1
    pointer = gate.index(old_contracts)
    assert pointer%4 == 0
    return {LUXURY_GOODS:data, bank.STATUS+at:struct.pack('<I',PACKED_PHRASES),
            bank.GATE+pointer:struct.pack('<I',CONTRACTS)}


def apply(arm):
    out = bytearray(arm)
    for at, data in patches(arm).items():
        out[at-BASE:at-BASE+len(data)] = data
    assert len(out) == len(arm)
    return bytes(out)
