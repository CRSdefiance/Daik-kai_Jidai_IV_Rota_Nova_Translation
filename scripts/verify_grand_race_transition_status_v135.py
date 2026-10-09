"""Verify saved full V135, exact inherited components and complete native status text."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_status_release import sha, validate_release_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.register_grand_race_help_v134 import components, patched_arm9
from scripts.register_grand_race_transition_status_v135 import BATCH


def main():
    path = Path('out/all_routes_combined_v135_candidate.nds')
    old_path = Path('out/all_routes_combined_v134_candidate.nds')
    if sha(old_path.read_bytes()) != '6af0f04f94538daa6cab58062c62e9dff578041da1f0b9ccf84b0b2fedcada9f':
        raise ValueError('Pinned full V134 differs')
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
    for row in batch['records']:
        offset = row['offset']
        size = len(bytes.fromhex(row['source_hex']))
        selected = arm9[offset:arm9.index(0, offset)].decode('ascii')
        if selected != row['english'] or arm9[offset:offset + size] != selected.encode('ascii').ljust(size, b'\0'):
            raise ValueError('Saved status loses full English, NUL or zero padding')
        selections.append({'id': row['id'], 'english': selected, 'position': [16, 64],
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
    if manifest['profile'] != 'all-routes-unified-v135' or len(manifest['batches']) != 431 or not all(manifest['checks'].values()):
        raise ValueError('Complete profile, batch count or checks differ')
    report = {'status': 'pass', 'candidate_sha256': sha(path.read_bytes()),
              'profile': manifest['profile'], 'batch_count': 431, 'selections': selections,
              'all_V134_components_exact_except_two_ARM9_status_spans': True,
              'all_3668_native_COMMON_selections_exact': True,
              'route_graphics_help_and_sound_bytes_unchanged': True,
              'ARM9_code_font_pointers_geometry_and_clear_strings_unchanged': True,
              'manifest_candidate_base_registry_hashes_verified': True,
              'runtime_verified': False}
    Path('work/analysis/grand_race_status_v135_saved_proof.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
