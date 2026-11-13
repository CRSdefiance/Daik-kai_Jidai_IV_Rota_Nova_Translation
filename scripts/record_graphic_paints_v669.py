"""Archive exact source-file bindings and retain all unresolved graphics scopes."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.inspect_graphic_paints_v669 import ROOT
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V669 Indexed image calls')
DOC = Path('docs/graphic_paints_v669_checkpoint.md')
KEY = 'actual407770_indexed_primitive_entries_whole_Frame_Marker_binding_cached_views_and828_baseline_pairs_v669'
SCRIPTS = ('scripts/inspect_graphic_paints_v669.py', 'scripts/observe_graphic_paints_v669.py',
           'scripts/run_graphic_paints_v669.py', 'scripts/verify_graphic_paints_v669.py',
           'scripts/record_graphic_paints_v669.py', 'scripts/observe_resource_dispatch_v668.py',
           'scripts/inspect_committed_gpu_v646.py', 'scripts/verify_frame_style_tiles_v584.py')


def copy(source, destination):
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    checked_copy(source, destination)


def main():
    pp = ROOT / 'proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_graphic_paints_v669.py').read_bytes())
    assert len(proof['reports']) == 6 and len(proof['native_host_controls']) == 13
    assert sum(c['records'] for c in proof['cases']) == 407770
    assert sum(c['binding_counts'].get('1', 0) for c in proof['cases']) == 126896
    assert sum(c['binding_counts'].get('6', 0) for c in proof['cases']) == 5899
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        data = read(Path('translations') / name)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k != 'current_goal_turn_classification')
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    save(ROOT / 'retained_development_assumptions.json', {
        'shared_metadata': 'Complete source census finds only __frame.pxl and __marker.pxl sharing this exact20-byte header. Initial live comparisons correctly refuse to bind Marker as Frame.',
        'initial_shared_header_unknowns': {'newgame': 4559, 'equipment': 1340},
        'resolution': 'Fresh complete Marker byte comparisons resolve every one as exact current Marker; all earlier fields and screenshots remain exact.',
        'native_control_expectation_failure': 'After adding Marker fallback, a corrupted Frame with shared metadata correctly matches neither complete atlas and receives joint unknown ID7, rather than legacy initial ID3. Expected scratch classification corrected; no source or ROM bytes changed.',
        'all_initial_traces_contracts_observer_and_runner_sources_retained': True,
        'no_initial_candidate_automatically_counted_as_Frame_corruption': True, 'full_goal_complete': False})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'status': 'original_primitive_entries_and_exact_source_files_verified_six_controls_still_open',
        'six_terminal_runs_four_observed_two_unmodified_baselines_no_gameplay_fixtures': True,
        'all828_sampled_two_screen_observer_baseline_pairs_exact': True,
        'thirteen_native_host_ABI_bounds_complete_file_and_last_byte_controls_pass': True,
        'all407770_entry_registers_descriptors_headers_flags_repeat_exact': True,
        'Frame126896_and_Marker5899_calls_bind_complete35444_byte_files': True,
        'all5899_shared_header_candidates_resolved_by_whole_Marker_comparison': True,
        'all_Frame_selected_source_footprints_exclude_five_miniature_cells_in_these_schedules': True,
        'Confirm_not_selected_through_these_three_primitives_in_these_schedules_not_global_nonuse': True,
        'cached_direct_views_observed_without_requiring_resource_getter_request': True,
        'entry_trace_does_not_prove_individual_paint_return_or_complete_display_per_call': True,
        'all_six_control_contexts_other_schedules_primitives_and_wider_graphics_still_open': True,
        'all18_original_plaques_incomplete22_historical_scopes_exact': True,
        'ROM_patch_registry_canonical_and_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    for name in frozen:
        target = Path('translations') / name
        data = read(target)
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(target, data)
    heading = '## V669: direct indexed-image calls and exact Frame/Marker source binding'
    addition = ('The unchanged V666 ROM completes six cold boots: four observed and two '
        'unmodified baselines for New Game/town and equipment cursor sequences. All828 sampled '
        'two-screen pairs match. One host-only interpreter slot observes original scaled, '
        'corner and tiled entry arguments, including cached-direct views. Thirteen native host '
        'controls preserve ABI/source bytes and reject last-byte corruption and invalid pointers. '
        'All407770 initial entry records repeat with identical registers/descriptors/headers/flags. '
        'The exact20-byte Frame/Marker header collision is resolved through whole35444-byte '
        'comparisons:126896 Frame and5899 Marker entries bind fully, with no unresolved shared '
        'candidate. All selected Frame footprints avoid five miniature cells; Confirm is not '
        'selected through these three primitives in these schedules. No individual paint-return, '
        'complete pixel-per-call or global non-use claim follows. All six actual control contexts, '
        'other schedules/primitives and broader graphics gates remain open. No ROM/patch/registry/'
        'pointer change or guide promotion;all18 plaques incomplete and22 scopes exact. Evidence '
        'archived on E;full goal active. See [V669 checkpoint](graphic_paints_v669_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        target = Path('docs') / name
        text = target.read_text(encoding='utf-8')
        if heading not in text:
            target.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for receipt in proof['reports']:
        folder = Path(receipt['path']).parent
        assert sha(Path(receipt['path']).read_bytes()) == receipt['sha256']
        for source in folder.rglob('*'):
            if source.is_file() and source.suffix.lower() in ('.json', '.png', '.bin'):
                copy(source, ARCHIVE / 'runs' / folder.name / source.relative_to(folder))
    for source in [DOC, *map(Path, SCRIPTS)]:
        copy(source, ARCHIVE / 'sources' / source.name)
    for source in ROOT.rglob('*'):
        if source.is_file():
            copy(source, ARCHIVE / 'analysis' / source.relative_to(ROOT))
    for name in frozen:
        copy(Path('translations') / name, ARCHIVE / 'audits' / name)
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        copy(Path('docs') / name, ARCHIVE / 'docs' / name)
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': pre['candidate_sha256'], 'reports': proof['reports'],
        'all_six_runs_terminal': True, 'four_observed_two_baselines': True,
        'private_process_opcode_slot_restored_original_DLL_unchanged_no_game_state_writes': True,
        'source_scripts': {p: sha(Path(p).read_bytes()) for p in SCRIPTS},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'no_global_nonuse_six_context_completion_or_guide_publication_inferred': True, 'full_goal_complete': False})
    print('V669 six runs/full bindings archived; three audits/four documents updated;18/22 scope preserved.', flush=True)


if __name__ == '__main__':
    main()
