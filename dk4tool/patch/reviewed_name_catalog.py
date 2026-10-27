"""Complete route-scoped message catalog using full lossless suffix storage."""

import struct

from dk4tool.patch.confirmed_name_message_catalog import CALLS, MACRO
from dk4tool.patch.main_pool_cache_visibility import BASE
from dk4tool.patch.sailing_no_target import Assembly
from dk4tool.patch.two_screen_layout import tail

ROUTE = 0x022796B0


def helper(entry, table, count):
    if not 0 < count <= 4096:
        raise ValueError('Bounded reviewed catalog required')
    a = Assembly()
    a.emit(0xE92D51FD)
    for index, field in enumerate(CALLS):
        a.load(12, f'caller{index}', BASE + field + 4)
        a.emit(0xE15E000C)
        a.branch('scoped', 0)
    a.branch('finish')
    a.mark('scoped')
    a.emit(0xE1A03001)
    a.load(4, 'table', table)
    a.load(5, 'count', count)
    a.mark('next')
    a.emit(0xE3550000)
    a.branch('finish', 0)
    a.load(6, 'route', ROUTE)
    a.emit(0xE5966000)
    a.emit(0xE3560003)
    a.branch('finish', 8)
    a.emit(0xE3A07001)
    a.emit(0xE1A07617)  # mov r7,r7,lsl r6
    a.emit(0xE594600C)
    a.emit(0xE1160007)
    a.branch('miss', 0)
    a.emit(0xE5946000)
    a.emit(0xE5947008)
    a.emit(0xE3A08000)
    a.mark('compare')
    a.emit(0xE7D6C008)
    a.emit(0xE7D32008)
    a.emit(0xE15C0002)
    a.branch('miss', 1)
    a.emit(0xE2888001)
    a.emit(0xE1580007)
    a.branch('compare', 3)
    a.emit(0xE5941004)
    a.branch('finish')
    a.mark('miss')
    a.emit(0xE2844010)
    a.emit(0xE2555001)
    a.branch('next')
    a.mark('finish')
    a.emit(0xE8BD51FD)
    a.emit(tail(entry + len(a.words) * 4, MACRO))
    return a.finish()


def pack_complete_strings(strings, pool_start, inherited):
    """Reuse complete NUL-terminated suffixes, never shortened translations."""
    payload = bytearray(inherited)
    stored, pointers = [], {}
    for raw in sorted(set(strings), key=lambda value: (-len(value), value)):
        if not raw or b'\0' in raw or len(raw) >= 512:
            raise ValueError('Complete bounded NUL string required')
        parent = next(((value, pointer) for value, pointer in stored if value.endswith(raw)), None)
        if parent:
            value, pointer = parent
            pointers[raw] = pointer + len(value) - len(raw)
        else:
            payload.extend(bytes(-len(payload) % 4))
            pointer = pool_start + len(payload)
            payload.extend(raw + b'\0')
            stored.append((raw, pointer))
            pointers[raw] = pointer
    for raw, pointer in pointers.items():
        at = pointer - pool_start
        if payload[at:at + len(raw) + 1] != raw + b'\0':
            raise ValueError('Suffix loses first/final characters or NUL')
    return payload, pointers


def table_bytes(rows, pointers):
    return b''.join(struct.pack('<4I', pointers[row['key']], pointers[row['target']],
                               len(row['key']) + 1, row['route_mask']) for row in rows)
