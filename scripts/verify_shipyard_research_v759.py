"""Verify the non-release Yard prototype against native buffer/font contracts."""

import struct
from itertools import product
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import (UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1,
                              UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_R6, UC_ARM_REG_R8,
                              UC_ARM_REG_R9, UC_ARM_REG_R10, UC_ARM_REG_SP)

from dk4tool.dialogue.font_audit import GameAsciiFont, SJIS_GLYPH_COUNT, SJIS_MAP_OFFSET, decode_glyph
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, call, machine
from scripts.probe_shipyard_layout_v759 import number, units
from scripts.probe_shipyard_runtime_v759 import (CURRENT, ROOT, NUMERIC_RAM, QUANTITY, PRICE_RETURNS,
                                               DAY_RETURN, assemble, loaded)
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_market_balanced_owners_v757 import scope_output
from scripts.verify_village_wrap_v608 import read, save

DEST = ROOT / 'typed_literal_runtime_RESEARCH'


def quantity_buffer_contract(arm, blobs):
    rows, ka = [], Ks(KS_ARCH_ARM, KS_MODE_ARM)
    for ret, n in product((*PRICE_RETURNS, DAY_RETURN), (0, 1, 2, 9, 10, 16, 99, 1000, 65535, 1000000, 2147483647)):
        machines = [loaded(arm, blobs), loaded(arm, blobs)]
        pointers, outputs = [], []
        for u, target in zip(machines, (BASE + 0xABF50, QUANTITY), strict=True):
            thunk = 0x02464000
            u.mem_write(thunk, bytes(ka.asm(f'ldr lr,[pc,#0]; b {target}; .word {ret}', thunk)[0]))
            u.mem_write(ret, bytes(ka.asm('b 0x027e0000', ret)[0]))
            call(u, thunk - BASE, (n,))
            ptr = u.reg_read(UC_ARM_REG_R0)
            pointers.append(ptr)
            outputs.append(bytes(u.mem_read(ptr, 80)).split(b'\0')[0])
        assert outputs[0] == number(n)
        suffix = (' day' if n == 1 else ' days') if ret == DAY_RETURN else (' gold coin' if n == 1 else ' gold coins')
        assert outputs[1] == outputs[0] + suffix.encode('ascii')
        start = pointers[0] + len(outputs[0]) - 127
        assert start <= pointers[1] < pointers[0] < start + 128
        before, after = [bytes(u.mem_read(BASE, 0x400000)) for u in machines]
        lo, hi = start - BASE, start + 128 - BASE
        assert before[:lo] == after[:lo] and before[hi:] == after[hi:]
        rows.append({'return_PC': ret, 'value': n, 'existing_native_buffer': [start, start + 128],
                     'all4MiB_RAM_equal_outside_original128_byte_numeric_buffer': True,
                     'fullwidth_digits_suffix_and_ABI_exact': True})
    return rows


