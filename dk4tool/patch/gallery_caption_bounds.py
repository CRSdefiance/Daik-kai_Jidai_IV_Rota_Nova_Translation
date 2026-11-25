"""Central Gallery title correction and all164 titles' arrow-safe bounds gate."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL, STAGE, cache_plan
from dk4tool.rom.nds import NdsImage

OFFSET = 0x1398C0
OLD = b'Maria and Her Companions at the Grand Review\0'
NEW = b"Maria's Party at the Grand Review\0"


def captions(arm):
    sections = MainCodeFile(arm, BASE).sections
    stage = next(s for s in sections if s.ramAddress == STAGE)
    plan = cache_plan(arm)
    assert plan and plan['payload_bytes'] == len(stage.data) - 48

    def string(pointer):
        if POOL <= pointer < POOL + plan['payload_bytes']:
            raw = bytes(stage.data[pointer - POOL:plan['payload_bytes']])
        else:
            owner = next((s for s in sections if s.ramAddress <= pointer < s.ramAddress + len(s.data)), None)
            if owner is None:
                raise ValueError(f'Gallery caption pointer has no proven resident/staged owner: {pointer:#x}')
            raw = bytes(owner.data[pointer - owner.ramAddress:])
        at = raw.find(b'\0', 0, 256)
        if at < 1:
            raise ValueError('Gallery caption lacks bounded complete NUL-terminated text')
        return raw[:at].decode('ascii')

    result = []
    for route, count, literal in [(0, 46, 0x432DC), (1, 41, 0x432E4),
                                  (2, 39, 0x432EC), (3, 38, 0x432F4)]:
        _, table = struct.unpack_from('<2I', arm, literal)
        for position in range(count):
            field = table - BASE + position * 4
            pointer = struct.unpack_from('<I', arm, field)[0]
            text = string(pointer)
            x = 128 - len(text) * 5 // 2
            width = (len(text) - 1) * 5 + 6
            result.append({'route': route, 'position': position, 'field': field,
                           'pointer': pointer, 'English': text, 'bounds': [x, x + width]})
    assert len(result) == 164
    return result


def validate(arm):
    rows = captions(arm)
    failures = [r for r in rows if r['bounds'][0] < 32 or r['bounds'][1] > 224]
    if failures:
        raise ValueError(f'Gallery captions overlap original arrows: {failures}')
    return rows


def transform(arm):
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    source_pointer = struct.unpack_from('<I', clean, 0x1158C0)[0]
    assert clean[source_pointer - BASE:].split(b'\0')[0].decode('cp932') == '総見式のマリアたち'
    if arm[OFFSET:OFFSET + len(OLD)] != OLD:
        raise ValueError('Exact original translated Grand Review title required')
    before = captions(arm)
    assert [(r['route'], r['position']) for r in before
            if r['bounds'][0] < 32 or r['bounds'][1] > 224] == [(3, 35)]
    assert before[-3]['field'] == 0x1158C0 and before[-3]['pointer'] == BASE + OFFSET
    result = arm[:OFFSET] + NEW.ljust(len(OLD), b'\0') + arm[OFFSET + len(OLD):]
    after = validate(result)
    assert len(result) == len(arm)
    assert [(a['route'], a['position']) for a, b in zip(before, after) if a != b] == [(3, 35)]
    return result, {'changed_records': ['SCENE_CAPTION_ROUTE_3_35'],
                    'original_Japanese': '総見式のマリアたち',
                    'English': NEW[:-1].decode(), 'owned_string_span': [OFFSET, len(OLD)],
                    'all164_final_captions_resolved_and_arrow_safe': after,
                    'permitted_native_caption_horizontal_bounds': [32, 224],
                    'code_pointers_palettes_borders_dimensions_and_other_data_unchanged': True,
                    'no_allocation_or_pool_growth': True, 'status': 'experimental'}


def apply_release(arm, path):
    config = json.loads(Path(path).read_text(encoding='utf-8'))
    assert config['format'] == 'dk4-gallery-caption-bounds-v1'
    assert sha(arm) == config['source_arm9_sha256']
    result, report = transform(arm)
    assert sha(result) == config['target_arm9_sha256']
    return result, report
