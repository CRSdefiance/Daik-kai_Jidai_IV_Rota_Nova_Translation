"""Prepare a current-ROM Maria coldboot using the existing isolated system unlock only."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Maria_current_context_20261109_v1')


def main():
    assert not ROOT.exists()
    release_path = Path('work/hodram_residual_release_v1/registered_release_verification.json')
    release = load(release_path)
    for path, expected in [(Path(release['candidate']), release['candidate_sha256']),
        (Path(release['manifest']), release['manifest_sha256']),
        (Path('translations/release_stack.json'), release['registry_sha256'])]:
        assert digest(path) == expected
    old = load('work/analysis/maria_intro_v684/preflight.json')
    donor = Path(old['donor'])
    assert digest(donor) == old['donor_sha256']
    fixture_path = Path('work/analysis/maria_intro_v684/unlock_manifest.json')
    assert digest(fixture_path) == old['unlock_manifest_sha256']
    fixture = load(fixture_path)
    assert fixture['fixture_save_sha256'] == old['donor_sha256']
    assert fixture['all_six_route_save_slots_and_footer_unchanged']
    assert fixture['only_system_low_four_bits_and_original_checksum_changed']
    assert fixture['earned_unlock_verified'] is False
    prior_inputs = Path('work/analysis/maria_opening_context_v2035/ordinary_existing_Maria_inputs.json')
    original_inputs = Path(load('work/analysis/maria_intro_v684/run_config.json')['inputs'])
    assert load(prior_inputs) == load(original_inputs)
    ROOT.mkdir()
    inputs = ROOT / 'ordinary_inputs.json'
    inputs.write_bytes(prior_inputs.read_bytes())
    fixture.update(production_ROM=release['candidate'], production_ROM_sha256=release['candidate_sha256'],
        current_test_scope='Current Maria runtime/name/substitution context; copied existing system unlock only, not earned progression.')
    own_fixture = ROOT / 'existing_system_unlock_manifest.json'
    save(own_fixture, fixture)
    save(ROOT / 'run_plan.json', dict(candidate=release['candidate'], candidate_sha256=release['candidate_sha256'],
        frames=31000, inputs=str(inputs), inputs_sha256=digest(inputs),
        donor=str(donor), donor_sha256=digest(donor), fixture_manifest=str(own_fixture),
        fixture_manifest_sha256=digest(own_fixture), output=str(ROOT / 'capture'),
        current_ROM_unchanged=True, no_savestate_orstory_location_RNG_funds_outcome_fixture=True,
        only_preexisting_isolated_system_unlock_not_earned=True,
        all301_independent_drafts_precede_current_conversation_intake=True,
        previous_goal_turn_classification='progress:301 source meanings and67 drafts saved to authoritative zero-credit checkpoint.',
        new_credit=0, full_goal_complete=False,
        evidence={str(p): digest(p) for p in [release_path, fixture_path, prior_inputs, original_inputs, Path(__file__)]}))
    print('Prepared31,000-frame current-ROM Maria context; existing isolated system unlock only; no ROM changes.')


if __name__ == '__main__':
    main()
