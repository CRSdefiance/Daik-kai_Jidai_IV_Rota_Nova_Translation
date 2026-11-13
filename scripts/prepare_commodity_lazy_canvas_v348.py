"""Research lazy canvas allocation after heap initialization."""

import json
import struct
from pathlib import Path

from dk4tool.patch.commodity_compact_layout import compact_helper
from dk4tool.patch.commodity_source_repack import transform
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_common_display_name_hook import branch_link

BASE = 0x02000000
ROOT = Path('work/analysis/commodity_lazy_canvas_v349')


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    source = NdsImage.open('out/all_routes_combined_v342_candidate.nds').read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    manuscript = json.loads(Path('translations/commodity_name_manuscript_v343.json').read_text(encoding='utf-8'))
    allocation = json.loads(Path('work/analysis/commodity_layout_v345/allocation.json').read_text())
    packed, names = transform(source, clean, manuscript, allocation)
    target = bytearray(packed)
    blocks = []
    for group in allocation['bins']:
        end = max((n['offset'] + len(n['English']) + 1 for n in group['names']), default=group['start'])
        lo = (end + 3) & ~3
        if group['end'] - lo >= 8:
            blocks.append((lo, group['end']))
    # The compact helper returns after32 bytes; its last8 owned bytes are free.
    blocks.append((0x15BB60, 0x15BB68))
    blocks.sort(key=lambda pair: (-(pair[1] - pair[0]), pair[0]))
    # All code lives in unused tails of source-owned, repacked name regions.
    instructions = [0xE92D4070, 0xE1A04000, 0xE1A05001, 0xE5952008,
                    0xE3520084, ('beq', 24), 0xE3A00C3B, ('bl', BASE + 0x5154),
                    0xE1A06000, 0xE3A01C3B, 0xE3A02000, 0xE1A03000,
                    0xE4832004, 0xE2511004, ('bne', 12),
                    0xE5951010, 0xE0811005, 0xE3A02A02, 0xE2822010,
                    ('bl', BASE + 0xCEC74), 0xE0460005, 0xE5850010,
                    0xE3A01084, 0xE5851008,
                    0xE1A00004, 0xE1A01005, 0xE3A02000, 0xE3A03000,
                    0xE8BD4070, ('b', BASE + 0xD3E44)]
    locations, used, left = [], [], len(instructions)
    for lo, hi in blocks:
        capacity = (hi - lo) // 4
        count = left if left <= capacity else capacity - 1
        locations.extend(BASE + lo + n * 4 for n in range(count))
        used.append((lo, hi, count))
        left -= count
        if not left:
            break
    assert not left, ('Insufficient owned code tails', blocks)
    for i, instruction in enumerate(instructions):
        addr = locations[i]
        if isinstance(instruction, tuple):
            kind, destination = instruction
            if kind in ('beq', 'bne'):
                destination = locations[destination]
            word = branch_link(addr, destination)
            word = (word & 0xFFFFFF) | {'bl': 0xEB000000, 'b': 0xEA000000,
                                      'beq': 0x0A000000, 'bne': 0x1A000000}[kind]
        else:
            word = instruction
        struct.pack_into('<I', target, addr - BASE, word)
    consumed = 0
    for lo, hi, count in used:
        consumed += count
        if consumed < len(instructions):
            addr = BASE + lo + count * 4
            struct.pack_into('<I', target, addr - BASE,
                             (branch_link(addr, locations[consumed]) & 0xFFFFFF) | 0xEA000000)
    # Only the original town bitmap binding call invokes the lazy allocation.
    assert struct.unpack_from('<I', source, 0xB59AC)[0] == branch_link(BASE + 0xB59AC, BASE + 0xD3E44)
    struct.pack_into('<I', target, 0xB59AC, branch_link(BASE + 0xB59AC, locations[0]))
    helper = compact_helper(BASE + 0x15BB40)
    target[0x15BB40:0x15BB60] = helper[:32]
    struct.pack_into('<I', target, 0xB63D4, branch_link(BASE + 0xB63D4, BASE + 0x15BB40))
    for i in range(5):
        struct.pack_into('<3I', target, 0x11A73C + i * 28 + 12, 0, 72 + i * 12, 96)
    # The town source view has its own fixed dimensions separate from the
    # shared image header; the240x192 on-screen parent remains unchanged.
    assert struct.unpack_from('<4I', source, 0x11A644) == (240, 192, 228, 72)
    struct.pack_into('<I', target, 0x11A650, 132)
    assert target[0x10DCB0:0x10DD0C] == source[0x10DCB0:0x10DD0C]
    restored = bytearray(target)
    for lo, hi, _ in used:
        restored[lo:hi] = packed[lo:hi]
    restored[0x15BB40:0x15BB68] = packed[0x15BB40:0x15BB68]
    for field in [0xB59AC, 0xB63D4, 0x11A650]:
        restored[field:field + 4] = packed[field:field + 4]
    for i in range(5):
        field = 0x11A73C + i * 28 + 12
        restored[field:field + 12] = packed[field:field + 12]
    assert bytes(restored) == packed
    (ROOT / 'research_arm9.bin').write_bytes(target)
    for variant, substitutions in [('normal', []), ('long', [(42, 115), (51, 103), (62, 108)])]:
        data = bytearray(target)
        data[0x9F068] = 4
        for displayed, label in substitutions:
            data[0x15EF18 + displayed * 12:0x15EF18 + displayed * 12 + 4] = target[0x15EF18 + label * 12:0x15EF18 + label * 12 + 4]
        rom = NdsImage.open('out/all_routes_combined_v342_candidate.nds')
        rom.replace_file('/__arm9__.bin', bytes(data))
        rom.save(ROOT / ('research_only_' + variant + '_Maria.nds'))
    plan = {'name_repack': names, 'lazy_entry': locations[0], 'instruction_addresses': locations,
            'source_arm9_sha256': sha(source), 'target_arm9_sha256': sha(target),
            'all_undeclared_bytes_exact_repacked_parent': True,
            'owned_tail_blocks': used, 'initial_header_initializer_exact': True,
            'old_pixels_copied_before_new_specialty_rows': True, 'allocation_guard_height': 132,
            'town_source_view_height_field': 0x11A650,
            'visible_parent_dimensions_preserved': [240, 192],
            'native_and_actual_verification_pending': True, 'not_for_handoff': True}
    (ROOT / 'plan.json').write_text(json.dumps(plan, indent=2) + '\n')
    print('Prepared lazy town-only canvas research in source-owned storage.')


if __name__ == '__main__':
    main()
