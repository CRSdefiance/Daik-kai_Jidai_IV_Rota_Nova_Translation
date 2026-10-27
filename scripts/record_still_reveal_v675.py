"""Record the resolved Maria reveal comparison without shrinking remaining scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_still_reveal_v675 import ENTRY, OLD_SCAN, ROOT, SCAN
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V675 Maria still reveal')
DOC = Path('docs/still_reveal_v675_checkpoint.md')
KEY = 'Maria_court_original_blinds20_native_paints22_actual_source_frames_two_DMA_boundaries_v675'
SCRIPTS = (
    'scripts/research_still_reveal_v675.py', 'scripts/observe_scene_entry_v675.py',
    'scripts/check_scene_filter_v675.py', 'scripts/run_still_reveal_v675.py',
    'scripts/replay_still_entry_v675.py', 'scripts/run_still_scanlines_v675.py',
    'scripts/observe_still_scanlines_v675.py', 'scripts/observe_transition_scanlines_v659.py',
    'scripts/verify_transition_scanlines_v659.py', 'scripts/research_town_scene_v644.py',
    'scripts/probe_button_prompt_native.py', 'scripts/verify_still_reveal_v675.py',
    'scripts/review_still_reveal_v675.py', 'scripts/record_still_reveal_v675.py',
    'scripts/verify_still_reveal_archive_v675.py')


def copy(source, target):
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    checked_copy(source, target)


def main():
    pp = ROOT / 'proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_still_reveal_v675.py').read_bytes())
    assert proof['specific_V674_blank_and_reveal_comparisons_resolved_without_ROM_change']
    assert len(proof['all20_actual_before_paint_native_replays']) == 20
    assert len(proof['actual_upper_source_and_display_cases']) == 22
    assert len(proof['full_two_screen_pairs']) == 64 and proof['all_source_scanlines'] == 4224
    review = read(ROOT / 'review_packet.json')
    assert review['script_sha256'] == sha(Path('scripts/review_still_reveal_v675.py').read_bytes())
    assert review['sha256'] == sha(Path(review['sheet']).read_bytes())
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': pre['candidate'], 'candidate_sha256': proof['candidate_sha256'],
        'status': 'specific_Maria_court_reveal_independent_native_paints_and_actual_source_RGB_verified',
        'twenty_actual_before_entry_snapshots_native_paints_all9_original_band_phases': True,
        'all983040_native_words_and1081344_actual_upper_RGB_pixels_exact': True,
        'all4224_actual_pre_RenderLine_source_rows64_whole_screen_pairs_and_four_terminal_RAM_states': True,
        'two_mixed_frames_predicted_from_original_native_inputs_and_DMA_sources_no_delay_fit': True,
        'source_engine_switch_and_lower_canvas_edge_ownership_explicit': True,
        'nine_host_selection_and_twelve_prefix_controls_no_emulated_state_writes': True,
        'existing_isolated_system_unlock_save_not_earned_unlock': True,
        'failed_guesses_incomplete_replays_and_main_only_observation_retained': True,
        'no_full_Maria_opening_M26_story_ownership_or_general_hardware_claim': True,
        'six_controls_eight_cards_legacy_comics_restoration_older_records_and_acceptance_open': True,
        'all18_plaques_incomplete22_historical_requirements_exact': True,
        'ROM_patch_registry_canonical_and_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert all(data[k] == value for k, value in pre['all_original_audits_before'][name].items()
                   if k != 'current_goal_turn_classification')
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(path, data)
    heading = '## V675: Maria original blinds painter and actual mixed-frame source reads'
    addition = ('Twenty actual before-entry snapshots reproduce all9 original band phases:983040 '
        'complete native output words exact against independent ROM palette/indices. Three new '
        '4000-frame runs and retained unmodified baseline give64 whole two-screen pairs and four '
        'exact terminal RAM states. The first scanline observer reads the lower/main display here; '
        'its evidence is retained. A private read-only bankC extension verifies4224 actual source '
        'rows and1081344 upper RGB pixels. Two mixed frames are predicted using original native '
        'paint inputs and actual upper DMA positions at rows68/143, not PNG fitting or shifted '
        'frames. The preceding edge belongs to the lower canvas;all8 original writes are bound '
        'rather than waived. Nine host selection and12 prefix controls pass. The specific V674 '
        'reveal gap closes without artwork/ROM changes; full Maria opening,M26 ownership,six '
        'controls,eight cards,legacy/comics/restoration,older checks and acceptance remain open. '
        'V666/patch/registry/pointers unchanged;all18 plaques incomplete and22 scopes exact. '
        'Evidence on E,no guide promotion. See [V675 checkpoint](still_reveal_v675_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        value = path.read_text(encoding='utf-8')
        if heading not in value:
            path.write_text(value.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    baseline = ENTRY.parent / 'maria_dispatch_v674_baseline'
    failed = [ENTRY.parent / f'still_reveal_v675_before_iterator{suffix}' for suffix in ('', '_v2')]
    for folder in (ENTRY, OLD_SCAN, SCAN, baseline, *failed):
        if not folder.exists():
            continue
        for source in folder.rglob('*'):
            if source.is_file() and source.suffix.lower() in ('.json', '.png', '.bin', '.log', '.txt'):
                copy(source, ARCHIVE / 'runs' / folder.name / source.relative_to(folder))
    for source in (DOC, *map(Path, SCRIPTS)):
        copy(source, ARCHIVE / 'sources' / source.name)
    for source in ROOT.rglob('*'):
        if source.is_file():
            copy(source, ARCHIVE / 'analysis' / source.relative_to(ROOT))
    initial = Path('work/analysis/still_reveal_v675.log')
    if initial.exists():
        copy(initial, ARCHIVE / 'analysis' / 'initial_bare_replay.log')
    for name in frozen:
        copy(Path('translations') / name, ARCHIVE / 'audits' / name)
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        copy(Path('docs') / name, ARCHIVE / 'docs' / name)
    for name in ('preflight.json', 'unlock_manifest.json', 'dispatch_inputs.json'):
        source = Path('work/analysis/maria_opening_v674') / name
        copy(source, ARCHIVE / 'inherited_maria_run_contract' / name)
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
        'all_three_new_runs_terminal_and_existing_unmodified_baseline_retained': True,
        'source_scripts': {path: sha(Path(path).read_bytes()) for path in SCRIPTS},
        'files': {str(path.relative_to(ARCHIVE)): sha(path.read_bytes()) for path in ARCHIVE.rglob('*')
                  if path.is_file() and path.name != 'provenance.json'},
        'no_full_Maria_route_M26_ownership_global_timing_or_guide_approval_claim': True,
        'full_goal_complete': False})
    print('V675 original painter/display evidence archived; three audits/four docs updated;18/22 scopes retained.', flush=True)


if __name__ == '__main__':
    main()
