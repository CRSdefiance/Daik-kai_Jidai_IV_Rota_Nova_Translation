"""Lossless caption allocation research; never build a playable ROM."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.execute_grand_race_waiting_widgets import TABLE
from scripts.execute_grand_race_waiting_widgets import execute as execute_widgets
from scripts.inventory_common_scene_caption_duplicates import CURRENT, CURRENT_SHA
from scripts.plan_grand_race_ui_allocation_v136 import byte_pointer_references, merge_ranges
from scripts.plan_scene_caption_source_pool import inspect_pool

BRANCH, POOL_START, POOL_END = 0xF8540, 0xF8544, 0xF8584
SHARED = {'Church': 0x156AB4, 'Hayreddin': 0x15D8B4, 'Maria': 0x15C030}


def pack(entries, ranges):
    """Fill smaller bins using exact subset sums, preserving every full string."""
    remaining = dict(entries)
    offsets, unused = {}, []
    for lo, hi in sorted(ranges, key=lambda span: (span[1] - span[0], span[0])):
        choices = {0: []}
        for key in sorted(remaining, key=lambda key: (-len(remaining[key]), key)):
            size = len(remaining[key])
            for total, selected in list(choices.items()):
                if total + size <= hi - lo and total + size not in choices:
                    choices[total + size] = selected + [key]
        for key in choices[max(choices)]:
            offsets[key] = lo
            lo += len(remaining.pop(key))
        if lo < hi:
            unused.append([lo, hi])
    if remaining:
        raise ValueError('Complete caption strings do not fit; no shortened fallback permitted')
    return offsets, unused


def compile_allocation(document, clean, canonical, current):
    if len(document['records']) != 164:
        raise ValueError('Every complete caption is required')
    pool = inspect_pool(document, clean, canonical, current)
    if pool['additional_literal_pointer_fields_requiring_consumer_review']:
        raise ValueError('Caption pool has unmapped literal consumers')
    if current[BRANCH:POOL_END] != struct.pack('<I', 0xE1A00000) * 17:
        raise ValueError('Guarded pool must be the exact redundant initializer NOPs')
    if byte_pointer_references(current, [(POOL_START, POOL_END)]):
        raise ValueError('Initializer spare region has another literal pointer consumer')
    incoming = []
    for field in range(0, len(current) - 3, 4):
        word = struct.unpack_from('<I', current, field)[0]
        if word >> 28 != 15 and word & 0x0E000000 == 0x0A000000:
            displacement = word & 0xFFFFFF
            if displacement & 0x800000:
                displacement -= 0x1000000
            target = field + 8 + displacement * 4
            if POOL_START <= target < POOL_END:
                incoming.append(field)
    if incoming:
        raise ValueError('Initializer spare region has a direct branch entrance')
    for text, offset in SHARED.items():
        raw = text.encode('ascii') + b'\0'
        if any(source[offset:offset + len(raw)] != raw for source in (canonical, current)):
            raise ValueError('Complete shared label differs from accepted canonical storage')
    texts = {row['english'] for row in document['records']} - {'Ironclad', *SHARED, 'Bianca'}
    raw_text = {text: text.encode('ascii') + b'\0' for text in texts}
    ranges = merge_ranges([*pool['owned_ranges'], [POOL_START, POOL_END]])
    offsets, unused = pack(raw_text, ranges)
    proposed = bytearray(current)
    for lo, hi in ranges:
        proposed[lo:hi] = bytes(hi - lo)
    for text, offset in offsets.items():
        proposed[offset:offset + len(raw_text[text])] = raw_text[text]
    # One unconditional branch skips the complete data island; no widget setup
    # instructions are omitted because these seventeen source words were NOPs.
    instruction = 0xEA000000 | ((POOL_END - BRANCH - 8) // 4)
    struct.pack_into('<I', proposed, BRANCH, instruction)
    selections = {**offsets, **SHARED}
    selections['Bianca'] = offsets['Angelo and Bianca'] + len('Angelo and ')
    pointers = []
    for row in document['records']:
        field = row['pointer_field']
        pointer = (struct.unpack_from('<I', current, field)[0] if row['english'] == 'Ironclad'
                   else 0x02000000 + selections[row['english']])
        struct.pack_into('<I', proposed, field, pointer)
        offset = pointer - 0x02000000
        expected = row['english'].encode('ascii') + b'\0'
        if proposed[offset:proposed.index(0, offset) + 1] != expected:
            raise ValueError('Saved complete caption loses leading/last characters or NUL')
        pointers.append({'id': row['id'], 'field': field, 'offset': offset, 'english': row['english']})
    widget_pointers = struct.unpack_from('<3I', current, TABLE)
    before = execute_widgets(current, widget_pointers, scratch_table=False)
    after = execute_widgets(proposed, widget_pointers, scratch_table=False)
    # The data-skipping branch changes the instruction count, preserving all
    # native constructors, linked records, following objects and caller state.
    for key in before.keys() | after.keys():
        if key != 'steps' and before.get(key) != after.get(key):
            raise ValueError(f'Caption island changes native waiting widget state: {key}')
    if before['steps'] - after['steps'] != 16:
        raise ValueError('Guarded caption branch did not replace exactly seventeen NOP steps')
    allowed = ranges + [(BRANCH, BRANCH + 4)] + [(row['field'], row['field'] + 4) for row in pointers]
    changed = [offset for offset, (old, new) in enumerate(zip(current, proposed, strict=True)) if old != new]
    if any(not any(lo <= offset < hi for lo, hi in allowed) for offset in changed):
        raise ValueError('Caption proposal changed unrelated bytes')
    return bytes(proposed), {
        'caption_count': 164, 'complete_selections': pointers,
        'owned_ranges': ranges, 'unused_ranges': unused, 'changed_bytes': len(changed),
        'shared_canonical_labels': SHARED, 'complete_bianca_suffix_shared': True,
        'guarded_initializer_data_bytes': 64, 'direct_entrances_into_data': incoming,
        'waiting_widget_before': before, 'waiting_widget_after': after,
        'retired_Ironclad_source_slot_unchanged': current[0x138984:0x13898C] == proposed[0x138984:0x13898C],
        'over_screen_width_pending': pool['over_screen_width']}


def main():
    if sha(CURRENT.read_bytes()) != CURRENT_SHA:
        raise ValueError('Pinned combined candidate differs')
    path = Path('translations/scene_caption_manuscript_v2.json')
    document = json.loads(path.read_text(encoding='utf-8'))
    clean, canonical, current = [NdsImage.open(path).read_file('/__arm9__.bin') for path in (
        'work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds', CURRENT)]
    proposed, report = compile_allocation(document, clean, canonical, current)
    report.update({'status': 'complete-caption-allocation-research-layout-and-release-gates-pending',
                   'candidate_sha256': CURRENT_SHA, 'manuscript_sha256': sha(path.read_bytes()),
                   'proposed_arm9_sha256': sha(proposed), 'rom_written': False, 'runtime_verified': False,
                   'limitations': ['All captions fit intact; 264-pixel caption still requires native layout.',
                                   'Guarded initializer execution preserves mapped native widget state; full gameplay and indirect/Thumb coverage pending.',
                                   'Strict staged source/dependency/ownership release component and registration pending.']})
    output = Path('work/analysis/scene_caption_complete_allocation_v137')
    output.mkdir(parents=True, exist_ok=True)
    (output / 'proposed_arm9.bin').write_bytes(proposed)
    (output / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    print('All 164 complete captions fit; 64-byte guarded data island preserves waiting widgets; layout/release gates pending.')


if __name__ == '__main__':
    main()
