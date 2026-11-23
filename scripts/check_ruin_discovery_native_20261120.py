"""Check original composition, centered widths, glyphs, and the power notice."""

from pathlib import Path
from struct import pack
from types import FunctionType

from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3
from unicorn.arm_const import UC_ARM_REG_R5, UC_ARM_REG_R8, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import check_departure_numerals_native_20261119 as digits
from scripts import stage_ruin_discovery_display_20261120 as stage
from scripts.check_madeira_resupply_numerals_20261120 import digest
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools, glyph_codes
from scripts.probe_button_prompt_native import STACK
from scripts.seal_shared_text_source_v1 import reference
from scripts.stage_mutiny_review_v1 import portrait_sheets, render_portrait
from scripts.verify_inn_numerals_native_20261119 import read_cstring
from scripts.verify_personal_gameplay_v841 import get_machine


batch = stage.batch
OUTPUT = stage.ROOT / 'native_discovery.json'
SHEET = stage.ROOT / 'ruin_name_lines.png'
AMOUNTS = (0, 1, 9, 10, 99, 100, 260, 1000, 65535, 2147483647)
WIDTH = 256


def composed(arm, raw, original, title, suffix):
    cpu, get = get_machine(arm, raw)
    root = get(0xCB16C) + 4

    def ptr(address):
        return int.from_bytes(cpu.mem_read(address, 4), 'little')

    def text(address):
        return bytes(cpu.mem_read(address, 128)).split(b'\0', 1)[0]

    buffer = []

    def intercept(core, pc, size, _):
        values = tuple(core.reg_read(register) for register in (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3))
        canvas, first, string, x = values
        if x & 0x80000000:
            x -= 0x100000000
        sp = core.reg_read(UC_ARM_REG_SP)
        y = ptr(sp)
        color = ptr(sp+4)
        buffer.append(dict(text=text(string).hex(), x=x, y=y, clear=first, color=color, canvas=canvas))
        core.reg_write(UC_ARM_REG_PC, core.reg_read(UC_ARM_REG_LR))

    hook = cpu.hook_add(UC_HOOK_CODE, intercept, begin=0x02106590, end=0x02106590)
    values = []
    try:
        for n in range(21):
            obj = root + 8*n
            getter = ptr(ptr(obj)+8)
            name = text(get(getter - stage.BASE, obj))
            if not original:
                assert name.isascii()
            buffer.clear()
            cpu.reg_write(UC_ARM_REG_R5, n)
            cpu.mem_write(STACK-544, b'\xa5'*16)
            cpu.mem_write(STACK, b'\xa5'*272)
            cpu.reg_write(UC_ARM_REG_SP, STACK)
            cpu.emu_start(0x0210628C, 0x02106340, count=40_000)
            assert cpu.reg_read(UC_ARM_REG_PC) == 0x02106340 and cpu.reg_read(UC_ARM_REG_SP) == STACK
            headline, body = buffer
            assert [row['canvas'] for row in buffer] == [STACK+8, STACK+8]
            assert [row['text'] for row in buffer] == [title.hex(), (name + suffix).hex()]
            assert [row['clear'] for row in buffer] == [1, 0] and [row['y'] for row in buffer] == [2, 64]
            for row in buffer:
                length = len(bytes.fromhex(row['text']))
                row['within_width'] = 0 <= row['x'] <= (WIDTH-length*6)
                assert row['x'] == 128 - length*3
                if not original:
                    assert row['within_width']
            assert bytes(cpu.mem_read(STACK-544, 16)) == b'\xa5'*16
            assert bytes(cpu.mem_read(STACK+8, 264)) == b'\xa5'*264
            values.append(dict(ruin_id=n, name=name.decode('cp932'), getter=getter, title=headline, body=body))
    finally:
        cpu.hook_del(hook)
    return values


