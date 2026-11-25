"""Archive actual indirect resource tracing without closing unresolved controls."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.inspect_resource_dispatch_v668 import ROOT
from scripts.record_regional_ui_v616 import checked_copy
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/resource_dispatch_v668_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V668 Resource dispatch')
KEY = 'actual53157_resource_requests11444_indirect_Frame_views_six_selected_rectangles_and_native_contracts_v668'
SCRIPTS = ('scripts/inspect_resource_dispatch_v668.py', 'scripts/observe_resource_dispatch_v668.py',
           'scripts/run_resource_dispatch_v668.py', 'scripts/verify_resource_dispatch_v668.py',
           'scripts/record_resource_dispatch_v668.py', 'scripts/inspect_committed_gpu_v646.py',
           'scripts/trace_resource_owner_tables_v585.py', 'scripts/verify_frame_style_tiles_v584.py')


def copy(source, destination):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    checked_copy(source, destination)


def main():
    proof_path = ROOT / 'proof.json'
    proof, pre = read(proof_path), read(ROOT / 'preflight.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_resource_dispatch_v668.py').read_bytes())
    assert proof['resource_request_records'] == 53157 and proof['all_Frame_requests'] == 31698
    assert proof['actual_Frame_virtual_getter_requests'] == 11444
    assert len(proof['native_source_rectangle_controls']) == 16 and len(proof['native_view_unwind_controls']) == 3
    assert not proof['full_goal_complete']
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        data = read(Path('translations') / name)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k != 'current_goal_turn_classification')
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    entry = {'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'status': 'actual_indirect_resource_callers_and_selected_view_rectangles_verified_six_controls_still_open',
        'three_terminal24100_frame_New_Game_runs_no_savestate_or_gameplay_fixtures': True,
        'all178_observer_baseline_whole_two_screen_pairs_exact': True,
        'seven_native_host_filter_controls_and_three_original_view_unwind_controls': True,
        '53157_actual_requests21_initialized_owners7_original_call_sites_validated': True,
        'all53157_initial_fields_exact_across_both_observer_versions': True,
        '31698_actual_Frame_requests11444_through_generic_virtual_view_getter': True,
        'two_original_corner_copy_parent_return_sites_and_six_selected_XYWH_rectangles_bound': True,
        'all11444_selected_rectangles_exclude_five_miniature_caption_cells': True,
        'twelve_actual_geometry_and_four_positive_native_parent_contracts_pass': True,
        'Confirm_not_requested_in_this_schedule_not_global_nonuse': True,
        'cached_direct_views_other_Frame_paths_other_schedules_and_all_six_control_parents_open': True,
        'no_individual_paint_retirement_palette_final_pixels_or_full_goal_credit_from_request_alone': True,
        'all18_original_plaques_incomplete22_historical_scopes_exact': True,
        'ROM_patch_registry_and_release_pointers_unchanged': True, 'archive': str(ARCHIVE), 'full_goal_complete': False}
    for name in frozen:
        target = Path('translations') / name
        data = read(target)
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(target, data)
    heading = '## V668: actual indirect resource callers and selected frame rectangles'
    addition = ('Three ordinary24100-frame V666 New Game runs finish normally. A host-only '
        'read-only filter temporarily replaces one pinned interpreter opcode pointer and '
        'restores it; original handler entry/arguments/host state are preserved. Seven native '
        'host controls pass and all178 sampled observer/baseline whole-screen pairs match. '
        'Both trace versions have53157 identical original entry records across21 initialized '
        'owners and7 validated call sites. Frame has31698 requests;11444 pass through the '
        'generic virtual getter to two original copy parents. Complete saved return slots '
        'and six selected source XYWHs are bound; all avoid the five miniature cells. Three '
        'native unwind and16 original parent geometry/positive controls pass with disclosed '
        'cache/pixel-call bridges. One early checker confused current LR with saved parent '
        'LR; its failure is retained and source/native stack offsets resolve it. No Confirm '
        'request in this schedule is not global non-use. Cached-direct views, other Frame '
        'paths/schedules and all six actual control parents remain open. No new pixel-paint '
        'or guide credit from a resource request. ROM/patch/registry/pointers unchanged;all18 '
        'plaques incomplete and22 scopes exact. Evidence archived on E;full goal active. See '
        '[V668 checkpoint](resource_dispatch_v668_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        target = Path('docs') / name
        text = target.read_text(encoding='utf-8')
        if heading not in text:
            target.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    reports = []
    for tag in ('observed', 'baseline', 'observed_stack'):
        folder = CAP / ('resource_dispatch_v668_newgame_' + tag)
        rp = folder / 'capture_report.json'
        receipt = next(r for r in proof['reports'] if r['tag'] == tag)
        assert sha(rp.read_bytes()) == receipt['sha256']
        reports.append(receipt)
        for source in folder.rglob('*'):
            if source.is_file() and source.suffix.lower() in ('.json', '.png', '.bin'):
                copy(source, ARCHIVE / 'runs' / tag / source.relative_to(folder))
    for source in [DOC, *map(Path, SCRIPTS)]:
        copy(source, ARCHIVE / 'sources' / source.name)
    for source in ROOT.rglob('*'):
        if source.is_file():
            copy(source, ARCHIVE / 'analysis' / source.relative_to(ROOT))
    for name in frozen:
        copy(Path('translations') / name, ARCHIVE / 'audits' / name)
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        copy(Path('docs') / name, ARCHIVE / 'docs' / name)
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': pre['candidate_sha256'], 'reports': reports,
        'all_three_runs_terminal': True, 'no_gameplay_fixtures_or_savestate': True,
        'host_diagnostic_table_slot_restored_and_original_DLL_file_unchanged': True,
        'source_scripts': {p: sha(Path(p).read_bytes()) for p in SCRIPTS},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'no_six_parent_completion_or_guide_publication_inferred': True, 'full_goal_complete': False})
    print('V668 traces/native contracts/screens archived; three audits/four documents updated;18/22 scopes exact.', flush=True)


if __name__ == '__main__':
    main()
