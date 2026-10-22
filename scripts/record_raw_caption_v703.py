"""Record the accepted raw16 alpha contract without inventing a production fix."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_raw_caption_v703 import ROOT
from scripts.record_memory_streams_v682 import copy
from scripts.run_room_gender_v694 import CAP
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V703 Raw caption display contract')
DOC = Path('docs/raw_caption_v703_checkpoint.md')
KEY = 'accepted_raw16_caption_exact_software_VRAM_words_bit15_display_contract_no_production_fix_v703'
SOURCES = ('scripts/prepare_raw_caption_v703.py', 'scripts/run_raw_caption_v703.py',
    'scripts/verify_raw_caption_v703.py', 'scripts/record_raw_caption_v703.py',
    'scripts/verify_raw_caption_archive_v703.py', 'scripts/prepare_standalone_tiles_v702.py',
    'scripts/lower_native_reference_v702.py', 'scripts/run_gender_exception_v697.py',
    'scripts/inspect_desmume_state_v249.py', 'scripts/observe_file_requests_v681.py',
    'scripts/check_file_requests_v681.py')


def main():
    pp = ROOT / 'proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_raw_caption_v703.py').read_bytes())
    assert proof['both_raw16_source_and_control_accepted_loaded_whole_not_rejected_as_indexed8']
    assert len(proof['eight_complete_actual_tiles_software_words_and_upper_pixel_models']) == 8
    assert proof['NO_production_alpha_correction_or_all_comics_clearance_inferred']
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    save(ROOT / 'visual_review.json', {'both_full_source_control_baseline_and_caption_RGB_composite_sheets_opened': True,
        'sheets': proof['review_sheets'], 'source_black_rectangle_control_complete_Huh_caption_visible': True,
        'first_final_letters_bubble_edge_and_adjacent_crop_pixels_retained_in_control': True,
        'controlled_alpha_import_not_production_defect_or_original_comic_scene': True,
        'no_guide_promotion_or_original_viewer_opacity_policy_inference': True})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'matched_generic_raw16_source_control_files_actually_loaded_and_copied': True,
        'all8_tiles_software_words393216_upper_pixels_and2304_control_RGB_reconstruction_exact': True,
        'identical_IO_palette_OAM_and_only1344_first_tile_bit15_LCDM_bytes_differ': True,
        'captured_direct_BG3_bankC_black_backdrop_and_core_bit15_gate_bind_display_difference': True,
        'all30_pre_fixture6_restored_full_RGB_pairs_and4_lower_source_control_pairs_exact': True,
        'original_source_caption_archive_brown_marks_and_all_production_art_unchanged': True,
        'not_indexed8_format_rejection_and_not_missing_English_glyph_data': True,
        'original_comic_viewer_descriptor_import_opacity_and_normal_scenes_remain_open': True,
        'NO_global_production_alpha_change_or_all_comics_completion_inferred': True,
        'all18_plaques_incomplete22_historical_scopes_and_full_goal_preserved': True,
        'production_ROM_patch_manifest_registry_donor_canonical_and_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert data == pre['all_original_audits_before'][name]
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(path, data)
        copy(path, ARCHIVE / 'audits' / name)
    heading = '## V703: accepted raw16 caption and matched opacity control'
    addition = (
        'Three terminal6800-frame cold boots exercise the compatible generic '
        'raw16 widget,not V587s rejecting indexed8 canvas. A source-preserved '
        '72x32 frame6 crop and same-RGB OR8000 research control both load via '
        'real uncached SDK/cache calls. All8 tile software words and full393216 '
        'upper pixels match. Actual bankC VRAM preserves words;complete671744 '
        'LCDM bytes differ only at1344 first-tile bit15 bytes,with I/O/palette/'
        'OAM identical. Captured identity BG3/direct mode,black backdrop and '
        'retained core rot_BMP_map alpha gate explain source black versus '
        'visible complete Huh control. All2304 control RGB pixels reconstruct '
        'source exactly. All30 pre-fixture6 restored full RGB pairs and4 lower '
        'source/control pairs pass. WRAX-extra-RAM verifier mistake retained '
        'and corrected using exporter WRAM guards. Both sheets opened. No '
        'source RGB/mark/archive/production art edits;no global alpha fix or '
        'ordinary comic-parent policy inferred. Original viewer/import/geometry/'
        'scenes/restoration remain open; next lead must bind any opacity import. '
        'All18 plaques incomplete,22 scopes exact,full goal active. V692/patch/'
        'registry/pointers/donor unchanged;research ROMs/evidence on E,no guide '
        'promotion/commit/push. See [V703 checkpoint](raw_caption_v703_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        content = path.read_text(encoding='utf-8')
        assert heading not in content
        path.write_text(content.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
        copy(path, ARCHIVE / 'docs' / name)
    for path in (*map(Path, SOURCES), DOC, Path(proof['native_GPU_CPP_rot_BMP_map_bit15_gate']['path'])):
        copy(path, ARCHIVE / 'sources' / path)
    external = {}
    for path in ROOT.rglob('*'):
        if path.is_file():
            if path.suffix.lower() == '.nds':
                external[str(path)] = sha(path.read_bytes())
            else:
                copy(path, ARCHIVE / 'analysis' / path.relative_to(ROOT))
    for folder in CAP.glob('raw_caption_v703_*'):
        for path in folder.rglob('*'):
            if path.is_file():
                external[str(path)] = sha(path.read_bytes())
    reference = proof['whole_native_lower_reference']
    for path in (reference['historical_ROM'], reference['phase_proof']):
        external[str(path)] = sha(Path(path).read_bytes())
    for row in reference['states']:
        external[row['binary']] = row['sha256']
    save(ARCHIVE / 'provenance.json', {'scripts': {p: sha(Path(p).read_bytes()) for p in SOURCES},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'external_E_drive_evidence': external,
        'accepted_raw16_diagnostic_not_an_original_comic_scene_or_production_fix': True,
        'research_ROMs_hash_referenced_not_release_promoted': True, 'full_goal_complete': False})
    print('V703 accepted raw16 display/alpha constraint recorded; original comic importer and full graphics goal remain open.', flush=True)


if __name__ == '__main__':
    main()
