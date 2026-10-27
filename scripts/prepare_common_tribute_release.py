"""Prepare reproducible tribute component/output locks; do not register a ROM."""

import json
from pathlib import Path

from ndspy.code import MainCodeFile

from dk4tool.patch.common_tribute_release import SOURCE_ARM9, SOURCE_COMMON, transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_monthly_word_wrap_hook import prepare


def write(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def main():
    rom = NdsImage.open('out/all_routes_combined_v142_candidate.nds')
    source = rom.read_file('/__arm9__.bin')
    saved, placement = prepare(source)
    resident = MainCodeFile(saved, 0x02000000).sections[1]
    payload = bytes(resident.data[6944:])
    component = {'format': 'dk4-tribute-runtime-component-v1', 'source_arm9_sha256': SOURCE_ARM9,
                 'target_arm9_sha256': sha(saved), 'payload_hex': payload.hex().upper(),
                 'payload_sha256': sha(payload), 'reserved_arena_low': placement['reserved_arena_low'],
                 'static_patches': [{'offset': at, 'source_hex': source[at:at + 4].hex().upper(),
                                     'replacement_hex': saved[at:at + 4].hex().upper()}
                                    for at in (0xB2590, 0x54798, 0x54160, 0xE45E4)]}
    component_path = 'translations/common_tribute_runtime_component_v1.json'
    manuscript_path = 'translations/common_tribute_repairs_manuscript_v2.json'
    write(component_path, component)
    document = json.loads(Path(manuscript_path).read_text(encoding='utf-8'))
    result = transform(rom.read_file('/COMMON/MESFILE.DK4'), source, document, component)
    config = {'format': 'dk4-common-tribute-release-v1', 'status': 'draft-review-incomplete',
              'source_common_sha256': SOURCE_COMMON, 'source_arm9_sha256': SOURCE_ARM9,
              'target_common_sha256': sha(result.common), 'target_arm9_sha256': sha(result.arm9),
              'manuscript': manuscript_path, 'runtime_component': component_path,
              'dependencies': {path: sha(Path(path).read_bytes()) for path in (manuscript_path, component_path)},
              'pending': ['complete widget/portrait construction proof', 'formatting gate approval',
                          'combined native town/monthly runtime regression after final repack',
                          'integrated experimental profile/build/patch verification', 'cold-boot gameplay']}
    write('translations/common_tribute_release_v1.json', config)
    proof = {'status': 'draft-complete-component-and-native-repack-output-locked',
             'authored_ids': list(range(76, 84)), 'changed_records': sorted(result.changed_records),
             'changed_offsets': sorted(result.changed_offsets), 'all_native_entries_compared': len(result.entries),
             'expected_common_sha256': sha(result.common), 'expected_arm9_sha256': sha(result.arm9),
             'profile_registered': False, 'playable_rom_built': False}
    write('work/analysis/common_tribute_release_plan.json', proof)
    print(f'Strict tribute plan ready: {len(result.changed_records)} records, {len(result.changed_offsets)} offsets; all {len(result.entries)} selections compared. Review gate remains closed.')


if __name__ == '__main__':
    main()
