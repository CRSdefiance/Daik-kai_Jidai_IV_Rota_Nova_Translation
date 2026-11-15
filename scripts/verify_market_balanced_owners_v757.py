"""Source-owned slots, ARM/Thumb ISA, complete restoration and inherited ABI."""

import struct
from pathlib import Path

from capstone import CS_ARCH_ARM, CS_MODE_THUMB, Cs
from ndspy.code import MainCodeFile, loadOverlayTable
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import POOL, cache_plan
from dk4tool.rom.nds import NdsImage
from scripts.prepare_product_pitches_v747 import native_layout
from scripts.probe_button_prompt_native import BASE, STACK, call, machine
from dk4tool.patch.market_stock_editorial_v2 import DONE, MAIN, RETRY, WEAK, balance_runtime as transform
ROOT = Path("work/analysis/market_balanced_v757")
from scripts.probe_market_stock_layout_v755 import experimental_arm
from scripts.review_market_stock_v755 import CURRENT
from scripts.verify_village_wrap_v608 import read, save


def scope_output(cpu, text, number, values, parent):
    template, source, output = 0x02420400, 0x02420020, 0x02420C20
    pointers = (0x02420800, 0x02420900)
    cpu.mem_write(template, text + b'\0')
    for address, value in zip(pointers, values):
        cpu.mem_write(address, value.encode('ascii') + b'\0')
    call(cpu, 0xD7720, (source, template, *pointers))
    cpu.mem_write(output - 16, b'\xA5' * 288)
    cpu.mem_write(STACK + 0x264, struct.pack('<I', parent))
    cpu.mem_write(STACK + 0x274, struct.pack('<I', number))
    call(cpu, 0x01FFCF3C - BASE, (output, source, 0))
    result = bytes(cpu.mem_read(output, 256)).split(b'\0', 1)[0]
    expected = text
    for value in values:
        expected = expected.replace(b'%s', value.encode('ascii'), 1)
    assert b' '.join(result.split()) == b' '.join(expected.split())
    assert bytes(cpu.mem_read(output - 16, 16)) == bytes(cpu.mem_read(output + 256, 16)) == b'\xA5' * 16
    return result


