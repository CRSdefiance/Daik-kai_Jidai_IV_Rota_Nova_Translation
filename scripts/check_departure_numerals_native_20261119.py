"""Verify each patched departure call, original varargs, and complete native glyphs."""

from itertools import product
from pathlib import Path
from struct import pack, unpack
from types import FunctionType, SimpleNamespace

from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1
from unicorn.arm_const import UC_ARM_REG_R2, UC_ARM_REG_R3, UC_ARM_REG_SP

from scripts import probe_escape_direct_source_v1186 as provider
from scripts import stage_departure_numerals_20261119 as stage
from scripts import stage_inn_numerals_20261119 as inn
from scripts.preflight_shared_dynamic_notice_wrap_v1 import font_tools, native_catalog, render
from scripts.probe_button_prompt_native import STACK, STOP
from scripts.verify_inn_numerals_native_20261119 import RING, RING_SIZE, normalize, read_cstring, save_sheets

base, native = stage.base, stage.native
ROOT = stage.ROOT / 'native_display'
PROOF = ROOT / 'native_display.json'
HISTORY = Path('translations/editorial_checkpoints/SharedText_20261110_v1/stored_notices_v1/checkpoint.json')
WRAPPER = 0x020546B8
FORMAT = 0x02054774
PREPARED = 0x0205479C
CASES = {0x02060BEC: (0, 1, 5, 9, 10, 15, 20, 99, 100, 999, 2147483647),
         0x0207A2E4: tuple(range(1, 13)), 0x0207A2F4: tuple(range(1, 32))}


def patched_snapshot(ctx, arm):
    raw = bytearray(ctx.raw)
    for pc in stage.SITES:
        at = pc - stage.BASE
        assert raw[at:at + 4] == ctx.arm[at:at + 4]
        raw[at:at + 4] = arm[at:at + 4]
    return bytes(raw)


def verify_numbers(old, new):
    ring = bytes(old.mem_read(RING, RING_SIZE))
    assert ring == bytes(new.mem_read(RING, RING_SIZE))
    checked = []
    for site, values in CASES.items():
        for slot, number in product(range(32), values):
            results = []
            for cpu in (old, new):
                cpu.mem_write(RING, ring[:8] + pack('<I', slot) + ring[12:])
                cpu.reg_write(UC_ARM_REG_SP, STACK)
                cpu.reg_write(UC_ARM_REG_R0, number)
                cpu.emu_start(site, site + 4, count=10000)
                assert cpu.reg_read(UC_ARM_REG_PC) == site + 4 and cpu.reg_read(UC_ARM_REG_SP) == STACK
                ptr = cpu.reg_read(UC_ARM_REG_R0)
                results.append((ptr, read_cstring(cpu, ptr), bytes(cpu.mem_read(RING, RING_SIZE))))
            (a, wide, before), (b, digits, after) = results
            assert a == b and a + len(wide) == RING + 12 + 128 * (slot + 1) - 1
            assert digits == normalize(wide) == str(number).encode('ascii')
            offset = a - RING
            assert before[:offset] == after[:offset] and before[offset + len(digits) + 1:] == after[offset + len(digits) + 1:]
            checked.append(dict(call=site, slot=slot, number=number, result_pointer=a,
                                original_hex=wide.hex(), current_hex=digits.hex()))
    return checked


def prepare_notice(cpu, message, template, arguments, buffers):
    scratch = 0x02660300
    pointers = [scratch + i * 64 for i in range(len(arguments))]
    for address, text in zip(pointers, arguments, strict=True):
        cpu.mem_write(address - 4, b'\xa5' * 4 + text + b'\0' + b'\xa5' * 4)
    cpu.mem_write(STACK, pack('<I', pointers[3] if len(pointers) == 4 else 0))
    cpu.reg_write(UC_ARM_REG_SP, STACK)
    cpu.reg_write(UC_ARM_REG_LR, STOP)
    registers = (UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3)
    for reg, value in zip(registers, ([message] + pointers + [0] * 3)[:4], strict=True):
        cpu.reg_write(reg, value)
    seen = []

    def inspect_format(u, pc, size, _):
        ptr = u.reg_read(UC_ARM_REG_R1)
        assert bytes(u.mem_read(ptr, len(template) + 1)) == template + b'\0'
        vector = u.reg_read(UC_ARM_REG_R2)
        assert unpack(f'<{len(pointers)}I', u.mem_read(vector, len(pointers) * 4)) == tuple(pointers)
        seen.append(pc)

    for pointer in buffers:
        cpu.mem_write(pointer - 16, b'\xa5' * 288)
    hook = cpu.hook_add(UC_HOOK_CODE, inspect_format, begin=FORMAT, end=FORMAT)
    try:
        cpu.emu_start(WRAPPER, PREPARED, count=3000000)
    finally:
        cpu.hook_del(hook)
    assert cpu.reg_read(UC_ARM_REG_PC) == PREPARED and seen == [FORMAT]
    wanted = template % arguments
    raw = [bytes(cpu.mem_read(p, 256)).split(b'\0', 1)[0] for p in buffers]
    assert raw == [wanted, wanted], raw
    for pointer in buffers:
        assert bytes(cpu.mem_read(pointer - 16, len(wanted) + 33)) == b'\xa5' * 16 + wanted + b'\0' + b'\xa5' * 16
    for address, text in zip(pointers, arguments, strict=True):
        assert bytes(cpu.mem_read(address - 4, len(text) + 9)) == b'\xa5' * 4 + text + b'\0' + b'\xa5' * 4
    return wanted


