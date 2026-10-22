"""Source-locked first-row margin correction through the existing modal painter."""

import json
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-unguarded-dialogue-alignment-v1'
    assert sha(source) == config['source_arm9_sha256']
    for file, digest in config['dependencies_sha256'].items():
        assert sha(Path(file).read_bytes()) == digest, file
    code = MainCodeFile(source, 0x02000000)
    before = [bytes(s.data) for s in code.sections]
    assert len(before) == 5 and code.sections[4].ramAddress == 0x01FFC000
    field = config['call_site']
    assert field == 0x54924
    old, new = bytes.fromhex(config['expected_call_hex']), bytes.fromhex(config['replacement_call_hex'])
    assert len(old) == len(new) == 4
    assert bytes(code.sections[0].data[field:field + 4]) == old
    code.sections[0].data[field:field + 4] = new
    assert len(before[4]) == config['original_autoload_length']
    code.sections[4].data.extend(bytes.fromhex(config['autoload_suffix_hex']))
    assert len(code.sections[4].data) <= 0x1000
    target = bytes(code.save())
    assert sha(target) == config['target_arm9_sha256']
    parsed = MainCodeFile(target, 0x02000000)
    assert all(bytes(parsed.sections[i].data) == before[i] for i in (1, 2, 3))
    assert bytes(parsed.sections[4].data[:len(before[4])]) == before[4]
    restored = bytearray(parsed.sections[0].data)
    restored[field:field + 4] = old
    at = code.codeSettingsOffs
    restored[at:at + 12] = before[0][at:at + 12]
    assert bytes(restored) == before[0]
    return target, {'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(target),
                    'source_text_controls_macros_font_dimensions_and_continuations_preserved': True,
                    'native_pair_flush_room_required_before_first_row_shift': True,
                    'other_inputs_use_inherited_painter': True,
                    'changed_records': ['COMMON_UNGUARDED_FIRST_ROW_MARGIN'],
                    'status': 'experimental', 'full_graphics_goal_complete': False}
