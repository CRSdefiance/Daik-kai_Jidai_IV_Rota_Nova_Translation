"""Record actual original-parent card display evidence while retaining reachability."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_memory_streams_v682 import copy
from scripts.run_village_cards_v699 import CAP, ROOT
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V699 Village card displays')
DOC = Path('docs/village_cards_v699_checkpoint.md')
KEY = 'eight_village_cards_original_event_parent16_actual_planes786432_pixels_v699'
SOURCES = ('scripts/run_village_cards_v699.py', 'scripts/verify_village_cards_v699.py',
    'scripts/record_village_cards_v699.py', 'scripts/verify_village_cards_archive_v699.py',
    'scripts/observe_file_requests_v681.py', 'scripts/check_file_requests_v681.py',
    'scripts/verify_event_still_routing_v426.py')


def main():
    pp = ROOT / 'proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_village_cards_v699.py').read_bytes())
    assert proof['eight_cards_two_complete_actual_holds_each786432_native5_pixels_exact']
    assert len(proof['complete_source_planes_and_resident_files']) == 18
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert sha(Path(pre['donor']).read_bytes()) == pre['donor_sha256']
    save(ROOT / 'visual_review.json', {'all8_complete_actual_two_screen_and_original_current_comparison_sheets_opened': True,
        'sheets': proof['review_sheets'],
        'white_background_is_original_source_art_not_missing_landscape': True,
        'complete_English_labels_readable_first_final_letters_fit': True,
        'image207_upper_source_stroke_preserved_identity_not_interpreted': True,
        'isolated_parent_argument_fixture_not_ordinary_village_use_or_guide_evidence': True})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'all8_cards_original_native_parent_loader_renderer_display_verified_with_CPU_argument_fixture': True,
        'all16_complete_card_holds786432_pixels_and18_whole_resident_PXL_files_exact': True,
        'all96_pre_fixture_full_RGB_RAM_pairs8_full_entry_states_and16_lower_hold_pairs_exact': True,
        'five_host_prefix8_read_and37_fixture_plan_controls_pass': True,
        'all8_card_files_unchanged_and_image207_fragment_preserved': True,
        'ordinary_scene_usage_computed_consumer_and_global_nonuse_NOT_proven': True,
        'all18_plaques_incomplete22_historical_objects_and_full_goal_preserved': True,
        'V698_prefix_and_V694_suffix_gaps_not_cleared': True,
        'ROM_patch_registry_donor_canonical_release_pointers_unchanged': True,
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
    heading = '## V699: eight village cards through the original event-image renderer'
    addition = (
        'Nine terminal4000-frame cold boots use original Maria New Game and the '
        'existing authorized unlock donor. Eight declared fixtures change only '
        'the original image84 parent argument R1 at3749; a disabled control keeps84. '
        'All16 full card planes786432 native5 pixels, two original84 planes98304 '
        'pixels and18 whole resident PXLs match. All96 pre-fixture whole RGB/RAM '
        'pairs,eight full CPU/WRAM/DTCM/ITCM entry states and16 lower holds match '
        'the control. Five native host8 read37 plan cases pass. Initial main-only '
        'option guard failure retained; final bounded DTCM options derive from '
        'the original script instruction. Both full and source/current sheets '
        'opened: white backgrounds are original placeholder art,all caption '
        'edges fit,image207 upper stroke retained. All8 files unchanged from '
        'reviewed V414. This closes fixture-based actual loader/render/crop '
        'coverage,not ordinary village triggers,indirect consumers or global '
        'nonuse. All18 plaques incomplete,22 historical scopes exact; V698 '
        'prefix/V694 suffix gaps and broader graphics/restoration/older checks/'
        'acceptance remain open. V692/patch/registry/pointers/donor unchanged; '
        'evidence on E,no guide promotion/commit/push. Full goal active. See '
        '[V699 checkpoint](village_cards_v699_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        content = path.read_text(encoding='utf-8')
        assert heading not in content
        path.write_text(content.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
        copy(path, ARCHIVE / 'docs' / name)
    for path in (*map(Path, SOURCES), DOC):
        copy(path, ARCHIVE / 'sources' / path)
    for path in ROOT.parent.rglob('*'):
        if path.is_file():
            copy(path, ARCHIVE / 'analysis' / path.relative_to(ROOT.parent))
    external = {}
    for folder in CAP.glob('village_cards_v699_*'):
        for path in folder.rglob('*'):
            if path.is_file():
                external[str(path)] = sha(path.read_bytes())
    save(ARCHIVE / 'provenance.json', {'scripts': {p: sha(Path(p).read_bytes()) for p in SOURCES},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'},
        'external_E_drive_evidence': external,
        'initial_no_fixture_failure_retained_final_nine_runs_terminal': True,
        'no_ordinary_village_use_earned_progress_or_guide_claim': True, 'full_goal_complete': False})
    print('V699 eight actual card display checks recorded; ordinary village use and broader scope remain open.', flush=True)


if __name__ == '__main__':
    main()
