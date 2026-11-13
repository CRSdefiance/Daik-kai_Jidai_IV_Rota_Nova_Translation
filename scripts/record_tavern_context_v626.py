"""Archive verified scheme contexts, preserve scopes, and retain new follow-ups."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_tavern_scheme_release_v626 import CAP, ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/tavern_scheme_context_v626_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V626 Tavern scheme contexts')
KEY = 'actual_all_four_Tavern_scheme_name_and_queued_voice_contexts_v626'


def main():
    proof_path = ROOT / 'release_proof.json'
    proof = read(proof_path)
    assert proof['candidate_sha256'] == sha(ROM.read_bytes())
    assert proof['script_sha256'] == sha(Path('scripts/verify_tavern_scheme_release_v626.py').read_bytes())
    assert len(proof['all32_complete_menu_masks']) == 32 and len(proof['fourteen_source_bound_dialogue_cases']) == 14
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    files = [DOC, ROM.with_suffix('.manifest.json'),
             Path('translations/tavern_scheme_context_manuscript_v1.json'),
             Path('translations/tavern_scheme_context_v1.json'), Path('translations/tavern_strategist_wrap_v1.json'),
             Path('dk4tool/patch/tavern_scheme_context.py'), Path('dk4tool/patch/tavern_strategist_wrap.py'),
             Path('scripts/native_strategist_fixture_v624.py'), Path('scripts/verify_tavern_scheme_native_v625.py'),
             Path('scripts/verify_tavern_queued_native_v626.py'), Path('scripts/verify_tavern_scheme_release_v626.py'),
             Path(__file__)]
    for source in files:
        checked_copy(source, ARCHIVE / source.name)
    for name in ('release_proof.json', 'queued_native_proof.json', 'patch_proof.json', 'preservation_proof.json',
                 'native_portrait_font_metrics_probe.py'):
        checked_copy(ROOT / name, ARCHIVE / name)
    older = Path('work/analysis/tavern_schemes_v625')
    for name in ('native_context_proof.json', 'two_voice_preview_proof.json', 'source_message_family.json'):
        checked_copy(older / name, ARCHIVE / ('V625_' + name))
    for path in older.glob('message_*_native.png'):
        checked_copy(path, ARCHIVE / path.name)
    screenshots = []
    for label, root, selected in (
        ('V624_old_names_and_wrap', CAP / 'tavern_schemes_v624_expert', (6000, 8000)),
        ('V625_direct_parent_only_not_a_queued_wrap_pass', CAP / 'tavern_schemes_v625_expert', (6000, 8000)),
        ('V626_actual_four_commands', CAP / 'tavern_schemes_v626_expert', range(3200, 24802)),
        ('V626_ordinary', CAP / 'tavern_schemes_v626_market', None)):
        report_path = root / 'capture_report.json'
        run = read(report_path)
        assert run['cold_boot'] and not run['savestate_loaded'] and not run['callback_errors']
        checked_copy(report_path, ARCHIVE / (label + '_capture_report.json'))
        journal = root / 'navigation_command_journal.json'
        if journal.exists():
            checked_copy(journal, ARCHIVE / (label + '_navigation_journal.json'))
        shots = {r['frame']: r for r in run['frames_captured']}
        for frame, shot in sorted(shots.items()):
            if selected is not None and frame not in selected:
                continue
            assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
            target = ARCHIVE / f'{label}_{frame:06d}_UNMODIFIED_NATIVE.png'
            checked_copy(shot['path'], target)
            screenshots.append({'path': str(target), 'sha256': shot['PNG_sha256'], 'frame': frame,
                                'ROM_sha256': run['ROM_sha256'], 'unmodified_capture': True,
                                'disclosed_Gerhard_room_XP_calendar_fixture': label != 'V626_ordinary',
                                'historical_control_not_a_current_pass': label.startswith(('V624_', 'V625_'))})
    save(ARCHIVE / 'provenance.json', {
        'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'], 'screenshots': screenshots,
        'full_native_RAM_and_ITCM_exports_retained_in_Generated_runs': True,
        'publication_approved': False, 'full_goal_complete': False,
        'files': {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir() if p.is_file() and p.name != 'provenance.json'}})
    entry = {
        'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'], 'profile': proof['profile'],
        'patch_sha256': proof['patch_sha256'], 'status': 'experimental_four_scheme_contexts_verified_model_and_content_followups_open',
        'all4_shared_scheme_name_getters_return_complete_English': True,
        'two_source_faithful_opposing_faction_voice_corrections': [918, 920],
        'queued_voice_tables_and_both_original_role_parent_formats_verified': True,
        'all32_menu_masks14_dialogue_cases19_ordinary_regression_screens': True,
        'original_Bribe_commit1000_gold_and3_cancelled_commands_verified': True,
        'V625_direct_portrait_scope_alone_did_not_fix_actual_queued_introduction': True,
        'CP932_I_renderer_model_column_difference_and_897_898_recruitment_content_remain_open': True,
        'all470_batches114_accepted_layers921_graphics57_embedded_extents_and_exact_patch_retained': True,
        'all18_original_plaques_incomplete_all22_historical_objects_retained': True,
        'broader_Confirm_miniature_village_card_legacy_comic_logo_movie_material_gates_open': True,
        'archive': str(ARCHIVE), 'unmodified_screenshots': len(screenshots),
        'full_goal_complete': False, 'canonical_promoted': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        protected = {k: v for k, v in data.items() if k in (
            'candidate', 'candidate_sha256', 'latest_candidate', 'latest_candidate_sha256',
            'current_verified_release_candidate', 'current_verified_release_candidate_sha256', 'latest_graphics_preservation')}
        data[KEY] = entry
        latest = data.get('latest_compiled_experimental_candidate_with_inherited_native_gap', {}).copy()
        latest.update({'candidate': str(ROM), 'sha256': proof['candidate_sha256'], 'profile': proof['profile'],
                       'four_scheme_contexts_and_queued_word_wrap_verified': True,
                       'broader_graphics_gates_remain_open': True})
        data['latest_compiled_experimental_candidate_with_inherited_native_gap'] = latest
        data['current_goal_turn_classification'] = 'progress'
        save(path, data)
        current = read(path)
        assert all(current[k] == value for k, value in protected.items())
        assert current.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert current.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    heading = '## V625/V626: shared scheme names and actual queued Strategist word wrapping'
    text = '''

All four shared scheme names now bind to complete English; two price-mistranslated
voices918/920 correctly ask for an opposing faction. V625's direct portrait tests
passed but did not fix the actual queued introduction. V626 recognizes the two
original role parents and twelve exact source voice tables. Its22008 unchanged
numeric dispatches,115 table/parent controls and160 queued voice layouts pass.
Actual cold boot passes32 menu masks and14 source-bound dialogue checks. Bribe
commits an original type9 object, then charges1000 after its arrangements notice
closes; the three other final confirmations cancel with funds/object exact.
All19 ordinary no-fixture New Game/Market screens match V624;470/114 stack,921/57
preservation and exact patch reconstruction pass. Experimental V626 SHA256:
6164af2ddc9f77475b59a0ec05c10d57a9d99fd3853859e72b0b5fcea8510388.

Ten complete dialogue masks match; four preserve a scoped CP932-I extra-column
host-raster prediction difference as an open calibration check. The actual left
stroke is present and every non-I pixel matches. Do not call those whole-glyph
masks exact. Independent recruitment alternatives897/898 still contain split
English and need a source-faithful repair. All18 original plaques incomplete,
all22 scopes exact,canonical/verified pointers retained;broader graphics gates
and the full goal stay open. ROM,patch,manifest and unmodified evidence are on E.
See [V625/V626 checkpoint](tavern_scheme_context_v626_checkpoint.md).
'''
    for name in ('todo', 'translation_progress', 'known_issues', 'release_build'):
        path = Path('docs') / (name + '.md')
        content = path.read_text(encoding='utf-8')
        if heading not in content:
            path.write_text(content.rstrip() + '\n\n' + heading + '\n' + text, encoding='utf-8')
    print(f'Archived {len(screenshots)} unmodified screenshots; three audits/progress updated;18/22 scopes and canonical retained.')


if __name__ == '__main__':
    main()
