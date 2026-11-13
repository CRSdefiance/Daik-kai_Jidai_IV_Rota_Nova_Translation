"""Two source Search keys in the existing188/172 banks;delta191/run64 codec."""
import inspect
from keystone import Ks, KS_ARCH_ARM, KS_MODE_THUMB
from ndspy.code import MainCodeFile
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from scripts import hot_spring_runtime_v1614 as previous
from scripts import battle_aftermath_runtime_v1253 as codec

BASE = 0x02000000
SOURCE = '48c3b6b4cc3818d97bbeaea4154368434e409acd58567c99987433b0fa0baff8'
CONTRACTS, GATE = previous.CONTRACTS, previous.GATE
TABLE_BYTES, GATE_BYTES = 188, 172
THRESHOLD = 191
NEW_KEYS = (0x6E80, 0x6EC0)


def contract_rows():
    rows = []
    for parent, offset, high, keys in previous.contract_rows():
        if parent == 0x02053DB8:
            assert (offset, high) == (0x27C, 0x0211) and not set(keys) & set(NEW_KEYS)
            keys = tuple(sorted((*keys, *NEW_KEYS)))
        rows.append((parent, offset, high, keys))
    return rows


def bind(function):
    source = inspect.getsource(function)
    assert source.count('896 if high else 384') == 1
    source = source.replace('896 if high else 384', '873 if high else 780')
    replacements = ([('gap >= 127', 'gap >= 191'), ('payload.append(127)', 'payload.append(191)'),
                     ('gap -= 127', 'gap -= 191'), ('min(128, length)', 'min(64, length)'),
                     ('payload.append(127+take)', 'payload.append(191+take)')]
                    if function is codec.encode else [('code <= 127', 'code <= 191'),
                     ('code != 127', 'code != 191'), ('length = code-127', 'length = code-191')])
    for old, new in replacements:
        assert old in source, old
        source = source.replace(old, new)
    env = dict(codec.__dict__)
    exec(compile(source, __file__, 'exec'), env)
    return env[function.__name__]


def table():
    value = bind(codec.encode)(contract_rows())
    rows, end = bind(codec.decode)(value)
    assert rows == contract_rows() and end == len(value) == 186
    return value + bytes(TABLE_BYTES - len(value))


def gate():
    old, assembly = previous.gate()
    assert assembly.count('cmp r7,#127') == 2 and assembly.count('subs r7,#127') == 1
    assembly = assembly.replace('cmp r7,#127', 'cmp r7,#191').replace('subs r7,#127', 'subs r7,#191')
    code = bytes(Ks(KS_ARCH_ARM, KS_MODE_THUMB).asm(assembly, GATE)[0])
    assert len(code) == 168
    result = code + b'\xc0\x46' * 2
    assert len(result) == GATE_BYTES and sum(a != b for a, b in zip(old, result, strict=True)) == 3
    return result, assembly


def apply(arm):
    assert sha(arm) == SOURCE
    assert arm[CONTRACTS-BASE:CONTRACTS-BASE+188] == previous.table()
    assert arm[GATE-BASE:GATE-BASE+172] == previous.gate()[0]
    special = {842-780, 905-780, 906-780, 1028-780, 1029-780}
    for parent, offset, high, keys in contract_rows():
        if high:
            shift = 4 if parent == 0x02053C14 else 5
            assert not {(key >> shift)-873 for key in keys} & special
    target, patches = bytearray(arm), []
    for at, value in [(CONTRACTS, table()), (GATE, gate()[0])]:
        old = arm[at-BASE:at-BASE+len(value)]
        target[at-BASE:at-BASE+len(value)] = value
        patches.append({'address': at, 'source_hex': old.hex(), 'target_hex': value.hex()})
    target = bytes(target)
    restored = bytearray(target)
    for p in patches:
        at = p['address']-BASE
        restored[at:at+len(bytes.fromhex(p['source_hex']))] = bytes.fromhex(p['source_hex'])
    assert bytes(restored) == arm
    old, new = [MainCodeFile(value, BASE) for value in [arm, target]]
    shape = lambda c: [(s.ramAddress, len(s.data), s.bssSize) for s in c.sections]
    assert shape(old) == shape(new) and cache_plan(arm) == cache_plan(target)
    assert all(old.sections[i].data == new.sections[i].data for i in [1, 2, 3, 4])
    assert len(new.sections[3].data)-48 == 123040
    return target, {'source_ARM9_sha256': sha(arm), 'target_ARM9_sha256': sha(target), 'patches': patches,
                    'private_spans': [[CONTRACTS, CONTRACTS+188], [GATE, GATE+172]],
                    'encoded_table_bytes': 186, 'owned_table_bytes': 188, 'native_gate_bytes': 168, 'owned_gate_bytes': 172,
                    'opcode_delta_skip_threshold': 191, 'maximum_contiguous_run': 64,
                    'numeric_encoding_bias': 780, 'pointer_encoding_bias': 873,
                    'all_prior_memberships_and_all8_parent_stack_high_word_contracts_exact': True,
                    'only_three_gate_immediate_bytes_changed': True,
                    'all_nonowned_ARM9_bytes_restore_exact': True,
                    'sections_BSS_cache_ITCM_arena_and123040_staged_bytes_exact': True,
                    'gate_assembly': gate()[1], 'research_only_no_ROM_registry_or_completion_change': True}
