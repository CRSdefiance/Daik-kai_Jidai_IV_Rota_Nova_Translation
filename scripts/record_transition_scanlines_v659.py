"""Archive observed scanlines with unmodified-core controls and retained scope."""

from pathlib import Path

from dk4tool.patch.grand_race_menu_release import sha
from scripts.record_regional_ui_v616 import checked_copy
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/transition_scanlines_v659')
DOC = Path('docs/transition_scanlines_v659_checkpoint.md')
ARCHIVE = Path('E:/Rota Nova translations/Screenshots/Test fixtures/V659 Transition scanlines')
KEY = 'actual_before_RenderLine_scanline_sources_resolve_Lil63_pixel_transition_edge_v659'


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
    assert len(proof['all30_whole_two_screen_observer_vs_unmodified_core_baselines']) == 30
    assert len(proof['ten_complete_independent_same_frame_upper_RGB_source_compositions']) == 10
    assert len(proof['frame2865_source_opacity_changes64_original_threshold5_positions']) == 64
    assert len(proof['frame2865_exact63_RGB_differences_predicted_with_no_delay_fit']) == 63
    assert not proof['full_goal_complete']
    frozen = read('work/analysis/confirm_material_v572/audit_scope_before.json')
    for name, scope in frozen.items():
        data = read(Path('translations') / name)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
        assert data.get('historical_pending_items_retained') == scope['historical_pending_items_retained']
        assert data.get('plaque_style_v247', {}).get('ongoing_plaque_inventory') == scope['ongoing_plaque_inventory']
    for source in (DOC, Path(__file__), *(Path(p) for p in proof['scripts']), *ROOT.glob('*.json'), *ROOT.glob('*.txt')):
        copy(source, ARCHIVE / source.name)
    captured = []
    for label, info in proof['reports'].items():
        for kind in ('observed', 'baseline'):
            report_path = Path(info[kind])
            assert sha(report_path.read_bytes()) == info[kind + '_sha256']
            report = read(report_path)
            tag = label.upper() + ('_DIAGNOSTIC_HOST_OBSERVED' if kind == 'observed' else '_UNMODIFIED_CORE_BASELINE')
            target = ARCHIVE / tag
            copy(report_path, target / 'capture_report.json')
            for shot in report['frames_captured']:
                source = Path(shot['path'])
                copy(source, target / source.name)
                captured.append({'run': tag, 'frame': shot['frame'], 'source': shot['path'],
                    'archive': str(target / source.name), 'PNG_sha256': shot['PNG_sha256'],
                    'host_core_instrumented': kind == 'observed', 'game_ROM_unmodified': True,
                    'guide_or_publication_approved': False})
            if kind == 'observed':
                folder = report_path.parent
                for name in ('scanlines', *(p.name for p in folder.glob('capture_gpu_state_*')),
                             *(p.name for p in folder.glob('capture_native_state_*'))):
                    parent = folder / name
                    for source in parent.rglob('*'):
                        if source.is_file():
                            copy(source, target / name / source.relative_to(parent))
    entry = {'documentation': str(DOC), 'proof': str(pp), 'proof_sha256': sha(pp.read_bytes()),
        'candidate': proof['candidate'], 'candidate_sha256': proof['candidate_sha256'],
        'four_terminal_ordinary_New_Game_cold_boots_no_savestate_or_gameplay_fixtures': True,
        'host_core_observer_explicitly_disclosed_and_all30_full_baseline_pairs_exact': True,
        'all4608_original_render_calls_actual_before_read_source_rows_IO_CPU_bound': True,
        'all1179648_source_bitmap_words_zero_or_exact_original_photo_and_dissolve_pattern': True,
        'ten_complete_same_frame_source_RGB_compositions491520_pixels_without_delay_fit': True,
        'Lil_frame2865_64_source_opacity_changes_predict_exact63_RGB_changes': True,
        'specific_V648_Lil_scanline_edge_resolved_not_all_DMA_cycles_or_physical_hardware': True,
        'all18_original_plaques_incomplete22_historical_scopes_exact': True,
        'other_graphics_and_acceptance_requirements_remain_open': True,
        'ROM_patch_manifest_registry_canonical_and_release_pointers_unchanged': True,
        'archive': str(ARCHIVE), 'no_guide_promotion': True, 'full_goal_complete': False}
    for name in frozen:
        path = Path('translations') / name
        data = read(path)
        data[KEY], data['current_goal_turn_classification'] = entry, 'progress'
        save(path, data)
        assert all(data[k] == v for k, v in pre['all_original_audits_before'][name].items()
                   if k not in (KEY, 'current_goal_turn_classification'))
    heading = '## V659: Lil transition edge resolved at the actual source scanline read'
    addition = ('Four ordinary cold boots compare current V653 and Japanese source with '
        'an explicitly disclosed diagnostic host RenderLine observer and unmodified-core '
        'baselines. All 30 full two-screen pairs match. All 4,608 observed source rows '
        'and 1,179,648 bitmap words match original photo colors/dissolve masks; IO/affine '
        'mapping and source code bind their interpretation. Ten independent same-frame '
        'ROM-source compositions match all 491,520 upper RGB pixels. At Lil2865, original '
        'DMA setup positions differ across row79: 64 threshold5 opacity changes predict '
        'the exact 63 displayed RGB differences, including one coincident source color. '
        'No delay fit, pixel waiver or artwork repair. This resolves the specific V648 '
        'Lil edge, not every DMA cycle, other transition or physical-device behavior. '
        'Evidence/observed versus baseline captures archived separately on E; no guide '
        'promotion. V653/patch/registry/pointers unchanged; all 18 plaques incomplete '
        'and 22 historical scopes exact. Full goal active. See '
        '[V659 checkpoint](transition_scanlines_v659_checkpoint.md).\n')
    for name in ('todo.md', 'translation_progress.md', 'known_issues.md', 'release_build.md'):
        path = Path('docs') / name
        text = path.read_text(encoding='utf-8')
        if heading not in text:
            path.write_text(text.rstrip() + '\n\n' + heading + '\n\n' + addition, encoding='utf-8')
    save(ARCHIVE / 'provenance.json', {'candidate_sha256': proof['candidate_sha256'],
        'captures': captured, 'no_guide_or_publication_promotion': True, 'full_goal_complete': False,
        'scripts': {str(p): sha(p.read_bytes()) for p in (Path(__file__), *(Path(p) for p in proof['scripts']))},
        'files': {str(p.relative_to(ARCHIVE)): sha(p.read_bytes()) for p in ARCHIVE.rglob('*')
                  if p.is_file() and p.name != 'provenance.json'}})
    print(f'V659 source timing evidence and {len(captured)} captures archived; three audits/four progress documents updated; full goal remains active.')


if __name__ == '__main__':
    main()
