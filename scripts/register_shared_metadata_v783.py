"""Register a new metadata-only replay; preserve all frozen V782 inputs."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch import shared_dialogue_editorial as owned
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/shared_metadata_v783')
OLD_CONFIG = Path('translations/shared_dialogue_editorial_release_v1.json')
CONFIG = Path('translations/shared_dialogue_editorial_release_v2.json')
MANUSCRIPT = Path('translations/shared_dialogue_editorial_manuscript_v3.json')
REGISTRY = Path('translations/release_stack.json')


def main():
    assert not CONFIG.exists()
    ROOT.mkdir(parents=True, exist_ok=True)
    cfg = read(OLD_CONFIG)
    old_manuscript = Path(cfg['manuscript'])
    assert sha(old_manuscript.read_bytes()) == cfg['manuscript_sha256']
    for p, h in cfg['dependencies'].items():
        assert sha(Path(p).read_bytes()) == h, p
    old, new = read(old_manuscript), read(MANUSCRIPT)
    assert len(old['records']) == len(new['records']) == 50
    affected = []
    for a, b in zip(old['records'], new['records'], strict=True):
        assert owned.compile_text(a) == owned.compile_text(b)
        changed = {k for k in set(a) | set(b) if a.get(k) != b.get(k)}
        assert changed <= {'speaker', 'context', 'localization_note'}
        if changed:
            assert 1035 <= b['message_id'] <= 1048
            affected.append(b['message_id'])
    assert affected == list(range(1035, 1049))
    equivalence = Path('work/analysis/shared_integration_v782/speaker_metadata_v3_equivalence.json')
    proof = Path('work/analysis/shared_integration_v782/role1_speaker_context_correction.json')
    assert read(equivalence)['all50_complete_encoded_paragraphs_identical']
    cfg.update({'manuscript': str(MANUSCRIPT), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
                'metadata_only_replay_of': str(OLD_CONFIG),
                'metadata_only_replay_of_sha256': sha(OLD_CONFIG.read_bytes())})
    cfg['dependencies'].update({str(p): sha(p.read_bytes()) for p in (OLD_CONFIG, old_manuscript, proof, equivalence)})
    registry = read(REGISTRY)
    assert 'all-routes-unified-v783' not in registry['profiles']
    assert len(registry['accepted_layers']) == 114
    save(ROOT/'release_stack_before_v783.json', registry)
    profile = deepcopy(registry['profiles']['all-routes-unified-v782'])
    assert profile['shared_dialogue_editorial'] == str(OLD_CONFIG)
    profile.update({'shared_dialogue_editorial': str(CONFIG),
                    'description': 'V782 exact binary replay with corrected First Mate speech-provider metadata;fleet/private actual samples remain pending.',
                    'status': 'experimental'})
    save(CONFIG, cfg)
    registry['profiles']['all-routes-unified-v783'] = profile
    save(REGISTRY, registry)
    save(ROOT/'registration.json', {
        'original_config': str(OLD_CONFIG), 'original_config_sha256': sha(OLD_CONFIG.read_bytes()),
        'original_manuscript': str(old_manuscript), 'original_manuscript_sha256': sha(old_manuscript.read_bytes()),
        'new_config': str(CONFIG), 'new_config_sha256': sha(CONFIG.read_bytes()),
        'new_manuscript': str(MANUSCRIPT), 'new_manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'corrected_context_IDs': affected, 'all50_compiled_paragraphs_exact': True,
        'all_previous_profiles_accepted_layers_and_canonical_unchanged': True,
        'expected_ROM_sha256': '9f55817772d2b1e940462f69103536654f0cbedbe959fb42670fc601f2d6e31d',
        'registered_build_pending': True, 'actual_fleet_private_samples_pending': True,
        'producer_sha256': sha(Path(__file__).read_bytes())})
    print('V783 metadata replay registered;all50 compiled texts and frozen V782 dependencies preserved.', flush=True)


if __name__ == '__main__':
    main()
