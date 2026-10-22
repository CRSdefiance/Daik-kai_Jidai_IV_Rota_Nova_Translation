"""Archive real regional-page evidence; retain the full graphics goal scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_regional_map_pages_v641 import CAP, CONTROL, ROM, ROOT
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/regional_map_pages_v641_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V641 Regional map pages')
GUIDE = Path('E:/Rota Nova translations/Screenshots/Guide candidates/V640 Regional maps')
KEY = 'all7_actual_ordinary_blue_regional_map_pages_and_North_Sea_repeat_v641'


def main():
    proof_path = ROOT / 'actual_regional_pages_proof.json'
    proof = read(proof_path)
    before = read(ROOT / 'preflight.json')
    assert proof['candidate_sha256'] == before['candidate_sha256'] == sha(ROM.read_bytes())
    assert proof['unique_actual_regional_pages_verified'] == list(range(7))
    rows = proof['all7_actual_regional_pages_and_North_Sea_repeat']
    assert len(rows) == 8
    assert proof['negative_wrong_page_rejected'] and not proof['full_goal_complete']
    for path, digest in proof['scripts'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, digest in before['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    # All comparisons precede archive writes and audit mutations.
    for name, scope in frozen.items():
        data = read(Path('translations') / name)
        assert all(data[k] == v for k, v in before['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    GUIDE.mkdir(parents=True, exist_ok=True)
    files = [DOC, proof_path, ROOT / 'preflight.json', ROOT / 'complete_replay_inputs.json',
             ROOT / 'actual_page_cases.json', ROOT / 'navigation_findings.json',
             ROOT / 'north_sea_draw_chain.json', ROOT / 'source_art_preservation.json', ROOT / 'visual_review.json',
             CAP / 'navigation_command_journal.json', ROM.with_suffix('.manifest.json'), Path(__file__)]
    files.extend(Path(p) for p in proof['scripts'])
    for source in files:
        checked_copy(source, ARCHIVE / source.name)
    for label, folder in (('current_V640', CAP), ('control_V636', CONTROL)):
        checked_copy(folder / 'capture_report.json', ARCHIVE / (label + '_capture_report.json'))
    screenshots, guides, native_exports = [], [], []
    for row in rows:
        frame, page = row['frame'], row['actual_source_page']
        for label, field in (('CURRENT_V640', 'PNG'), ('CONTROL_V636', 'control_PNG')):
            shot = row[field]
            target = ARCHIVE / f'{label}_page{page}_frame{frame:06d}_UNMODIFIED_NATIVE.png'
            checked_copy(shot['path'], target)
            screenshots.append({'path': str(target), 'frame': frame, 'page': page,
                'actual_region': row['actual_region'], 'sha256': shot['PNG_sha256'],
                'unmodified_capture': True, 'ordinary_map_browsing_not_travel': True,
                'control': label.startswith('CONTROL')})
            if label.startswith('CURRENT') and frame in (42800, 50000):
                guide = GUIDE / target.name
                checked_copy(shot['path'], guide)
                guides.append({**screenshots[-1], 'path': str(guide)})
        export = row['native_export']
        checked_copy(export['path'], ARCHIVE / f'frame{frame:06d}_native_state.json')
        native_exports.append(export)
    save(GUIDE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
        'source_report': proof['reports'][0], 'screenshots': guides,
        'ordinary_no_preloaded_save_no_savestate_no_cheat': True,
        'map_browsing_not_voyage_docking_or_earned_discovery': True,
        'publication_approved': False, 'full_route_completion_not_claimed': True})
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
        'control_candidate_sha256': proof['control_candidate_sha256'], 'screenshots': screenshots,
        'guide_candidates': guides, 'read_only_native_exports': native_exports,
        'all_full_RAM_VRAM_and_run_files_remain_on_E': True, 'full_goal_complete': False,
        'files': {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir()
                  if p.is_file() and p.name != 'provenance.json'}})
    entry = {'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'],
        'all7_actual_blue_regional_pages_verified_in_ordinary_browsing': True,
        'North_Sea_repeat_after_all_regions_verified': True,
        'all312320_source_indices_and_actual_VRAM_crop_pixels_verified': True,
        'all786432_current_and_V636_control_two_screen_pixels_exact': True,
        'all8_actual_map_callbacks_full_ABI_clean_code_palette_source_extent_and_destination_verified': True,
        'Med_hover_Y_page0_diagnostic_preserved_wrong_page_negative_control_rejected': True,
        'route_overlay_producers_sepia_legacy_other_map_states_remain_open': True,
        'no_voyage_docking_earned_route_unlock_or_full_route_claim': True,
        'all18_original_plaques_incomplete_all22_scopes_exact': True,
        'ROM_patch_registry_canonical_and_all_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'guide_candidates': str(GUIDE),
        'full_goal_complete': False, 'canonical_promoted': False}
    for name in frozen:
        path = Path('translations') / name
        data = read(path)
        data[KEY] = entry
        data['current_goal_turn_classification'] = 'progress'
        save(path, data)
        current = read(path)
        assert all(current[k] == v for k, v in before['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
    heading = '## V641: all seven actual regional map pages through ordinary controls'
    addition = """

Fresh current V640 and V636 control cold boots use the same ordinary50000-frame
schedule, without saves, savestates or fixtures. All7 actual blue regional pages
plus North Sea repeat match complete source bitmaps and palettes:312320 native
indices. Eight registered map painters pass full ABI/clean code and actual full
extent/destination checks;312320 VRAM pixels match the displayed map crops.
All786432 paired two-screen pixels match without exclusions, including overlays
and five black upper-screen states. Hover Med+Y retained page0;A Done commits the
chosen region. The preserved diagnostic and rejected wrong-page control prevent
mistaking tooltips for actual pages.16 unmodified current/control screens and2
ordinary map-browsing guide candidates are saved on E. No ROM/patch/registry or
release pointer changes;V640 remains compiled experimental. All18 plaques remain
incomplete and22 historical scopes exact. Sepia/legacy/other map states and route
overlay producers remain open alongside the broader graphics gates. See
[V641 checkpoint](regional_map_pages_v641_checkpoint.md).
"""
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip() + '\n\n' + heading + '\n' + addition, encoding='utf-8')
    for path, digest in before['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    print('Archived16 unmodified regional map screens/2 guide candidates;3 additive audits;all18/22 scopes and release artifacts preserved.')


if __name__ == '__main__':
    main()
