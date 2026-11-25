"""Audit the existing dispatcher extent and preserve inherited full outputs."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import POOL, cache_plan
from dk4tool.rom.nds import NdsImage
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.probe_button_prompt_native import BASE, machine
from scripts.probe_market_stock_layout_v755 import experimental_arm
from scripts.review_market_stock_v755 import CURRENT, ROOT
from scripts.verify_village_wrap_v608 import save


def main():
    rom = NdsImage.open(CURRENT)
    arm = rom.read_file('/__arm9__.bin')
    new, patch = experimental_arm(arm)
    code = MainCodeFile(arm, BASE)
    units = [(f'section{i}', POOL if i == 3 else s.ramAddress, bytes(s.data))
             for i, s in enumerate(code.sections)]
    units += [(f'overlay{i}', s.ramAddress, bytes(s.data)) for i, s in loadOverlayTable(
        rom.rom.arm9OverlayTable, lambda _, f: rom.rom.files[f]).items()]
    pointers, branches = [], []
    lo, hi = 0x01FFCF54, 0x01FFCF78
    for label, base, raw in units:
        for at in range(len(raw) - 3):
            word = struct.unpack_from('<I', raw, at)[0]
            if lo <= word < hi:
                pointers.append((label, base + at, word))
        for at in range(0, len(raw) - 3, 4):
            word = struct.unpack_from('<I', raw, at)[0]
            if (word >> 25) & 7 != 5:
                continue
            delta = word & 0xFFFFFF
            if delta & 0x800000:
                delta -= 0x1000000
            target = base + at + 8 + delta * 4
            if lo <= target < hi:
                branches.append((label, base + at, target))
    assert pointers == [] and branches == [('section4', 0x01FFCBFC, lo)], (pointers, branches)
    assert cache_plan(arm) == cache_plan(new)
    assert [(s.ramAddress, len(s.data), s.bssSize) for s in code.sections] == [
        (s.ramAddress, len(s.data), s.bssSize) for s in MainCodeFile(new, BASE).sections]
    machines = [machine(a) for a in (arm, new)]
    for a, cpu in zip((arm, new), machines, strict=True):
        cpu.mem_write(POOL, bytes(MainCodeFile(a, BASE).sections[3].data[:-48]))
    # Exercise each inherited range and both old redundant870-873 endpoints,
    # plus adjacent fallback boundaries through the complete printf/copy/wrap.
    ids = (0, 456, 457, 480, 481, 652, 653, 655, 656, 674, 675, 681, 682,
           687, 688, 741, 742, 766, 771, 800, 801, 802, 819, 820, 821,
           869, 870, 871, 872, 873, 874, 988, 989, 3647, 3648, 3667)
    controls = []
    for parent in (0x02054014, 0x02053FCC, 0x02054044, 0x02053D24, 0x02053DB8):
        for n in ids:
            # A single natural line works in selected and fallback consumers;
            # complete output bytes and all native guards must be identical.
            raw = b' Inherited text stays intact.'
            before, after = [native_layout(cpu, raw, n, (), parent) for cpu in machines]
            assert before == after
            controls.append({'parent': parent, 'id': n, 'formatted_hex': after[0].hex(),
                             'complete_output_and_guards_identical': True})
    save(ROOT / 'experimental_filter_ownership.json', {
        'source_ARM9_sha256': sha(arm), 'research_ARM9_sha256': sha(new),
        'existing_owned_dispatcher_extent': [lo, hi],
        'all_unaligned_absolute_aliases': pointers, 'all_direct_branch_owners': branches,
        'all_main_autoload_and_current_overlay_units': [r[0] for r in units],
        'patch': patch, 'all180_inherited_complete_output_controls': controls,
        'all_section_sizes_pool_cache_shapes_and_other_bytes_unchanged': True,
        'formatter_quality_new_prose_integration_and_gameplay_still_pending': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    assert len(controls) == 180
    print('Dispatcher ownership and180 inherited complete native controls pass; research only.', flush=True)


if __name__ == '__main__':
    main()
