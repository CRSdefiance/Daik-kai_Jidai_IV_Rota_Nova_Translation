"""Full Tavern prose/provider formatter research; never emits a playable ROM."""

import json
import struct
from itertools import product
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_SP

from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shipyard_editorial import DISPATCH, LITERAL
from dk4tool.rom.nds import NdsImage
from scripts.context_tavern_conversations_v763 import CURRENT, RAM_REPORT, PRIVATE, private_directions
from scripts.probe_button_prompt_native import BASE, STACK, machine
from scripts.native_call_abi_v764 import call
from scripts.review_tavern_conversations_v763 import MANUSCRIPT
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_market_gameplay_v753 import snapshot
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read, save

ROOT = Path('work/analysis/tavern_conversations_v764')
GATE, TYPES, TYPE_HELPER = 0x02472000, 0x02470200, 0x02471000
PORT_PREFIX = 0x02132020
GIFT_TABLES = (0x021166E0, 0x02116610)
PROFESSIONS = (b'trader', b'pirate', b'soldier', b'conqueror')


def code():
    ka = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    gate = bytes(ka.asm(f'''
push {{r3,r4,lr}}
ldr r3,[sp,#0x270]
ldr ip,direct_parent
cmp r3,ip
beq direct
ldr ip,yes_parent
cmp r3,ip
beq yes
ldr ip,gift_parent
cmp r3,ip
beq gift
ldr ip,player_parent
cmp r3,ip
bne fallback
ldr r4,[sp,#0x27c]
sub r4,r4,#0x300
cmp r4,#0x39
beq selected
b fallback
direct:
ldr r4,[sp,#0x280]
sub r4,r4,#0x300
sub r4,r4,#0x34
cmp r4,#30
bls selected
b fallback
yes:
ldr r4,[sp,#0x280]
sub r4,r4,#0x300
cmp r4,#0x47
beq selected
b fallback
gift:
ldr r4,[sp,#0x27c]
ldr ip,gift_table1
cmp r4,ip
beq selected
ldr ip,gift_table2
cmp r4,ip
beq selected
fallback:
pop {{r3,r4,lr}}
b {PORT_PREFIX}
selected:
pop {{r3,r4,lr}}
b {LITERAL}
direct_parent: .word 0x02054014
yes_parent: .word 0x02053fcc
gift_parent: .word 0x02053c14
player_parent: .word 0x02053c5c
gift_table1: .word {GIFT_TABLES[0]}
gift_table2: .word {GIFT_TABLES[1]}
''', GATE)[0])
    helper = bytes(ka.asm(f'''
ldrb r1,[r0,#9]
cmp r1,#4
bhs original
ldr r0,table
ldr r0,[r0,r1,lsl #2]
bx lr
original: b 0x0203cf70
table: .word {TYPES}
''', TYPE_HELPER)[0])
    return {GATE: gate, TYPE_HELPER: helper,
        DISPATCH: bytes(ka.asm(f'b {GATE}', DISPATCH)[0]),
        BASE + 0x59CC8: bytes(ka.asm(f'bl {TYPE_HELPER}', BASE + 0x59CC8)[0])}


def loaded(arm, changed=True):
    u = machine(arm); u.mem_write(BASE, snapshot(read(RAM_REPORT), 3200))
    if changed:
        private_directions(u)
        at = TYPES + 0x20
        for index, value in enumerate(PROFESSIONS):
            u.mem_write(TYPES + index * 4, struct.pack('<I', at)); u.mem_write(at, value + b'\0'); at += len(value) + 1
        for at, blob in code().items(): u.mem_write(at, blob)
    return u


