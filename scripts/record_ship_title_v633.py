"""Archive verified title captures and add evidence without narrowing the audit."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_ship_title_v633 import ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/ship_title_v633_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Audit comparisons/V633 Ship headings')
GUIDE = Path('E:/Rota Nova translations/Screenshots/Guide candidates/V633 Ship headings')
KEY = 'complete_actual_Ship_Info_and_shared_Refit_headings_v633'


def main():
    proof_path = ROOT / 'release_proof.json'
    proof = read(proof_path)
    assert proof['candidate_sha256'] == sha(ROM.read_bytes())
    assert not proof['Refit_actual_context_still_pending'] and len(proof['actual_Refit_titles']) == 2
    assert proof['script_sha256'] == sha(Path('scripts/verify_ship_title_v633.py').read_bytes())
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    GUIDE.mkdir(parents=True, exist_ok=True)
    files = [DOC, proof_path, ROM.with_suffix('.manifest.json'),
             Path('translations/ship_info_title_crop_v1.json'),
             Path('dk4tool/patch/ship_info_title_crop.py'),
             Path('scripts/prepare_ship_title_v633.py'), Path('scripts/verify_ship_title_v633.py'), Path(__file__)]
    files.extend(ROOT / name for name in (
        'native_preview_proof.json', 'source_safety_proof.json', 'preservation_proof.json',
        'patch_proof.json', 'market_inputs.json', 'refit_inputs.json', 'refit_anchors.json',
        'continuation_state.json', 'build.log', 'Ship_Info_actual_V627_then_V633_4x.png'))
    files.extend(ROOT.glob('*NATIVE_TITLE_PREVIEW.png'))
    for path in files:
        checked_copy(path, ARCHIVE / path.name)
    shots, guides = [], []
    for receipt in proof['reports']:
        report_path = Path(receipt['path'])
        assert sha(report_path.read_bytes()) == receipt['sha256']
        report = read(report_path)
        label = report_path.parent.name
        checked_copy(report_path, ARCHIVE / (label + '_capture_report.json'))
        journal = report_path.parent / 'navigation_command_journal.json'
        if journal.exists():
            checked_copy(journal, ARCHIVE / (label + '_navigation_journal.json'))
        frames = {s['frame']: s for s in report['frames_captured']}
        for frame, shot in frames.items():
            if 'market' not in label and frame not in (3200, 5200, 5600, 6400, 6800, 7200):
                continue
            target = ARCHIVE / f'{label}_{frame:06d}_UNMODIFIED_NATIVE.png'
            checked_copy(shot['path'], target)
            record = {'path': str(target), 'frame': frame, 'sha256': shot['PNG_sha256'],
                      'ROM_sha256': report['ROM_sha256'], 'cold_boot_no_savestate': True,
                      'no_synthetic_gameplay_fixtures': True, 'unmodified_capture': True}
            shots.append(record)
            if label == 'ship_title_v633_selection_actual' and frame == 5600 or label == 'ship_title_v633_refit_actual' and frame in (6800, 7200):
                guide = GUIDE / target.name
                checked_copy(shot['path'], guide)
                guides.append({**record, 'path': str(guide), 'source_report': str(report_path),
                               'copied_save_not_new_acquisition_or_completed_refit': True})
    save(GUIDE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
                                   'screenshots': guides, 'publication_approved': False})
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
                                     'screenshots': shots, 'guide_candidates': guides,
                                     'enlarged_comparison_separate_from_unmodified_captures': True,
                                     'full_RAM_exports_retained_in_Generated_runs': True,
                                     'publication_approved': False, 'full_goal_complete': False,
                                     'files': {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir()
                                               if p.is_file() and p.name != 'provenance.json'}})
    entry = {'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
             'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'], 'profile': proof['profile'],
             'patch_sha256': proof['patch_sha256'], 'status': 'experimental_actual_both_heading_modes_verified',
             'complete_Ship_Info98_ink_restores24_clipped_final_fo_pixels': True,
             'two_actual_Refit65_ink_masks_centered': True,
             'every_other_actual_screen_pixel_and19_ordinary_regression_frames_exact_V627': True,
             'all31_owners_references_all_other30_texts_and_section_shapes_verified': True,
             'five_invalid_source_owner_reference_controls_rejected': True,
             'all470_batches114_layers921_graphics57_embedded_extents_exact_patch_retained': True,
             'ordinary_copied_save_inputs_no_gameplay_fixture_or_savestate': True,
             'all18_original_plaques_incomplete_all22_historical_objects_exact': True,
             'five_miniature_Confirm_and_broader_graphics_contexts_still_open': True,
             'archive': str(ARCHIVE), 'guide_archive': str(GUIDE),
             'full_goal_complete': False, 'canonical_promoted': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        before = data.copy()
        data[KEY] = entry
        latest_key = 'latest_compiled_experimental_candidate_with_inherited_native_gap'
        latest = data.get(latest_key, {}).copy()
        latest.update({'candidate': str(ROM), 'sha256': proof['candidate_sha256'], 'profile': proof['profile'],
                       'complete_actual_Ship_Info_and_Refit_title_crops_verified': True,
                       'broader_graphics_gates_remain_open': True})
        data[latest_key] = latest
        data['current_goal_turn_classification'] = 'progress'
        save(path, data)
        current = read(path)
        assert all(current[k] == v for k, v in before.items()
                   if k not in (KEY, latest_key, 'current_goal_turn_classification'))
        assert current.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    heading = '## V633: complete Ship Info and shared Refit headings'
    text = '''

Ordinary ship selection exposed Ship Info clipped to Ship In: the complete native
bitmap held98 ink pixels but its48-pixel display crop retained74. Widening and
centering the original view to66 preserves all letters. Refit uses the same view;
four existing terminal padding bytes fund UI centering spaces without pool,
section, startup or staged-payload growth. All31 references and other30 texts
are exact;every other ROM file/component is unchanged from V627. Actual ordinary
copied-save Ship Info and two Refit views pass complete masks and all other screen
pixels;all19 no-save New Game/Market screens are exact. Full470/114 stack,921/57
preservation and exact clean patch reconstruction pass. Experimental V633 SHA256:
eea7c88cd8c6082cf56a8779421018913f2ef9b40ca3cc77fe1d1b13b74ec05f.
Unmodified captures,proof and guide candidates saved on E. All18 plaque objects
and22 historical scopes remain exact/open;canonical and V610 verified pointers
remain unchanged. Miniature/Confirm,legacy,village,material and other movie/context
gates remain open. Full goal active. See [V633 checkpoint](ship_title_v633_checkpoint.md).
'''
    for name in ('todo', 'translation_progress', 'known_issues', 'release_build'):
        path = Path('docs') / (name + '.md')
        content = path.read_text(encoding='utf-8')
        if heading not in content:
            path.write_text(content.rstrip() + '\n\n' + heading + '\n' + text, encoding='utf-8')
    print(f'V633 archived {len(shots)} unmodified screenshots and {len(guides)} guide candidates;18/22 scopes exact,full goal open.')


if __name__ == '__main__':
    main()
