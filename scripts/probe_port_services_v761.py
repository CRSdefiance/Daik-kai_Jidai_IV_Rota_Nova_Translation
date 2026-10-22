"""Research-only native formatting of the complete18-entry service manuscript.

No ARM9 file, ROM, registry entry or production ownership approval is emitted.
The candidate padding placements below are only disposable Unicorn writes.
"""

import struct
from pathlib import Path

from keystone import KS_ARCH_ARM, KS_MODE_ARM, Ks
from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.shipyard_editorial import DIRECT, YESNO, DISPATCH, LITERAL
from dk4tool.patch.shop_business_editorial import compile_paragraph
from dk4tool.rom.nds import NdsImage
from scripts.probe_button_prompt_native import BASE, STACK, machine
from scripts.probe_shipyard_layout_v759 import number
import scripts.probe_shipyard_runtime_v759 as prior
from scripts.review_port_services_v761 import CURRENT, MANUSCRIPT, RAM_REPORT, ROOT
from scripts.verify_common_alignment_native_v257 import raster
from scripts.verify_market_gameplay_v753 import snapshot
from scripts.verify_shipyard_gameplay_v760 import independent_font
from scripts.verify_village_wrap_v608 import read, save

PREFIX, TAIL = 0x02132020, 0x02147C20
DEST = ROOT / 'native_RESEARCH'


def assemble():
    ka = Ks(KS_ARCH_ARM, KS_MODE_ARM)
    prefix = bytes(ka.asm(f'push {{r3,r4,lr}}; ldr r3,[sp,#0x270]; ldr r4,[sp,#0x280]; b {TAIL}', PREFIX)[0])
    tail = bytes(ka.asm(f'''
ldr ip,direct_parent
cmp r3,ip
beq direct
ldr ip,yes_parent
cmp r3,ip
bne fallback
sub r4,r4,#0x400
cmp r4,#0xde
beq selected
fallback:
b {DISPATCH + 4}
direct:
sub r4,r4,#0x300
cmp r4,#0x28
beq selected
sub r4,r4,#0x100
cmp r4,#0xdd
bne fallback
selected:
pop {{r3,r4,lr}}
b {LITERAL}
direct_parent: .word 0x02054014
yes_parent: .word 0x02053fcc
''', TAIL)[0])
    assert len(prefix) == 16 and len(tail) == 80
    return {PREFIX: prefix, TAIL: tail, DISPATCH: bytes(ka.asm(f'b {PREFIX}', DISPATCH)[0])}


def loaded(arm, changed=True):
    u = machine(arm); u.mem_write(BASE, snapshot(read(RAM_REPORT), 3200))
    if changed:
        for address, blob in assemble().items(): u.mem_write(address, blob)
    return u


def membership(arm):
    u = loaded(arm)
    hook = u.hook_add(UC_HOOK_CODE, lambda c, at, size, unused: c.emu_stop() if at in (LITERAL, 0x01FFCF40) else None)
    selected = 0
    try:
        for parent in (0x02054014, 0x02053FCC, 0x02054044, 0x02053D24, 0x02053DB8):
            for table in (0x02118460, 0x021184C0):
                for n in range(3668):
                    u.mem_write(STACK + 0x264, struct.pack('<I', parent)); u.mem_write(STACK + 0x274, struct.pack('<I', n))
                    u.mem_write(STACK + 0x27C, struct.pack('<I', table)); u.reg_write(UC_ARM_REG_SP, STACK)
                    u.emu_start(0x01FFCF3C, 0x027E0000, count=100)
                    expected = (parent == 0x02054014 and n in (*DIRECT, 808, 1245)
                        or parent == 0x02053FCC and n in (*YESNO, 1246)
                        or parent in (0x02053D24, 0x02053DB8) and table == 0x02118460)
                    assert u.reg_read(UC_ARM_REG_PC) == (LITERAL if expected else 0x01FFCF40), (parent, n)
                    assert u.reg_read(UC_ARM_REG_SP) == STACK
                    selected += expected
    finally:
        u.hook_del(hook)
    return {'count': 36680, 'selected': selected, 'only_exact_direct808_1245_and_YesNo1246_additions': True,
        'all_prior_Yard_and_queued_memberships_preserved': True}


