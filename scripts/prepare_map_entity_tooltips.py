"""Complete map tooltip localization research; no playable ROM or approval."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.compile_scene_caption_allocation import pack
from scripts.plan_grand_race_ui_allocation_v136 import byte_pointer_references

BASE = 0x02000000
SOURCE_SHA = '9a4b950d452631a6cc60721177e1f8e2b1ad778d854b6e42b11df04fdb2828a5'
RANGES = ((0x1190EC, 0x119104), (0x1478B8, 0x1478D8))
ROWS = (
    ('PIRATES', 0x1190EC, 8, 0x705EC, '海賊', 'Pirates',
     'A pirate fleet, selected when the faction resolver returns no object.'),
    ('MONSTER', 0x1190F4, 8, 0x705E8, '怪物', 'Monster',
     'A monster, selected by the special entity type 0xB5.'),
    ('UNKNOWN', 0x1190FC, 8, 0x705E0, '？？？', '???',
     'An unidentified faction/entity; preserve the question-mark label.'),
    ('CLASS', 0x1478B8, 8, 0x705F0, '%s\n%s級', '%s\n%s class',
     'Entity/faction name followed by ship class. Preserve both substitutions.'),
    ('ARMAMENT', 0x1478C0, 24, 0x705F4, '%s  %6s％\n武装度 %8s',
     '%s  %6s%%\nArmament %8s',
     'Name, six-column percentage and eight-column armament rating. Preserve all three substitutions.'),
)
CODE_RANGES = ((0x70424, 0x70498), (0x70528, 0x70590),
               (0xD7720, 0xD77B8))
SHARED = {'Monster': 0x17223D}


def formatted_text(row):
    # The paired renderer consumes a byte after LF before changing rows when
    # the preceding row has odd ASCII parity. Generate the protective blank;
    # keep it out of the editorial English. Two blanks protect both parity
    # cases: the second blank absorbs the cursor reset for an even first row.
    return row['english'].replace('\n', '\n  ') if row['id'].endswith(('CLASS', 'ARMAMENT')) else row['english']


def prepare(clean, canonical, current):
    if sha(current) != SOURCE_SHA:
        raise ValueError('Exact V139 ARM9 required')
    refs = {field: offset for _, offset, _, field, *_ in ROWS}
    records = []
    for key, offset, capacity, field, japanese, english, meaning in ROWS:
        raw = japanese.encode('cp932') + b'\0'
        for image in (clean, canonical, current):
            if image[offset:offset + capacity] != raw.ljust(capacity, b'\0'):
                raise ValueError('Map tooltip source/padding differs')
            if struct.unpack_from('<I', image, field)[0] != BASE + offset:
                raise ValueError('Map tooltip source pointer differs')
        records.append({
            'id': 'MAP_ENTITY_TOOLTIP_' + key, 'source_offset': offset,
            'source_capacity': capacity, 'pointer_field': field,
            'source_hex': raw[:-1].hex(), 'japanese': japanese, 'english': english,
            'speaker': 'Map entity tooltip', 'source_meaning': meaning,
            'context': 'Native map selection 70424:70470; class format at 70488 and armament format at 7057C, through D7720.',
            'localization_note': 'Full natural UI wording. Retain name/class/percentage/armament substitutions. ASCII percent uses native printf escape %% instead of the Japanese full-width percent glyph. The source newline separates tooltip rows; it is not an authored dialogue wrap.',
            'review': {'source': True, 'context': True, 'localization': True,
                       'naturalness': True, 'formatting': False},
        })
    for image in (clean, canonical, current):
        if byte_pointer_references(image, RANGES) != refs:
            raise ValueError('Map tooltip pool has additional literal/interior consumers')
        for lo, hi in CODE_RANGES:
            if image[lo:hi] != clean[lo:hi]:
                raise ValueError('Map tooltip consumer/printf code differs')
    for text, offset in SHARED.items():
        raw = text.encode('ascii') + b'\0'
        if current[offset:offset + len(raw)] != raw:
            raise ValueError('Existing complete shared tooltip string differs')
    entries = {formatted_text(r): formatted_text(r).encode('ascii') + b'\0'
               for r in records if r['english'] not in SHARED}
    offsets, unused = pack(entries, RANGES)
    proposed = bytearray(current)
    for lo, hi in RANGES:
        proposed[lo:hi] = bytes(hi - lo)
    for text, offset in offsets.items():
        proposed[offset:offset + len(entries[text])] = entries[text]
    for row in records:
        target = SHARED[row['english']] if row['english'] in SHARED else offsets[formatted_text(row)]
        struct.pack_into('<I', proposed, row['pointer_field'], BASE + target)
    allowed = {i for lo, hi in RANGES for i in range(lo, hi)}
    allowed.update(i for f in refs for i in range(f, f + 4))
    if any(i not in allowed for i, (a, b) in enumerate(zip(current, proposed, strict=True)) if a != b):
        raise ValueError('Map tooltip allocation changes unrelated bytes')
    document = {'format': 'dk4-map-entity-tooltip-manuscript-v2',
                'translation_policy': 'natural-dialogue-v2', 'target_locale': 'en-US',
                'status': 'source-reviewed-native-formatting-pending',
                'source_arm9_sha256': sha(current), 'clean_arm9_sha256': sha(clean),
                'records': records}
    report = {'status': 'source-locked-complete-allocation-native-rendering-pending',
              'source_arm9_sha256': sha(current), 'target_arm9_sha256': sha(proposed),
              'owned_ranges': RANGES, 'owned_bytes': sum(hi - lo for lo, hi in RANGES),
              'allocated_bytes': sum(map(len, entries.values())), 'unused_ranges': unused,
              'selections': [{'id': r['id'], 'pointer_field': r['pointer_field'],
                              'offset': SHARED[r['english']] if r['english'] in SHARED else offsets[formatted_text(r)],
                              'english': r['english'], 'formatted_text': formatted_text(r)}
                             for r in records],
              'shared_strings': [{'text': text, 'offset': offset,
                                  'full_nul_sha256': sha(text.encode('ascii') + b'\0')}
                                 for text, offset in SHARED.items()],
              'newline_policy': 'machine-generated LF-two-space guard; six-pixel native continuation indent for both ASCII parities',
              'source_code_locks': [{'start': lo, 'end': hi, 'sha256': sha(clean[lo:hi])}
                                    for lo, hi in CODE_RANGES],
              'limitations': ['No native pixel/layout approval or ROM integration.',
                              'Literal coverage does not prove indirect/Thumb/overlay ownership.',
                              'Dynamic name/class width and physical routing require verification.']}
    return document, bytes(proposed), report


def main():
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    canonical = NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/__arm9__.bin')
    current = NdsImage.open('out/all_routes_combined_v139_candidate.nds').read_file('/__arm9__.bin')
    document, proposed, report = prepare(clean, canonical, current)
    Path('translations/map_entity_tooltip_manuscript_v2.json').write_text(
        json.dumps(document, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    destination = Path('work/analysis/map_entity_tooltips_v139')
    destination.mkdir(parents=True, exist_ok=True)
    (destination / 'proposed_arm9.bin').write_bytes(proposed)
    (destination / 'report.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(f"Five complete strings fit {report['allocated_bytes']}/{report['owned_bytes']} owned bytes; formatting pending.")


if __name__ == '__main__':
    main()
