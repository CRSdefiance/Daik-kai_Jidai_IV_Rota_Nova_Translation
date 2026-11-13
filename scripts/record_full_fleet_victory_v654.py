"""Archive completed victory evidence while preserving every wider graphics gate."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/full_fleet_victory_v654')
DOC = Path('docs/full_fleet_victory_v654_checkpoint.md')
KEY = 'original_five_ship_victory_rewards_all5_cargo_positions_and_complete_Spoils_contexts_v654'
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V654 Five ship victory')


def copy(source, destination):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    checked_copy(source, destination)


def main():
    pp = ROOT / 'proof.json'
    proof, pre = read(pp), read(ROOT / 'replay_preflight.json')
    assert proof['script_sha256'] == sha(Path('scripts/verify_full_fleet_victory_v654.py').read_bytes())
    assert proof['terminal28400_cold_boot_no_savestate_and_no_callback_errors']
    assert len(proof['all12_complete4096_pixel_Spoils_banners']) == 12
    assert len(proof['all21_original_cargo_headings_and_selected_ship_fields']) == 21
    assert len(proof['complete_nine_actual_reward_and_warning_text_planes']) == 9
    assert proof['native_funds_increments4200_then75_exact'] and not proof['full_goal_complete']
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        data = read(Path('translations') / name)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    scripts = ['scripts/run_full_fleet_victory_v654.py', 'scripts/verify_full_fleet_victory_v654.py',
               'scripts/record_full_fleet_victory_v654.py', 'scripts/native_full_fleet_proximity_v653.py']
    for path in [DOC, *ROOT.glob('*.json'), *ROOT.glob('*.txt'), *ROOT.glob('*.log'), *map(Path, scripts)]:
        copy(path, ARCHIVE / path.name)
    report = read(proof['report'])
    assert sha(Path(proof['report']).read_bytes()) == proof['report_sha256']
    copy(proof['report'], ARCHIVE / 'terminal_replay_capture_report.json')
    for shot in report['frames_captured']:
        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
        copy(shot['path'], ARCHIVE / 'terminal_replay' / Path(shot['path']).name)
    interrupted = Path(pre['original_interrupted_output'])
    assert not (interrupted / 'capture_report.json').exists()
    copy(interrupted / 'navigation_command_journal.json', ARCHIVE / 'interrupted_exploration' / 'navigation_command_journal.json')
    for path in interrupted.glob('frame_*.png'):
        copy(path, ARCHIVE / 'interrupted_exploration' / path.name)
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'terminal28400_frame_fresh_cold_boot84_unmodified_capture_records82_unique_states': True,
        'earlier_absent_process_and_missing_report_preserved_as_interrupted_not_completed': True,
        'same_pre_Y41_whole_screens_original_Y_automatic_duel_reaches_capture_and_victory': True,
        'two_coordinate_only_approach_fixtures_no_health_enemy_crew_or_result_writes': True,
        'five_original_surviving_named_ships_and_native4200_then75_coin_increments': True,
        'nine_complete_text_planes21_complete_headings12_whole4096_pixel_Spoils_banners': True,
        'all5_actual_cargo_positions_and_full_R_wrap_warning_cancel_and_accept': True,
        'one_hover_frame_not_counted_as_whole_banner_or_complete_tooltip_clearance': True,
        'no_comprehensive_permanent_cargo_acquisition_or_new_normal_Save_claim': True,
        'bounded82_frame_miniature_search_does_not_close_six_actual_parent_requirements': True,
        'all18_original_plaques_incomplete22_historical_scopes_exact': True,
        'ROM_patch_manifest_registry_canonical_and_all_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'no_new_guide_candidate_or_publication_credit': True,
        'full_goal_complete': False}
    for name in frozen:
        path = Path('translations') / name
        data = read(path)
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(path, data)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
    heading = '## V654: original five-ship victory, rewards and complete Spoils contexts'
    addition = ('A fresh V653 cold boot repeats the same two coordinate-only approach fixtures '
        'and reaches victory using the original Y automatic duel control. The first process '
        'ended without a report;its handle/process absence was verified and its evidence '
        'retained as interrupted. A new same-command replay terminates normally at28400 '
        'with84 capture records/82 unique states. All41 pre-Y screens match the earlier '
        'loss path;all five ships survive. Original funds rise25975 to30175 to30250, '
        'matching4200+75 rewards. Nine complete native text planes,21 ship headings '
        'and12 whole4096-pixel Spoils banners pass. All5 cargo positions,wrap and '
        'Finish/cancel/accept are exercised. A hover-occluded banner receives no whole '
        'credit;no full cargo-acquisition or new normal Save claim. Six small-control '
        'parents and wider graphics gates remain open. No ROM/patch/registry/pointer '
        'change;all18 plaques incomplete and22 scopes exact. Evidence on E;full goal active. '
        'See [V654 checkpoint](full_fleet_victory_v654_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': pre['candidate_sha256'],
        'completed_replay_and_interrupted_exploration_are_separate': True,
        'RAM_native_exports_and_original_reports_retained_at_original_E_paths': True,
        'two_coordinate_only_fixtures_disclosed_no_earned_voyage_or_full_route_claim': True,
        'scripts': {p: sha(Path(p).read_bytes()) for p in scripts},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'}, 'full_goal_complete': False})
    print('V654 archived; all three audits/four progress documents updated; ROM and every release pointer unchanged.')


if __name__ == '__main__':
    main()
