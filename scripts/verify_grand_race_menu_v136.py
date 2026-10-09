"""Verify saved full V136, exact inherited components and complete native status text."""

import json
import struct
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha, validate_release_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.probe_grand_race_menu_copy import execute_copy
from scripts.register_grand_race_help_v134 import components, patched_arm9
from scripts.register_grand_race_menu_v136 import BATCH


def main():
    path = Path('out/all_routes_combined_v136_candidate.nds')
    old_path = Path('out/all_routes_combined_v135_candidate.nds')
    if sha(old_path.read_bytes()) != '9b63f9595b41bf209467753673b7e11ee46595f77c4c9cd273b7f11633468c3e':
        raise ValueError('Pinned full V135 differs')
    old = components(NdsImage.open(old_path))
    saved = components(NdsImage.open(path))
    batch = json.loads(Path(BATCH).read_text(encoding='utf-8'))
    baseline = NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/__arm9__.bin')
    validate_release_batch(batch, baseline)
    if old.keys() != saved.keys():
        raise ValueError('File/component identities changed')
    for name, data in old.items():
        expected = patched_arm9(data, batch) if name == '/__arm9__.bin' else data
        if saved[name] != expected:
            raise ValueError(f'Unexpected saved component change: {name}')
    arm9 = saved['/__arm9__.bin']
    selections = []
    fields = {'START': 0x115354, 'READ_RULES': 0x115364,
              'ABOUT': 0x1153A4, 'BASIC_RULES': 0x1153B4,
              'MAP_SUPPLIES': 0x1153C4, 'LIMITS': 0x1153D4}
    for row in batch['records']:
        offset = row['offset']
        field = fields[row['id'].removeprefix('GRAND_RACE_UI_')]
        if struct.unpack_from('<4I', arm9, field) != (0x02000000 + offset, 1, 1, 0):
            raise ValueError('Native selector entry no longer selects complete label')
        size = len(bytes.fromhex(row['source_hex']))
        selected = arm9[offset:arm9.index(0, offset)].decode('ascii')
        if selected != row['english'] or arm9[offset:offset + size] != selected.encode('ascii').ljust(size, b'\0'):
            raise ValueError('Saved status loses full English, NUL or zero padding')
        if execute_copy(arm9, selected.encode('ascii') + b'\0') != selected.encode('ascii') + b'\0':
            raise ValueError('Actual native copier loses label characters')
        selections.append({'id': row['id'], 'english': selected, 'native_label_area': [84, 20],
                           'width_px': len(selected) * 6, 'complete_text_and_leading_character_intact': True})
    old_common = common_message_entries(old['/COMMON/MESFILE.DK4'], old['/__arm9__.bin'], clean=False)
    new_common = common_message_entries(saved['/COMMON/MESFILE.DK4'], arm9, clean=False)
    if old_common != new_common or len(new_common) != 3668:
        raise ValueError('Native COMMON selections changed')
    manifest = json.loads(path.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    for field, artifact in [('candidate_sha256', manifest['candidate_rom']),
                            ('base_sha256', manifest['base_rom']),
                            ('release_stack_sha256', manifest['release_stack'])]:
        if sha(Path(artifact).read_bytes()) != manifest[field]:
            raise ValueError(f'Manifest hash differs: {field}')
    if manifest['profile'] != 'all-routes-unified-v136' or len(manifest['batches']) != 432 or not all(manifest['checks'].values()):
        raise ValueError('Complete profile, batch count or checks differ')
    report = {'status': 'pass', 'candidate_sha256': sha(path.read_bytes()),
              'profile': manifest['profile'], 'batch_count': 432, 'selections': selections,
              'all_V135_components_exact_except_six_ARM9_menu_spans': True,
              'all_3668_native_COMMON_selections_exact': True,
              'route_graphics_help_and_sound_bytes_unchanged': True,
              'ARM9_code_font_pointers_geometry_and_clear_strings_unchanged': True,
              'manifest_candidate_base_registry_hashes_verified': True,
              'runtime_verified': False}
    Path('work/analysis/grand_race_menu_v136_saved_proof.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
