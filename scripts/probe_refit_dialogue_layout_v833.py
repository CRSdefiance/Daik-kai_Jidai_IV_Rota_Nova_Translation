"""Actual native quantities/printf/dispatch and independent complete font planes."""

import struct
from pathlib import Path

from keystone import Ks, KS_ARCH_ARM, KS_MODE_ARM
from PIL import Image, ImageDraw
from unicorn.arm_const import UC_ARM_REG_R0

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import refit_dialogue_runtime_v833 as runtime
from scripts.context_refit_dialogue_v832 import ROM
from scripts.native_call_abi_v764 import call
from scripts.probe_button_prompt_native import BASE, STACK, STOP
from scripts.review_refit_dialogue_v832 import MANUSCRIPT
from scripts.verify_arrival_native_v792 import prepared
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read, save

ROOT = runtime.ROOT
TEMPLATE, VALUE, PRINTF, WRAPPED = 0x02420000, 0x02421000, 0x02422020, 0x02423020


def main():
    rom = NdsImage.open(ROM)
    arm = (ROOT / 'ARM9_RESEARCH_ONLY.bin').read_bytes()
    proof = read(ROOT / 'native_runtime_verification.json')
    assert proof['research_ARM9_sha256'] == sha(arm)
    plan = read(ROOT / 'runtime_plan.json')
    raw_path = Path('work/emulation_v193/refit_editorial_v831_after/frame_020000_arm9_ram.bin')
    raw = raw_path.read_bytes()
    rows = read(MANUSCRIPT)['records']
    ka = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    matrix = []
    for row in rows:
        n = row['message_id']
        values = list(range(256)) + [999, 65535, 2147483647] if n == 1263 else list(range(256)) if n == 1267 else [None]
        for case_index, number in enumerate(values):
            if case_index % 32 == 0:
                cpu = prepared(arm)
                cpu.mem_write(BASE, raw)
                for patch in plan['patches']:
                    cpu.mem_write(patch['address'], bytes.fromhex(patch['target_hex']))
            template = b' ' + row['english'].encode('ascii')
            cpu.mem_write(TEMPLATE, template + b'\0')
            args = []
            value = None
            if number is not None:
                if n == 1267:
                    thunk = 0x02464000
                    cpu.mem_write(thunk, bytes(ka.asm(f'ldr lr,[pc,#0];b {runtime.QUANTITY};.word {runtime.NEW_DAY_RETURN}', thunk)[0]))
                    cpu.mem_write(runtime.NEW_DAY_RETURN, bytes(ka.asm(f'b {STOP}', runtime.NEW_DAY_RETURN)[0]))
                    call(cpu, thunk - BASE, (number,))
                else:
                    call(cpu, 0xABF50, (number,))
                pointer = cpu.reg_read(UC_ARM_REG_R0)
                value = bytes(cpu.mem_read(pointer, 100)).split(b'\0')[0]
                cpu.mem_write(VALUE, value + b'\0')
                args = [VALUE]
            cpu.mem_write(PRINTF - 16, b'\xA5' * 288)
            call(cpu, 0xD7720, (PRINTF, TEMPLATE, *args))
            expected = template % ((value,) if value is not None else ())
            result = bytes(cpu.mem_read(PRINTF, 256)).split(b'\0')[0]
            assert result == expected
            assert bytes(cpu.mem_read(PRINTF - 16, 16)) == bytes(cpu.mem_read(PRINTF + 256, 16)) == b'\xA5' * 16
            assert bytes(cpu.mem_read(TEMPLATE, len(template) + 1)) == template + b'\0'
            parent = 0x02053DB8 if n <= 1262 else 0x02054014
            for off, v in ((0x264, parent), (0x274, n), (0x27C, 0x02118680 if n <= 1262 else 0)):
                cpu.mem_write(STACK + off, struct.pack('<I', v))
            cpu.mem_write(WRAPPED - 16, b'\x5A' * 288)
            call(cpu, 0x01FFCF3C - BASE, (WRAPPED, PRINTF, 0), instruction_limit=2000000)
            formatted = bytes(cpu.mem_read(WRAPPED, 256)).split(b'\0')[0]
            assert b' '.join(formatted.split()) == b' '.join(expected.split()), (n, number, formatted, expected)
            assert bytes(cpu.mem_read(WRAPPED - 16, 16)) == bytes(cpu.mem_read(WRAPPED + 256, 16)) == b'\x5A' * 16
            assert bytes(cpu.mem_read(PRINTF, len(expected) + 1)) == expected + b'\0'
            lines = [line.strip().decode('cp932') for line in formatted.split(b'\n')]
            lengths = [len(line.encode('cp932')) for line in lines]
            assert 1 <= len(lines) <= 4 and max(lengths) <= 35
            findings = []
            if len(lines) > 1 and len(lines[-1].split()) == 1:
                findings.append('single_word_final_row')
            if any(line.split()[-1].strip('.,!?;:').lower() in {'a', 'an', 'the', 'to', 'of', 'with', 'for', 'from'} for line in lines[:-1]):
                findings.append('weak_line_end')
            matrix.append({'message_id': n, 'number': number, 'native_argument_hex': value.hex() if value else None,
                           'formatted_hex': formatted.hex(), 'lines': lines, 'line_byte_counts': lengths,
                           'findings': findings, 'actual_parent': parent,
                           'native_printf_quantities_and_complete_word_and_guard_ABI_checks_pass': True})
    save(ROOT / 'native_layout_matrix.json', {'count': len(matrix), 'cases': matrix,
                                             'manuscript_sha256': sha(MANUSCRIPT.read_bytes()), 'ARM9_sha256': sha(arm),
                                             'source_RAM_sha256': sha(raw), 'actual_new_gameplay_not_claimed': True})
    print('All', len(matrix), 'native quantity/printf/paragraph cases pass. Building complete glyph planes.', flush=True)
    selected, seen = [], set()
    for row in matrix:
        key = (row['message_id'], tuple(row['line_byte_counts']))
        cover_digits = row['message_id'] == 1267 and row['number'] in (0, 1, 2, 9, 10, 39, 48, 67, 99, 100, 255)
        if key not in seen or cover_digits:
            selected.append(row)
            seen.add(key)
    kanji = rom.read_file('/GRP/KANJI.FNT')
    assert kanji == NdsImage.open('out/all_routes_combined_v255_candidate.nds').read_file('/GRP/KANJI.FNT')
    panels, planes = [], []
    folder = ROOT / 'native_font_previews'
    folder.mkdir(exist_ok=True)
    for i, row in enumerate(selected):
        formatted = bytes.fromhex(row['formatted_hex'])
        plane = raster(arm, formatted, 0x01FFCE40 - BASE, size=(228, 64), instruction_limit=2000000)
        assert plane == independent_font(arm, kanji, row['lines'])
        image = Image.frombytes('L', (228, 64), bytes(20 if v == 1 else 130 if v == 15 else 230 for v in plane)).convert('RGB')
        path = folder / f"message_{row['message_id']}_{i:03d}.png"
        image.save(path)
        panel = Image.new('RGB', (480, 188), '#263238')
        ImageDraw.Draw(panel).text((12, 8), f"COMMON {row['message_id']} / value {row['number']} / controlled native", fill='white')
        panel.paste(image.resize((456, 128), Image.Resampling.NEAREST), (12, 36))
        panels.append(panel)
        planes.append({'case': row, 'native_font_plane_sha256': sha(plane), 'preview': str(path),
                       'preview_sha256': sha(path.read_bytes()), 'complete_native_and_independent_plane_equal': True})
    sheets = []
    for start in range(0, len(panels), 8):
        subset = panels[start:start + 8]
        sheet = Image.new('RGB', (960, 188 * ((len(subset) + 1) // 2)), '#172126')
        for i, panel in enumerate(subset):
            sheet.paste(panel, (i % 2 * 480, i // 2 * 188))
        path = ROOT / f'native_dialogue_sheet_{start // 8 + 1}.png'
        sheet.save(path)
        sheets.append({'path': str(path), 'sha256': sha(path.read_bytes())})
    save(ROOT / 'native_font_proof.json', {'ARM9_sha256': sha(arm), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
                                         'matrix_case_count': len(matrix), 'complete_native_font_planes': planes,
                                         'review_sheets': sheets, 'visual_review_pending': True,
                                         'findings': [r for r in matrix if r['findings']],
                                         'all12_records_all_generated_geometry_and_decimal_digit_glyphs_covered': True,
                                         'actual_revised_scenes_registration_and_ROM_patch_pending': True,
                                         'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(len(planes), 'complete font planes and', len(sheets), 'sheets generated;visual review pending.', flush=True)


if __name__ == '__main__':
    main()
