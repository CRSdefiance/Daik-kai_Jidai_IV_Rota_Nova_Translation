"""Native mixed-width shipyard probes; report unfinished layout/grammar gates.

Forced wrapping is a research-only call to the inherited helper, bypassing its
release allowlist. It is never registered or emitted in a ROM here.
"""

import re
import struct
from itertools import product
from pathlib import Path

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shop_business_editorial import compile_paragraph
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, call, machine
from scripts.review_shipyard_editorial_v759 import CURRENT, MANUSCRIPT, ROOT
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_village_wrap_v608 import read, save

PRICES = (1, 9, 99, 1000, 50000, 1000000, 2147483647)
NAMES = ('A', 'Vestaros', 'FALCON', 'ICARUS', 'ABCDEFGHIJKLMNOPQRSTUVW', 'A B C D E F G H I J K L')
NUMBERS = read(ROOT / 'native_context.json')['source_number_formatter_identical_and_actual_initialized_contract']['samples']


def loaded(arm):
    u = machine(arm)
    u.mem_write(0x02387A20, bytes(MainCodeFile(arm, BASE).sections[3].data[:-48]))
    return u


def number(n):
    # Source-native ABF50 format is independently proved as full-width decimal.
    # Unlisted boundary samples use that exact observed encoding contract.
    raw = str(n).translate(str.maketrans('0123456789', '０１２３４５６７８９')).encode('cp932')
    if str(n) in NUMBERS:
        assert raw.hex() == NUMBERS[str(n)]
    return raw


def layout(u, raw, n, values, force=False):
    template, filtered, output, wrapped = 0x02420000, 0x02420410, 0x02420810, 0x02420C10
    pointers = (0x02422000, 0x02422100, 0x02422200)
    u.mem_write(template, raw + b'\0')
    u.mem_write(filtered - 16, b'\xA5' * 288)
    call(u, 0x53914, (filtered, template, 0x02425000))
    filtered_bytes = bytes(u.mem_read(filtered, 256)).split(b'\0')[0]
    assert filtered_bytes == raw, (n, 'literal/control preservation', raw, filtered_bytes)
    for ptr, value in zip(pointers, values):
        u.mem_write(ptr, value + b'\0')
    u.mem_write(output - 16, b'\xA5' * 288)
    u.mem_write(STACK, struct.pack('<I', pointers[2]))
    call(u, 0xD7720, (output, filtered, pointers[0], pointers[1]))
    expected = raw
    for value in values:
        expected = expected.replace(b'%s', value, 1)
    assert bytes(u.mem_read(output, len(expected) + 1)) == expected + b'\0'
    assert bytes(u.mem_read(output - 16, 16)) == b'\xA5' * 16
    assert bytes(u.mem_read(output + len(expected) + 1, 271 - len(expected))) == b'\xA5' * (271 - len(expected))
    u.mem_write(wrapped - 16, b'\xA5' * 288)
    parent = 0x02053DB8 if 791 <= n <= 797 else 0x02053FCC if n in (789, 800, 802, 803, 804) else 0x02054014
    u.mem_write(STACK + 0x264, struct.pack('<I', parent))
    u.mem_write(STACK + 0x274, struct.pack('<I', n))
    u.mem_write(STACK + 0x27C, struct.pack('<I', 0x02118460))
    try:
        call(u, (0x01FFCF78 if force else 0x01FFCF3C) - BASE, (wrapped, output, 0))
    except Exception as error:
        from unicorn.arm_const import UC_ARM_REG_PC
        raise RuntimeError(f'ID{n} forced={force} values={[v.hex() for v in values]} PC={u.reg_read(UC_ARM_REG_PC):#x}') from error
    result = bytes(u.mem_read(wrapped, 256)).split(b'\0')[0]
    assert bytes(u.mem_read(wrapped - 16, 16)) == bytes(u.mem_read(wrapped + 256, 16)) == b'\xA5' * 16
    assert b' '.join(result.split()) == b' '.join(expected.split()), (n, values)
    rows = [r.strip() for r in result.split(b'\n')]
    decoded = result.decode('cp932')
    normal = decoded.translate(str.maketrans('０１２３４５６７８９', '0123456789'))
    flags = []
    if len(rows) > 4 or any(len(r) > 35 for r in rows):
        flags.append('not_complete_four_row_word_layout')
    if len(rows) > 1 and len(rows[-1]) <= 8:
        flags.append('short_final_row')
    weak = {'a', 'an', 'as', 'at', 'for', 'from', 'in', 'of', 'the', 'to', 'with'}
    if any(r.decode('cp932').split()[-1].strip('.,!?;:').lower() in weak for r in rows[:-1] if r.split()):
        flags.append('weak_line_end')
    if re.search(r'(?<![0-9])1 (?:gold coins|days|masts)\b', ' '.join(normal.split())):
        flags.append('singular_quantity_grammar')
    return result, {'id': n, 'values_hex': [v.hex() for v in values], 'parent': parent,
                    'forced_research_helper': force, 'formatted_hex': result.hex(),
                    'lines': [r.decode('cp932') for r in rows], 'visible_column_counts': list(map(len, rows)), 'findings': flags,
                    'all_native_word_bytes_printf_source_output_guards_and_ABI_preserved': True}


def units(raw):
    result, at = [], 0
    for word, token in enumerate(raw.split()):
        at = 0
        while at < len(token):
            width = 2 if 0x81 <= token[at] <= 0x9F or 0xE0 <= token[at] <= 0xFC else 1
            result.append((int.from_bytes(token[at:at + width], 'big'), word))
            at += width
    return result


