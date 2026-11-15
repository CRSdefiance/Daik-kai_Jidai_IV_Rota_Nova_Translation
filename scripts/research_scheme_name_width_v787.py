"""Native scheme-list width and row rendering; no release or GPU claim."""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP, UC_ARM_REG_LR

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import cache_plan
from dk4tool.rom.nds import NdsImage
from scripts.audit_item_runtime_storage_v785 import census, CURRENT
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/scheme_name_width_v787')
PRIOR = Path('work/analysis/item_diplomacy_context_v786')
WIDTH = 0x0209145C
WIDGET, IDS = 0x02460000, 0x02461000
HEADER, VIEW, CTX = 0x02450000, 0x02453000, 0x02454000
RAM = Path('E:/Rota Nova translations/Generated/work/emulation_v193/item_guild_v786/frame_003200_arm9_ram.bin')


def live(arm, widened):
    cpu = machine(arm)
    raw = RAM.read_bytes()
    assert sha(raw) == '4983f1b5bba0d2a570b4d432e902c19b345beb2cf16d392a80baf0190bacf079'
    cpu.mem_write(BASE, raw)
    # Preserve the live heap and globals. Reloading all static sections would
    # overwrite the startup stage that the game has already returned to its
    # heap. Only the guarded research deltas belong in this live snapshot.
    for path in ('work/analysis/item_diplomacy_runtime_v785/runtime_plan.json',
                 'work/analysis/item_diplomacy_context_v786/nominal_provider_research.json'):
        for row in read(path)['patches']:
            before, after = map(bytes.fromhex, (row['source_hex'], row['target_hex']))
            assert bytes(cpu.mem_read(row['address'], len(before))) == before
            cpu.mem_write(row['address'], after)
    if widened:
        assert bytes(cpu.mem_read(WIDTH, 4)) == struct.pack('<I', 0xE3A0000A)
        word = struct.unpack_from('<I', arm, WIDTH-BASE)[0]
        assert word in (0xE3A00017, 0xE3A00018)
        cpu.mem_write(WIDTH, struct.pack('<I', word))
    return cpu


def get(cpu, fn, args=()):
    call(cpu, fn, args, instruction_limit=1000000)
    return cpu.reg_read(UC_ARM_REG_R0)


def scheme(cpu, kind):
    root = get(cpu, 0xCB130)
    obj = root+4
    assert struct.unpack('<I', cpu.mem_read(obj, 4))[0] == 0x0214C618
    # One-byte native CPU input only; no real quest, letter or save is created.
    cpu.mem_write(obj+4, bytes([kind]))
    assert get(cpu, 0x211E4, (0x0D000000,)) == obj
    return obj


def widget(cpu):
    cpu.mem_write(WIDGET-16, b'\xa5'*0x2D0)
    cpu.mem_write(WIDGET, bytes(0x2B0))
    assert get(cpu, 0x4F500, (WIDGET,)) == WIDGET
    assert bytes(cpu.mem_read(WIDGET-16, 16)) == bytes(cpu.mem_read(WIDGET+0x2B0, 16)) == b'\xa5'*16


