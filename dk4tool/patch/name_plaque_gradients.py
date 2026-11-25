"""Restore source-specific name gradients and keep the embedded sprite synchronized."""
import json
import struct
from collections import Counter
from pathlib import Path

from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha


def apply_release(candidate, clean, config_path):
    config = json.loads(Path(config_path).read_text(encoding='utf-8'))
    if config['format'] != 'dk4-name-plaque-gradients-v1':
        raise ValueError('Unknown name gradient format')
    path, archive_path = config['file_path'], config['archive_path']
    old_data, clean_data = candidate.read_file(path), clean.read_file(path)
    archive_data = candidate.read_file(archive_path)
    if (sha(old_data), sha(clean_data), sha(archive_data)) != (
            config['source_sha256'], config['clean_sha256'], config['source_archive_sha256']):
        raise ValueError('Original or inherited name plaque storage differs')
    old, original = PxlImage.from_bytes(old_data), PxlImage.from_bytes(clean_data)
    result = PxlImage.from_bytes(clean_data)
    if old.palette != original.palette or (old.width, old.height) != (44, 60):
        raise ValueError('Name plaque material palette or dimensions differ')
    for row in config['records']:
        _, top, _, _ = row['box']
        for expected in row['row_gradients']:
            y = expected['row']
            if not top + 1 <= y < top + 10:
                raise ValueError('Gradient row escapes its source face')
            counts = Counter(original.indices[y*44+x] for x in range(4, 40)
                             if original.indices[y*44+x] != 15)
            ranked = counts.most_common()
            if len(ranked) > 1 and ranked[0][1] <= ranked[1][1]:
                raise ValueError('Original gradient is ambiguous')
            if ranked[0] != (expected['index'], expected['source_votes']):
                raise ValueError('Original gradient row differs')
            for x in range(4, 40):
                if original.indices[y*44+x] == 15:
                    result.indices[y*44+x] = expected['index']
    for n, index in enumerate(old.indices):
        if index == 15:
            result.indices[n] = 15
    if {n for n, v in enumerate(result.indices) if v == 15} != {n for n, v in enumerate(old.indices) if v == 15}:
        raise ValueError('Name plaque white font/chrome mask differs')
    output = result.to_bytes()
    if output[:result.pixels_offset] != old_data[:old.pixels_offset] or sha(output) != config['target_sha256']:
        raise ValueError('Name gradient target or metadata differs')
    archive = IlnkContainer.parse(archive_data)
    block = archive.blocks[12]
    clean_block = IlnkContainer.parse(clean.read_file(archive_path)).blocks[12]
    loose_colours = struct.unpack('<16H', old_data[20:52])
    embedded_colours = struct.unpack('<16H', block[20:52])
    if (block[64:] != old_data[old.pixels_offset:] or block[:64] != clean_block[:64] or
            any((a & 0x7FFF) != (b & 0x7FFF) for a, b in zip(loose_colours, embedded_colours, strict=True))):
        raise ValueError('Name embedded sprite is not synchronized with inherited loose sprite')
    archive.blocks[12] = block[:64] + output[result.pixels_offset:]
    archive_output = archive.to_bytes()
    if sha(archive_output) != config['target_archive_sha256'] or len(archive_output) != len(archive_data):
        raise ValueError('Name embedded synchronization target or extent differs')
    return {path: output, archive_path: archive_output}, [
        {'file_path': path, 'changed_records': [r['id'] + '_OWN_GRADIENT' for r in config['records']],
         'source_sha256': sha(old_data), 'target_sha256': sha(output),
         'all5_original_materials_and_full_English_masks_retained': True},
        {'file_path': archive_path, 'changed_records': ['DK4_NAME_PLAQUE_GRADIENTS_EMBEDDED_BLOCK12'],
         'source_sha256': sha(archive_data), 'target_sha256': sha(archive_output),
         'only_block12_pixels_changed_headers_palette_offsets_and_other_blocks_exact': True}]
