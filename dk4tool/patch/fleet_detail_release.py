"""Guarded complete fleet captions, sort glyphs and known old-default alias."""

import json
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha


def apply_release(source, clean, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-fleet-detail-release-v1'
    assert sha(source) == config['source_arm9_sha256']
    for file, digest in config['dependencies_sha256'].items():
        assert sha(Path(file).read_bytes()) == digest, file
    for row in config['source_records']:
        raw = bytes.fromhex(row['source_hex'])
        at = row['offset']
        assert clean[at:at + len(raw)] == raw
    code = MainCodeFile(source, 0x02000000)
    before = [bytes(s.data) for s in code.sections]
    assert len(before) == 5 and code.sections[4].ramAddress == 0x01FFC000
    owned = config['owned_main_ranges']
    for row in config['main_patches']:
        at = row['offset']
        old, new = bytes.fromhex(row['expected_hex']), bytes.fromhex(row['replacement_hex'])
        assert len(old) == len(new)
        assert any(lo <= at < at + len(old) <= hi for lo, hi in owned)
        assert bytes(code.sections[0].data[at:at + len(old)]) == old
        code.sections[0].data[at:at + len(old)] = new
    assert len(before[4]) == config['original_autoload_length']
    code.sections[4].data.extend(bytes.fromhex(config['autoload_suffix_hex']))
    assert len(code.sections[4].data) <= 0x1000
    target = bytes(code.save())
    assert sha(target) == config['target_arm9_sha256']
    parsed = MainCodeFile(target, 0x02000000)
    assert all(bytes(parsed.sections[i].data) == before[i] for i in (1, 2, 3))
    assert bytes(parsed.sections[4].data[:len(before[4])]) == before[4]
    restored = bytearray(parsed.sections[0].data)
    for row in config['main_patches']:
        at = row['offset']; old = bytes.fromhex(row['expected_hex'])
        restored[at:at + len(old)] = old
    at = code.codeSettingsOffs
    restored[at:at + 12] = before[0][at:at + 12]
    assert bytes(restored) == before[0]
    return target, {'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(target),
                    'source_records': config['source_records'],
                    'prior_sections_payload_heap_bounds_and_user_name_fields_preserved': True,
                    'only_known_old_default_tuple_displays_approved_Joakim': True,
                    'sort_original_font_palette_cells_points_and_full_glyphs_preserved': True,
                    'changed_records': config['changed_records'],
                    'status': 'experimental', 'full_graphics_goal_complete': False}
