"""Guarded cumulative commodity names and scoped town/market UI integration."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha

BASE, TABLE, COUNT = 0x02000000, 0x15EF18, 124


def apply_release(source, clean, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-commodity-ui-release-v1'
    assert sha(source) == config['source_arm9_sha256']
    for file, digest in config['dependencies_sha256'].items():
        assert sha(Path(file).read_bytes()) == digest, file
    manuscript = json.loads(Path(config['manuscript']).read_text(encoding='utf-8'))
    assert len(manuscript['records']) == COUNT
    code = MainCodeFile(source, BASE)
    before = [bytes(s.data) for s in code.sections]
    assert len(before) == 4
    permitted = config['owned_main_ranges']
    for row in config['main_section_patches']:
        offset = row['offset']
        old, new = bytes.fromhex(row['expected_hex']), bytes.fromhex(row['replacement_hex'])
        assert len(old) == len(new) and any(lo <= offset < offset + len(old) <= hi for lo, hi in permitted)
        assert bytes(code.sections[0].data[offset:offset + len(old)]) == old
        code.sections[0].data[offset:offset + len(old)] = new
    extra = config['new_autoload_section']
    payload = bytes.fromhex(extra['data_hex'])
    assert extra['ram_address'] == 0x01FFC000 and len(payload) <= 0x1000
    for s in code.sections:
        assert s.ramAddress + len(s.data) + s.bssSize <= extra['ram_address'] or extra['ram_address'] + len(payload) <= s.ramAddress
    code.sections.append(MainCodeFile.Section(payload, extra['ram_address'], 0))
    target = bytes(code.save())
    assert sha(target) == config['target_arm9_sha256']
    parsed = MainCodeFile(target, BASE)
    assert all(bytes(parsed.sections[i].data) == before[i] for i in (1, 2, 3))
    assert target[0xE45DC:0xE45E0] == source[0xE45DC:0xE45E0]
    assert target[0x9F068:0x9F06C] == source[0x9F068:0x9F06C]  # No Maria visibility fixture.
    for row in manuscript['records']:
        index = row['index']
        field = TABLE + index * 12
        pointer = struct.unpack_from('<I', target, field)[0] - BASE
        assert target[pointer:target.index(0, pointer)].decode('ascii') == row['English']
        assert target[field + 4:field + 12] == source[field + 4:field + 12]
        old_pointer = struct.unpack_from('<I', clean, field)[0] - BASE
        assert clean[old_pointer:clean.index(0, old_pointer)].decode('cp932') == row['Japanese']
    # Enforce the printf contract that failed in the legacy translation.
    if config.get('full_market_printf_guard'):
        assert set(config['printf_pointer_fields']) == {0xC3EF8, 0xC4074}
    for field in config['printf_pointer_fields']:
        pointer = struct.unpack_from('<I', target, field)[0]
        offset = pointer - extra['ram_address']
        assert payload[offset:payload.index(0, offset)] == b'%s\n  %s %d%%'
    report = {'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(target),
              'all124_complete_names_and_metadata_verified': True,
              'fresh49_names_localized': sum(r['change_required'] for r in manuscript['records']),
              'old_autoload_sections_heap_bounds_and_Maria_unlock_behavior_preserved': True,
              'new_declared_autoload_span': [extra['ram_address'], extra['ram_address'] + len(payload)],
              'changed_records': ['COMMODITY_NAME_' + str(r['index']) for r in manuscript['records'] if r['change_required']]
                                 + ['COMMODITY_TOWN_NAME_LAYOUT', 'COMMODITY_MARKET_PRIVATE_NAME_LAYOUT',
                                    'COMMODITY_NATIVE_PRINTF_TERMINATOR', 'COMMODITY_SHORTAGE_TREND_LABELS'],
              'status': 'experimental-scoped-native-and-emulator-verified',
              'full_graphics_goal_complete': False}
    if config.get('price_name_layout'):
        report['changed_records'].append('COMMODITY_PRICE_NAME_LAYOUT')
    if config.get('cargo_format_layout'):
        report['changed_records'].append('COMMODITY_CARGO_PRINTF_TERMINATOR_AND_STATUS')
    return target, report
