"""Prospective literal-path layout research for32 source-reviewed paragraphs.

Uses original printf and the existing production literal formatter directly.
This does not prove the future dispatcher or region-provider integration.
"""

import struct
from itertools import product
from pathlib import Path

from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R8, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shipyard_editorial import LITERAL
from dk4tool.rom.nds import NdsImage
from scripts.context_tavern_continuation_v768 import CURRENT, RAM_REPORT
from scripts.native_call_abi_v764 import call
from scripts.native_machine_scoped_v764 import machine
from scripts.probe_button_prompt_native import BASE, STACK
from scripts.review_tavern_continuation_v768 import MANUSCRIPT
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_market_gameplay_v753 import snapshot
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/tavern_continuation_layout_v768_v2')


def amount_cases(arm, raw, context):
    u = machine(arm); u.mem_write(BASE, raw)
    current = [None]; captured = []
    def town(c, at, size, unused):
        c.reg_write(UC_ARM_REG_R0, current[0]); c.reg_write(UC_ARM_REG_PC, c.reg_read(UC_ARM_REG_LR))
    def price(c, at, size, unused):
        p = c.reg_read(UC_ARM_REG_R2)
        value = bytes(c.mem_read(p, 64)).split(b'\0')[0]
        captured.append({'town_object': current[0], 'numeric_price': c.reg_read(UC_ARM_REG_R8), 'amount_hex': value.hex()})
        c.emu_stop()
    hooks = [u.hook_add(UC_HOOK_CODE, town, begin=BASE + 0xB6618, end=BASE + 0xB6618),
        u.hook_add(UC_HOOK_CODE, price, begin=BASE + 0x53CB0, end=BASE + 0x53CB0)]
    try:
        for place in context['real_town_names']:
            current[0] = place['object']; u.reg_write(UC_ARM_REG_SP, STACK)
            u.emu_start(BASE + 0x58350, BASE + 0x5839C, count=10000)
    finally:
        for hook in hooks: u.hook_del(hook)
    assert len(captured) == 90
    return captured


def format_case(u, row, source_values):
    values = tuple(source_values[i] for i in row['English_argument_source_indices'])
    raw = b' ' + row['english'].removesuffix('{PAD}').encode('ascii')
    template, output, wrapped = 0x02420000, 0x02420810, 0x02420C10
    pointers = [0x02422000 + 0x100 * i for i in range(3)]
    u.mem_write(template, raw + b'\0')
    for p, value in zip(pointers, values): u.mem_write(p, value + b'\0')
    u.mem_write(output - 16, b'\xa5' * 288)
    u.mem_write(STACK, struct.pack('<I', pointers[2]))
    call(u, 0xD7720, (output, template, pointers[0], pointers[1]))
    expected = raw
    for value in values: expected = expected.replace(b'%s', value, 1)
    assert len(expected) < 236
    assert bytes(u.mem_read(output, len(expected) + 1)) == expected + b'\0'
    assert bytes(u.mem_read(output - 16, 16)) == b'\xa5' * 16
    assert bytes(u.mem_read(output + len(expected) + 1, 271 - len(expected))) == b'\xa5' * (271 - len(expected))
    u.mem_write(wrapped - 16, b'\xa5' * 288)
    call(u, LITERAL - BASE, (wrapped, output, 0), instruction_limit=2000000)
    result = bytes(u.mem_read(wrapped, 256)).split(b'\0')[0]
    assert bytes(u.mem_read(wrapped - 16, 16)) == bytes(u.mem_read(wrapped + 256, 16)) == b'\xa5' * 16
    assert b' '.join(result.split()) == b' '.join(expected.split())
    lines = [line.strip().decode('cp932') for line in result.split(b'\n')]
    findings = []
    if len(lines) > 4 or any(len(line.encode('cp932')) > 35 for line in lines): findings.append('four_row_width_bound')
    if len(lines) > 1 and len(lines[-1].encode('cp932')) <= 8: findings.append('short_final_row')
    weak = {'a', 'an', 'as', 'at', 'for', 'from', 'in', 'of', 'the', 'to', 'with'}
    if any(line.split()[-1].strip('.,!?;:').lower() in weak for line in lines[:-1] if line.split()): findings.append('weak_line_end')
    return {'id': row['message_id'], 'source_values_hex': [v.hex() for v in source_values],
        'English_values_hex': [v.hex() for v in values], 'formatted_hex': result.hex(),
        'lines': lines, 'findings': findings, 'exact_printf_and_complete_words_and_guards_and_callee_saved_ABI': True}


