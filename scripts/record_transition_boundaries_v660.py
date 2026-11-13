"""Archive all18 source boundary states and preserve the complete open goal."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/transition_boundaries_v660')
DOC = Path('docs/transition_boundaries_v660_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V660 Transition boundaries')
KEY = 'all18_original_movie_scene_boundary_states36_same_frame_source_RGB_compositions_v660'


def copy(source, destination):
    destination.parent.mkdir(parents=True, exist_ok=True)
    checked_copy(source, destination)


def main():
    pp = ROOT / 'proof.json'
    proof, pre = read(pp), read(ROOT / 'preflight.json')
    for path, digest in proof['scripts'].items():
        assert sha(Path(path).read_bytes()) == digest
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    assert len(proof['all18_original_boundary_state_frames_exact_source_RGB_in_current_and_clean']) == 36
    assert len(proof['all72_whole_two_screen_observer_vs_unmodified_core_pairs']) == 72
    assert proof['complete_independent_upper_RGB_comparisons'] == 1769472
    stripe = proof['pre_boundary_Hodram3117_six_of_eight_stripes_match_complete_original_native_control']
    assert sha(Path(stripe['path']).read_bytes()) == stripe['sha256']
    assert not proof['full_goal_complete']
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        data = read(Path('translations') / name)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    for source in (DOC, Path(__file__), *(Path(p) for p in proof['scripts']),
                   *ROOT.glob('*.json'), *ROOT.glob('*.txt'), *ROOT.glob('*.bin')):
        copy(source, ARCHIVE / source.name)
    captures = []
    for route, details in proof['routes'].items():
        for label, info in details['reports'].items():
            for kind in ('observed', 'baseline'):
                report_path = Path(info[kind])
                assert sha(report_path.read_bytes()) == info[kind + '_sha256']
                report = read(report_path)
                tag = route.upper() + '_' + label.upper() + (
                    '_DIAGNOSTIC_HOST_OBSERVED' if kind == 'observed' else '_UNMODIFIED_CORE_BASELINE')
                destination = ARCHIVE / tag
                copy(report_path, destination / 'capture_report.json')
                for shot in report['frames_captured']:
                    source = Path(shot['path'])
                    copy(source, destination / source.name)
                    captures.append({'run': tag, 'frame': shot['frame'], 'source': shot['path'],
                        'archive': str(destination / source.name), 'PNG_sha256': shot['PNG_sha256'],
                        'host_core_instrumented': kind == 'observed', 'game_ROM_unmodified': True,
                        'guide_or_publication_approved': False})
                if kind == 'observed':
                    folder = report_path.parent
                    for name in ('scanlines', *(p.name for p in folder.glob('capture_gpu_state_*')),
                                 *(p.name for p in folder.glob('capture_native_state_*'))):
                        for source in (folder / name).rglob('*'):
                            if source.is_file():
                                copy(source, destination / name / source.relative_to(folder / name))
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': proof['candidate'], 'candidate_sha256': proof['candidate_sha256'],
        'twelve_terminal_ordinary_New_Game_runs_no_savestate_or_gameplay_fixtures': True,
        'all72_whole_two_screen_observed_vs_unmodified_core_baselines_exact': True,
        'all10368_actual_source_scanlines2654208_original_photo_or_transparent_words': True,
        'all18_retained_boundary_states36_whole_upper_source_RGB_compositions1769472_pixels': True,
        'all_three_specific_V647_V648_boundary_comparisons_resolved_without_delay_fit': True,
        'pre_boundary_Hodram_stripes_bound_to_complete_original_native_progress_control': True,
        'no_every_movie_DMA_cycle_physical_hardware_or_entire_campaign_claim': True,
        'all18_original_plaque_entries_incomplete22_historical_scopes_exact': True,
        'other_actual_consumers_material_equipment_gameplay_and_acceptance_remain_open': True,
        'ROM_patch_manifest_registry_canonical_and_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'no_guide_promotion': True, 'full_goal_complete': False}
    for name in frozen:
        path = Path('translations') / name
        data = read(path)
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(path, data)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
    heading = '## V660: all18 retained movie-to-scene states receive complete source RGB verification'
    addition = ('Twelve ordinary current/clean New Game runs finish normally. Reused bounded '
        'host observation is disclosed/restored; all72 full unmodified-core baseline pairs '
        'match. All10,368 source scanlines/2,654,208 source words and original IO/affine '
        'interpretation pass. All18 V648 state frames now have36 complete same-frame '
        'source RGB compositions across current and clean:1,769,472 exact pixels. '
        'Original photo palette/indices, FLS bindings/geometry and captain getters bind '
        'every state. Initial Hodram3117 full-opacity assumption is rejected and replaced '
        'by a complete original native six-of-eight stripe control; no frame is waived. '
        'The specific Rafael/Lil/Hodram boundary comparisons are resolved without delay '
        'fitting; other movies/frames, hardware and broader graphics gates remain open. '
        'All18 plaques incomplete and22 historical scopes exact. Evidence/captures on E; '
        'no guide approval or ROM/patch/registry/pointer change. Full goal active. See '
        '[V660 checkpoint](transition_boundaries_v660_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
        'captures': captures, 'no_guide_or_publication_promotion': True, 'full_goal_complete': False,
        'scripts': {str(p): sha(p.read_bytes()) for p in (Path(__file__), *(Path(p) for p in proof['scripts']))},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'}})
    print(f'V660 proof and {len(captures)} capture records archived; three audits/four progress documents updated; full graphics goal active.')


if __name__ == '__main__':
    main()
