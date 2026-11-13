"""Record the bounded Save/Load stream and plaque evidence without closing scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_memory_streams_v682 import ROOT
from scripts.record_regional_ui_v616 import checked_copy
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V682 Save Load memory streams')
DOC = Path('docs/memory_streams_v682_checkpoint.md')
KEY = 'actual_Save_Load_memory_buffers32_full_pairs36_Level_Power_regions_v682'
SCRIPTS = ('scripts/prepare_memory_streams_v682.py', 'scripts/observe_memory_streams_v682.py',
    'scripts/check_memory_streams_v682.py', 'scripts/run_memory_streams_v682.py',
    'scripts/verify_memory_streams_v682.py', 'scripts/record_memory_streams_v682.py',
    'scripts/verify_memory_streams_archive_v682.py', 'scripts/observe_file_requests_v681.py')


def copy(source, target):
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    checked_copy(source, target)


def main():
    pp = ROOT / 'proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_memory_streams_v682.py').read_bytes())
    assert proof['two_terminal14200_frame_cold_boots32_whole_screen_pairs_and_terminal_RAM_exact']
    assert len(proof['source_Save_Load_asset_exact_V612_and_all36_plaque_regions26568_pixels_verified']) == 36
    assert proof['two_mode1_payloads74030_bytes_exact_donor_save_slots5_and0']
    config = read(ROOT / 'run_config.json')
    assert sha(Path(config['donor']).read_bytes()) == config['donor_sha256']
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    save(ROOT / 'visual_review.json', {'eight_actual_Save_Load_frames_opened': True,
        'complete_labels_six_slot_list_confirmation_and_final_Stockholm_display_reviewed': True,
        'no_new_defect_identified_in_selected_views': True,
        'wood_restoration_remains_approximate_all18_entries_incomplete': True,
        'test_evidence_not_guide_promotion': True})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'status': 'known_Save_Load_RAM_streams_and_current_Level_Power_verified_other_consumers_open',
        'two_terminal14200_frame_cold_boots32_complete_baseline_pairs_and_terminal_RAM_exact': True,
        '33_callbacks9_selected_records_complete_CPU_and4MiB_WRAM_unchanged_all_slots_restored': True,
        'two_complete37015_byte_mode1_payloads_exact_donor_slots6_and1': True,
        'mode2_current_game_preview_buffer_full_byte_readback_not_actual_cartridge_save': True,
        'mode2_cursor124_is_independent_of37015_byte_highwater_and_not_last_call_history': True,
        'known_modes_ignore_filename_not_additional_graphics_loaders_other_callers_open': True,
        '20_native_host_prefix8_mirror_controls40_complete_native_memory_operations': True,
        '36_complete_Level_Power_regions26568_native5_pixels_and_full_font_masks_verified': True,
        'both_failed_analyzer_assumptions_retained_no_production_change_or_new_emulator_run': True,
        'all18_plaques_incomplete22_original_requirements_exact_other_gates_open': True,
        'ROM_patch_registry_canonical_and_release_pointers_unchanged': True,
        'preceding_status_only_turn_classification': 'no_progress',
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
    heading = '## V682: actual Save/Load RAM streams and current Level/Power plaques'
    addition = ('Two complete14200-frame cold boots match32 whole two-screen pairs and terminal '
        'RAM. Nine selected records among33 read-only callbacks bind two complete37015-byte '
        'mode1 donor payloads to human slots6/1 and the mode2 current-game Save preview '
        'buffer. Original memory readback verifies all three;no actual cartridge Save '
        'or whole-game roundtrip is claimed. Cursor124 versus highwater37015 resolves '
        'an initial analyzer assumption;the rejected extra header-refresh idempotence '
        'probe/log is retained and removed from the current proof,without production '
        'changes.20 host-prefix,8 mirror and40 complete native operation controls pass. '
        'All36 Level/Power regions26568 native5 pixels and complete font masks match; '
        'the eight-frame review includes final Stockholm. Known mode1/2 callers are '
        'RAM serialization paths,not extra filename loaders;other consumers remain '
        'open. Hidden wood remains approximate;all18 plaques incomplete,22 historical '
        'scopes exact. V678/patch/registry/pointers unchanged;no guide promotion. '
        'Previous status-only turn:no progress;this checkpoint:progress. Evidence '
        'archived on E;full goal active. See [V682 checkpoint](memory_streams_v682_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        value = path.read_text(encoding='utf-8')
        assert heading not in value
        path.write_text(value.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    for mode in ('observed', 'baseline'):
        folder = CAP / f'memory_streams_v682_{mode}'
        for source in folder.rglob('*'):
            if source.is_file():
                copy(source, ARCHIVE / 'runs' / folder.name / source.relative_to(folder))
    for source in (DOC, *map(Path, SCRIPTS)):
        copy(source, ARCHIVE / 'sources' / source.name)
    for source in ROOT.rglob('*'):
        if source.is_file():
            copy(source, ARCHIVE / 'analysis' / source.relative_to(ROOT))
    for name in frozen:
        copy(Path('translations') / name, ARCHIVE / 'audits' / name)
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        copy(Path('docs') / name, ARCHIVE / 'docs' / name)
    save(ARCHIVE / 'provenance.json', {'source_scripts': {p: sha(Path(p).read_bytes()) for p in SCRIPTS},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
            if p.is_file() and p.name != 'provenance.json'}, 'candidate_sha256': pre['candidate_sha256'],
        'scope_is_known_Save_Load_callers_and_selected_plaques_not_all_graphics': True, 'full_goal_complete': False})
    print('V682 Save/Load RAM-stream and current plaque evidence archived;18/22 scopes retained.', flush=True)


if __name__ == '__main__':
    main()
