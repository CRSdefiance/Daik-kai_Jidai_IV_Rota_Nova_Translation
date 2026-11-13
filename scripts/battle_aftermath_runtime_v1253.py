"""Research-only byte delta/run selector, confined to existing owned spans.

Each even-aligned row retains its parent/stack/high-word header. Header size is
payload bytes. Opcodes 0..126 advance to one valid key, 127 advances 127 without
selecting a key, and 128..255 select the next 1..128 contiguous keys. Padding
127 preserves halfword alignment without introducing any accepted key.
"""
import struct

from keystone import Ks, KS_ARCH_ARM, KS_MODE_THUMB
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from scripts import escape_direct_runtime_v1183b as previous
from scripts.research_aftermath_contract_codec_v1251 import rows as contract_rows

BASE = 0x02000000
SOURCE = '384b993eb89c5578acb66925ff1f6412e1a3d68073164600b896dc563779276c'
CONTRACTS, GATE = previous.CONTRACTS, previous.GATE
TABLE_BYTES, GATE_BYTES = 188, 172


def encode(rows):
    result = bytearray()
    for parent, offset, high, values in rows:
        shift = (4 if parent == 0x02053C14 else 5) if high else 0
        assert all(v & ((1 << shift)-1) == 0 for v in values)
        bias = 896 if high else 384
        keys = sorted((v >> shift)-bias for v in values)
        assert keys and 0 <= keys[0] <= keys[-1] < 65536
        payload = bytearray()
        last, i = 0, 0
        while i < len(keys):
            low, j = keys[i], i
            while j+1 < len(keys) and keys[j+1] == keys[j]+1:
                j += 1
            gap = low-last
            while gap >= 127:
                payload.append(127)
                gap -= 127
            payload.append(gap)
            last = low
            length = keys[j]-low
            while length:
                take = min(128, length)
                payload.append(127+take)
                last += take
                length -= take
            i = j+1
        if len(payload) & 1:
            payload.append(127)
        field = (offset+24-0x180)//4
        assert 0 <= field < 128 and len(payload) < 256
        assert high in (0, 0x0211)
        result.extend(struct.pack('<HBB', parent & 65535, field | (128 if high else 0), len(payload)))
        result.extend(payload)
    return bytes(result)


def decode(data, count=8):
    pos, rows = 0, []
    for _ in range(count):
        assert pos & 1 == 0
        parent, field, size = struct.unpack_from('<HBB', data, pos)
        pos += 4
        parent |= 0x02050000
        high = 0x0211 if field & 128 else 0
        offset = (field & 127)*4+0x180-24
        shift = (4 if parent == 0x02053C14 else 5) if high else 0
        bias, current, values = (896 if high else 384), 0, []
        end = pos+size
        assert end <= len(data)
        while pos < end:
            code = data[pos]
            pos += 1
            if code <= 127:
                current += code
                if code != 127:
                    values.append((current+bias) << shift)
            else:
                length = code-127
                values.extend((n+bias) << shift for n in range(current+1, current+length+1))
                current += length
        assert values == sorted(set(values))
        rows.append((parent, offset, high, tuple(values)))
    return rows, pos


def table():
    rows = contract_rows()
    result = encode(rows)
    decoded, end = decode(result)
    assert decoded == rows and end == len(result) == 184
    return result + bytes(TABLE_BYTES-len(result))


def gate():
    _, assembly = previous.gate()
    old = 'lsls r7,r7,#1\nadds r4,#4'
    assert assembly.count(old) == 1
    assembly = assembly.replace(old, 'adds r4,#4')
    start = assembly.index('ldrb r5,[r4,#3]\nadds r4,#4\ncmp r5,#0')
    end = assembly.index('fallback:\n', start)
    assembly = assembly[:start] + '''mov r6,r3
ldrb r5,[r4,#3]
adds r4,#4
ranges:
ldrb r7,[r4]
adds r4,#1
cmp r7,#127
bhi run_range
subs r3,r3,r7
bne next_range
cmp r7,#127
bne hit
b next_range
run_range:
subs r7,#127
subs r3,r3,r7
bls hit
next_range:
subs r5,#1
bne ranges
''' + assembly[end:]
    assert assembly.count('selected:\n') == 1
    assembly = assembly.replace('selected:\n', 'hit:\nmov r3,r6\nselected:\n')
    suffix = '\nexternal_ranges: .hword 40,49\n'
    assert assembly.count(suffix) == 1
    assembly = assembly.replace(suffix, '')
    code = bytes(Ks(KS_ARCH_ARM, KS_MODE_THUMB).asm(assembly, GATE)[0])
    assert len(code) == 168
    return code + b'\xc0\x46' * ((GATE_BYTES-len(code))//2), assembly


def apply(arm):
    assert sha(arm) == SOURCE
    assert arm[CONTRACTS-BASE:CONTRACTS-BASE+TABLE_BYTES] == previous.table()
    assert arm[GATE-BASE:GATE-BASE+GATE_BYTES] == previous.gate()[0]
    target = bytearray(arm)
    patches = []
    for at, value in ((CONTRACTS, table()), (GATE, gate()[0])):
        old = arm[at-BASE:at-BASE+len(value)]
        target[at-BASE:at-BASE+len(value)] = value
        patches.append({'address': at, 'source_hex': old.hex(), 'target_hex': value.hex()})
    result = bytes(target)
    a, b = (MainCodeFile(v, BASE) for v in (arm, result))
    shape = lambda c: [(s.ramAddress, len(s.data), s.bssSize) for s in c.sections]
    assert shape(a) == shape(b) and cache_plan(arm) == cache_plan(result)
    assert all(a.sections[i].data == b.sections[i].data for i in (1, 2, 3, 4))
    assert len(b.sections[3].data)-48 == 123040
    assert result[previous.PACKED_PHRASES-BASE:previous.END-BASE] == arm[previous.PACKED_PHRASES-BASE:previous.END-BASE]
    restored = bytearray(result)
    for p in patches:
        value = bytes.fromhex(p['source_hex'])
        restored[p['address']-BASE:p['address']-BASE+len(value)] = value
    assert bytes(restored) == arm
    return result, {
        'source_ARM9_sha256': sha(arm), 'target_ARM9_sha256': sha(result),
        'patches': patches, 'private_spans': [[CONTRACTS, CONTRACTS+188], [GATE, GATE+172]],
        'encoded_table_bytes': 184, 'owned_table_bytes': 188,
        'native_gate_bytes': 168, 'owned_gate_bytes': 172,
        'all_headers_even_aligned_no_unaligned_halfword_loads': True,
        'no_additional_stack_or_register_scratch': True,
        'packed_status_phrases_and_live_suffix_pointer_preserved': True,
        'sections_BSS_cache_ITCM_staged123040_exact': True,
        'all_other_ARM9_bytes_restore_exact': True,
        'gate_assembly': gate()[1], 'research_only_not_registered_or_gameplay_verified': True,
    }