def main():
    arm = NdsImage.open(CURRENT).read_file('/__arm9__.bin')
    doc = read(MANUSCRIPT)
    matrices, previews, compile_errors, context_errors = [], [], [], []
    cpu, count = loaded(arm), 0
    for row in doc['records']:
        n = row['message_id']
        text = row['english'].removesuffix('{PAD}')
        if '%s' in text:
            raw = b' ' + text.encode('ascii')
            cases = ([(number(m), number(h)) for m, h in product((1, 3, 5), (1, 100, 65535))] if n == 786 else
                     [(number(p),) for p in PRICES] if n in (789, 799, 800, 802) else
                     [(number(p),) for p in (5, 22, 40)] if n == 798 else
                     [(s.encode('ascii'), number(p), number(d)) for s, p, d in product(NAMES, PRICES, range(1, 17))] if n == 803 else
                     [(s.encode('ascii'), number(p)) for s, p in product(NAMES, PRICES)])
        else:
            try:
                raw, _ = compile_paragraph(row['english'])
            except ValueError as error:
                compile_errors.append({'id': n, 'error': str(error)})
                continue
            cases = [()]
        sample = cases[0]
        for values in cases:
            if count % 64 == 0:
                cpu = loaded(arm)
            for force in (False, True):
                try:
                    formatted, check = layout(cpu, raw, n, values, force)
                except RuntimeError as error:
                    if not values or values[0] not in (b'FALCON', b'ICARUS'):
                        raise
                    # These supplied name values enter original macro handlers.
                    # This isolated probe lacks the real actor/global object
                    # context. Retain the failure and require actual name testing.
                    context_errors.append({'id': n, 'values_hex': [v.hex() for v in values],
                        'forced_research_helper': force, 'error': str(error),
                        'requires_real_actor_and_actual_ship_name_fixture': True})
                    cpu = loaded(arm)
                    continue
                matrices.append(check)
                if values == sample:
                    events = []
                    plane = raster(arm, formatted, 0x01FFCE40 - BASE, size=(228, 96), instruction_limit=1000000, glyph_events=events)
                    visible = [e for e in events if e['code'] != 32]
                    expected = units(formatted)
                    complete = [e['code'] for e in visible] == [c for c, _ in expected]
                    split_words = []
                    if complete:
                        words = {}
                        for (_, word), event in zip(expected, visible, strict=True):
                            words.setdefault(word, set()).add(event['y'])
                        split_words = [k for k, ys in words.items() if len(ys) > 1]
                    path = ROOT / f'native_draft_{n}_{int(force)}.png'
                    Image.frombytes('L', (228, 96), bytes(0 if p else 255 for p in plane)).save(path)
                    previews.append({**check, 'preview': str(path), 'complete_native_glyph_sequence': complete,
                                     'words_crossing_native_auto_rows': split_words,
                                     'all_ink_inside_four_rows': all(e['y'] + 11 <= 64 and e['x'] + (12 if e['code'] > 255 else 6) <= 228 for e in visible)})
            count += 1
    save(ROOT / 'layout_matrix_DRAFT.json', {'cases': matrices, 'count': len(matrices), 'printf_value_cases': count,
        'compile_errors': compile_errors, 'unresolved_argument_context_cases': context_errors, 'producer_sha256': sha(Path(__file__).read_bytes()),
        'samples': previews, 'research_only_not_integrated_or_approved': True})
    for start in range(0, len(previews), 12):
        group = previews[start:start + 12]
        sheet = Image.new('RGB', (1404, 4 * 245), '#30343c')
        draw = ImageDraw.Draw(sheet)
        for k, item in enumerate(group):
            x, y = k % 3 * 468, k // 3 * 245
            label = f"{item['id']} {'FORCED RESEARCH' if item['forced_research_helper'] else 'EXISTING DISPATCH'}"
            draw.text((x + 4, y + 2), label, fill='white')
            draw.text((x + 4, y + 18), ','.join(item['findings'])[:65], fill='#ffcc88')
            sheet.paste(Image.open(item['preview']).convert('RGB').resize((456, 192), Image.Resampling.NEAREST), (x + 4, y + 40))
        sheet.save(ROOT / f'native_draft_review_{start // 12 + 1:02d}.png')
    save(ROOT / 'layout_findings_DRAFT.json', {'by_message': {str(n): {mode: sum(bool(r['findings']) for r in matrices if r['id'] == n and r['forced_research_helper'] == force)
        for mode, force in (('existing_dispatch', False), ('forced_research', True))} for n in range(784, 805)},
        'singular_quantity_cases': sum('singular_quantity_grammar' in r['findings'] for r in matrices),
        'whole_word_layout_cases': sum('not_complete_four_row_word_layout' in r['findings'] for r in matrices),
        'compile_errors': compile_errors, 'unresolved_argument_context_count': len(context_errors), 'not_all_supplied_boundary_values_claimed_reachable_in_game': True,
        'next': 'Prove actual numeric bounds and resolve quantity agreement. Extend reviewed consumer-specific wrapping/balancing with owned storage; preserve complete source facts. Then integrate,verify all native copies/exact patch and actual Yard scenes.'})
    print(f'{len(matrices)} native layouts, {len(previews)} glyph planes, {len(compile_errors)} static compile failures; {len(context_errors)} name-context cases unresolved. Findings remain; no ROM emitted.', flush=True)


if __name__ == '__main__':
    main()
