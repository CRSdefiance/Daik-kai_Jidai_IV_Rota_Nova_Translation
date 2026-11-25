"""Reconcile remaining COMMON text with the four native scene-caption arrays.

An inline caption consumer does not prove that its separate COMMON copy is unused.
"""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries

BASE = 0x02000000
CLEAN_SHA = '0d1541022ef95afe02ad7a1a381a1fc3e5e74442a5f0408f436d68a5d306d731'
CURRENT = Path('out/all_routes_combined_v137_candidate.nds')
CURRENT_SHA = '985c99f003a975d7512c249f09a13008f19ed15bb5f533d5c8f1747e6bca19fb'
ROOTS = ((0, 0x432E0, 0x115CAC), (1, 0x432E8, 0x115A04),
         (2, 0x432F0, 0x115968), (3, 0x432F8, 0x115834))


def captions(source):
    if sha(source) != CLEAN_SHA:
        raise ValueError('Clean scene-caption source differs')
    rows = []
    for route, literal, start in ROOTS:
        if struct.unpack_from('<I', source, literal)[0] != BASE + start:
            raise ValueError('Native route caption root differs')
        field = start
        # Lil's caption array directly precedes Hodram's caption array, with no
        # numeric/sentinel separator. The next independently referenced root is
        # an ownership boundary even when its first word is another valid pointer.
        next_root = min((lo for _, _, lo in ROOTS if lo > start), default=len(source))
        while field < next_root and 0x02130000 <= (pointer := struct.unpack_from('<I', source, field)[0]) < 0x02140000:
            offset = pointer - BASE
            raw = source[offset:source.index(0, offset)]
            if not raw:
                raise ValueError('Caption cannot be empty')
            rows.append({'route_index': route, 'index': (field - start) // 4,
                         'root_literal': literal, 'table_start': start,
                         'pointer_field': field, 'offset': offset,
                         'source_hex': raw.hex(), 'japanese': raw.decode('cp932')})
            field += 4
            if field - start > 256 * 4:
                raise ValueError('Caption table lacks a bounded terminator')
    return rows


def inventory(source, current, entries):
    rows = captions(source)
    for row in rows:
        field = row['pointer_field']
        pointer = struct.unpack_from('<I', current, field)[0]
        if not BASE <= pointer < BASE + len(current):
            raise ValueError('Current caption pointer escapes ARM9')
        offset = pointer - BASE
        row['current_offset'] = offset
        raw = current[offset:current.index(0, offset)]
        row['current_hex'] = raw.hex()
        row['current_text'] = raw.decode('cp932')
        row['changed_from_clean'] = raw != bytes.fromhex(row['source_hex'])
        row['exact_remaining_common_ids'] = [e.message_id for e in entries[3393:3607] if e.text == bytes.fromhex(row['source_hex'])]
    selection_rows = []
    for entry in [*entries[3289:3320], *entries[3393:3607]]:
        needle = entry.text + b'\0'
        hits, position = [], 0
        while (position := source.find(needle, position)) >= 0:
            hits.append(position)
            position += 1
        selection_rows.append({'message_id': entry.message_id, 'block': entry.block,
                               'record': entry.record_index, 'source_hex': entry.text.hex(),
                               'japanese': entry.text.decode('cp932'), 'exact_inline_offsets': hits,
                               'mapped_caption_fields': [row['pointer_field'] for row in rows
                                                        if entry.message_id in row['exact_remaining_common_ids']],
                               'common_consumer_verified': False})
    return rows, selection_rows


def main():
    if sha(CURRENT.read_bytes()) != CURRENT_SHA:
        raise ValueError('Pinned combined candidate differs')
    clean = NdsImage.open('work/clean.nds')
    source = clean.read_file('/__arm9__.bin')
    entries = common_message_entries(clean.read_file('/COMMON/MESFILE.DK4'), source)
    current = NdsImage.open(CURRENT).read_file('/__arm9__.bin')
    rows, selections = inventory(source, current, entries)
    report = {'status': 'mapped-inline-scene-caption-tables-common-consumers-pending',
              'clean_arm9_sha256': sha(source), 'candidate_sha256': CURRENT_SHA,
              'candidate_arm9_sha256': sha(current),
              'caption_count': len(rows),
              'route_caption_counts': {str(route): sum(row['route_index'] == route for row in rows) for route in range(4)},
              'remaining_common_selection_count': len(selections),
              'exact_inline_duplicate_count': sum(bool(row['exact_inline_offsets']) for row in selections),
              'mapped_caption_common_selection_count': sum(bool(row['mapped_caption_fields']) for row in selections),
              'captions': rows, 'remaining_common_selections': selections,
              'consumer': {'route_guard': [0x42E30, 0x42E40], 'route_dispatch': [0x42E5C, 0x42ED4],
                           'selected_caption': [0x42FD0, 0x4300C], 'wrapper': [0x456A0, 0x4570C],
                           'width_calculation': 'native strlen * 6, centered around x128',
                           'renderer': 'D5404 via draw-local D5160 initialization; canonical renderer retained',
                           'caption_y': 70,
                           'native_count_initialization': [0x42C74, 0x42C94],
                           'native_count_fields': {'0': [0x2C, 46], '1': [0x30, 41],
                                                   '2': [0x34, 39], '3': [0x38, 38]},
                           'native_y_initialization': [0x42C44, 0x42C4C]},
              'limitations': ['Exact inline duplicates and caption consumers do not establish COMMON visibility or nonuse.',
                             'Nonpointer words/next roots bound source arrays and native count initialization agrees; keyboard/navigation/index loop execution is pending.',
                             'Caption y/font/extent/fullscreen and gameplay remain pending; no translation integration credit.']}
    report['consumer']['source_span_locks'] = [
        {'start': lo, 'end': hi, 'sha256': sha(source[lo:hi]),
         'canonical_sha256': sha(NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/__arm9__.bin')[lo:hi])}
        for lo, hi in ((0x42C44, 0x42C4C), (0x42C74, 0x42C94),
                       (0x42E30, 0x42ED4), (0x42FD0, 0x4300C), (0x456A0, 0x4570C))]
    output = Path('work/analysis/common_scene_caption_duplicates_v137.json')
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"Mapped {len(rows)} captions across four routes; {report['mapped_caption_common_selection_count']} remaining COMMON selections match mapped captions; {report['exact_inline_duplicate_count']} have exact inline duplicates.")


if __name__ == '__main__':
    main()
