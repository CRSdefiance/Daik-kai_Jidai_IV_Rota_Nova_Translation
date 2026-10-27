"""Audit prior/current direct references to the separately reserved name section."""

import json
import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.audit_joint_name_pool_references import scan


def matches(raw, begin, end):
    result, cursor = [], 2
    while True:
        at = raw.find(b'\x38\x02', cursor)
        if at < 0:
            break
        cursor = at + 1
        field = at - 2
        pointer = struct.unpack_from('<I', raw, field)[0]
        if begin <= pointer < end:
            result.append({'field': field, 'pointer': pointer})
    return result


def main():
    before = NdsImage.open('out/all_routes_combined_v147_candidate.nds')
    clean = NdsImage.open('work/clean.nds')
    saved = Path('work/analysis/persistent_name_section_arm9.bin').read_bytes()
    proof = json.loads(Path('work/analysis/persistent_name_section_proof.json').read_text(encoding='utf-8'))
    consumers = json.loads(Path('work/analysis/persistent_name_consumers_proof.json').read_text(encoding='utf-8'))
    if sha(saved) != proof['research_sha256'] or sha(saved) != consumers['research_sha256']:
        raise ValueError('Exact persistent section and repeated consumers required')
    begin, end = proof['placement']['base'], proof['placement']['heap_low']
    code = MainCodeFile(saved, 0x02000000)
    bss_end_field = code.codeSettingsOffs + 16
    prior = []
    for label, image in (('clean', clean), ('v147', before)):
        raw = image.read_file('/__arm9__.bin')
        found = matches(raw, begin, end)
        if {(r['field'], r['pointer']) for r in found} != {(bss_end_field, begin), (0xE45DC, begin)}:
            raise ValueError('Prior reserved-range reference ownership changed')
        prior.append({'source': label, 'matches': found})
    registered = {move['field']: move for move in proof['placement']['moves']}
    directory_field = struct.unpack_from('<I', saved, code.codeSettingsOffs + 4)[0] - 0x02000000 - 12
    found = matches(saved, begin, end)
    for ref in found:
        at, pointer = ref['field'], ref['pointer']
        if at in registered:
            old = registered[at]['runtime_pointer']
            if pointer != begin + old - 0x027E0000:
                raise ValueError('Registered current name pointer differs')
            ref['classification'] = 'complete-registered-name-owner'
        elif at == bss_end_field and pointer == begin:
            ref['classification'] = 'unchanged-exclusive-bss-clear-end'
        elif at == directory_field and pointer == begin:
            ref['classification'] = 'new-sdk-autoload-section-destination'
        else:
            raise ValueError('Unclassified pointer into reserved name section')
    if sum(r['classification'] == 'complete-registered-name-owner' for r in found) != 239:
        raise ValueError('Current complete-owner count differs')
    overlays = loadOverlayTable(before.rom.arm9OverlayTable, lambda oid, fid: before.files[fid])
    overlay_matches = {str(i): matches(bytes(o.data), begin, end) for i, o in overlays.items()}
    if any(overlay_matches.values()):
        raise ValueError('Unclassified overlay reserved-range reference')
    legacy = scan(saved, consumers['complete_string_owners'])
    if {r['offset'] for r in legacy} != {0x436A3, 0x134173}:
        raise ValueError('Unclassified legacy pool reference remains')
    for begin_at, end_at in ((0x436A0, 0x436A8), (0x134170, 0x134178)):
        if saved[begin_at:end_at] != clean.read_file('/__arm9__.bin')[begin_at:end_at]:
            raise ValueError('Legacy cross-word nonpointer context changed')
    report = {'status': 'pass-direct-reference-ownership-persistent-section',
              'research_sha256': sha(saved), 'prior_arm9_references': prior,
              'current_arm9_references': found, 'decompressed_overlay_references': overlay_matches,
              'legacy_cross_word_nonpointer_matches': legacy, 'candidate_changed': False,
              'limits': ['Direct all-byte reference ownership is proven; computed pointers and all physical runtime paths are not enumerated.']}
    Path('work/analysis/persistent_name_reference_proof.json').write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print('239 complete name references plus BSS/autoload metadata classified; no overlay or unexplained legacy address matches.')


if __name__ == '__main__':
    main()
