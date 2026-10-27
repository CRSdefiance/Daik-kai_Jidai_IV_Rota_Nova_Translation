"""Add the two original escape-speech tables within the same212-byte bank."""
import struct
from types import FunctionType
from ndspy.code import MainCodeFile
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from scripts import sighting_runtime_v1071 as previous
from scripts import battle_declaration_runtime_v993b as table_encoder

BASE = 0x02000000
SOURCE = '60619fb17a6201de88e3462975c49469a2458c7c19db34b9ae7ab7d20e3452a8'
CONTRACTS, END = previous.CONTRACTS, previous.END
TABLE_BYTES = 188
PACKED_PHRASES = CONTRACTS+TABLE_BYTES
STATUS_LITERAL, GATE = previous.STATUS_LITERAL, previous.GATE


def contract_rows():
    rows = []
    for parent, offset, high, values in previous.contract_rows():
        values = set(values)
        if parent == 0x02053DB8:
            assert (offset, high) == (0x27C, 0x0211)
            assert not values & {0x7500, 0x7620}
            values.update((0x7500, 0x7620))
        rows.append((parent, offset, high, tuple(sorted(values))))
    return rows


def table():
    build = FunctionType(table_encoder.table.__code__,
        {**table_encoder.table.__globals__, 'TABLE_BYTES': TABLE_BYTES,
         'contract_rows': contract_rows})
    return build()


def apply(arm):
    assert sha(arm) == SOURCE
    assert arm[CONTRACTS-BASE:CONTRACTS-BASE+previous.TABLE_BYTES] == previous.table()
    assert struct.unpack_from('<I', arm, STATUS_LITERAL-BASE)[0] == previous.PACKED_PHRASES
    packed = arm[previous.PACKED_PHRASES-BASE:previous.PACKED_PHRASES-BASE+24]
    assert arm[previous.PACKED_PHRASES-BASE+24:END-BASE] == bytes(4)
    public = table()+packed
    assert len(public) == END-CONTRACTS == 212 and PACKED_PHRASES+24 == END
    target = bytearray(arm)
    changes = []
    for address, value in ((CONTRACTS, public), (STATUS_LITERAL, struct.pack('<I', PACKED_PHRASES))):
        before = arm[address-BASE:address-BASE+len(value)]
        target[address-BASE:address-BASE+len(value)] = value
        changes.append({'address': address, 'source_hex': before.hex(), 'target_hex': value.hex()})
    result = bytes(target)
    old, new = MainCodeFile(arm, BASE), MainCodeFile(result, BASE)
    shape = lambda code: [(s.ramAddress, len(s.data), s.bssSize) for s in code.sections]
    assert shape(old) == shape(new) and cache_plan(arm) == cache_plan(result)
    assert all(old.sections[i].data == new.sections[i].data for i in (1, 2, 3, 4))
    assert len(new.sections[3].data)-48 == 123040
    assert result[GATE-BASE:GATE-BASE+164] == arm[GATE-BASE:GATE-BASE+164]
    restored = bytearray(result)
    for row in changes:
        data = bytes.fromhex(row['source_hex'])
        restored[row['address']-BASE:row['address']-BASE+len(data)] = data
    assert bytes(restored) == arm
    return result, {'source_ARM9_sha256': sha(arm), 'research_ARM9_sha256': sha(result),
        'public_changes': changes, 'only_new_membership': {'parent02053DB8': [0x02117500, 0x02117620]},
        'contract_table_bytes_before_after': [184, 188], 'public_bank_bytes_before_after': [212, 212],
        'packed_status24_bytes_exact_moved4': True, 'native_gate164_and_ITCM_modal128_exact': True,
        'all_sections_BSS_cache_allocations_and_entire123040_staged_bytes_exact': True,
        'all_other_ARM9_bytes_restore_exact': True,
        'private_spans': [[CONTRACTS, END], [STATUS_LITERAL, STATUS_LITERAL+4]],
        'research_only_selector_status_fonts_integration_and_actual_pending': True}
