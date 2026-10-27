"""Source-locked complete translations of the two remaining ordinary names."""

import json
from pathlib import Path

from dk4tool.dialogue.review import validate_natural_dialogue_batch
from dk4tool.patch.grand_race_menu_release import sha

SOURCE = '30ae21c22c5f2d1e42a986331aa52a0df6e9d69fcf6a8f9d195726e751f4ea66'
TARGET = 'dde53bd0a3832dc4c01437f119ba10faaaab47b053234fb27bbcab545710862a'
NAMES = [(61, 0x15C1E8, 'ヴェルス', 'Vels'), (77, 0x15C7D0, 'アカブー', 'Akaboo')]


def transform(source):
    if sha(source) != SOURCE:
        raise ValueError('Residual names require the exact complete V149 stack')
    saved = bytearray(source)
    for _, at, japanese, english in NAMES:
        if source[at:at + 12] != japanese.encode('cp932').ljust(12, b'\0'):
            raise ValueError('Original complete given-name owner differs')
        saved[at:at + 12] = (english.encode('ascii') + b'\0').ljust(12, b'\0')
    if sha(saved) != TARGET:
        raise ValueError('Residual names differ from reviewed target')
    return bytes(saved)


def apply_release(source, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if (config.get('format') != 'dk4-residual-character-name-release-v1'
            or config['source_arm9_sha256'] != SOURCE or config['target_arm9_sha256'] != TARGET):
        raise ValueError('Residual name release identity differs')
    if set(config['dependencies']) != {config['manuscript'], config['native_review']}:
        raise ValueError('Both name manuscript and native review required')
    for path, digest in config['dependencies'].items():
        if sha(Path(path).read_bytes()) != digest:
            raise ValueError('Name manuscript or native review changed')
    document = json.loads(Path(config['manuscript']).read_text(encoding='utf-8'))
    validate_natural_dialogue_batch(document)
    if len(document['records']) != 2:
        raise ValueError('Both complete character names required')
    for row, (_, at, japanese, english) in zip(document['records'], NAMES, strict=True):
        if (row['offset'] != at or row['capacity'] != 12 or row['japanese'] != japanese
                or row['english'] != english + '{PAD}'
                or source[at:at + 12] != bytes.fromhex(row['source_hex'])):
            raise ValueError('Original source/complete character spelling differs')
    review = json.loads(Path(config['native_review']).read_text(encoding='utf-8'))
    native, paired, visual = review['getters'], review['paired'], review['native_ink_visual_review']
    if (native['research_sha256'] != TARGET or paired['research_sha256'] != TARGET
            or native['all_207_ordinary_given_names_printable_without_japanese'] is not True
            or len(native['native_given_names']) != 207 or len(native['fleet_rasters']) != 4
            or {(r['index'], r['row'], r['text']) for r in paired['cases']}
            != {(index, row, english) for index, _, _, english in NAMES for row in (0, 1)}
            or len(paired['rasters']) != 4
            or any(not r['independent_pixels_match'] or not r['header_descriptor_and_pixel_guards_preserved']
                   for r in paired['rasters'])
            or any(not r['native_captain_selector_and_name_dispatch_verified']
                   or not r['full_glyph_order_bounds_and_independent_pixels_verified'] for r in native['fleet_rasters'])
            or visual['panels_reviewed'] != 2 or visual['rows_reviewed'] != 4
            or visual['complete_leading_and_final_glyphs'] is not True
            or visual['no_clipping_or_row_overlap'] is not True):
        raise ValueError('Complete name getter and native layout evidence required')
    saved = transform(source)
    return saved, {'status': 'pass-residual-character-names-native-layout-gameplay-pending',
                   'arm9_sha256': sha(saved), 'translated_given_name_indices': [61, 77],
                   'unchanged_given_names': 205, 'paired_name_rasters': 4,
                   'fleet_name_rasters': 4, 'runtime_verified': False}
