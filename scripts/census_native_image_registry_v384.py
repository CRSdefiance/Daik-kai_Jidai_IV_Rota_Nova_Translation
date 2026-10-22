"""Inventory real initialized PXL owners feeding the generic cached-file path."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import machine
from scripts.research_online_loader_v190 import resource_call

ROOT = Path('work/analysis/legacy_archive_access_v384')
ROM = Path('out/all_routes_combined_v383_candidate.nds')


def main():
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for lo, hi in [(0x10E190, 0x11182C), (0x111A90, 0x1123D0), (0xD6590, 0xD65B0)]:
        assert arm[lo:hi] == clean[lo:hi]
    u = machine(arm)
    primary = resource_call(u, 0x10E190, ())
    online = resource_call(u, 0x111A90, ())
    memory = bytes(u.mem_read(0x02000000, 0x400000))
    owners = []
    paths = {name.casefold(): name for _, name, _ in rom.iter_files()}
    for at in range(0x300000, len(memory) - 20, 4):
        if struct.unpack_from('<I', memory, at)[0] != 0x02160538:
            continue
        fields = struct.unpack_from('<5I', memory, at)
        pointer = fields[3]
        assert 0x02000000 <= pointer < 0x02400000
        raw = memory[pointer - 0x02000000:].split(b'\0', 1)[0]
        assert raw and len(raw) < 128 and all(32 <= b < 127 for b in raw)
        name = '/' + raw.decode('ascii').replace('\\', '/').lstrip('/')
        assert name.lower().endswith('.pxl')
        resolved = paths.get(name.casefold())
        owners.append({'owner': 0x02000000 + at, 'fields': list(fields),
                       'native_filename': name, 'path': resolved,
                       'exact_ROM_filename_match': resolved is not None,
                       'file_sha256': sha(rom.read_file(resolved)) if resolved else None})
    assert owners
    represented = {r['path'] for r in owners if r['path'] is not None}
    all_pxl = {name for _, name, _ in rom.iter_files() if name.lower().endswith('.pxl')}
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
             'original_primary_and_Online_registry_initializers_execute': True,
             'primary_distinct_instructions': len(primary), 'Online_distinct_instructions': len(online),
             'known_PXL_owner_vtable': 0x02160538, 'scan_bounds': [0x02300000, 0x02400000],
             'initialized_owners': owners, 'distinct_registered_PXL_paths': len(represented),
             'initialized_owner_filenames_without_exact_ROM_match': [r for r in owners if r['path'] is None],
             'all_ROM_PXL_paths': len(all_pxl),
             'PXL_paths_without_this_initialized_owner': sorted(all_pxl - represented),
             'no_CMMNIMG_WINFRAME_SLACKIMG_archives_in_this_PXL_owner_class': True,
             'scope': 'PXL owner class with exact original vtable after original primary and Online initialization, in the declared scanned RAM bounds. Other owner classes, later dynamic registrations, file-ID loads, generic readers, actual gameplay/GPU and raw archive consumers remain open.',
             'unused_resource_claim': False, 'ROM_changed': False, 'full_goal_complete': False}
    (ROOT / 'PXL_registry_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(len(owners), 'actual initialized owners;', len(represented), 'distinct matching PXL paths;',
          len(all_pxl - represented), 'PXL files require other registration contexts.')
    print('Unresolved filename owners:', len([r for r in owners if r['path'] is None]))


if __name__ == '__main__':
    main()
