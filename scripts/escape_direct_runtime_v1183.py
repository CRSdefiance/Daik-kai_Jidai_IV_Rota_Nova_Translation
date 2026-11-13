"""Correct the source-proven direct portrait escape contract; existing allocations only."""
import struct
from keystone import Ks, KS_ARCH_ARM, KS_MODE_THUMB
from ndspy.code import MainCodeFile
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from scripts import duel_escape_runtime_v1152 as previous
from scripts.refit_dialogue_runtime_v833 import gate as old_gate

BASE = 0x02000000
SOURCE = 'e2a4226d7b6c1264539a56269d72ecd8f88f6ecf68a9b5ef3494f991163ad1e7'
CONTRACTS, END, GATE = previous.CONTRACTS, previous.END, previous.GATE
TABLE_BYTES = 188
PACKED_PHRASES, STATUS_LITERAL = previous.PACKED_PHRASES, previous.STATUS_LITERAL
DIRECT_PARENT, KEYS = 0x02053F40, (0x7500, 0x7620)


def contract_rows():
    rows = []
    for parent, offset, high, values in previous.contract_rows():
        values = set(values)
        if parent == 0x02053DB8:
            assert set(KEYS) <= values
            values.difference_update(KEYS)
        rows.append((parent, offset, high, tuple(sorted(values))))
    rows.append((DIRECT_PARENT, 0x274, 0x0211, KEYS))
    return rows


def table():
    # Restore the seven historical rows to their original184 bytes. The new
    # direct consumer has a header with count0, selecting its two separately
    # stored keys in the same previously owned172-byte gate allocation.
    data = previous.previous.table()
    assert len(data) == 184
    field = (0x274 + 24 - 0x180)//4 | 128
    result = data + struct.pack('<HBB', DIRECT_PARENT & 65535, field, 0)
    assert len(result) == TABLE_BYTES
    return result


def gate():
    _, assembly = old_gate()
    assert assembly.count('movs r5,#7') == 1
    assembly = assembly.replace('movs r5,#7', 'movs r5,#8')
    old = '''ldrb r7,[r4,#2]
lsrs r7,r7,#1
bcs aligned32
lsls r7,r3,#28
bne fallback
lsrs r3,r3,#4
b pointer_bias
aligned32:
lsls r7,r3,#27
bne fallback
lsrs r3,r3,#5'''
    new = '''ldrb r7,[r4,#2]
lsls r7,r7,#31
lsrs r7,r7,#31
adds r7,#4
rors r3,r7
lsrs r5,r3,#16
bne fallback'''
    assert assembly.count(old) == 1
    assembly = assembly.replace(old, new)
    old = 'ldrb r5,[r4,#3]\nadds r4,#4\nranges:'
    new = '''ldrb r5,[r4,#3]
adds r4,#4
cmp r5,#0
bne ranges
adr r4,external_ranges
movs r5,#2
ranges:'''
    assert assembly.count(old) == 1
    assembly = assembly.replace(old, new)
    assembly += '\nexternal_ranges: .hword 40,49\n'
    code = bytes(Ks(KS_ARCH_ARM, KS_MODE_THUMB).asm(assembly, GATE)[0])
    assert len(code) <= 172, len(code)
    return code, assembly


def apply(arm):
    assert sha(arm) == SOURCE
    assert arm[CONTRACTS-BASE:CONTRACTS-BASE+TABLE_BYTES] == previous.table()
    assert arm[GATE-BASE:GATE-BASE+164] == old_gate()[0]
    assert arm[GATE-BASE+164:GATE-BASE+172].hex() == '68de160282bd0000'
    code, assembly = gate()
    target = bytearray(arm)
    patches = {CONTRACTS: table(), GATE: code}
    changes = []
    for at, value in patches.items():
        before = arm[at-BASE:at-BASE+len(value)]
        target[at-BASE:at-BASE+len(value)] = value
        changes.append({'address': at, 'source_hex': before.hex(), 'target_hex': value.hex()})
    result = bytes(target)
    a, b = (MainCodeFile(v, BASE) for v in (arm, result))
    shape = lambda c: [(s.ramAddress, len(s.data), s.bssSize) for s in c.sections]
    assert shape(a) == shape(b) and cache_plan(arm) == cache_plan(result)
    assert all(a.sections[i].data == b.sections[i].data for i in (1,2,3,4))
    assert len(b.sections[3].data)-48 == 123040
    assert result[PACKED_PHRASES-BASE:END-BASE] == arm[PACKED_PHRASES-BASE:END-BASE]
    restored = bytearray(result)
    for row in changes:
        value = bytes.fromhex(row['source_hex']); at = row['address']-BASE
        restored[at:at+len(value)] = value
    assert bytes(restored) == arm
    return result, {'source_ARM9_sha256': sha(arm), 'target_ARM9_sha256': sha(result),
        'patches': changes, 'gate_bytes': len(code), 'gate_owned_capacity':172,
        'public_bank_bytes':212, 'contract_table_bytes':188,
        'removed_wrong_queued_memberships': [0x02053DB8,0x27C,0x0211,list(KEYS)],
        'correct_original_direct_contract':[DIRECT_PARENT,0x274,0x0211,list(KEYS)],
        'source_binding_proof':'work/analysis/escape_direct_frame_v1182/original_direct_frame_contract.json',
        'gate_assembly':assembly, 'packed_status24_and_literal_exact':True,
        'sections_BSS_cache_ITCM_and_staged123040_exact':True,
        'private_spans':[[CONTRACTS,CONTRACTS+TABLE_BYTES],[GATE,GATE+172]],
        'all_other_ARM9_bytes_restore_exact':True,
        'research_only_not_yet_gameplay_verified':True}
