"""Record tested Refit repair, retained failures and unchanged full graphics scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.run_refit_display_v712 import ROM
from scripts.run_room_gender_v694 import CAP
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/refit_help_v713')
RELEASE = Path('work/analysis/refit_help_v712')
DOC = Path('docs/refit_help_v713_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V713 Refit help layout and lifetime')
KEY = 'refit31_natural_paragraphs_expanded_crop23_actual_displays49_New_Game_native_heap_lifetime_v713'
SOURCES = ('dk4tool/dialogue/refit_help.py', 'dk4tool/patch/refit_help_repack.py',
    'dk4tool/patch/refit_help_layout.py', 'dk4tool/patch/refit_help_layout_v2.py',
    'scripts/build_integrated_release.py', 'scripts/prepare_refit_layout_v712.py',
    'scripts/verify_refit_release_v712.py', 'scripts/run_refit_display_v712.py',
    'scripts/finish_refit_display_v712.py', 'scripts/trace_refit_heap_v713.py',
    'scripts/verify_refit_heap_v713.py', 'scripts/record_refit_help_v713.py',
    'translations/refit_help_manuscript_v2.json', 'translations/refit_help_repack_v2.json',
    'translations/refit_help_layout_v2.json')


def main():
    proof, heap = read(RELEASE / 'display_proof.json'), read(ROOT / 'heap_proof.json')
    release = read(RELEASE / 'release_proof.json')
    assert proof['candidate_sha256'] == heap['candidate_sha256'] == release['candidate_sha256'] == sha(ROM.read_bytes())
    assert len(proof['23_actual_help_compositions']) == 23
    assert len({r['message_id'] for r in proof['23_actual_help_compositions']}) == 13
    assert len(heap['all59_whole_two_screen_RGB_pairs_and_full4MiB_capture_RAM_pairs_exact']) == 59
    assert len(heap['six_actual_complete_lifetime_events']) == 6
    assert proof['verifier_sha256'] == sha(Path('scripts/finish_refit_display_v712.py').read_bytes())
    assert heap['verifier_sha256'] == sha(Path('scripts/verify_refit_heap_v713.py').read_bytes())
    assert release['registry_sha256'] == sha(Path('translations/release_stack.json').read_bytes())
    assert release['manifest_sha256'] == sha(ROM.with_suffix('.manifest.json').read_bytes())
    assert release['patch_sha256'] == sha(ROM.with_suffix('.xdelta').read_bytes())
    assert DOC.exists()
    save(ROOT / 'visual_review.json', {'before_after_complete16_screen_sheet_opened': proof['review_sheet'],
        'actual_Topsail_fourth_wind_line_complete_and_left_aligned': True,
        'original_headings_details_buttons_and_wood_background_preserved': True,
        'final_Copenhagen_Equipment_Rename_popup_visually_reviewed': True,
        'plaque_texture_approval_not_inferred_no_guide_promotion': True})
    release['actual_changed_screen_and_native_heap_lifetime_pending'] = False
    release['actual_display_proof'] = str(RELEASE / 'display_proof.json')
    release['actual_display_proof_sha256'] = sha((RELEASE / 'display_proof.json').read_bytes())
    release['actual_heap_proof'] = str(ROOT / 'heap_proof.json')
    release['actual_heap_proof_sha256'] = sha((ROOT / 'heap_proof.json').read_bytes())
    save(RELEASE / 'release_proof.json', release)
    entry = {'documentation': str(DOC), 'release_proof': str(RELEASE / 'release_proof.json'),
        'release_proof_sha256': sha((RELEASE / 'release_proof.json').read_bytes()),
        'actual_display_proof': str(RELEASE / 'display_proof.json'),
        'actual_display_proof_sha256': release['actual_display_proof_sha256'],
        'actual_heap_proof': str(ROOT / 'heap_proof.json'),
        'actual_heap_proof_sha256': release['actual_heap_proof_sha256'],
        'candidate': str(ROM), 'candidate_sha256': release['candidate_sha256'],
        '31_source_faithful_natural_paragraphs_and_complete_native_expanded_fonts': True,
        'actual23_help_displays_cover13_distinct_messages_all59_whole_RGB_models49_New_Game_pairs': True,
        'actual_one9072_byte_native_allocation_matching_free_cleared_pointer59_whole_RAM_RGB_pairs': True,
        'original_heading_three_detail_rows_and_all675_PXL_FLS_files_preserved': True,
        'full470_batches114_accepted_layers_original_pool_allocator_bounds_and_cache_preserved': True,
        'V706_and_V710_runtime_failures_revoked_retained_not_parents': True,
        'V708_actual_three_strip_clipping_rejected_not_finished_handoff': True,
        '31_ordinary_visits_repeated_entry_stress_and_full_routes_not_claimed': True,
        'all18_plaques_incomplete22_historical_objects_exact': True,
        'small_control_village_legacy_comic_material_model_gaps_and_final_acceptance_remain_open': True,
        'older_record_based_checks_to_revisit_after_full_goal': True,
        'canonical_baseline_and_user_donor_unchanged': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    pre = read(RELEASE / 'preflight.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert KEY not in data
        assert data == pre['all_original_audits_before'][name]
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        pointer = data['latest_compiled_experimental_candidate_with_inherited_native_gap']
        assert pointer['candidate'].endswith('all_routes_combined_v692_candidate.nds')
        pointer.update(candidate=str(ROM), sha256=release['candidate_sha256'], profile='all-routes-unified-v712',
            refit31_paragraphs_source_reviewed_native_font_and_actual13_contexts_verified=True,
            refit_bitmap_original_allocator_lifetime_verified=True)
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(path, data)
        copy(path, ARCHIVE / 'audits' / name)
    heading = '## V712/V713: complete Refit help and actual native bitmap lifetime'
    paragraph = (
        'Source-reviewed31 COMMON paragraphs now use natural English and generated word wraps. '
        'Original three-strip composition clipped longer text and shared later bitmap rows with '
        'heading/details. The new168x108 bitmap gives five explanation rows and preserves the '
        'heading and all three detail rows. All31 native font planes pass; actual23 displays '
        'cover13 messages, all59 whole Yard models and49 New Game RGB pairs pass. A separate '
        'ordinary20600-frame cancel/exit run records one9072-byte original allocation/free and '
        'cleared pointer; all59 common whole RGB/RAM pairs match, five ships and25975 funds '
        'remain. V706 boot-growth and V710 wrong-allocator failures are revoked and retained; '
        'supplied native bridges did not establish actual allocation. V708 clipping was caught '
        'before handoff. V712 preserves all675 graphics,3637 other COMMON strings,470 batches '
        'and114 accepted layers; clean patch reconstructs exactly. Only the experimental pointer '
        'advances; canonical unchanged. Complete before/after sheet and exit screen reviewed. '
        'All18 plaques incomplete,22 historical requirements exact; normal control/card/legacy/'
        'comic contexts,wood/restoration,model gaps and final acceptance remain open. Revisit '
        'older record-based checks after the full goal. Evidence on E,no guide promotion,commit '
        'or push. Full goal active. See [V713 checkpoint](refit_help_v713_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        content = path.read_text(encoding='utf-8')
        assert heading not in content
        path.write_text(content.rstrip() + '\n\n' + heading + '\n\n' + paragraph, encoding='utf-8')
        copy(path, ARCHIVE / 'docs' / name)
    for p in (*map(Path, SOURCES), DOC):
        copy(p, ARCHIVE / 'sources' / p)
    for p in (RELEASE / 'actual_before_after_refit.png', RELEASE / 'prechange_native_background.png'):
        copy(p, ARCHIVE / 'review' / p.name)
    # Screenshots are copied for convenient review; full RAM and reports stay at
    # their existing E-drive paths with a complete external hash inventory.
    for folder in ('refit_help_v712_yard', 'refit_help_v712_newgame', 'refit_help_v713_heap_lifetime'):
        for p in (CAP / folder).glob('*.png'):
            copy(p, ARCHIVE / 'screenshots' / folder / p.name)
    external = {}
    for version in range(706, 714):
        folder = Path(f'work/analysis/refit_help_v{version}')
        if folder.exists():
            for p in folder.rglob('*'):
                if p.is_file():
                    external[str(p.resolve())] = sha(p.read_bytes())
                    if p.suffix in ('.json', '.log', '.md', '.txt'):
                        copy(p, ARCHIVE / 'analysis' / str(version) / p.relative_to(folder))
        for folder in CAP.glob(f'refit_help_v{version}_*'):
            for p in folder.rglob('*'):
                if p.is_file():
                    external[str(p)] = sha(p.read_bytes())
    for p in (ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'),
              Path('translations/release_stack.json')):
        external[str(p.resolve())] = sha(p.read_bytes())
    save(ARCHIVE / 'provenance.json', {'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes())
        for p in ARCHIVE.rglob('*') if p.is_file() and p.name != 'provenance.json'},
        'external_E_drive_evidence': external, 'full_goal_complete': False})
    print('V713 recorded and archived on E; all18 plaques/22 historical scopes retained; V712 experimental, full goal active.', flush=True)


if __name__ == '__main__':
    main()
