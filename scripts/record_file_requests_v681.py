"""Archive actual filename/source returns and current full Gallery evidence."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.prepare_file_requests_v681 import ROOT
from scripts.record_regional_ui_v616 import checked_copy
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V681 Actual file requests')
DOC = Path('docs/file_requests_v681_checkpoint.md')
KEY = 'actual234_SDK_filename_requests_four_complete_raw_returns_all164_Gallery_positions_v681'
SCRIPTS = ('scripts/prepare_file_requests_v681.py', 'scripts/observe_file_requests_v681.py',
    'scripts/check_file_requests_v681.py', 'scripts/run_file_requests_v681.py', 'scripts/verify_file_requests_v681.py',
    'scripts/record_file_requests_v681.py', 'scripts/verify_file_requests_archive_v681.py',
    'scripts/verify_gallery_carousels_v522.py')


def copy(source, target):
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    checked_copy(source, target)


def main():
    pp = ROOT / 'proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_file_requests_v681.py').read_bytes())
    assert proof['all164_current_Gallery_photos_captions_descriptions_and_wraps_verified']
    assert proof['ordinary_four_actual_raw14_to17_payloads_complete_no_IO_stubs']
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    save(ROOT / 'visual_review.json', {'twelve_actual_Gallery_first_middle_last_frames_four_routes_opened': True,
        'caption_edge_letters_bounds_headings_descriptions_and_photos_reviewed': True,
        'no_new_defect_identified_in_selected_views': True,
        'system_unlock_fixture_not_earned_access_no_guide_approval': True})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'status': 'actual_Gallery_and_ordinary_file_paths_complete_raw_positive_control_other_consumers_open',
        'four_terminal_cold_boots193_complete_observed_baseline_pairs_and_terminal_RAM_exact': True,
        '234_actual_SDK_filename_entries_and8_original_raw_entry_return_events': True,
        'all_four_actual_raw14144_byte_blocks14_15_16_17_exact_source_no_IO_bridges': True,
        'all159_Gallery_photo_filenames_requested_before164_source_verified_displays': True,
        'all164_complete_captions_headings_descriptions_runtime_pointers_and4_wraps_verified': True,
        'photo_source_comparison_is_complete_five_bit_planes_baseline_RGB_is_full_precision': True,
        '15_native_prefix_ABI_and8_main_RAM_mirror_controls': True,
        'every_callback_CPU_prefix_and4MiB_WRAM_unchanged_all3_opcode_slots_restored': True,
        'no_legacy_Confirm_or_standalone_request_in_these_schedules_not_global_nonuse': True,
        'Gallery_system_unlock_save_disclosed_not_earned_progress_or_guide_approval': True,
        'all18_plaques_incomplete22_original_requirements_exact_other_gates_open': True,
        'ROM_patch_registry_canonical_and_release_pointers_unchanged': True,
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
    heading = '## V681: actual filename requests and complete current Event Scenes'
    addition = ('Four terminal cold boots compare193 complete observed/baseline pairs and '
        'two full terminal RAM pairs. A read-only three-slot host trace records234 SDK '
        'filename entries plus four original raw entries/four caller returns. Actual '
        'New Game raw blocks14..17 return all14144 source bytes each without SDK bridges '
        'or forced selectors. Gallery records195 requests/178 paths;all159 distinct photo '
        'paths precede their164 displayed positions. The unchanged original verifier '
        'passes all164 full photo five-bit planes8060928 comparisons,complete captions/'
        'headings/descriptions/runtime pointers,popup labels and four wraps;baseline RGB '
        'is full precision.15 native prefix/ABI and8 bounded mirror controls pass;every '
        'callback preserves CPU prefix/full4MiB WRAM and all slots restore. Twelve current '
        'Gallery frames visually reviewed. No rawcomic/legacy/standalone/Confirm request '
        'through this interface in these schedules is not global non-use;other paths '
        'stay open. Gallery access uses the disclosed original system-unlock save;no '
        'earned/guide claim. V678/patch/registry/pointers unchanged;all18 plaques incomplete '
        'and22 scopes exact. Evidence on E,full graphics goal active. See '
        '[V681 checkpoint](file_requests_v681_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        value = path.read_text(encoding='utf-8')
        assert heading not in value
        path.write_text(value.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    for case in ('ordinary', 'gallery'):
        for mode in ('observed', 'baseline'):
            folder = CAP / f'file_requests_v681_{case}_{mode}'
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
        'actual_file_request_scope_not_global_unused_art_or_earned_Gallery_access': True, 'full_goal_complete': False})
    print('V681 actual file requests/Gallery/source evidence archived;18/22 scopes retained.', flush=True)


if __name__ == '__main__':
    main()
