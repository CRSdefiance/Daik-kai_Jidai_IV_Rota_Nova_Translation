"""Capture a fresh captain2 context from the exact registered ROM using qualified ordinary inputs."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest

ROOT = Path('work/Lil382_residual_A_clean_20261110/current_context_v1')
RELEASE = Path('work/maria315_B286_B302_release_v1/registered_release_verification.json')
PRIOR = Path('work/analysis/retrospective_Lil_context_runs_v7836/route2/run_plan.json')


def main():
    assert not ROOT.exists()
    release, prior = map(load, [RELEASE, PRIOR])
    assert digest('translations/release_stack.json') == release['registry_sha256']
    assert digest(release['candidate']) == release['candidate_sha256']
    assert not release['own_registered_startup_pending'] and release['clean_input_patch_byte_exact']
    assert prior['route'] == prior['expected_original_captain_ID'] == 2 and prior['frames'] == 4001
    assert digest(prior['inputs']) == prior['inputs_sha256']
    assert prior['no_RAM_code_observer_savestate_roles_roster_funds_RNG_orresult_forcing']
    assert not prior['existing_system_only_unlock_not_earned'] and prior['source_donor'] is None
    ROOT.mkdir()
    inputs = ROOT/'ordinary_Lil_inputs.json'
    inputs.write_bytes(Path(prior['inputs']).read_bytes())
    assert digest(inputs) == prior['inputs_sha256']
    argv = ['--rom', release['candidate'], '--out', str(ROOT/'capture'), '--frames', '4001',
        '--inputs-json', str(inputs), '--capture-every', '999999', '--capture-at', '180', '2000', '4000', '--dump-ram']
    save(ROOT/'run_plan.json', dict(candidate=release['candidate'], candidate_sha256=release['candidate_sha256'],
        registered_release=str(RELEASE), registered_release_sha256=digest(RELEASE),
        prior_ordinary_input_plan=str(PRIOR), prior_ordinary_input_plan_sha256=digest(PRIOR),
        frames=4001, inputs=str(inputs), inputs_sha256=digest(inputs),
        sealed_382_clean_drafts=str(ROOT.parent/'clean_draft_seal_v1.json'),
        sealed_382_clean_drafts_sha256=digest(ROOT.parent/'clean_draft_seal_v1.json'),
        no_savestate_battery_observer_RAM_roster_role_money_RNG_oroutcome_override=True,
        opening_not_new_382_optional_event_activation=True, all_contextual_comparisons_andfive_gates_pending=True,
        guide_photos=False, new_credit=0, producer_sha256=digest(__file__)))
    save(ROOT/'worker_argv.json', dict(argv=argv, candidate_sha256=release['candidate_sha256'], new_credit=0))
    print('Prepared4001-frame ordinary Lil context onregistered Maria315;no battery,overlay oroptional scene forcing.')


if __name__ == '__main__':
    main()
