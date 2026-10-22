"""Registered ancestry, scoped binary changes, rejection controls and exact patch."""

from copy import deepcopy
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_help_editorial import CONFIG, apply_release, current_entries, plan
from dk4tool.patch.levelup_stat_format import current_entries as previous_entries
from dk4tool.patch.xdelta import apply_xdelta, make_xdelta
from dk4tool.rom.nds import NdsImage
from scripts.prepare_refit_editorial_v830 import MANUSCRIPT
from scripts.prepare_refit_release_v831 import ROOT
from scripts.verify_refit_release_v708 import files
from scripts.verify_village_wrap_v608 import read, save

ROM = Path('out/all_routes_combined_v831_candidate.nds')
OLD = Path('out/all_routes_combined_v829_candidate.nds')


def rejected(action):
    try:
        action()
    except (ValueError, AssertionError):
        return True
    raise AssertionError('Invalid editorial release input accepted')


def main():
    old, new = map(NdsImage.open, (OLD, ROM))
    before, after = files(old), files(new)
    changed = {p for p in before if before[p] != after[p]}
    assert before.keys() == after.keys() and changed == {'/COMMON/MESFILE.DK4', '/__arm9__.bin'}
    common, arm, proof = apply_release(before['/COMMON/MESFILE.DK4'], before['/__arm9__.bin'], CONFIG)
    assert common == after['/COMMON/MESFILE.DK4'] and arm == after['/__arm9__.bin']
    original = previous_entries(before['/COMMON/MESFILE.DK4'], before['/__arm9__.bin'])
    actual = current_entries(common, arm)
    assert len(actual) == 3668
    physically_changed = [a.message_id for a, b in zip(original, actual, strict=True) if a.text != b.text]
    assert len(physically_changed) == 18
    assert all(original[i].text == actual[i].text for i in (676, 677))
    registry = read('translations/release_stack.json')
    prior = read(ROOT / 'registry_before.json')
    restored = deepcopy(registry)
    profile = restored['profiles'].pop('all-routes-unified-v831')
    assert restored == prior and len(registry['accepted_layers']) == 114
    inherited = deepcopy(profile)
    inherited.pop('refit_help_editorial')
    for key in ('description', 'note', 'status'):
        inherited[key] = prior['profiles']['all-routes-unified-v829'][key]
    assert inherited == prior['profiles']['all-routes-unified-v829']
    manifest, old_manifest = read(ROM.with_suffix('.manifest.json')), read(OLD.with_suffix('.manifest.json'))
    assert manifest['candidate_sha256'] == sha(ROM.read_bytes())
    assert manifest['release_stack_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert manifest['base_sha256'] == registry['canonical_baseline']['sha256']
    assert manifest['batches'] == old_manifest['batches'] and len(manifest['batches']) == 471
    assert manifest['required_batches'] == old_manifest['required_batches'] and all(manifest['checks'].values())
    for path, records in old_manifest['changed_records'].items():
        assert set(records) <= set(manifest['changed_records'][path])
    manuscript = read(MANUSCRIPT)
    bad = deepcopy(manuscript)
    bad['records'][0]['current_text_hex'] = '42'
    controls = [rejected(lambda: plan(b'X' + before['/COMMON/MESFILE.DK4'][1:], before['/__arm9__.bin'], manuscript)),
                rejected(lambda: plan(before['/COMMON/MESFILE.DK4'], b'X' + before['/__arm9__.bin'][1:], manuscript)),
                rejected(lambda: plan(before['/COMMON/MESFILE.DK4'], before['/__arm9__.bin'], bad))]
    assert all(controls)
    clean = Path('work/clean.nds')
    patch, reconstructed = ROM.with_suffix('.xdelta'), ROOT / 'V831_exact_patch_reconstruction.nds'
    make_xdelta(clean, ROM, patch)
    apply_xdelta(clean, patch, reconstructed)
    assert reconstructed.read_bytes() == ROM.read_bytes()
    save(ROOT / 'registered_release_verification.json', {
        'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'patch': str(patch), 'patch_sha256': sha(patch.read_bytes()),
        'manifest_sha256': sha(ROM.with_suffix('.manifest.json').read_bytes()),
        'registry_sha256': sha(Path('translations/release_stack.json').read_bytes()),
        'changed_components_relative_to_V829': sorted(changed),
        'changed_native_message_IDs': physically_changed, 'all3650_other_text_strings_exact': True,
        'all_graphics_scripts_HELP_ARM7_overlays_other_files_exact': True,
        'all_prior_profiles471_batches114_accepted_layers_preserved': True,
        'late_stage_replay_matches_complete_target_bytes': True,
        'bad_source_COMMON_ARM9_and_stale_current_record_rejected': controls,
        'exact_clean_input_patch_reconstruction': str(reconstructed),
        'native_repack_proof': proof, 'actual_panel_and_startup_verification_pending': True,
        'canonical_not_promoted': True, 'verifier_sha256': sha(Path(__file__).read_bytes()),
        'full_goal_complete': False})
    print('V831 full471/114 release and exact clean patch pass;only18 texts/native metadata changed. Actual panels pending.', flush=True)


if __name__ == '__main__':
    main()