def source_copy_arguments(arm, blobs):
    rows, ka = [], Ks(KS_ARCH_ARM, KS_MODE_ARM)
    for days, amount, supplied_name in product((0, 1, 2, 16), (1, 50000), ('Vestaros', 'FALCON', 'ICARUS')):
        u = loaded(arm, blobs)
        for ret in (*PRICE_RETURNS, DAY_RETURN):
            u.mem_write(ret - 4, bytes(ka.asm(f'bl {QUANTITY}', ret - 4)[0]))
        model, vt, getter, name = 0x02450000, 0x02451000, 0x02452000, 0x02453000
        u.mem_write(model, struct.pack('<I', vt))
        u.mem_write(vt + 4, struct.pack('<I', getter))
        u.mem_write(name, supplied_name.encode('ascii') + b'\0')
        u.reg_write(UC_ARM_REG_SP, STACK)
        u.emu_start(BASE + 0x63038, BASE + 0x63044, count=10)
        assert struct.unpack('<I', u.mem_read(STACK + 0x18, 4))[0] == 804
        for reg, value in ((UC_ARM_REG_R6, model), (UC_ARM_REG_R8, amount),
                           (UC_ARM_REG_R9, 0x02454000), (UC_ARM_REG_R10, 0x02455000)):
            u.reg_write(reg, value)
        observed = []
        def watch(cpu, at, size, unused):
            if at in (BASE + 0x62B8C, getter):
                cpu.reg_write(UC_ARM_REG_R0, days if at == BASE + 0x62B8C else name)
                cpu.reg_write(UC_ARM_REG_PC, cpu.reg_read(UC_ARM_REG_LR))
            elif at == BASE + 0x53F9C:
                selected = cpu.reg_read(UC_ARM_REG_R1)
                pointers = [cpu.reg_read(UC_ARM_REG_R2), cpu.reg_read(UC_ARM_REG_R3)]
                if selected == 803:
                    pointers.append(struct.unpack('<I', cpu.mem_read(STACK, 4))[0])
                observed.append((selected, [bytes(cpu.mem_read(p, 80)).split(b'\0')[0] for p in pointers]))
                cpu.emu_stop()
        h = u.hook_add(UC_HOOK_CODE, watch)
        try:
            u.emu_start(BASE + 0x63114, 0x027E0000, count=10000)
        finally:
            u.hook_del(h)
        expected = [supplied_name.encode('ascii'), number(amount) + (b' gold coin' if amount == 1 else b' gold coins')]
        if days:
            expected.append(number(days) + (b' day' if days == 1 else b' days'))
        assert observed == [(803 if days else 804, expected)], observed
        rows.append({'days_supplied_at_preparation_boundary': days, 'price_input': amount, 'tagged_name_getter': supplied_name,
                     'original_selected_message': observed[0][0], 'argument_hex': [v.hex() for v in expected],
                     'actual_original_numeric_calls_execute_typed_adapter_then_native_ABF50': True})
    return rows


def inherited(arm, blobs):
    rows = []
    for index, (parent, n, text) in enumerate(product(
            (0x02054014, 0x02053FCC, 0x02054044, 0x02053D24, 0x02053DB8),
            (676, 677, 761, 767, 768, 769, 770, 388, 1000),
            ('A clear sentence.', 'An ordinary paragraph with several words to check wrapping and complete letters.',
             "A longer ordinary sentence needs a natural ending, so let's check every line and the final words.",
             'Here is one more ordinary paragraph. It has a few short words and a longer final sentence.'))):
        old = machine(arm)
        old.mem_write(BASE, NUMERIC_RAM.read_bytes())
        new = loaded(arm, blobs)
        for u in (old, new):
            u.mem_write(STACK + 0x27C, struct.pack('<I', 0x021184C0))
        a, b = [scope_output(u, text.encode('ascii'), n, (), parent) for u in (old, new)]
        assert a == b, (parent, n, text, a, b)
        rows.append({'parent': parent, 'message_ID': n, 'input': text, 'complete_native_output_and_ABI_equal': True})
    return rows


