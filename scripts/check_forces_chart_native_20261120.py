"""Check all chart states and regional Power limits on the original painter."""

from pathlib import Path
from struct import pack, unpack_from

from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R5, UC_ARM_REG_R6
from unicorn.arm_const import UC_ARM_REG_R8, UC_ARM_REG_R9, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts import replay_forces_relationships_20261115 as history
from scripts import stage_forces_chart_fields_20261120 as stage
from scripts.verify_forces_relationships_20261115 import BOX, HEADER, STACK, VIEW, font_points
from scripts.verify_inn_numerals_native_20261119 import read_cstring


BASE = stage.runtime.BASE
OUTPUT, SHEET = stage.ROOT / 'native_fields.json', stage.ROOT / 'native_fields.png'
SIZE = 256 * 192 // 2
DRAW = 0x020D5404
CONTEXT = STACK + 0x27C

# Start at each original field's condition, including the home and ties getters.
# The stop PCs are the original common points after the draw.
STATIC = {
    'UNKNOWN_LEADER': ('?', 84, 30, 0x08CF3C, 0x08D074, 0),
    'UNKNOWN_LEVEL': ('?', 132, 80, 0x08D0A4, 0x08D0E4, 0),
    'UNKNOWN_FUNDS': ('?', 56, 108, 0x08D150, 0x08D190, 0),
    'UNKNOWN_POWER': ('?', 56, 128, 0x08D190, 0x08D230, 0),
    'UNKNOWN_HOME': ('?', 56, 148, 0x08D230, 0x08D2A4, 0),
    'NO_HOME': ('None', 56, 148, 0x08D230, 0x08D2A4, 3),
    'SELF_TIES': ('-', 56, 168, 0x08D2A4, 0x08D2F8, 3),
}


