"""Source-reviewed complete Golden Route labels and lossless allocation research."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.compile_scene_caption_allocation import pack
from scripts.plan_grand_race_ui_allocation_v136 import byte_pointer_references

ROWS = (
    ('PREVIOUS', 0x16A1A0, 8, 0x12EC28, '前へ', 'Previous', 'Previous Golden Route record/page'),
    ('NEXT', 0x16A1A8, 8, 0x12EC2C, '次へ', 'Next', 'Next Golden Route record/page'),
    ('SWITCH', 0x16A1B8, 12, 0x12EC4C, '切り替え', 'Switch', 'Switch the viewer display'),
    ('FOUND', 0x16A1C4, 16, 0x16A1B0, '黄金航路発見！', 'Golden Route Found!', 'A Golden Route has been discovered'),
    ('RECORDS', 0x16A1D4, 16, 0x16A1B4, '黄金航路の記録', 'Golden Route Records', 'Records of Golden Routes'),
    ('EMPTY', 0x16AF7C, 28, 0xF14D8, '黄金航路の記録は有りません', 'No Golden Route records.', 'There are no Golden Route records'),
)
RANGES = ((0x16A1A0, 0x16A1B0), (0x16A1B8, 0x16A1E4), (0x16AF7C, 0x16AF98))
SHARED = {'Next': 0x11B53C, 'Switch': 0x14C114}
SOURCE_SHA = '004aef018e9731fc5ab202ac40cfffe70e2cdc2060e44e7d7ea64946128c7b83'
MANUSCRIPT = Path('translations/golden_route_viewer_manuscript_v2.json')


def compile_manuscript(clean, canonical, current):
    if sha(current) != SOURCE_SHA:
        raise ValueError('Full V138 Golden Route input is required')
    records = []
    expected_refs = {}
    for key, offset, capacity, field, japanese, english, meaning in ROWS:
        raw = japanese.encode('cp932') + b'\0'
        padded = raw.ljust(capacity, b'\0')
        if any(source[offset:offset + capacity] != padded for source in (clean, canonical, current)):
            raise ValueError('Golden Route source/padding ownership differs')
        if any(struct.unpack_from('<I', source, field)[0] != 0x02000000 + offset for source in (clean, canonical, current)):
            raise ValueError('Golden Route literal consumer differs')
        expected_refs[field] = offset
        records.append({'id': 'GOLDEN_ROUTE_VIEWER_' + key, 'source_offset': offset,
                        'source_capacity': capacity, 'pointer_field': field,
                        'source_hex': raw[:-1].hex(), 'japanese': japanese, 'english': english,
                        'speaker': 'Golden Route viewer', 'source_meaning': meaning,
                        'context': ('Native title array 16A1B0, selected by F2BFC:F2C40.' if key in ('FOUND', 'RECORDS')
                                    else 'Zero-record guard F0B70:F0B90 invokes formatted message dialog 5473C.' if key == 'EMPTY'
                                    else 'Native footer descriptor selects this label through CA890/CA780.'),
                        'localization_note': 'Natural complete UI wording; retain discovery, records, navigation and zero-record meaning.',
                        'review': {'source': True, 'context': True, 'localization': True,
                                   'naturalness': True, 'formatting': False}})
    if byte_pointer_references(current, RANGES) != expected_refs:
        raise ValueError('Golden Route source pool has another literal/interior consumer')
    for text, offset in SHARED.items():
        raw = text.encode('ascii') + b'\0'
        if any(source[offset:offset + len(raw)] != raw for source in (canonical, current)):
            raise ValueError('Accepted complete shared English differs')
    return {'format': 'dk4-golden-route-viewer-manuscript-v2', 'translation_policy': 'natural-dialogue-v2',
            'target_locale': 'en-US', 'status': 'source-reviewed-native-formatting-pending',
            'clean_arm9_sha256': sha(clean), 'source_arm9_sha256': sha(current), 'records': records,
            'limitations': ['Native formatted title/footer/modal consumers require complete execution and layout gates.',
                            'Literal pointer coverage does not establish computed/Thumb/overlay ownership.',
                            'No separate COMMON translations or ROM integration credit.']}


def compile_allocation(document, source):
    if sha(source) != SOURCE_SHA or len(document['records']) != 6:
        raise ValueError('Complete source-locked Golden Route scope required')
    for row, (key, offset, capacity, field, japanese, _, _) in zip(document['records'], ROWS, strict=True):
        if (row['id'], row['source_offset'], row['source_capacity'], row['pointer_field'], row['japanese'], row['source_hex']) != (
                'GOLDEN_ROUTE_VIEWER_' + key, offset, capacity, field, japanese, japanese.encode('cp932').hex()):
            raise ValueError('Golden Route manuscript source or complete consumer scope differs')
        if not all(row['review'][gate] is True for gate in ('source', 'context', 'localization', 'naturalness')):
            raise ValueError('Golden Route editorial review is incomplete')
        text = row['english']
        if not text or text != text.strip() or any(not 32 <= ord(c) <= 126 for c in text) or '%' in text:
            raise ValueError('Golden Route labels require complete printable literal English')
    entries = {row['english']: row['english'].encode('ascii') + b'\0'
               for row in document['records'] if row['english'] not in SHARED}
    offsets, unused = pack(entries, RANGES)
    proposed = bytearray(source)
    for lo, hi in RANGES:
        proposed[lo:hi] = bytes(hi - lo)
    for text, offset in offsets.items():
        proposed[offset:offset + len(entries[text])] = entries[text]
    selections = {**offsets, **SHARED}
    cases = []
    for row in document['records']:
        target = selections[row['english']]
        struct.pack_into('<I', proposed, row['pointer_field'], 0x02000000 + target)
        raw = row['english'].encode('ascii') + b'\0'
        if proposed[target:proposed.index(0, target) + 1] != raw:
            raise ValueError('Complete Golden Route text or leading/last bytes/NUL differ')
        cases.append({'id': row['id'], 'pointer_field': row['pointer_field'], 'offset': target,
                      'english': row['english'], 'width_pixels_at_six': len(row['english']) * 6})
    allowed = [*RANGES, *((row['pointer_field'], row['pointer_field'] + 4) for row in document['records'])]
    if any(old != new and not any(lo <= at < hi for lo, hi in allowed)
           for at, (old, new) in enumerate(zip(source, proposed, strict=True))):
        raise ValueError('Golden Route proposal changes unrelated bytes')
    return bytes(proposed), {'selections': cases, 'owned_ranges': RANGES, 'unused_ranges': unused,
                             'owned_bytes': sum(hi - lo for lo, hi in RANGES),
                             'unused_bytes': sum(hi - lo for lo, hi in unused),
                             'shared_accepted_full_labels': SHARED, 'code_changed': False}


def main():
    clean, canonical, current = [NdsImage.open(path).read_file('/__arm9__.bin') for path in (
        'work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds', 'out/all_routes_combined_v138_candidate.nds')]
    document = compile_manuscript(clean, canonical, current)
    proposed, report = compile_allocation(document, current)
    MANUSCRIPT.write_text(json.dumps(document, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    report.update({'status': 'complete-source-reviewed-golden-route-allocation-native-formatting-pending',
                   'source_arm9_sha256': SOURCE_SHA, 'proposed_arm9_sha256': sha(proposed),
                   'manuscript_sha256': sha(MANUSCRIPT.read_bytes()), 'rom_written': False})
    output = Path('work/analysis/golden_route_viewer_complete_v138')
    output.mkdir(parents=True, exist_ok=True)
    (output / 'proposed_arm9.bin').write_bytes(proposed)
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print(f'All six complete Golden Route labels fit; {report["unused_bytes"]} source-owned bytes spare; native formatting pending.')


if __name__ == '__main__':
    main()