def variants(n, context, amounts):
    organizations = [bytes.fromhex(r['name_hex']) for r in context['real_company_names']]
    towns = [bytes.fromhex(r['name_hex']) for r in context['real_town_names']]
    items = [bytes.fromhex(r['name_hex']) for r in context['real_item_names_and_native_regions']]
    regions = [r['proposed_dialogue_region_phrase'].encode('ascii') for r in context['seven_region_labels_and_proposed_private_dialogue_phrases']]
    addresses = (b'Sir', b"Ma'am")
    surnames = sorted({bytes.fromhex(c['arguments_hex'][0]) for c in context['original_provider_fragments'] if c['id'] == 875}
        | {b'ABCDEFGHIJKLMNOPQRSTUVW', b'FALCON', b'ICARUS', b'FIONA', b'FORTUNE', b'FURY'})
    if n in (851, 879, 880, 881, 882): yield from product(organizations, towns)
    elif 852 <= n <= 858:
        values = {bytes.fromhex(c['amount_hex']) for c in amounts}
        # Boundary amounts are explicit synthetic number-size tests,not earned costs.
        values |= {str(v).translate(str.maketrans('0123456789', '０１２３４５６７８９')).encode('cp932') for v in (1, 9, 10, 99, 100, 999, 9999, 99999, 999999, 9999999, 99999999, 999999999, 2147483647)}
        yield from ((v,) for v in sorted(values))
    elif n == 863: yield from product(items, regions)
    elif n == 870: yield from product(addresses, items, regions)
    elif n in (869, 875): yield from ((v,) for v in surnames)
    elif n in (871, 872): yield from product(surnames, addresses)
    elif n in (873, 877): yield from ((v,) for v in addresses)
    elif n == 876: yield from ((v,) for v in organizations)
    elif n == 878: yield from product(organizations, addresses)
    else: yield ()


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open(CURRENT); arm = rom.read_file('/__arm9__.bin')
    context = read('work/analysis/tavern_continuation_v768/native_context_partial.json')
    manuscript = read(MANUSCRIPT)
    raw = snapshot(read(RAM_REPORT), 3200)
    amounts = amount_cases(arm, raw, context)
    save(ROOT / 'native_90_town_amounts.json', amounts)
    cases, findings = [], []
    for row in manuscript['records']:
        before = len(cases)
        for i, values in enumerate(variants(row['message_id'], context, amounts)):
            if i % 64 == 0: u = machine(arm)
            result = format_case(u, row, values); cases.append(result)
            if result['findings']: findings.append(result)
        print(f'ID{row["message_id"]}: {len(cases)-before} layouts; {len(findings)} findings so far.', flush=True)
    save(ROOT / 'native_layout_matrix.json', {'count': len(cases), 'findings_count': len(findings), 'cases': cases,
        'supplied_combinations_and_numeric_bounds_not_all_claimed_legal_or_earned_states': True})
    save(ROOT / 'layout_findings.json', findings)
    assert not findings, f'{len(findings)} cases need presentation repair'
    previews, seen = [], set(); kanji = rom.read_file('/GRP/KANJI.FNT')
    for row in cases:
        marker = (row['id'], tuple(len(line.encode('cp932')) % 2 for line in row['lines']))
        if marker in seen: continue
        seen.add(marker)
        formatted = bytes.fromhex(row['formatted_hex'])
        plane = raster(arm, formatted, 0x01FFCE40 - BASE, size=(228,64), instruction_limit=1000000)
        assert plane == independent_font(arm, kanji, row['lines'])
        path = ROOT / f'complete_font_{len(previews):03d}_ID{row["id"]}.png'
        Image.frombytes('L', (228,64), bytes(0 if p else 255 for p in plane)).save(path)
        previews.append({**row, 'path': str(path), 'sha256': sha(path.read_bytes()), 'independent_full_font_plane_exact': True})
    sheets = []
    for start in range(0,len(previews),12):
        sheet=Image.new('RGB',(1428,720),'#30343c'); draw=ImageDraw.Draw(sheet)
        for i,row in enumerate(previews[start:start+12]):
            x,y=i%3*476,i//3*180
            draw.text((x+5,y+4),f'RESEARCH ID{row["id"]} / {start+i}',fill='white')
            sheet.paste(Image.open(row['path']).convert('RGB').resize((456,128),Image.Resampling.NEAREST),(x+5,y+24))
        path=ROOT/f'complete_fonts_{start//12:02d}_2x.png';sheet.save(path);sheets.append({'path':str(path),'sha256':sha(path.read_bytes())})
    save(ROOT/'verification.json',{'candidate':str(CURRENT),'candidate_sha256':sha(CURRENT.read_bytes()),
        'manuscript_sha256':sha(MANUSCRIPT.read_bytes()), 'complete_native_layouts':len(cases),
        'complete_font_planes':previews,'preview_sheets':sheets,'all32_IDs_covered':sorted({r['id'] for r in cases}),
        'direct_existing_literal_path_only_not_future_dispatch_or_provider_approval':True,
        'no_registered_ROM_patch_or_actual_gameplay_claim':True, 'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print(f'{len(cases)} layouts and{len(previews)} independent full-font planes pass; research only.',flush=True)


if __name__ == '__main__': main()
