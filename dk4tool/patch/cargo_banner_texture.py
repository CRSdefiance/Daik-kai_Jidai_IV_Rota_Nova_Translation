"""Reconstruct concealed cargo-banner strokes and shadows from local source wood."""
import json
from pathlib import Path

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha


def components(points):
    remaining = set(points)
    groups = []
    while remaining:
        first = min(remaining, key=lambda p: (p[1], p[0]))
        remaining.remove(first)
        group, pending = {first}, [first]
        while pending:
            x, y = pending.pop()
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    neighbour = (x+dx, y+dy)
                    if neighbour in remaining:
                        remaining.remove(neighbour)
                        group.add(neighbour)
                        pending.append(neighbour)
        groups.append(group)
    return groups


def repair(original, current, *, shadow_indices=(2, 3), shadow_radius=0,
           expected_counts=(216, 158), context_bottom=13):
    assert (original.width, original.height) == (256, 16)
    assert current.source[:current.pixels_offset] == original.source[:original.pixels_offset]
    white = {(x, y) for y in range(16) for x in range(256) if original.indices[y*256+x] == 15}
    if shadow_radius:
        shadows = {(x, y) for y in range(1, context_bottom) for x in range(2, 64)
                   if original.indices[y*256+x] in shadow_indices
                   and any(abs(x-a) <= shadow_radius and abs(y-b) <= shadow_radius for a, b in white)}
    else:
        shadows = {(x+1, y+1) for x, y in white if x < 255 and y < 15
                   and original.indices[(y+1)*256+x+1] in shadow_indices}
    hidden = white | shadows
    if expected_counts is not None:
        assert (len(white), len(shadows)) == tuple(expected_counts)
    assert all(original.indices[y*256+x] not in (*shadow_indices, 15)
               for y in range(1, context_bottom) for x in range(128, 248))
    result = PxlImage.from_bytes(original.source)
    groups = []
    for group in components(hidden):
        left, right = min(x for x, _ in group), max(x for x, _ in group)
        # A coherent original patch per connected stroke/shadow component.
        # Choose its offset using only visible source neighbours, never English art.
        context = {(x+dx, y+dy) for x, y in group for dx in range(-2, 3) for dy in (-1, 0, 1)
                   if 2 <= x+dx < 254 and 1 <= y+dy < context_bottom and (x+dx, y+dy) not in hidden}
        assert context
        options = []
        for offset in range(128-left, 248-right):
            if not all(128 <= x+offset < 248 for x, _ in context):
                continue
            score = sum(sum(abs(a-b) for a, b in zip(original.palette[original.indices[y*256+x]][:3],
                                                    original.palette[original.indices[y*256+x+offset]][:3], strict=True))
                        for x, y in context)
            options.append((score, abs(offset-128), offset))
        score, _, offset = min(options)
        for x, y in group:
            assert 128 <= x+offset < 248
            assert original.indices[y*256+x+offset] != 15
            result.indices[y*256+x] = original.indices[y*256+x+offset]
        groups.append({'bounds': [left, min(y for _, y in group), right+1, max(y for _, y in group)+1],
                       'points': len(group), 'donor_offset': offset, 'visible_context_points': len(context),
                       'RGB_context_distance_sum': score})
    english = {n for n, value in enumerate(current.indices) if value == 15}
    for n in english:
        result.indices[n] = 15
    assert {n for n, value in enumerate(result.indices) if value == 15} == english
    material = {n for n in range(4096) if (n % 256, n // 256) not in hidden and n not in english}
    assert all(result.indices[n] == original.indices[n] == current.indices[n] for n in material)
    assert all(result.indices[y*256+x] not in shadow_indices for x, y in shadows if y*256+x not in english)
    return result, {'original_white_points': len(white), 'original_diagonal_shadow_points': len(shadows),
                    'uncovered_original_shadow_points_retained_before': sum(current.indices[y*256+x] == original.indices[y*256+x] for x, y in shadows),
                    'uncovered_original_shadow_points_after': 0, 'all_English_ink_points_exact': len(english),
                    'all_visible_material_points_outside_stroke_shadow_and_English_exact': len(material),
                    'changed_pixels': sum(a != b for a, b in zip(current.indices, result.indices, strict=True)),
                    'source_donor_region': [128, 1, 248, context_bottom], 'component_donors': groups,
                    'concealed_background_is_inferred_not_exact_recovery': True}


def apply_release(candidate, clean, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-cargo-banner-texture-v1':
        raise ValueError('Unknown cargo banner texture format')
    path = config['file_path']
    before, source = candidate.read_file(path), clean.read_file(path)
    if (sha(before), sha(source)) != (config['source_sha256'], config['clean_sha256']):
        raise ValueError('Cargo banner source or inherited pixels differ')
    result, proof = repair(PxlImage.from_bytes(source), PxlImage.from_bytes(before))
    output = result.to_bytes()
    if sha(output) != config['target_sha256'] or len(output) != len(before):
        raise ValueError('Cargo banner reconstructed target or extent differs')
    return output, {**proof, 'file_path': path, 'changed_records': [config['id']],
                    'source_sha256': sha(before), 'target_sha256': sha(output)}


def apply_header_release(candidate, clean, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-header-wood-textures-v1':
        raise ValueError('Unknown wooden header format')
    files, reports = {}, []
    for row in config['records']:
        path = row['file_path']
        before, source = candidate.read_file(path), clean.read_file(path)
        if (sha(before), sha(source)) != (row['source_sha256'], row['clean_sha256']):
            raise ValueError('Wooden header source lock differs')
        result, proof = repair(PxlImage.from_bytes(source), PxlImage.from_bytes(before),
                               shadow_indices=tuple(row['shadow_indices']), shadow_radius=2,
                               expected_counts=row['expected_source_face_shadow_counts'], context_bottom=14)
        output = result.to_bytes()
        if sha(output) != row['target_sha256'] or len(output) != len(before):
            raise ValueError('Wooden header output or extent differs')
        proof['original_proximity_shadow_points'] = proof.pop('original_diagonal_shadow_points')
        files[path] = output
        reports.append({**proof, 'file_path': path, 'changed_records': [row['id']],
                        'source_sha256': sha(before), 'target_sha256': sha(output)})
    return files, reports
