"""Seal the bounded patch audit without promoting or modifying any ROM."""

import hashlib
import json
from pathlib import Path

ROOT = Path('work/patch_interaction_audit_20261027')

OBSERVATIONS = {
    'guild': 'Seoul Guild purchase/sale dialogs, changed funds, return to town.',
    'inn': 'One/three-night stays, date/funds changes and town return.',
    'palace': 'Istanbul contract fee/share dialog and town return.',
    'port': 'Historical label corrected: actually Yard last-ship sale refusal and return.',
    'shipyard': 'Yard sale refusal and return; this does not cover ship construction/purchase.',
    'square': 'Shop captions, portraits, trends and conversation progress; no freeze.',
    'refit': 'Equipment grid, descriptions, choices and return to remodeling menu.',
    'town_market_tavern': 'Historical label corrected: Maria opening and Tavern welcome/drink; no Market visit.',
    'recruitment': 'Recruitment offer, patron answer, sailor/capacity dialog and Tavern return.',
    'help': 'Town-command Help pages and return to town.',
    'save_load': 'Load selection and actual change from Syracuse to saved Stockholm game.',
    'gallery': 'Multiple character portraits/names and return; inherited prepared unlock.',
    'race': 'Local host waiting roster and return to title; no wireless match.',
    'hodram_opening': 'Opening choice, crew/Manuel conversations and Stockholm town.',
    'lil_opening': 'Amsterdam opening, Fernando/permit conversations and initial sailing handoff.',
    'maria_opening': 'Ian/Xien/Yukihisa opening conversations and Hangzhou town; prepared system unlock.',
    'rafael_guided': 'Ask him choice, Julio conversations and initial town tutorial handoff; not the whole tutorial.',
    'church_controlled': 'Prayer choice, peace response and repeated visit/return; bounded calendar/facility prerequisite.',
    'battle_controlled': 'Encounter/tutorial conversations, naval engagement and sea/ship inspection; no observed victory.',
    'battle_followup': 'Naval engagement, changing crew/supplies, disengagement, Deck/Lookout duty selection, Fleet Info/ship pages and sea return.',
    'battle_aftermath_controlled': 'Current-ROM duel challenge/acceptance, visible fencing combat with falling HP, enemy flagship fleeing/victory speech, aftermath and Gerhard level-up/sea return; bounded disposable pre-duel prerequisites, last applied5770 before challenge5782.',
    'main_menus': 'Sound Setup controls/preview requests, Report/Sailing Help prompts, captain selection/back, Extras/About/Online pages and title return; audio not assessed.',
    'facility_tour': 'Actual Market contract refusal, Palace contract, committed cargo sale (5299 to8071), price pages, Port Cargo Setup, Dock/Swap Ships and town return; Angelo joining event progressed.',
    'battle_menu_timing_followup': 'Readiness probe only: ordinary sailing/message dismissal works, but original fixture fleet5 has no live mobile ship at4800 or5400. No battle-menu/victory credit.',
}


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def save(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')


def main():
    target = read(ROOT/'target.json')
    assert sha(target['ROM']) == target['sha256']
    assert sha('translations/release_stack.json') == target['registry_sha256']
    assert Path('translations/release_stack.json').read_bytes() == (ROOT/'release_stack_at_start.json').read_bytes()
    assert sha('out/raphael_natural_v2_accepted_base.nds') == '3cb827e4c52ab2086fb5a626835d72192085a958581279d3c79b0200bbf405fe'
    trace = read(ROOT/'construction_write_provenance.json')
    assert trace['exact_registered_reconstruction'] and trace['ROM_sha256'] == target['sha256']
    memory = read(ROOT/'runtime_storage_mutations.json')
    assert not any(memory['unexpected_mutations'].values()) and memory['negative_controls_passed']
    outcomes = []
    visual = read(ROOT/'visual_index.json')
    for path in sorted((ROOT/'cases').glob('*/capture/capture_report.json')):
        name = path.parents[1].name
        report = read(path)
        assert name in OBSERVATIONS and name in visual
        assert report['ROM_sha256'] == target['sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        battery = report.get('battery_save_preloaded')
        if battery:
            assert sha(battery['source']) == battery['source_sha256']
        visual[name].update(visual_review_pending=False, representative_sheet_visually_reviewed=True,
            observation=OBSERVATIONS[name], all_captured_frames_individually_reviewed=False)
        fixture_fields = [k for k,v in report.items() if 'fixture' in k and v]
        outcomes.append(dict(case=name, frames=report['frames'], report=str(path), report_sha256=sha(path),
            observation=OBSERVATIONS[name], prepared_battery=battery, runtime_fixture_fields=fixture_fields,
            callback_errors=[], savestate_loaded=False,
            status='readiness_probe_only' if name=='battle_menu_timing_followup' else 'representative_scope_reviewed'))
    assert len(outcomes) == len(OBSERVATIONS)
    save(ROOT/'visual_index.json',visual)
    test_results = read(ROOT/'isolated_tests/effective_results.json')
    test_summary = read(ROOT/'isolated_tests/summary.json')
    classification = read(ROOT/'isolated_tests/missing_input_classification.json')
    assert set(classification['terminal_exception_counts']) == {'FileNotFoundError'}
    assert len(classification['files']) == sum(r['exit_code'] != 0 for r in test_results)
    recovered = [r for r in read(ROOT/'legacy_fixture_recovery_results.json') if r['status']=='restored_exact_historical_input']
    assert len(recovered) == 40
    for row in recovered:
        assert sha(row['ROM']) == row['sha256']
    moved = read(ROOT/'fixture_storage_relocation.json')
    assert len(moved) == 40
    for row in moved:
        assert sha(row['destination']) == row['sha256']
    failures = [
        dict(case='battle_menu_controlled', status='fixture_rejected_before_write',
             reason='Expected live original Speyer mobile ship, but fleet5 mobile pointer is zero.',
             evidence=str(ROOT/'battle_menu_rejected_precondition.json')),
        dict(case='battle_menu_followup', status='audit_runner_error',
             reason='Empty generated command prefix included a blank JSON line. Fixed; separate timing follow-up completed. No game defect inferred.'),
    ]
    save(ROOT/'coverage_matrix.json',dict(completed_sessions=outcomes, unsuccessful_attempts=failures,
        exact_user_tutorial_crowd_state_replayed=False, full_routes_completed=False,
        battle_victory_and_duel_completed=True, all_battle_or_duel_outcomes_covered=False,
        wireless_match_completed=False, hardware_verified=False))
    scripts = sorted(Path('scripts').glob('*audit*20261027.py'))
    scripts += [Path('scripts/audit_patch_memory_20261027.py'),Path('scripts/inspect_patch_runtime_memory_20261027.py'),
                Path('scripts/trace_patch_construction_20261027.py'),Path('scripts/restore_audit_fixtures_20261027.py'),
                Path('scripts/rebuild_remaining_audit_fixtures_20261027.py')]
    receipt = dict(target=target, ROM_and_registry_and_canonical_unchanged=True,
        additional_confirmed_ROM_defects=0, prior_Square_collision_repair_still_valid=True,
        completed_sessions=len(outcomes), representative_sessions=len(outcomes)-1,
        completed_session_frames=sum(r['frames'] for r in outcomes),
        same_frame_memory_snapshots=sum(len(r) for r in memory['cases'].values()),
        captured_attempts_in_memory_check=len(memory['cases']),
        compared_bytes_per_snapshot=memory['compared_bytes_per_snapshot'],
        unexpected_mutations=memory['unexpected_mutations'],
        test_files_passed=sum(r['exit_code']==0 for r in test_results),
        test_files_blocked_missing_inputs=sum(r['exit_code']!=0 for r in test_results),
        fully_passing_file_test_outcomes=test_summary['fully_passing_file_outcomes'],
        blocked_file_test_outcomes=test_summary['partially_blocked_file_outcomes'],
        exact_historical_fixtures_restored=len(recovered),
        reconstruction_copies_moved_and_hash_verified=len(moved),
        original_clean_ROM_sha256=sha('work/clean.nds'),
        build_replacement_stages=trace['ARM9_replacement_stages'],
        final_construction_writer_ranges=len(trace['final_changed_byte_writer_ranges']),
        current_ROM_duel_victory_and_aftermath_observed=True,
        visual_review='All representative sheets plus identified direct screenshots reviewed; not every captured frame.',
        source_hashes={str(p):sha(p) for p in sorted(set(scripts))},
        broad_release_certification=False, cosmetic_work_paused=True, promotion_performed=False,
        retention_preview='Refused pre-existing C-path pin outside approved physical folders; no deletion attempted.')
    save(ROOT/'final_audit_receipt.json',receipt)
    print(json.dumps({k:receipt[k] for k in ['completed_sessions','completed_session_frames','same_frame_memory_snapshots',
        'test_files_passed','test_files_blocked_missing_inputs','additional_confirmed_ROM_defects']},indent=2))


if __name__ == '__main__':
    main()
