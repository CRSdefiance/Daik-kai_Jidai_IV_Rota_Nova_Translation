"""Current village backdrop selectors and actual Narvik source/painter evidence."""

import struct
from pathlib import Path

from ndspy.code import loadOverlayTable
from PIL import Image
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_SP,
)

from dk4tool.graphics.pxl import PxlImage
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_village_backgrounds_v643 import relocate
from scripts.probe_button_prompt_native import BASE, STACK, call, machine
from scripts.probe_worldmap_overlays_v638 import color5
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/village_backgrounds_v643')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/village_backgrounds_v643_narvik')
ROM = Path('out/all_routes_combined_v640_candidate.nds')
CONTEXT, SPRITE, HEADER, DEST = 0x023117AC, 0x02192274, 0x022A554C, 0x022E1794


def native_selector_cases(arm, clean_arm, raw):
    u, original = machine(arm), machine(clean_arm)
    u.mem_write(BASE, raw)
    all_executed, rows = set(), []

    def get(offset, args=()):
        executed = call(u, offset, args)
        assert all(bytes(u.mem_read(a, 4)) == bytes(original.mem_read(a, 4)) for a in executed)
        all_executed.update(executed)
        return u.reg_read(UC_ARM_REG_R0)

    store = get(0xCB178)
    for village in range(24):
        town = village + 90
        record = store + 4 + town * 108
        vt = struct.unpack('<I', u.mem_read(record, 4))[0]
        name_method = struct.unpack('<I', u.mem_read(vt + 8, 4))[0]
        name_pointer = get(name_method - BASE, (record,))
        name = bytes(u.mem_read(name_pointer, 96)).split(b'\0')[0].decode('ascii')
        metadata = get(0xB5690, (record,))
        offset = metadata - BASE
        assert 0 <= offset <= len(arm) - 116
        assert bytes(u.mem_read(metadata, 116)) == arm[offset:offset + 116]
        assert arm[offset + 20] == clean_arm[offset + 20] == 0
        predicate = get(0xB521C, (record,))
        assert predicate == 0
        values = [get(0xB7294, (town, context)) for context in range(12)]
        assert len(set(values)) == 1 and values[0] in (43, 44, 48)
        rows.append({'village': village, 'town_ID': town, 'name': name,
                     'original_B521C_metadata_predicate': predicate,
                     'original_ROM_metadata_address': metadata,
                     'whole116_byte_runtime_metadata_record_exact_current_ROM': True,
                     'readonly_metadata_flag20_exact_clean_zero_not_development': True,
                     'all12_supplied_context_selector_results': values,
                     'town_background_file': f'/towngrp/towngrp{values[0]:02d}.pxl',
                     'not24_ordinary_village_visits_or_a_global_card_exclusion': True})
    return rows, sorted(all_executed)


