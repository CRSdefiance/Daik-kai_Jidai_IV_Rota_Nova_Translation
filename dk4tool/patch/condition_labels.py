"""Reviewed condition labels with preserved original strings and effect code."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha


def apply_release(source, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-condition-labels-v1'
    assert sha(source) == config['source_arm9_sha256']
    for path, digest in config['dependencies'].items():
        assert sha(Path(path).read_bytes()) == digest, path
    code = MainCodeFile(source, 0x02000000)
    before = [bytes(s.data) for s in code.sections]
    assert len(before) == 5 and code.sections[4].ramAddress == 0x01FFC000
    assert len(before[4]) == config['original_autoload_length'] == 3880
    assert {r['field'] for r in config['pointer_changes']} == {0x1483C4, 0x1483D0, 0x1483D4}
    for row in config['pointer_changes']:
        assert struct.unpack_from('<I', before[0], row['field'])[0] == row['old_pointer']
        struct.pack_into('<I', code.sections[0].data, row['field'], row['new_pointer'])
    code.sections[4].data.extend(bytes.fromhex(config['autoload_suffix_hex']))
    assert len(code.sections[4].data) == 3900
    assert len(code.sections[4].data) <= 4096
    target = bytes(code.save())
    assert sha(target) == config['target_arm9_sha256']
    parsed = MainCodeFile(target, 0x02000000)
    assert all(bytes(parsed.sections[i].data) == before[i] for i in (1, 2, 3))
    assert bytes(parsed.sections[4].data[:3880]) == before[4]
    restored = bytearray(parsed.sections[0].data)
    for row in config['pointer_changes']:
        struct.pack_into('<I', restored, row['field'], row['old_pointer'])
    at = code.codeSettingsOffs
    restored[at:at + 12] = before[0][at:at + 12]
    assert bytes(restored) == before[0]
    return target, {'changed_records': ['MOOD_STATE_5_CONFUSED', 'HEALTH_STATE_2_HURT', 'HEALTH_STATE_3_WOUNDED'],
                    'all_original_string_bytes_effect_code_font_palettes_and_dimensions_preserved': True,
                    'reserved_data_extent': 3900, 'no_new_code_or_arenas': True,
                    'status': 'experimental', 'full_goal_complete': False}
