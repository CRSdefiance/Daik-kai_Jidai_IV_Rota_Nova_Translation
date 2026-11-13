"""Exact combined release ancestry and clean-ROM patch reconstruction."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import make_xdelta, apply_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.verify_fleet_release_v375 import files

ROOT = Path('work/analysis/guild_description_release_v443')
ROM = Path('out/all_routes_combined_v443_candidate.nds')
PARENT = Path('out/all_routes_combined_v440_candidate.nds')


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def main():
    manifest, parent_manifest = read(ROM.with_suffix('.manifest.json')), read(PARENT.with_suffix('.manifest.json'))
    digest = sha(ROM.read_bytes())
    assert manifest['candidate_sha256'] == digest
    assert manifest['profile'] == 'all-routes-unified-v443'
    assert manifest['base_sha256'] == parent_manifest['base_sha256']
    assert manifest['batches'] == parent_manifest['batches'] and len(manifest['batches']) == 470
    assert manifest['required_batches'] == parent_manifest['required_batches']
    assert all(manifest['checks'].values())
    registry_path = Path('translations/release_stack.json')
    assert manifest['release_stack_sha256'] == sha(registry_path.read_bytes())
    profiles = read(registry_path)['profiles']
    assert all(profiles[manifest['profile']][k] == v for k, v in profiles['all-routes-unified-v440'].items()
               if k not in ('description', 'note'))
    previous, current = files(NdsImage.open(PARENT)), files(NdsImage.open(ROM))
    assert previous.keys() == current.keys()
    changed = sorted(k for k in previous if previous[k] != current[k])
    assert changed == ['/COMMON/MESFILE.DK4', '/__arm9__.bin']
    research = Path('work/analysis/guild_description_v442')
    assert current['/COMMON/MESFILE.DK4'] == (research / 'research_COMMON.bin').read_bytes()
    assert current['/__arm9__.bin'] == (research / 'research_arm9.bin').read_bytes()
    patch = ROM.with_suffix('.xdelta')
    make_xdelta(Path('work/clean.nds'), ROM, patch)
    reconstruction = ROOT / 'patch_reconstruction.nds'
    apply_xdelta(Path('work/clean.nds'), patch, reconstruction)
    assert reconstruction.read_bytes() == ROM.read_bytes()
    proof = {
        'candidate': str(ROM), 'candidate_sha256': digest, 'patch_sha256': sha(patch.read_bytes()),
        'exact_clean_patch_reconstruction': True,
        'parent': str(PARENT), 'parent_sha256': sha(PARENT.read_bytes()),
        'profile': manifest['profile'], 'canonical_base': manifest['base_rom'],
        'canonical_base_sha256': manifest['base_sha256'],
        'all470_inherited_batches_and_stages_retained': True,
        'changed_internal_files_from_V440': changed,
        'research_buffers_exact': True,
        'transform_proof': str(research / 'transform_proof.json'),
        'native_proof': str(research / 'native_proof.json'),
        'actual_cold_boot_guild_verification_pending': True,
        'all18_plaques_incomplete': True, 'full_goal_complete': False,
        'release_status': 'experimental',
    }
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print('V443: all470 inherited batches/stages retained; only COMMON/ARM9 changed; exact clean patch reconstruction passes.')


if __name__ == '__main__':
    main()
