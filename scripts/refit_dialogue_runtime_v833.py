"""Research-only exact Refit memberships within current owned allocations."""

import struct
from pathlib import Path

from keystone import Ks, KS_ARCH_ARM, KS_MODE_ARM, KS_MODE_THUMB
from ndspy.code import MainCodeFile

from dk4tool.patch import captain_prompt_wrap as modal
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.item_diplomacy_runtime import assemble as gate_source
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.patch.recruitment_quantity_runtime import assemble as old_quantity
from dk4tool.patch.shipyard_editorial import QUANTITY, PRICE_RETURNS, DAY_RETURN
from scripts import ceremony_runtime_v808 as previous

BASE = 0x02000000
SOURCE = '278028874ab612693246fc816f5a44d420648ab0c6992009702b443baa0d9be7'
ROOT = Path('work/analysis/refit_dialogue_v833')
TABLE_BYTES = 176
CONTRACTS = previous.CONTRACTS
PACKED_PHRASES = CONTRACTS + TABLE_BYTES
FILTER = PACKED_PHRASES + 24
NEW_DAY_RETURN = 0x02017B90


def contract_rows():
    rows = []
    for parent, offset, high, old in previous.contract_rows():
        values = set(old)
        if parent == 0x02054014:
            values.update(range(1263, 1268))
        elif parent == 0x02053DB8:
            values.add(0x8680)
        rows.append((parent, offset, high, tuple(sorted(values))))
    return rows


def table():
    data = bytearray()
    for parent, offset, high, values in contract_rows():
        shift = (4 if parent == 0x02053C14 else 5) if high else 0
        # Preserve the prior normalized key for every consumer, then apply one
        # universal bias. Special coordinate/status routes use the same bias.
        bias = 896 if high else 384
        keys = sorted((n >> shift) - bias for n in values)
        assert min(keys) >= 0 and max(keys) < 1024
        ranges = []
        for key in keys:
            if ranges and key == ranges[-1][1] + 1:
                ranges[-1] = ranges[-1][0], key
            else:
                ranges.append((key, key))
        words = []
        for lo, hi in ranges:
            while lo <= hi:
                end = min(lo + 63, hi)
                words.append(lo | (end - lo) << 10)
                lo = end + 1
        field = (offset + 24 - 0x180) // 4
        data.extend(struct.pack('<HBB', parent & 65535, field | (128 if high else 0), len(words)))
        data.extend(struct.pack('<' + 'H' * len(words), *words))
    assert len(data) == TABLE_BYTES
    return bytes(data)


def gate():
    _, assembly = gate_source()
    assembly = assembly.replace(f'contracts: .word {previous.bank.CONTRACTS}', f'contracts: .word {CONTRACTS}')
    assert assembly.count('ready:\nldrb r5') == 1
    assembly = assembly.replace('ready:\nldrb r5', 'ready:\nsubs r3,#192\nsubs r3,#192\nldrb r5')
    assembly = assembly.replace('lsls r7,r6,#21\nlsrs r7,r7,#21', 'lsls r7,r6,#22\nlsrs r7,r7,#22')
    assembly = assembly.replace('lsrs r6,r6,#11', 'lsrs r6,r6,#10')
    # 842-384=458. Replacing its literal load with two Thumb instructions
    # consumes old alignment and frees exactly the literal word for the bias.
    assembly = assembly.replace('ldr r4,coord_ID', 'movs r4,#229\nlsls r4,r4,#1')
    assembly = assembly.replace('coord_ID: .word 842\n', '')
    code = bytes(Ks(KS_ARCH_ARM, KS_MODE_THUMB).asm(assembly, previous.bank.GATE)[0])
    assert len(code) == 164
    return code, assembly


def modal_code():
    _, _, assembly, helper = previous.modal_code()
    assembly = assembly.replace(f'bl {previous.MODAL_FILTER}', f'subs r3,#20\nbl {FILTER}')
    assembly = assembly.replace('movs r6,#0', 'ldr r6,ordinary_wrap').replace('movs r6,#1', 'ldr r6,balanced_wrap')
    old = 'cmp r6,#0\nbne balanced\nblx 0x01ffca00\nb wrapped\nbalanced:\nbl 0x02147ae4\nwrapped:'
    assert assembly.count(old) == 1
    assembly = assembly.replace(old, 'blx r6')
    assembly += '\nordinary_wrap: .word 0x01ffca00\nbalanced_wrap: .word 0x02147ae5\n'
    ka, kt = Ks(KS_ARCH_ARM, KS_MODE_ARM), Ks(KS_ARCH_ARM, KS_MODE_THUMB)
    stub = bytes(ka.asm(f'ldr ip,[pc];bx ip;.word {modal.ADDRESS+13}', modal.ADDRESS)[0])
    body = bytes(kt.asm(assembly, modal.ADDRESS + 12)[0])
    filt = bytes(kt.asm(helper.removeprefix('subs r3,#20\n'), FILTER)[0])
    assert len(stub + body) == 128 and len(filt) == 12 and FILTER + 12 == previous.END
    return stub + body, filt, assembly


