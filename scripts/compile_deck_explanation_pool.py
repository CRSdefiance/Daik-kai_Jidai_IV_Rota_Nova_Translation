"""Research complete aligned Deck pool relocation, preserving every inherited owner."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inventory_arm9_text import components
from scripts.probe_deck_explanation_layout import format_paragraph
from scripts.probe_deck_explanation_sources import ROWS, SOURCE


def compile_pool(image, proof):
    source = image.read_file('/__arm9__.bin')
    if sha(source) != SOURCE or proof['current_arm9_sha256'] != SOURCE:
        raise ValueError('Exact complete V145 Deck source required')
    pool = proof['adjacent_complete_owned_pool_lead']
    start, end = pool['source_span']
    if (start, end) != (0x133024, 0x133240):
        raise ValueError('Deck complete owned pool differs')
    owners = pool['owners']
    references = pool['all_byte_position_address_candidates']
    actual = []
    for name, _, raw in components(image):
        for position in range(len(raw) - 3):
            target = struct.unpack_from('<I', raw, position)[0] - 0x02000000
            if start <= target < end:
                actual.append((name, position, target))
    if actual != [(r['component'], r['field_offset'], r['target_offset']) for r in references]:
        raise ValueError('Deck byte-position reference inventory differs')
    if len(owners) != 31 or len(references) != 31:
        raise ValueError('Deck complete owner/reference set differs')
    paragraphs = {offset: english for _, offset, _, _, english, _ in ROWS}
    packed, moves = bytearray(), []
    cursor = start
    for owner in owners:
        old = owner['offset']
        capacity = owner['source_capacity']
        if old != cursor or source[old:old + capacity] != bytes.fromhex(owner['current_bytes_hex']):
            raise ValueError('Complete Deck source owners are not exact/contiguous')
        cursor += capacity
        text = format_paragraph(paragraphs[old]) if old in paragraphs else owner['current_text']
        raw = text.encode('cp932') + b'\0'
        new = start + len(packed)
        packed.extend(raw)
        packed.extend(b'\0' * (-len(packed) % 4))
        moves.append({'old_offset': old, 'new_offset': new, 'source_capacity': capacity,
                      'complete_text': text, 'bytes_including_nul': len(raw),
                      'inherited_wording_preserved': old not in paragraphs})
    if cursor != end or len(packed) > end - start:
        raise ValueError('Complete Deck prose does not fit the whole owned pool')
    saved = bytearray(source)
    saved[start:end] = packed.ljust(end - start, b'\0')
    by_old = {m['old_offset']: m for m in moves}
    for ref in references:
        field = ref['field_offset']
        if ref['component'] != 'arm9' or ref['interior_byte_offset'] or start <= field < end:
            raise ValueError('Deck reference grammar requires separate relocation handling')
        move = by_old[ref['owner_offset']]
        struct.pack_into('<I', saved, field, 0x02000000 + move['new_offset'])
    restored = bytearray(saved)
    restored[start:end] = source[start:end]
    for ref in references:
        field = ref['field_offset']
        restored[field:field + 4] = source[field:field + 4]
    if bytes(restored) != source:
        raise ValueError('Deck research relocation changes unrelated bytes')
    return bytes(saved), {'status': 'pass-research-deck-complete-aligned-pool-connected-consumers-pending',
                          'source_arm9_sha256': SOURCE, 'research_arm9_sha256': sha(saved),
                          'source_span': [start, end], 'owned_pool_bytes': end - start,
                          'used_aligned_bytes': len(packed), 'spare_bytes': end - start - len(packed),
                          'moves': moves, 'references': references,
                          'all_other_arm9_bytes_preserved': True, 'runtime_verified': False}


def main():
    image = NdsImage.open('out/all_routes_combined_v145_candidate.nds')
    proof_path = Path('work/analysis/deck_explanations_source_proof.json')
    proof = json.loads(proof_path.read_text(encoding='utf-8'))
    saved, report = compile_pool(image, proof)
    report['source_proof_sha256'] = sha(proof_path.read_bytes())
    Path('work/analysis/deck_explanations_pool_arm9.bin').write_bytes(saved)
    Path('work/analysis/deck_explanations_pool_proof.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f"Complete Deck pool uses {report['used_aligned_bytes']}/{report['owned_pool_bytes']} bytes; 31 aligned owners/references, all inherited wording preserved.")


if __name__ == '__main__':
    main()
