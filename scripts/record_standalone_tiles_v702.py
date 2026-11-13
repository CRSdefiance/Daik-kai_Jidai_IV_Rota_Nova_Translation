"""Record tiled native source coverage with explicit research-ROM and phase limits."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_standalone_tiles_v702 import ROOT
from scripts.record_memory_streams_v682 import copy
from scripts.run_room_gender_v694 import CAP
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V702 Standalone source tiles')
DOC = Path('docs/standalone_tiles_v702_checkpoint.md')
KEY = 'standalone_copyright_ship69_actual_tiles80848_source_pixels_and_whole_native_lower_states_v702'
SOURCES = ('scripts/prepare_standalone_tiles_v702.py', 'scripts/run_standalone_tiles_v702.py',
    'scripts/verify_standalone_tiles_v702.py', 'scripts/lower_native_reference_v702.py',
    'scripts/record_standalone_tiles_v702.py', 'scripts/verify_standalone_tiles_archive_v702.py',
    'scripts/run_gender_exception_v697.py', 'scripts/run_small_controls_v701.py',
    'scripts/observe_file_requests_v681.py', 'scripts/check_file_requests_v681.py')


def main():
    pp = ROOT / 'proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_standalone_tiles_v702.py').read_bytes())
    assert len(proof['complete_actual_source_tile_results']) == 69
    assert proof['all80848_source_pixels_covered_exactly_once']
    assert len(proof['all138_complete_lower_planes_match_original_native_cursor_states']) == 138
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    save(ROOT / 'visual_review.json', {'all3_source_actual_tile_composite_and_whole_fixture_screen_sheets_opened': True,
        'sheets': proof['review_sheets'], 'copyright_all_letters_punctuation_and_original_date_visible': True,
        'ship_material_sheet_source_mast_sail_panel_rail_and_transparent_regions_preserved': True,
        'composites_labelled_not_one_game_frame_no_normal_scene_or_guide_credit': True,
        'no_source_palette_alpha_header_extent_or_art_edits': True})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'two_entire_source_files_copyright_ship_unchanged_to_clean': True,
        'all69_actual_native_tiles_cover_every80848_source_pixel_exactly_once': True,
        'all69_upper_source_models3391488_pixels_and_exact_RGB_difference_positions_pass': True,
        'all138_whole_lower_planes_match_complete_original_native_cursor_states_not_ring_masks': True,
        'actual_same_frame_clock_phase_equality_not_claimed_initial236_pixel_failure_retained': True,
        'all30_pre_fixture_and6_restored_full_RGB_pairs_exact': True,
        'two_uncached_real_SDK_opens_and69_complete_original_native_cache_bindings_pass': True,
        'only_research_borrowed_slot_changes_all_other_files_ARM9_ARM7_ids_overlays_banner_exact': True,
        'original_standalone_consumers_normal_scene_and_intended_whole_composition_remain_open': True,
        'all18_plaques_incomplete22_historical_scopes_and_full_goal_preserved': True,
        'production_ROM_art_patch_manifest_registry_donor_canonical_release_pointers_unchanged': True,
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
    heading = '## V702: complete copyright and ship texture coverage through native tiles'
    addition = (
        'Four terminal7000/12700-frame cold boots use two research cache-slot '
        'ROMs and two normal production baselines. Only the borrowed kakutei '
        'payload changes in research; entire source copyright/ship PXLs remain '
        'clean-exact,all other files/ARM9/ARM7/IDs/overlays/banner exact. Original '
        'uncached SDK loading and69 complete cache getters bind six copyright '
        'and63 ship tiles. Every80848 source pixel is covered once;69 whole '
        'upper source models3391488 native5 pixels and exact RGB difference '
        'positions pass. All138 complete lower planes match one of two '
        'version-bound original native cursor states; initial236 lower-pixel '
        'phase mismatch retained,not masked or called same-frame tick proof. '
        'All30 pre-fixture and6 restored whole RGB pairs match. Only declared '
        'view words/temporary R3 change,inputs restore before normal exit. '
        'Three sheets opened; composites labelled not one game frame. Copyright '
        'Latin/date and ship material retained,no new translation or production '
        'art edit. Original filename consumers/normal whole scenes remain open; '
        'historical656/660 loader census unchanged. Initial import errors before '
        'emulation retained; final producer frozen. All18 plaques incomplete,22 '
        'scopes exact,broader graphics/restoration/older checks/acceptance open. '
        'V692/patch/registry/pointers/donor unchanged; research ROMs/evidence on '
        'E,no guide promotion/commit/push. Full goal active. See '
        '[V702 checkpoint](standalone_tiles_v702_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        content = path.read_text(encoding='utf-8')
        assert heading not in content
        path.write_text(content.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
        copy(path, ARCHIVE / 'docs' / name)
    for path in (*map(Path, SOURCES), DOC):
        copy(path, ARCHIVE / 'sources' / path)
    external = {}
    for path in ROOT.rglob('*'):
        if path.is_file():
            if path.suffix.lower() == '.nds':
                external[str(path)] = sha(path.read_bytes())
            else:
                copy(path, ARCHIVE / 'analysis' / path.relative_to(ROOT))
    for folder in CAP.glob('standalone_tiles_v702_*'):
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
        'research_ROMs_hash_referenced_on_E_not_duplicated_or_release_promoted': True,
        'tile_composites_not_normal_whole_scenes_or_guide_images': True, 'full_goal_complete': False})
    print('V702 complete native source-tile coverage recorded; original consumers,normal scenes and full graphics goal remain open.', flush=True)


if __name__ == '__main__':
    main()
