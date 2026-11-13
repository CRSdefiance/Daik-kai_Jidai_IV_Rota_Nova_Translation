"""Real COMMON cache -> scoped PIC component -> complete original duel fonts.

CPU research only: file open/read, SDK bitmap clear, UI registration and GPU
submission are explicit boundaries. Original table selection, copy, printf,
macro, cache-range loops, compiled layout and both font painters execute.
"""
from pathlib import Path
import struct

from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2,
                               UC_ARM_REG_R3, UC_ARM_REG_SP, UC_ARM_REG_LR,
                               UC_ARM_REG_PC)
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.duel_postmacro_layout_v1134 import layout
from scripts.probe_duel_cache_scope_v1150 import pipeline, PLAN_PATH, BASE, CACHE
from scripts.probe_duel_compiled_fonts_v1136c import expected_plane
from scripts.probe_button_prompt_native import STACK
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/duel_resident_fonts_v1151')
TABLES = {'challenge': 0x02117340, 'acceptance': 0x02117360, 'threat': 0x021174E0}


def execute(arm, common, raw, actor, name, family, table, number, text, font, kanji):
    cpu, get, state = pipeline(arm, common, raw)
    controller, argument = 0x02460000, 0x02469000
    widget = controller + 0x214
    cpu.mem_write(controller, bytes(0x600))
    cpu.mem_write(controller + 0x34, struct.pack('<2I', actor, actor))
    cpu.mem_write(argument, name + b'\0')
    get(0xE14C, widget)

    def bypass(u):
        u.reg_write(UC_ARM_REG_PC, u.reg_read(UC_ARM_REG_LR))

    registration = []

    def register(u, pc, size, unused):
        assert u.reg_read(UC_ARM_REG_R0) == widget
        registration.append(widget)
        bypass(u)

    hook = cpu.hook_add(UC_HOOK_CODE, register, begin=BASE+0xD351C, end=BASE+0xD351C)
    try:
        get(0xDEF4, widget)
    finally:
        cpu.hook_del(hook)
    view = widget + 0x3C
    header = struct.unpack('<I', cpu.mem_read(view+16, 4))[0]
    h = struct.unpack('<5I', cpu.mem_read(header, 20))
    assert h[:3] == (4, 52, 36)
    assert struct.unpack('<2I', cpu.mem_read(view+40, 8)) == (208, 36)
    rectangle = struct.unpack('<4i', cpu.mem_read(widget+32, 16))
    assert rectangle == (52, 16, 204, 80)
    pixels, count = (header+h[4]) & 0xFFFFFFFF, 208*36//2
    guards = [(pixels-16, bytes(cpu.mem_read(pixels-16, 16))),
              (pixels+count, bytes(cpu.mem_read(pixels+count, 16)))]
    clears, draw, events = [], {}, []
    output, lines = layout(text)

    def clear(u, pc, size, unused):
        image, color, point, extent = [u.reg_read(r) for r in
            (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)]
        assert image == header and color == 0
        assert struct.unpack('<2i', u.mem_read(point, 8)) == (0, 0)
        assert struct.unpack('<2i', u.mem_read(extent, 8)) == (208, 36)
        assert struct.unpack('<5I', u.mem_read(image, 20)) == h
        u.mem_write(pixels, bytes(count))
        clears.append(header)
        bypass(u)

    def entry(u, pc, size, unused):
        context, pointer = u.reg_read(UC_ARM_REG_R0), u.reg_read(UC_ARM_REG_R1)
        before = state['front'][-1]
        assert before['expanded_hex'] == text.hex() and before['eligible']
        assert state['active'] and context == before['context'] and pointer == before['pointer']
        assert bytes(u.mem_read(pointer, 1024)).split(b'\0')[0] == output
        assert context-pointer == 0x400
        x, y = struct.unpack('<2i', u.mem_read(context+36, 8))
        assert x == 0 and y == (12 if len(lines) == 1 else 0)
        draw.update(context=context, pointer=pointer, x=x, y=y)
        # Read-only assertion; execute the unmodified original painter.

    def glyph(u, pc, size, unused):
        code, style = struct.unpack('<2I', u.mem_read(u.reg_read(UC_ARM_REG_SP), 8))
        events.append({'kind': 'cp932' if pc == 0x01FF83AC else 'ascii',
            'code': code, 'style': style, 'x': u.reg_read(UC_ARM_REG_R2),
            'y': u.reg_read(UC_ARM_REG_R3)})
        if pc == 0x01FF83AC:
            assert struct.unpack('<I', u.mem_read(u.reg_read(UC_ARM_REG_R0)+12, 4))[0] == 0

    def painted(u, pc, size, unused):
        assert state['active']
        draw['consumed_bytes'] = u.reg_read(UC_ARM_REG_R0)-draw['pointer']

    # Both source painters and the whole cache component run without a host text
    # or Y substitution. Cache synchronization instructions have only their
    # hardware effects bridged by pipeline; all loop arithmetic executes.
    compiler = read('work/analysis/duel_layout_native_v1141b/compiler_provenance.json')
    from capstone import Cs, CS_ARCH_ARM, CS_MODE_THUMB
    binary = Path(compiler['binary']).read_bytes()
    callsite = [i for i in Cs(CS_ARCH_ARM, CS_MODE_THUMB).disasm(binary[:44], CACHE)
                if i.mnemonic in ('blx', 'bx') and i.op_str.startswith('r')]
    # duel_draw calls D5404 via BLX; derive its return, not an assumed offset.
    assert len(callsite) == 1 and callsite[0].mnemonic == 'blx'
    painter_return = callsite[0].address+callsite[0].size
    hooks = [cpu.hook_add(UC_HOOK_CODE, clear, begin=0x01FFB2DC, end=0x01FFB2DC),
        cpu.hook_add(UC_HOOK_CODE, entry, begin=BASE+0xD5404, end=BASE+0xD5404),
        cpu.hook_add(UC_HOOK_CODE, glyph, begin=BASE+0xD16B4, end=BASE+0xD16B4),
        cpu.hook_add(UC_HOOK_CODE, glyph, begin=0x01FF83AC, end=0x01FF83AC),
        cpu.hook_add(UC_HOOK_CODE, painted, begin=painter_return, end=painter_return)]
    cpu.mem_write(STACK, struct.pack('<I', argument))
    try:
        get(0xD458, controller, 0 if family == 'challenge' else 1, 60, table)
    finally:
        for hook in hooks:
            cpu.hook_del(hook)
    assert len(registration) == len(clears) == len(state['front']) == 1
    assert state['component_entries'] == state['component_returns'] == 1 and not state['active']
    assert [r['message_ID'] for r in state['gets']] == [number, 1931]
    assert len(state['data_lines']) == len(state['instruction_lines']) == state['drains'] == 47
    assert state['data_lines'] == state['instruction_lines']
    assert draw['consumed_bytes'] == len(output)
    assert bytes(cpu.mem_read(argument, len(name)+1)) == name+b'\0'
    assert bytes(cpu.mem_read(header, 20)) == struct.pack('<5I', *h)
    assert all(bytes(cpu.mem_read(at, len(value))) == value for at, value in guards)
    packed = bytes(cpu.mem_read(pixels, count))
    native = bytes((value >> shift) & 15 for value in packed for shift in (0, 4))
    expected, letters = expected_plane(arm, kanji, font, lines)
    assert [(e['kind'], e['code'], e['x'], e['y']) for e in events if e['code'] != 32] == letters
    assert all(e['style'] == 15 and 0 <= e['x'] and
        e['x']+(12 if e['kind'] == 'cp932' else 6) <= 144 and
        0 <= e['y'] and e['y']+12 <= 36 for e in events)
    assert native == bytes(expected)
    visible = bytes(native[y*208+x] for y in range(36) for x in range(144))
    assert sum(bool(v) for v in native) == sum(bool(v) for v in visible)
    requests = []

    def gpu(u, pc, size, unused):
        sizep, destination = struct.unpack('<2I', u.mem_read(u.reg_read(UC_ARM_REG_SP), 8))
        requests.append({'image': u.reg_read(UC_ARM_REG_R1),
            'source': list(struct.unpack('<2i', u.mem_read(u.reg_read(UC_ARM_REG_R3), 8))),
            'size': list(struct.unpack('<2i', u.mem_read(sizep, 8))),
            'destination': list(struct.unpack('<2i', u.mem_read(destination, 8)))})
        bypass(u)

    point, renderer = 0x02469100, 0x02469200
    cpu.mem_write(point, struct.pack('<2i', 52, 16))
    cpu.mem_write(renderer, struct.pack('<I', 0x0215FA94))
    cpu.mem_write(STACK, struct.pack('<3I', 0, point, 0))
    hook = cpu.hook_add(UC_HOOK_CODE, gpu, begin=0x01FF92D8, end=0x01FF92D8)
    try:
        get(0xCFC14, renderer, view, 0x0211460C, 3)
    finally:
        cpu.hook_del(hook)
    assert requests == [{'image': header, 'source': [0, i*12], 'size': [144, 12],
                         'destination': [56, 20+i*20]} for i in range(3)]
    return {'message_ID': number, 'family': family, 'actor_object': actor,
        'name_hex': name.hex(), 'expanded_hex': text.hex(), 'formatted_hex': output.hex(),
        'lines': lines, 'source_208x36_4bit_SHA256': sha(native),
        'visible_144x36_4bit_SHA256': sha(visible), 'full_font_ink': sum(bool(v) for v in native),
        'native_getter_IDs': [number, 1931], 'file_reads': state['file_provider'].reads,
        'native_cache_flush_and_invalidate_lines': state['data_lines'],
        'PIC_entry_return_and_no_reentry_or_code_writes_while_active': True,
        'original_painters_exact_to_independent_ASCII_CP932_shadow_and_layout': True,
        'full_first_last_glyphs_uniform_margins_no_overflow_or_crop_loss': True,
        'original_macro_printf_voice_copy_and_complete_stack_register_ABI_pass': True,
        'original_three144x12_crop_submissions_exact': True}, visible


