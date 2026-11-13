"""Bind complete duel names to original getters, source cells and actual pixels."""

import struct
from pathlib import Path

from PIL import Image
from unicorn import UC_HOOK_CODE, UC_HOOK_MEM_WRITE
from unicorn.arm_const import (
    UC_ARM_REG_PC,
    UC_ARM_REG_R0,
    UC_ARM_REG_R1,
    UC_ARM_REG_R2,
    UC_ARM_REG_R3,
    UC_ARM_REG_R4,
    UC_ARM_REG_R5,
    UC_ARM_REG_R6,
    UC_ARM_REG_R7,
    UC_ARM_REG_R8,
    UC_ARM_REG_R9,
    UC_ARM_REG_R10,
    UC_ARM_REG_R11,
    UC_ARM_REG_SP,
)

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_battle_fixture_v645 import apply_fixture
from scripts.probe_button_prompt_native import BASE, STACK, call, machine
from scripts.verify_regional_ui_v616 import native5
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/battle_selection_v645')
CAP = Path('E:/Rota Nova translations/Generated/work/emulation_v193/battle_selection_v645_actual')
ROM = Path('out/all_routes_combined_v640_candidate.nds')
DUEL, VIEW, HEADER, PIXELS = 0x0218D4D8, 0x0218D6BC, 0x022BD83C, 0x022BFDD0
LOWER, UPPER, SURFACE_BYTES = 0x022E1794, 0x022F9794, 98304
CONTEXT, TABLE, PALETTE = 0x023117AC, 0x02114580, 0x02125A20
NAMES = ('Hodram', 'Speyer')
CODE_RANGES = ((0xD028, 0xD208), (0xD700, 0xD79C), (0xCFC14, 0xCFDFC), (0x7EAF4, 0x7EB24),
               (0x1371C, 0x13734), (0xCB184, 0xCB190))


def state(arm, raw, itcm):
    u = machine(arm)
    u.mem_write(BASE, raw)
    assert len(itcm) == 32768
    u.mem_write(0x01FF0000, itcm)
    u.mem_write(0x01FF8000, itcm)
    return u


def word(u, address):
    return struct.unpack('<I', u.mem_read(address, 4))[0]


def source_mask(font):
    result = bytearray(256 * 24)
    for row, name in enumerate(NAMES):
        for index, ch in enumerate(name):
            glyph = font.decode(ch)
            for y in range(11):
                for x in range(6):
                    if glyph.getpixel((x, y)):
                        result[(row * 12 + y) * 256 + index * 6 + x] = 1
    return bytes(result)


