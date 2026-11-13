"""Prove the registered metadata replay is exactly the previously tested ROM."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.xdelta import apply_xdelta
from scripts.register_shared_metadata_v783 import ROOT, CONFIG, MANUSCRIPT, OLD_CONFIG, REGISTRY
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v783_candidate.nds')
OLD_ROM = Path('out/all_routes_combined_v782_candidate.nds')


def main():
    old, new = OLD_ROM.read_bytes(), ROM.read_bytes()
    assert new == old
    digest = sha(new)
    assert digest == '9f55817772d2b1e940462f69103536654f0cbedbe959fb42670fc601f2d6e31d'
    registration = read(ROOT/'registration.json')
    assert digest == registration['expected_ROM_sha256']
    cfg = read(CONFIG)
    for p, h in cfg['dependencies'].items():
        assert sha(Path(p).read_bytes()) == h, p
    assert sha(MANUSCRIPT.read_bytes()) == cfg['manuscript_sha256'] == registration['new_manuscript_sha256']
    assert sha(OLD_CONFIG.read_bytes()) == registration['original_config_sha256']
    m, om = read(ROM.with_suffix('.manifest.json')), read(OLD_ROM.with_suffix('.manifest.json'))
    registry, before = read(REGISTRY), read(ROOT/'release_stack_before_v783.json')
    assert set(registry) == set(before)
    assert all(registry[k] == before[k] for k in registry if k != 'profiles')
    assert set(registry['profiles']) == set(before['profiles']) | {'all-routes-unified-v783'}
    assert all(registry['profiles'][p] == v for p, v in before['profiles'].items())
    assert len(registry['accepted_layers']) == 114
    profile, parent = registry['profiles']['all-routes-unified-v783'], registry['profiles']['all-routes-unified-v782']
    assert {k for k in set(profile) | set(parent) if profile.get(k) != parent.get(k)} == {'description', 'shared_dialogue_editorial'}
    assert profile['shared_dialogue_editorial'] == str(CONFIG)
    assert m['profile'] == 'all-routes-unified-v783' and m['candidate_sha256'] == digest
    assert m['release_stack_sha256'] == sha(REGISTRY.read_bytes()) and all(m['checks'].values())
    for key in ('base_rom', 'base_sha256', 'changed_paths', 'changed_records', 'required_batches', 'batches',
                'checks', 'story_percent_contract', 'final_plaque_contract', 'final_raw_art_contract', 'final_graphics_copy_contract'):
        assert m[key] == om[key], key
    assert len(m['batches']) == 470
    for p in ('/COMMON/MESFILE.DK4', '/__arm9__.bin'):
        stage = m['relocations'][p]['shared_dialogue_editorial']
        previous = om['relocations'][p]['shared_dialogue_editorial']
        assert stage['release_config'] == str(CONFIG) and stage['release_config_sha256'] == sha(CONFIG.read_bytes())
        assert stage['proof'] == previous['proof']
    clean = Path('work/clean.nds')
    assert sha(clean.read_bytes()) == 'f4f07c975cc293f5b2ba469747693d3dd37f2e6dfc408cf5910adf5e83d9177d'
    patch = ROM.with_suffix('.xdelta')
    shutil.copyfile(OLD_ROM.with_suffix('.xdelta'), patch)
    rebuilt = ROOT/'patch_reconstruction_RESEARCH_ONLY.nds'
    apply_xdelta(clean, patch, rebuilt)
    assert rebuilt.read_bytes() == new
    old_root = Path('work/analysis/shared_integration_v782')
    protected = read(old_root/'checkpoint.json')['protected_files_unchanged']
    for p, h in protected.items():
        assert sha(Path(p).read_bytes()) == h, p
    evidence = [old_root/p for p in ('registered_verification.json', 'patch_proof.json', 'newgame_regression.json',
                'recruit_capacity_gameplay_verification.json', 'recruit_shortfall_gameplay_verification.json',
                'warning_gameplay_verification.json', 'information_gameplay_verification.json',
                'village_casual_gameplay_verification.json', 'village_formal_gameplay_verification.json',
                'information_village_checkpoint.json')]
    save(ROOT/'verification.json', {
        'candidate': str(ROM), 'candidate_sha256': digest, 'whole_ROM_identical_to_V782': True,
        'profile': m['profile'], 'manifest_sha256': sha(ROM.with_suffix('.manifest.json').read_bytes()),
        'corrected_manuscript': str(MANUSCRIPT), 'corrected_manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'all50_compiled_paragraphs_and_all_ROM_files_components_graphics_exact': True,
        'all470_batches114_accepted_layers_and_canonical_preserved': True,
        'all_prior_profiles_and_frozen_V782_inputs_preserved': True,
        'registered_speaker_context_replay_complete': True,
        'clean_source_sha256': sha(clean.read_bytes()), 'patch': str(patch), 'patch_sha256': sha(patch.read_bytes()),
        'byte_exact_clean_input_reconstruction': True,
        'inherited_evidence_by_exact_whole_ROM_identity': [{'path': str(p), 'sha256': sha(p.read_bytes())} for p in evidence],
        'new_scene_activations_claimed': False, 'new_editorial_completion_credit': 0,
        'remaining_actual_families': ['fleet1030-1034', 'private1049-1069'],
        'protected_files_unchanged': protected, 'full_goal_complete': False,
        'producer_sha256': sha(Path(__file__).read_bytes())})
    print('V783 registered replay equals every V782 ROM byte;exact clean-input patch reconstructs it. Speaker metadata registration complete;fleet/private samples pending.', flush=True)


if __name__ == '__main__':
    main()
