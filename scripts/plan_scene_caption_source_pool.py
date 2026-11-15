"""Inventory complete caption storage/pointer ownership before any relocation."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inventory_common_scene_caption_duplicates import CURRENT, CURRENT_SHA
from scripts.plan_grand_race_ui_allocation_v136 import byte_pointer_references, merge_ranges


def inspect_pool(manuscript, clean, canonical, current):
    ranges, slots = [], []
    expected = {row['pointer_field']: row['source_offset'] for row in manuscript['records']}
    for row in manuscript['records']:
        lo, raw = row['source_offset'], bytes.fromhex(row['source_hex'])
        capacity = (len(raw) + 4) // 4 * 4
        original = raw.ljust(capacity, b'\0')
        if lo % 4 or clean[lo:lo + capacity] != original:
            raise ValueError('Caption source/padding ownership differs')
        pointer = struct.unpack_from('<I', current, row['pointer_field'])[0] - 0x02000000
        # Ironclad already has a separately owned terminated English pointer;
        # its old eight-byte storage was filled without a NUL by an older layer.
        reserved = row['english'] == 'Ironclad'
        if not reserved and (canonical[lo:lo + capacity] != original or current[lo:lo + capacity] != original):
            raise ValueError('Caption pool includes changed or unverified inherited storage')
        if not reserved and pointer != lo:
            raise ValueError('Caption consumer was retargeted outside reviewed source')
        if reserved and current[pointer:current.index(0, pointer)].decode('ascii') != 'Ironclad':
            raise ValueError('Complete inherited Ironclad pointer differs')
        slots.append({'id': row['id'], 'start': lo, 'end': lo + capacity,
                      'source_hex': original.hex(), 'canonical_hex': canonical[lo:lo + capacity].hex(),
                      'current_hex': current[lo:lo + capacity].hex(), 'reserved_inherited_name': reserved})
        if not reserved:
            ranges.append((lo, lo + capacity))
    owned = merge_ranges(ranges)
    references = byte_pointer_references(clean, owned)
    caption_refs = {field: target for field, target in references.items() if field in expected}
    if any(expected[field] != target for field, target in caption_refs.items()):
        raise ValueError('Caption source pointer has a different original selection')
    other = {field: target for field, target in references.items() if field not in expected}
    english = {row['english'] for row in manuscript['records'] if row['english'] != 'Ironclad'}
    total = sum(len(text) + 1 for text in english)
    capacity = sum(hi - lo for lo, hi in owned)
    existing = {}
    for text in sorted(english):
        raw, hits, at = text.encode('ascii') + b'\0', [], 0
        while (at := current.find(raw, at)) >= 0:
            if not any(lo <= at < hi for lo, hi in owned):
                hits.append(at)
            at += 1
        if hits:
            existing[text] = hits
    return {'slots': slots, 'owned_ranges': owned, 'owned_capacity': capacity,
            'complete_unique_english_bytes_with_nul': total,
            'raw_capacity_deficit_before_external_sharing': max(0, total - capacity),
            'mapped_caption_pointer_fields': caption_refs,
            'additional_literal_pointer_fields_requiring_consumer_review': other,
            'existing_complete_english_candidates_not_yet_approved_dependencies': existing,
            'over_screen_width': [{'id': row['id'], 'english': row['english'],
                                   'width_pixels': row['native_centering_width_pixels']}
                                  for row in manuscript['records'] if row['native_centering_width_pixels'] > 256]}


def main():
    if sha(CURRENT.read_bytes()) != CURRENT_SHA:
        raise ValueError('Pinned candidate differs')
    manuscript_path = Path('translations/scene_caption_manuscript_v2.json')
    document = json.loads(manuscript_path.read_text(encoding='utf-8'))
    sources = [NdsImage.open(path).read_file('/__arm9__.bin') for path in (
        'work/clean.nds', 'out/raphael_natural_v2_accepted_base.nds', CURRENT)]
    if sha(sources[0]) != document['source_arm9_sha256']:
        raise ValueError('Clean caption source differs')
    report = inspect_pool(document, *sources)
    report.update({'status': 'full-caption-source-pool-ownership-inventory-relocation-pending',
                   'manuscript_sha256': sha(manuscript_path.read_bytes()),
                   'candidate_sha256': CURRENT_SHA, 'rom_written': False,
                   'limitations': ['Literal pointer scan includes every byte position, unaligned and interior targets.',
                                   'Computed/Thumb/overlay consumers remain a separate coverage requirement.',
                                   'Existing complete English candidates require source-locked owning dependencies before sharing.',
                                   'Complete English is retained; capacity/width deficits are not permission to drop scene information.']})
    output = Path('work/analysis/scene_caption_source_pool_v137.json')
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(f"Caption pool: {report['owned_capacity']} owned bytes / {report['complete_unique_english_bytes_with_nul']} full English bytes; {len(report['additional_literal_pointer_fields_requiring_consumer_review'])} additional literal consumers; {len(report['over_screen_width'])} wider-than-screen label.")


if __name__ == '__main__':
    main()
