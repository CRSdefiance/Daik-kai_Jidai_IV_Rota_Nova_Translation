"""Bind bounded local-art results to exact ROM sources and control witnesses."""
import hashlib
import struct
from collections import Counter
from pathlib import Path

from PIL import Image

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/local_art_correspondence_v649')


def main():
    pre, decoded = read(ROOT / 'preflight.json'), read(ROOT / 'decoded_sources.json')
    search, geometry, review = [read(ROOT / n) for n in
        ['local_correspondence_leads.json', 'geometric_control_and_review.json', 'visual_review_result.json']]
    for p, h in pre['release_hashes'].items():
        assert sha(Path(p).read_bytes()) == h
    assert sha(Path(pre['prior_proof']).read_bytes()) == pre['prior_proof_sha256']
    assert search['script_sha256'] == sha(Path('scripts/search_local_art_v649.py').read_bytes())
    assert geometry['source_results_sha256'] == sha((ROOT / 'local_correspondence_leads.json').read_bytes())
    clean = NdsImage.open('work/clean.nds')
    files = {p: b for _, p, b in clean.iter_files()}
    expected = set()
    for path, data in files.items():
        if path.lower().endswith('.pxl'):
            expected.add((path, None))
        elif path.lower().endswith('.fls'):
            expected.update((path, i) for i in range(FlsArchive(data).count))
    assert len(expected) == 921
    assert {(a['path'], a['texture']) for a in decoded['targets']} == expected
    movies = {}
    for asset in decoded['targets']:
        data = files[asset['path']]
        assert sha(data) == asset['source_file_sha256']
        assert sha(Path(asset['PNG']).read_bytes()) == asset['PNG_sha256']
        if asset['texture'] is None:
            flags, width, height = struct.unpack_from('<3I', data)
            depth = flags & 255
            assert depth in (4, 8, 16)
            extent = [width * (4 if depth == 4 else 2 if depth == 8 else 1), height]
        else:
            if asset['path'] not in movies:
                movies[asset['path']] = FlsArchive(data)
            row = movies[asset['path']].records[asset['texture']]
            extent = [row[0] >> 16, row[1] & 65535]
        assert asset['native_size'] == extent == list(Image.open(asset['PNG']).size)
    raw = IlnkContainer.parse(files['/GRP/SLACKIMG.DK4']).blocks[19]
    for q in decoded['queries']:
        assert sha(raw[q['frame'] * 153600:(q['frame'] + 1) * 153600]) == q['source_bytes_sha256']
        assert sha(Path(q['PNG']).read_bytes()) == q['PNG_sha256']
        assert Image.open(q['PNG']).size == (320, 240)
    assert Counter(q['frame'] for q in search['queries']) == {i: 6 for i in range(21)}
    for q in search['queries']:
        x, y, r, b = q['source_box']
        assert 0 <= x < r <= 320 and 0 <= y < b <= 240 and r - x == b - y == 48
    assert set(geometry['control_geometry_witnesses']) == {f'CONTROL_{i}' for i in range(6)}
    assert all(len(v) >= 2 and all(w['maximum_coordinate_error_proxy_pixels'] <= 3 and w['gray_NCC'] > .90
        for w in v) for v in geometry['control_geometry_witnesses'].values())
    assert not geometry['high_score_two_patch_geometric_leads']
    assert review['all3_labeled_pages_and21_best_actual_leads_inspected']
    assert len(review['per_frame_disposition']) == 21
    assert review['partial_shared_character_art_and_unsearched_transforms_not_excluded']
    for item in geometry['review_pages']:
        assert sha(Path(item['path']).read_bytes()) == item['sha256']
    assert review['page_hashes'] == geometry['review_pages']
    feature = ROOT / 'local_features_float16.bin'
    assert feature.stat().st_size == search['indexed_local_windows'] * 128
    with feature.open('rb') as stream:
        feature_sha = hashlib.file_digest(stream, 'sha256').hexdigest()
    actual = search['assets'][:921]
    assert len([a for a in actual if not a['indexed_windows']]) == 17
    assert search['assets'][-1]['path'] == 'NEGATIVE_UNIFORM' and search['assets'][-1]['indexed_windows'] == 0
    result = {'candidate': pre['candidate'], 'candidate_sha256': pre['candidate_sha256'],
        'previous_goal_turn_classification': 'progress', 'current_goal_turn_classification': 'progress',
        'all921_original_loose_native_views_source_hashes_and_dimensions_checked': True,
        'original_source_counts': decoded['counts'], 'raw_source_frames': 21, 'source_patch_queries': 126,
        'proxy_indexed_local_windows_including_controls': search['indexed_local_windows'],
        'original_asset_indexed_windows': sum(a['indexed_windows'] for a in actual),
        '904_original_views_have_eligible_local_windows_17_explicitly_without': True,
        'six_transformed_controls_retrieved_at_correct_known_warp_locations_with2plus_source_patches':
            {k: len(v) for k, v in geometry['control_geometry_witnesses'].items()},
        'uniform_negative_has_no_windows': True,
        'initial_hash_only_missed_control4_failure_and_source_preserved': True,
        'full_patch_correlation_added_without_lowering_control_NCC_gate': True,
        'zero_two_patch_actual_geometric_leads_under_declared_thresholds': True,
        'three_sheets_all21_best_actual_leads_visually_reviewed_no_new_complete_picture_or_caption_copy_established': True,
        'not_global_copy_exclusion_or_legacy_runtime_non_use_proof': True,
        'native_loading_crop_composition_or_new_gameplay_screenshot_credit': False,
        'feature_cache': {'path': str(feature), 'bytes': feature.stat().st_size, 'sha256': feature_sha},
        'numerical_runtime': read(ROOT / 'numerical_runtime.json'),
        'proof_inputs': {p.name: sha(p.read_bytes()) for p in ROOT.glob('*.json') if p.name != 'correspondence_proof.json'},
        'scripts': {str(p): sha(p.read_bytes()) for p in Path('scripts').glob('*v649.py')},
        'all18_plaques_incomplete_all22_historical_requirements_exact': True,
        'plaque_material_review_requested_no_user_answer_or_approval_inferred': True,
        'ROM_patch_registry_canonical_and_release_pointers_unchanged': True,
        'full_goal_complete': False}
    save(ROOT / 'correspondence_proof.json', result)
    print('V649 verified:921 source views,126 local queries,6 geometry-checked controls;no new confirmed caption-copy or runtime-consumer claim.')


if __name__ == '__main__':
    main()
