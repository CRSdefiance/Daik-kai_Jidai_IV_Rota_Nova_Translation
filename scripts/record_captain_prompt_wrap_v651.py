"""Archive the actual formatter repair and preserve the entire graphics goal."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/captain_prompt_wrap_v651')
DOC = Path('docs/captain_prompt_wrap_v651_checkpoint.md')
KEY = 'actual_five_captain_instruction_states_whole_words_native_bitmap_and_complete_V640_preservation_v651'
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V651 Captain instruction wrapping')
GUIDE = Path('E:/Rota Nova translations/Screenshots/Guide candidates/V651 Captain assignment')


def main():
    pp = ROOT / 'release_proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    assert len(proof['actual_complete_prompt269_and272_pixels']) == 5 and not proof['full_goal_complete']
    assert proof['comparisons']['newgame']['changed_frames'] == []
    assert proof['exact_all_byte_clean_patch_reconstruction']
    assert sha(Path(proof['candidate']).read_bytes()) == proof['candidate_sha256']
    assert sha(Path(proof['candidate']).with_suffix('.xdelta').read_bytes()) == proof['patch_sha256']
    reload = read(ROOT / 'five_ship_save_cold_reload.json')
    assert reload['source_battery_unchanged'] and len(reload['all5_original_model_getters']) == 5
    scripts = ['dk4tool/patch/captain_prompt_wrap.py', 'scripts/prepare_captain_prompt_wrap_v651.py',
               'scripts/probe_captain_prompt_wrap_v651.py', 'scripts/probe_captain_caller_v651.py',
               'scripts/run_captain_prompt_wrap_v651.py', 'scripts/verify_captain_prompt_wrap_v651.py',
               'scripts/record_captain_prompt_wrap_v651.py']
    assert proof['script_sha256'] == sha(Path(scripts[-2]).read_bytes())
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    latest = 'latest_compiled_experimental_candidate_with_inherited_native_gap'
    for name, scope in frozen.items():
        data = read(Path('translations') / name)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, latest, 'current_goal_turn_classification'))
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    GUIDE.mkdir(parents=True, exist_ok=True)
    for source in [DOC, *ROOT.glob('*.json'), *ROOT.glob('*.png'), *ROOT.glob('*.log'),
                   *map(Path, scripts), Path('translations/captain_prompt_wrap_v1.json')]:
        checked_copy(source, ARCHIVE / source.name)
    guides = []
    for receipt in [*proof['reports'], {'case': 'saved_five_ship', 'path': reload['report'], 'sha256': reload['report_sha256']}]:
        path = Path(receipt['path'])
        assert sha(path.read_bytes()) == receipt['sha256']
        case = receipt['case']
        checked_copy(path, ARCHIVE / (case + '_capture_report.json'))
        folder = ARCHIVE / case
        folder.mkdir(exist_ok=True)
        report = read(path)
        for shot in report['frames_captured']:
            destination = folder / Path(shot['path']).name
            checked_copy(shot['path'], destination)
            if case == 'fleet_candidate' and shot['frame'] in (32600, 35800):
                target = GUIDE / destination.name
                checked_copy(destination, target)
                guides.append({'path': str(target), 'sha256': shot['PNG_sha256'],
                               'source_report': str(path), 'frame': shot['frame'],
                               'ordinary_input_no_gameplay_fixture_unmodified_capture': True})
    assert len(guides) == 2
    save(GUIDE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
                                  'screenshots': guides, 'publication_approved': False})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
             'candidate': proof['candidate'], 'candidate_sha256': proof['candidate_sha256'],
             'profile': proof['profile'], 'patch_sha256': proof['patch_sha256'],
             'status': 'experimental_captain_modal_word_wrap_verified',
             'all4_native_IDs_added_only_at_exact_original_modal_parent': True,
             'all3664_other_IDs48_wrong_parent_and9_failure_controls_preserved': True,
             'five_actual_prompt_states_complete_native_glyphs_and_other_pixels_exact': True,
             'two_actual_complete10944_cell_bitmap_views_match_original_native_context_replay': True,
             'all89_New_Game_and149_other_fleet_whole_two_screen_pairs_exact': True,
             'four_terminal_no_fixture_comparisons_and_fifth_saved_fleet_reload': True,
             'all470_batches114_layers921_views57_embedded_extents_and_exact_patch_retained': True,
             'all18_original_plaques_incomplete_22_historical_scopes_exact': True,
             'miniature_Confirm_and_other_graphics_gates_open': True,
             'archive': str(ARCHIVE), 'guide_archive': str(GUIDE),
             'canonical_promoted': False, 'full_goal_complete': False}
    for name in frozen:
        path = Path('translations') / name
        data = read(path)
        data[KEY] = entry
        current = data.get(latest, {}).copy()
        current.update({'candidate': proof['candidate'], 'sha256': proof['candidate_sha256'],
                        'profile': proof['profile'], 'captain_instruction269_272_actual_word_wrap_verified': True,
                        'broader_graphics_gates_remain_open': True})
        data[latest], data['current_goal_turn_classification'] = current, 'progress'
        save(path, data)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, latest, 'current_goal_turn_classification'))
    heading = '## V651: captain-instruction modal family and complete actual wrapping'
    addition = ('Preserves all English prose and routes native captain IDs269..272 through '
        'the existing exact-parent modal wrapper in its128 owned bytes. All3668 IDs,48 '
        'wrong-parent and9 failure controls pass. Five actual269/272 states retain complete '
        'words/letters and aligned margins;all other pixels are exact. Two captured228x48 '
        'bitmap views match native replay using actual6x12 source cells/palette15;original '
        'display spacing is16. All89 New Game and149 other fleet screen pairs are exact; '
        'five-ship saved setup also cold reloads. V651 retains470 batches/114 layers/all921 '
        'views and57 embedded extents with an exact clean patch. Candidate/patch/captures '
        'and two guide candidates are on E. Latest compiled experimental pointer advances; '
        'canonical/V610 verified pointers remain. All18 plaques incomplete and22 scopes '
        'exact;full goal active. See [V651 checkpoint](captain_prompt_wrap_v651_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
        'all_used_test_batteries_are_isolated_copies_not_savestates': True,
        'RAM_native_exports_and_ROM_patch_retained_at_original_E_paths': True,
        'scripts': {p: sha(Path(p).read_bytes()) for p in scripts},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'}, 'full_goal_complete': False})
    print('V651 archived;three audits updated;latest compiled experimental pointer advances;all18/22 scopes retained.')


if __name__ == '__main__':
    main()