def actual_source(u):
    packed = bytes(u.mem_read(PIXELS, 464 * 96 // 2))
    return bytes((packed[(y * 464 + x) // 2] >> (4 * (x % 2))) & 15
                 for y in range(24) for x in range(256))


def original_names(arm, raw, itcm):
    u = state(arm, raw, itcm)
    call(u, 0xCB184, ())
    people = u.reg_read(UC_ARM_REG_R0)
    opponent = word(u, DUEL + 0x38)
    opponent_id, remainder = divmod(opponent - people - 4, 32)
    assert (opponent_id, remainder) == (29, 0)
    assert word(u, VIEW + 0x10) == HEADER
    assert struct.unpack('<6I', u.mem_read(VIEW + 0x18, 24)) == (0, 0, 0, 0, 256, 24)
    assert struct.unpack('<3I', u.mem_read(HEADER, 12)) == (4, 116, 96)
    assert (HEADER + word(u, HEADER + 12)) & 0xFFFFFFFF == PALETTE
    assert HEADER + word(u, HEADER + 16) == PIXELS
    before = bytes(u.mem_read(PIXELS, 464 * 96 // 2))
    # Reconstruct through the original name setup, original character getters,
    # original text-object constructor and original painter. No string is supplied.
    glyphs, executed = [], set()

    def trace(cpu, address, size, unused):
        executed.add(address)
        if address == BASE + 0xD16B4:
            code, color = struct.unpack('<2I', cpu.mem_read(cpu.reg_read(UC_ARM_REG_SP), 8))
            glyphs.append((code, color, cpu.reg_read(UC_ARM_REG_R2), cpu.reg_read(UC_ARM_REG_R3)))

    u.reg_write(UC_ARM_REG_SP, STACK)
    u.mem_write(STACK + 0x14, struct.pack('<I', opponent_id))
    saved = {r: 0xB6451000 + i for i, r in enumerate((UC_ARM_REG_R4, UC_ARM_REG_R6,
        UC_ARM_REG_R7, UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_R11))}
    for r, v in saved.items():
        u.reg_write(r, v)
    u.reg_write(UC_ARM_REG_R10, DUEL)
    u.reg_write(UC_ARM_REG_R5, 0)
    hook = u.hook_add(UC_HOOK_CODE, trace)
    try:
        u.emu_start(BASE + 0xD700, BASE + 0xD79C, count=2000000)
    finally:
        u.hook_del(hook)
    assert u.reg_read(UC_ARM_REG_PC) == BASE + 0xD79C
    assert u.reg_read(UC_ARM_REG_SP) == STACK
    assert all(u.reg_read(r) == v for r, v in saved.items())
    assert u.reg_read(UC_ARM_REG_R10) == DUEL and u.reg_read(UC_ARM_REG_R5) == 0
    assert {BASE + x for x in (0xD393C, 0xD5160, 0x1371C, 0x7EAF4, 0xD5404, 0xD16B4)} <= executed
    expected = [(ord(ch), 1, index * 6, row * 12)
                for row, name in enumerate(NAMES) for index, ch in enumerate(name)]
    assert glyphs == expected
    assert bytes(u.mem_read(PIXELS, len(before))) == before
    for address in executed:
        source = (itcm[(address & 32767):(address & 32767) + 4]
                  if 0x01FF0000 <= address < BASE else raw[address - BASE:address - BASE + 4])
        assert bytes(u.mem_read(address, 4)) == source
    return u, {'source_opponent_id_from_original_people_table': opponent_id,
        'actual_getters_and_original_name_setup_executed_no_supplied_strings': True,
        'complete_glyph_calls': glyphs, 'whole_22272_byte_canvas_unchanged_by_native_name_refresh': True,
        'source_fragment_0200D700_to_0200D79C_register_and_stack_contract_passes': True,
        'all_executed_words_match_actual_RAM_or_ITCM': True,
        'executed_instruction_addresses': sorted(executed)}


def paint_names(arm, raw, itcm, erase=None):
    u = state(arm, raw, itcm)
    if erase is not None:
        row, source_x = erase
        for y in range(row * 12, row * 12 + 12):
            address = PIXELS + (y * 464 + source_x) // 2
            u.mem_write(address, bytes(3))
    source = actual_source(u)
    palette = struct.unpack('<16H', u.mem_read(PALETTE, 32))
    assert palette[0] == 0 and palette[1] == 0xF39C
    assert word(u, word(u, CONTEXT) + 12) == BASE + 0xCFC14
    descriptors = struct.unpack('<14i', u.mem_read(TABLE, 56))
    assert descriptors == (-1, 156, 82, 0, 0, 96, 12, -1, 4, 82, 0, 12, 96, 12)
    guards = bytes(u.mem_read(LOWER - 16, 16)), bytes(u.mem_read(UPPER + SURFACE_BYTES, 16))
    u.mem_write(LOWER, b'\xA5' * SURFACE_BYTES * 2)
    calls = []

    def trace(cpu, address, size, unused):
        if address == 0x01FF92D8:
            sp = cpu.reg_read(UC_ARM_REG_SP)
            size_ptr, dest_ptr = struct.unpack('<2I', cpu.mem_read(sp, 8))
            calls.append({'screen': cpu.reg_read(UC_ARM_REG_R0),
                'source_header': cpu.reg_read(UC_ARM_REG_R1), 'palette_bank': cpu.reg_read(UC_ARM_REG_R2),
                'source': list(struct.unpack('<2i', cpu.mem_read(cpu.reg_read(UC_ARM_REG_R3), 8))),
                'size': list(struct.unpack('<2i', cpu.mem_read(size_ptr, 8))),
                'destination': list(struct.unpack('<2i', cpu.mem_read(dest_ptr, 8)))})

    # Use the actual screen, source header and palette in the original caller.
    hook = u.hook_add(UC_HOOK_CODE, trace)
    u.mem_write(STACK, bytes(12))
    try:
        executed = call(u, 0xCFC14, (CONTEXT, VIEW, TABLE, 2), instruction_limit=1000000)
    finally:
        u.hook_del(hook)
    assert len(calls) == 2
    expected = bytearray(b'\xA5' * SURFACE_BYTES * 2)
    for row, dx in ((0, 156), (1, 4)):
        assert calls[row]['source'] == [0, row * 12]
        assert calls[row]['size'] == [96, 12] and calls[row]['destination'] == [dx, 82]
        assert calls[row]['source_header'] == HEADER and calls[row]['palette_bank'] == 0
        assert calls[row]['screen'] == 0
        for y in range(12):
            for x in range(96):
                index = source[(row * 12 + y) * 256 + x]
                if index:
                    struct.pack_into('<H', expected, ((82 + y) * 256 + dx + x) * 2, palette[index])
    result = bytes(u.mem_read(LOWER, SURFACE_BYTES * 2))
    assert result == expected
    assert bytes(u.mem_read(LOWER - 16, 16)) == guards[0]
    assert bytes(u.mem_read(UPPER + SURFACE_BYTES, 16)) == guards[1]
    assert actual_source(u) == source
    for address in executed:
        original = (itcm[(address & 32767):(address & 32767) + 4]
                    if 0x01FF0000 <= address < BASE else raw[address - BASE:address - BASE + 4])
        assert bytes(u.mem_read(address, 4)) == original
    return result, {'original_two_native_name_draws': calls,
        'all196608_output_bytes_match_independent_transparent_source_copy': True,
        'source_and_adjacent_guards_unchanged_full_native_ABI_passes': True,
        'original_source_destinations_and_complete96x12_crops_used': True}


def original_frame_and_names(arm, raw, itcm, rom):
    u = state(arm, raw, itcm)
    source_before = bytes(u.mem_read(PIXELS, 464 * 96 // 2))
    # Resolve the actual cached Frame owner, not a supplied bitmap or getter.
    call(u, 0xD6558, (0x02313F60,))
    frame_header = u.reg_read(UC_ARM_REG_R0)
    frame_file = rom.read_file('/_pxl/__frame.pxl')
    assert bytes(u.mem_read(frame_header, len(frame_file))) == frame_file
    u.mem_write(LOWER, b'\xA5' * SURFACE_BYTES * 2)
    guards = bytes(u.mem_read(LOWER - 16, 16)), bytes(u.mem_read(UPPER + SURFACE_BYTES, 16))
    writes, executed = set(), set()

    def written(cpu, kind, address, size, value, unused):
        if LOWER <= address < UPPER + SURFACE_BYTES:
            writes.update(range(address, address + size))

    u.reg_write(UC_ARM_REG_R0, DUEL)
    u.reg_write(UC_ARM_REG_R1, CONTEXT)
    u.reg_write(UC_ARM_REG_SP, STACK)
    hook = u.hook_add(UC_HOOK_CODE, lambda cpu, p, s, d: executed.add(p))
    wh = u.hook_add(UC_HOOK_MEM_WRITE, written)
    try:
        # The original draw prefix paints portrait frames, stat frames, name
        # frames and both names. The following GPU setup/3D work is not run.
        u.emu_start(BASE + 0xD028, BASE + 0xD208, count=5000000)
    finally:
        u.hook_del(hook)
        u.hook_del(wh)
    assert u.reg_read(UC_ARM_REG_PC) == BASE + 0xD208
    assert u.reg_read(UC_ARM_REG_SP) == STACK - 0xF0
    assert u.reg_read(UC_ARM_REG_R10) == DUEL and u.reg_read(UC_ARM_REG_R9) == CONTEXT
    for row, dx in ((0, 156), (1, 4)):
        for y in range(12):
            for x in range(96):
                address = LOWER + ((82 + y) * 256 + dx + x) * 2
                assert {address, address + 1} <= writes
    assert bytes(u.mem_read(LOWER - 16, 16)) == guards[0]
    assert bytes(u.mem_read(UPPER + SURFACE_BYTES, 16)) == guards[1]
    assert bytes(u.mem_read(PIXELS, len(source_before))) == source_before
    assert not ({BASE + p for p in (0xDED50, 0xDEBDC, 0xDEB70, 0xDED08)} & executed)
    for address in executed:
        source = (itcm[(address & 32767):(address & 32767) + 4]
                  if 0x01FF0000 <= address < BASE else raw[address - BASE:address - BASE + 4])
        assert bytes(u.mem_read(address, 4)) == source
    return bytes(u.mem_read(LOWER, SURFACE_BYTES)), {
        'fragment': [BASE + 0xD028, BASE + 0xD208],
        'actual_cached_Frame_header': frame_header, 'actual_cached_whole_Frame_file_sha256': sha(frame_file),
        'both_complete_namefields_fully_written_after_destination_poisoning': True,
        'original_border_background_and_transparent_name_composition_no_finished_output_input': True,
        'all_executed_words_match_actual_RAM_or_ITCM_source_names_and_guards_unchanged': True,
        'no_loader_or_getter_bridge_GPU_or_portrait_3D_composition_claim': True,
        'whole_parent_function_ABI_not_claimed_from_prefix': True}


def main():
    pre = read(ROOT / 'preflight.json')
    for path, digest in pre['release_hashes'].items():
        assert sha(Path(path).read_bytes()) == digest
    report_path = CAP / 'capture_report.json'
    report = read(report_path)
    assert report['ROM_sha256'] == pre['candidate_sha256']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['frames'] == 22001
    donor = report['battery_save_preloaded']
    assert sha(Path(donor['source']).read_bytes()) == donor['source_sha256']
    fixtures = report['synthetic_battle_recovery_proximity_fixtures']
    assert len(fixtures) == 1 and fixtures[0]['frame'] == 21200
    assert fixtures[0]['action'] == 'recover_and_approach'
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    for start, end in CODE_RANGES:
        assert arm[start:end] == clean[start:end]
    assert arm[0x114580:0x1145B8] == clean[0x114580:0x1145B8]
    assert clean[0x15D864:0x15D874].split(b'\0')[0].decode('cp932') == 'シュパイヤー'
    assert arm[0x15D864:0x15D874].split(b'\0')[0] == b'Speyer'
    assert b'Spever\0' not in arm
    before = (CAP / 'frame_021200_arm9_ram.bin').read_bytes()
    after, fixture = apply_fixture(arm, before, 'recover_and_approach')
    assert fixture['before_RAM_sha256'] == fixtures[0]['before_RAM_sha256']
    assert sha(after) == fixtures[0]['after_RAM_sha256']
    assert fixture['changes'] == fixtures[0]['changes'] and len(fixture['owned_bytes']) == 12
    rejected = []
    for name, code, ram, action in (
        ('wrong ARM', arm[:-1] + bytes([arm[-1] ^ 1]), before, 'recover'),
        ('wrong RAM size', arm, before[:-1], 'recover'),
        ('boolean action', arm, before, True), ('unknown action', arm, before, 'victory')):
        try:
            apply_fixture(code, ram, action)
        except ValueError:
            rejected.append(name)
        else:
            raise AssertionError(name)
    font, shots = GameAsciiFont.from_arm9(arm), {s['frame']: s for s in report['frames_captured']}
    mask, cases = source_mask(font), []
    for frame in (22000, 22001):
        native_path = CAP / f'native_state_{frame:06d}/native_state.json'
        # Native export at22000 is sufficient only for that frame. Every tested
        # RAM is paired to its own export, never a later cache that could be reused.
        if frame == 22001:
            native_path = Path(report['read_only_native_state']['path'])
        native = read(native_path)
        assert native['read_only_export'] and not native['state_loaded']
        assert native['main_RAM_unchanged_by_export'] and native['serialized_RAM_matches_same_frame_direct_export']
        for item in native['regions'].values():
            assert sha(Path(item['path']).read_bytes()) == item['sha256']
        raw = (CAP / f'frame_{frame:06d}_arm9_ram.bin').read_bytes()
        itcm = Path(native['regions']['ITCM']['path']).read_bytes()
        u, named = original_names(arm, raw, itcm)
        assert actual_source(u) == mask
        shot = shots[frame]
        assert sha(Path(shot['path']).read_bytes()) == shot['PNG_sha256']
        im = native5(Image.open(shot['path']))
        composition, composed = original_frame_and_names(arm, raw, itcm, rom)
        flat_black_errors = 0
        for row, dx in ((0, 156), (1, 4)):
            for y in range(12):
                for x in range(96):
                    value = struct.unpack_from('<H', composition, ((82 + y) * 256 + dx + x) * 2)[0]
                    expected = tuple((value >> shift) & 31 for shift in (0, 5, 10))
                    assert im.getpixel((dx + x, 192 + 82 + y)) == expected
                    # Independent full glyph cells, including every blank cell.
                    assert (expected == (28, 28, 28)) == bool(mask[(row * 12 + y) * 256 + x])
                    flat = (28, 28, 28) if mask[(row * 12 + y) * 256 + x] else (0, 0, 0)
                    flat_black_errors += expected != flat
        assert flat_black_errors > 0  # Original source fill is dark gray, not zero black.
        out, paint = paint_names(arm, raw, itcm)
        negatives = []
        for row, sx, label in ((0, 0, 'Hodram first H'), (0, 30, 'Hodram last m'),
                               (1, 0, 'Speyer first S'), (1, 30, 'Speyer last r')):
            control, _ = paint_names(arm, raw, itcm, (row, sx))
            count = sum(out[i:i + 2] != control[i:i + 2] for i in range(0, len(out), 2))
            assert count == sum(mask[(row * 12 + y) * 256 + sx + x] for y in range(12) for x in range(6)) > 0
            negatives.append({'label': label, 'whole_frame_changed_pixels': count})
        y, v = font.decode('y'), font.decode('v')
        delta = [(xx, yy) for yy in range(11) for xx in range(6) if y.getpixel((xx, yy)) != v.getpixel((xx, yy))]
        assert len(delta) == 4
        assert all((im.getpixel((4 + 18 + xx, 192 + 82 + yy)) == (28, 28, 28)) == bool(y.getpixel((xx, yy)))
                   for xx, yy in delta)
        cases.append({'frame': frame, 'PNG': shot, 'RAM_sha256': sha(raw),
            'native_state': str(native_path), 'native_state_sha256': sha(native_path.read_bytes()),
            'name_setup': named, 'native_painter': paint, 'original_composition': composed,
            'rejected_initial_flat_black_background_assumption_pixels': flat_black_errors,
            'complete_source_cells_verified': len(mask),
            'complete_actual_namefield_pixels_verified': 2304, 'all_four_first_final_deletions_rejected': negatives,
            'all_four_y_not_v_distinguishing_pixels_visible_correctly': True})
    assert len(cases) == 2
    result = {'candidate': str(ROM), 'candidate_sha256': pre['candidate_sha256'],
        'report': str(report_path), 'report_sha256': sha(report_path.read_bytes()),
        'battle_fixture': fixtures[0], 'fixture_negative_controls_rejected': rejected,
        'cases': cases, 'source_Japanese_surname': 'シュパイヤー', 'localized_surname': 'Speyer',
        'no_spelling_or_graphics_change_needed_original_font_y_is_complete': True,
        'battle_radial_Functions_is_Load_Quit_Game_Options_actual_observation_only': True,
        'miniature_Confirm_ordinary_parents_remain_open_no_global_nonuse_claim': True,
        'scripts': {p: sha(Path(p).read_bytes()) for p in (
            'scripts/native_battle_fixture_v645.py', 'scripts/run_battle_selection_v645.py', str(Path(__file__)))},
        'no_ROM_patch_registry_or_release_pointer_changes': True, 'full_goal_complete': False}
    save(ROOT / 'battle_name_proof.json', result)
    print('V645 original name setup and actual complete namefield pixels pass; no spelling/graphics repair needed.')


if __name__ == '__main__':
    main()
