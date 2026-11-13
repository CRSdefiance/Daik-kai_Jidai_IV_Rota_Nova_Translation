"""Complete native research for eight Market drafts; no ROM is emitted."""

import ast
import struct
from copy import deepcopy
from pathlib import Path

from ndspy.code import MainCodeFile, loadOverlayTable
from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.market_contract_editorial import BASE, GOV, IDS, INVESTMENT, NAMES, PALACE, PORT, TARGET, compile_text, transform
from dk4tool.patch.market_stock_editorial_v2 import compile_text as compile_inherited
from dk4tool.rom.nds import NdsImage
from scripts.prepare_product_pitches_v747 import native_layout, wrapper_dispatch
from scripts.probe_button_prompt_native import STACK, call, machine
from scripts.review_market_contract_v758 import CURRENT, ROOT, context_cases
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_market_balanced_owners_v757 import scope_output
from scripts.verify_village_wrap_v608 import read, save


def loaded(arm):
    u = machine(arm)
    u.mem_write(0x02387A20, bytes(MainCodeFile(arm, BASE).sections[3].data[:-48]))
    return u


def main():
    rom = NdsImage.open(CURRENT)
    common, arm = rom.read_file('/COMMON/MESFILE.DK4'), rom.read_file('/__arm9__.bin')
    doc = deepcopy(read('translations/market_contract_manuscript_v1.json'))
    doc.update({'current_ARM9_sha256': sha(arm), 'current_COMMON_sha256': sha(common)})
    for row in doc['records']:
        row['review']['formatting'] = True
    common2, arm2, patch = transform(common, arm, doc)
    (ROOT / 'research_COMMON.bin').write_bytes(common2)
    (ROOT / 'research_ARM9.bin').write_bytes(arm2)
    save(ROOT / 'native_repack_and_ownership_RESEARCH.json', patch)
    save(ROOT / 'manuscript_native_RESEARCH.json', doc)
    # The only parser change is a strict additional directory digest. Existing
    # function bodies and old supported directories are unchanged.
    old_parser = (ROOT / 'common_message_table_before_v758.py').read_text(encoding='utf-8')
    new_parser_path = Path('dk4tool/script/common_message_table.py')
    new_parser = new_parser_path.read_text(encoding='utf-8')
    def functions(text):
        return [ast.dump(n, include_attributes=False) for n in ast.parse(text).body if isinstance(n, (ast.FunctionDef, ast.ClassDef))]
    assert functions(old_parser) == functions(new_parser)
    # All changed source spans have a complete owner list. The moved literal is
    # in the unused final four bytes of the retired Lil Gallery description.
    regions = ((0x02139830, 0x02139834), (0x021399B4, 0x021399D4), (0x01FFC664, 0x01FFC680))
    units = [(f'section{k}', s.ramAddress, bytes(s.data)) for k, s in enumerate(MainCodeFile(arm, BASE).sections)]
    units += [(f'overlay{k}', s.ramAddress, bytes(s.data)) for k, s in loadOverlayTable(rom.rom.arm9OverlayTable, lambda _, f: rom.rom.files[f]).items()]
    aliases, branches = [], []
    for label, base, data in units:
        for off in range(len(data) - 3):
            value = struct.unpack_from('<I', data, off)[0]
            if any(lo <= value < hi for lo, hi in regions):
                aliases.append((label, base + off, value))
        for off in range(0, len(data) - 3, 4):
            word = struct.unpack_from('<I', data, off)[0]
            if word >> 25 & 7 == 5:
                delta = word & 0xFFFFFF
                if delta & 0x800000:
                    delta -= 0x1000000
                target = base + off + 8 + 4 * delta
                if any(lo <= target < hi for lo, hi in regions):
                    branches.append((label, base + off, target))
    assert aliases == []
    assert sorted(branches) == [('section4', 0x01FFCF50, 0x01FFC664), ('section4', 0x01FFCFD0, 0x021399B4)]
    source_code, target_code = [MainCodeFile(a, BASE) for a in (arm, arm2)]
    restored = [bytearray(s.data) for s in target_code.sections]
    for at, size in patch['owned_metadata_fields']:
        restored[0][at:at + size] = source_code.sections[0].data[at:at + size]
    for address, size in ((GOV, 44), (0x02139830, 4), (0x021399B4, 32),
                          *((BASE + int(p), 4) for p in patch['provider_ownership']['relocated_pointer_fields'])):
        at = address - BASE
        restored[0][at:at + size] = source_code.sections[0].data[at:at + size]
    restored[4][0x664:0x680] = source_code.sections[4].data[0x664:0x680]
    assert all(bytes(a) == bytes(b.data) for a, b in zip(restored, source_code.sections, strict=True))
    assert [(s.ramAddress, len(s.data), s.bssSize) for s in source_code.sections] == [(s.ramAddress, len(s.data), s.bssSize) for s in target_code.sections]
    old, new = wrapper_dispatch(arm), wrapper_dispatch(arm2)
    assert [i for i, (a, b) in enumerate(zip(old, new, strict=True)) if a != b] == [761]
    cpu = loaded(arm2)
    destinations = []
    def stop(u, address, size, unused):
        if address in (0x01FFCA00, 0x0213B958):
            u.emu_stop()
    hook = cpu.hook_add(UC_HOOK_CODE, stop)
    try:
        for n in range(3668):
            cpu.mem_write(STACK + 0x36C, struct.pack('<I', n))
            cpu.reg_write(UC_ARM_REG_SP, STACK)
            cpu.emu_start(0x021399B4, 0x027E0000, count=20)
            target = cpu.reg_read(UC_ARM_REG_PC)
            assert target == (0x0213B958 if n in (761, 767, 768, 769, 770) else 0x01FFCA00)
            destinations.append(target)
    finally:
        cpu.hook_del(hook)
    # The full original parent guard remains byte-exact; explicit complete
    # outputs also test both queued call sites with stale direct message IDs.
    assert arm2[0x13B958:0x13B964] == arm[0x13B958:0x13B964]
    cpus = [loaded(a) for a in (arm, arm2)]
    controls = []
    for parent in (0x02053FCC, 0x02054044, 0x02053D24, 0x02053DB8):
        for table in (0x02117B40, 0x021181E0, 0x021182A0, 0x02118300, 0x021184C0, 0x02118480):
            for n in (761, 767, 768, 769, 770):
                outputs = []
                for u in cpus:
                    u.mem_write(STACK + 0x27C, struct.pack('<I', table))
                    outputs.append(scope_output(u, b' Existing words and line handling stay exactly the same.', n, (), parent))
                assert outputs[0] == outputs[1]
                controls.append({'parent': parent, 'table': table, 'id': n, 'full_output_and_ABI_equal': True})
    # Full current names, including deliberately unaligned reused suffixes,
    # pass through the real original printf routine with buffer guards.
    providers = []
    for label, old, new, expected in (('Palace', GOV + 8, PALACE, b'Palace'),
                                     ('Investment', GOV + 16, INVESTMENT, b'Investment'),
                                     ('Port', GOV + 28, PORT, b'Port'),
                                     ('Target', GOV + 36, TARGET, b'Target')):
        for u, address in zip(cpus, (old, new), strict=True):
            u.mem_write(0x02420000, b'%s\0')
            u.mem_write(0x02421000, b'\xA5' * 96)
            call(u, 0xD7720, (0x02421010, 0x02420000, address))
            assert bytes(u.mem_read(0x02421000, 16)) == b'\xA5' * 16
            assert bytes(u.mem_read(0x02421010, len(expected) + 1)) == expected + b'\0'
            assert bytes(u.mem_read(0x02421011 + len(expected), 79 - len(expected))) == b'\xA5' * (79 - len(expected))
        providers.append({'label': label, 'old_pointer': old, 'new_pointer': new, 'complete_native_printf_and_guards_exact': True})
    meanings = context_cases(arm2)
    assert [bytes.fromhex(r['argument_hex']).decode('ascii') for r in meanings['contract_facility_cases']] == list(NAMES)
    font = GameAsciiFont.from_arm9(arm2)
    pictures, cases = [], []
    weak = {'a', 'an', 'as', 'at', 'for', 'from', 'in', 'of', 'the', 'to', 'with'}
    for row in doc['records']:
        n = row['message_id']
        raw = compile_text(row)
        for values in ((name,) for name in NAMES) if n == 761 else [()]:
            parent = 0x02054014 if n == 761 else 0x02053DB8
            cpu.mem_write(STACK + 0x27C, struct.pack('<I', 0x02118480))
            formatted, lines = native_layout(cpu, raw, n, values, parent)
            assert len(lines[-1]) > 8 and all(s.split()[-1].strip('.,!?;:').lower() not in weak for s in lines[:-1])
            plane = raster(arm2, formatted, 0x01FFCE40 - BASE, size=(228, 64), instruction_limit=1000000)
            expected = bytearray(228 * 64)
            for line_index, line in enumerate(lines):
                for column, char in enumerate(line):
                    glyph = font.decode(char)
                    for y in range(11):
                        for x in range(6):
                            if glyph.getpixel((x, y)):
                                expected[(16 * line_index + y) * 228 + 6 + column * 6 + x] = 1
            assert plane == bytes(expected), (n, values, lines)
            path = ROOT / f'native_{n}_{len(pictures):02d}.png'
            Image.frombytes('L', (228, 64), bytes(0 if p else 255 for p in plane)).save(path)
            pictures.append({'id': n, 'values': values, 'lines': lines, 'preview': str(path), 'complete_glyphs_blanks_bounds_and_ABI': True})
    # Existing stock prose exhaustively exercises the changed entry dispatch.
    # Compare to every completed V757 layout, not a newly invented oracle.
    prior = read('work/analysis/market_balanced_v757/native_layout_matrix_RESEARCH.json')['all_cases']
    inherited = {r['message_id']: r for r in read('translations/market_stock_manuscript_v3.json')['records']}
    for k, old in enumerate(prior):
        if k % 64 == 0:
            cpu = loaded(arm2)
        formatted, lines = native_layout(cpu, compile_inherited(inherited[old['id']]), old['id'], old['values'])
        assert formatted.hex() == old['formatted_hex'] and lines == old['lines']
        if k % 2000 == 0:
            print(f'{k} inherited stock layouts exactly match V757', flush=True)
    assert len(prior) == 31013
    sheet = Image.new('RGB', (1404, 525), '#30343c')
    draw = ImageDraw.Draw(sheet)
    for k, item in enumerate(pictures):
        x, y = k % 3 * 468, k // 3 * 175
        draw.text((x + 4, y + 2), f"{item['id']} {' / '.join(item['values'])}", fill='white')
        sheet.paste(Image.open(item['preview']).convert('RGB').resize((456, 128), Image.Resampling.NEAREST), (x + 4, y + 22))
    sheet.save(ROOT / 'all9_native_previews_2x.png')
    save(ROOT / 'native_review_RESEARCH.json', {'source_ROM_sha256': sha(CURRENT.read_bytes()), 'target_COMMON_sha256': sha(common2),
        'target_ARM9_sha256': sha(arm2), 'all9_complete_font_planes': pictures, 'all18340_dispatch_cases_only761_changes': True,
        'all3668_private_entry_ID_membership_cases': destinations, 'all120_non_direct_full_output_controls': controls,
        'all4_other_label_native_printf_guards_and_full_bytes': providers, 'all31013_inherited_stock_outputs_equal_V757': True,
        'all_current_code_pointer_aliases': aliases, 'all_current_code_branch_owners': branches,
        'all_other_section_bytes_and_shapes_exact_after_owned_restoration': True,
        'native_source_decision_cases': meanings, 'strict_parser_change_function_bodies_identical': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'production_module_sha256': sha(Path('dk4tool/patch/market_contract_editorial.py').read_bytes()),
        'actual_gameplay_and_registered_integration_pending': True, 'full_goal_complete': False})
    print('Nine complete native planes,scope/owners/ABI and31013 inherited layouts pass; gameplay/integration pending.', flush=True)


if __name__ == '__main__':
    main()
