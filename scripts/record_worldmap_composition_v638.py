"""Archive exact map composition evidence without narrowing historical scopes."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.probe_worldmap_overlays_v638 import ROM, ROOT
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_village_wrap_v608 import read, save

DOC = Path('docs/worldmap_composition_v638_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V638 World Map composition')
GUIDE = Path('E:/Rota Nova translations/Screenshots/Guide candidates/V636 World Map')
KEY = 'actual_original_World_Map281_overlay_producers_and_complete_composition_v638'


def main():
    proof_path = ROOT / 'native_composition_proof.json'
    proof = read(proof_path)
    assert sha(ROM.read_bytes()) == proof['candidate_sha256']
    assert proof['complete_actual_composite_pixels'] == 39040
    assert len(proof['original_registered_cursor_marker_and_map_callbacks']) == 3
    assert len(proof['all4_complete_current_and_historical_two_screen_regressions']) == 4
    for path, digest in proof['scripts'].items():
        assert sha(Path(path).read_bytes()) == digest
    report = read(proof['report'])
    assert sha(Path(proof['report']).read_bytes()) == proof['report_sha256']
    pre_path = ROOT / 'release_and_audit_before.json'
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    if not pre_path.exists():
        save(pre_path, {
            'audits': {name: read(Path('translations') / name) for name in frozen},
            'release_artifacts': {str(p): sha(p.read_bytes()) for p in (
                ROM, ROM.with_suffix('.xdelta'), ROM.with_suffix('.manifest.json'),
                Path('translations/release_stack.json'), Path('out/raphael_natural_v2_accepted_base.nds'))}})
    before = read(pre_path)
    for path, digest in before['release_artifacts'].items():
        assert sha(Path(path).read_bytes()) == digest
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    GUIDE.mkdir(parents=True, exist_ok=True)
    files = [DOC, proof_path, pre_path, ROOT / 'overlay_source_leads.json',
             ROOT / 'cursor_callback_probe.json', ROOT / 'registered_sprite_probe.json',
             Path(proof['report']), Path('scripts/headless_desmume_v193.py'), Path(__file__),
             ROM.with_suffix('.manifest.json'), Path('work/analysis/condition_matrix_v637/visual_review.json')]
    files.extend(Path(path) for path in proof['scripts'])
    for path in files:
        prefix = 'V637_' if path.name == 'visual_review.json' else ''
        checked_copy(path, ARCHIVE / (prefix + path.name))
    shots = {r['frame']: r for r in report['frames_captured']}
    screenshots = []
    for frame in (34800, 35200, 35600, 36000):
        row = shots[frame]
        target = ARCHIVE / f'ORDINARY_V636_frame{frame:06d}_UNMODIFIED_NATIVE.png'
        checked_copy(row['path'], target)
        screenshots.append({'path': str(target), 'frame': frame, 'sha256': row['PNG_sha256'],
                            'unmodified_capture': True, 'no_save_or_RAM_fixture': True})
        if frame == 36000:
            checked_copy(row['path'], GUIDE / target.name)
    save(GUIDE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
        'source_report': proof['report'], 'source_report_sha256': proof['report_sha256'],
        'frame': 36000, 'unmodified_capture': True, 'ordinary_no_preloaded_save_no_savestate_no_cheat': True,
        'complete_observed_map_composite_verified': True, 'publication_approved': False,
        'complete_route_or_all_map_states_not_claimed': True})
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
        'screenshots': screenshots, 'guide_candidate': str(GUIDE), 'full_goal_complete': False,
        'complete_RAM_native_and_original_run_files_retained_on_E': True,
        'files': {p.name: sha(p.read_bytes()) for p in ARCHIVE.iterdir()
                  if p.is_file() and p.name != 'provenance.json'}})
    entry = {
        'documentation': str(DOC), 'proof': str(proof_path), 'proof_sha256': sha(proof_path.read_bytes()),
        'candidate': str(ROM), 'candidate_sha256': proof['candidate_sha256'],
        'actual_original_cursor_marker_and_map_painters_complete_ABI_source_exact': True,
        'actual_whole_files_palette_banks_source_crops_and_native_destination_points_verified': True,
        'V551281_overlay_producer_gap_resolved_in_observed_state': True,
        'complete_actual_map_composite_pixels': 39040, 'complete_actual_physical_VRAM_crop_pixels': 39040,
        'four_whole_two_screen_regression_captures_exact': True,
        'mask_creation_other_pages_and_sepia_legacy_consumers_remain_open': True,
        'diagnostic_later_background_callback_failure_excluded_from_passing_scope': True,
        'all18_plaque_entries_incomplete_all22_historical_scopes_exact': True,
        'ROM_patch_registry_canonical_and_all_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'guide_candidate': str(GUIDE),
        'full_goal_complete': False, 'canonical_promoted': False,
    }
    for name, scope in frozen.items():
        path = Path('translations') / name
        data = read(path)
        assert all(data[k] == v for k, v in before['audits'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
        data[KEY] = entry
        data['current_goal_turn_classification'] = 'progress'
        save(path, data)
        assert all(read(path)[k] == v for k, v in before['audits'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
    heading = '## V638: original World Map overlay producers and whole observed composition'
    addition = '''

A fresh ordinary36000-frame V636 cold boot binds V551's281 unresolved overlay
pixels to the actual original cursor/marker callbacks, complete resident frame
and marker files, palette banks56/29 and executed crop/destination operands.
Three complete registered painter calls pass saved-register/stack ABI and every
executed instruction matches clean. All39040 map-composite pixels and39040
physical VRAM pixels match without excluded overlays; four whole two-screen
regression captures are exact. Four unmodified current screenshots and proofs
are saved on E, with one ordinary guide candidate. Full V637/V638 run folders are
also on E with path-preserving junctions and every moved file hash verified.
No ROM/patch/registry or release pointer changes. Original mask creation, other
map pages and sepia/legacy/raw comic/title consumers remain open. All18 original
plaques remain incomplete and22 historical scopes exact. Full goal active. See
[V638 checkpoint](worldmap_composition_v638_checkpoint.md).
'''
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip() + '\n\n' + heading + '\n' + addition, encoding='utf-8')
    print('Archived4 ordinary map captures and1 guide candidate;3 audits updated additively;all18/22 scopes and release artifacts preserved.')


if __name__ == '__main__':
    main()