def format_case(u, row, values):
    n = row['message_id']; raw = b' ' + row['english'].removesuffix('{PAD}').encode('ascii')
    template, output, wrapped = 0x02420000, 0x02420810, 0x02420C10
    pointers = [0x02422000 + 0x100 * i for i in range(5)]
    u.mem_write(template, raw + b'\0')
    for p, value in zip(pointers, values, strict=False): u.mem_write(p, value + b'\0')
    u.mem_write(output - 16, b'\xa5' * 288); u.mem_write(STACK, struct.pack('<3I', *pointers[2:]))
    call(u, 0xD7720, (output, template, pointers[0], pointers[1]))
    expected = raw
    for value in values: expected = expected.replace(b'%s', value, 1)
    assert len(expected) < 236 and bytes(u.mem_read(output, len(expected) + 1)) == expected + b'\0'
    assert bytes(u.mem_read(output - 16, 16)) == b'\xa5' * 16
    assert bytes(u.mem_read(output + len(expected) + 1, 271 - len(expected))) == b'\xa5' * (271 - len(expected))
    parent = 0x02053C14 if 830 <= n <= 833 or 835 <= n <= 838 else 0x02053C5C if n == 825 else 0x02053FCC if n == 839 else 0x02054014
    u.mem_write(STACK + 0x264, struct.pack('<I', parent)); u.mem_write(STACK + 0x274, struct.pack('<I', n))
    table = GIFT_TABLES[0 if n <= 833 else 1] if parent == 0x02053C14 else n if parent == 0x02053C5C else 0
    u.mem_write(STACK + 0x270, struct.pack('<I', table))
    u.mem_write(STACK + 0x27C, struct.pack('<I', 0x021184C0))
    u.mem_write(wrapped - 16, b'\xa5' * 288)
    call(u, 0x01FFCF3C - BASE, (wrapped, output, 0), instruction_limit=2000000)
    result = bytes(u.mem_read(wrapped, 256)).split(b'\0')[0]
    assert bytes(u.mem_read(wrapped - 16, 16)) == bytes(u.mem_read(wrapped + 256, 16)) == b'\xa5' * 16
    assert b' '.join(result.split()) == b' '.join(expected.split()), (n, values, result, expected)
    lines = [line.strip().decode('cp932') for line in result.split(b'\n')]
    findings = []
    if len(lines) > 4 or any(len(line.encode('cp932')) > 35 for line in lines): findings.append('four_row_width_bound')
    if len(lines) > 1 and len(lines[-1].encode('cp932')) <= 8: findings.append('short_final_row')
    weak = {'a', 'an', 'as', 'at', 'for', 'from', 'in', 'of', 'the', 'to', 'with'}
    if any(line.split()[-1].strip('.,!?;:').lower() in weak for line in lines[:-1] if line.split()): findings.append('weak_line_end')
    return {'id': n, 'values_hex': [v.hex() for v in values], 'parent': parent, 'table_or_player_ID': table,
        'formatted_hex': result.hex(), 'lines': lines, 'findings': findings,
        'whole_printf_wrap_bytes_guards_and_callee_saved_ABI_exact': True}


def variants(n, context):
    items = [bytes.fromhex(r['name_hex']) for r in context['actual218_item_names']]
    towns = [bytes.fromhex(r['name_hex']) for r in context['actual90_town_names']]
    goods = [bytes.fromhex(r['name_hex']) for r in context['actual124_named_commodity_objects']]
    qualifiers, ns, ew = (b'a little', b'far', b'very far'), (b'north', b'south'), (b'east', b'west')
    if n in (820, 821):
        people = (b'Hodram Bergstrom', b'Rafael Castor', b'Maria Huamei Li', b'ABCDEFGHIJKLMNOPQRSTUVW', b'FALCON', b'ICARUS')
        yield from product(people, towns, PROFESSIONS)
    elif n in (822, 823): yield from ((v,) for v in towns)
    elif n == 827:
        yield from ((v,) for v in (b'Rafael', b'Hodram', b'Lil', b'Maria', b'Camille', b'FALCON', b'ICARUS', b'FIONA', b'FORTUNE', b'FURY', b'ABCDEFGHIJKLMNOPQRSTUVW'))
    elif n in (828, 830, 831, 832, 833, 846): yield from ((v,) for v in items)
    elif n == 842: yield from ((bytes.fromhex(r['argument_hex']),) for r in context['actual_coordinate_formatter_arguments_for842'])
    elif n == 843: yield from product(items, qualifiers, ns, qualifiers, ew)
    elif n in (844, 845): yield from product(items, qualifiers, ew if n == 844 else ns)
    elif n in (847, 848): yield from ((v,) for v in goods)
    elif n in (849, 850): yield from product(towns, goods)
    else: yield ()


