import struct

from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs

from scripts.inventory_native_common_calls import (
    TARGETS,
    direct_bl_target,
    locally_resolved_argument,
)


def resolve(words, register='r1'):
    raw = struct.pack(f'<{len(words)}I', *words)
    cs = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    cs.detail = True
    return locally_resolved_argument(list(cs.disasm(raw, 0x02000000)), raw,
                                     0x02000000, register)


def test_signed_arm_bl_and_non_bl():
    assert direct_bl_target(0xEBFFFFFF, 0x1000) == 0x1004
    assert direct_bl_target(0xEB000001, 0x1000) == 0x100C
    assert direct_bl_target(0xEA000001, 0x1000) is None
    assert direct_bl_target(0xFA000001, 0x1000) is None


def test_mov_add_propagates_local_constant():
    assert resolve([0xE3A00007, 0xE2801001]) == 8


def test_conditional_assignment_invalidates_old_value():
    assert resolve([0xE3A01007, 0x13A01008]) is None


def test_call_clobbers_argument_register():
    assert resolve([0xE3A01007, 0xEB000000]) is None


def test_call_preserves_saved_register():
    assert resolve([0xE3A04007, 0xEB000000, 0xE1A01004]) == 7


def test_branch_does_not_invent_incoming_value():
    assert resolve([0xE3A01007, 0xEA000000]) is None
    assert resolve([0xE1A01004]) is None


def test_varargs_native_id_registers():
    assert TARGETS[0x02053F9C] == TARGETS[0x02053FE4] == 'r1'
    assert all(TARGETS[t] == 'r0' for t in (0x02054624, 0x0205466C, 0x020546B8))
