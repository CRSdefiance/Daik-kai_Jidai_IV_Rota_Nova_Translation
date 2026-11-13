"""Lock the nine native race-help selections and their traced ARM draw paths."""

import hashlib
import json
import struct
from pathlib import Path

from dk4tool.rom.nds import NdsImage

BASE = 0x02000000
GROUPS = ((0x1152A8, (0x1152CC,)),
          (0x11530C, (0x1152DC, 0x1152B4, 0x1152D4, 0x1152EC)),
          (0x1152E4, (0x1152C4, 0x1152BC)),
          (0x115304, (0x1152AC, 0x1152FC)))
SPANS = ((0x3E8E8, 0x3EA04), (0x3F190, 0x3F3DC),
         (0x3F51C, 0x3F758), (0xD4DA8, 0xD4FC8),
         (0xD5070, 0xD51AC), (0xD5404, 0xD5824),
         (0xD596C, 0xD5AF8), (0x1603E4, 0x160408),
         (0x5CA8, 0x5D34), (0xD1AAC, 0xD1ACC), (0xD1B14, 0xD1B3C),
         (0x10E120, 0x10E154), (0x3E4D8, 0x3E6D0),
         (0x3EA38, 0x3EA54), (0xD43B0, 0xD4440),
         (0xD3A1C, 0xD3A7C), (0xD4A7C, 0xD4B88), (0x160360, 0x160384))


def word(data, offset):
    return struct.unpack_from('<I', data, offset)[0]


def branch(data, offset, expected):
    instruction = word(data, offset)
    if instruction >> 24 != 0xEB:
        raise ValueError(f'Expected unconditional ARM BL at {offset:#x}')
    displacement = instruction & 0xFFFFFF
    if displacement & 0x800000:
        displacement -= 0x1000000
    target = BASE + offset + 8 + displacement * 4
    if target != BASE + expected:
        raise ValueError(f'Wrong draw target at {offset:#x}')


def main():
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    baseline_path = Path('out/raphael_natural_v2_accepted_base.nds')
    if hashlib.sha256(baseline_path.read_bytes()).hexdigest() != '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe':
        raise ValueError('Canonical accepted baseline changed')
    baseline = NdsImage.open(baseline_path).read_file('/__arm9__.bin')
    current = NdsImage.open('out/all_routes_combined_v133_candidate.nds').read_file('/__arm9__.bin')
    manuscript = json.loads(Path('translations/grand_race_rules_manuscript_v2.json').read_text(encoding='utf-8'))
    locks = []
    for start, end in SPANS:
        if baseline[start:end] != current[start:end]:
            raise ValueError(f'Traced code/context changed at {start:#x}')
        locks.append({'start': start, 'end': end,
                      'source_sha256': hashlib.sha256(clean[start:end]).hexdigest(),
                      'accepted_and_current_sha256': hashlib.sha256(current[start:end]).hexdigest(),
                      'clean_to_accepted_changed_bytes': sum(a != b for a, b in zip(clean[start:end], current[start:end], strict=True))})
    selections = []
    for index, (table, descriptors) in enumerate(GROUPS):
        offset = 0x115334 + index * 8
        if (word(clean, offset), word(clean, offset + 4)) != (BASE + table, len(descriptors)):
            raise ValueError('Help group pointer/count differs')
        for page, descriptor in enumerate(descriptors):
            if word(clean, table + page * 4) != BASE + descriptor:
                raise ValueError('Help page pointer differs')
            row = next(r for r in manuscript['records'] if r['descriptor_offset'] == descriptor)
            if word(clean, descriptor + 4) != BASE + row['source_offset']:
                raise ValueError('Help body pointer differs')
            raw = bytes.fromhex(row['source_hex'])
            start = row['source_offset']
            if clean[start:start + len(raw)] != raw or current[start:start + len(raw)] != raw:
                raise ValueError('Complete source body differs')
            selections.append({'group': index, 'page': page, 'descriptor': descriptor,
                               'body': start, 'id': row['id']})
    if len(selections) != 9 or len({r['descriptor'] for r in selections}) != 9:
        raise ValueError('Help selection coverage differs')
    if clean[0x1152A8:0x115354] != current[0x1152A8:0x115354]:
        raise ValueError('Grouped descriptor region changed')
    for offset, target in ((0x3E974, 0xD5160), (0x3E9A8, 0xD5404), (0x3E9E0, 0xD5404),
                           (0x3F32C, 0xD5160), (0x3F360, 0xD5404), (0x3F398, 0xD5404),
                           (0x3F5C4, 0xD5160), (0x3F5F8, 0xD5404), (0x3F630, 0xD5404),
                           (0x3F6C8, 0xD5160), (0x3F6FC, 0xD5404), (0x3F734, 0xD5404),
                           (0xD5500, 0xD596C), (0x5CC8, 0xD1AAC),
                           (0x10E12C, 0xD1B14), (0x3E6A0, 0x3EA38),
                           (0x3E5F0, 0xD43D4), (0xD43C4, 0xD3A1C)):
        branch(current, offset, target)
    refs = []
    for offset in range(0, len(clean) - 3, 4):
        value = word(clean, offset) - BASE
        if 0x137B90 <= value < 0x138294:
            refs.append({'pointer_word': offset, 'target': value})
    expected = {(r['descriptor'] + 4, r['body']) for r in selections}
    if {(r['pointer_word'], r['target']) for r in refs} != expected:
        raise ValueError('Additional aligned references into race body region')
    report = {'status': 'static-consumer-mapped-formatting-and-runtime-pending',
              'candidate': 'out/all_routes_combined_v133_candidate.nds',
              'source_arm9_sha256': hashlib.sha256(clean).hexdigest(),
              'candidate_arm9_sha256': hashlib.sha256(current).hexdigest(),
              'code_locks': locks, 'selections': selections,
              'aligned_body_region_references': refs,
              'draw_paths': {'initial': 0x3F190, 'direct_page': 0x3E8E8,
                             'previous_and_next': 0x3F51C,
                             'context': 0xD5160, 'draw': 0xD5404},
              'body_cursor': {'x': 0, 'y': 12},
              'font_metrics': {'ascii_width': 6, 'line_height': 12,
                               'startup_setter_call': 0x5CC8,
                               'constructor_call': 0x10E12C},
              'widget_bounds': {'width': 252, 'height': 108,
                                'dimension_constructor': 0x3EA38,
                                'dimension_to_widget': 0xD3A1C,
                                'rectangle_copy': 0xD4A7C},
              'ASCII_behavior': 'Each byte advances once; glyph backend queues the first ASCII byte and flushes pairs. LF changes cursor without flushing that queue. The accepted newline/cursor repair is inherited exactly; formatting must account for both its guard behavior and pair phase.',
              'limitations': ['Aligned ARM9 references are exhaustive only for that reference grammar.',
                              'Startup metrics and widget dimensions are statically mapped; live confirmation remains pending.',
                              'Safe automatic wrapping and ASCII pair phase require a dedicated formatter.',
                              'No playable batch, ROM change or formatting approval.']}
    out = Path('work/analysis/grand_race_help_consumer_proof.json')
    out.write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'status': report['status'], 'pages': len(selections),
                      'aligned_body_references': len(refs), 'code_locks': len(locks)}))


if __name__ == '__main__':
    main()
