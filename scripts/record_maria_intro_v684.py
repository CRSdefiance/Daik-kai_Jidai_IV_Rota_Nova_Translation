"""Record actual opening coverage and the unwaived percent defect with full scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.run_maria_intro_v684 import CAP, ROOT
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V684 Maria complete opening')
DOC = Path('docs/maria_intro_v684_checkpoint.md')
KEY = 'actual_complete_Maria_opening_to_Hangzhou45_photo_holds37_caption_masks_real_percent_defect_v684'
SCRIPTS = ('scripts/run_maria_intro_v684.py', 'scripts/verify_maria_intro_v684.py',
           'scripts/record_maria_intro_v684.py', 'scripts/trace_file_ids_v683.py')


def main():
    pp = ROOT / 'proof.json'
    pre, proof = read(ROOT / 'preflight.json'), read(pp)
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_maria_intro_v684.py').read_bytes())
    assert proof['two_fresh31000_frame_runs49_whole_baseline_pairs_and49_pilot_pairs_and_terminal_RAM_exact']
    assert proof['one_confirmed_percent_corruption_not_waived_and_repair_required']
    assert len(proof['actual_source_art_cases']) == 45
    assert sum(c['status'] == 'complete_native_font_mask_pass' for c in proof['caption_cases']) == 37
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'status': 'full_opening_navigation_source_art_verified_percent_defect_and_blank_hold_contexts_open',
        'actual_normal_inputs_to_Hangzhou_no_story_location_or_movie_fixture': True,
        'system_unlock_save_is_authorized_isolated_access_not_earned': True,
        '49_complete_baseline_pairs49_pilot_pairs_and_three_terminal_RAM_states_exact': True,
        '45_complete_source_photo_holds2211840_RGB5_pixels_seven_actual_requested_files': True,
        '37_complete_dialogue_foreground_masks_with_actual_FI_Maria_expansion': True,
        'three_blank_holds_four_join_notices_Town_no_chapter_font_clearance': True,
        'SC3_B33_R0137_actual_3_percent_octal_corruption_is_unwaived_and_requires_repair': True,
        'two_more_literal_percent_route_records_identified_for_source_review': True,
        'all18_plaques_incomplete22_historical_objects_exact_broader_graphics_open': True,
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
    heading = '## V684: complete Maria opening navigation and a real percent-format defect'
    addition = ('Ordinary Maria New Game reaches Hangzhou with the authorized isolated '
        'system unlock and no story/location/movie substitution. Two31000-frame runs '
        'match49 whole baseline pairs,49 pilot pairs and all terminal RAM.45 upper '
        'photo holds2211840 RGB5 pixels bind seven actual requested source photos;37 '
        'complete dialogue foreground masks and native FI=Maria expansions pass. '
        'Three blank holds retain unresolved wait/padding context;four dynamic join '
        'notices and Town get no chapter-font claim. The actual SC3B33R0137 phrase '
        '3% of sales is corrupted by native octal parsing of percent-space-o. It '
        'fails the intended mask and remains unwaived. Source review also finds '
        'SC2B133R0136 and SC3B135R0325 literal-percent hazards;registered repairs '
        'and a source-bound final-build contract gate follow separately. Initial '
        'stdin EOF and ASCII-only speaker/font assumptions are retained. V678/patch/'
        'registry/pointers unchanged;all18 plaques incomplete,22 scopes exact,full '
        'graphics goal active. Evidence archived on E,no guide promotion. See '
        '[V684 checkpoint](maria_intro_v684_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    for case in ('pilot', 'pilot_interactive', 'observed', 'baseline'):
        folder = CAP / ('maria_intro_v684_' + case)
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
    files = {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
             if p.is_file() and p.name != 'provenance.json'}
    save(ARCHIVE / 'provenance.json', {'files': files, 'candidate_sha256': pre['candidate_sha256'],
        'known_percent_defect_not_waived_and_original_graphics_scope_preserved': True, 'full_goal_complete': False})
    # Finish with independent reads of copied bytes and frozen source invariants.
    assert all(sha((ARCHIVE / name).read_bytes()) == digest for name, digest in files.items())
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    for name in frozen:
        data = read(Path('translations') / name)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k != 'current_goal_turn_classification')
        assert (Path('translations') / name).read_bytes() == (ARCHIVE / 'audits' / name).read_bytes()
    save(ROOT / 'final_verification.json', {'archive_files_verified': len(files),
        'full_opening_navigation_source_art37_foreground_masks_and_unwaived_defect_saved': True,
        'all_release_hashes_unchanged18_plaques_incomplete22_scopes_exact': True,
        'recorder_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f'V684 final: {len(files)} archive files exact; real percent defect retained for repair; graphics goal active.', flush=True)


if __name__ == '__main__':
    main()
