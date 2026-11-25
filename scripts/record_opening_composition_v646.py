"""Archive ordinary opening proof without changing prior requirements/releases."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/opening_composition_v646')
KEY = 'ordinary_opening_all170_M28_native_views_committed_geometry_VRAM_611_complete_RGB_frames_v646'
DOC = Path('docs/opening_composition_v646_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V646 Opening source composition')
GUIDE = Path('E:/Rota Nova translations/Screenshots/Guide candidates/V640 Opening movie')


def main():
    pp = ROOT / 'opening_composition_proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    assert proof['all611_complete_upper_RGB_compositions_exact_without_exclusions']
    assert proof['all22_English_planes_entire_ink_shadow_sampled_and44_boundary_controls_rejected']
    assert not proof['full_goal_complete']
    for p, digest in proof['scripts'].items():
        assert sha(Path(p).read_bytes()) == digest
    for p, digest in pre['release_hashes'].items():
        assert sha(Path(p).read_bytes()) == digest
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        current = read(Path('translations') / name)
        assert all(current[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
        assert current.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert current.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    ARCHIVE.mkdir(parents=True, exist_ok=True)
    for source in [DOC, *ROOT.glob('*.json'), *ROOT.glob('*.png'), *ROOT.glob('*.py'),
                   *[Path(p) for p in proof['scripts']]]:
        checked_copy(source, ARCHIVE / source.name)
    report = read(proof['reports']['baseline']['path'])
    captures = ARCHIVE / 'Unmodified ordinary captures'
    captures.mkdir(exist_ok=True)
    copied = []
    for shot in report['frames_captured']:
        target = captures / Path(shot['path']).name
        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
        checked_copy(shot['path'], target)
        copied.append({'frame': shot['frame'], 'path': str(target), 'PNG_sha256': shot['PNG_sha256']})
    for name, info in proof['reports'].items():
        checked_copy(info['path'], ARCHIVE / f'capture_report_{name}.json')
    full = read(proof['reports']['committed_full']['path'])
    sources = ARCHIVE / 'Original core source'
    sources.mkdir(exist_ok=True)
    for p, digest in full['read_only_capture_GPU_states'][0]['read_only_committed_geometry']['source_files'].items():
        assert sha(Path(p).read_bytes()) == digest
        checked_copy(p, sources / Path(p).name)
    license_file = Path(next(iter(full['read_only_capture_GPU_states'][0]['read_only_committed_geometry']['source_files']))).parent.parent / 'COPYING'
    if license_file.exists():
        checked_copy(license_file, sources / 'COPYING')
    GUIDE.mkdir(parents=True, exist_ok=True)
    shots = {s['frame']: s for s in report['frames_captured']}
    guide = []
    for frame, label in ((825, 'FULL_TITLE'), (2001, 'HODRAM_NAME')):
        shot = shots[frame]
        target = GUIDE / f'V640_{label}_frame{frame:06d}_UNMODIFIED.png'
        checked_copy(shot['path'], target)
        guide.append({'frame': frame, 'path': str(target), 'PNG_sha256': shot['PNG_sha256']})
    save(GUIDE / 'provenance_v646.json', {'candidate_sha256': proof['candidate_sha256'],
        'source_report': proof['reports']['baseline'], 'captures': guide,
        'ordinary_startup_no_inputs_save_state_exports_or_fixtures': True,
        'guide_candidates_only_no_publication_approval': True})
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
        'unmodified_ordinary_captures': copied, 'guide_candidates': guide,
        'original_full_native_exports_remain_on_E_in_report_paths': True,
        'derived_sheets_and_source_snapshots_distinct_from_captures': True,
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'}, 'full_goal_complete': False})
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': proof['candidate'], 'candidate_sha256': proof['candidate_sha256'],
        'ordinary_no_input_no_save_no_fixture_original_opening': True,
        'all170_M28_native_source_views_in169_groups_indices30_31_indistinguishable': True,
        'all611_complete_upper_RGB_compositions_exact_30031872_pixels_no_exclusions': True,
        'all22_English_planes_complete_ink_shadow_coverage_and44_boundary_controls_pass': True,
        'pinned_source_committed_lists_native_VRAM_and_actual_Y_sort_no_fitted_alpha': True,
        'independent_no_export_complete_two_screen_frames_match': proof['independent_baseline_no_export_complete_two_screen_frame_comparisons'],
        'unsampled_intermediates_other_movies_graphics_and_hardware_not_inferred': True,
        'all18_original_plaques_incomplete_all22_historical_scopes_exact': True,
        'ROM_patch_registry_canonical_and_all_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'guide_candidates': str(GUIDE), 'full_goal_complete': False}
    for name in frozen:
        path = Path('translations') / name
        current = read(path)
        current[KEY] = entry
        current['current_goal_turn_classification'] = 'progress'
        save(path, current)
        assert all(read(path)[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
    heading = '## V646: ordinary opening source views, committed rendering and complete RGB'
    addition = """
Original current V640 startup,no inputs/saves/fixtures,now binds all170 M28 native
views in169 equivalence groups;30/31 cannot be distinguished.611 complete upper
RGB compositions30031872 pixels pass without exclusions,including actual source
palettes/native extents,22 complete English planes and44 boundary controls.
Read-only committed render-list/VRAM export resolves pending-list mismatches;
source Y sorting resolves the remaining3260 mid-fade pixels with original alpha8.
One fixed display lag1 passes;0/2/3 have counterexamples. Independent no-export
two-screen captures match. Source/geometry/VRAM/code snapshots and unmodified PNGs
are on E,with2 ordinary guide candidates. No ROM/patch/registry/pointer change.
All18 plaques remain incomplete and22 historical scopes exact;other card,control,
legacy,movie/material and acceptance gates remain open. See [V646 checkpoint](opening_composition_v646_checkpoint.md).
"""
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    for p, digest in pre['release_hashes'].items():
        assert sha(Path(p).read_bytes()) == digest
    print('V646 archived and audits/progress updated;18 plaques/22 scopes and release pointers retained.')


if __name__ == '__main__':
    main()
