"""Original registered map painters and complete actual bitmap composition."""

import struct
from pathlib import Path

from ndspy.code import loadOverlayTable
from PIL import Image
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (
    UC_ARM_REG_LR,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_SP,
)

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import call, machine
from scripts.probe_worldmap_overlays_v638 import CAP, ROM, ROOT, color5
from scripts.verify_village_wrap_v608 import read, save

BASE = 0x02000000
CONTEXT = 0x023117C4


def native_callback(rom, clean, raw, sprite):
    arm = rom.read_file('/__arm9__.bin')
    u, original = machine(arm), machine(clean.read_file('/__arm9__.bin'))
    u.mem_write(BASE, raw)
    for image, cpu in ((rom, u), (clean, original)):
        overlay = loadOverlayTable(image.rom.arm9OverlayTable, lambda i, f, image=image: image.files[f])[0]
        cpu.mem_write(overlay.ramAddress, bytes(overlay.data))

    def words(p, n):
        return list(struct.unpack(f'<{n}I', u.mem_read(p, n * 4)))

    assert words(CONTEXT, 1) == [0x0215FA94]
    vtable = words(sprite, 1)[0]
    method = words(vtable + 12, 1)[0]
    events, views = [], []

    def trace(cpu, address, size, unused):
        if address == 0x020D4170:
            view = cpu.reg_read(UC_ARM_REG_R0)
            views.append({'view': view, 'words': words(view, 12)})
        if address != 0x01FF92D8:
            return
        screen, header, bank, xy = [cpu.reg_read(r) for r in
                                  (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)]
        size_pointer, destination_pointer = words(cpu.reg_read(UC_ARM_REG_SP), 2)
        events.append({'helper': address, 'original_caller_return': cpu.reg_read(UC_ARM_REG_LR),
                       'screen_selector': screen, 'header': header, 'header_words': words(header, 5),
                       'palette_bank': bank, 'source_xy': words(xy, 2), 'source_size': words(size_pointer, 2),
                       'destination_point': words(destination_pointer, 2)})

    handle = u.hook_add(UC_HOOK_CODE, trace)
    try:
        executed = call(u, method - BASE, (sprite, CONTEXT), instruction_limit=500000)
    finally:
        u.hook_del(handle)
    assert len(events) == len(views) == 1
    assert not ({0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08} & executed)
    assert all(bytes(u.mem_read(a, 4)) == bytes(original.mem_read(a, 4)) for a in executed)
    return {'sprite': sprite, 'sprite_vtable': vtable, 'original_registered_callback': method,
            'actual_context': CONTEXT, 'actual_view_getter': views[0], 'draw': events[0],
            'full_return_stack_and_saved_register_ABI_pass': True,
            'all_executed_instruction_words_exact_clean': True,
            'actual_captured_resources_no_file_or_getter_bridge': True,
            'executed_instruction_addresses': sorted(executed)}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    digest = sha(ROM.read_bytes())
    assert digest == 'c4ff537ddcd4da5eb1743fb28cd0eb160492e9b660af080ddae44e94a9f4d95d'
    report_path = CAP / 'capture_report.json'
    report = read(report_path)
    assert report['ROM_sha256'] == digest and report['frames'] == 36000
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report.get('battery_save_preloaded')
    assert not any(v for k, v in report.items() if k.startswith('synthetic_'))
    assert report['scripted_input_schedule'] == read('work/analysis/town_force_texture_v544/map_inputs.json')
    for shot in report['frames_captured']:
        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
    snapshots = report['read_only_capture_RAM_snapshots']
    for snap in snapshots:
        assert sha(Path(snap['path']).read_bytes()) == snap['sha256']
    raw = (CAP / 'frame_036000_arm9_ram.bin').read_bytes()
    assert raw == (CAP / 'final_arm9_ram.bin').read_bytes()
    native = report['read_only_capture_native_states'][0]
    assert native['frame'] == 36000 and native['read_only_export'] and not native['state_loaded']
    assert native['serialized_RAM_matches_same_frame_direct_export'] and native['main_RAM_unchanged_by_export']
    assert sha(Path(native['path']).read_bytes()) == native['sha256']
    for region in native['regions'].values():
        assert sha(Path(region['path']).read_bytes()) == region['sha256']
    chain, seen = [], set()
    sprite = struct.unpack_from('<I', raw, CONTEXT - BASE + 20)[0]
    while sprite:
        assert sprite not in seen and len(seen) < 100
        assert BASE <= sprite <= BASE + len(raw) - 48
        seen.add(sprite)
        vtable, next_sprite = struct.unpack_from('<2I', raw, sprite - BASE)
        method = struct.unpack_from('<I', raw, vtable - BASE + 12)[0]
        chain.append({'sprite': sprite, 'vtable': vtable, 'registered_callback': method})
        sprite = next_sprite
    assert {0x0218BD0C, 0x0218C07C, 0x02190E80} <= seen
    callbacks = {
        'cursor': native_callback(rom, clean, raw, 0x0218BD0C),
        'marker': native_callback(rom, clean, raw, 0x0218C07C),
        'map': native_callback(rom, clean, raw, 0x02190E80),
    }
    specs = [('cursor', '/_pxl/__frame.pxl', 0x02313F60, (80, 32), (24, 24), 56, (128, 96)),
             ('marker', '/_pxl/__marker.pxl', 0x02313F74, (176, 96), (16, 16), 29, (124, 40))]
    overlays = []
    for label, path, owner, xy, size, bank, destination in specs:
        row, blob = callbacks[label], rom.read_file(path)
        draw, view = row['draw'], row['actual_view_getter']
        assert draw['source_xy'] == list(xy) and draw['source_size'] == list(size)
        assert draw['palette_bank'] == bank and draw['destination_point'] == list(destination)
        assert draw['screen_selector'] == 0
        assert view['words'][3] == owner and view['words'][7:9] == list(xy)
        assert view['words'][10:12] == list(size) and view['words'][9] & 0xFFFF == bank
        name_pointer = struct.unpack_from('<I', raw, owner - BASE + 12)[0]
        filename = raw[name_pointer - BASE:].split(b'\0')[0].decode('ascii')
        assert '/' + filename == path
        assert raw[draw['header'] - BASE:draw['header'] - BASE + len(blob)] == blob
        asset, source = PxlImage.from_bytes(blob), PxlImage.from_bytes(clean.read_file(path))
        palette = struct.unpack_from('<16H', blob, 20 + bank * 32)
        assert blob[20 + bank * 32:52 + bank * 32] == source.source[20 + bank * 32:52 + bank * 32]
        pixels = []
        for y in range(size[1]):
            for x in range(size[0]):
                index = asset.indices[(xy[1] + y) * asset.width + xy[0] + x]
                assert index == source.indices[(xy[1] + y) * source.width + xy[0] + x]
                pixels.append(palette[index] & 32767)
        assert palette[0] & 32767 == 0
        overlays.append({'label': label, 'file': path, 'file_sha256': sha(blob), 'owner': owner,
                         'actual_initialized_owner_filename_field': filename,
                         'entire_resident_file_matches_ROM': True,
                         'actual_source_origin': list(xy), 'actual_source_size': list(size),
                         'actual_palette_bank': bank, 'actual_destination_point': list(destination),
                         'all_selected_original_indices_and_palette_exact': True,
                         'pixels': pixels})
    map_draw = callbacks['map']['draw']
    assert map_draw['header'] == 0x02279B38 and map_draw['source_xy'] == [0, 0]
    assert map_draw['source_size'] == [244, 160] and map_draw['destination_point'] == [6, 16]
    assert map_draw['palette_bank'] == 0 and map_draw['screen_selector'] == 0
    header = map_draw['header'] - BASE
    assert struct.unpack_from('<5I', raw, header) == (4, 61, 160, 20, 52)
    palette = struct.unpack_from('<16H', raw, header + 20)
    indices = [n for b in raw[header + 52:header + 52 + 19520] for n in (b & 15, b >> 4)]
    base_pixels = [palette[n] & 32767 for n in indices]
    expected = base_pixels.copy()
    # Positions come from executed registered callbacks, independently of image fitting.
    for row in overlays:
        width, height = row['actual_source_size']
        dx, dy = [a - b for a, b in zip(row['actual_destination_point'], map_draw['destination_point'], strict=True)]
        for y in range(height):
            for x in range(width):
                color = row['pixels'][y * width + x]
                if color:
                    expected[(dy + y) * 244 + dx + x] = color
    shot = next(r for r in report['frames_captured'] if r['frame'] == 36000 and 'final' in r['path'])
    image = Image.open(shot['path']).convert('RGB')
    actual = [color5(image.getpixel((x + 6, y + 208))) for y in range(160) for x in range(244)]
    assert expected == actual
    assert sum(a != b for a, b in zip(base_pixels, actual, strict=True)) == 281
    vram = Path(native['regions']['LCDM']['path']).read_bytes()
    actual_vram = [struct.unpack_from('<H', vram, 0x60000 + 2 * ((y + 16) * 256 + x + 6))[0] & 32767
                   for y in range(160) for x in range(244)]
    assert actual_vram == actual
    historical_folder = Path('E:/Rota Nova translations/Generated/work/emulation_v193/worldmap_source_v551')
    historical_report = read(historical_folder / 'capture_report.json')
    historical_shots = {r['frame']: r for r in historical_report['frames_captured']}
    current_shots = {r['frame']: r for r in report['frames_captured']}
    regression = []
    for frame in (34800, 35200, 35600, 36000):
        old_shot, current_shot = historical_shots[frame], current_shots[frame]
        assert sha(Path(old_shot['path']).read_bytes()) == old_shot['PNG_sha256']
        assert Image.open(old_shot['path']).convert('RGB').tobytes() == Image.open(current_shot['path']).convert('RGB').tobytes()
        regression.append({'frame': frame, 'historical_PNG_sha256': old_shot['PNG_sha256'],
                           'current_PNG_sha256': current_shot['PNG_sha256'],
                           'complete98304_two_screen_pixels_exact': True})
    seaarea = rom.read_file('/_pxl/seaarea.pxl')
    assert seaarea == clean.read_file('/_pxl/seaarea.pxl')
    source_indices = [n for b in seaarea[276 + 7 * 19520:276 + 8 * 19520] for n in (b & 15, b >> 4)]
    assert all(a == b or a == 0 for a, b in zip(indices, source_indices, strict=True))
    assert sum(bool(n) for n in indices) == 9674
    proof = {
        'candidate': str(ROM), 'candidate_sha256': digest,
        'report': str(report_path), 'report_sha256': sha(report_path.read_bytes()),
        'RAM_sha256': sha(raw), 'native_export_sha256': native['sha256'],
        'ordinary_current_ROM_no_preloaded_save_no_fixtures_no_savestate': True,
        'original_registered_cursor_marker_and_map_callbacks': callbacks,
        'actual_captured_renderer_sprite_chain': chain,
        'all3_callbacks_full_ABI_and_executed_instructions_exact_clean': True,
        'all_resident_source_files_and_actual_original_owner_filename_bindings_verified': True,
        'native_source_crops_palettes_and_destination_points_not_chosen_from_fitted_pixels': True,
        'original_overlay_sources': [{k: v for k, v in r.items() if k != 'pixels'} for r in overlays],
        'complete_actual_composite_pixels': len(actual), 'prior281_unexplained_overlay_points_resolved': True,
        'complete_actual_physical_VRAM_crop_pixels': len(actual_vram),
        'all4_complete_current_and_historical_two_screen_regressions': regression,
        'historical_report': str(historical_folder / 'capture_report.json'),
        'historical_report_sha256': sha((historical_folder / 'capture_report.json').read_bytes()),
        'software_screen_selector0_not_assumed_to_be_upper_screen': True,
        'actual_dynamic_map_source_page': 7, 'nonzero_source_exact_pixels': 9674,
        'mask_creation_other_pages_and_sepia_legacy_use_remain_open': True,
        'diagnostic_whole_chain_last_background_call_failed_not_counted_as_passing':
            str(ROOT / 'registered_sprite_probe.json'),
        'scripts': {str(p): sha(p.read_bytes()) for p in [Path(__file__), Path('scripts/probe_worldmap_overlays_v638.py')]},
        'ROM_patch_registry_canonical_changed': False,
        'all18_plaques_remain_incomplete_all22_scopes_retained': True,
        'hardware_device_verification': False, 'full_goal_complete': False,
    }
    save(ROOT / 'native_composition_proof.json', proof)
    print('Three original registered painters pass ABI/source checks;281 overlay points resolved;39040 whole actual map composite and39040 VRAM pixels exact.')


if __name__ == '__main__':
    main()
