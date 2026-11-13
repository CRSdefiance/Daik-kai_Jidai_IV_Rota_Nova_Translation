"""Research private backing storage; no registry or release handoff."""

import json
import struct
from pathlib import Path

from dk4tool.patch.commodity_compact_layout import compact_helper
from dk4tool.patch.commodity_source_repack import transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_display_name_hook import branch_link

ROOT = Path('work/analysis/commodity_private_canvas_v347')
BASE = 0x02000000


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    source = NdsImage.open('out/all_routes_combined_v342_candidate.nds').read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    manuscript = json.loads(Path('translations/commodity_name_manuscript_v343.json').read_text(encoding='utf-8'))
    allocation = json.loads(Path('work/analysis/commodity_layout_v345/allocation.json').read_text())
    packed, names = transform(source, clean, manuscript, allocation)
    target = bytearray(packed)
    lo, hi = 1432612, 1432644
    group = next(g for g in allocation['bins'] if g['start'] == lo and g['end'] == hi)
    assert not group['names']
    # Clear the new allocation without touching the surrounding heap blocks.
    clear = struct.pack('<5I', 0xE1A03000, 0xE4832004, 0xE2511004,
                        0x1AFFFFFC, 0xE12FFF1E)
    target[lo:hi] = clear + bytes(hi - lo - len(clear))
    entry = 0x10DCB0
    assert struct.unpack_from('<I', source, entry)[0] == 0xE92D4000
    words = [0xE92D4010, 0xE59F4040, 0xE3A00C3B,
             branch_link(BASE + entry + 12, BASE + 0x5154),
             0xE3A01C3B, 0xE3A02000,
             branch_link(BASE + entry + 24, BASE + lo),
             0xE0400004, 0xE5840010, 0xE59F1024, 0xE0411004, 0xE584100C,
             0xE3A01004, 0xE5841000, 0xE3A01039, 0xE5841004,
             0xE3A01084, 0xE5841008, 0xE8BD8010, 0x022BD774, 0x02125A20]
    code = struct.pack('<21I', *words)
    target[entry:0x10DD0C] = code + bytes(0x10DD0C - entry - len(code))
    helper = compact_helper(BASE + 0x15BB40)
    target[0x15BB40:0x15BB68] = helper + bytes(40 - len(helper))
    struct.pack_into('<I', target, 0xB63D4, branch_link(BASE + 0xB63D4, BASE + 0x15BB40))
    for i in range(5):
        row = 0x11A73C + i * 28
        struct.pack_into('<3I', target, row + 12, 0, 72 + i * 12, 96)
    # All original non-specialty descriptors, including percentages, stay exact.
    for i in (*range(8), *range(13, 21)):
        field = 0x11A65C + i * 28
        assert target[field:field + 28] == source[field:field + 28]
    (ROOT / 'research_arm9.bin').write_bytes(target)
    for variant, substitutions in [('normal', []), ('long', [(42, 115), (51, 103), (62, 108)])]:
        data = bytearray(target)
        data[0x9F068] = 4
        for displayed, label in substitutions:
            field = 0x15EF18 + displayed * 12
            data[field:field + 4] = target[0x15EF18 + label * 12:0x15EF18 + label * 12 + 4]
        rom = NdsImage.open('out/all_routes_combined_v342_candidate.nds')
        rom.replace_file('/__arm9__.bin', bytes(data))
        rom.save(ROOT / ('research_only_' + variant + '_Maria.nds'))
    proof = {'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(target),
             'name_repack': names, 'native_canvas_initializer': entry,
             'clear_helper_region': [lo, hi], 'allocation_bytes': 0x3B00,
             'logical_backing_size': [228, 132], 'original_size': [228, 72],
             'ROM_art_dimensions_palettes_and_visible_positions_unchanged': True,
             'original_non_specialty_coordinates_preserved': True,
             'native_allocator_lifetime_and_actual_startup_pending': True,
             'research_only_not_for_handoff': True}
    (ROOT / 'plan.json').write_text(json.dumps(proof, indent=2) + '\n')
    print('Private canvas research prepared; native allocation and playback unproven.')


if __name__ == '__main__':
    main()
