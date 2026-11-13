"""Retain source-view origins in the shared compact ASCII callback."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_commodity_market_v350 import helper

SOURCE = 'd1bf89d13b0094eaa27464849279e1fdb3254cc6f9f82699522adf0ae8e188df'
FIELD, ORIGINAL, WRAPPER = 0x160400, 0x020D501C, 0x01FFC71C


def transform(source):
    if sha(source) != SOURCE:
        raise ValueError('Compact source origins require the complete V617 ARM9')
    code = MainCodeFile(source, 0x02000000)
    before = [bytes(s.data) for s in code.sections]
    assert len(before) == 5 and code.sections[4].ramAddress == 0x01FFC000
    assert struct.unpack_from('<I', source, FIELD)[0] == ORIGINAL
    # The market's existing wrapper resolves the original source-view point,
    # adds the supplied local point, then calls the unchanged absolute painter.
    # Its low byte 1C preserves the compact dispatch class discriminator.
    old = helper(source)[0x11C:]
    expected = bytearray(old)
    from scripts.probe_common_display_name_hook import branch_link

    struct.pack_into('<I', expected, 84, branch_link(WRAPPER + 84, ORIGINAL))
    assert before[4][0x71C:0x77C] == expected and len(expected) == 96
    assert struct.unpack_from('<I', before[4], 0x61C)[0] == WRAPPER
    assert source[0xD573C:0xD574C] == bytes.fromhex('1c3093e5ffc003e21c005ce3050000ea')
    struct.pack_into('<I', code.sections[0].data, FIELD, WRAPPER)
    target = bytes(code.save())
    restored = bytearray(MainCodeFile(target, 0x02000000).sections[0].data)
    restored[FIELD:FIELD + 4] = before[0][FIELD:FIELD + 4]
    assert restored == before[0]
    assert all(bytes(s.data) == before[i] for i, s in enumerate(
        MainCodeFile(target, 0x02000000).sections) if i)
    return target, {
        'source_arm9_sha256': SOURCE, 'target_arm9_sha256': sha(target),
        'callback_field': FIELD, 'old_absolute_callback': ORIGINAL,
        'existing_source_origin_callback': WRAPPER, 'wrapper_bytes': 96,
        'wrapper_sha256': sha(expected), 'only_one_existing_font_callback_changed': True,
        'all_code_strings_other_callbacks_sections_pool_startup_and_arenas_exact': True,
        'market_private_font_already_uses_same_wrapper': True,
        'changed_records': ['COMPACT_ASCII_SOURCE_BITMAP_ORIGIN'],
        'experimental': True, 'full_goal_complete': False,
    }


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-compact-bitmap-origin-v1'
    target, proof = transform(source)
    assert config['proof'] == proof
    return target, proof