def atlas(painter, arm, title, rows):
    independent = GameAsciiFont.from_arm9(arm)
    def paint(row):
        code = bytes.fromhex(row['text'])
        glyph_events = []
        plane = painter(arm, code, 0xD5404, size=(WIDTH,16), instruction_limit=1_000_000, glyph_events=glyph_events)
        assert [p['code'] for p in glyph_events if p['code'] != 32] == glyph_codes(code)
        assert glyph_codes(code)[0] == code[0] and glyph_codes(code)[-1] == code[-1]
        shifted = bytearray(WIDTH*16)
        own = bytearray(WIDTH*16)
        for i, char in enumerate(code.decode('ascii')):
            glyph = independent.decode(char)
            for y in range(11):
                for x in range(6):
                    own[(y+1)*WIDTH + i*6 + x] = bool(glyph.getpixel((x,y)))
        assert plane == own, (code, sum(plane), sum(own))
        for y in range(16):
            off = y*WIDTH
            shifted[off+row['x']:off+row['x']+len(code)*6] = plane[off:off+len(code)*6]
        return bytes(shifted)

    entries = [(title, 'Heading')] + [(row['body'], row['name']) for row in rows]
    image = Image.new('RGB', (530*2, 52*((len(entries)+1)//2)), '#242932')
    draw = ImageDraw.Draw(image)
    for n, (row, label) in enumerate(entries):
        bitmap = paint(row)
        row['ink_sha256'] = batch.digest(bitmap)
        x,y = 530*(n%2),52*(n//2)
        draw.text((x+5,y+2), label, fill='white')
        block = Image.frombytes('L',(WIDTH,16),bytes(0 if ink else 255 for ink in bitmap))
        image.paste(block.resize((512,32),Image.Resampling.NEAREST),(x+5,y+17))
    image.save(SHEET)


def main():
    assert not OUTPUT.exists() and not SHEET.exists()
    proof = batch.load(stage.PROOF)
    old_release = batch.load(stage.parent.RELEASE)
    old_startup = batch.load(old_release['own_registered_startup'])
    locator = old_startup['read_only_snapshot']
    raw = Path(locator['path']).read_bytes()
    assert batch.digest(raw) == locator['sha256'] and locator['read_only_export']
    clean, prior, target = map(batch.NdsImage.open, (batch.CLEAN, stage.parent.ROM, stage.ROM))
    clean_arm, old_arm, new_arm = [rom.read_file(batch.ARM) for rom in (clean, prior, target)]
    assert stage.patch(old_arm, clean_arm)[0] == new_arm and digest(stage.ROM) == proof['candidate_sha256']
    prior_rows = composed(old_arm, raw, True, stage.SOURCE_TITLE.encode('cp932'), stage.SOURCE_SUFFIX.encode('cp932'))
    mapped = bytearray(raw)
    for off, (size, _, _) in stage.STRINGS.items():
        assert raw[off:off+size] == old_arm[off:off+size]
        mapped[off:off+size] = new_arm[off:off+size]
    at = stage.POWER_CALL - stage.BASE
    assert raw[at:at+4] == old_arm[at:at+4]
    mapped[at:at+4] = new_arm[at:at+4]
    mapped = bytes(mapped)
    names = composed(new_arm, mapped, False, stage.TITLE, stage.SUFFIX)
    assert [n['name'] for n in names] == [n['name'] for n in prior_rows]
    assert len({n['name'] for n in names}) == len(names) == 21
    painter, _, font = font_tools(target)
    title = names[0]['title']
    assert all(row['title'] == title for row in names)
    atlas(painter, new_arm, title, names)

    old_cpu, _ = get_machine(old_arm, raw)
    new_cpu, _ = get_machine(new_arm, mapped)
    verify = FunctionType(digits.verify_numbers.__code__, digits.verify_numbers.__globals__ |
                          {'CASES': {stage.POWER_CALL: AMOUNTS}})
    ring = verify(old_cpu, new_cpu)
    assert len(ring) == 320
    common = target.read_file(batch.COMMON)
    assert prior.read_file(batch.COMMON) == common
    current = batch.owned_entries(common, new_arm, batch.digest(new_arm[batch.DIRECTORY_OFFSET:batch.TABLE_OFFSET]))
    source = batch.common_message_entries(clean.read_file(batch.COMMON), clean_arm)
    sources = source[stage.POWER_NOTICE]
    installed = current[stage.POWER_NOTICE]
    assert installed.text == b'Power increased by %s.' and sources.text.count(b'%s') == 1
    kanji = target.read_file('/GRP/KANJI.FNT')
    samples, pages = [], []
    for number in AMOUNTS:
        new_cpu.reg_write(UC_ARM_REG_SP, STACK)
        new_cpu.reg_write(UC_ARM_REG_R8, number)
        new_cpu.emu_start(0x020610D8, 0x020610E8, count=30_000)
        assert new_cpu.reg_read(UC_ARM_REG_PC) == 0x020610E8 and new_cpu.reg_read(UC_ARM_REG_R0) == stage.POWER_NOTICE
        ptr = new_cpu.reg_read(UC_ARM_REG_R1)
        text = bytes(new_cpu.mem_read(ptr, 24)).split(b'\0', 1)[0]
        assert text == str(number).encode('ascii')
        result = digits.prepare_notice(new_cpu, stage.POWER_NOTICE, installed.text, (text,),
                                       tuple(int.from_bytes(new_arm[x:x+4],'little') for x in (0x54890,0x54894)))
        ink, glyphs = render_portrait(painter, new_arm, kanji, result)
        assert [g['code'] for g in glyphs] == glyph_codes(result)
        assert glyphs[0]['code'] == ord('P') and glyphs[-1]['code'] == ord('.')
        pages.append((f'Power / {number}', ink))
        samples.append(dict(amount=number, display=result.decode('ascii'), ink_sha256=batch.digest(ink)))
    sheets = portrait_sheets(stage.ROOT, pages)
    batch.write(OUTPUT, dict(candidate_sha256=proof['candidate_sha256'], source_snapshot=locator,
        original_centering_and_draw_handoff_preserved=True, old_cases=prior_rows, current_cases=names, font=font,
        name_sheet=str(SHEET), name_sheet_sha256=digest(SHEET),
        power_notice=dict(message_ID=stage.POWER_NOTICE, source_Japanese=sources.text.decode('cp932'),
          source_reference=reference(sources), current_reference=reference(installed),
          source_hex=sources.text.hex(), current_hex=installed.text.hex(), native_ring_cases=ring,
          cases=samples, sheets=sheets), offline=True, new_credit=0))
    print('Both native draw calls, 21 complete ruin names and 10 power increments passed.')


if __name__ == '__main__':
    main()
