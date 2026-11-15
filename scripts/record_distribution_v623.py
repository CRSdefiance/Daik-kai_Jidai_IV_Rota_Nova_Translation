"""Archive original reward/distribution contexts and retain the full audit scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_plaza_distribution_v623 import CAP, ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/post_battle_distribution_v623_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V623 Spoils and distribution')
KEY = 'actual_Spoils_and_Square_Distributed_Goods_complete_contexts_v623'


def main():
    proof_path = ROOT / 'release_proof.json'
    proof = read(proof_path)
    spoils_path = Path('work/analysis/post_battle_cargo_v622/release_proof.json')
    spoils = read(spoils_path)
    assert proof['candidate_sha256'] == sha(ROM.read_bytes())
    assert proof['script_sha256'] == sha(Path('scripts/verify_plaza_distribution_v623.py').read_bytes())
    assert spoils['script_sha256'] == sha(Path('scripts/verify_post_battle_cargo_v622.py').read_bytes())
    assert len(proof['actual_complete_menu_rows_two_selection_states']) == 4
    assert len(proof['complete_Distributed_Goods_banners_original_mode2']) == 3
    assert len(spoils['five_complete_ordinary_Spoils_banners']) == 5
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    files = [DOC, ROM.with_suffix('.manifest.json'), Path('translations/plaza_distribution_label_v1.json'),
             Path('dk4tool/patch/plaza_distribution_label.py'), Path('scripts/native_missionary_fixture_v623.py'),
             Path('scripts/prepare_plaza_distribution_v623.py'), Path('scripts/verify_post_battle_cargo_v622.py'),
             Path('scripts/verify_plaza_distribution_v623.py'), Path(__file__),
             Path('work/analysis/post_battle_cargo_v622/istanbul_prefix.json')]
    for path in files:
        checked_copy(path, ARCHIVE / path.name)
    for prefix, source in (
        ('V622_spoils', spoils_path), ('V623_distribution', proof_path),
        ('V623_patch', ROOT / 'patch_proof.json'), ('V623_preservation', ROOT / 'preservation_proof.json'),
        ('V623_native_label_fit', ROOT / 'native_label_fit_proof.json'),
        ('V623_source_fixture', ROOT / 'source_missionary_fixture_proof.json'),
        ('V623_fixture_negatives', ROOT / 'fixture_negative_controls.json')):
        checked_copy(source, ARCHIVE / (prefix + '_proof.json'))
    screenshots = []
    runs = (
        ('post_battle_Spoils', CAP / 'post_battle_cargo_v622_actual', range(24800, 30402)),
        ('V621_Japanese_control', CAP / 'distribution_menu_v621_fixture', (4000, 4400)),
        ('V623_distribution', CAP / 'distribution_menu_v623_fixture', range(3200, 8002)),
        ('V623_ordinary', CAP / 'plaza_distribution_v623_market', None))
    for label, root, selected in runs:
        path = root / 'capture_report.json'
        run = read(path)
        assert run['cold_boot'] and not run['savestate_loaded'] and not run['callback_errors']
        checked_copy(path, ARCHIVE / (label + '_capture_report.json'))
        journal = root / 'navigation_command_journal.json'
        if journal.exists():
            checked_copy(journal, ARCHIVE / (label + '_navigation_journal.json'))
        shots = {r['frame']: r for r in run['frames_captured']}
        for frame, row in sorted(shots.items()):
            if selected is not None and frame not in selected:
                continue
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
            target = ARCHIVE / f'{label}_{frame:06d}_UNMODIFIED_NATIVE.png'
            checked_copy(row['path'], target)
            screenshots.append({'path': str(target), 'frame': frame, 'sha256': row['PNG_sha256'],
                                'ROM_sha256': run['ROM_sha256'], 'context': label,
                                'synthetic_ship_proximity_used': label == 'post_battle_Spoils',
                                'synthetic_Chapel_Manuel_assignment_used': label in ('V621_Japanese_control', 'V623_distribution'),
                                'unmodified_capture': True})
    save(ARCHIVE / 'provenance.json', {
        'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'],
        'screenshots': screenshots, 'full_native_RAM_exports_retained_in_Generated_runs': True,
        'publication_approved': False, 'full_goal_complete': False,
        'files': {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir() if p.is_file() and p.name != 'provenance.json'}})
    entry = {
        'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'spoils_proof': str(spoils_path), 'spoils_proof_sha256': sha(spoils_path.read_bytes()),
        'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'], 'profile': proof['profile'],
        'patch_sha256': proof['patch_sha256'], 'status': 'experimental_complete_menu_and_both_original_header_contexts_verified',
        'one_confirmed_Japanese_Square_action_localized_as_Distribute_Goods': True,
        'source_owned_two_string_repack_no_code_pool_or_section_growth': True,
        'five_actual_original_post_battle_Spoils_headers_pixels': 20480,
        'three_actual_original_Distributed_Goods_headers_pixels': 12288,
        'original_unload_select_cancel_finish_and_free_sample_distribution_controls_verified': True,
        'Missionary_context_uses_disclosed_three_byte_Chapel_assignment_fixture': True,
        'normal_refit_qualification_assignment_or_earned_battle_voyage_not_claimed': True,
        'two_menu_selection_states_all_letters_blanks_and_original_96x12_crops_verified': True,
        'all10_post_menu_frames_exact_V621_and19_ordinary_no_fixture_screens_exact': True,
        'all470_batches114_layers921_graphics57_embedded_extents_and_exact_patch_retained': True,
        'all18_original_plaque_entries_incomplete_all22_historical_objects_exact': True,
        'historical_material_source_inference_and_user_review_scope_retained': True,
        'Confirm_five_miniatures_eight_village_cards_legacy_comic_movie_material_gates_still_open': True,
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
        previous = data.get('latest_compiled_experimental_candidate_with_inherited_native_gap', {}).copy()
        previous.update({'candidate': str(ROM), 'sha256': proof['candidate_sha256'], 'profile': proof['profile'],
                         'Spoils_and_Distributed_Goods_original_contexts_verified_with_disclosed_fixtures': True,
                         'broader_graphics_gates_remain_open': True})
        data['latest_compiled_experimental_candidate_with_inherited_native_gap'] = previous
        data['current_goal_turn_classification'] = 'progress'
        save(path, data)
        current = read(path)
        assert all(current[k] == value for k, value in protected.items())
        assert current.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert current.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    heading = '## V623: original Spoils and Square goods-distribution contexts'
    text = '''

V622 verifies nine actual post-battle Spoils owner/file/mode3 bindings, five whole
banners/20480 pixels, normal Unload/Select/cancel/finish and complete warnings on
unchanged V621. The initial301-pixel Armor tooltip overlap is contextual occlusion.

The Square's second action requires goods and a Missionary and was still Japanese.
V623 repacks its exclusive source strings as Trends/Distribute Goods with no code,
pool or section growth. Two old/new cold boots use an explicit three-byte empty
room-to-Chapel/Manuel assignment fixture;no goods,attributes,menu or outcome flags
are injected. Both menu selection states pass complete font masks and original
96x12 source/destination crops. Three original mode2 Distributed Goods banners
pass12288 pixels;normal free-sample distribution consumes the existing two Iron
slots and ten post-menu frames match V621. Nineteen ordinary no-fixture New Game/
Market screens match;all470/114 layers,921/57 preservation and exact clean patch
pass. Current experimental ROM SHA256:
`4c7f8098d2e793514204fe78b54f922cc190daf39502811c51ec43751719b6d9`.

ROM,patch,manifest,unmodified screenshots and source-bound proofs are on E.
Normal refit/qualifications/earned assignment or voyage are not claimed. All18
plaques remain incomplete,all22 historical scopes exact,canonical and verified
pointers unchanged. Confirm/miniatures,village cards,legacy/comic/movie/material
and broader gameplay stay open;goal active. See
[V622/V623 checkpoint](post_battle_distribution_v623_checkpoint.md).
'''
    for name in ('todo', 'translation_progress', 'known_issues', 'release_build'):
        path = Path('docs') / (name + '.md')
        content = path.read_text(encoding='utf-8')
        if heading not in content:
            path.write_text(content.rstrip() + '\n\n' + heading + '\n' + text, encoding='utf-8')
    print(f'Archived{len(screenshots)} unmodified captures;3 audits and progress updated;18/22 scopes/canonical retained.')


if __name__ == '__main__':
    main()
