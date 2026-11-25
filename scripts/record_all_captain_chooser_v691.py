"""Record current all-four chooser coverage with every original pending scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.run_all_captain_chooser_v691 import CAP, ROOT
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V691 All captain chooser')
DOC = Path('docs/all_captain_chooser_v691_checkpoint.md')
KEY = 'actual_all_four_captain_chooser56_complete_fields198016_photo_pixels14_cache_hits_v691'
SCRIPTS = tuple('scripts/' + p for p in (
    'run_all_captain_chooser_v691.py', 'verify_all_captain_chooser_v691.py',
    'record_all_captain_chooser_v691.py', 'verify_all_captain_chooser_archive_v691.py',
    'trace_chooser_raw_independence_v690.py', 'observe_file_requests_v681.py'))


def main():
    pre, proof = read(ROOT / 'preflight.json'), read(ROOT / 'proof.json')
    pp = ROOT / 'proof.json'
    assert proof['runner_sha256'] == sha(Path(SCRIPTS[0]).read_bytes())
    assert proof['verifier_sha256'] == sha(Path(SCRIPTS[1]).read_bytes())
    assert proof['all56_whole_name_middle_surname_company_fields_complete']
    assert proof['all14_complete_portrait_planes198016_native5_pixels_match_original']
    assert proof['all14_full_RGB_case_pairs_equal']
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    save(ROOT / 'visual_review.json', {
        'opened_all_four_control_and_declared_fixture_actual_screens': proof['review_sheet'],
        'sheet_sha256': proof['review_sheet_sha256'],
        'all_four_names_middle_last_company_fields_and_whole_portraits_reviewed': True,
        'no_new_clipping_stale_letters_or_missing_edges_identified': True,
        'fixture_access_not_earned_no_guide_approval_or_global_nonuse_claim': True})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'two_terminal5200_frame_runs_actual_all_four_selections_and_reverse_return_cycle': True,
        'all56_whole113x11_name_middle_surname_company_masks_including_blanks_exact': True,
        'all14_original104x136_photo_planes198016_native5_pixels_exact_including_Maria': True,
        'all14_real_initialized_owners_original_native_cached_files_and_ABI_verified': True,
        '14_whole_RGB_pairs_equal_raw_pattern_persists_all_captains_other_RAM_exact': True,
        'existing_authorized_system_unlock_not_earned_second_case_single_declared_raw_fixture': True,
        'biography_prose_not_rewritten_or_granted_full_editorial_review': True,
        'all18_plaques_incomplete22_original_scopes_exact_other_graphics_contexts_open': True,
        'ROM_manifest_patch_registry_canonical_donors_release_pointers_unchanged': True,
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
    heading = '## V691: actual all-four captain portraits, names and return cycle'
    addition = (
        'Two5200-frame V685 cold boots cycle Rafael/Hodram/Lil/Maria and back '
        'using the unchanged authorized system-unlock donor. All56 whole113x11 '
        'first/middle/last/company fields match independent complete font masks, '
        'including empty/trailing cells. All14 full104x136 portraits198016 '
        'native-five-bit pixels match original PXL files;14 original cache-hit '
        'getters bind actual owners/whole files with complete ABI and no I/O '
        'bridges.14 whole RGB case pairs match while the declared raw17 pattern '
        'persists across every captain state;all other captured/terminal main '
        'RAM is exact. Actual four-captain sheet reviewed,no new visible defect '
        'identified. This closes current loose-portrait/default-field coverage, '
        'not other raw consumers,all frames,prose or global nonuse. All18 plaques '
        'remain incomplete and22 original scopes exact;ROM/patch/registry/donors/'
        'pointers unchanged. Evidence on E,no guide approval. See '
        '[V691 checkpoint](all_captain_chooser_v691_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        assert heading not in text
        path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
        copy(path, ARCHIVE / 'docs' / name)
    for p in (DOC, *map(Path, SCRIPTS)):
        copy(p, ARCHIVE / 'sources' / p.name)
    for p in ROOT.rglob('*'):
        if p.is_file():
            copy(p, ARCHIVE / 'analysis' / p.relative_to(ROOT))
    for case in ('control', 'poison'):
        folder = CAP / ('all_captain_chooser_v691_' + case)
        for p in folder.rglob('*'):
            if p.is_file():
                copy(p, ARCHIVE / 'runs' / case / p.relative_to(folder))
    copy(pre['inherited_identical_host_controls'], ARCHIVE / 'controls/native_prefix_controls.json')
    save(ARCHIVE / 'provenance.json', {
        'scripts': {p: sha(Path(p).read_bytes()) for p in SCRIPTS},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'fixture_screens_not_guide_approved': True, 'full_goal_complete': False})
    print('V691 all-four chooser source photos, full name fields and declared fixture archived on E.', flush=True)


if __name__ == '__main__':
    main()