def font_planes(arm, cases):
    font = GameAsciiFont.from_arm9(arm)
    mapping = struct.unpack_from(f'<{SJIS_GLYPH_COUNT}H', arm, SJIS_MAP_OFFSET)
    kanji = NdsImage.open(CURRENT).read_file('/GRP/KANJI.FNT')
    assert kanji == NdsImage.open('out/all_routes_combined_v255_candidate.nds').read_file('/GRP/KANJI.FNT')
    seen, previews = set(), []
    for case in cases:
        lines = case['lines']
        shape = (case['id'], len(lines), tuple(len(t.encode('cp932')) % 2 for t in lines))
        name = bytes.fromhex(case['values_hex'][0]) if case['id'] in (803, 804) else b''
        marker = ('literal_name', case['id'], name) if name in (b'FALCON', b'ICARUS', b'FIONA', b'FORTUNE', b'FURY') else None
        if shape in seen and (marker is None or marker in seen):
            continue
        seen.add(shape)
        if marker:
            seen.add(marker)
        raw = bytes.fromhex(case['formatted_hex'])
        events = []
        pixels = raster(arm, raw, 0x01FFCE40 - BASE, size=(228, 64), instruction_limit=1000000, glyph_events=events)
        assert [e['code'] for e in events if e['code'] != 32] == [c for c, _ in units(raw)]
        expected = bytearray(228 * 64)
        for row, line in enumerate(lines):
            x = 6
            for char in line:
                code = char.encode('cp932')
                glyph = font.decode(char) if len(code) == 1 else decode_glyph(kanji, mapping.index(int.from_bytes(code, 'big')))
                if len(code) == 2:
                    # Original Shift-JIS style1 draws the source bitmap in
                    # colour1 and its (1,1) shadow in colour15. ASCII has its
                    # separate renderer. Preserve the full indexed plane.
                    for y in range(11):
                        for dx in range(glyph.width):
                            if glyph.getpixel((dx, y)):
                                assert dx < 11 and x + dx + 1 < 228 and row * 16 + y + 1 < 64
                                expected[(row * 16 + y + 1) * 228 + x + dx + 1] = 15
                for y in range(11):
                    for dx in range(glyph.width):
                        if glyph.getpixel((dx, y)):
                            assert x + dx < 228 and row * 16 + y < 64
                            expected[(row * 16 + y) * 228 + x + dx] = 1
                x += 6 * len(code)
        assert pixels == bytes(expected), (case['id'], lines)
        path = DEST / f'complete_font_{len(previews):03d}_ID{case["id"]}.png'
        Image.frombytes('L', (228, 64), bytes(0 if p else 255 for p in pixels)).save(path)
        previews.append({**case, 'preview': str(path), 'sha256': sha(path.read_bytes()),
                         'complete_independent_ASCII_KANJI_glyph_plane_equal': True,
                         'all_visible_lines_start_at_x6_with_complete_first_and_final_glyphs': True})
    for start in range(0, len(previews), 12):
        group = previews[start:start + 12]
        sheet = Image.new('RGB', (1404, 4 * 175), '#30343c')
        draw = ImageDraw.Draw(sheet)
        for i, row in enumerate(group):
            x, y = i % 3 * 468, i // 3 * 175
            draw.text((x + 4, y + 2), f"RESEARCH {row['id']} / {row['lines'][-1]}", fill='white')
            sheet.paste(Image.open(row['preview']).convert('RGB').resize((456, 128), Image.Resampling.NEAREST), (x + 4, y + 22))
        sheet.save(DEST / f'font_review_{start // 12 + 1:02d}.png')
    return previews


def main():
    arm = NdsImage.open(CURRENT).read_file('/__arm9__.bin')
    blobs = assemble(arm)
    frozen = read(DEST / 'research_code.json')
    assert frozen['blobs'] == {hex(a): b.hex() for a, b in blobs.items()}
    assert frozen['producer_sha256'] == sha(Path('scripts/probe_shipyard_runtime_v759.py').read_bytes())
    matrix = read(DEST / 'native_layout_matrix.json')
    assert matrix['count'] == 1124 and matrix['findings_count'] == 0
    report = {'typed_buffer_contracts': quantity_buffer_contract(arm, blobs),
              'original_copy_argument_fragments': source_copy_arguments(arm, blobs),
              'complete_inherited_output_controls': inherited(arm, blobs),
              'full_font_planes': font_planes(arm, matrix['cases']),
              'native_matrix_sha256': sha((DEST / 'native_layout_matrix.json').read_bytes()),
              'producer_sha256': sha(Path(__file__).read_bytes()),
              'research_only_storage_ownership_integration_and_actual_gameplay_pending': True}
    save(DEST / 'verification.json', report)
    print(f"{len(report['typed_buffer_contracts'])} complete 4MiB buffer comparisons; {len(report['original_copy_argument_fragments'])} original copy fragments; {len(report['complete_inherited_output_controls'])} inherited outputs; {len(report['full_font_planes'])} complete font planes. No ROM emitted.", flush=True)


if __name__ == '__main__':
    main()