def main():
    rom = NdsImage.open(CURRENT)
    original = rom.read_file('/__arm9__.bin')
    filtered, _ = experimental_arm(original)
    arm, report = transform(filtered)
    before, after = MainCodeFile(filtered, BASE), MainCodeFile(arm, BASE)
    ranges = [(a, a + len(bytes.fromhex(raw))) for a, raw in report['source_string_patches']]
    assert all(a < b <= c for (a, b), (c, d) in zip(sorted(ranges), sorted(ranges)[1:]))
    units = [(f'section{i}', POOL if i == 3 else s.ramAddress, bytes(s.data))
             for i, s in enumerate(before.sections)]
    units += [(f'overlay{i}', s.ramAddress, bytes(s.data)) for i, s in loadOverlayTable(
        rom.rom.arm9OverlayTable, lambda _, f: rom.rom.files[f]).items()]
    aliases, branches, helpers, helper_literals, control_aliases, control_branches = [], [], [], [], [], []
    for label, base, raw in units:
        for at in range(len(raw) - 3):
            value = struct.unpack_from('<I', raw, at)[0]
            if any(lo <= value < hi for lo, hi in ranges):
                aliases.append((label, base + at, value))
            if value == 0x01FFCA00:
                helper_literals.append((label, base + at))
            if 0x01FFCA14 <= value < 0x01FFCA18 or 0x01FFCB40 <= value < 0x01FFCB70:
                control_aliases.append((label, base + at, value))
        for at in range(0, len(raw) - 3, 4):
            word = struct.unpack_from('<I', raw, at)[0]
            if (word >> 25) & 7 != 5:
                continue
            delta = word & 0xFFFFFF
            if delta & 0x800000:
                delta -= 0x1000000
            target = base + at + 8 + delta * 4
            if any(lo <= target < hi for lo, hi in ranges):
                branches.append((label, base + at, target))
            if target == 0x01FFCA00:
                helpers.append((label, base + at, word))
            if 0x01FFCA14 <= target < 0x01FFCA18 or 0x01FFCB40 <= target < 0x01FFCB70:
                control_branches.append((label, base + at, target))
    assert aliases == branches == helper_literals == [], (aliases, branches, helper_literals)
    assert helpers and all((w & 0xF000000) == 0xB000000 for _, _, w in helpers), helpers
    assert control_aliases == [] and control_branches == [('section4', 0x01FFCAAC, 0x01FFCB40)]
    # These source slots are complete retired Japanese strings/NUL padding from
    # the earlier Gallery/item relocation. Their current owners have moved.
    inventory = read('work/analysis/market_stock_v755/readonly_source_span_inventory_RESEARCH.json')
    for a, b in ranges:
        assert any(lo <= a and b <= hi for lo, hi in inventory['merged'])
    restored = [bytearray(s.data) for s in after.sections]
    for a, b in ranges:
        restored[0][a - BASE:b - BASE] = before.sections[0].data[a - BASE:b - BASE]
    for a, size in ((0xA14, 4), (0xB40, 48), (0xFD0, 4)):
        restored[4][a:a + size] = before.sections[4].data[a:a + size]
    assert all(bytes(s) == bytes(t.data) for s, t in zip(restored, before.sections, strict=True))
    assert [(s.ramAddress, len(s.data), s.bssSize) for s in before.sections] == [
        (s.ramAddress, len(s.data), s.bssSize) for s in after.sections]
    assert cache_plan(filtered) == cache_plan(arm)
    # Validate the actual halfwords against ARM946's Thumb-1 BL and BLX-register
    # instruction set. Unicorn alone would also accept newer Thumb instructions.
    thumb = []
    for address, size in ((MAIN, report['main_bytes'] - 8),
                          (WEAK, report['weak_bytes'] - 4), (RETRY, report['retry_bytes']), (DONE, 6)):
        raw = arm[address - BASE:address - BASE + size]
        decoded = list(Cs(CS_ARCH_ARM, CS_MODE_THUMB).disasm(raw, address))
        assert sum(i.size for i in decoded) == size
        for i in decoded:
            if i.size == 4:
                a, b = struct.unpack('<HH', i.bytes)
                assert i.mnemonic == 'bl' and a & 0xF800 == 0xF000 and b & 0xF800 == 0xF800, (hex(i.address), i.mnemonic, i.bytes.hex())
            else:
                assert i.size == 2
        thumb.append({'address': address, 'code_bytes': size,
                      'all_32bit_instructions_are_Thumb1_BL': True})
    cpus = [machine(a) for a in (original, arm)]
    for a, u in zip((original, arm), cpus, strict=True):
        u.mem_write(POOL, bytes(MainCodeFile(a, BASE).sections[3].data[:-48]))
    ids = (0, 456, 457, 480, 481, 652, 653, 655, 656, 674, 675, 681, 682,
           687, 688, 741, 742, 766, 771, 800, 801, 802, 819, 820, 821,
           869, 870, 871, 872, 873, 874, 988, 989, 3647, 3648, 3667)
    controls = []
    for parent in (0x02054014, 0x02053FCC, 0x02054044, 0x02053D24, 0x02053DB8):
        for number in ids:
            raw = b' Inherited text stays intact.'
            a, b = [native_layout(u, raw, number, (), parent) for u in cpus]
            assert a == b
            controls.append({'parent': parent, 'id': number, 'formatted_hex': b[0].hex()})
    scope = []
    templates = read('translations/market_stock_manuscript_v1.json')['records'][:4]
    for parent in (0x02053FCC, 0x02054044, 0x02053D24, 0x02053DB8):
        for table in (0x02117B40, 0x021181E0, 0x021182A0, 0x02118300, 0x021184C0):
            for row in templates:
                text = b' ' + row['english'].removesuffix('{PAD}').encode('ascii')
                values = ('Tea',) * text.count(b'%s')
                results = []
                for u in cpus:
                    u.mem_write(STACK + 0x27C, struct.pack('<I', table))
                    results.append(scope_output(u, text, row['message_id'], values, parent))
                assert results[0] == results[1], (parent, table, row['message_id'], results)
                scope.append({'parent': parent, 'table': table, 'id': row['message_id'],
                              'complete_output_and_saved_ABI_equal_V754': True})
    direct = []
    for raw in (b'', b' ', b'   ', b' One short line.', b'  Multiple   spaces and\n\n guard spaces stay normalized.',
                b' Trailing spaces stay normalized.   ', b' ' + b'word ' * 25,
                b' ' + b'word ' * 50, b' ' + b'x' * 36, b' ' + b'x' * 37,
                b' ' + b'x' * 238, b' Before\nafter.\n   The last line.'):
        results = []
        for u in cpus:
            source, output = 0x02420000, 0x02421010
            u.mem_write(source, raw + b'\0')
            u.mem_write(output - 16, b'\xA5' * 272)
            call(u, 0x01FFCA00 - BASE, (source, output))
            results.append((u.reg_read(UC_ARM_REG_R0), bytes(u.mem_read(output - 16, 272))))
        assert results[0] == results[1]
        assert results[1][1][:16] == results[1][1][-16:] == b'\xA5' * 16
        direct.append({'input_hex': raw.hex(), 'result': results[1][0],
                       'complete_output_success_failure_and_guards_exact': True})
    weak_words = {'a', 'an', 'as', 'at', 'for', 'from', 'in', 'of', 'the', 'to', 'with'}
    hashes = {int.from_bytes(w.encode('ascii'), 'big') for w in weak_words}
    texts = [r['english'].removesuffix('{PAD}').replace('%s', '') for r in read('translations/market_stock_manuscript_v1.json')['records'][:4]]
    texts += [r['name'] for r in read('work/analysis/product_pitches_v747/runtime_name_catalog.json')['products']]
    tokens = sorted({w for s in texts for w in s.split()})
    assert all((int.from_bytes(w.encode('ascii'), 'big') & 0xFFFFFFFF in hashes) == (w in weak_words) for w in tokens)
    save(ROOT / 'ownership_ABI.json', {'source_V754_ARM9_sha256': sha(original),
        'filtered_source_ARM9_sha256': sha(filtered), 'research_ARM9_sha256': sha(arm),
        'source_owned_patch_ranges': ranges, 'all_current_unaligned_pointer_owners': aliases,
        'all_current_direct_branch_owners': branches, 'all_original_helper_pointer_aliases': helper_literals,
        'all_original_control_aliases': control_aliases, 'all_original_control_branches': control_branches,
        'all_existing_helper_calls_are_direct_ARM_BL': helpers,
        'new_private_adapter_is_the_sole_Thumb_caller': True,
        'Thumb_ISA_checks': thumb, 'all180_inherited_full_output_controls': controls,
        'all80_non_direct_post_format_output_and_ABI_controls': scope,
        'all_scoped_template_and124_product_word_hashes_have_no_false_weak_matches': tokens,
        'all12_direct_helper_success_failure_ABI_and_output_controls': direct,
        'all_other_section_bytes_pool_startup_shapes_and_cache_plan_exact': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'actual_gameplay_pending': True,
        'full_goal_complete': False})
    print('Owned-string aliases, Thumb-1 ISA,180 inherited outputs and12 helper ABI/bound controls pass.', flush=True)


if __name__ == '__main__':
    main()
