"""Archive actual regional UI evidence without finalizing historical audit scopes."""

import shutil
from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_regional_ui_v616 import ROM, ROOT, read, save

DOC = Path('docs/regional_ui_v616_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V616 Regional UI')
KEY = 'actual_original_regional_fleet_UI_and_guarded_policy_family_v616'


def checked_copy(source, destination):
    source, destination = Path(source), Path(destination)
    shutil.copyfile(source, destination)
    assert sha(source.read_bytes()) == sha(destination.read_bytes())


def main():
    proof_path = ROOT / 'release_proof.json'
    proof = read(proof_path)
    assert proof['candidate_sha256'] == sha(ROM.read_bytes())
    assert proof['script_sha256'] == sha(Path('scripts/verify_regional_ui_v616.py').read_bytes())
    assert len(proof['whole_source_composites']) == 11 and len(proof['actual_all5_regional_plaque_frames']) == 4
    assert len(proof['both_complete_Ship_Name_font_masks']) == 2
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    files = [DOC, proof_path, ROOT / 'native_dispatch_proof.json', ROOT / 'preservation_proof.json',
             ROOT / 'patch_proof.json', ROOT / 'source_art_control.json', ROOT / 'policy_replay_inputs.json',
             ROOT / 'names_final_inputs.json', ROOT / 'market_inputs.json', ROOT / 'build.log',
             ROOT / 'actual_source_English_regional_comparison.png', ROM.with_suffix('.manifest.json'),
             Path('translations/shipyard_ui_labels_v1.json'), Path('translations/regional_policy_prompts_v1.json'),
             Path('translations/regional_policy_prompts_manuscript_v1.json'), Path('translations/regional_policy_wrap_v1.json'),
             Path('work/analysis/regional_fleet_v615/original_formation_native_proof.json'),
             Path('work/analysis/regional_fleet_v615/formed_fixture_manifest.json'),
             Path('work/analysis/regional_fleet_v615/observed_native_word_split_blocker.json'),
             Path('work/analysis/regional_fleet_v615/actual_exact_font_prompt_readback.json'),
             Path('dk4tool/patch/ship_name_heading.py'), Path('dk4tool/patch/shipyard_ui_labels.py'),
             Path('dk4tool/patch/regional_policy_prompts.py'), Path('dk4tool/patch/regional_policy_wrap.py'),
             Path('scripts/probe_regional_policy_wrap_v616.py'), Path('scripts/prepare_shipyard_ui_v615.py'),
             Path('scripts/prepare_regional_policy_wrap_v616.py'), Path('scripts/run_regional_ui_v616.py'),
             Path('scripts/verify_regional_ui_v616.py'), Path(__file__)]
    for path in files:
        checked_copy(path, ARCHIVE / path.name)
    screenshots = []
    for receipt in proof['reports']:
        path = Path(receipt['path'])
        assert sha(path.read_bytes()) == receipt['sha256']
        run = read(path)
        context = path.parent.name.removeprefix('regional_ui_v616_')
        checked_copy(path, ARCHIVE / (context + '_capture_report.json'))
        selected = {r['frame']: r for r in run['frames_captured']}
        wanted = {r['frame'] for r in proof['whole_source_composites']} if context in ('policy', 'source') else {6200, 10200}
        if context == 'market':
            wanted = set(selected)
        for frame in sorted(wanted):
            row = selected[frame]
            assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
            target = ARCHIVE / f'{context}_{frame:06d}_UNMODIFIED_NATIVE.png'
            checked_copy(row['path'], target)
            screenshots.append({'path': str(target), 'sha256': row['PNG_sha256'], 'frame': frame,
                                'context': context, 'ROM_sha256': run['ROM_sha256'],
                                'fixture_save_used': context != 'market', 'unmodified_capture': True})
    # Preserve the two actual failed native-wrap controls alongside the repair.
    before = Path('E:/Rota Nova translations/Generated/work/emulation_v193/shipyard_ui_v615_actual')
    for frame in (13800, 15800):
        source = before / f'frame_{frame:06d}_navigation.png'
        target = ARCHIVE / f'V615_FAILED_WORD_SPLIT_{frame:06d}.png'
        checked_copy(source, target)
        screenshots.append({'path': str(target), 'sha256': sha(target.read_bytes()), 'frame': frame,
                            'context': 'V615 failed word-wrap control', 'unmodified_capture': True, 'passed': False})
    save(ARCHIVE / 'provenance.json', {'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'],
         'screenshots': screenshots, 'publication_approved': False, 'full_goal_complete': False,
         'all_regional_names_runs_use_explicit_formed_test_save_with_synthetic_prerequisites': True,
         'market_run_no_save_no_fixtures': True,
         'files': {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir() if p.is_file() and p.name != 'provenance.json'}})
    entry = {'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
             'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'], 'patch_sha256': proof['patch_sha256'],
             'profile': proof['profile'], 'status': 'experimental_verified_actual_subset_remaining_variants_open',
             'original_regional_fleet_formed_and_saved_to_isolated_slot6_then_cold_reloaded': True,
             'all5_regional_plaques_actual_source_frame_comparison_verified': True,
             'complete_regional_pixels': proof['complete_native_regional_pixels'],
             'whole_Japanese_art_source_pairs': len(proof['whole_source_composites']),
             'all4_policy_labels_and_both_Ship_Name_callers_complete_native_font_masks': True,
             'actual_Patrol_Dock_word_splits_corrected_by_existing_shared_guarded_wrapper': True,
             'all3668_native_IDs_exercised_only127_to134_added': True,
             'original321_327_and40_other_parent_controls_preserved': True,
             'all470_batches114_layers921_graphics57_embedded_extents_and_exact_patch_retained': True,
             'ordinary19_New_Game_Market_screens_exact_V613': True,
             'remaining_family_variants': proof['remaining_in_this_family'],
             'all18_original_plaques_incomplete_all22_historical_objects_exact': True,
             'archive': str(ARCHIVE), 'unmodified_archived_screenshots': len(screenshots),
             'V610_verified_pointers_retained_pending_remaining_family_gates': True,
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
            'regional_fleet_native_context_still_open': False,
            'actual_all5_regional_plaque_context_verified': True,
            'regional_policy_confirmation_war_contract_and_financial_variants_still_open': True}
        data['current_goal_turn_classification'] = 'progress'
        save(path, data)
        now = read(path)
        assert all(now[k] == v for k, v in pointers.items())
        assert now.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert now.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    text = '''

## V616: actual regional plaques, Ship Name callers and guarded policy prompts

Original Shipyard/Dock controls form Manuel's regional fleet using three bounded
prerequisite fixtures, preserving Gerhard's refusal. Normal slot6 Save and cold
reload retain it; the source donor is unchanged. World Map Fleet/Village selection
finally exposes all5 regional plaques. Original formation verifies24912 full-region
pixels; V616's independent Japanese-art control verifies11 complete screen pairs,
including4 active regional states and16608 full-region pixels. This closes the
previous missing display context, not the remaining policy/financial variants.

The coordinated V615 source repair adds both Ship Name captions,4 policy choices,
mission/confirmation text and8 complete native prompts. Native127/128 had split
one English sentence;133 was an unrelated save fallback. Actual Patrol/Dock then
expose mid-word physical wrapping despite previews. V616 reuses the existing
guarded word wrapper for all8 IDs. All3668 IDs and40 other-parent controls pass;
only127..134 gain wrapping,original321/327 remain. No section/pool/cache grows.
Actual corrected notices retain complete have/under and equal x22 line origins.
Both original purchase/rename Ship Name callers and all4 menu labels pass complete
font/blank-cell masks. The ordinary24100-frame no-fixture New Game/Market run
matches all19 whole V613 screens. Full470/114 integration,921/57 preservation and
exact clean patch pass; screenshots,source controls and failed V615 cases are on E.

V616 remains experimental. Attack Town and132..134 gameplay branches,all4 order
confirmations,other mission descriptions and nonzero monthly values remain. All18
original plaque objects and22 historical scopes are exact and incomplete; V610
verified pointers/canonical stay unchanged. Broader graphics gates and the later
older-record review remain open. See [V616 checkpoint](regional_ui_v616_checkpoint.md).
'''
    heading = '## V616: actual regional plaques, Ship Name callers and guarded policy prompts'
    for name in ('todo', 'translation_progress', 'known_issues', 'plaque_background_texture_defect', 'release_build'):
        path = Path('docs') / (name + '.md')
        content = path.read_text(encoding='utf-8')
        if heading not in content:
            path.write_text(content.rstrip() + '\n' + text, encoding='utf-8')
    print(f'Archived{len(screenshots)} unmodified captures and source proofs on E; all3 audits/progress updated;18/22 scopes and V610 verified pointers exact. Goal active.')


if __name__ == '__main__':
    main()
