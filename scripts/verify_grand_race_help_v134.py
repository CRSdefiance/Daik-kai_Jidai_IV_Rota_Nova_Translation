"""Verify the saved combined V134 help layer and preservation of all V133 files."""

import json
import struct
from itertools import pairwise
from pathlib import Path

from dk4tool.dialogue.grand_race_help import model_native_ascii
from dk4tool.patch.grand_race_help_release import sha, validate_release_batch
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import common_message_entries
from scripts.register_grand_race_help_v134 import BATCH, components, patched_arm9


def main():
    path = Path('out/all_routes_combined_v134_candidate.nds')
    previous = components(NdsImage.open('out/all_routes_combined_v133_candidate.nds'))
    saved = components(NdsImage.open(path))
    batch = json.loads(Path(BATCH).read_text(encoding='utf-8'))
    baseline = NdsImage.open('out/raphael_natural_v2_accepted_base.nds').read_file('/__arm9__.bin')
    validate_release_batch(batch, baseline)
    if previous.keys() != saved.keys():
        raise ValueError('ROM file/component identities changed')
    for name, data in previous.items():
        expected = patched_arm9(data, batch) if name == '/__arm9__.bin' else data
        if saved[name] != expected:
            raise ValueError(f'Unexpected saved component change: {name}')
    old_arm9, arm9 = previous['/__arm9__.bin'], saved['/__arm9__.bin']
    allowed = set()
    for row in batch['records']:
        offset, size = row['offset'], len(bytes.fromhex(row['source_hex']))
        allowed.update(range(offset, offset + size))
    if len(old_arm9) != len(arm9) or any(a != b and index not in allowed for index, (a, b) in enumerate(zip(old_arm9, arm9, strict=True))):
        raise ValueError('ARM9 changed outside declared data spans')
    manuscript_path = Path(batch['native_text_repack']['manuscript'])
    manuscript = json.loads(manuscript_path.read_text(encoding='utf-8'))
    pages = []
    ranges = []
    for row in manuscript['records']:
        descriptor = row['descriptor_offset']
        title_ptr, body_ptr = struct.unpack_from('<II', arm9, descriptor)
        title_offset, body_offset = title_ptr - 0x02000000, body_ptr - 0x02000000
        title = arm9[title_offset:].split(b'\0', 1)[0].decode('ascii')
        body = arm9[body_offset:].split(b'\0', 1)[0]
        if title != row['draft_english_title'] or title_offset != row['title_offset']:
            raise ValueError('Saved heading/title pointer differs')
        if not 0x137B90 <= body_offset < body_offset + len(body) + 1 <= 0x138294:
            raise ValueError('Saved body extends outside original shared region')
        ranges.append((body_offset, body_offset + len(body) + 1))
        lines = [line.rstrip(b' ').decode('ascii') for line in body.split(b'\n ')]
        if ' '.join(lines) != row['english'] or len(lines) > 8:
            raise ValueError('Saved body drops/changes complete manuscript or exceeds page')
        draws = model_native_ascii(body)
        for index, line in enumerate(lines):
            expected = [(char, x * 6, 12 + index * 12) for x, char in enumerate(line) if char != ' ']
            actual = [draw for draw in draws if draw[2] == 12 + index * 12 and draw[0] != ' ']
            if actual != expected:
                raise ValueError('Saved body loses or misplaces a visible character')
        pages.append({'id': row['id'], 'heading': title, 'body_offset': body_offset,
                      'line_count': len(lines), 'complete_prose_and_pair_positions_exact': True})
    sorted_ranges = sorted(ranges)
    if any(a[1] != b[0] for a, b in pairwise(sorted_ranges)):
        raise ValueError('Saved bodies overlap or leave unexpected padding')
    if sorted_ranges[0][0] != 0x137B90 or sorted_ranges[-1][1] != 0x138292 or arm9[0x138292:0x138294] != b'\0\0':
        raise ValueError('Saved formatted region accounting differs')
    common_before = common_message_entries(previous['/COMMON/MESFILE.DK4'], old_arm9, clean=False)
    common_after = common_message_entries(saved['/COMMON/MESFILE.DK4'], arm9, clean=False)
    if common_before != common_after or len(common_after) != 3668:
        raise ValueError('An existing native COMMON selection changed')
    manifest = json.loads(path.with_suffix('.manifest.json').read_text(encoding='utf-8'))
    for field, artifact in [('candidate_sha256', manifest['candidate_rom']),
                            ('base_sha256', manifest['base_rom']),
                            ('release_stack_sha256', manifest['release_stack'])]:
        if sha(Path(artifact).read_bytes()) != manifest[field]:
            raise ValueError(f'Manifest hash differs: {field}')
    if manifest['profile'] != 'all-routes-unified-v134' or len(manifest['batches']) != 430 or not all(manifest['checks'].values()):
        raise ValueError('Manifest profile, complete batch count or release checks differ')
    report = {'status': 'pass', 'candidate': path.as_posix(), 'candidate_sha256': sha(path.read_bytes()),
              'profile': manifest['profile'], 'complete_batch_count': 430, 'pages': pages,
              'all_v133_components_preserved_except_18_help_data_spans': True,
              'all_3668_native_common_selections_byte_exact': True,
              'COMMON_and_all_route_graphics_files_byte_exact': True,
              'ARM9_executable_font_and_page_group_tables_unchanged': True,
              'formatted_body_bytes': 1794, 'original_region_bytes': 1796,
              'manifest_candidate_base_and_registry_hashes_verified': True,
              'live_page_navigation_verified': False}
    Path('work/analysis/grand_race_help_v134_saved_proof.json').write_text(json.dumps(report, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
