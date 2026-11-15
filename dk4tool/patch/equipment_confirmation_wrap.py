"""Source-locked equipment confirmation word wrapping after name expansion."""

import json
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha


def apply_release(source, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-equipment-confirmation-wrap-v1'
    assert sha(source) == config['source_arm9_sha256']
    for file, digest in config['dependencies_sha256'].items():
        assert sha(Path(file).read_bytes()) == digest, file
    code = MainCodeFile(source, 0x02000000)
    before = [bytes(s.data) for s in code.sections]
    assert len(before) == 5 and code.sections[4].ramAddress == 0x01FFC000
    assert config['scope'] == {'native_parent_return': 0x020546E8, 'native_message_ids': [321, 327]}
    field = config['macro_call']
    assert field == 0x54798
    old = bytes.fromhex(config['expected_call_hex'])
    new = bytes.fromhex(config['replacement_call_hex'])
    assert len(old) == len(new) == 4
    assert bytes(code.sections[0].data[field:field + 4]) == old
    code.sections[0].data[field:field + 4] = new
    suffix = bytes.fromhex(config['autoload_suffix_hex'])
    assert len(before[4]) == config['original_autoload_length']
    assert len(before[4]) + len(suffix) <= 0x1000
    code.sections[4].data.extend(suffix)
    target = bytes(code.save())
    assert sha(target) == config['target_arm9_sha256']
    parsed = MainCodeFile(target, 0x02000000)
    assert all(bytes(parsed.sections[i].data) == before[i] for i in (1, 2, 3))
    assert bytes(parsed.sections[4].data[:len(before[4])]) == before[4]
    restored = bytearray(parsed.sections[0].data)
    restored[field:field + 4] = old
    settings = code.codeSettingsOffs
    restored[settings:settings + 12] = before[0][settings:settings + 12]
    assert bytes(restored) == before[0]
    return target, {
        'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(target),
        'scope': config['scope'],
        'source_prose_names_controls_and_previous_payload_bytes_preserved': True,
        'other_messages_preserve_inherited_wrapper': True,
        'changed_records': ['COMMON_321_EQUIPMENT_WORD_WRAP', 'COMMON_327_EQUIPMENT_WORD_WRAP'],
        'status': 'experimental', 'full_graphics_goal_complete': False,
    }