def dispatch(arm):
    from dk4tool.patch.shipyard_editorial import DIRECT, YESNO
    u = loaded(arm); selected = 0
    h = u.hook_add(UC_HOOK_CODE, lambda c, at, size, unused: c.emu_stop() if at in (LITERAL, 0x01FFCF40) else None)
    try:
        for parent, old_table, n in product((0x02054014, 0x02053FCC, 0x02054044, 0x02053D24, 0x02053DB8), (0x02118460, 0x021184C0), range(3668)):
            u.mem_write(STACK + 0x264, struct.pack('<I', parent)); u.mem_write(STACK + 0x274, struct.pack('<I', n))
            u.mem_write(STACK + 0x270, bytes(4)); u.mem_write(STACK + 0x27C, struct.pack('<I', old_table)); u.reg_write(UC_ARM_REG_SP, STACK)
            u.emu_start(0x01FFCF3C, 0x027E0000, count=200)
            expected = (parent == 0x02054014 and n in (*DIRECT, 808, 1245, *range(820, 851))
                or parent == 0x02053FCC and n in (*YESNO, 1246, 839)
                or parent in (0x02053D24, 0x02053DB8) and old_table == 0x02118460)
            assert u.reg_read(UC_ARM_REG_PC) == (LITERAL if expected else 0x01FFCF40), (parent, n)
            assert u.reg_read(UC_ARM_REG_SP) == STACK; selected += expected
        for parent, word, unrelated in product((0x02053C14, 0x02053C5C), (*GIFT_TABLES, 825, 0x02118460, 0), (0, 825, 850, 3667, 0x02412345)):
            u.mem_write(STACK + 0x264, struct.pack('<I', parent)); u.mem_write(STACK + 0x270, struct.pack('<I', word))
            u.mem_write(STACK + 0x274, struct.pack('<I', unrelated)); u.reg_write(UC_ARM_REG_SP, STACK)
            u.emu_start(0x01FFCF3C, 0x027E0000, count=200)
            expected = parent == 0x02053C14 and word in GIFT_TABLES or parent == 0x02053C5C and word == 825
            assert u.reg_read(UC_ARM_REG_PC) == (LITERAL if expected else 0x01FFCF40)
            assert u.reg_read(UC_ARM_REG_SP) == STACK
    finally: u.hook_del(h)
    return {'all36680_earlier_parent_ID_table_memberships': True, 'all50_new_player_and_gift_scope_cases': True,
        'old_memberships_preserved_new_direct820_850_YesNo839_and_exact_player_gift_contracts_only': True}


