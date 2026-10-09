import struct

from scripts.plan_grand_race_ui_allocation_v136 import BASE, byte_pointer_references


def test_unaligned_interior_reference_is_not_lost():
    data = bytearray(32)
    struct.pack_into('<I', data, 5, BASE + 103)
    assert byte_pointer_references(data, [(100, 108)]) == {5: 103}


def test_final_possible_pointer_field_is_scanned():
    data = bytearray(11)
    struct.pack_into('<I', data, 7, BASE + 100)
    assert byte_pointer_references(data, [(100, 108)]) == {7: 100}


def test_end_boundaries_and_neighbor_gaps_are_excluded():
    data = bytearray(24)
    for field, target in ((0, 99), (4, 108), (8, 110), (12, 120), (16, 125)):
        struct.pack_into('<I', data, field, BASE + target)
    assert byte_pointer_references(data, [(100, 108), (120, 125)]) == {12: 120}


def test_arm9_relative_integer_is_not_a_runtime_pointer():
    data = struct.pack('<II', 100, BASE + 100)
    assert byte_pointer_references(data, [(100, 108)]) == {4: 100}
