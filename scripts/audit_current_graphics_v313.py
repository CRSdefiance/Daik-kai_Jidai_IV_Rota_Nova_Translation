"""Refresh all921 asset preservation checks on the actual current candidate."""

import json
import struct
from pathlib import Path

from dk4tool.graphics.fls import FlsArchive
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage

ROOT = Path('work/analysis/current_graphics_v313')
ROM = Path('out/all_routes_combined_v309_candidate.nds')


def main():
    clean, current = NdsImage.open('work/clean.nds'), NdsImage.open(ROM)
    files = {p: bytes(raw) for _, p, raw in current.iter_files()}
    rows = []
    for _, path, source in clean.iter_files():
        saved = files[path]
        if path.casefold().endswith('.pxl'):
            a, b = struct.unpack_from('<5I', source), struct.unpack_from('<5I', saved)
            assert a[:3] == b[:3], path
            depth = a[0] & 255
            palette_bytes = 32 if depth == 4 else 512 if depth == 8 else 0
            assert source[a[3]:a[3] + palette_bytes] == saved[b[3]:b[3] + palette_bytes], path
            assert len(source) - a[4] == len(saved) - b[4], path
            rows.append({'path': path, 'kind': 'PXL', 'depth': depth,
                         'flags_pitch_height_and_palette_preserved': True,
                         'complete_pixel_payload_extent_preserved': True, 'changed': source != saved,
                         'source_file_sha256': sha(source), 'current_file_sha256': sha(saved)})
        elif path.casefold().endswith('.fls'):
            a, b = FlsArchive(source), FlsArchive(saved)
            assert a.count == b.count and a.compressed_storage == b.compressed_storage
            for index in range(a.count):
                old, new = a.texture(index), b.texture(index)
                assert (old.flags, old.width, old.height) == (new.flags, new.width, new.height)
                assert old.palette == new.palette and len(old.indices) == len(new.indices)
                # Complete metadata dimensions include native view and padding.
                assert a.records[index][:2] == b.records[index][:2]
                rows.append({'path': path, 'kind': 'FLS', 'texture': index,
                             'flags_native_view_storage_dimensions_and_palette_preserved': True,
                             'complete_pixel_payload_extent_preserved': True,
                             'compressed_storage': a.compressed_storage, 'changed': old.indices != new.indices,
                             'source_pixel_sha256': sha(bytes(old.indices)), 'current_pixel_sha256': sha(bytes(new.indices))})
    assert len(rows) == 921
    assert sum(r['kind'] == 'PXL' for r in rows) == 660
    assert sum(r['kind'] == 'FLS' for r in rows) == 261
    assert sum(r['kind'] == 'PXL' and r['depth'] not in (4, 8) for r in rows) == 42
    proof = {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
             'clean_sha256': sha(Path('work/clean.nds').read_bytes()), 'entries': rows,
             'all921_source_formats_flags_palettes_dimensions_and_payload_extents_preserved': True,
             'changed_entries': sum(r['changed'] for r in rows),
             'preservation_does_not_prove_translation_border_crop_alpha_or_gameplay_completion': True,
             'full_goal_complete': False}
    ROOT.mkdir(parents=True, exist_ok=True)
    (ROOT / 'preservation_proof.json').write_text(json.dumps(proof, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({'PXL': 660, 'FLS': 261, 'direct_colour_PXL': 42,
                      'changed_entries': proof['changed_entries'], 'all_preservation_checks_pass': True}))


if __name__ == '__main__':
    main()