def layout_models(template, towns, skies):
    # No month or day exceeds two digits. Model every calendar field, sky and town together.
    count = 0
    for date, sky, name in product(((str(m).encode(), str(d).encode()) for m in range(1, 13) for d in range(1, 32)), skies, towns):
        rows = (template % (*date, sky, name)).split(b'\n')
        assert len(rows) == 3 and all(row.isascii() and len(row.strip()) <= 35 for row in rows)
        count += 1
    return count


def main():
    assert not ROOT.exists()
    proof, previous = map(base.load, (stage.PROOF, stage.parent.RELEASE))
    assert base.digest(stage.ROM) == proof['candidate_sha256']
    ctx = native.RegisteredRuntime(stage.parent.RELEASE, previous['own_registered_startup'], captain=3)
    assert ctx.release['candidate_sha256'] == proof['predecessor_sha256']
    rom, clean = map(base.NdsImage.open, (stage.ROM, native.CLEAN))
    arm = rom.read_file(stage.ARM)
    assert native.digest(arm) == proof['target_ARM9_sha256'] and rom.read_file(stage.COMMON) == ctx.common
    raw = patched_snapshot(ctx, arm)
    old, _, _ = provider.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    new, _, _ = provider.machine(arm, ctx.common, raw, ctx.plan)
    checked = verify_numbers(old, new)
    assert len(checked) == 32 * sum(map(len, CASES.values()))
    catalog = native_catalog(ctx)
    towns = [r['name'].encode('ascii') for r in catalog['towns']]
    skies = [sky.encode('ascii') for sky in catalog['sky']]
    assert b'Ceuta' in towns and b'Sky: Sunny' in skies
    w = inn.workflow
    directory = native.digest(arm[w.DIRECTORY_OFFSET:w.TABLE_OFFSET])
    current = w.owned_entries(ctx.common, arm, directory)
    source = w.common_message_entries(clean.read_file(stage.COMMON), clean.read_file(stage.ARM))
    old_records = {r['message_ID']: r for r in base.load(HISTORY)['records']}
    cases = {85: [(str(n).encode(),) for n in (0, 1, 20, 100, 2147483647)],
             86: [(b'1', b'23', b'Sky: Sunny', b'Ceuta'), (b'12', b'31', max(skies, key=len), max(towns, key=len))]}
    buffers = unpack('<2I', arm[0x54890:0x54898])
    raster, _, font = font_tools(rom)
    kanji = rom.read_file('/GRP/KANJI.FNT')
    previews, records = [], []
    for message, options in cases.items():
        original = old_records[message]
        template = current[message].text
        assert template.hex() == original['target_hex'] and source[message].text.hex() == original['source_hex']
        layouts = []
        for values in options:
            expanded = prepare_notice(new, message, template, values, buffers)
            expected_rows = 1 if message == 85 else 3
            assert len(expanded.split(b'\n')) == expected_rows
            pixels, events = render(raster, arm, kanji, expanded)
            assert all(event['code'] < 128 and event['x'] < 216 for event in events)
            label = expanded.decode('ascii').replace('\n', ' // ')
            previews.append((f'{message}  {label}', pixels + bytes(228 * 16)))
            layouts.append(dict(arguments=[arg.decode('ascii') for arg in values], expanded_hex=expanded.hex(),
                plane_sha256=native.digest(pixels), complete_buffer_and_glyph_bounds=True, pages=1))
        source_ref, current_ref = w.reference(source[message]), w.reference(current[message])
        records.append(dict(id=original['id'], message_ID=message, file_path=stage.COMMON, speaker='System',
            context='Departing port after supplies and readiness are checked.', source_Japanese=original['source_Japanese'],
            source_meaning=('Approximate remaining sailing range in days.' if message == 85 else
                            'Month and day, current sky conditions, and the town just departed.'),
            english=original['english'], source_reference=source_ref, current_reference=current_ref,
            registered_reference=current_ref | dict(candidate_sha256=proof['candidate_sha256']),
            source_hex=source[message].text.hex(), current_hex=template.hex(), decision='retention',
            localization_note=original['rationale'] + ' Only the native argument digit width is updated.',
            manual_break_reason=original['layout_reason'] or None, review=original['review'] | dict(formatting=True),
            layout_cases=layouts))
    matrix = layout_models(current[86].text, towns, skies)
    ROOT.mkdir()
    sheets = FunctionType(save_sheets.__code__, save_sheets.__globals__ | {'stage': SimpleNamespace(ROOT=ROOT)})(previews)
    receipt = dict(candidate_sha256=proof['candidate_sha256'], predecessor_sha256=proof['predecessor_sha256'],
        translation_policy='natural-dialogue-v2', encoder='dialogue-relocatable-v1', target_locale='en-US',
        review_gates=['source', 'context', 'localization', 'naturalness', 'formatting'], records=records,
        executed_num_cases=checked, modeled_date_sky_town_combinations=matrix, sheets=sheets, font_contract=font,
        evidence={str(p): base.digest(p) for p in (stage.PROOF, HISTORY, Path(__file__))})
    base.save(PROOF, receipt)
    print(f'Checked {len(checked)} native number calls and seven native displays. Modeled {matrix} date, sky and town combinations.')


if __name__ == '__main__':
    main()