def geometry(arm, widened, count):
    cpu = live(arm, widened)
    scheme(cpu, 2)
    widget(cpu)
    cpu.mem_write(IDS, struct.pack('<'+'I'*count, *([0x0D000000]*count)))
    cpu.mem_write(STACK, struct.pack('<5I', 0, 0, 0, 0, 1))
    for reg, value in ((UC_ARM_REG_R0, WIDGET), (UC_ARM_REG_R1, IDS),
                       (UC_ARM_REG_R2, count), (UC_ARM_REG_R3, 0),
                       (UC_ARM_REG_SP, STACK), (UC_ARM_REG_LR, STOP)):
        cpu.reg_write(reg, value)
    seen = []
    def before_create(c, at, size, data):
        rectangle = struct.unpack('<4i', c.mem_read(c.reg_read(UC_ARM_REG_R3), 16))
        seen.append(rectangle)
        c.emu_stop()
    hook = cpu.hook_add(UC_HOOK_CODE, before_create, begin=0x0204F1EC, end=0x0204F1EC)
    try:
        cpu.emu_start(0x0204F0AC, STOP, count=100000)
    finally:
        cpu.hook_del(hook)
    assert len(seen) == 1
    x, y, right, bottom = seen[0]
    cells = (struct.unpack_from('<I', arm, WIDTH-BASE)[0] & 255) if widened else 10
    assert right-x == cells*6+16 and bottom-y == min(count, 10)*16+12
    assert 0 <= x < right <= 256 and 0 <= y < bottom <= 192
    # The original inner rectangle uses exactly the calculated content width,
    # not the outer frame's16 pixels of padding. Execute its pure arithmetic
    # fragment with the original padding literal, preserving the measured
    # width/row-height registers. Window allocation/drawing remains unmodeled.
    cpu.emu_start(0x0204F240, 0x0204F244, count=1)
    cpu.emu_start(0x0204F26C, 0x0204F270, count=1)
    cpu.emu_start(0x0204F278, 0x0204F27C, count=1)
    cpu.emu_start(0x0204F284, 0x0204F2AC, count=16)
    inner = struct.unpack('<4i', cpu.mem_read(cpu.reg_read(UC_ARM_REG_SP)+0x78, 16))
    assert inner[2]-inner[0] == cells*6 and inner[3]-inner[1] == min(count, 10)*16-4
    return {'width_cells': cells, 'count': count, 'rectangle': list(seen[0]),
        'original_inner_rectangle_fragment': list(inner),
        'source_constructor_and_resolver_virtual_width_loop_executed': True,
        'stopped_before_native_SDK_window_allocation': True}


