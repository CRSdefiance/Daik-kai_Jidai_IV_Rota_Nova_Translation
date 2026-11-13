"""Research full fleet names in two already proved source-owned allocations."""

import json
import struct
from pathlib import Path

from dk4tool.patch.available_companions_release import apply_release
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inventory_arm9_text import components
from scripts.probe_available_companions import empty_branch, parenthesized_format
from scripts.probe_fleet_name_sources import SOURCE, getter
from scripts.probe_options_narrow_prompts import execute, respond


def main():
    image = NdsImage.open('out/all_routes_combined_v147_candidate.nds')
    source = image.read_file('/__arm9__.bin')
    parent = NdsImage.open('out/all_routes_combined_v146_candidate.nds').read_file('/__arm9__.bin')
    inherited, _ = apply_release(parent, 'translations/available_companions_release_v1.json')
    if source != inherited or sha(source) != SOURCE:
        raise ValueError('Exact complete reviewed V147 source required')
    # Companion pool occupies 108 of its 136 original owned bytes, leaving 28.
    spare, spare_end = 0x138878, 0x138894
    old, old_end = 0x135260, 0x135270
    if any(source[spare:spare_end]):
        raise ValueError('Reviewed companion pool spare bytes changed')
    refs = []
    for name, _, raw in components(image):
        for p in range(len(raw) - 3):
            target = struct.unpack_from('<I', raw, p)[0] - 0x02000000
            if old <= target < old_end or spare <= target < spare_end:
                refs.append((name, p, target))
    if refs != [('arm9', 0x36B54, old)]:
        raise ValueError('Relocation target has unclassified/interior address references')
    saved = bytearray(source)
    pirate, unidentified = b'Pirate %s\0', b'Unidentified fleet\0'
    saved[old:old_end] = pirate.ljust(16, b'\0')
    saved[spare:spare_end] = unidentified.ljust(28, b'\0')
    struct.pack_into('<I', saved, 0x36B54, 0x02000000 + spare)
    struct.pack_into('<I', saved, 0x36B58, 0x02000000 + old)
    restored = bytearray(saved)
    for a, b in ((old, old_end), (spare, spare_end), (0x36B54, 0x36B5C)):
        restored[a:b] = source[a:b]
    if restored != source:
        raise ValueError('Fleet relocation changes unrelated bytes')
    saved = bytes(saved)
    cases = [getter(saved, unidentified='Unidentified fleet')]
    cases += [getter(saved, name, pirate='Pirate ', ring_index=index)
              for index in range(32) for name in ('', 'A', 'Even', 'Fleet', '海', 'Indigo海')]
    companion = empty_branch(saved)
    options = [execute(saved, kind, flags) for kind in ('sailing', 'reports')
               for flags in (0, 1, 2, 3, 255)]
    responses = [respond(saved, kind, flags, accepted) for kind in ('sailing', 'reports')
                 for flags in (0, 1, 2, 3, 255) for accepted in (False, True)]
    names = [parenthesized_format(saved, name) for name in ('', 'A', 'Even', 'Fleet', '海', 'Indigo海')]
    proof = {'status': 'pass-research-full-fleet-name-relocation-display-pending',
             'source_arm9_sha256': sha(source), 'research_arm9_sha256': sha(saved),
             'native_cases': cases, 'complete_native_case_count': len(cases),
             'inherited_companion_case': companion, 'inherited_options_cases': options,
             'inherited_options_responses': responses, 'inherited_parenthesized_cases': names,
             'allocations': [{'start': old, 'end': old_end, 'complete_text': 'Pirate %s'},
                             {'start': spare, 'end': spare_end, 'complete_text': 'Unidentified fleet'}],
             'address_candidates_in_reused_allocations': refs,
             'inherited_companion_pool_strings_preserved': True,
             'inherited_ordinary_fleet_format_preserved': True,
             'all_other_arm9_bytes_preserved': True, 'candidate_changed': False,
             'limits': ['Native branch inputs and captain names are fixtures.',
                        'All 32 ring indices execute for six names; actual name bounds and lifetime remain open.',
                        'Actual display callers/raster and physical gameplay are not verified.',
                        'Formatting approval and strict integrated release remain pending.']}
    Path('work/analysis/fleet_name_relocated_arm9.bin').write_bytes(saved)
    Path('work/analysis/fleet_name_relocation_proof.json').write_text(json.dumps(proof, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Full English fleet names relocated without ARM9 growth; {len(cases)} actual native getter/formatter cases pass.')


if __name__ == '__main__':
    main()
