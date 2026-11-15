"""Verify final Tavern repair integration, inherited graphics and exact patch."""

import json
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_fleet_release_v375 import files, match

ROM = Path('out/all_routes_combined_v383_candidate.nds')
ROOT = Path('work/analysis/tavern_release_v383')


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def main():
    manifest = read(ROM.with_suffix('.manifest.json'))
    parent = read('out/all_routes_combined_v378_candidate.manifest.json')
    digest = sha(ROM.read_bytes())
    assert manifest['candidate_sha256'] == digest and manifest['profile'] == 'all-routes-unified-v383'
    assert manifest['base_sha256'] == parent['base_sha256'] == (
        '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe')
    assert manifest['batches'] == parent['batches'] and len(manifest['batches']) == 470
    stack_path = Path('translations/release_stack.json')
    stack = read(stack_path)
    assert manifest['release_stack_sha256'] == sha(stack_path.read_bytes())
    old = stack['profiles']['all-routes-unified-v378']
    new = stack['profiles']['all-routes-unified-v383']
    assert all(new[k] == v for k, v in old.items() if k not in ('note', 'description'))
    assert set(new) - set(old) == {'tavern_round_announcement'}
    a, b = files(NdsImage.open('out/all_routes_combined_v378_candidate.nds')), files(NdsImage.open(ROM))
    assert a.keys() == b.keys()
    assert [n for n in a if a[n] != b[n]] == ['/COMMON/MESFILE.DK4']
    assert b['/COMMON/MESFILE.DK4'] == Path('work/analysis/tavern_round_v382/target_common.bin').read_bytes()
    assert ROM.read_bytes() == Path('work/analysis/tavern_round_v382/research_only_tavern.nds').read_bytes()
    assert (ROOT / 'patch_reconstruction.nds').read_bytes() == ROM.read_bytes()
    assert sha(Path('work/clean.nds').read_bytes()) == (
        'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d')
    captures = {}
    for old_name, new_name in [('tavern_round_v382_revised', 'tavern_final_v383'),
                               ('alignment_new_game_v378', 'tavern_new_game_v383')]:
        captures[new_name] = match(Path('work/emulation_v193') / old_name,
                                   Path('work/emulation_v193') / new_name, digest)
    plaques = read('translations/graphics_completion_campaign_v1.json')['plaque_style_v247']['ongoing_plaque_inventory']
    assert len(plaques) == 18 and all(not p['fully_completed'] for p in plaques)
    proof = {'candidate': str(ROM), 'candidate_sha256': digest, 'profile': manifest['profile'],
             'patch_sha256': sha(ROM.with_suffix('.xdelta').read_bytes()),
             'base': manifest['base_rom'], 'base_sha256': manifest['base_sha256'],
             'exact_clean_patch_reconstruction': True,
             'all470_batches_and_all_V378_stages_retained': True,
             'only_COMMON_changed_ARM9_all_graphics_and_other_components_exact': True,
             'exact_final_ROM_replay_frames': captures,
             'actual_announcement_proof': 'work/analysis/tavern_round_v382/live_proof.json',
             'native_source_and_ABI_proof': 'work/analysis/tavern_round_v382/native_proof.json',
             'all18_plaques_incomplete': True, 'full_goal_complete': False,
             'status': 'experimental', 'canonical_promotion': False,
             'weapon_armor_acquired': False, 'hardware_device_verification': False}
    (ROOT / 'release_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(f'V383: full inherited stack, exact patch and {sum(captures.values())} final-ROM frames pass.')


if __name__ == '__main__':
    main()
