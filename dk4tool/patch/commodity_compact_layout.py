"""Complete commodity names and a specialty-only compact painter without growth."""

import struct

from dk4tool.patch.commodity_source_repack import transform as repack
from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_common_display_name_hook import branch_link

BASE = 0x02000000
CALL = 0xB63D4
ROWS = [0x11A73C + i * 28 for i in range(5)]


def compact_helper(address):
    return struct.pack('<9I', 0xE92D4070, 0xE1A04000, 0xE590501C,
                       0xE3E02000, 0xE580201C,
                       branch_link(address + 20, BASE + 0xD5404),
                       0xE584501C, 0xE8BD8070, 0xE1A00000)


def transform(source, clean, manuscript, allocation):
    packed, names = repack(source, clean, manuscript, allocation)
    target = bytearray(packed)
    region = allocation['specialty_helper_region']
    lo, hi = region['start'], region['end']
    assert hi - lo == 40 and lo % 4 == 0
    fields = {r['pointer_field'] for r in manuscript['records']}
    for field in range(0, len(source) - 3, 4):
        ptr = struct.unpack_from('<I', source, field)[0] - BASE
        if lo <= ptr < hi:
            assert field in fields
    helper = compact_helper(BASE + lo)
    target[lo:hi] = helper + bytes(hi - lo - len(helper))
    original = branch_link(BASE + CALL, BASE + 0xD5404)
    assert struct.unpack_from('<I', source, CALL)[0] == original
    struct.pack_into('<I', target, CALL, branch_link(BASE + CALL, BASE + lo))
    changes = []
    for i, row in enumerate(ROWS):
        expected = (-1, 152, 88 + i * 16, 108, i * 12, 72, 12)
        assert struct.unpack_from('<7i', source, row) == expected
        assert struct.unpack_from('<7i', clean, row) == expected
        struct.pack_into('<I', target, row + 20, 96)
        changes.append({'descriptor': row, 'old_width': 72, 'new_width': 96,
                        'source_rect': [108, i * 12, 204, i * 12 + 12],
                        'local_destination': [152, 88 + i * 16, 248, 100 + i * 16]})
    # Keep the original 228x72 backing bitmap and visible percentage geometry.
    percentage_changes = []
    for i, (x, y) in enumerate([(60, 12), (204, 36), (204, 48)]):
        row = 0x11A7C8 + i * 28
        original = struct.unpack_from('<7i', source, row)
        assert original[3:5] == (180, i * 12)
        assert source[row:row + 28] == clean[row:row + 28]
        struct.pack_into('<2I', target, row + 12, x, y)
        percentage_changes.append({'descriptor': row, 'old_source': list(original[3:5]),
                                   'new_source': [x, y], 'visible_geometry_preserved': True})
    rectangles = [struct.unpack_from('<7i', target, 0x11A65C + i * 28)[3:7] for i in range(21)]
    for i, (x, y, w, h) in enumerate(rectangles):
        assert 0 <= x < x + w <= 228 and 0 <= y < y + h <= 72
        for xx, yy, ww, hh in rectangles[:i]:
            assert x + w <= xx or xx + ww <= x or y + h <= yy or yy + hh <= y
    restored = bytearray(target)
    restored[lo:hi] = packed[lo:hi]
    restored[CALL:CALL + 4] = packed[CALL:CALL + 4]
    for row in ROWS:
        restored[row + 20:row + 24] = packed[row + 20:row + 24]
    for change in percentage_changes:
        row = change['descriptor']
        restored[row + 12:row + 20] = packed[row + 12:row + 20]
    assert bytes(restored) == packed
    return bytes(target), {'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(target),
                           'name_repack': names, 'helper_region': [lo, hi], 'helper': BASE + lo,
                           'helper_bytes': helper.hex(), 'call_field': CALL,
                           'specialty_crop_rows': changes,
                           'percentage_source_relocations': percentage_changes,
                           'tracking_restored_after_each_specialty_only_call': True,
                           'no_pool_heap_backing_bitmap_or_startup_expansion': True,
                           'actual_display_and_other_name_contexts_pending': True}
