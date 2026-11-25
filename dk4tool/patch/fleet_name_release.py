"""Complete fleet labels in source-owned storage after persistent-name repair."""

import json
import struct
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.persistent_name_release import TARGET as SOURCE


def transform(source):
    if sha(source) != SOURCE:
        raise ValueError('Fleet labels require the exact complete V148 stack')
    old, spare = 0x135260, 0x138878
    if (source[old:old + 16] != '所属不明艦隊'.encode('cp932').ljust(16, b'\0')
            or source[0x135258:old] != '海賊%s'.encode('cp932').ljust(8, b'\0')
            or any(source[spare:spare + 28])
            or struct.unpack_from('<2I', source, 0x36B54) != (0x02135260, 0x02135258)):
        raise ValueError('Original fleet owners, references or companion spare differ')
    saved = bytearray(source)
    saved[old:old + 16] = b'Pirate %s\0'.ljust(16, b'\0')
    saved[spare:spare + 28] = b'Unidentified fleet\0'.ljust(28, b'\0')
    struct.pack_into('<2I', saved, 0x36B54, 0x02138878, 0x02135260)
    return bytes(saved)


def apply_release(source, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config.get('format') != 'dk4-fleet-name-release-v1' or config['source_arm9_sha256'] != SOURCE:
        raise ValueError('Fleet release format or source identity differs')
    if set(config['dependencies']) != {config['manuscript'], config['native_review']}:
        raise ValueError('Both fleet manuscript and native review required')
    for path, digest in config['dependencies'].items():
        if sha(Path(path).read_bytes()) != digest:
            raise ValueError('Fleet release dependency changed')
    manuscript = json.loads(Path(config['manuscript']).read_text(encoding='utf-8'))
    validate_natural_dialogue_batch(manuscript)
    rows = manuscript['records']
    expected = [(0x135258, 8, '海賊%s', 'Pirate %s{PAD}'),
                (0x135260, 16, '所属不明艦隊', 'Unidentified fleet{PAD}')]
    if len(rows) != 2:
        raise ValueError('Both complete source-faithful fleet labels required')
    for row, (at, size, japanese, english) in zip(rows, expected, strict=True):
        if (row['offset'] != at or row['capacity'] != size or row['japanese'] != japanese
                or row['english'] != english or source[at:at + size] != bytes.fromhex(row['source_hex'])):
            raise ValueError('Complete fleet source/wording lock differs')
    review = json.loads(Path(config['native_review']).read_text(encoding='utf-8'))
    saved = transform(source)
    visual = review['native_ink_visual_review']
    cases = review['cases']
    ordinary = [r for r in cases if r['captain_index_fixture'] != r['current_character_fixture']
                and r['captain_index_fixture'] != 208]
    players = [r for r in cases if r['captain_index_fixture'] == r['current_character_fixture']]
    if (review['source_arm9_sha256'] != SOURCE or review['research_arm9_sha256'] != sha(saved)
            or config['target_arm9_sha256'] != sha(saved) or len(cases) != 456
            or len(ordinary) != 414 or len(players) != 40
            or {(r['caller'], r['captain_index_fixture']) for r in ordinary}
            != {(kind, index) for kind in ('fixed', 'centered') for index in range(207)}
            or visual['panels_reviewed'] != 10
            or visual['complete_leading_and_final_glyphs'] is not True
            or visual['no_clipping_or_row_overlap'] is not True
            or any(not r['native_captain_selector_and_name_dispatch_verified']
                   or not r['full_glyph_order_bounds_and_independent_pixels_verified'] for r in cases)):
        raise ValueError('Complete native fleet selection/glyph review required')
    return saved, {'status': 'pass-full-fleet-labels-mapped-native-displays-gameplay-pending',
                   'arm9_sha256': sha(saved), 'literal_references': 2,
                   'ordinary_name_rasters': 414, 'stored_player_name_rasters': 40,
                   'sentinel_rasters': 2, 'runtime_verified': False}
