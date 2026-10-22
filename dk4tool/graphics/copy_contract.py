"""Check registered embedded graphics copies after every release stage.

This is byte/pixel preservation, not ordinary-consumer or native display proof.
Expected copies come from selected source-locked batches and final loose PXLs.
"""

import hashlib
import json
from collections import defaultdict
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage
from dk4tool.graphics.raw_bgr555_art import FORMAT as RAW_FORMAT

ILNK = 'dk4-ilnk-pxl-sync-v1'
BANKED = 'dk4-obj-banked-pxl-sync-v1'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def reference(candidate, batch, path, transitions):
    name = batch.get('source_image_path', '')
    if not isinstance(name, str) or not name.startswith('/'):
        raise ValueError(f'{path}: final graphics copy needs an absolute reference path')
    expected = batch.get('source_image_sha256')
    applied = []
    for stage in transitions.get(name, []):
        if expected != stage['source_sha256']:
            raise ValueError(f'{path}: final graphics reference transition source differs')
        expected = stage['target_sha256']
        applied.append(stage)
    raw = candidate.read_file(name)
    if digest(raw) != expected:
        raise ValueError(f'{path}: final graphics reference changed after its registered sync')
    image = PxlImage.from_bytes(raw)
    if image.bits_per_pixel != 4:
        raise ValueError(f'{path}: final graphics copy requires a 4bpp PXL')
    return image, {'registered_sync_reference_sha256': batch['source_image_sha256'],
                   'final_reference_sha256': expected, 'registered_later_transitions': applied}


