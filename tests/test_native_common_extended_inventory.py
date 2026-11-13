import struct
from types import SimpleNamespace

import pytest
from capstone import CS_ARCH_ARM, CS_MODE_ARM, Cs

from scripts.inventory_native_common_extended_calls import (
    arm_candidates,
    joined_context_argument,
    mapped_dynamic_producers,
    table_message_candidates,
    thumb_candidates,
)

BASE = 0x02000000


def branch_word(address, target, link=False):
    return (0xEB000000 if link else 0xEA000000) | (((target - address - 8) // 4) & 0xFFFFFF)


def test_visible_join_does_not_select_last_linear_case():
    raw = struct.pack('<4I', 0xE3A01007, branch_word(BASE + 4, BASE + 12),
                      0xE3A01008, 0xE1A00002)
    cs = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    cs.detail = True
    assert joined_context_argument(list(cs.disasm(raw, BASE)), raw, BASE, 'r1') is None


def test_assignment_after_join_can_resolve():
    raw = struct.pack('<4I', 0xE3A01007, branch_word(BASE + 4, BASE + 12),
                      0xE3A01008, 0xE3A01009)
    cs = Cs(CS_ARCH_ARM, CS_MODE_ARM)
    cs.detail = True
    assert joined_context_argument(list(cs.disasm(raw, BASE)), raw, BASE, 'r1') == 9


def test_direct_tail_and_wrapper_id_addend():
    raw = struct.pack('<2I', 0xE3A01005, branch_word(BASE + 4, 0x020BF328))
    rows = arm_candidates(raw, BASE)
    assert len(rows) == 1
    assert rows[0]['kind'] == 'direct-tail-branch'
    assert rows[0]['native_id_constant'] == 142


def test_pc_literal_resolves_register_tail():
    raw = struct.pack('<4I', 0xE59FC004, 0xE12FFF1C, 0xE1A00000, 0x020546B8)
    rows = arm_candidates(raw, BASE)
    assert len(rows) == 1
    assert rows[0]['target'] == 0x020546B8
    assert rows[0]['kind'] == 'locally-resolved-register-tail'
    assert rows[0]['native_id_constant'] is None


def test_unknown_register_target_is_not_invented():
    assert arm_candidates(struct.pack('<I', 0xE12FFF1C), BASE) == []


def test_thumb_bl_target_and_unknown_id():
    delta = 0x02054624 - BASE - 4
    raw = struct.pack('<2H', 0xF000 | ((delta >> 12) & 0x7FF),
                      0xF800 | ((delta >> 1) & 0x7FF))
    rows = thumb_candidates(raw, BASE)
    assert len(rows) == 1
    assert rows[0]['target'] == 0x02054624
    assert rows[0]['native_id_constant'] is None


def test_non_call_thumb_pair_does_not_match():
    assert thumb_candidates(struct.pack('<2H', 0xF000, 0x0000), BASE) == []


def test_actor_variant_argument_is_table_pointer_not_message_id():
    raw = struct.pack('<3I', 0xE59F1000, branch_word(BASE + 4, 0x02053EC0, True),
                      0x02117620)
    rows = arm_candidates(raw, BASE)
    assert len(rows) == 1
    assert rows[0]['native_id_constant'] is None
    assert rows[0]['native_table_address_constant'] == 0x02117620


def test_fallback_slots_keep_sentinel_and_native_sources():
    raw = struct.pack('<8I', 0, 1, *([0xFFFFFFFF] * 6))
    entries = [SimpleNamespace(text=b'First'), SimpleNamespace(text=b'Second')]
    rows = table_message_candidates(BASE, raw, entries)
    assert rows[:2] == [{'slot': 0, 'message_id': 0, 'source': 'First'},
                        {'slot': 1, 'message_id': 1, 'source': 'Second'}]
    assert all(row['message_id'] is None and row['source'] is None for row in rows[2:])


@pytest.mark.parametrize('address', [None, BASE + 1, BASE - 4, BASE + 4])
def test_fallback_table_requires_aligned_bounded_storage(address):
    assert table_message_candidates(address, b'\xff' * 32, []) is None


def test_fallback_table_rejects_out_of_range_native_id():
    assert table_message_candidates(BASE, struct.pack('<8I', *([2] * 8)), []) is None


def test_reviewed_switch_target_literal_is_locked():
    with pytest.raises(ValueError, match='switch tail literal'):
        mapped_dynamic_producers(bytes(0x59138), [])