def machine(arm, raw, model):
    cpu, get = history.get_machine(arm, raw)
    company = get(0xCB160) + 4
    assert get(0x397D8) == 0 and get(0x3CD24, company) != 0x73
    if model == 'NO_HOME':
        cpu.mem_write(company + 11, b'\x73')
    header = pack('<5I', 4, 256 // 4, 192, 20, 20)
    cpu.mem_write(HEADER - 16, b'\xa5' * 16 + header + bytes(SIZE) + b'\xa5' * 16)
    get(0xD3D80, VIEW)
    cpu.mem_write(STACK, pack('<4I', 256, 192, 0, 0))
    get(0xD3AFC, VIEW, HEADER, 0, 0)
    get(0xD5160, CONTEXT, VIEW, 1)
    return cpu, get, company, header


def run(cpu, font, spec, header):
    identifier, text, x, y, start, end, knowledge, company = spec
    cpu.mem_write(CONTEXT + 0x24, pack('<2I', x, y))
    cpu.reg_write(UC_ARM_REG_R6, company)
    cpu.reg_write(UC_ARM_REG_R8, knowledge)
    cpu.reg_write(UC_ARM_REG_R9, 0)
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    calls = []

    def watch(uc, _pc, _size, _data):
        at, src = [uc.reg_read(reg) for reg in (UC_ARM_REG_R0, UC_ARM_REG_R1)]
        calls.append([at, read_cstring(uc, src)])

    hook = cpu.hook_add(UC_HOOK_CODE, watch, begin=DRAW, end=DRAW)
    try:
        cpu.emu_start(BASE + start, BASE + end, count=200000)
    finally:
        cpu.hook_del(hook)
    assert cpu.reg_read(UC_ARM_REG_PC) == BASE + end and cpu.reg_read(UC_ARM_REG_SP) == STACK
    if identifier != 'REGIONAL_POWER':
        assert calls == [[CONTEXT, text.encode('ascii')]]
    assert bytes(cpu.mem_read(HEADER, 20)) == header
    assert bytes(cpu.mem_read(HEADER - 16, 16)) == bytes(cpu.mem_read(HEADER + 20 + SIZE, 16)) == b'\xa5' * 16
    pixels = bytes(n for b in cpu.mem_read(HEADER + 20, SIZE) for n in (b & 15, b >> 4))
    observed = {(i % 256, i // 256) for i, px in enumerate(pixels) if px}
    expected = font_points(font, text, x, y + 1)
    assert observed == expected, (identifier, text, min(observed), min(expected),
                                  len(expected - observed), len(observed - expected))
    assert text and x + len(text) * 6 <= 256 and y + 12 <= BOX[3]
    ink = min(px for px in pixels if px)
    assert set(pixels) == {0, ink}
    image = Image.frombytes('L', (256, 192), pixels).crop((x, y, 256, y + 13)).point(lambda p: 246 if p else 32)
    return dict(field=identifier, text=text, origin=[x, y], byte_length=len(text), painted_pixels=len(observed),
                native_bounds=[x, y, x + len(text) * 6, y + 12], full_glyph_plane=True,
                exact_calls=[[at, text.hex()] for at, text in calls]), image


def main():
    assert not OUTPUT.exists() and not SHEET.exists()
    stored = stage.batch.load(stage.PROOF)
    history_report = stage.batch.load(history.REFERENCE)
    assert stage.parent.base.digest(stage.ROM) == stored['candidate_sha256']
    snapshot, = [r for r in history_report['read_only_capture_RAM_snapshots'] if r['frame'] == 13280]
    assert snapshot['read_only_export'] and stage.parent.base.digest(snapshot['path']) == snapshot['sha256']
    raw = bytearray(Path(snapshot['path']).read_bytes())
    arm = stage.batch.NdsImage.open(stage.ROM).read_file(stage.batch.ARM)
    for row in stored['rows']:
        offset, n = row['offset'], row['slot_bytes']
        assert raw[offset:offset + n] == bytes.fromhex(row['source_and_current_hex'])
        raw[offset:offset + n] = arm[offset:offset + n]
    font = GameAsciiFont.from_arm9(arm)
    cases = [(kind, *spec, None, None) for kind, spec in STATIC.items()]
    for region in range(7):
        cases.extend(('REGIONAL_POWER', None, 56, 128, 0x08D1D8, 0x08D214, 3, region, v)
                     for v in (0, 122, 9999))
    sheet = Image.new('RGB', (939, 49 * ((len(cases) + 1) // 2)), '#263238')
    draw = ImageDraw.Draw(sheet)
    results = []
    for i, (identifier, text, x, y, start, end, knowledge, region, site_power) in enumerate(cases):
        cpu, get, company, header = machine(arm, bytes(raw), identifier)
        if region is not None:
            name = read_cstring(cpu, unpack_from('<I', cpu.mem_read(get(0x945B4, region), 4))[0]).decode('ascii')
            cap = unpack_from('<I', arm, 0x3CC70)[0]
            assert cap == 9999 or site_power == 0
            cpu.mem_write(company + 16, pack('<7H', *([site_power] * 7)))
            total = get(0x3CBFC, company)
            assert total == 7 * site_power and get(0x3CC74, company, region) == site_power
            cpu.reg_write(UC_ARM_REG_R9, 0)
            from unicorn.arm_const import UC_ARM_REG_R7
            cpu.reg_write(UC_ARM_REG_R7, region)
            text = f'{total} ({name}: {site_power})'
        receipt, image = run(cpu, font, (identifier, text, x, y, start, end, knowledge, company), header)
        receipt.update(region=region, regional_power=site_power)
        label = identifier.replace('_', ' ').title()
        if region is not None:
            label = f'{label} / {name.strip()} / {site_power}'
        xp, yp = i % 2 * 469, i // 2 * 49
        draw.text((xp + 6, yp + 1), label, fill='white')
        sheet.paste(image.resize((image.width * 2, 26), Image.Resampling.NEAREST), (xp + 6, yp + 17))
        results.append(receipt)
    sheet.save(SHEET)
    stage.batch.write(OUTPUT, dict(candidate_sha256=stored['candidate_sha256'], snapshot=snapshot,
        exact_original_regional_caps=True, substitutions_and_original_format_preserved=True, cases=results,
        complete_one_line_glyphs_and_allocation=True, native_not_gameplay=True, sheet=str(SHEET),
        sheet_sha256=stage.parent.base.digest(SHEET)))
    print(f'{len(results)} original chart draw paths passed with complete glyphs and bounds.')


if __name__ == '__main__':
    main()
