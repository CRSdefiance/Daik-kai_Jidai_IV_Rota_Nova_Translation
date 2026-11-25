"""Rebuild the real map mask from original area bits, records and native code.

Only isolated Unicorn copies change. Existing V638 screenshots remain the actual
gameplay evidence; synthetic area-bit controls do not establish earned maps.
"""

import struct
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.probe_worldmap_overlays_v638 import CAP, ROM
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/worldmap_mask_v639')
BASE, PAGE_BYTES = 0x02000000, 19520
SCRATCH, STORE, PIXELS = 0x022403C0, 0x022857AC, 0x02279B6C


def words(cpu, address, count):
    return struct.unpack(f'<{count}I', cpu.mem_read(address, count * 4))


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm = rom.read_file('/__arm9__.bin')
    assert sha(ROM.read_bytes()) == 'c4ff537ddcd4da5eb1743fb28cd0eb160492e9b660af080ddae44e94a9f4d95d'
    source_proof_path = Path('work/analysis/worldmap_composition_v638/native_composition_proof.json')
    prior = read(source_proof_path)
    report_path = CAP / 'capture_report.json'
    assert sha(report_path.read_bytes()) == prior['report_sha256']
    report = read(report_path)
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    raw_path = CAP / 'frame_036000_arm9_ram.bin'
    raw = raw_path.read_bytes()
    assert sha(raw) == prior['RAM_sha256']
    expected_actual = raw[PIXELS - BASE:PIXELS - BASE + PAGE_BYTES]
    seaarea = rom.read_file('/_pxl/seaarea.pxl')
    assert seaarea == clean.read_file('/_pxl/seaarea.pxl')
    page = seaarea[276 + 7 * PAGE_BYTES:276 + 8 * PAGE_BYTES]
    original = machine(clean.read_file('/__arm9__.bin'))
    all_executed = set()

    def invoke(cpu, offset, args):
        executed = call(cpu, offset, args, instruction_limit=1800000)
        assert not ({0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08} & executed)
        assert all(bytes(cpu.mem_read(a, 4)) == bytes(original.mem_read(a, 4)) for a in executed)
        all_executed.update(executed)

    def fresh():
        cpu = machine(arm)
        cpu.mem_write(BASE, raw)
        invoke(cpu, 0x989E8, (0x0218A3B8,))
        receiver = cpu.reg_read(UC_ARM_REG_R0)
        assert receiver == 0x0218A3A8
        assert words(cpu, receiver + 0x6C80, 1) == (1,)
        return cpu, receiver

    probe, receiver = fresh()
    invoke(probe, 0xCB118, ())
    area_store = probe.reg_read(UC_ARM_REG_R0)
    bit_word_address = area_store + 4
    assert words(probe, bit_word_address, 1) == (0,)
    invoke(probe, 0x9458C, (7,))
    source_map_record = probe.reg_read(UC_ARM_REG_R0)
    world_rect = words(probe, source_map_record + 4, 4)
    target_rect = struct.unpack_from('<4I', arm, 0x119984)
    assert world_rect == (0, 0, 40000, 20000) and target_rect == (0, 0, 244, 160)
    regions = []
    for index in range(24):
        invoke(probe, 0xCACAC, (area_store, index))
        record = probe.reg_read(UC_ARM_REG_R0)
        values = words(probe, record, 13)
        invoke(probe, 0xCADA0, (record,))
        assert probe.reg_read(UC_ARM_REG_R0) == index
        invoke(probe, 0xCAD68, (record,))
        assert probe.reg_read(UC_ARM_REG_R0) == 0
        rectangles = []
        for slot, start in ((0, 5), (1, 9)):
            x, y, width, height = values[start:start + 4]
            if width == 0:
                continue
            assert 0 <= x < x + width <= 40000 and 0 <= y < y + height <= 20000
            # Independent positive-coordinate rational model. Native CEF D0
            # selects these same bounds through its original geometry routine.
            rect = [x * 244 // 40000, y * 160 // 20000,
                    (x + width) * 244 // 40000, (y + height) * 160 // 20000]
            rectangles.append({'slot': slot, 'world_xy_size': [x, y, width, height], 'map_bounds': rect})
        regions.append({'index': index, 'native_record': record,
                        'record_sha256': sha(bytes(probe.mem_read(record, 52))),
                        'original_visibility_bit': 0, 'rectangles': rectangles})
    assert sum(len(r['rectangles']) for r in regions) == 28

    # Negative cache control: retained "ready" flag must leave poisoned scratch
    # untouched. The successful rebuild below therefore cannot be a cache hit.
    cached, cache_receiver = fresh()
    poison = b'\xA5' * PAGE_BYTES
    cached.mem_write(SCRATCH, poison)
    invoke(cached, 0x8F334, (cache_receiver, 7, 0))
    assert bytes(cached.mem_read(SCRATCH, PAGE_BYTES)) == poison
    cases = []
    for label, enabled in (('actual_capture_bits', ()), ('isolated_area14_bit', (14,)),
                           ('isolated_all24_bits', tuple(range(24)))):
        cpu, root = fresh()
        setter_receipts = []
        for index in enabled:
            before = bytes(cpu.mem_read(BASE, len(raw)))
            invoke(cpu, 0xCAD38, (regions[index]['native_record'], 1))
            after = bytes(cpu.mem_read(BASE, len(raw)))
            changes = [BASE + i for i, (a, b) in enumerate(zip(before, after, strict=True)) if a != b]
            permitted = set(range(bit_word_address, bit_word_address + 4)) | set(range(STORE + 0x8520, STORE + 0x8524))
            assert set(changes) <= permitted
            setter_receipts.append({'area': index, 'original_setter': BASE + 0xCAD38,
                                    'changed_addresses': changes,
                                    'before_RAM_sha256': sha(before), 'after_RAM_sha256': sha(after)})
        bits = sum(1 << index for index in enabled)
        assert words(cpu, bit_word_address, 1) == (bits,)
        for region in regions:
            invoke(cpu, 0xCAD68, (region['native_record'],))
            assert cpu.reg_read(UC_ARM_REG_R0) == (bits & (1 << region['index']))
        # Supplied cache invalidation is restricted to this one control word in
        # an isolated native copy; live emulator RAM and battery saves are untouched.
        cpu.mem_write(root + 0x6C80, bytes(4))
        cpu.mem_write(SCRATCH, poison)
        guard_before = (bytes(cpu.mem_read(SCRATCH - 16, 16)), bytes(cpu.mem_read(SCRATCH + PAGE_BYTES, 16)))
        erasures, selected = [], {'index': None}

        def trace(uc, address, size, unused, selected=selected, erasures=erasures):
            if address == BASE + 0xCACAC:
                selected['index'] = uc.reg_read(UC_ARM_REG_R1)
            if address == BASE + 0xD5C98:
                assert uc.reg_read(UC_ARM_REG_R1) == 0
                erasures.append({'area': selected['index'],
                                 'map_bounds': list(words(uc, uc.reg_read(UC_ARM_REG_R2), 4))})

        hook = cpu.hook_add(UC_HOOK_CODE, trace)
        try:
            invoke(cpu, 0x8F334, (root, 7, 0))
        finally:
            cpu.hook_del(hook)
        expected_rectangles = [{'area': r['index'], 'map_bounds': q['map_bounds']}
                               for r in regions if r['index'] not in enabled for q in r['rectangles']]
        assert erasures == expected_rectangles
        source_indices = [n for b in page for n in (b & 15, b >> 4)]
        erased = set()
        for row in expected_rectangles:
            x0, y0, x1, y1 = row['map_bounds']
            for y in range(y0, y1):
                for x in range(x0, x1):
                    source_indices[y * 244 + x] = 0
                    erased.add((x, y))
        independent = bytes(source_indices[i] | source_indices[i + 1] << 4
                            for i in range(0, len(source_indices), 2))
        actual = bytes(cpu.mem_read(SCRATCH, PAGE_BYTES))
        assert actual == independent
        assert words(cpu, root + 0x6C80, 1) == (1,)
        assert guard_before == (bytes(cpu.mem_read(SCRATCH - 16, 16)),
                                bytes(cpu.mem_read(SCRATCH + PAGE_BYTES, 16)))
        if not enabled:
            assert actual == expected_actual and len(erased) == 28865
            assert sum(bool(n) for n in source_indices) == 9674
        if len(enabled) == 24:
            assert actual == page and not erasures
        invoke(cpu, 0x47470, (STORE,))
        assert words(cpu, STORE + 0x8520, 2) == (9, 0)
        target_guard = (bytes(cpu.mem_read(PIXELS - 16, 16)), bytes(cpu.mem_read(PIXELS + PAGE_BYTES, 16)))
        cpu.mem_write(PIXELS, poison)
        invoke(cpu, 0x8F334, (root, 7, 1))
        assert bytes(cpu.mem_read(PIXELS, PAGE_BYTES)) == independent
        assert words(cpu, STORE + 0x8520, 2) == (7, 0)
        assert target_guard == (bytes(cpu.mem_read(PIXELS - 16, 16)),
                                bytes(cpu.mem_read(PIXELS + PAGE_BYTES, 16)))
        # A repeated original getter path is a cache hit and preserves destination.
        before_hit = bytes(cpu.mem_read(PIXELS, PAGE_BYTES))
        invoke(cpu, 0x8F334, (root, 7, 1))
        assert bytes(cpu.mem_read(PIXELS, PAGE_BYTES)) == before_hit
        cases.append({'label': label, 'enabled_area_bits': list(enabled), 'visibility_word': bits,
                      'setter_receipts': setter_receipts, 'native_erasure_rectangles': erasures,
                      'union_erased_pixels': len(erased), 'remaining_nonzero_pixels': sum(bool(n) for n in source_indices),
                      'all19520_packed_bytes_and39040_indices_match_independent_model': True,
                      'bitmap_sha256': sha(actual), 'poisoned_destination_complete_native_copy_exact': True,
                      'mask_ready_and_page_cache_flags_verified': True, 'both_buffers_adjacent_guards_exact': True,
                      'repeated_original_copy_cache_hit_preserves_destination': True,
                      'synthetic_area_state_never_applied_to_emulator': bool(enabled)})
    # Current actual area data remains unchanged on disk and in the immutable export.
    assert raw_path.read_bytes() == raw and sha(ROM.read_bytes()) == prior['candidate_sha256']
    palette = struct.unpack_from('<16H', raw, PIXELS - BASE - 32)
    colors = [((v & 31) * 255 // 31, ((v >> 5) & 31) * 255 // 31, ((v >> 10) & 31) * 255 // 31) for v in palette]
    sheet = Image.new('RGB', (1500, 420), '#263238')
    draw = ImageDraw.Draw(sheet)
    font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 18)
    for x, title, packed in ((8, 'Original source painting: page7', page),
                              (508, 'Actual native mask:28 rectangles', expected_actual),
                              (1008, 'Controlled all24 bits: source restored', page)):
        indices = [n for b in packed for n in (b & 15, b >> 4)]
        panel = Image.new('RGB', (244, 160))
        panel.putdata([colors[n] for n in indices])
        draw.text((x, 8), title, font=font, fill='white')
        sheet.paste(panel.resize((488, 320), Image.Resampling.NEAREST), (x, 40))
    draw.text((8, 380), 'Derived bitmap review at2x. Source/native tests reuse V638; controlled states are not gameplay or earned discovery.', font=font, fill='#dfd3ac')
    sheet_path = ROOT / 'MAP_MASK_SOURCE_REVIEW_2x_DERIVED.png'
    sheet.save(sheet_path)
    proof = {
        'candidate': str(ROM), 'candidate_sha256': prior['candidate_sha256'],
        'source_capture_report': str(report_path), 'source_capture_report_sha256': sha(report_path.read_bytes()),
        'source_actual_RAM': str(raw_path), 'source_actual_RAM_sha256': sha(raw),
        'source_composition_proof': str(source_proof_path), 'source_composition_proof_sha256': sha(source_proof_path.read_bytes()),
        'reuses_V638_cold_boot_not_a_new_emulator_run': True,
        'actual_original_controller_getter': BASE + 0x989E8, 'actual_controller': receiver,
        'mask_scratch': SCRATCH, 'page_cache_store': STORE, 'actual_map_pixels': PIXELS,
        'area_visibility_word_address': bit_word_address, 'captured_visibility_word': 0,
        'source_world_bounds': list(world_rect), 'target_pixel_bounds': list(target_rect),
        'all24_actual_area_records': regions, 'three_complete_native_mask_and_copy_cases': cases,
        'all_native_calls_full_return_stack_saved_register_ABI_and_executed_words_exact_clean': True,
        'executed_instruction_addresses': sorted(all_executed),
        'no_file_getter_painter_or_filesystem_bridge': True,
        'actual19520_bytes_and_all39040_indices_source_construction_verified': True,
        'captured_background_pixels': {'cleared_by_original_rectangles': 28865,
                                       'already_zero_source_pixels_outside_rectangles': 501,
                                       'total_zero_pixels': 29366},
        'retained_ready_flag_poisoned_scratch_negative_control_rejected_rebuild': True,
        'only_one_mask_cache_word_invalidated_in_isolated_copy': receiver + 0x6C80,
        'synthetic_area_bits_changed_only_by_original_setter_never_live_or_saved': True,
        'guide_or_earned_map_discovery_not_claimed_for_controls': True,
        'first_probe_reversed_scratch_and_store_addresses_excluded': str(ROOT / 'initial_mask_probe.json'),
        'derived_review_sheet': str(sheet_path), 'derived_review_sheet_sha256': sha(sheet_path.read_bytes()),
        'ROM_patch_registry_canonical_changes': False,
        'other_actual_map_pages_sepia_and_legacy_consumers_remain_open': True,
        'all18_plaques_incomplete_all22_historical_scopes_retained': True,
        'script_sha256': sha(Path(__file__).read_bytes()),
        'hardware_device_verification': False, 'full_goal_complete': False,
    }
    save(ROOT / 'native_mask_proof.json', proof)
    print('Original mask source verified:24 area bits,28 rectangles,all39040 actual indices; three guarded native rebuild/copy cases pass independent models.')


if __name__ == '__main__':
    main()
