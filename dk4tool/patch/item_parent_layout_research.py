"""Fit full English detail rows within the native 256-pixel item screen."""

import struct

from dk4tool.patch.grand_race_menu_release import sha

SOURCE = 'edb1032dd92bfbe0c73f18ffdcae71f3b78108bab4ed7546f8b8d3fada739663'
TABLE, STRIDE = 0x116358, 28


def transform(source):
    if sha(source) != SOURCE:
        raise ValueError('Exact cache-maintained item research required')
    if struct.unpack_from('<I', source, 0x4D590)[0] != 0x02116358:
        raise ValueError('Native seven-row item parent descriptor differs')
    rows = [list(struct.unpack_from('<7i', source, TABLE + i * STRIDE)) for i in range(7)]
    expected = [[-1, 8, 2, 0, 84, 240, 12], [-1, 56, 24, 48, 0, 144, 12],
                [-1, 56, 40, 0, 12, 240, 12], [-1, 56, 56, 0, 24, 240, 12],
                [-1, 8, 112, 0, 36, 240, 12], [-1, 8, 128, 0, 48, 240, 12],
                [-1, 8, 144, 0, 60, 240, 12]]
    if rows != expected:
        raise ValueError('Original item parent positions/source crops differ')
    saved = bytearray(source)
    changes = []
    for row, x, y in ((2, 8, 64), (3, 8, 80)):
        for column, value in ((1, x), (2, y)):
            field = TABLE + row * STRIDE + column * 4
            before = struct.unpack_from('<i', source, field)[0]
            struct.pack_into('<i', saved, field, value)
            changes.append({'field': field, 'row': row, 'before': before, 'after': value})
    restored = bytearray(saved)
    for change in changes:
        struct.pack_into('<i', restored, change['field'], change['before'])
    if bytes(restored) != source:
        raise ValueError('Item parent changes unrelated code/text/crops')
    return bytes(saved), {'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(saved),
                         'fields': changes, 'changed_byte_count': sum(a != b for a, b in zip(source, saved)),
                         'full_item_text_helpers_cache_bootstrap_and_other_crops_preserved': True,
                         'reason': 'Category/effect and owner rows at x56 extend to x296; full English needs the entire text width. '
                                   'Move both full rows to x8 below the icon, at y64/y80.',
                         'status': 'parent-layout-research-native-composite-proof-pending'}