def main():
    DEST.mkdir(parents=True, exist_ok=True)
    rom = NdsImage.open(CURRENT); arm = rom.read_file('/__arm9__.bin'); doc = read(MANUSCRIPT)
    assert sha(CURRENT.read_bytes()) == doc['current_ROM_sha256'] == '4558b145919f4eaa3bd0369cef587dd89f91f880bbc3f2fe5f782ee554793bc0'
    scope = membership(arm)
    # The frozen prototype's formatting driver only needs this extra Yes/No ID.
    # Its assembler and all repository modules remain unchanged on disk.
    prior.YESNO = (*prior.YESNO, 1246)
    cpu = loaded(arm)
    cases, renders = [], []
    kanji = rom.read_file('/GRP/KANJI.FNT'); font = GameAsciiFont.from_arm9(arm)
    for row in doc['records']:
        n, text = row['message_id'], row['english'].removesuffix('{PAD}')
        if n in (808, 1245, 1246):
            template = b' ' + text.encode('ascii')
            names = ('Hodram', 'Rafael', 'Lil', 'Maria', 'Camille', 'FALCON', 'ICARUS', 'FIONA', 'FORTUNE', 'FURY', 'ABCDEFGHIJKLMNOPQRSTUVW')
            variants = [(v.encode('ascii'),) for v in names] if n == 808 else [(number(v),) for v in (0, 1, 2, 9, 1000, 21400, 2147483647)]
        else:
            template = text.encode('ascii') if n == 267 else compile_paragraph(row['english'])[0]
            variants = [()]
        for values in variants:
            if n == 267:
                wrapped, lines, findings = template, [text], []
            else:
                result = prior.layout(cpu, template, n, values)
                wrapped, lines, findings = bytes.fromhex(result['formatted_hex']), result['lines'], result['findings']
            assert not findings, (n, values, lines, findings)
            pixels = raster(arm, wrapped, 0xD5404 if n == 267 else 0x01FFCE40 - BASE,
                size=(240, 64) if n == 267 else (228, 64), instruction_limit=1000000)
            if n == 267:
                expected = bytearray(240 * 64)
                for col, char in enumerate(text):
                    glyph = font.decode(char)
                    for y in range(11):
                        for x in range(6):
                            if glyph.getpixel((x, y)): expected[y * 240 + col * 6 + x] = 1
                assert pixels == bytes(expected)
            else:
                assert pixels == independent_font(arm, kanji, lines), (n, lines)
            width = 240 if n == 267 else 228
            path = DEST / f'full_font_{len(cases):03d}_ID{n}.png'
            Image.frombytes('L', (width, 64), bytes(0 if p else 255 for p in pixels)).save(path)
            cases.append({'id': n, 'values_hex': [v.hex() for v in values], 'template_hex': template.hex(),
                'formatted_hex': wrapped.hex(), 'lines': lines, 'findings': findings,
                'complete_independent_font_plane_and_native_buffer_guards': True, 'preview': str(path), 'preview_sha256': sha(path.read_bytes())})
            renders.append(path)
    # Entire preceding Yard layout matrix must survive the new dispatcher shim.
    rows = {r['message_id']: r for r in read('translations/shipyard_editorial_manuscript_v3.json')['records']}
    from dk4tool.patch.shipyard_common import compile_text
    previous = read('work/analysis/shipyard_editorial_v759/typed_literal_runtime_RESEARCH/native_layout_matrix.json')['cases']
    for row in previous:
        result = prior.layout(cpu, compile_text(rows[row['id']]), row['id'], tuple(bytes.fromhex(v) for v in row['values_hex']))
        assert result['formatted_hex'] == row['formatted_hex'] and result['lines'] == row['lines']
    sheets = []
    for start in range(0, len(cases), 12):
        sheet = Image.new('RGB', (1428, 720), '#30343c'); draw = ImageDraw.Draw(sheet)
        for index, row in enumerate(cases[start:start + 12]):
            x, y = index % 3 * 476, index // 3 * 180
            args = ','.join(bytes.fromhex(v).decode('cp932') for v in row['values_hex'])
            draw.text((x + 5, y + 4), f"RESEARCH ID{row['id']} {args}", fill='white')
            image = Image.open(row['preview']).convert('RGB').resize((456, 128), Image.Resampling.NEAREST)
            sheet.paste(image, (x + 5, y + 24))
        path = DEST / f'full_fonts_{start // 12:02d}_2x.png'; sheet.save(path)
        sheets.append({'path': str(path), 'sha256': sha(path.read_bytes())})
    save(DEST / 'verification.json', {'source_ROM_sha256': sha(CURRENT.read_bytes()),
        'manuscript_sha256': sha(MANUSCRIPT.read_bytes()), 'dispatch': scope, 'complete_native_font_cases': cases,
        'all1124_prior_Yard_layouts_identical': True, 'preview_sheets': sheets,
        'research_only_not_owned_storage_approval_or_ROM_integration': True,
        'candidate_CPU_only_patch_spans': {hex(a): b.hex() for a, b in assemble().items()},
        'producer_sha256': sha(Path(__file__).read_bytes()), 'actual_gameplay_pending': True, 'full_goal_complete': False})
    print(f'{len(cases)} complete native layouts/fonts;36680 exact scope cases;1124 preceding Yard outputs unchanged. Research only, no ROM emitted.', flush=True)


if __name__ == '__main__':
    main()
