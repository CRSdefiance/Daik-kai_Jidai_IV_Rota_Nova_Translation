"""Pack full tooltip/creature names while retaining every Golden Route label."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.compile_scene_caption_allocation import pack
from scripts.execute_golden_route_heading import TABLE_LITERAL
from scripts.inventory_map_tooltip_classes import execute_class, inventory
from scripts.plan_grand_race_ui_allocation_v136 import byte_pointer_references
from scripts.prepare_golden_route_viewer import ROWS as GOLDEN_ROWS
from scripts.prepare_map_entity_tooltips import RANGES as MAP_RANGES
from scripts.prepare_map_entity_tooltips import SOURCE_SHA, formatted_text, prepare

BASE = 0x02000000
OLD_TABLE, NEW_TABLE = 0x16A1B0, 0x15B7E8
RANGES = ((0x16A1A0, 0x16A1E4), (0x16AF7C, 0x16AF98), *MAP_RANGES,
          (0x15BC58, 0x15BC60), (0x15B958, 0x15B960), (0x15B76C, 0x15B770))
OWNED = (*RANGES, (NEW_TABLE, NEW_TABLE + 8))
SHARED = {'Monster': 0x17223D, 'Whale': 0x15BB90, 'Shark': 0x15CB59,
          'Next': 0x11B53C, 'Switch': 0x14C114}


def compile_allocation(clean, canonical, current):
    if sha(current) != SOURCE_SHA:
        raise ValueError('Complete V139 parent required')
    map_document, _, _ = prepare(clean, canonical, current)
    class_report, creatures = inventory(clean, current)
    golden = []
    for key, offset, capacity, field, japanese, english, meaning in GOLDEN_ROWS:
        raw = japanese.encode('cp932') + b'\0'
        if clean[offset:offset + capacity] != raw.ljust(capacity, b'\0'):
            raise ValueError('Clean Golden Route pool ownership differs')
        pointer = struct.unpack_from('<I', current, field)[0] - BASE
        if current[pointer:current.index(0, pointer) + 1] != english.encode('ascii') + b'\0':
            raise ValueError('Inherited complete Golden Route label differs')
        golden.append({'id': 'GOLDEN_ROUTE_VIEWER_' + key, 'english': english,
                       'pointer_field': field, 'source_meaning': meaning})
    for image in (clean, canonical, current):
        if struct.unpack_from('<I', image, TABLE_LITERAL)[0] != BASE + OLD_TABLE:
            raise ValueError('Native Golden Route title-table literal differs')
        if byte_pointer_references(image, [(OLD_TABLE, OLD_TABLE + 8)]) != {TABLE_LITERAL: OLD_TABLE}:
            raise ValueError('Title table has additional literal/interior consumers')
    records = [*map_document['records'], *creatures, *golden]
    expected_refs = {TABLE_LITERAL: OLD_TABLE}
    for row in records:
        field = row['pointer_field']
        target = struct.unpack_from('<I', current, field)[0] - BASE
        if any(lo <= target < hi for lo, hi in OWNED):
            expected_refs[field] = target
    if byte_pointer_references(current, OWNED) != expected_refs:
        raise ValueError('Combined owned pool has an unmapped literal/interior consumer')
    for text, offset in SHARED.items():
        raw = text.encode('ascii') + b'\0'
        if current[offset:offset + len(raw)] != raw:
            raise ValueError('Complete existing shared text/NUL differs')
        if any(lo <= offset < hi for lo, hi in OWNED):
            raise ValueError('Shared storage overlaps reclaimed pool')
    entries = {formatted_text(row): formatted_text(row).encode('ascii') + b'\0'
               for row in records if row['english'] not in SHARED}
    offsets, unused = pack(entries, RANGES)
    proposed = bytearray(current)
    for lo, hi in OWNED:
        proposed[lo:hi] = bytes(hi - lo)
    for text, offset in offsets.items():
        proposed[offset:offset + len(entries[text])] = entries[text]
    selections = []
    for row in records:
        field = row['pointer_field']
        if field in (OLD_TABLE, OLD_TABLE + 4):
            field = NEW_TABLE + field - OLD_TABLE
        target = SHARED[row['english']] if row['english'] in SHARED else offsets[formatted_text(row)]
        struct.pack_into('<I', proposed, field, BASE + target)
        if proposed[target:proposed.index(0, target) + 1] != formatted_text(row).encode('ascii') + b'\0':
            raise ValueError('Full compiled English/guards/NUL differ')
        selections.append({'id': row['id'], 'old_pointer_field': row['pointer_field'],
                           'pointer_field': field, 'offset': target, 'english': row['english'],
                           'formatted_text': formatted_text(row)})
    struct.pack_into('<I', proposed, TABLE_LITERAL, BASE + NEW_TABLE)
    allowed = [*OWNED, (TABLE_LITERAL, TABLE_LITERAL + 4),
               *((r['pointer_field'], r['pointer_field'] + 4) for r in records)]
    if any(a != b and not any(lo <= i < hi for lo, hi in allowed)
           for i, (a, b) in enumerate(zip(current, proposed, strict=True))):
        raise ValueError('Combined allocation changes unrelated bytes')
    native_classes = [execute_class(bytes(proposed), index) for index in range(39)]
    for row in creatures:
        if native_classes[row['class_index']]['text'] != row['english']:
            raise ValueError('Native class constructor does not select complete creature English')
    report = {'status': 'complete-owned-pool-allocation-native-formatting-pending',
              'source_arm9_sha256': sha(current), 'target_arm9_sha256': sha(proposed),
              'owned_ranges': OWNED, 'string_ranges': RANGES,
              'string_capacity': sum(hi - lo for lo, hi in RANGES),
              'string_bytes': sum(map(len, entries.values())), 'unused_ranges': unused,
              'title_table': {'old': OLD_TABLE, 'new': NEW_TABLE, 'literal': TABLE_LITERAL,
                              'sole_literal_consumer_verified': True},
              'selections': selections, 'native_classes': native_classes,
              'class_source_code_locks': class_report['source_code_locks'],
              'shared_full_strings': [{'text': text, 'offset': offset,
                                       'sha256_with_nul': sha(text.encode('ascii') + b'\0')}
                                      for text, offset in SHARED.items()],
              'limitations': ['All native heading/footer/modal and tooltip pixels must be replayed after repacking.',
                             'Dynamic faction/user-name/numeric bounds, physical routing and release approval remain pending.',
                             'Literal pointer coverage does not prove indirect/Thumb/overlay ownership.']}
    return bytes(proposed), report


def main():
    images = [NdsImage.open(path).read_file('/__arm9__.bin') for path in (
        'work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds',
        'out/all_routes_combined_v139_candidate.nds')]
    proposed, report = compile_allocation(*images)
    root = Path('work/analysis/map_creature_complete_v139')
    root.mkdir(parents=True, exist_ok=True)
    (root / 'proposed_arm9.bin').write_bytes(proposed)
    (root / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"All 15 full labels/formats fit {report['string_bytes']}/{report['string_capacity']} owned string bytes; all 39 class constructors pass.")


if __name__ == '__main__':
    main()
