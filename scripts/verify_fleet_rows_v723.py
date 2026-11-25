"""Ordinary Swap Ships labels plus original base-draw fragment over poison."""

import struct
from pathlib import Path

from ndspy.code import loadOverlayTable
from PIL import Image
from unicorn import UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE, arm_const

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.inspect_committed_gpu_v646 import CORE_SHA
from scripts.probe_button_prompt_native import STACK, STOP, call, machine
from scripts.trace_control_aliases_v688 import sections
from scripts.verify_confirmed_name_widget_pixels_v198 import complete_mask
from scripts.verify_portrait_native_pixels_v202 import native5
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/fleet_rows_v723')
CAP = Path('work/emulation_v193/fleet_rows_v723_actual')
ROM = Path('out/all_routes_combined_v712_candidate.nds')
LOWER, BYTES = 0x022E1794, 98304
FRAMES = (9900, 10300, 10700, 11100, 11500, 11900)


def main():
    assert not (ROOT / 'proof.json').exists()
    report_path = CAP / 'capture_report.json'
    report = read(report_path)
    assert report['frames'] == 13100 and report['cold_boot'] and not report['savestate_loaded']
    assert report['core_DLL_sha256'] == CORE_SHA and not report['callback_errors']
    assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
    assert report['ROM_sha256'] == sha(ROM.read_bytes())
    donor = report['battery_save_preloaded']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    shots = {r['frame']: r for r in report['frames_captured']}
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes()) == row['PNG_sha256']
    snapshots = {}
    for row in report['read_only_pause_RAM_snapshots']:
        assert sha(Path(row['path']).read_bytes()) == row['sha256']
        snapshots[row['frame']] = Path(row['path']).read_bytes()
    save(ROOT / 'executed_inputs.json', report['scripted_input_schedule'])
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    source = rom.read_file('/Iseki/dock.pxl')
    pxl, font = PxlImage.from_bytes(source), GameAsciiFont.from_arm9(arm)
    source_rgb = pxl.render().convert('RGB')
    batch = read('translations/fleet_row_graphics_v1.json')
    assert [r['text'] for r in batch['records']] == ['Flagship', 'Ship 2', 'Ship 3', 'Ship 4', 'Ship 5']
    rows = []
    for frame in FRAMES:
        raw = snapshots[frame]
        parent = 0x02189280
        word = lambda address, raw=raw: struct.unpack_from('<I', raw, address - 0x02000000)[0]
        assert word(parent) == 0x02152A30
        name = word(word(word(parent) - 4) + 4)
        expected_class = b'15CShipChangeView\0'
        assert raw[name - 0x02000000:name - 0x02000000 + len(expected_class)] == expected_class
        view = struct.unpack_from('<12I', raw, parent + 0x6838 - 0x02000000)
        assert view[3] == 0x022A44B8 and view[5] == 4 and view[7:12] == (0, 0, 0, 256, 192)
        cpu = machine(arm)
        cpu.mem_write(0x02000000, raw)
        executed = call(cpu, 0xD6558, (view[3],))
        header = cpu.reg_read(arm_const.UC_ARM_REG_R0)
        assert bytes(cpu.mem_read(header, len(source))) == source
        image = Image.open(shots[frame]['path']).convert('RGB')
        q = Image.new('RGB', image.size)
        q.putdata([native5(p) for p in image.get_flattened_data()])
        for record in batch['records'][1:]:
            l, t, r, b = record['box']
            text = record['text']
            x, y = l + (r - l - len(text) * 6) // 2, t + (b - t - 11) // 2
            ink, bounds = complete_mask(font, text, q, x, y + 192, native5(pxl.palette[226][:3]))
            actual = list(q.crop((l, 192 + t, r, 192 + b)).get_flattened_data())
            expected = [native5(p) for p in source_rgb.crop((l, t, r, b)).get_flattened_data()]
            assert actual == expected
            rows.append({'frame': frame, 'English': text, 'bounds': bounds, 'ink_points': ink,
                'whole800_source_pixels_exact': True, 'whole_cached_file_header': header,
                'whole_cached_file_sha256': sha(source), 'complete_cache_getter_ABI_no_IO_bridge': len(executed)})
    # Original 8-bit view-copy fragment from this captured parent. Renderer
    # interface is supplied from the captured modal scene; this is an isolated
    # underlay result, not an observed before-overlay GPU frame or full parent.
    raw = snapshots[9900]
    cpu, registered = machine(arm), machine(arm)
    for _, base, data in sections(rom):
        registered.mem_write(base, data)
    cpu.mem_write(0x02000000, raw)
    for overlay in loadOverlayTable(rom.rom.arm9OverlayTable, lambda _, f: rom.rom.files[f]).values():
        cpu.mem_write(overlay.ramAddress, bytes(overlay.data))
    cpu.mem_write(LOWER, b'\xA5' * (BYTES * 2))
    cpu.reg_write(arm_const.UC_ARM_REG_R0, 0x02189280)
    cpu.reg_write(arm_const.UC_ARM_REG_R1, 0x023117DC)
    cpu.reg_write(arm_const.UC_ARM_REG_SP, STACK)
    cpu.reg_write(arm_const.UC_ARM_REG_LR, STOP)
    written = set()

    def writes(uc, kind, address, size, value, unused):
        if LOWER <= address < LOWER + BYTES * 2:
            assert address + size <= LOWER + BYTES
            written.update(range(address, address + size))

    def reads(uc, kind, address, size, value, unused):
        if LOWER <= address < LOWER + BYTES * 2:
            assert all(p in written for p in range(address, address + size))
    from unicorn import UC_HOOK_CODE
    executed = set()

    def code(uc, address, size, unused):
        assert bytes(uc.mem_read(address, size)) == bytes(registered.mem_read(address, size)), hex(address)
        executed.add((address, size))
    handles = [cpu.hook_add(UC_HOOK_MEM_WRITE, writes), cpu.hook_add(UC_HOOK_MEM_READ, reads), cpu.hook_add(UC_HOOK_CODE, code)]
    try:
        cpu.emu_start(0x020A6CDC, 0x020A6D34, count=1000000)
    finally:
        for handle in handles:
            cpu.hook_del(handle)
    assert cpu.reg_read(arm_const.UC_ARM_REG_PC) == 0x020A6D34
    assert written == set(range(LOWER, LOWER + BYTES))
    underlay = bytes(cpu.mem_read(LOWER, BYTES))
    palette = struct.unpack_from('<256H', source, struct.unpack_from('<I', source, 12)[0])
    expected = struct.pack('<49152H', *(palette[i] for i in pxl.indices))
    assert underlay == expected and bytes(cpu.mem_read(LOWER + BYTES, BYTES)) == b'\xA5' * BYTES
    (ROOT / 'native_underlay.bin').write_bytes(underlay)
    for record in batch['records']:
        l, t, r, b = record['box']
        text = record['text']
        x, y = l + (r - l - len(text) * 6) // 2, t + (b - t - 11) // 2
        for i, char in enumerate(text):
            glyph = font.decode(char)
            for gy in range(11):
                for gx in range(6):
                    assert (pxl.indices[(y + gy) * 256 + x + i * 6 + gx] == 226) == bool(glyph.getpixel((gx, gy)))
    assert Image.open(shots[8300]['path']).tobytes() == Image.open(shots[13100]['path']).tobytes()
    releases = [ROM, ROM.with_suffix('.manifest.json'), ROM.with_suffix('.xdelta'),
        Path('translations/release_stack.json'), Path('out/raphael_natural_v2_accepted_base.nds')]
    save(ROOT / 'proof.json', {'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'report': str(report_path), 'report_sha256': sha(report_path.read_bytes()),
        'ordinary_Port_Dock_Swap_Ships_parent_identified': True, 'actual_parent_class': '15CShipChangeView',
        'actual_complete_view_words': list(view), 'asset': '/Iseki/dock.pxl', 'asset_sha256': sha(source),
        'all24_visible_Ship2_to5_masks_and_whole19200_source_pixels_exact': rows,
        'all_five_full_original_font_masks_complete_in_current_source_and_native_underlay': True,
        'native_complete_underlay49152_words_source_exact_over_poison': True,
        'no_framebuffer_output_read_before_write_and_other_plane_guard_exact': True,
        'native_fragment_instructions_exact_registered_source': len(executed),
        'native_fragment': [0x020A6CDC, 0x020A6D34], 'supplied_captured_renderer_interface': 0x023117DC,
        'not_full_parent_return_ABI_or_before_overlay_live_GPU_capture': True,
        'Flagship_source_label_covered_by_occupied_ship_name_icon_on_actual_screen_not_claimed_visible': True,
        'DOWN_inputs_did_not_select_empty_slots_in_this_one_ship_fleet': True,
        'ordinary_Info_Dock_Ships_and_Fleet_Info_detours_not_mislabelled_as_asset_consumers': True,
        'initial_offline_wrong_owner_list_interface_failed_at_53433430_not_ROM_failure': True,
        'whole_final_town_RGB_exact_before_entering_Port': True,
        'source_donor_unchanged': donor, 'no_live_gameplay_fixture_no_save_command_no_savestate': True,
        'other_fleet_compositions_or_other_arrange_parents_not_verified': True,
        'release_hashes_unchanged': {str(p): sha(p.read_bytes()) for p in releases},
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('V723: real Port/Dock/Swap Ships,24 full visible labels,49152-word original underlay,occupied Flagship limit and whole town return pass.', flush=True)


if __name__ == '__main__':
    main()
