"""Local multiscale image correspondences are leads, not runtime-use proof.

Run with the bundled Python/numpy runtime; project-native decoders run separately.
"""
import hashlib
import json
from pathlib import Path

import numpy as np
from PIL import Image

ROOT = Path('work/analysis/local_art_correspondence_v649')
WINDOWS = (8, 12, 16, 20, 24, 32, 40, 48, 64)
PATCH, STEP = 48, 4
C = np.cos(np.pi * (np.arange(8)[None, :] + .5) * np.arange(8)[:, None] / 8).astype(np.float32)
C[0] *= 1 / np.sqrt(2)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def save(path, data):
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def phash(cells):
    coefficients = (C @ cells @ C.T).reshape(-1, 64)
    median = np.median(coefficients[:, 1:], axis=1)
    bits = coefficients > median[:, None]
    bits[:, 0] = False
    return np.packbits(bits, axis=1).copy().view('<u8').ravel()


def signature(image):
    a = np.asarray(image.resize((8, 8), Image.Resampling.BOX), dtype=np.float32)
    gray = a @ np.array([.299, .587, .114], dtype=np.float32)
    centered = gray.ravel() - gray.mean()
    norm = np.linalg.norm(centered)
    return a, centered / norm if norm > 0 else centered


def queries(metadata):
    result = []
    for row in metadata['queries']:
        image = Image.open(row['PNG']).convert('RGB')
        a = np.asarray(image, dtype=np.float32)
        candidates = []
        xs = sorted({*range(0, image.width - PATCH + 1, 24), image.width - PATCH})
        ys = sorted({*range(0, image.height - PATCH + 1, 24), image.height - PATCH})
        for y in ys:
            for x in xs:
                p = a[y:y + PATCH, x:x + PATCH]
                gray = p @ np.array([.299, .587, .114], dtype=np.float32)
                spread = float(gray.std())
                if spread < 10:
                    continue
                colored = float(np.mean(p.max(axis=2) - p.min(axis=2) >= 20))
                candidates.append((spread * (.25 + colored), x, y))
        selected = []
        for score, x, y in sorted(candidates, reverse=True):
            if any(abs(x - q['box'][0]) < 40 and abs(y - q['box'][1]) < 40 for q in selected):
                continue
            crop = image.crop((x, y, x + PATCH, y + PATCH))
            cells, vec = signature(crop)
            gray = cells @ np.array([.299, .587, .114], dtype=np.float32)
            q = {'frame': row['frame'], 'box': [x, y, x + PATCH, y + PATCH], 'score': score,
                 'hash': int(phash(gray[None, :, :])[0]), 'image': crop, 'cells': cells, 'vector': vec}
            selected.append(q)
            if len(selected) == 6:
                break
        assert selected
        result.extend(selected)
    return result


def build_index(assets):
    hashes, owners, positions = [], [], []
    feature_path = ROOT / 'local_features_float16.bin'
    stream = feature_path.open('wb')
    for owner, asset in enumerate(assets):
        image = asset['proxy']
        gray = np.asarray(image.convert('L'), dtype=np.float32)
        integral = np.pad(gray, ((1, 0), (1, 0))).cumsum(axis=0).cumsum(axis=1)
        count = 0
        for width in WINDOWS:
            if width > min(image.size):
                continue
            xs = sorted({*range(0, image.width - width + 1, STEP), image.width - width})
            ys = sorted({*range(0, image.height - width + 1, STEP), image.height - width})
            x, y = np.meshgrid(xs, ys)
            x, y = x.ravel(), y.ravel()
            edges = np.rint(np.linspace(0, width, 9)).astype(int)
            x0, x1 = x[:, None, None] + edges[:-1][None, None, :], x[:, None, None] + edges[1:][None, None, :]
            y0, y1 = y[:, None, None] + edges[:-1][None, :, None], y[:, None, None] + edges[1:][None, :, None]
            area = np.diff(edges)[:, None] * np.diff(edges)[None, :]
            cells = (integral[y1, x1] - integral[y0, x1] - integral[y1, x0] + integral[y0, x0]) / area
            valid = cells.std(axis=(1, 2)) >= 10
            if not valid.any():
                continue
            h = phash(cells[valid])
            vectors = cells[valid].reshape(-1, 64).astype(np.float32)
            vectors -= vectors.mean(axis=1)[:, None]
            vectors /= np.linalg.norm(vectors, axis=1)[:, None]
            vectors.astype(np.float16).tofile(stream)
            hashes.append(h)
            owners.append(np.full(len(h), owner, dtype=np.int16))
            positions.append(np.column_stack([x[valid], y[valid], np.full(valid.sum(), width)]).astype(np.int16))
            count += len(h)
        asset['indexed_windows'] = count
        if owner % 120 == 0:
            print('index', owner, '/', len(assets), flush=True)
    stream.close()
    hashes = np.concatenate(hashes)
    return hashes, np.concatenate(owners), np.concatenate(positions), np.memmap(
        feature_path, dtype=np.float16, mode='r', shape=(len(hashes), 64))


