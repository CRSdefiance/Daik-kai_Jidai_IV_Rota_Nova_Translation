"""Record actual control loading/rendering fixtures without normal-parent clearance."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.run_small_controls_v701 import CAP, ROOT
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V701 Small control widget displays')
DOC = Path('docs/small_controls_v701_checkpoint.md')
KEY = 'six_exact_control_graphics_actual_widget12_full_planes_and_Confirm_original_load_v701'
SOURCES = ('scripts/run_small_controls_v701.py', 'scripts/verify_small_controls_v701.py',
    'scripts/record_small_controls_v701.py', 'scripts/verify_small_controls_archive_v701.py',
    'scripts/run_gender_exception_v697.py', 'scripts/observe_file_requests_v681.py',
    'scripts/check_file_requests_v681.py', 'scripts/verify_frame_style_tiles_v584.py')


def main():
    pp = ROOT / 'proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_small_controls_v701.py').read_bytes())
    assert len(proof['six_exact_assets_original_loader_and_widget_complete_rectangles_verified']) == 12
    assert proof['complete_control_native5_pixels'] == 4608
    assert len(proof['all12_whole_source_predicted_two_screen_images']) == 12
    assert proof['Confirm_original_uncached_owner_real_SDK_open_and_full532_byte_file_verified']
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    save(ROOT / 'visual_review.json', {'six_complete_actual_widget_and_normal_restored_Info_roster_sheets_opened': True,
        'sheets': proof['review_sheets'], 'all_six_complete_first_final_letters_native_compact_sizes_readable': True,
        'Confirm_border_and_padding_visible': True,
        'fixture_substitutes_gender_view_not_production_layout': True,
        'original_profile_gender_zodiac_and_roster_restore_visible_and_pixel_exact': True,
        'no_normal_control_location_palette_or_interaction_clearance_no_guide_promotion': True})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'all_six_exact_control_files_rectangles_original_live_widget_display_verified_under_fixture': True,
        'Confirm_actual_original_uncached_SDK_Open_and532_byte_source_copy_verified': True,
        'all12_complete_native5_source_models1179648_pixels4608_control_pixels_exact': True,
        'all90_pre_fixture_full_RGB_RAM_pairs_and18_restored_full_RGB_pairs_exact': True,
        'all14_complete_original_cache_getter_bindings_and12_negative_pixel_controls_pass': True,
        'only_six_view_words_and_temporary_CPU_R3_argument_changed_restore_before_normal_exit': True,
        'normal_locations_intended_palettes_states_and_embedded_copy_use_remain_open': True,
        'all18_plaques_incomplete22_historical_scopes_and_full_goal_preserved': True,
        'V698_prefix_and_V694_suffix_gaps_not_cleared': True,
        'ROM_patch_manifest_registry_donor_canonical_release_pointers_unchanged': True,
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
    heading = '## V701: six exact control graphics in the original live widget'
    addition = (
        'Seven terminal7000-frame cold boots exercise Confirm/Pick Cargo/Pick Ship/'
        'Done/Rank/Cancel through the original live image widget plus a normal '
        'baseline. Exact source files and registered coordinate pair are inputs; '
        'only six view-source words and temporary CPU R3 change. Confirm starts '
        'uncached,requests its actual original SDK filename and copies its whole '
        '532-byte file. Fourteen full native cache getters,no I/O bridges,bind '
        'held source files. All12 source-predicted full screens1179648 native5 '
        'pixels include4608 complete control pixels; actual whole RGB differences '
        'are exactly source-predicted. Palette alpha uses stored words:Confirm14 '
        'transparent,0 opaque;12 wrong palette/alpha/placement controls fail. All90 '
        'pre-fixture RGB/RAM pairs,six pre-write full RAM states and18 restored '
        'full screens match. Live inputs restore6401/6500 before normal B6501; '
        'later freed heap is not persistent view state. Both sheets opened,all '
        'letters fit. Normal control parents,intended palettes/states and embedded '
        'use remain open; no ordinary-context/guide credit. All18 plaques '
        'incomplete,22 scopes exact,V698/V694 model gaps and broader graphics/'
        'restoration/older checks/acceptance open. V692/patch/registry/pointers/'
        'donor unchanged; evidence on E,no commit/push. Full goal active. See '
        '[V701 checkpoint](small_controls_v701_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        content = path.read_text(encoding='utf-8')
        assert heading not in content
        path.write_text(content.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
        copy(path, ARCHIVE / 'docs' / name)
    for path in (*map(Path, SOURCES), DOC):
        copy(path, ARCHIVE / 'sources' / path)
    for path in ROOT.rglob('*'):
        if path.is_file():
            copy(path, ARCHIVE / 'analysis' / path.relative_to(ROOT))
    external = {}
    for folder in CAP.glob('small_controls_v701_*'):
        for path in folder.rglob('*'):
            if path.is_file():
                external[str(path)] = sha(path.read_bytes())
    save(ARCHIVE / 'provenance.json', {'scripts': {p: sha(Path(p).read_bytes()) for p in SOURCES},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'external_E_drive_evidence': external,
        'seven_runs_terminal_diagnostic_widgets_not_normal_control_screens_or_guide': True,
        'full_goal_complete': False})
    print('V701 six actual exact-source widget displays and native Confirm load recorded; normal control contexts remain open.', flush=True)


if __name__ == '__main__':
    main()
