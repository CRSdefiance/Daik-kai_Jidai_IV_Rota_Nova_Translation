"""Independent control geometry and explicitly provisional local-art leads."""
import math
from collections import defaultdict
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/local_art_correspondence_v649')


def proxy(asset):
    image = Image.open(asset['PNG']).convert('RGB')
    image.thumbnail((128, 128), Image.Resampling.BOX)
    return image


def transform(q, hit):
    x, y, r, _b = hit['proxy_box']
    sx, sy, _, _ = q['source_box']
    scale = (r - x) / 48
    return scale, x - scale * sx, y - scale * sy


def main():
    result_path = ROOT / 'local_correspondence_leads.json'
    data, source = read(result_path), read(ROOT / 'decoded_sources.json')
    assert data['script_sha256'] == sha(Path('scripts/search_local_art_v649.py').read_bytes())
    assert data['original_native_assets'] == len(source['targets']) == 921
    assert len(data['queries']) == 126 and len(data['assets']) == 928
    for asset in data['assets']:
        if asset['PNG']:
            assert sha(Path(asset['PNG']).read_bytes()) == asset['PNG_sha256']
    controls, actual = defaultdict(dict), defaultdict(list)
    for qid, q in enumerate(data['queries']):
        for hit in q['top_local_leads']:
            asset = data['assets'][hit['asset_index']]
            if asset.get('source_control_frame') == q['frame'] and hit['gray_NCC'] > .90:
                image = proxy(asset)
                fx, fy = image.width / asset['native_size'][0], image.height / asset['native_size'][1]
                size = [round(320 * asset['scale']), round(240 * asset['scale'])]
                x, y, r, b = q['source_box']
                expected = [(13 + x * size[0] / 320) * fx, (11 + y * size[1] / 240) * fy,
                            (13 + r * size[0] / 320) * fx, (11 + b * size[1] / 240) * fy]
                error = max(abs(a - b) for a, b in zip(expected, hit['proxy_box'], strict=True))
                if error <= 3:
                    controls[asset['path']][qid] = {'query': qid, 'source_box': q['source_box'],
                        'expected_known_warp_box': expected, 'retrieved_box': hit['proxy_box'],
                        'maximum_coordinate_error_proxy_pixels': error, 'gray_NCC': hit['gray_NCC']}
            elif not asset['synthetic_search_control']:
                actual[q['frame']].append({'query': qid, 'source_box': q['source_box'], **hit})
    assert set(controls) == {f'CONTROL_{i}' for i in range(6)}
    assert all(len(c) >= 2 for c in controls.values()), {k: len(v) for k, v in controls.items()}
    assert data['assets'][-1]['path'] == 'NEGATIVE_UNIFORM' and data['assets'][-1]['indexed_windows'] == 0
    clusters = []
    for frame, hits in actual.items():
        by_asset = defaultdict(list)
        for hit in hits:
            if hit['gray_NCC'] >= .93 and hit['RGB_mean_absolute_error'] <= 24:
                by_asset[hit['asset_index']].append(hit)
        for owner, matches in by_asset.items():
            for anchor in matches:
                at = transform(anchor, anchor)
                coherent = {}
                for match in matches:
                    mt = transform(match, match)
                    if abs(math.log(mt[0] / at[0])) <= .15 and max(abs(mt[1] - at[1]), abs(mt[2] - at[2])) <= 4:
                        coherent[tuple(match['source_box'])] = match
                if len(coherent) >= 2:
                    clusters.append({'frame': frame, 'asset_index': owner,
                        'path': data['assets'][owner]['path'], 'texture': data['assets'][owner]['texture'],
                        'geometric_lead_only_not_identity_or_runtime_use': True, 'matches': list(coherent.values())})
                    break
    pages = []
    for start in range(0, 21, 7):
        sheet = Image.new('RGB', (1040, 7 * 280), (30, 37, 43))
        draw = ImageDraw.Draw(sheet)
        for row, frame in enumerate(range(start, min(start + 7, 21))):
            best = max(actual[frame], key=lambda h: h['score'])
            original = Image.open(source['queries'][frame]['PNG']).convert('RGB')
            target_asset = data['assets'][best['asset_index']]
            target = Image.open(target_asset['PNG']).convert('RGB')
            target.thumbnail((320, 240), Image.Resampling.NEAREST)
            yy = row * 280
            draw.text((8, yy + 4), f'Raw frame {frame:02d} / SOURCE', fill='white')
            draw.text((344, yy + 4), f'LEAD ONLY {best["path"]} / {best["texture"]}', fill='white')
            sheet.paste(original, (8, yy + 25))
            sheet.paste(target, (344, yy + 25))
            qimage = original.crop(tuple(best['source_box'])).resize((128, 128), Image.Resampling.NEAREST)
            timage = proxy(target_asset).crop(tuple(best['proxy_box'])).resize((128, 128), Image.Resampling.NEAREST)
            sheet.paste(qimage, (682, yy + 25))
            sheet.paste(timage, (822, yy + 25))
            draw.text((682, yy + 164), f'Gray NCC {best["gray_NCC"]:.3f}', fill='white')
            draw.text((682, yy + 181), f'RGB error {best["RGB_mean_absolute_error"]:.1f}', fill='white')
            draw.text((682, yy + 204), 'High scores can match simple edges.', fill='white')
            draw.text((682, yy + 221), 'No copy/consumer claim from score.', fill='white')
        path = ROOT / f'LOCAL_LEADS_ONLY_frames{start:02d}_{min(start+6,20):02d}.png'
        sheet.save(path)
        pages.append({'path': str(path), 'sha256': sha(path.read_bytes())})
    review = {'source_results': str(result_path), 'source_results_sha256': sha(result_path.read_bytes()),
        'all6_controls_have_at_least2_independent_source_boxes_at_correct_known_warp_positions': True,
        'control_geometry_witnesses': {k: list(v.values()) for k, v in controls.items()},
        'uniform_negative_has_no_eligible_windows': True,
        'original921_views_decoded_source_views_with_zero_eligible_windows': [a for a in data['assets'][:921] if not a['indexed_windows']],
        'high_score_two_patch_geometric_leads': clusters,
        'best_actual_leads_by_frame': {k: max(v, key=lambda h: h['score']) for k, v in actual.items()},
        'review_pages': pages, 'visual_review_pending': True,
        'source_crops_scales_features_are_a_bounded_lead_search_not_global_copy_exclusion': True,
        'full_goal_complete': False}
    save(ROOT / 'geometric_control_and_review.json', review)
    print('V649 six controls independently located at known warp positions;two-patch actual geometric leads', len(clusters),
          ';zero-window native views', len(review['original921_views_decoded_source_views_with_zero_eligible_windows']))


if __name__ == '__main__':
    main()