def row(arm, widened, kind, height, text, diagnostic_wrap=False):
    cpu = live(arm, widened)
    obj = scheme(cpu, kind)
    cells = get(cpu, WIDTH-BASE, (obj,))
    visible_width = cells*6
    storage_width = (visible_width+3)//4*4
    length = storage_width*height//2
    original = struct.pack('<5I', 4, storage_width//4, height, 0x02452000-HEADER, 20)
    cpu.mem_write(HEADER-16, b'\xa5'*(20+length+32))
    cpu.mem_write(HEADER, original+bytes(length))
    cpu.mem_write(VIEW-16, b'\xa5'*80)
    get(cpu, 0xD3D80, (VIEW,))
    cpu.mem_write(STACK, struct.pack('<4I', visible_width, height, 0, 0))
    get(cpu, 0xD3AFC, (VIEW, HEADER, 0, 0))
    extent = struct.unpack('<2I', cpu.mem_read(VIEW+0x28, 8))
    assert extent == (visible_width, height)
    font = struct.unpack_from('<I', arm, 0xD5088)[0]
    cpu.mem_write(font+4, struct.pack('<2I', 6, 16))
    kanji = NdsImage.open(CURRENT).read_file('/GRP/KANJI.FNT')
    cpu.mem_write(struct.unpack_from('<I', arm, 0xD19B8)[0], kanji)
    get(cpu, 0xD5160, (CTX, VIEW, 1))
    # The real4FC70 row parent calls D5160,then sets the clip and invokes
    # virtual8C without enabling paragraph wrap. D5160/D5A98 initialize14=0.
    assert struct.unpack('<I', cpu.mem_read(CTX+0x14, 4))[0] == 0
    if diagnostic_wrap:
        get(cpu, 0xD5A10, (CTX, 1))
    widget(cpu)
    cpu.mem_write(IDS, struct.pack('<I', 0x0D000000))
    # Source-observed list fields: original native constructor, encoded-ID
    # source array and default renderer; no invented vtable or replacement draw.
    child = WIDGET+0x10
    child_vtable = struct.unpack('<I', cpu.mem_read(child, 4))[0]
    assert struct.unpack('<I', cpu.mem_read(child_vtable+0x8C, 4))[0] == 0x0204F8D4
    cpu.mem_write(child+0x74, struct.pack('<2I', IDS, 0))
    name_pointer = get(cpu, 0x93D5C, (kind,))
    end = get(cpu, 0x4F8D4, (child, 0, CTX))
    packed = bytes(cpu.mem_read(HEADER+20, length))
    pixels = bytes(n for value in packed for n in (value & 15, value >> 4))
    font_ref = GameAsciiFont.from_arm9(arm)
    expected = bytearray(storage_width*height)
    for index, char in enumerate(text):
        glyph = font_ref.decode(char)
        for y in range(min(height, 11)):
            for x in range(6):
                at_x = index*6+x
                if at_x < storage_width and glyph.getpixel((x, y)):
                    expected[y*storage_width+at_x] = 1
    assert bytes(cpu.mem_read(HEADER, 20)) == original
    assert bytes(cpu.mem_read(HEADER-16, 16)) == bytes(cpu.mem_read(HEADER+20+length, 16)) == b'\xa5'*16
    assert bytes(cpu.mem_read(VIEW-16, 16)) == bytes(cpu.mem_read(VIEW+48, 16)) == b'\xa5'*16
    complete = end-name_pointer == len(text) and pixels == bytes(expected)
    path = ROOT/f'{"dialogue_mode_DIAGNOSTIC" if diagnostic_wrap else "wide" if widened else "old"}_{cells}cells_type{kind}_height{height}.png'
    Image.frombytes('L', (storage_width, height), bytes(0 if p else 255 for p in pixels)).save(path)
    return {'type': kind, 'text': text, 'height': height, 'visible_width': visible_width,
        'storage_width': storage_width, 'returned_byte_count': end-name_pointer,
        'complete_native_row_and_independent_font_exact': complete,
        'native_list_wrap_flag': int(diagnostic_wrap), 'correct_native_child_vtable_row_slot': child_vtable+0x8C,
        'all_bitmap_and_view_guards_exact': True, 'PNG': str(path), 'PNG_sha256': sha(path.read_bytes())}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    source = (PRIOR/'NOMINAL_PROVIDER_RESEARCH_ONLY.bin').read_bytes()
    provider = read(PRIOR/'nominal_provider_research.json')
    assert sha(source) == provider['target_research_ARM9_sha256']
    rom = NdsImage.open(CURRENT)
    refs = census(rom, [[WIDTH, WIDTH+8]], [])
    assert refs == [['absolute', 'section0', 0x0214C624, WIDTH, False]], refs
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    assert source[WIDTH-BASE:WIDTH-BASE+8] == clean[WIDTH-BASE:WIDTH-BASE+8] == bytes.fromhex('0a00a0e31eff2fe1')
    texts = [r['text'] for r in provider['native_getter_cases'] if r['getter'] == 0x02093D5C]
    assert len(texts) == 10 and max(map(len, texts)) == 23
    target = bytearray(source)
    struct.pack_into('<I', target, WIDTH-BASE, 0xE3A00018)
    target = bytes(target)
    assert source[:WIDTH-BASE]+struct.pack('<I', 0xE3A00018)+source[WIDTH-BASE+4:] == target
    assert len(source) == len(target) and cache_plan(source) == cache_plan(target)
    (ROOT/'WIDTH_RESEARCH_ONLY.bin').write_bytes(target)
    geometry_cases = [geometry(raw, changed, n) for raw, changed in ((source, False), (target, True)) for n in (1, 10, 11)]
    rows = []
    for changed, arm in ((False, source), (True, target)):
        for height in (12, 16):
            for kind, text in enumerate(texts):
                result = row(arm, changed, kind, height, text)
                if changed:
                    assert result['complete_native_row_and_independent_font_exact'], result
                rows.append({'widened': changed, **result})
    bad = [r for r in rows if not r['widened'] and not r['complete_native_row_and_independent_font_exact']]
    assert {r['type'] for r in bad} == set(range(6)) | {7}, bad
    odd_width = bytearray(target)
    struct.pack_into('<I', odd_width, WIDTH-BASE, 0xE3A00017)
    odd_width = bytes(odd_width)
    odd = row(odd_width, True, 2, 12, texts[2])
    assert odd['returned_byte_count'] == len(texts[2]) and not odd['complete_native_row_and_independent_font_exact']
    diagnostic = row(odd_width, True, 2, 12, texts[2], diagnostic_wrap=True)
    assert not diagnostic['complete_native_row_and_independent_font_exact']
    source_spans = [(0x4F0AC, 0x4F32C), (0x4F500, 0x4F588), (0x4F708, 0x4F934),
                    (0x4FA84, 0x4FB5C), (0x4FB5C, 0x4FCEC), (0xD5160, 0xD51AC), (0xD5A98, 0xD5AE8)]
    assert all(source[lo:hi] == clean[lo:hi] for lo, hi in source_spans)
    save(ROOT/'native_width_verification.json', {'source_ARM9_sha256': sha(source), 'target_ARM9_sha256': sha(target),
        'one_existing_instruction_patch': {'address': WIDTH, 'source_hex': source[WIDTH-BASE:WIDTH-BASE+4].hex(),
                                          'target_hex': target[WIDTH-BASE:WIDTH-BASE+4].hex()},
        'sole_source_width_getter_reference': refs, 'derived_maximum_English_name_cells': 23,
        'reported_name_width_cells': 24, 'paired_blank_terminal_cell_reserved': 1,
        'actual_list_context_initializes_wrap_flag_zero': True,
        'odd23_cell_minimal_backing_surface_sensitivity': odd,
        'source_parent_and_context_spans': [{'span': [lo, hi], 'sha256': sha(source[lo:hi])} for lo, hi in source_spans],
        'initial_dialogue_wrap_setting_was_probe_error_not_a23_cell_game_defect': diagnostic,
        'all6_native_geometry_cases': geometry_cases, 'all40_original_list_row_bitmap_cases': rows,
        'old_width_reproduces_incomplete_rows_for_six_new_names_and_earlier_Forge_Papers': sorted({r['type'] for r in bad}),
        'new_width_all20_full_rows_exact': True,
        'native_widget_constructor_resolver_vtable_name_getter_default_row_and_SDK_font_executed': True,
        'declared_CPU_scheme_type_and_list_array_fixtures_not_earned_letters': True,
        'full_SDK_window_allocation_GPU_and_actual_menu_playback_pending': True,
        'explicit_width_override_callers_and_other_virtual_consumers_pending': True,
        'no_playable_ROM_COMMON_or_completion_credit': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    sheet = Image.new('RGB', (900, 10*72), '#30343c')
    draw = ImageDraw.Draw(sheet)
    for kind in range(10):
        draw.text((8, kind*72+3), f'{kind}: {texts[kind]} | old width / corrected width (native CPU)', fill='white')
        for x, changed in ((8, False), (200, True)):
            item = next(r for r in rows if r['type'] == kind and r['height'] == 16 and r['widened'] == changed)
            img = Image.open(item['PNG']).convert('RGB')
            sheet.paste(img.resize((img.width*3, img.height*3), Image.Resampling.NEAREST), (x, kind*72+20))
    sheet.save(ROOT/'old_and_corrected_name_rows_3x.png')
    print(f'Six original sizing cases and40 native list-row cases;old10-cell width truncates{len({r["type"] for r in bad})} names,new24-cell width preserves all10. Original wrap0,odd-pitch and wrong-mode diagnostics are separate. Actual UI playback remains.', flush=True)


if __name__ == '__main__':
    main()
