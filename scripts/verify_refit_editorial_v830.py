"""Execute current native Refit fonts for every proposed editorial paragraph.

The captured help object and a supplied pixel allocation are controlled inputs.
This is not an emulator scene activation, native allocator or GPU proof.
"""

import struct
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R4, UC_ARM_REG_R5

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.refit_help import compile_paragraph
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.refit_help_layout_v2 import BASE, INIT_END, INIT_START
from dk4tool.rom.nds import NdsImage
from scripts.prepare_refit_editorial_v830 import MANUSCRIPT, ROM, ROOT
from scripts.probe_button_prompt_native import STOP, call, machine
from scripts.verify_village_wrap_v608 import read, save

PIXELS, TEXT = 0x02450020, 0x02440020


def main():
    manuscript = read(MANUSCRIPT)
    assert manuscript['current_candidate_sha256'] == sha(ROM.read_bytes())
    target = NdsImage.open(ROM).read_file('/__arm9__.bin')
    old = read('work/analysis/refit_help_v712/native_layout_proof.json')
    old_arm = Path('work/analysis/refit_help_v712/target_ARM9.bin').read_bytes()
    for lo, hi in old['layout']['owned_spans']:
        assert target[lo:hi] == old_arm[lo:hi], 'Refit constructor/crop ownership drift'
    events_path = Path(old['actual_V709_consumer_events'])
    row = read(events_path)['rows'][0]
    raw = Path(row['RAM']).read_bytes()
    assert sha(raw) == row['RAM_sha256']
    u = machine(target)
    u.mem_write(BASE, raw)
    # Install actual current static code/data over the supplied historical globals.
    for section in MainCodeFile(target, BASE).sections:
        u.mem_write(section.ramAddress, bytes(section.data))
    requests = []

    def bridge(uc, pc, size, data):
        if pc == 0x02005154:
            requests.append(uc.reg_read(UC_ARM_REG_R0))
            assert requests == [9072]
            uc.reg_write(UC_ARM_REG_R0, PIXELS)
            uc.reg_write(UC_ARM_REG_PC, uc.reg_read(UC_ARM_REG_LR))
        elif pc == BASE + INIT_END:
            uc.reg_write(UC_ARM_REG_PC, STOP)

    handle = u.hook_add(UC_HOOK_CODE, bridge)
    parent = 0x0218F790
    u.reg_write(UC_ARM_REG_R4, 1)
    u.reg_write(UC_ARM_REG_R5, parent)
    u.emu_start(BASE + INIT_START, STOP, count=10000)
    assert u.reg_read(UC_ARM_REG_PC) == STOP and requests == [9072]
    u.hook_del(handle)
    header, context = parent + 0x1C38, row['R0_context']
    assert struct.unpack('<3I', u.mem_read(header, 12)) == (4, 42, 108)
    assert (header + struct.unpack('<I', u.mem_read(header + 16, 4))[0]) & 0xFFFFFFFF == PIXELS
    u.mem_write(context + 16, struct.pack('<I', 108))
    prepared = bytes(u.mem_read(BASE, 0x400000))
    font = GameAsciiFont.from_arm9(target)
    results, panels = [], []
    previews = ROOT / 'native_previews'
    previews.mkdir(exist_ok=True)
    for record in manuscript['records']:
        u.mem_write(BASE, prepared)
        u.mem_write(PIXELS - 16, b'\xA5' * (9072 + 32))
        u.mem_write(PIXELS, bytes(9072))
        compiled, lines = compile_paragraph(record['english'])
        u.mem_write(TEXT - 16, b'\x5A' * (len(compiled) + 32))
        u.mem_write(TEXT, compiled)
        before = bytes(u.mem_read(BASE, 0x400000))
        executed = call(u, 0xD5404, (context, TEXT), instruction_limit=1000000)
        after = bytes(u.mem_read(BASE, 0x400000))
        assert all(context <= BASE + i < context + 72 for i, (a, b) in enumerate(zip(before, after)) if a != b)
        packed = bytes(u.mem_read(PIXELS, 9072))
        actual = bytes(n for value in packed for n in (value & 15, value >> 4))
        expected = bytearray(168 * 108)
        for line_index, line in enumerate(lines):
            for index, char in enumerate(line):
                glyph = font.decode(char)
                for y in range(11):
                    for x in range(6):
                        if glyph.getpixel((x, y)):
                            expected[(line_index * 12 + y) * 168 + index * 6 + x] = 1
        assert actual == expected
        assert all(v == 0 for v in actual[60 * 168:])
        assert bytes(u.mem_read(PIXELS - 16, 16)) == bytes(u.mem_read(PIXELS + 9072, 16)) == b'\xA5' * 16
        assert bytes(u.mem_read(TEXT - 16, 16)) == bytes(u.mem_read(TEXT + len(compiled), 16)) == b'\x5A' * 16
        assert bytes(u.mem_read(TEXT, len(compiled))) == compiled
        plane = Image.frombytes('L', (168, 108), actual).point(lambda v: 10 if v else 224).convert('RGB')
        path = previews / f"COMMON_{record['message_id']}_native.png"
        plane.save(path)
        panel = Image.new('RGB', (528, 240), '#263238')
        ImageDraw.Draw(panel).text((12, 10), f"COMMON {record['message_id']} / {record['editorial_decision']} / controlled native font", fill='white')
        panel.paste(plane.crop((0, 0, 168, 60)).resize((504, 180), Image.Resampling.NEAREST), (12, 40))
        panels.append(panel)
        results.append({'message_id': record['message_id'], 'English': record['english'], 'lines': lines,
                        'compiled_hex': compiled.hex(), 'full168x108_indices_sha256': sha(actual),
                        'native_preview': str(path), 'native_preview_sha256': sha(path.read_bytes()),
                        'complete_independent_font_plane_equal': True,
                        'all_body_rows_start_at_x0_and_fit_first60_rows': True,
                        'heading_and_three_detail_rows_blank_unmodified': True,
                        'text_and_pixel_guards_and_ABI_preserved': True,
                        'executed_instruction_addresses': sorted(executed)})
    sheets = []
    for start in range(0, len(panels), 8):
        selected = panels[start:start + 8]
        sheet = Image.new('RGB', (1056, 240 * ((len(selected) + 1) // 2)), '#172126')
        for index, panel in enumerate(selected):
            sheet.paste(panel, ((index % 2) * 528, (index // 2) * 240))
        path = ROOT / f'native_review_sheet_{start // 8 + 1}.png'
        sheet.save(path)
        sheets.append({'path': str(path), 'sha256': sha(path.read_bytes())})
    save(ROOT / 'native_font_verification.json', {
        'candidate': str(ROM), 'candidate_sha256': sha(ROM.read_bytes()),
        'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'captured_context_source': str(events_path), 'captured_RAM_sha256': sha(raw),
        'current_static_code_data_installed': True, 'supplied9072_byte_allocation': True,
        'current_frozen_refit_layout_owned_spans_equal': old['layout']['owned_spans'],
        'records': results, 'native_pixels_compared': len(results) * 168 * 108,
        'review_sheets': sheets, 'visual_review_pending': True,
        'actual_new_scene_activation_pending': True, 'registered_integration_pending': True,
        'scope': 'Controlled execution of current native font with supplied captured help-object globals. No new emulator scene, allocator, GPU or gameplay completion claim.',
        'verifier_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print('All31 current native fonts/independent complete planes/guards pass;four sheets await visual review.', flush=True)


if __name__ == '__main__':
    main()