def correlation_candidates(query_list, features):
    """Retain top512 full normalized cell correlations, with bounded memory."""
    result = []
    for start in range(0, len(query_list), 6):
        selected = query_list[start:start + 6]
        q = np.stack([v['vector'] for v in selected])
        best_values = np.full((len(q), 512), -np.inf, dtype=np.float32)
        best_indices = np.zeros((len(q), 512), dtype=np.int64)
        for chunk in range(0, len(features), 131072):
            scores = q @ np.asarray(features[chunk:chunk + 131072], dtype=np.float32).T
            k = min(512, scores.shape[1])
            ix = np.argpartition(scores, -k, axis=1)[:, -k:]
            vals = np.take_along_axis(scores, ix, axis=1)
            indices = np.concatenate([best_indices, ix + chunk], axis=1)
            values = np.concatenate([best_values, vals], axis=1)
            keep = np.argpartition(values, -512, axis=1)[:, -512:]
            best_values = np.take_along_axis(values, keep, axis=1)
            best_indices = np.take_along_axis(indices, keep, axis=1)
        order = np.argsort(-best_values, axis=1, stable=True)
        result.extend(np.take_along_axis(best_indices, order, axis=1))
        print('full correlation', min(start + 6, len(query_list)), '/', len(query_list), flush=True)
    return result


def refine(query, asset, position):
    x, y, width = (int(v) for v in position)
    image, best = asset['proxy'], None
    for size in range(max(8, width - 2), width + 3):
        for yy in range(max(0, y - 2), min(y + 2, image.height - size) + 1):
            for xx in range(max(0, x - 2), min(x + 2, image.width - size) + 1):
                crop = image.crop((xx, yy, xx + size, yy + size))
                cells, vector = signature(crop)
                ncc = float(vector @ query['vector'])
                error = float(np.mean(np.abs(cells - query['cells'])))
                score = ncc - error / 512
                if best is None or score > best['score']:
                    best = {'score': score, 'gray_NCC': ncc, 'RGB_mean_absolute_error': error,
                            'proxy_box': [xx, yy, xx + size, yy + size]}
    assert best is not None
    return best