def main():
    ROOT.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open(CURRENT); arm = rom.read_file('/__arm9__.bin'); doc = read(MANUSCRIPT)
    context = read('work/analysis/tavern_conversations_v763/native_context.json')
    assert doc['current_ROM_sha256'] == sha(CURRENT.read_bytes())
    scopes = dispatch(arm); print('Exact inherited and new caller/table scopes pass.', flush=True)
    # Exercise all256 enum values; only four valid professions change case.
    machines = [loaded(arm, flag) for flag in (False, True)]
    roles = []
    for value in range(256):
        outputs = []
        for cpu, fn in zip(machines, (0x3CF70, TYPE_HELPER - BASE), strict=True):
            cpu.mem_write(0x02478000, bytes(9) + bytes((value,)) + bytes(6)); call(cpu, fn, (0x02478000,))
            outputs.append(bytes(cpu.mem_read(cpu.reg_read(UC_ARM_REG_R0), 64)).split(b'\0')[0])
        assert outputs[1] == (PROFESSIONS[value] if value < 4 else outputs[0])
        roles.append({'enum': value, 'source_hex': outputs[0].hex(), 'new_hex': outputs[1].hex()})
    u = loaded(arm); cases, findings = [], []
    for row in doc['records']:
        before = len(cases)
        for index, values in enumerate(variants(row['message_id'], context)):
            if index % 64 == 0:
                u = loaded(arm)
            result = format_case(u, row, values); cases.append(result)
            if result['findings']: findings.append(result)
            if index and index % 2048 == 0:
                print(f'ID{row["message_id"]}: {index} cases in progress.', flush=True)
        print(f'ID{row["message_id"]}: {len(cases) - before} complete layouts; {len(findings)} findings so far.', flush=True)
    save(ROOT / 'native_layout_matrix.json', {'count': len(cases), 'findings_count': len(findings), 'cases': cases,
        'supplied_field_combinations_not_all_claimed_legal_or_earned_world_states': True})
    save(ROOT / 'layout_findings.json', findings)
    save(ROOT / 'provider_and_dispatch.json', {'dispatch': scopes, 'all256_profession_enum_outputs': roles,
        'CPU_only_code_hex': {hex(at): blob.hex() for at, blob in code().items()},
        'no_production_storage_approval_or_ROM_emitted': True, 'source_ROM_sha256': sha(CURRENT.read_bytes()),
        'producer_sha256': sha(Path(__file__).read_bytes()),
        'bounded_ABI_helper_sha256': sha(Path('scripts/native_call_abi_v764.py').read_bytes()),
        'fresh_initialized_CPU_every64_cases': True})
    assert not findings, f'{len(findings)} layout cases require correction before release'
    # Full decoded planes for every paragraph/line shape,plus special names
    # and all distinct coordinate spacing shapes. No cropped glyph comparisons.
    seen, previews = set(), []; kanji = rom.read_file('/GRP/KANJI.FNT')
    for row in cases:
        marker = (row['id'], tuple(len(x.encode('cp932')) % 2 for x in row['lines']))
        values = [bytes.fromhex(v) for v in row['values_hex']]
        if values and values[0] in (b'FALCON', b'ICARUS', b'FIONA', b'FORTUNE', b'FURY'): marker += (values[0],)
        if marker in seen: continue
        seen.add(marker); formatted = bytes.fromhex(row['formatted_hex'])
        pixels = raster(arm, formatted, 0x01FFCE40 - BASE, size=(228, 64), instruction_limit=1000000)
        assert pixels == independent_font(arm, kanji, row['lines'])
        path = ROOT / f'complete_font_{len(previews):03d}_ID{row["id"]}.png'
        Image.frombytes('L', (228, 64), bytes(0 if p else 255 for p in pixels)).save(path)
        previews.append({**row, 'preview': str(path), 'preview_sha256': sha(path.read_bytes()), 'independent_whole_glyph_plane_exact': True})
    sheets = []
    for start in range(0, len(previews), 12):
        sheet = Image.new('RGB', (1428, 720), '#30343c'); draw = ImageDraw.Draw(sheet)
        for i, row in enumerate(previews[start:start + 12]):
            x, y = i % 3 * 476, i // 3 * 180
            draw.text((x + 5, y + 4), f'RESEARCH ID{row["id"]} / {start + i}', fill='white')
            sheet.paste(Image.open(row['preview']).convert('RGB').resize((456, 128), Image.Resampling.NEAREST), (x + 5, y + 24))
        path = ROOT / f'complete_fonts_{start // 12:02d}_2x.png'; sheet.save(path); sheets.append({'path': str(path), 'sha256': sha(path.read_bytes())})
    save(ROOT / 'verification.json', {'source_ROM_sha256': sha(CURRENT.read_bytes()), 'manuscript_sha256': sha(MANUSCRIPT.read_bytes()),
        'complete_native_layouts': len(cases), 'complete_font_planes': previews, 'preview_sheets': sheets,
        'all31_message_IDs_covered': sorted({r['id'] for r in cases}), 'provider_dispatch_report': str(ROOT / 'provider_and_dispatch.json'),
        'research_only_no_owned_storage_registered_ROM_patch_or_actual_gameplay_claim': True,
        'producer_sha256': sha(Path(__file__).read_bytes()), 'full_goal_complete': False})
    print(f'{len(cases)} native layouts and{len(previews)} complete font planes pass. Research only.', flush=True)


if __name__ == '__main__': main()
