"""Archive Golden Route native evidence; keep historical scopes and open gates."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_golden_plaques_v613 import RECORDS, ROM, ROOT, read, save

DOC = Path('docs/golden_route_plaques_v613_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V613 Golden Route')
KEY = 'actual_Golden_Discovery_and_both_Records_source_frame_release_v613'


def checked_copy(source, destination):
    source, destination = Path(source), Path(destination)
    shutil.copyfile(source, destination)
    assert sha(source.read_bytes()) == sha(destination.read_bytes())


def main():
    proof_path = ROOT / 'release_proof.json'
    proof = read(proof_path)
    assert proof['candidate_sha256'] == sha(ROM.read_bytes())
    assert proof['patch_sha256'] == sha(ROM.with_suffix('.xdelta').read_bytes())
    assert proof['script_sha256'] == sha(Path('scripts/verify_golden_plaques_v613.py').read_bytes())
    assert len(proof['actual_native_bindings']) == 39 and len(proof['actual_whole_composites']) == 63
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    files = [DOC, proof_path, ROOT / 'source_transform_proof.json', ROOT / 'independent_static_proof.json',
             ROOT / 'preservation_proof.json', ROOT / 'source_art_control.json', ROOT / 'fixture_rows.json',
             ROOT / 'initial_header_model_correction.json',
             ROOT / 'complete_records_inputs.json', ROOT / 'complete_sale_inputs.json', ROOT / 'complete_market_inputs.json',
             ROOT / 'build.log', ROOT / 'source_current_repair_sheet.png', ROOT / 'actual_original_current_repair.png',
             ROM.with_suffix('.manifest.json'), Path('translations/golden_route_plaques_v1.json'),
             Path('dk4tool/patch/golden_route_plaques.py'), Path('scripts/prepare_golden_plaques_v613.py'),
             Path('scripts/run_golden_plaques_v613.py'), Path('scripts/native_golden_route_fixture_v613.py'),
             Path('scripts/verify_golden_plaques_v613.py'), Path(__file__)]
    for path in files:
        checked_copy(path, ARCHIVE / path.name)
    screenshots = []
    for context, receipts in proof['reports'].items():
        for variant, receipt in receipts.items():
            path = Path(receipt['path'])
            assert sha(path.read_bytes()) == receipt['sha256']
            run = read(path)
            checked_copy(path, ARCHIVE / f'{context}_{variant}_capture_report.json')
            shots = {r['frame']: r for r in run['frames_captured']}
            for frame in RECORDS if context == 'records' else (33400,):
                row = shots[frame]
                assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
                target = ARCHIVE / f'{context}_{variant}_{frame:06d}_NATIVE_FIXTURE.png'
                checked_copy(row['path'], target)
                screenshots.append({'path': str(target), 'sha256': row['PNG_sha256'], 'frame': frame,
                                    'context': context, 'variant': variant, 'ROM_sha256': run['ROM_sha256'],
                                    'unmodified_native_capture': True, 'isolated_synthetic_test_data': True,
                                    'ordinary_earned_profit_or_progress': False})
    assert len(screenshots) == 39
    save(ARCHIVE / 'provenance.json', {'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'],
         'screenshots': screenshots, 'original_art_variant_is_research_control_not_clean_Japanese_game': True,
         'source_save_unchanged': True, 'fixture_scope': proof['fixtures'], 'publication_approved': False,
         'hardware_device_verification': False, 'full_goal_complete': False,
         'files': {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir() if p.is_file() and p.name != 'provenance.json'}})
    entry = {'documentation': str(DOC), 'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'],
             'patch_sha256': proof['patch_sha256'], 'profile': proof['profile'],
             'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
             'status': 'native_Golden_art_verified_with_explicit_test_fixtures_inherited_regional_gap_open',
             'all8_complete_source_reviewed_headings': True, 'independent_font_ink_points': 715,
             'original_frame_samples': 2928, 'changed_indices': 5027, 'whole_source_current_frame_pairs': 63,
             'actual_native_original_resource_getter_bindings': 39, 'all3_Golden_atlases_in_actual_original_views': True,
             'original_sale_tutorial_Guild_state1_2_3_observed_under_cost_fixture': True,
             'record_fixture_promoted_report_state_explicit': True, 'ordinary_earned_Golden_progress_not_claimed': True,
             'only_three_atlases_changed_all_code_and_other_art_dialogue_exact_V612': True,
             'all470_batches114_layers_retained_exact_clean_patch_and19_ordinary_frames_verified': True,
             'all921_formats_palettes_and57_embedded_extents_retained': True,
             'all18_original_plaques_incomplete_all22_historical_objects_retained': True,
             'inherited_regional_native_context_still_open': True, 'V610_latest_verified_pointers_retained': True,
             'archive': str(ARCHIVE), 'unmodified_fixture_screenshots': 39,
             'full_goal_complete': False, 'canonical_promoted': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        pointers = {k: v for k, v in data.items() if k in ('candidate', 'candidate_sha256', 'latest_candidate',
                    'latest_candidate_sha256', 'current_verified_release_candidate', 'current_verified_release_candidate_sha256',
                    'latest_graphics_preservation')}
        data[KEY] = entry
        data['latest_compiled_experimental_candidate_with_inherited_native_gap'] = {
            'candidate': str(ROM), 'sha256': proof['candidate_sha256'], 'profile': proof['profile'],
            'Save_Load_native_verified': True, 'Golden_Route_native_verified_under_explicit_test_fixtures': True,
            'regional_fleet_native_context_still_open': True}
        save(path, data)
        now = read(path)
        assert all(now[k] == v for k, v in pointers.items())
        assert now.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert now.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    text = '''

## V613: Golden Route Discovery and both Records source-frame repair

Three Golden Route atlases now retain source frames and fine original grain in
place of broad fills, missing rims and a residual Japanese stroke. Eight complete
headings read Goods / Profit % / Reward / Total Rewards. The total qualifier is
retained; original data/calculations remain unchanged. All715 independent font
points,16 end-letter erasure controls and2928 source frame samples pass;5027
indices change. Discovery's percentage face expands40 to44 pixels, ending before
its live value. Hidden grain remains explicit reconstruction, not recovered art.

Actual original Records controls exercise both modes and all five rows. A separate
ordinary New Game buys Salt, then an authorized isolated cost-word fixture triggers
the original sale, tutorial and Guild reporting path. Original record states1,2,3
and the real Golden Route Found screen are observed. No earned trading/profit/
travel/payment/user-save progress is claimed. Source comparison uses a separately
labeled V612-code/original-three-atlases control, not a clean Japanese playthrough.
All39 actual view/getter bindings,63 whole current/source screen pairs and19
ordinary no-fixture New Game/Market regression frames pass. All470 batches114
layers,921 graphics formats/palettes and57 embedded extents remain; the exact
clean-ROM patch reconstructs V613. Thirty-nine unmodified fixture captures,
source comparisons, schedules and provenance are on E.

V613 is experimental with V611's regional native context still open; V610 remains
the latest verified pointer. All18 original plaques remain incomplete, all22
historical scopes exact, and wider graphics/movie/legacy/gameplay gates remain.
Full goal active; canonical unchanged. See
[V613 Golden Route checkpoint](golden_route_plaques_v613_checkpoint.md).
'''
    heading = '## V613: Golden Route Discovery and both Records source-frame repair'
    for name in ('todo', 'translation_progress', 'known_issues', 'plaque_background_texture_defect', 'release_build'):
        path = Path('docs') / (name + '.md')
        content = path.read_text(encoding='utf-8')
        if heading not in content:
            path.write_text(content.rstrip() + '\n' + text, encoding='utf-8')
    print('Archived39 explicit fixture screenshots on E; audits updated;18/22 scopes and V610 verified pointers retained.')


if __name__ == '__main__':
    main()