def backdrop(rom, clean, raw, blob):
    source = PxlImage.from_bytes(blob)
    assert (source.width, source.height, source.bits_per_pixel) == (256, 192, 8)
    h = HEADER - BASE
    assert struct.unpack_from('<5I', raw, h) == (0x108, 128, 192, 40, 552)
    assert raw[h + 40:h + 552] == blob[20:532]
    assert raw[h + 552:h + 552 + 49152] == bytes(source.indices)
    resident = raw.find(blob)
    assert resident >= 0 and raw.find(blob, resident + 1) == -1
    node = struct.unpack_from('<I', raw, CONTEXT - BASE + 20)[0]
    chain, seen = [], set()
    while node:
        assert node not in seen and len(seen) < 100
        seen.add(node)
        vt, following = struct.unpack_from('<2I', raw, node - BASE)
        method = struct.unpack_from('<I', raw, vt - BASE + 12)[0]
        chain.append({'sprite': node, 'callback': method})
        node = following
    assert next(r for r in chain if r['sprite'] == SPRITE)['callback'] == 0x020B78A8
    arm = rom.read_file('/__arm9__.bin')
    u, original = machine(arm), machine(clean.read_file('/__arm9__.bin'))
    u.mem_write(BASE, raw)
    for image, cpu in ((rom, u), (clean, original)):
        overlay = loadOverlayTable(image.rom.arm9OverlayTable, lambda i, f, image=image: image.files[f])[0]
        cpu.mem_write(overlay.ramAddress, bytes(overlay.data))
    # Only a copy is poisoned; the live emulator and source palette/pixels are not modified.
    before, after = bytes(u.mem_read(DEST - 16, 16)), bytes(u.mem_read(DEST + 98304, 16))
    u.mem_write(DEST, b'\xA5' * 98304)
    views, draws, writes = [], [], []

    def words(address, n=2):
        return list(struct.unpack(f'<{n}I', u.mem_read(address, n * 4)))

    def code(cpu, address, size, unused):
        if address == 0x020D4170:
            view = cpu.reg_read(UC_ARM_REG_R0)
            views.append({'view': view, 'words': words(view, 12)})
        if address == 0x01FF92D8:
            screen, header, bank, xy = [cpu.reg_read(r) for r in
                (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)]
            size_pointer, destination = words(cpu.reg_read(UC_ARM_REG_SP))
            draws.append({'screen_selector': screen, 'header': header, 'palette_bank': bank,
                          'source_xy': words(xy), 'source_size': words(size_pointer),
                          'destination_point': words(destination)})

    def write(cpu, access, address, size, value, unused):
        if not STACK - 4096 <= address < STACK:
            writes.append((address, size, value))

    h1, h2 = u.hook_add(UC_HOOK_CODE, code), u.hook_add(UC_HOOK_MEM_WRITE, write)
    try:
        executed = call(u, 0xB78A8, (SPRITE, CONTEXT), instruction_limit=500000)
    finally:
        u.hook_del(h1)
        u.hook_del(h2)
    assert len(views) == len(draws) == 1
    assert views[0]['words'][3:5] == [CONTEXT, HEADER]
    assert draws == [{'screen_selector': 0, 'header': HEADER, 'palette_bank': 0,
        'source_xy': [0, 0], 'source_size': [256, 192], 'destination_point': [0, 0]}]
    assert len(writes) == 49152
    assert [(a, n) for a, n, _ in writes] == [(DEST + 2 * i, 2) for i in range(49152)]
    palette = struct.unpack_from('<256H', blob, 20)
    expected = b''.join(struct.pack('<H', palette[i]) for i in source.indices)
    assert bytes(u.mem_read(DEST, 98304)) == expected
    assert bytes(u.mem_read(DEST - 16, 16)) == before and bytes(u.mem_read(DEST + 98304, 16)) == after
    assert bytes(u.mem_read(HEADER, 552 + 49152)) == raw[h:h + 552 + 49152]
    assert all(bytes(u.mem_read(a, 4)) == bytes(original.mem_read(a, 4)) for a in executed)
    assert not ({0x020DED50, 0x020DEBDC, 0x020DEB70, 0x020DED08} & executed)
    return {'entire_unique_resident_source_file_address': BASE + resident,
        'entire_source_palette512_bytes_and_native49152_indices_exact': True,
        'actual_chain': chain, 'view': views[0], 'draw': draws[0],
        'actual_native_destination': DEST, 'all49152_full16bit_palette_words_exact_including_high_bit': True,
        'destination_poisoned_adjacent_guards_source_palette_and_pixels_preserved': True,
        'full_return_stack_saved_register_ABI_and_all_executed_code_words_clean': True,
        'no_file_getter_source_or_painter_bridge': True, 'executed_instruction_addresses': sorted(executed)}


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    rom, clean = NdsImage.open(ROM), NdsImage.open('work/clean.nds')
    arm, clean_arm = rom.read_file('/__arm9__.bin'), clean.read_file('/__arm9__.bin')
    for row in pre['all10_original_source_ranges']:
        lo, hi = row['offset']
        assert arm[lo:hi] == clean_arm[lo:hi]
    path = CAP / 'capture_report.json'
    run = read(path)
    assert run['ROM_sha256'] == pre['candidate_sha256'] and run['frames'] == 15700
    assert run['cold_boot'] and not run['savestate_loaded'] and not run['callback_errors']
    assert run['scripted_input_schedule'] == read(ROOT / 'complete_replay_inputs.json')
    donor = run['battery_save_preloaded']
    assert donor['source_sha256'] == pre['donor_sha256'] == sha(Path(donor['source']).read_bytes())
    assert donor['copied_byte_exact_before_cold_boot']
    assert not any(v for k, v in run.items() if k.startswith('synthetic_') and k != 'synthetic_location_fixtures')
    shots = {r['frame']: r for r in run['frames_captured']}
    for r in run['frames_captured']:
        assert sha(Path(r['path']).read_bytes()) == r['PNG_sha256']
    snapshots = {r['frame']: r for r in run['read_only_capture_RAM_snapshots'] + run['read_only_pause_RAM_snapshots']}
    for r in snapshots.values():
        assert r['read_only_export'] and sha(Path(r['path']).read_bytes()) == r['sha256']
    initial = Path(snapshots[5200]['path']).read_bytes()
    _, fixture = relocate(arm, initial, 15)
    assert run['synthetic_location_fixtures'] == [{'frame': 5200, **fixture}]
    assert fixture['expected_selector_point_after_original_update'] == [22048, 2234]
    rows, selector_code = native_selector_cases(arm, clean_arm, initial)
    sources = {}
    for i in (43, 44, 48):
        name = f'/towngrp/towngrp{i:02d}.pxl'
        assert rom.read_file(name) == clean.read_file(name)
        sources[name] = sha(rom.read_file(name))
    old_path = Path(pre['historical_report'])
    assert sha(old_path.read_bytes()) == pre['historical_report_sha256']
    old = {s['frame']: s for s in read(old_path)['frames_captured']}
    comparisons = []
    for frame in sorted(shots.keys() & old.keys()):
        assert sha(Path(old[frame]['path']).read_bytes()) == old[frame]['PNG_sha256']
        a, b = Image.open(shots[frame]['path']).convert('RGB'), Image.open(old[frame]['path']).convert('RGB')
        assert a.size == b.size == (256, 384) and a.tobytes() == b.tobytes()
        comparisons.append({'frame': frame, 'whole98304_pixels_exact': True,
                            'current_PNG': shots[frame], 'historical_PNG': old[frame]})
    assert len(comparisons) == 54
    development, absent = [], []
    for frame, value in ((7200, 0), (11800, 0), (12600, 2), (15700, 2)):
        raw = Path(snapshots[frame]['path']).read_bytes()
        u = machine(arm)
        u.mem_write(BASE, raw)
        call(u, 0xCB178, ())
        town = u.reg_read(UC_ARM_REG_R0) + 4 + 105 * 108
        call(u, 0xB50D8, (town,))
        assert u.reg_read(UC_ARM_REG_R0) == value
        call(u, 0xB7294, (105, 0))
        assert u.reg_read(UC_ARM_REG_R0) == 48
        development.append({'frame': frame, 'actual_town105_development': value,
                             'original_town_background_selector_result': 48})
        assert all(raw.find(rom.read_file(f'/evstill/evstill{i:03d}.pxl')) < 0
                   for i in (168, 169, 170, 171, 206, 207, 208, 209))
        absent.append(frame)
    final = Path(snapshots[15700]['path']).read_bytes()
    painted = backdrop(rom, clean, final, rom.read_file('/towngrp/towngrp48.pxl'))
    assert {r['frame'] for r in run['read_only_capture_native_states']} == {7200, 8000, 12600, 15700}
    for state in run['read_only_capture_native_states']:
        assert state['read_only_export'] and not state['state_loaded'] and state['main_RAM_unchanged_by_export']
        assert state['serialized_RAM_matches_same_frame_direct_export']
        assert sha(Path(state['path']).read_bytes()) == state['sha256']
        for region in state['regions'].values():
            assert sha(Path(region['path']).read_bytes()) == region['sha256']
    native = next(r for r in run['read_only_capture_native_states'] if r['frame'] == 15700)
    assert native['read_only_export'] and not native['state_loaded'] and native['main_RAM_unchanged_by_export']
    assert native['serialized_RAM_matches_same_frame_direct_export']
    for r in native['regions'].values():
        assert sha(Path(r['path']).read_bytes()) == r['sha256']
    vram = Path(native['regions']['LCDM']['path']).read_bytes()
    im = Image.open(shots[15700]['path']).convert('RGB')
    assert [struct.unpack_from('<H', vram, 0x60000 + 2 * i)[0] & 32767 for i in range(49152)] == [
        color5(im.getpixel((i % 256, i // 256 + 192))) for i in range(49152)]
    proof = {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'report': str(path), 'report_sha256': sha(path.read_bytes()), 'fixture': fixture,
        'source_background_files_exact_clean': sources, 'all24_original_village_background_selectors': rows,
        'all288_supplied_context_calls_full_ABI_and_clean_executed_code': selector_code,
        'actual_Narvik_development_and_background_selection': development,
        'actual_complete_original_Narvik_backdrop_painter': painted,
        'all54_complete_current_and_historical_two_screen_comparisons': comparisons,
        'all5308416_two_screen_comparison_pixels_exact': True,
        'all49152_actual_lower_VRAM_pixels_exact_to_capture': True,
        'source_plane_not_an_independent_reconstruction_of_all_final_UI_overlays': True,
        'sampled_complete_village_cards_absent_frames_not_global_unused_claim': absent,
        'undeveloped_menu_retains_Sea_View_developed_port_uses_towngrp48': True,
        'whole_chain_diagnostics_not_credited_as_complete': [
            str(ROOT / p) for p in ('complete_chain_diagnostic.json', 'expanded_chain_diagnostic.json', 'font_chain_failure_detail.json')],
        'next_concrete_chain_dependency': {'reader_PC': 0x01FF9470, 'unmapped_CPU_VRAM_address': 0x0601BFC8,
            'requires_actual_bank_alias_data_before_whole_chain_credit': True},
        'ordinary_village_cards_miniature_Confirm_and_wider_graphics_scope_still_open': True,
        'all18_original_plaques_incomplete_all22_historical_scopes_retained': True,
        'ROM_patch_registry_canonical_and_all_release_pointers_unchanged': True,
        'normal_long_distance_travel_all24_village_visits_or_hardware_not_claimed': True,
        'full_goal_complete': False, 'scripts': {str(p): sha(p.read_bytes()) for p in (
            Path(__file__), Path('scripts/native_village_backgrounds_v643.py'),
            Path('scripts/run_village_backgrounds_v643.py'), Path('scripts/headless_desmume_v193.py'))}}
    save(ROOT / 'native_background_proof.json', proof)
    print('288 original selector calls;full49152 source palette-word backdrop;54 whole two-screen regressions;Narvik0-to2 development passes. Other card/whole-chain contexts remain open.')


if __name__ == '__main__':
    main()
