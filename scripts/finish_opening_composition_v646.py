"""Finalize full opening evidence, export invariance and binary source anchors."""

import struct
from collections import Counter
from pathlib import Path
from types import SimpleNamespace

from PIL import Image

from dk4tool.patch.grand_race_menu_release import sha
from scripts import inspect_committed_gpu_v646 as inspector
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/opening_composition_v646')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def main():
    result, pre = read(ROOT / 'full_composition_results.json'), read(ROOT / 'preflight.json')
    assert not result['failures'] and len(result['cases']) == 611
    assert result['source_candidates_seen']['/FLS/M28.fls'] == list(range(170))
    assert len(result['source_equivalence_groups']['/FLS/M28.fls']) == 169
    assert [g for g in result['source_equivalence_groups']['/FLS/M28.fls'] if len(g) > 1] == [[30, 31]]
    assert not result['unproved_English_boundary_controls']
    assert len(result['opaque_English_boundary_controls']) == 22
    assert all(len(v['both_boundary_deletions_rejected']) == 2
               and all(c['whole_RGB_pixels_changed'] > 0 for c in v['both_boundary_deletions_rejected'])
               for v in result['opaque_English_boundary_controls'].values())
    assert set(result['fixed_lag1_alternatives_rejected']) == {'0', '2', '3'}
    assert sha(Path('scripts/verify_opening_composition_v646.py').read_bytes()) == result['script_sha256']
    for p, digest in pre['release_hashes'].items():
        assert sha(Path(p).read_bytes()) == digest
    paths = {name: CAP / f'opening_composition_v646_{name}/capture_report.json'
             for name in ('actual', 'detail', 'committed_v2', 'committed_full', 'baseline')}
    reports = {name: read(p) for name, p in paths.items()}
    for name, report in reports.items():
        assert report['ROM_sha256'] == pre['candidate_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not report['scripted_input_schedule'] and not report.get('battery_save_preloaded')
        assert not any(k.startswith('synthetic_') for k in report)
    baseline, full = reports['baseline'], reports['committed_full']
    assert baseline['frames'] == full['frames'] == 7400
    assert not baseline.get('read_only_capture_GPU_states')
    old = {s['frame']: s for s in baseline['frames_captured']}
    compared = set()
    for shot in full['frames_captured']:
        a, b = Path(shot['path']), Path(old[shot['frame']]['path'])
        assert sha(a.read_bytes()) == shot['PNG_sha256'] and sha(b.read_bytes()) == old[shot['frame']]['PNG_sha256']
        ai, bi = Image.open(a).convert('RGB'), Image.open(b).convert('RGB')
        assert ai.size == bi.size == (256, 384) and ai.tobytes() == bi.tobytes()
        compared.add(shot['frame'])
    assert len(compared) == len(old)
    # Independently bind every recorded source anchor back to the exact DLL.
    image = inspector.ImageReader(SimpleNamespace(_handle=0))  # File parsing only; no native read.
    anchors = full['read_only_capture_GPU_states'][0]['read_only_committed_geometry']['source_SFORMAT_anchors']
    delta = anchors['GSET']['runtime_address'] - anchors['GSET']['source_VA']
    for key, entry in anchors.items():
        offset = entry['record_file_offset']
        desc, size, count, value = struct.unpack_from('<QIIQ', image.raw, offset)
        assert (size, count, value) == (entry['size'], entry['count'], entry['source_VA'])
        assert value + delta == entry['runtime_address']
        assert desc + delta == entry['runtime_description_address']
        assert image.source_va(offset) + delta == entry['runtime_record_address']
        pos = next(start + desc - image.link_base - rva for rva, extent, start, fsize, flags in image.sections
                   if rva <= desc - image.link_base < rva + fsize)
        assert image.raw[pos:pos + len(key) + 1] == key.encode() + b'\0'
    assert all(s['read_only_committed_geometry']['source_SFORMAT_anchors'] == anchors
               for s in full['read_only_capture_GPU_states'])
    rejected = []
    for name, args in (('null/low source pointer', (0, 1, 0, 1)),
                       ('array overrun', (0x10001, 1, 0x10000, 1)),
                       ('oversized source array', (0x10000, 1, 0x10000, 5120001))):
        try:
            inspector.allocated_read(*args)
        except ValueError:
            rejected.append(name)
        else:
            raise AssertionError(name)
    original_core = inspector.CORE
    inspector.CORE = SimpleNamespace(read_bytes=lambda: b'incorrect pinned core')
    try:
        try:
            inspector.ImageReader(SimpleNamespace(_handle=0))
        except AssertionError:
            rejected.append('wrong core SHA before native address use')
        else:
            raise AssertionError('Wrong core admitted')
    finally:
        inspector.CORE = original_core
    order = read(ROOT / 'source_sort_resolution.json')
    assert order['RGB_differences'] == 0 and order['old_submission_order_differences'] == 3260
    assert order['order']['original_polygon_order'] == [0, 2, 3, 4, 1]
    sources = Counter(c['source_movie'] for c in result['cases'])
    review = read(ROOT / 'visual_review.json')
    assert review['twelve_anchors_visually_reviewed'] and review['full_native_825_and2001_reviewed']
    proof = {'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'previous_goal_turn_classification': 'progress',
        'source_movies': dict(sources), 'M28_all170_native_source_views_represented_in169_equivalence_groups': True,
        'M28_indices30_31_pixel_equivalence_not_two_distinguished_runtime_IDs': True,
        'complete_original_source_palettes_and_all_native_view_cells_match_actual_texture_VRAM': True,
        'all611_complete_upper_RGB_compositions_exact_without_exclusions': True,
        'complete_upper_RGB_pixel_comparisons': 611 * 49152,
        'fixed_committed_geometry_to_display_lag': 1,
        'wrong_lags0_2_3_have_explicit_counterexamples': result['fixed_lag1_alternatives_rejected'],
        'all22_English_planes_entire_ink_shadow_sampled_and44_boundary_controls_rejected': True,
        'English_boundary_controls': result['opaque_English_boundary_controls'],
        'source_render_sort_resolves_midfade_no_fitted_alpha_or_pixel_waiver': order,
        'independent_baseline_no_export_complete_two_screen_frame_comparisons': len(compared),
        'baseline_complete_two_screen_pixels_exact': len(compared) * 98304,
        'baseline_and_export_capture_records': [len(baseline['frames_captured']), len(full['frames_captured'])],
        'read_only_export_does_not_change_any_compared_complete_frame': True,
        'all_binary_SFORMAT_anchor_records_and_relocated_addresses_match_pinned_DLL': len(anchors),
        'unsafe_array_bounds_and_wrong_core_rejected_before_copy': rejected,
        'native_geometry_VRAM_source_fields_hash_checked_no_framebuffer_expected_source': True,
        'actual_exporter_source': str(ROOT / 'exporter_committed_full_source.py'),
        'actual_exporter_source_sha256': result['actual_exporter_source_sha256'],
        'maintained_exporter_adds_redundant_descriptor_assertion_verified_by_static_anchor_check': True,
        'reports': {k: {'path': str(p), 'sha256': sha(p.read_bytes())} for k, p in paths.items()},
        'results': str(ROOT / 'full_composition_results.json'),
        'results_sha256': sha((ROOT / 'full_composition_results.json').read_bytes()),
        'scripts': {str(p): sha(p.read_bytes()) for p in Path('scripts').glob('*v646.py')},
        'all18_plaques_remain_incomplete_all22_historical_scopes_retained': True,
        'ROM_patch_registry_release_pointers_and_canonical_unchanged': True,
        'unsampled_intermediate_states_other_movies_other_graphics_and_hardware_not_inferred': True,
        'full_goal_complete': False}
    save(ROOT / 'opening_composition_proof.json', proof)
    print('V646 finalized:', 611, 'complete source compositions;', len(compared), 'whole two-screen baseline matches;170 M28 views;22 English planes.')


if __name__ == '__main__':
    main()
