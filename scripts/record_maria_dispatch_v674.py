"""Retain corrected source ownership and explicit transition gaps, not a false close."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_maria_opening_v674 import ROOT
from scripts.record_regional_ui_v616 import checked_copy
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V674 Maria source dispatch')
DOC = Path('docs/maria_dispatch_v674_checkpoint.md')
KEY = 'actual_Maria_New_Game_evstill084_and_two_FLS_requests_correct_movie_mapping_and_reveal_gap_v674'
SCRIPTS = ('scripts/prepare_maria_opening_v674.py', 'scripts/run_maria_opening_v674.py',
           'scripts/factory_filter_controls_v674.py', 'scripts/run_maria_dispatch_v674.py',
           'scripts/inspect_movie_operand_v674.py', 'scripts/verify_maria_dispatch_v674.py',
           'scripts/record_maria_dispatch_v674.py', 'scripts/verify_maria_archive_v674.py',
           'scripts/observe_graphic_paints_v669.py')


def copy(source, target):
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    checked_copy(source, target)


def main():
    pp = ROOT / 'proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_maria_dispatch_v674.py').read_bytes())
    assert proof['primitive_records'] == 19196 and proof['ordinary_primitive_entries'] == 19194
    assert len(proof['Maria_actual_two_source_bound_court_backgrounds']) == 2
    assert [(r['frame'], r['movie_index']) for r in proof['FLS_factory_requests']] == [(16, 0), (559, 28)]
    operand = read(ROOT / 'movie_operand_proof.json')
    assert operand['script_sha256'] == sha(Path('scripts/inspect_movie_operand_v674.py').read_bytes())
    assert len(operand['scans']['clean']) == len(operand['scans']['current']) == 20
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'status': 'actual_source084_two_stable_views_verified_initial_movie_mapping_retracted_reveal_painter_open',
        'three_terminal4000_frame_cold_boots_pilot_observed_baseline': True,
        'all14_whole_two_screen_pairs11_pilot_states_and_terminal_RAM_exact': True,
        'existing_authorized_system_unlock_save_not_earned_unlock': True,
        'all98304_two_stable_court_upper_pixels_and_complete_resident_source_parts_exact': True,
        'blank3700_and_incomplete_striped_reveal3800_separately_retained_not_full_art_credit': True,
        'actual_two_original_FLS_factory_requests0_and28_no26_in_this_schedule': True,
        'factory_first12_fields_only_guard13_inapplicable_blitter_fields_explicit': True,
        '512_clean_current_original_movie_operand_fragment_cases_and40_container_byte_searches': True,
        'M26_character_story_ownership_or_global_nonuse_not_proven': True,
        'original_reveal_painter_timing_and_full_Maria_opening_still_open': True,
        'six_control_contexts_other_legacy_and_restoration_gates_open': True,
        'all18_plaques_incomplete22_historical_requirements_exact': True,
        'ROM_patch_registry_canonical_and_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k != 'current_goal_turn_classification')
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(path, data)
    heading = '## V674: Maria actual still-image source and corrected movie hypothesis'
    addition = ('Three terminal4000-frame cold boots use original New Game with the existing '
        'authorized system-unlock save. All14 current two-screen pairs,11 pilot states and full '
        'terminal RAM match. Native factory requests are only0 and28; the unsupported Maria=M26 '
        'assumption is retracted. Actual court evstill084 has complete resident palette/indices '
        'and98304 displayed pixels exact across3900/4000. Blank3700 is separate;3800 has17245 '
        'source cells still black during a horizontal-blinds reveal. Its full software/display '
        'match is diagnostic, not independent expected painting; original reveal/timing remain '
        'open. All512 packed-movie fragment cases match clean/current;40 container byte scans '
        'do not turn speaker-control/Latin byte coincidences into decoded triggers.19196 trace '
        'records include19194 guarded primitives and two request-register records with explicit '
        'inapplicable blitter guard13. Failed assumptions retained, no ROM or native result '
        'substitution. M26 ownership, full Maria opening, six controls and broader graphics '
        'remain open. V666/patch/registry/pointers unchanged; all18 plaques incomplete and22 '
        'scopes exact. See [V674 checkpoint](maria_dispatch_v674_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    folders = [CAP / 'maria_opening_v674_pilot', CAP / 'maria_dispatch_v674_observed', CAP / 'maria_dispatch_v674_baseline']
    for folder in folders:
        for source in folder.rglob('*'):
            if source.is_file() and source.suffix.lower() in ('.json', '.png', '.bin'):
                copy(source, ARCHIVE / 'runs' / folder.name / source.relative_to(folder))
    for source in (DOC, *map(Path, SCRIPTS)):
        copy(source, ARCHIVE / 'sources' / source.name)
    for source in ROOT.rglob('*'):
        if source.is_file():
            copy(source, ARCHIVE / 'analysis' / source.relative_to(ROOT))
    for name in frozen:
        copy(Path('translations') / name, ARCHIVE / 'audits' / name)
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        copy(Path('docs') / name, ARCHIVE / 'docs' / name)
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': pre['candidate_sha256'],
        'all_three_runs_terminal': True, 'source_scripts': {p: sha(Path(p).read_bytes()) for p in SCRIPTS},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'no_M26_Maria_mapping_global_nonuse_or_full_reveal_completion_claim': True, 'full_goal_complete': False})
    print('V674 source dispatch, stable courts and retained reveal gap archived; three audits/four docs updated;18/22 retained.')


if __name__ == '__main__':
    main()
