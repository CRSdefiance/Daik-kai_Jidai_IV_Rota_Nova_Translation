"""Record actual second-parent coverage and explicitly retain native suffix gaps."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.inspect_committed_gpu_v646 import SOURCE
from scripts.record_memory_streams_v682 import copy
from scripts.run_room_gender_v694 import CAP, ROOT
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V694 Actual room gender symbols')
KEY = 'actual_second_room_gender_parent28_complete_cells165_whole_pairs_native_suffix_gap_retained_v694'
DOC = Path('docs/room_gender_v694_checkpoint.md')
SOURCES = ('scripts/observe_room_gender_v694.py', 'scripts/run_room_gender_v694.py',
    'scripts/run_room_gender_selection_v694.py', 'scripts/run_room_gender_ITCM_v694.py',
    'scripts/replay_room_gender_v694.py', 'scripts/verify_room_gender_v694.py',
    'scripts/record_room_gender_v694.py', 'scripts/verify_room_gender_archive_v694.py',
    'scripts/observe_file_requests_v681.py', 'scripts/check_file_requests_v681.py')


def main():
    pp = ROOT / 'proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_room_gender_v694.py').read_bytes())
    assert proof['actual_second_loose_marker_parent_and_both_gender_cells_verified']
    assert proof['total_whole_RGB_pairs'] == 165 and proof['complete_native5_pixels'] == 7168
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    save(ROOT / 'visual_review.json', {'six_actual_room_selection_screens_opened': proof['review_sheet'],
        'sheet_sha256': proof['review_sheet_sha256'],
        'Hodram_Maria_Yukihisa_Xien_Yan_and_Maria_return_cells_complete_inside_boxes': True,
        'draft_sheet_actor10_label_corrected_from_Ian_to_actual_Xien_Yan_no_game_change': True,
        'native_suffix_memory_mismatch_embedded_consumer_and_identity8_exception_unresolved': True,
        'no_guide_promotion_or_user_acceptance_inferred': True})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': proof['candidate'], 'candidate_sha256': proof['candidate_sha256'],
        'actual_second_CDeckPersonnelView_room5_parent_and_both_gender_symbols_verified': True,
        'original_None32_null_room_bypass_explains_previous_missed_helper': True,
        'four_actual_actors_whole_original_native_cache_getters_source_bank48_and_draw_point80_80': True,
        'all28_complete16x16_cells7168_native5_pixels_and84_negative_controls_pass': True,
        'all165_whole_two_screen_RGB_pairs_and5_complete_terminal_RAM_pairs_exact': True,
        'native_intermediate_construction_states_exact_full_return_memory_mismatch_retained': True,
        'embedded_copy_consumer_and_identity8_story_exception_live_coverage_still_open': True,
        'all18_plaques_incomplete22_original_scopes_and_other_graphics_open_or_exact': True,
        'ROM_manifest_patch_registry_canonical_and_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        audit = read(path)
        assert audit == pre['all_original_audits_before'][name]
        assert audit.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert audit.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        audit[KEY], audit['current_goal_turn_classification'] = entry, 'progress'
        save(path, audit)
        copy(path, ARCHIVE / 'audits' / name)
    heading = '## V694: actual second room parent and complete gender symbols'
    addition = (
        'Previous status-only goal turn made no progress. Normal menu selection of a real '
        'Deck room reaches the original gender helper; None32 returns null and deliberately '
        'bypasses it. Actual parent RTTI is CDeckPersonnelView. Four actual actors bind whole '
        'Marker files through complete original native cache hits,bank48 and original draw '
        'point80,80. All28 complete16x16 cells7168 native5 pixels,including four female holds '
        'and return cycles,match;84 wrong-sex/palette/placement controls fail. Five observed '
        'versus unobserved cold-boot pairs match165 whole RGB screens and five full terminal '
        'RAM states. All intermediate native checkpoints through gender construction match '
        'complete CPU/RAM/DTCM/ITCM state;full helper return registers/CPSR/ITCM match but '
        'main-RAM/DTCM differences remain unwaived. Both None bypasses are fully exact. '
        'Actual review sheet opened;draft actor10 label corrected to Xien Yan. This closes '
        'second loose-parent display coverage,not embedded-copy use,identity8 story exception '
        'or full suffix equivalence. All18 plaques incomplete,22 historical scopes exact '
        'and broader graphics/restoration/older checks/acceptance open. V692/patch/registry/'
        'pointers unchanged;no guide promotion,commit or push. Evidence on E;full goal active. '
        'See [V694 checkpoint](room_gender_v694_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        content = path.read_text(encoding='utf-8')
        assert heading not in content
        path.write_text(content.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
        copy(path, ARCHIVE / 'docs' / name)
    for path in (*map(Path, SOURCES), DOC):
        copy(path, ARCHIVE / 'sources' / path)
    for name in ('MMU.cpp', 'MMU.h', 'armcpu.h'):
        copy(SOURCE / name, ARCHIVE / 'core_source' / name)
    for path in ROOT.rglob('*'):
        if path.is_file():
            copy(path, ARCHIVE / 'analysis' / path.relative_to(ROOT))
    external = {}
    for folder in CAP.glob('room_gender_v694_*'):
        for path in folder.rglob('*'):
            if path.is_file():
                external[str(path)] = sha(path.read_bytes())
    save(ARCHIVE / 'provenance.json', {'scripts': {p: sha(Path(p).read_bytes()) for p in SOURCES},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'external_E_drive_evidence': external, 'no_guide_promotion_or_new_ROM': True,
        'native_complete_return_memory_mismatches_retained': True, 'full_goal_complete': False})
    print('V694 actual second-parent symbol evidence, native limits and unchanged audit scope recorded on E.', flush=True)


if __name__ == '__main__':
    main()