def main():
    assert not ROOT.exists()
    plan = read(PLAN_PATH)
    arm, common = Path(plan['target_ARM9']).read_bytes(), Path(plan['target_COMMON']).read_bytes()
    assert sha(arm) == plan['target_ARM9_sha256'] and sha(common) == plan['target_COMMON_sha256']
    catalog = read('work/analysis/duel_scope_names_v1117b/source_name_layout_catalogue.json')
    raw = Path(catalog['snapshot']).read_bytes()
    assert sha(raw) == catalog['snapshot_sha256']
    rom = NdsImage.open(plan['source_ROM'])
    kanji = rom.read_file('/GRP/KANJI.FNT')
    assert sha(Path(plan['source_ROM']).read_bytes()) == plan['source_ROM_sha256']
    assert kanji == NdsImage.open('work/clean.nds').read_file('/GRP/KANJI.FNT')
    font_base = struct.unpack_from('<I', arm, 0xD19B8)[0]-BASE
    assert raw[font_base:font_base+len(kanji)] == kanji
    font = GameAsciiFont.from_arm9(arm)
    cpu, get = get_machine(arm, raw)
    representatives = {}
    for row in catalog['names']:
        for family, table in TABLES.items():
            number = get(0x53F4C, row['object'], table)
            representatives.setdefault(number, (family, table, row['object']))
    assert set(representatives) == set(range(1931, 1951))
    records = {r['message_id']: r for r in read('translations/duel_editorial_manuscript_v3.json')['records']}
    matrix_path = Path('work/analysis/duel_native_layout_v1134/compiled_native_DP_matrix.json')
    matrix = read(matrix_path)
    selected, seen = [], set()
    for row in matrix['cases']:
        key = row['message_ID'], row['input_hex']
        if key not in seen:
            seen.add(key)
            selected.append(row)
    assert len(selected) == 1356
    ROOT.mkdir(parents=True)
    results, previews = [], []
    for row in selected:
        number = row['message_ID']
        text = bytes.fromhex(row['input_hex'])
        template = records[number]['english'].encode('ascii')
        if b'%s' in template:
            prefix, suffix = template.split(b'%s')
            assert text.startswith(prefix) and text.endswith(suffix)
            name = text[len(prefix):len(text)-len(suffix)] if suffix else text[len(prefix):]
            assert template.replace(b'%s', name) == text
        else:
            assert template == text
            name = b'Clifford'
        family, table, actor = representatives[number]
        result, visible = execute(arm, common, raw, actor, name, family, table, number, text, font, kanji)
        assert result['formatted_hex'] == row['generated_hex']
        result['source_kind'] = row['kind']
        results.append(result)
        if number in (1931, 1933, 1938, 1944) and len(previews) < 12 and (
            row['kind'] == 'legal-name-stress' and not text.isascii() or
            row['kind'] == 'source' and (b'Clifford' in text or b'\x82\x65ernando' in text or number == 1944)):
            path = ROOT/f'resident_native_{len(previews):02d}_ID{number}.png'
            canvas = Image.new('RGB', (864, 198), '#263238')
            draw = ImageDraw.Draw(canvas)
            draw.text((4, 4), f'Real COMMON loader + resident PIC + original font/crops; CPU research; ID{number}', fill='white')
            im = Image.frombytes('L', (144, 36), bytes(255-v*17 for v in visible))
            canvas.paste(im.resize((864, 144), Image.Resampling.NEAREST), (0, 30))
            canvas.save(path)
            previews.append({'path': str(path), 'sha256': sha(path.read_bytes()), 'message_ID': number})
        if len(results) % 100 == 0:
            print(f'Resident scoped PIC + complete original fonts: {len(results)}/{len(selected)}', flush=True)
    proof = ROOT/'cache_resident_complete_fonts.json'
    save(proof, {'target_plan': str(PLAN_PATH), 'target_plan_sha256': sha(PLAN_PATH.read_bytes()),
        'ARM9_sha256': sha(arm), 'COMMON_sha256': sha(common), 'native_matrix': str(matrix_path),
        'unique_complete_font_cases': len(results), 'cases': results, 'research_previews': previews,
        'all1356_distinct_expansions_cover_all4700_source_and_legal_name_inputs': True,
        'original_COMMON_loader_voice_printf_macro_scoped_PIC_fonts_and_crops_execute': True,
        'all_cache_component_bytes_immutable_without_COMMON_reentry_until_return': True,
        'CPU_source_resident_ILNK_header_reopened_into_original_allocation': True,
        'boundaries': ['file open/read', 'SDK clear', 'UI registration', 'GPU submission', 'hardware MCR effects'],
        'native_DC_and_IC_range_loop_arithmetic_executes47_lines_each': True,
        'no_host_text_or_context_Y_replacement': True,
        'actual_emulator_cache_hardware_duel_dismissal_and_scene_transitions_pending': True,
        'no_playable_ROM_registry_or_completion_credit': True, 'all33_formatting_gates_remain_false': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    path = Path('translations/editorial_review_current_v1.json')
    ledger = read(path)
    assert ledger['records_editorially_completed'] == 1196 and ledger['records_with_source_and_prose_pass'] == 1267
    ledger['duel_prose_v1103'].update(cache_resident_complete_fonts=str(proof),
        formatting_status='real-cache-scoped-PIC-complete-fonts-pass;13-escape-integration-original-duel-scenes-open')
    save(path, ledger)
    print('1356 resident scoped PIC native font/crop cases pass; actual emulator and13 escape paragraphs remain open.', flush=True)


if __name__ == '__main__':
    main()
