"""Record original wedding source ownership and retain the actual-playback gate."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.research_wedding_command_v676 import ROOT
from scripts.run_village_visits_v664 import CAP
from scripts.verify_village_wrap_v608 import read, save

ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V676 Lil wedding source')
DOC = Path('docs/wedding_source_v676_checkpoint.md')
KEY = 'original_Lil_B70_4906_wedding_movie_M26_source_consumer_and_live_B22_control_v676'
SCRIPTS = ('scripts/research_wedding_command_v676.py', 'scripts/load_wedding_block_v676.py',
           'scripts/prepare_wedding_runtime_v676.py', 'scripts/observe_wedding_runtime_v676.py',
           'scripts/run_wedding_runtime_v676.py', 'scripts/verify_wedding_source_v676.py',
           'scripts/record_wedding_source_v676.py', 'scripts/verify_wedding_archive_v676.py',
           'scripts/observe_graphic_paints_v669.py', 'scripts/factory_filter_controls_v674.py',
           'scripts/research_graphics_file_open_v301.py')


def copy(source, target):
    target = Path(target)
    target.parent.mkdir(parents=True, exist_ok=True)
    checked_copy(source, target)


def main():
    pp = ROOT / 'proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    assert proof['verifier_sha256'] == sha(Path('scripts/verify_wedding_source_v676.py').read_bytes())
    assert proof['M26_Lil_chapter70_source_consumer_identified_actual_wedding_playback_still_open']
    assert proof['total_records'] == 19744 and proof['primitive_entry_count'] == 19739
    assert proof['original_Lil_CS2_block70_command'] == {'offset': 4324, 'word': 0x4906, 'native_movie_args': [26, 0, 1, 0]}
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'status': 'original_Lil_wedding_source_consumer_identified_actual_M26_playback_still_open',
        'source': '/data/SC2.DK4 block70 offset4324 word4906 -> M26',
        '414_original_clean_current_linear_command_extents_not_runtime_branch_reachability': True,
        '512_complete_original_selector_ABI_guard_cases_playback_reset_bridges_disclosed': True,
        'two_original_CS_block70_loaders_all6764_bytes_exact_only_SDK_IO_bridged': True,
        'four_original_M22_M26_filename_generation_cases_stop_before_decoder': True,
        'two_ordinary_Lil_New_Game_cold_boots_no_save_savestate_or_gameplay_fixtures': True,
        'all12_whole_screen_pairs_and_terminal_RAM_exact': True,
        'actual_B22_loader_chapter2_and_M22_requests_with_four_full3000_byte_buffers': True,
        '39_native_host_controls_three_original_alias_slots_restored_before_filter_free': True,
        'inapplicable_blitter_guards_retained_and_first12_nonprimitive_fields_only': True,
        'two_original_M26_source_photos_retained_not_actual_wedding_screenshots': True,
        'actual_wedding_loading_composition_crops_transitions_and_earned_trigger_not_proven': True,
        'all18_plaques_incomplete22_original_requirements_exact_other_gates_open': True,
        'ROM_patch_registry_canonical_and_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'full_goal_complete': False}
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert all(data[key] == value for key, value in pre['all_original_audits_before'][name].items()
                   if key != 'current_goal_turn_classification')
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(path, data)
    heading = '## V676: original Lil wedding command and ordinary loader/selector control'
    addition = ('M26 has an original source consumer:SC2 block70 offset4324 word4906. '
        'The separate chapter-movie family adds20 to its low byte;the earlier4200-family '
        'search did not cover it. Two original clean/current CS loaders reproduce6764 whole '
        'block bytes with only SDK I/O bridged;414 linear native extents and512 complete '
        'selector ABI/guard cases pass with explicit playback/reset/effect bridges. Four '
        'native M22/M26 filenames bind exact source files before decoding. Two ordinary '
        '4000-frame Lil New Games,no gameplay fixtures,match12 whole screen pairs and full '
        'terminal RAM. Original B22 loader/chapter2/M22 requests and four entire3000-byte '
        'resident buffers bind the live mechanism.39 host controls pass across921/927/92F '
        'slots sharing513F0;all pointers restored.19744 entries include19739 ordinary zero-guard '
        'primitives and five explicit argument-only records. Both original wedding source '
        'pictures are retained; actual M26 wedding playback/crops/transitions remain next. '
        'V666/patch/registry/pointers unchanged;all18 plaques incomplete and22 scopes exact. '
        'Evidence on E,no guide promotion. See [V676 checkpoint](wedding_source_v676_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        value = path.read_text(encoding='utf-8')
        if heading not in value:
            path.write_text(value.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    for tag in ('observed', 'baseline'):
        folder = CAP / ('wedding_source_v676_' + tag)
        for source in folder.rglob('*'):
            if source.is_file() and source.suffix.lower() in ('.json', '.png', '.bin', '.log', '.txt'):
                copy(source, ARCHIVE / 'runs' / folder.name / source.relative_to(folder))
    for source in (DOC, *map(Path, SCRIPTS)):
        copy(source, ARCHIVE / 'sources' / source.name)
    for source in ROOT.rglob('*'):
        if source.is_file():
            copy(source, ARCHIVE / 'analysis' / source.relative_to(ROOT))
    for item in proof['M26_original_scene_art']:
        source = Path(item['source_preview'])
        copy(source, ARCHIVE / 'original_source_art_not_gameplay_capture' / source.name)
    for name in frozen:
        copy(Path('translations') / name, ARCHIVE / 'audits' / name)
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        copy(Path('docs') / name, ARCHIVE / 'docs' / name)
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': pre['candidate_sha256'],
        'two_ordinary_runs_terminal_no_gameplay_fixtures': True,
        'source_scripts': {path: sha(Path(path).read_bytes()) for path in SCRIPTS},
        'files': {str(path.relative_to(ARCHIVE)): sha(path.read_bytes()) for path in ARCHIVE.rglob('*')
                  if path.is_file() and path.name != 'provenance.json'},
        'source_consumer_identified_not_actual_wedding_playback_or_earned_story_claim': True,
        'full_goal_complete': False})
    print('V676 original wedding source and live control archived; three audits/four docs updated;18/22 preserved.', flush=True)


if __name__ == '__main__':
    main()
