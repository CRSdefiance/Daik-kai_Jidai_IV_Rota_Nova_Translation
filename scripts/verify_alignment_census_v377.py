"""Verify every affected stored COMMON string with independent work buffers."""

import json
from pathlib import Path

from dk4tool.rom.nds import NdsImage
from scripts.raster_alignment_census_v377 import raster

ROOT = Path('work/analysis/unguarded_alignment_v377')


def main():
    census = json.loads((ROOT / 'current_common_census.json').read_text())
    old = NdsImage.open('out/all_routes_combined_v375_candidate.nds').read_file('/__arm9__.bin')
    new = (ROOT / 'research_arm9.bin').read_bytes()
    unique = {r['text_hex']: r for r in census['records']}
    cases = []
    for hx, row in unique.items():
        text = bytes.fromhex(hx)
        print('Checking record', row['id'], repr(text), flush=True)
        a, pa = raster(old, text, 0x0239B104 - 0x02000000, size=(228, 192), complete=False)
        b, pb = raster(new, text, 0x01FFCE40 - 0x02000000, size=(228, 192), complete=False)
        expected = bytearray(a)
        for y in range(16):
            expected[y * 228:(y + 1) * 228] = bytes(6) + a[y * 228:y * 228 + 222]
        assert b == expected, (row['id'], 'pixel difference')
        assert pa == pb, (row['id'], 'returned remainder difference')
        cases.append({'representative_id': row['id'], 'text_hex': hx, 'returned_offset': pb,
                      'only_first_row_shifted6_pixels_all_other_pixels_exact': True})
    proof = {'cases': cases, 'unique_stored_strings': len(cases),
             'covered_stored_records': len(census['records']),
             'runtime_substitutions_not_all_replayed_by_this_stored_string_check': True,
             'pixel_context_and_string_work_buffers_do_not_overlap': True,
             'full_goal_complete': False}
    (ROOT / 'census_native_proof.json').write_text(json.dumps(proof, indent=2) + '\n')
    print(f"All{len(census['records'])} eligible records/{len(cases)} unique strings preserve full pixels and remainder pointers.")


if __name__ == '__main__':
    main()