def ilnk_group(candidate, source, file_path, rows, all_batches, transitions):
    original = IlnkContainer.parse(source)
    actual_bytes = candidate.read_file(file_path)
    actual = IlnkContainer.parse(actual_bytes)
    prefix = 8 + (len(original.blocks) + 1) * 4
    if len(source) != len(actual_bytes) or source[:prefix] != actual_bytes[:prefix]:
        raise ValueError(f'{file_path}: final graphics copy allocation/directory changed')
    expected = [bytearray(block) for block in original.blocks]
    ownership, geometries, reports = defaultdict(set), {}, []
    for path, batch in rows:
        image, version = reference(candidate, batch, path, transitions)
        index, header, width, height, x, y = (int(batch.get(k, -1)) for k in (
            'block_index', 'block_header_size', 'target_width', 'target_height', 'target_x', 'target_y'))
        if not 0 <= index < len(original.blocks):
            raise ValueError(f'{path}: final graphics copy block is out of range')
        block = original.blocks[index]
        if digest(block) != batch.get('source_block_sha256'):
            raise ValueError(f'{path}: final graphics copy source block changed')
        if (header < 0 or width <= 0 or width % 2 or height <= 0 or x < 0 or x % 2 or y < 0
                or image.width % 2 or x + image.width > width or y + image.height > height
                or len(block) != header + width * height // 2):
            raise ValueError(f'{path}: invalid final packed graphics copy geometry')
        geometry = (header, width, height)
        if index in geometries and geometries[index] != geometry:
            raise ValueError(f'{path}: inconsistent final graphics copy block geometry')
        geometries[index] = geometry
        owned = set()
        for row in range(image.height):
            for column in range(0, image.width, 2):
                at = header + (y + row) * (width // 2) + (x + column) // 2
                pixel = row * image.width + column
                expected[index][at] = image.indices[pixel] | image.indices[pixel + 1] << 4
                owned.add(at)
        if owned & ownership[index]:
            raise ValueError(f'{path}: overlapping final graphics copy ownership')
        ownership[index].update(owned)
        reports.append({'batch': str(path), 'batch_sha256': digest(path.read_bytes()),
                        'record': batch['id'], 'reference': batch['source_image_path'],
                        'reference_version': version, 'block': index,
                        'source_rectangle': [0, 0, image.width, image.height],
                        'destination': [x, y], 'complete_packed_bytes': len(owned)})
    # The separate final raw-art contract reconstructs this one entire block.
    # No arbitrary unrelated-block exception is granted to other batch formats.
    raw = [(path, b) for path, b in all_batches if b.get('file_path') == file_path
           and b.get('format') == RAW_FORMAT]
    delegated = set()
    if raw:
        if len(raw) != 1 or file_path != '/GRP/SLACKIMG.DK4' or 19 in ownership:
            raise ValueError(f'{file_path}: unsupported overlapping raw/copy ownership')
        delegated.add(19)
    protected = []
    for index, wanted in enumerate(expected):
        if index in delegated:
            continue
        if actual.blocks[index] != bytes(wanted):
            raise ValueError(f'{file_path}: final embedded graphics/source differs in block {index}')
        protected.append({'block': index, 'bytes': len(wanted), 'sha256': digest(wanted),
                          'contains_registered_copy': index in ownership})
    return {'path': file_path, 'format': ILNK, 'copies': reports,
            'source_file_sha256': digest(source), 'final_file_sha256': digest(actual_bytes),
            'source_allocation_directory_headers_and_unowned_blocks_verified': True,
            'verified_complete_blocks': protected, 'blocks_delegated_to_final_raw_art_contract': sorted(delegated)}


def banked_group(candidate, source, file_path, rows, transitions):
    if len(rows) != 1:
        raise ValueError(f'{file_path}: final banked graphics copy requires one registered owner')
    path, batch = rows[0]
    image, version = reference(candidate, batch, path, transitions)
    offset, width, height, count, blank = (int(batch.get(k, -1)) for k in (
        'target_offset', 'bank_width', 'bank_height', 'bank_count', 'blank_index'))
    size = width * height * count // 2
    if (offset < 0 or offset % 32 or width <= 0 or width % 8 or height <= 0 or height % 8
            or count <= 0 or not 0 <= blank <= 15 or offset + size > len(source)
            or size != batch.get('target_region_bytes') or image.width != width * count
            or not 0 < image.height <= height
            or [image.width, image.height] != batch.get('source_image_extent')):
        raise ValueError(f'{path}: invalid final banked graphics copy geometry')
    if digest(source[offset:offset + size]) != batch.get('source_region_sha256'):
        raise ValueError(f'{path}: final banked graphics copy source region changed')
    allowed = set(batch.get('allowed_indices', []))
    if blank not in allowed or not set(image.indices) <= allowed:
        raise ValueError(f'{path}: final banked graphics copy palette roles changed')
    expected = bytearray(source)
    # Inverse destination-address model: resolve each native tile byte back to
    # two pixels of the complete logical atlas, including padded rows.
    for at in range(size):
        bank, within = divmod(at, width * height // 2)
        tile, in_tile = divmod(within, 32)
        ty, tx = divmod(tile, width // 8)
        row, pair = divmod(in_tile, 4)
        x, y = bank * width + tx * 8 + pair * 2, ty * 8 + row
        lo = image.indices[y * image.width + x] if y < image.height else blank
        hi = image.indices[y * image.width + x + 1] if y < image.height else blank
        expected[offset + at] = lo | hi << 4
    actual = candidate.read_file(file_path)
    if actual != bytes(expected):
        raise ValueError(f'{file_path}: final banked graphics/source differs')
    return {'path': file_path, 'format': BANKED, 'batch': str(path),
            'batch_sha256': digest(path.read_bytes()), 'record': batch['record_id'],
            'reference': batch['source_image_path'], 'reference_version': version,
            'source_file_sha256': digest(source), 'final_file_sha256': digest(actual),
            'complete_native_bank_bytes': size, 'source_prefix_suffix_and_padding_verified': True}


def verify_final_graphics_copies(candidate, baseline, batch_paths, profile=None):
    """Validate selected copy families without modifying the candidate."""
    batches = [(Path(p), json.loads(Path(p).read_text(encoding='utf-8'))) for p in batch_paths]
    # These later registered stages intentionally update both a loose image and
    # its embedded copy. Follow their source-to-target locks in builder order;
    # the early sync reference hash is not the final image hash in such profiles.
    transitions = defaultdict(list)
    for key, name in (('name_plaque_gradients', '/_pxl/slackimg12.pxl'),
                      ('marker_price_ownership', '/_pxl/__marker.pxl'),
                      ('marker_header_materials', '/_pxl/__marker.pxl')):
        stage_path = (profile or {}).get(key)
        if stage_path:
            stage_path = Path(stage_path)
            stage = json.loads(stage_path.read_text(encoding='utf-8'))
            if stage.get('file_path', name) != name:
                raise ValueError(f'{stage_path}: registered reference transition path differs')
            transitions[name].append({'stage': key, 'config': str(stage_path),
                                      'config_sha256': digest(stage_path.read_bytes()),
                                      'source_sha256': stage['source_sha256'],
                                      'target_sha256': stage['target_sha256']})
    groups = defaultdict(list)
    for path, batch in batches:
        if batch.get('format') in (ILNK, BANKED):
            file_path = batch.get('file_path', '')
            if not isinstance(file_path, str) or not file_path.startswith('/'):
                raise ValueError(f'{path}: final graphics copy needs an absolute destination path')
            groups[file_path].append((path, batch))
    report = {'applicable': bool(groups), 'families': [],
              'preservation_only_not_native_consumers_visual_acceptance_or_full_goal_completion': True}
    for file_path, rows in sorted(groups.items()):
        source = baseline.read_file(file_path)
        if any(digest(source) != b.get('source_file_sha256') for _, b in rows):
            raise ValueError(f'{file_path}: final graphics copy canonical source changed')
        formats = {b['format'] for _, b in rows}
        if formats == {ILNK}:
            family = ilnk_group(candidate, source, file_path, rows, batches, transitions)
        elif formats == {BANKED}:
            family = banked_group(candidate, source, file_path, rows, transitions)
        else:
            raise ValueError(f'{file_path}: incompatible final graphics copy formats')
        report['families'].append(family)
    return report
