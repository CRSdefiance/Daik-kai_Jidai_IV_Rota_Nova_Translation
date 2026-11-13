"""Archive the five-label menu pass and retain all unresolved graphics gates."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_tavern_schemes_v624 import CAP, ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/tavern_schemes_v624_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V624 Tavern scheme menus')
KEY = 'actual_hidden_Tavern_scheme_five_menu_labels_v624'


def main():
    proof_path = ROOT / 'release_proof.json'
    proof = read(proof_path)
    assert proof['candidate_sha256'] == sha(ROM.read_bytes())
    assert proof['script_sha256'] == sha(Path('scripts/verify_tavern_schemes_v624.py').read_bytes())
    assert len(proof['complete_four_row_menus_all_eight_selection_states']) == 32
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    files = [DOC, ROM.with_suffix('.manifest.json'), Path('translations/tavern_scheme_labels_v1.json'),
             Path('translations/tavern_scheme_labels_review_v1.json'),
             Path('dk4tool/patch/tavern_scheme_labels.py'), Path('scripts/native_strategist_fixture_v624.py'),
             Path('scripts/prepare_tavern_schemes_v624.py'), Path('scripts/verify_tavern_schemes_v624.py'),
             Path(__file__)]
    for path in files:
        checked_copy(path, ARCHIVE / path.name)
    for name in ('release', 'patch', 'preservation', 'native_label_fit', 'expert_fixture'):
        checked_copy(ROOT / (name + '_proof.json'), ARCHIVE / (name + '_proof.json'))
    screenshots = []
    for label, root, frames in (
        ('V623_Japanese_control', CAP / 'tavern_schemes_v623_expert', (4400, 6400, 6000, 8000)),
        ('V624_menu_and_open_dialogue_defects', CAP / 'tavern_schemes_v624_expert', range(3200, 9202)),
        ('V624_ordinary', CAP / 'tavern_schemes_v624_market', None)):
        report_path = root / 'capture_report.json'
        report = read(report_path)
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        checked_copy(report_path, ARCHIVE / (label + '_capture_report.json'))
        journal = root / 'navigation_command_journal.json'
        if journal.exists():
            checked_copy(journal, ARCHIVE / (label + '_navigation_journal.json'))
        shots = {x['frame']: x for x in report['frames_captured']}
        for frame, shot in sorted(shots.items()):
            if frames is not None and frame not in frames:
                continue
            assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
            target = ARCHIVE / f'{label}_{frame:06d}_UNMODIFIED_NATIVE.png'
            checked_copy(shot['path'], target)
            screenshots.append({'path': str(target), 'sha256': shot['PNG_sha256'], 'frame': frame,
                                'ROM_sha256': report['ROM_sha256'], 'unmodified_capture': True,
                                'uses_disclosed_room_experience_and_calendar_fixture': label != 'V624_ordinary',
                                'dialogue_defects_still_open': frame in (6000, 8000)})
    save(ARCHIVE / 'provenance.json', {
        'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'], 'screenshots': screenshots,
        'full_native_RAM_exports_retained_in_Generated_runs': True,
        'publication_approved': False, 'full_goal_complete': False,
        'files': {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir() if p.is_file() and p.name != 'provenance.json'}})
    entry = {
        'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'], 'profile': proof['profile'],
        'patch_sha256': proof['patch_sha256'], 'status': 'experimental_five_menu_labels_verified_related_dialogue_open',
        'five_complete_English_labels_all8_selection_states_32_source_and_framebuffer_masks_pass': True,
        'only_source_owned_text_and_five_pointers_no_pool_or_code_growth': True,
        'uses_disclosed_room_XP_and_three_day_calendar_fixture': True,
        'earned_refit_qualifications_experience_time_or_campaign_progress_not_claimed': True,
        'nineteen_ordinary_no_fixture_screens_exact_V623': True,
        'all470_batches114_accepted_layers921_graphics57_embedded_extents_and_exact_patch_retained': True,
        'related_dialogue_and_all_four_command_contexts_still_open': proof['command_context_followups'],
        'all18_original_plaques_incomplete_all22_historical_objects_retained': True,
        'broader_graphics_material_legacy_village_Confirm_and_miniature_gates_open': True,
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
                       'five_Tavern_scheme_menu_labels_verified_related_dialogue_open': True,
                       'broader_graphics_gates_remain_open': True})
        data['latest_compiled_experimental_candidate_with_inherited_native_gap'] = latest
        data['current_goal_turn_classification'] = 'progress'
        save(path, data)
        current = read(path)
        assert all(current[k] == v for k, v in protected.items())
        assert current.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert current.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    heading = '## V624: hidden Tavern scheme menus and newly exposed dialogue follow-ups'
    text = '''

Five complete labels now read Schemes, Lure Fleet, Forge Papers, Bad Rumors and
Bribe. Source-owned spans and five pointers are repacked without code/pool growth.
Two original-input cold boots use a disclosed Gerhard room assignment, one XP word
and three calendar days fixture. All8 menu selection states pass32 complete native
source-view/framebuffer font masks. Twelve outside-menu frames and19 ordinary
no-fixture New Game/Market frames match V623. Full470/114 stack,921/57 preservation
and exact clean-ROM patch reconstruction pass; only ARM9 changes. Experimental
V624 SHA2564eaf22d1f69f6eb49f624a557698a281bd6eedb8b396023007aebcdda35bee63.

Do not close the surrounding command dialogue: the original introduction909 still
splits words, and Bribe still expands Japanese from the separate general scheme
name table. Both reproduce in V623. Repair the later portrait-wrap family and all
four general scheme-name bindings, then test every command entry/cancel context.
All18 plaques incomplete/all22 historical scopes exact; canonical and verified
pointers retained. All broader graphics gates remain open; goal active. ROM,
patch, manifest and unmodified evidence are on E. See
[V624 checkpoint](tavern_schemes_v624_checkpoint.md).
'''
    for name in ('todo', 'translation_progress', 'known_issues', 'release_build'):
        path = Path('docs') / (name + '.md')
        content = path.read_text(encoding='utf-8')
        if heading not in content:
            path.write_text(content.rstrip() + '\n\n' + heading + '\n' + text, encoding='utf-8')
    print(f'Archived {len(screenshots)} unmodified captures; all three audits updated,18/22 original scopes and canonical retained.')


if __name__ == '__main__':
    main()
