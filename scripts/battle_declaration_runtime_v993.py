"""Research-only named-declaration membership inside the existing212-byte public bank."""
import struct
from keystone import Ks, KS_ARCH_ARM, KS_MODE_ARM, KS_MODE_THUMB
from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from scripts import refit_dialogue_runtime_v833 as previous

BASE = 0x02000000
SOURCE = '2ec349ded94dd9ad3394aea9211c0006dac78a30bc7dd7880ad648c1bf73338c'
CONTRACTS = previous.CONTRACTS
TABLE_BYTES = 178
PACKED_PHRASES = CONTRACTS+TABLE_BYTES
FILTER = PACKED_PHRASES+24
END = previous.previous.END
MODAL = previous.modal.ADDRESS
STATUS_LITERAL = previous.previous.STATUS+76


def contract_rows():
    result = []
    for parent, offset, high, old in previous.contract_rows():
        values = set(old)
        if parent == 0x02053D24:
            assert high == 0x0211 and offset == 0x27C
            values.add(0x7420)
        result.append((parent, offset, high, tuple(sorted(values))))
    return result


def table():
    data = bytearray()
    for parent, offset, high, values in contract_rows():
        shift = (4 if parent == 0x02053C14 else 5) if high else 0
        bias = 896 if high else 384
        assert all(not n & ((1 << shift)-1) for n in values)
        keys = sorted((n >> shift)-bias for n in values)
        assert min(keys) >= 0 and max(keys) < 1024
        ranges = []
        for key in keys:
            if ranges and key == ranges[-1][1]+1:
                ranges[-1] = ranges[-1][0], key
            else:
                ranges.append((key, key))
        words = []
        for lo, hi in ranges:
            while lo <= hi:
                end = min(lo+63, hi)
                words.append(lo | (end-lo) << 10)
                lo = end+1
        field = (offset+24-0x180)//4
        data.extend(struct.pack('<HBB', parent & 65535, field | (128 if high else 0), len(words)))
        data.extend(struct.pack('<'+'H'*len(words), *words))
    assert len(data) == TABLE_BYTES
    return bytes(data)


def modal_code():
    assembly = previous.modal_code()[2]
    old = f'subs r3,#20\nbl {previous.FILTER}\nsubs r3,#32'
    new = f'subs r3,#19\nbeq fallback\nbl {FILTER}\nsubs r3,#33'
    assert assembly.count(old) == 1
    assembly = assembly.replace(old, new)
    # Domain1..7 encodes original289..295,excluding292,using bits0..6 of0x77.
    # The caller rejects zero BEFORE the variable shift:Thumb LSR byzero keeps
    # incoming carry and must never accidentally admit original288.
    helper = '''movs r4,#119
lsrs r4,r3
bcc done
movs r3,#58
done:
bx lr
'''
    ka, kt = Ks(KS_ARCH_ARM, KS_MODE_ARM), Ks(KS_ARCH_ARM, KS_MODE_THUMB)
    stub = bytes(ka.asm(f'ldr ip,[pc];bx ip;.word {MODAL+13}', MODAL)[0])
    body = bytes(kt.asm(assembly, MODAL+12)[0])
    filt = bytes(kt.asm(helper, FILTER)[0])
    assert len(stub+body) == 128 and len(filt) == 10 and FILTER+10 == END
    return stub+body, filt, assembly, helper


def apply(arm):
    assert sha(arm) == SOURCE
    assert arm[CONTRACTS-BASE:CONTRACTS-BASE+previous.TABLE_BYTES] == previous.table()
    assert arm[previous.previous.bank.GATE-BASE:previous.previous.bank.GATE-BASE+164] == previous.gate()[0]
    assert struct.unpack_from('<I', arm, STATUS_LITERAL-BASE)[0] == previous.PACKED_PHRASES
    words = arm[previous.PACKED_PHRASES-BASE:previous.PACKED_PHRASES-BASE+24]
    assert arm[previous.FILTER-BASE:END-BASE] == previous.modal_code()[1]
    wrap, filt, assembly, helper = modal_code()
    public = table()+words+filt
    assert len(public) == END-CONTRACTS == 212
    old = MainCodeFile(arm, BASE)
    itcm = old.sections[4]
    offset = MODAL-itcm.ramAddress
    assert bytes(itcm.data[offset:offset+128]) == previous.modal_code()[0]
    target = bytearray(arm)
    changes = []
    for at, data in ((CONTRACTS, public), (STATUS_LITERAL, struct.pack('<I', PACKED_PHRASES))):
        before = arm[at-BASE:at-BASE+len(data)]
        target[at-BASE:at-BASE+len(data)] = data
        changes.append({'address': at, 'source_hex': before.hex(), 'target_hex': data.hex()})
    new = MainCodeFile(bytes(target), BASE)
    new.sections[4].data[offset:offset+128] = wrap
    result = bytes(new.save())
    final = MainCodeFile(result, BASE)
    shape = lambda c: [(s.ramAddress, len(s.data), s.bssSize) for s in c.sections]
    assert shape(old) == shape(final) and cache_plan(arm) == cache_plan(result)
    assert all(old.sections[n].data == final.sections[n].data for n in (1, 2, 3))
    assert len(final.sections[3].data)-48 == 123040
    restored = MainCodeFile(result, BASE)
    restored.sections[4].data[offset:offset+128] = previous.modal_code()[0]
    restored_raw = bytearray(restored.save())
    for row in changes:
        at = row['address']-BASE
        restored_raw[at:at+len(bytes.fromhex(row['source_hex']))] = bytes.fromhex(row['source_hex'])
    assert bytes(restored_raw) == arm
    return result, {'source_ARM9_sha256': sha(arm), 'research_ARM9_sha256': sha(result),
                    'public_changes': changes, 'ITCM_modal_address': MODAL,
                    'ITCM_modal_source_hex': previous.modal_code()[0].hex(), 'ITCM_modal_target_hex': wrap.hex(),
                    'contract_table_bytes_before_after': [176, 178], 'filter_bytes_before_after': [12, 10],
                    'entire_public_bank_bytes_before_after': [212, 212],
                    'native_gate164_bytes_exact': True, 'packed_status24_bytes_exact_moved2': True,
                    'only_new_membership': {'parent02053D24': [0x02117420]},
                    'all_other_memberships_unchanged': True,
                    'private_spans': [[CONTRACTS, END], [MODAL, MODAL+128], [STATUS_LITERAL, STATUS_LITERAL+4]],
                    'all_sections_BSS_cache_and_entire123040_staged_payload_unchanged': True,
                    'all_other_ARM9_bytes_restore_exactly': True,
                    'zero_shift_domain_rejected_before_carry_bitset_filter': True,
                    'modal_assembly': assembly, 'filter_assembly': helper,
                    'research_only_not_registered_or_gameplay_verified': True}