def main():
    metadata = json.loads((ROOT / 'decoded_sources.json').read_text(encoding='utf-8'))
    assets = []
    for row in metadata['targets']:
        assert sha(Path(row['PNG']).read_bytes()) == row['PNG_sha256']
        image = Image.open(row['PNG']).convert('RGB')
        proxy = image.copy()
        proxy.thumbnail((128, 128), Image.Resampling.BOX)
        assets.append({**row, 'proxy': proxy, 'synthetic_search_control': False})
    controls = ROOT / 'Synthetic search controls'
    controls.mkdir(exist_ok=True)
    # Known source transformations are independent retrieval controls, not ROM art.
    for i, (frame, scale, quantize) in enumerate([(4, .5, False), (7, .8, True), (8, 1, False),
                                                (16, .8, False), (20, .5, True), (7, 1, True)]):
        original = Image.open(metadata['queries'][frame]['PNG']).convert('RGB')
        size = tuple(round(v * scale) for v in original.size)
        transformed = original.resize(size, Image.Resampling.BOX)
        if quantize:
            transformed = Image.fromarray((np.asarray(transformed) // 16 * 16).astype(np.uint8))
        canvas = Image.new('RGB', (size[0] + 26, size[1] + 22), (97, 97, 97))
        canvas.paste(transformed, (13, 11))
        path = controls / f'CONTROL_{i}_source_frame{frame:02d}.png'
        canvas.save(path)
        proxy = canvas.copy()
        proxy.thumbnail((128, 128), Image.Resampling.BOX)
        assets.append({'path': f'CONTROL_{i}', 'texture': None, 'PNG': str(path), 'PNG_sha256': sha(path.read_bytes()),
            'native_size': list(canvas.size), 'proxy': proxy, 'source_control_frame': frame,
            'scale': scale, 'quantized16_levels': quantize, 'synthetic_search_control': True})
    assets.append({'path': 'NEGATIVE_UNIFORM', 'texture': None, 'PNG': None, 'native_size': [128, 128],
        'proxy': Image.new('RGB', (128, 128), (128, 128, 128)), 'synthetic_search_control': True})
    query_list = queries(metadata)
    hashes, owners, positions, features = build_index(assets)
    assert assets[-1]['indexed_windows'] == 0
    print('indexed', len(hashes), 'local windows; queries', len(query_list), flush=True)
    cosine = correlation_candidates(query_list, features)
    rows, controls_seen = [], set()
    for number, query in enumerate(query_list):
        value = np.uint64(query['hash'])
        distances = np.bitwise_count(hashes ^ value)
        best = np.concatenate([cosine[number], np.argsort(distances, stable=True)[:512]])
        selected, seen = [], {}
        for index in best:
            owner = int(owners[index])
            if owner not in seen and len(seen) >= 16:
                continue
            if seen.get(owner, 0) >= 2:
                continue
            seen[owner] = seen.get(owner, 0) + 1
            selected.append(index)
            if len(selected) >= 32:
                break
        hits = []
        for index in selected:
            owner = int(owners[index])
            candidate = assets[owner]
            match = refine(query, candidate, positions[index])
            hits.append({'asset_index': owner, 'path': candidate['path'], 'texture': candidate['texture'],
                'synthetic_search_control': candidate['synthetic_search_control'],
                'coarse_hash_hamming': int(distances[index]), **match})
            if candidate.get('source_control_frame') == query['frame'] and match['gray_NCC'] > .90:
                controls_seen.add(candidate['path'])
        row = {'frame': query['frame'], 'source_box': query['box'],
               'top_local_leads': sorted(hits, key=lambda v: v['score'], reverse=True)}
        rows.append(row)
        if number % 12 == 0:
            print('queries', number, '/', len(query_list), 'controls', len(controls_seen), flush=True)
            save(ROOT / 'local_search_progress.json', {'through_query': number, 'rows': rows, 'not_final': True})
    serial_assets = [{k: v for k, v in a.items() if k != 'proxy'} for a in assets]
    result = {'original_native_assets': 921, 'assets': serial_assets, 'queries': rows,
        'indexed_local_windows': len(hashes), 'window_sizes_proxy_pixels': WINDOWS, 'grid_step_proxy_pixels': STEP,
        'all6_transformed_source_controls_retrieved': sorted(controls_seen), 'uniform_negative_has_no_windows': True,
        'actual_correspondences_require_visual_and_source_verification': True,
        'partial_crops_other_scales_rotations_alpha_compositions_and_unmodeled_formats_not_excluded': True,
        'no_global_non_use_or_runtime_consumer_claim': True,
        'script_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False}
    save(ROOT / 'local_correspondence_leads.json', result)
    assert len(controls_seen) == 6, controls_seen
    print('V649 local search completed with all6 transformed source controls.', flush=True)


if __name__ == '__main__':
    main()
