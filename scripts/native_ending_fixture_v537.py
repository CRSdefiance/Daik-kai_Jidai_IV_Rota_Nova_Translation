"""Opt-in ending-state fixture; no ROM edits or earned completion claim."""

import struct

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
)

from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_button_prompt_native import call, machine

BASE = 0x02000000
ARM_SHA = '4a42ec3e5ea9fe4b0df425b22a9d446f44336912b237c2474bafbb8331bc6865'
# V578 checks all five V537 ending/captain/teardown/playback source ranges
# against the clean ROM before extending the fixture to this exact V573 build.
VERIFIED_ARM_SHAS = frozenset({
    ARM_SHA,
    '1f94c9c084552fa93cefd80ad195dda054cf9fdaa06a488d2a3943b37822aa5f',
    # V583 independently checks the same five clean-code ranges for V581.
    '60948e7a8f50abc838cfdf49114782aeeb977b75352dc741e90e8dafd161150e',
    # V594 checks the five ending ranges against clean source and proves that
    # V593 differs from V581 only in15 bytes of two Deck room text slots.
    '869431ccc3de5436ef9b33f9f3807d28c298be57cc757c2ee4c3618fba82651e',
    # V630 independently pins all five original ending ranges and full FLS
    # update/draw/selector/math ranges against clean source before a new run.
    'b846e39d42a0d7bded3607c672f94cf251f8d63892cf9444a02b6805713fcc29',
    # V642 independently checks all ten pinned original ending/FLS code ranges
    # and complete M29-M32 movies against clean before testing exact V640.
    '54e35ccaf340a40506a98b0bc3fb7b14091eacac3548fe305d8e553922aa8da1',
})


def request_ending(arm, raw, captain):
    if sha(arm) not in VERIFIED_ARM_SHAS or len(raw) != 0x400000:
        raise ValueError('Ending fixture requires an exact verified ARM9 and 4 MiB RAM')
    if type(captain) is not int or not 0 <= captain <= 3:
        raise ValueError('Supply expected active captain ID 0..3')
    manager = struct.unpack_from('<I', arm, 0x7F250)[0]
    if manager != struct.unpack_from('<I', arm, 0x5D44)[0] or manager != 0x02279668:
        raise ValueError('Original main-loop/captain state manager differs')
    state_offset = manager + 0x54 - BASE
    prior = struct.unpack_from('<I', raw, state_offset)[0]
    if prior != 1:
        raise ValueError('Ending fixture requires active gameplay state 1')
    u = machine(arm)
    u.mem_write(BASE, raw)
    call(u, 0x7F244, ())
    if u.reg_read(UC_ARM_REG_R0) != captain:
        raise ValueError('Actual active captain differs from requested fixture')
    observed = []

    def contracts(uc, address, size, data):
        if address == BASE + 0xCF7A4:
            # Screen teardown is outside this bounded selection proof.
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif address == BASE + 0xD2B1C:
            observed.append([uc.reg_read(r) for r in
                             (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)])
            uc.reg_write(UC_ARM_REG_R0, 0)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))

    handle = u.hook_add(UC_HOOK_CODE, contracts)
    try:
        executed = call(u, 0x40BF4, ())
    finally:
        u.hook_del(handle)
    if observed != [[29 + captain, 0, 0, 0]] or BASE + 0x7F244 not in executed:
        raise ValueError('Original ending selection differs')
    after = bytearray(raw)
    struct.pack_into('<I', after, state_offset, 4)
    changes = [{'address': BASE + i, 'before': raw[i], 'after': after[i]}
               for i in range(state_offset, state_offset + 4) if raw[i] != after[i]]
    return bytes(after), {
        'synthetic_ending_fixture': True, 'earned_completion_verified': False,
        'active_captain_id': captain, 'state_manager': manager,
        'prior_state': prior, 'requested_state': 4, 'changes': changes,
        'only_temporary_gameplay_state_field_changed': True,
        'original_ending_selector': BASE + 0x40BF4,
        'native_dispatch_arguments': observed[0], 'movie': f'/FLS/M{29 + captain:02d}.fls',
        'selector_proof_contracts': ['CF7A4 teardown skipped', 'D2B1C arguments observed; playback skipped'],
        'actual_playback_verified_by_this_helper': False,
        'before_RAM_sha256': sha(raw), 'after_RAM_sha256': sha(after),
    }