def quantity():
    # Private to the exact eight source-locked BL return addresses. Their low
    # byte bits7..5 equal4 precisely for the two duration callers. No general
    # LR-to-unit API is introduced; closure and all earlier results must pass.
    returns = (*PRICE_RETURNS, DAY_RETURN, NEW_DAY_RETURN)
    assert [r for r in returns if (r & 255) >> 5 == 4] == [DAY_RETURN, NEW_DAY_RETURN]
    ka, kt = Ks(KS_ARCH_ARM, KS_MODE_ARM), Ks(KS_ARCH_ARM, KS_MODE_THUMB)
    start = QUANTITY + 12
    head = bytes(ka.asm(f'ldr ip,[pc];bx ip;.word {start|1}', QUANTITY)[0])
    assembly = '''push {r4-r7,lr}
mov r4,r0
mov r3,lr
lsls r3,r3,#24
lsrs r3,r3,#29
cmp r3,#4
adr r5,coins
bne kind_ready
adr r5,days
kind_ready:
blx 0x020abf50
mov r6,r0
ldrb r1,[r5]
adds r5,#1
cmp r4,#1
bne plural
subs r1,#1
plural:
subs r0,r6,r1
mov r7,r0
digits:
ldrb r2,[r6]
adds r6,#1
cmp r2,#0
beq suffix
strb r2,[r7]
adds r7,#1
b digits
suffix:
ldrb r2,[r5]
adds r5,#1
strb r2,[r7]
adds r7,#1
subs r1,#1
bne suffix
movs r2,#0
strb r2,[r7]
pop {r4-r7,pc}
.align 2
coins: .byte 11
.ascii " gold coins"
days: .byte 5
.ascii " days"
.align 2
'''
    body = bytes(kt.asm(assembly, start)[0])
    old = old_quantity()[QUANTITY]
    code = head + body
    assert len(code) <= len(old) == 104
    return code + old[len(code):], assembly


def apply(arm):
    assert sha(arm) == SOURCE
    assert arm[CONTRACTS - BASE:CONTRACTS - BASE + previous.TABLE_BYTES] == previous.table()
    old_gate = gate_source()[0][previous.bank.GATE][:164].replace(
        struct.pack('<I', previous.bank.CONTRACTS), struct.pack('<I', CONTRACTS))
    assert arm[previous.bank.GATE - BASE:previous.bank.GATE - BASE + 164] == old_gate
    assert arm[QUANTITY - BASE:QUANTITY - BASE + 104] == old_quantity()[QUANTITY]
    ka = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    old_call = bytes(ka.asm('bl 0x020abf50', NEW_DAY_RETURN - 4)[0])
    assert arm[NEW_DAY_RETURN - BASE - 4:NEW_DAY_RETURN - BASE] == old_call
    words = arm[previous.PACKED_PHRASES - BASE:previous.PACKED_PHRASES - BASE + 24]
    wrap, filt, _ = modal_code()
    old_filter = bytes(Ks(KS_ARCH_ARM, KS_MODE_THUMB).asm(previous.modal_code()[3], previous.MODAL_FILTER)[0])
    assert arm[previous.MODAL_FILTER - BASE:previous.END - BASE] == old_filter
    public = table() + words + filt
    assert len(public) == previous.END - CONTRACTS == 212
    status_literal = previous.STATUS + 76
    assert struct.unpack_from('<I', arm, status_literal - BASE)[0] == previous.PACKED_PHRASES
    patches = {CONTRACTS: public, previous.bank.GATE: gate()[0],
               status_literal: struct.pack('<I', PACKED_PHRASES), QUANTITY: quantity()[0],
               NEW_DAY_RETURN - 4: bytes(ka.asm(f'bl {QUANTITY}', NEW_DAY_RETURN - 4)[0])}
    target = bytearray(arm)
    proof = []
    for at, data in patches.items():
        before = arm[at - BASE:at - BASE + len(data)]
        target[at - BASE:at - BASE + len(data)] = data
        proof.append({'address': at, 'source_hex': before.hex(), 'target_hex': data.hex()})
    old, new = MainCodeFile(arm, BASE), MainCodeFile(bytes(target), BASE)
    section = new.sections[4]
    off = modal.ADDRESS - section.ramAddress
    assert bytes(section.data[off:off + 128]) == previous.modal_code()[0]
    section.data[off:off + 128] = wrap
    target = bytes(new.save())
    shape = lambda c: [(s.ramAddress, len(s.data), s.bssSize) for s in c.sections]
    assert shape(old) == shape(new) and cache_plan(arm) == cache_plan(target)
    assert all(old.sections[n].data == new.sections[n].data for n in (1, 2, 3))
    assert len(new.sections[3].data) - 48 == 123040
    return target, {'source_ARM9_sha256': sha(arm), 'target_ARM9_sha256': sha(target),
                    'patches': proof, 'ITCM_modal_address': modal.ADDRESS,
                    'ITCM_modal_source_hex': previous.modal_code()[0].hex(), 'ITCM_modal_target_hex': wrap.hex(),
                    'contract_table_bytes_before_after': [174, 176], 'filter_bytes_before_after': [14, 12],
                    'only_new_memberships': {'direct_parent02054014': list(range(1263, 1268)),
                                            'queued_parent02053DB8': [0x02118680]},
                    'private_quantity_exact_return_addresses': list(returns_for_proof()),
                    'all_owned_footprints_sections_BSS_cache_and_staged_payload_unchanged': True,
                    'research_only_not_registered_or_gameplay_verified': True}


def returns_for_proof():
    return (*PRICE_RETURNS, DAY_RETURN, NEW_DAY_RETURN)
