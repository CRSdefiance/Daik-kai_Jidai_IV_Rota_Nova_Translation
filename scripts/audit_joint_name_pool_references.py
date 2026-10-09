"""Inventory all-byte old name-pool address matches, including decompressed overlays."""

import json
import struct
from pathlib import Path

from ndspy.code import loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_joint_name_runtime_pool import prepare


def scan(raw, owners, known_fields=None):
    known_fields = {} if known_fields is None else known_fields
    matches = []
    cursor = 2
    while True:
        suffix = raw.find(b'\x17\x02', cursor)
        if suffix < 0:
            break
        cursor = suffix + 1
        at = suffix - 2
        pointer = struct.unpack_from('<I', raw, at)[0]
        if not 0x02171E48 <= pointer < 0x02172464:
            continue
        owner = next((o for o in owners if o['old_pointer'] <= pointer
                      < o['old_pointer'] + len(o.get('inherited_text', o['text']).encode('cp932')) + 1), None)
        kind = ('registered-field' if at in known_fields else
                'unregistered-owner-start' if owner and pointer == owner['old_pointer'] else
                'unregistered-owner-interior' if owner else 'allocation-padding-or-other-address')
        matches.append({'offset': at, 'pointer': pointer, 'classification': kind,
                        'owner': owner, 'registered_record': known_fields.get(at)})
    return matches


def main():
    image = NdsImage.open('out/all_routes_combined_v147_candidate.nds')
    source = image.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    saved, _, _, moves, owners = prepare(source, clean)
    known = {m['field']: m['id'] for m in moves}
    before = scan(source, owners, known)
    after = scan(saved, owners)
    exceptions = {
        0x436A3: (0x436A0, 0x436A8, 'Unaligned match across native MOV r4,r0 and BL CD330 instruction words.'),
        0x134173: (0x134170, 0x134178, 'Unaligned match across preserved words 02021714 and 02021720; not a name pointer.'),
    }
    if {m['offset'] for m in after} != set(exceptions):
        raise ValueError('Unclassified residual old-pool address match')
    for match in after:
        begin, end, explanation = exceptions[match['offset']]
        if saved[begin:end] != clean[begin:end]:
            raise ValueError('Residual nonpointer context differs from clean source')
        match['classification'] = 'source-identical-cross-word-nonpointer'
        match['classification_evidence'] = {'begin': begin, 'end': end,
                                            'source_hex': clean[begin:end].hex(),
                                            'explanation': explanation}
    if sum(m['classification'] == 'registered-field' for m in before) != 239:
        raise ValueError('Registered reference count differs')
    overlays = loadOverlayTable(image.rom.arm9OverlayTable, lambda oid, fid: image.files[fid])
    overlay_matches = []
    for index, overlay in sorted(overlays.items()):
        for match in scan(bytes(overlay.data), owners):
            overlay_matches.append({'overlay_id': index, 'ram_base': overlay.ramAddress, **match})
    result = {'status': 'pass-all-byte-known-owner-reference-inventory',
              'source_sha256': sha(source), 'research_sha256': sha(saved),
              'source_arm9_matches': before, 'repaired_arm9_matches': after,
              'decompressed_overlay_matches': overlay_matches, 'overlays_scanned': len(overlays),
              'limits': ['Raw address matches may be code, runtime globals or data; classify before rewriting.',
                         'Computed pointers, mutable copies and runtime writes are not proven by a static address scan.',
                         'Original string starts/interiors are derived from batch-owned complete text, not guessed zero padding.']}
    Path('work/analysis/joint_name_pool_reference_inventory.json').write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'239 registered references; {len(after)} residual ARM9 address matches; {len(overlay_matches)} decompressed overlay matches across {len(overlays)} overlays.')
    for match in after:
        print(f"{match['offset']:06X}: {match['pointer']:08X} {match['classification']}")


if __name__ == '__main__':
    main()
