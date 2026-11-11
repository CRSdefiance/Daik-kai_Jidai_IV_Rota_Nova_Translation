"""Prove the scoped notice selector and render runtime substitutions offline."""

import argparse
import struct
from itertools import product
from pathlib import Path
from types import SimpleNamespace

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw
from unicorn import UC_HOOK_CODE
from unicorn.arm_const import UC_ARM_REG_LR, UC_ARM_REG_PC, UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_SP

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.patch.shared_notice_wrap_v1 import MESSAGE_IDS, NOTICE_PARENT, SELECTOR, transform
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_literal_static_layout_v1 import ENTRY, HEIGHT, WIDTH
from scripts.preflight_literal_notice_formatting_v1 import ARCHIVE, OUTPUT, run_case
from scripts.primary_town_native_font_v2102 import font_tools, glyph_codes
from scripts.probe_button_prompt_native import STACK, STOP, machine
from scripts.probe_regional_policy_wrap_v616 import DEST, TEXT
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.stage_ship_command_release_v1 import RELEASE, STARTUP
from scripts.verify_shipyard_gameplay_v760 import SJIS_GLYPH_COUNT, SJIS_MAP_OFFSET, decode_glyph


PRIOR = Path('work/SharedText_20261110_v1/dynamic_notice_layout_v1')
ROOT = PRIOR.with_name('dynamic_notice_layout_v3')
PRIOR_LAYOUT = PRIOR.with_name('dynamic_notice_layout_v2') / 'native_preflight.json'
AMENDMENTS = {
    85: ('Sailing days left: about %s.', 'Use a count label so the singular value 1 reads naturally. '
        'Keep the approximation and the remaining sailing range.'),
    87: ('%s skill is too low.', 'Both original calls supply a named skill, including the Command fallback. '
        'Naming the skill explicitly gives Swords a singular subject and avoids implying missing equipment.'),
    90: ('%s was defeated...', 'The displayed place already identifies the town. Keep the military defeat '
        'and subdued ellipsis distinct from surrender, and keep the full short report together.'),
    93: ('%s has a fleet from %s under fire.', 'Keep the named town as attacker and the named company as '
        'the fleet affiliation. Placing the company inside the sentence handles names ending in Co.'),
    95: ('In %s, %s gained market share by selling a lot of %s!', 'The seller gained market share through '
        'large sales. Keep the argument order and plain ASCII In. Place the result before its cause '
        'to avoid the fourth row found with long catalog names.'),
}


def manuscript():
    rows = {row['message_ID']: row for row in load(OUTPUT)['records'] if row['native_substitution_count']}
    prior = {row['message_ID']: row['after'] for row in
             load(ARCHIVE / 'literal_notice_amendments_v1.json')['amended_records']}
    findings = []
    for number, (english, reason) in AMENDMENTS.items():
        row = rows[number]
        findings.append(dict(message_ID=number, previous_proposed_English=prior.get(number, row['english']),
            revised_English=english, rationale=reason, source_reference=row['source_reference'],
            current_reference=row['current_reference'], source_hex=row['source_hex'], current_hex=row['current_hex']))
        rows[number] = {**row, 'english': english}
    # The existing date template deliberately gives date, sky, and departure their own rows.
    rows[86]['english'] = bytes.fromhex(rows[86]['current_hex']).decode('cp932').replace('\n', '{LB}')
    assert len(rows) == 11
    return rows, findings


def native_catalog(ctx):
    cpu, get, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)

    def pointer(address):
        return struct.unpack('<I', cpu.mem_read(address, 4))[0]

    def string(address):
        return bytes(cpu.mem_read(address, 128)).split(b'\0', 1)[0].decode('cp932')

    catalog = {}
    for kind, getter, count, stride in (
        ('towns', 0xCB178, 90, 108), ('goods', 0xCB124, 124, 16), ('companies', 0xCB160, 20, 76)
    ):
        root = get(getter) + 4
        entries = []
        for index in range(count):
            obj = root + index * stride
            name_getter = pointer(pointer(obj) + 8)
            name = string(get(name_getter - BASE, obj))
            assert name and name.isascii()
            entries.append(dict(index=index, name=name, native_name_getter=name_getter))
        catalog[kind] = entries
    catalog['sky'] = [string(p) for p in struct.unpack_from('<3I', ctx.arm, 0x7A050)]
    catalog['requirements'] = sorted({string(get(0x7EEB0, i)) for i in range(10)})
    catalog['number_samples'] = {value: string(get(0xABF50, value)) for value in (1, 9, 12, 30, 31, 99, 123)}
    catalog['pirate_short_name_samples'] = []
    for index in (34, 69):
        obj = ctx.actor_root + 4 + index * 32
        getter = pointer(pointer(obj) + 0x20)
        catalog['pirate_short_name_samples'].append(dict(actor=index, name=string(get(getter - BASE, obj)),
            native_name_getter=getter))
    ctx.calls.clear()
    return catalog


def eligible_model(text, paragraph):
    if not paragraph:
        return [row.strip() for row in text.splitlines()]
    lines = ['']
    for word in text.split():
        current = lines[-1]
        candidate = f'{current} {word}' if current else word
        if len(candidate.encode('cp932')) <= (36 if len(lines) == 1 else 35):
            lines[-1] = candidate
        else:
            lines.append(word)
    return lines


def catalog_cases(rows, catalog):
    towns, companies, goods = (
        sorted({r['name'] for r in catalog[kind]}) for kind in ('towns', 'companies', 'goods')
    )
    domains = {
        87: (catalog['requirements'],), 90: (towns,), 91: (towns,), 93: (towns, companies),
        95: (towns, companies, goods), 96: (companies,), 125: (towns,), 126: (towns,),
    }
    groups = {}
    extremes = {}
    for number, domain in domains.items():
        count = 0
        selected = {}
        for args in product(*domain):
            text = rows[number]['english'] % args
            lines = eligible_model(text, number in MESSAGE_IDS)
            widths = [len(line.encode('cp932')) for line in lines]
            assert 1 <= len(lines) <= 3 and all(0 < w <= (36 if i == 0 else 35)
                for i, w in enumerate(widths)), (number, args, lines)
            count += 1
            key = len(lines), tuple(width % 2 for width in widths)
            rank = len(text), max(widths), args
            if key not in selected or rank > selected[key][0]:
                selected[key] = rank, args
        groups[number] = count
        extremes[number] = sorted({args for _, args in selected.values()})
    return groups, extremes


def verify_dispatch(original, changed):
    machines = []
    for arm in (original, changed):
        cpu = machine(arm)
        sections = MainCodeFile(arm, BASE).sections
        cpu.mem_write(POOL, bytes(sections[3].data[:-48]))
        machines.append(cpu)

    text = b'These instructions contain several complete words and preserve every leading and final character.'

    def run_selector(cpu, parent, number):
        source = b'\xa5' * 16 + text + b'\0' + b'\xa5' * 16
        cpu.mem_write(TEXT - 16, source)
        cpu.mem_write(DEST - 16, b'\xa5' * 288)
        for offset, value in ((0xC4, parent), (0xCC, 0), (0xD0, number)):
            cpu.mem_write(STACK + offset, struct.pack('<I', value))
        for register, value in ((UC_ARM_REG_SP, STACK), (UC_ARM_REG_LR, STOP), (UC_ARM_REG_R0, DEST),
                               (UC_ARM_REG_R1, TEXT), (UC_ARM_REG_R2, 0)):
            cpu.reg_write(register, value)
        executed = []
        hook = cpu.hook_add(UC_HOOK_CODE, lambda _, address, size, data: executed.append(address))
        try:
            cpu.emu_start(0x01FFC828, STOP, count=50000)
        finally:
            cpu.hook_del(hook)
        assert cpu.reg_read(UC_ARM_REG_PC) == STOP and cpu.reg_read(UC_ARM_REG_SP) == STACK
        assert bytes(cpu.mem_read(TEXT - 16, len(source))) == source
        assert bytes(cpu.mem_read(DEST - 16, 16)) == bytes(cpu.mem_read(DEST + 256, 16)) == b'\xa5' * 16
        result = bytes(cpu.mem_read(DEST, 256))
        assert b'\0' in result
        return result, tuple(address for address in executed if not SELECTOR <= address < SELECTOR + 0x100)

    for number in range(3668):
        before, after = (run_selector(cpu, NOTICE_PARENT, number) for cpu in machines)
        if number in MESSAGE_IDS:
            assert 0x01FFCA00 not in before[1] and 0x01FFCA00 in after[1] and after[0] != before[0], number
            assert b' '.join(after[0].split(b'\0')[0].split()) == text, number
        else:
            assert before == after, number
    other_parents = (0x0205469C, 0x02054720, 0x02054764, 0x02054014)
    for parent, number in product(other_parents, MESSAGE_IDS):
        before, after = (run_selector(cpu, parent, number) for cpu in machines)
        assert before == after, (parent, number)
    return dict(notice_parent_IDs=3668, exact_legacy_results=3668 - len(MESSAGE_IDS),
        new_formatter_results=list(MESSAGE_IDS), unchanged_other_parent_cases=len(other_parents) * len(MESSAGE_IDS))


def render(raster, arm, kanji, raw):
    events = []
    pixels = raster(arm, raw, ENTRY, size=(WIDTH, HEIGHT), instruction_limit=2000000, glyph_events=events)
    visible = [event for event in events if event['code'] != 32]
    assert [event['code'] for event in visible] == glyph_codes(raw)
    font = GameAsciiFont.from_arm9(arm)
    mapping = struct.unpack_from(f'<{SJIS_GLYPH_COUNT}H', arm, SJIS_MAP_OFFSET)
    expected = bytearray(WIDTH * HEIGHT)
    lines = raw.decode('cp932').split('\n')
    assert 1 <= len(lines) <= 3
    cursor = 0
    for row, line in enumerate(lines):
        y = row * 16
        body = line.strip()
        x = visible[cursor]['x']
        assert x in (0, 6) and x + len(body.encode('cp932')) * 6 <= 216
        for char in body:
            encoded = char.encode('cp932')
            if char != ' ':
                code = int.from_bytes(encoded, 'big')
                assert visible[cursor] == dict(code=code, style=1, x=x, y=y)
                cursor += 1
                if len(encoded) == 1:
                    glyph = font.decode(char)
                    for gy in range(glyph.height):
                        for gx in range(glyph.width):
                            if glyph.getpixel((gx, gy)):
                                expected[(y + gy + 1) * WIDTH + x + gx] = 1
                else:
                    glyph = decode_glyph(kanji, mapping.index(code))
                    for gy in range(11):
                        for gx in range(glyph.width):
                            if glyph.getpixel((gx, gy)):
                                expected[(y + gy + 1) * WIDTH + x + gx + 1] = 15
                    for gy in range(11):
                        for gx in range(glyph.width):
                            if glyph.getpixel((gx, gy)):
                                expected[(y + gy) * WIDTH + x + gx] = 1
            x += 6 * len(encoded)
    assert cursor == len(visible) and pixels == bytes(expected), (raw, visible)
    return pixels, visible


def contact_sheets(results):
    sheets = []
    for offset in range(0, len(results), 12):
        batch = results[offset:offset + 12]
        sheet = Image.new('RGB', (936, 122 * ((len(batch) + 1) // 2)), '#263238')
        draw = ImageDraw.Draw(sheet)
        for index, case in enumerate(batch):
            x, y = index % 2 * 468, index // 2 * 122
            draw.text((x + 4, y + 3), f"{offset + index + 1}. ID {case['message_ID']}", fill='white')
            with Image.open(case['preview']) as page:
                sheet.paste(page.resize((456, 96), Image.Resampling.NEAREST), (x + 4, y + 19))
        path = ROOT / f'sheet_{offset // 12 + 1:02d}.png'
        sheet.save(path)
        sheets.append(dict(path=str(path), sha256=digest(path), pages=len(batch)))
    return sheets


def pagination(raster, arm, kanji, raw):
    pages = []
    remaining = raw
    while remaining:
        pixels, consumed = raster(arm, remaining, ENTRY, size=(WIDTH, HEIGHT), complete=False,
            instruction_limit=2000000)
        assert consumed > 0
        segment = remaining[:consumed]
        remaining = remaining[consumed:]
        if remaining:
            assert segment.endswith(b'\n') and remaining.startswith(b'  ')
        expected, glyphs = render(raster, arm, kanji, segment.removesuffix(b'\n'))
        assert pixels == expected
        pages.append(dict(visible_text=segment.decode('cp932').splitlines(), consumed_bytes=consumed,
            remaining_bytes=len(remaining), glyphs=glyphs, pixels=pixels))
    return pages


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fresh-dispatch', action='store_true')
    args = parser.parse_args()
    assert not ROOT.exists()
    ctx = RegisteredRuntime(RELEASE, STARTUP, captain=3)
    binding = ctx.receipt()
    catalog = native_catalog(ctx)
    rows, findings = manuscript()
    model, cases = catalog_cases(rows, catalog)
    original = ctx.arm
    ctx.arm, ownership = transform(original)
    dispatch_proof = PRIOR / 'native_preflight.json'
    previous = load(dispatch_proof)
    assert previous['registered_input'] == binding and previous['research_transform'] == ownership
    assert digest(PRIOR / 'ARM9_RESEARCH_ONLY.bin') == ownership['target_ARM9_sha256']
    dispatch = verify_dispatch(original, ctx.arm) if args.fresh_dispatch else previous['dispatch']
    assert dispatch == dict(notice_parent_IDs=3668, exact_legacy_results=3662,
        new_formatter_results=list(MESSAGE_IDS), unchanged_other_parent_cases=24)
    sections = MainCodeFile(ctx.arm, BASE).sections
    ctx.sections = [*sections, SimpleNamespace(ramAddress=POOL, data=bytes(sections[3].data[:-48]))]
    raster, _, _ = font_tools(ctx.image)
    kanji = ctx.image.read_file('/GRP/KANJI.FNT')
    nums = catalog['number_samples']
    cases.update({
        85: [(nums[n],) for n in (1, 99, 123)],
        86: [(nums[1], nums[1], catalog['sky'][1], 'Amsterdam'),
             (nums[12], nums[31], catalog['sky'][0], 'Santo Domingo'),
             (nums[9], nums[30], catalog['sky'][2], 'Lisbon')],
        94: [(town, actor['name']) for town, actor in zip(('Lisbon', 'Santo Domingo'),
            catalog['pirate_short_name_samples'], strict=True)],
    })
    cases[93].extend([('Lisbon', 'Castor Co.'), ('Santo Domingo', 'Bergstrom Fleet')])
    cases[95].extend([('Amsterdam', 'Argot Co.', 'Wool Cloth'),
                      ('Santo Domingo', 'Bergstrom Fleet', 'North Sea Ambergris')])
    prior_layout = load(PRIOR_LAYOUT)
    assert prior_layout['registered_input'] == binding and prior_layout['research_transform'] == ownership
    reusable = {(case['message_ID'], tuple(case['arguments'])): case for case in prior_layout['records']}
    ROOT.mkdir()
    results = []
    for number, samples in sorted(cases.items()):
        for args in dict.fromkeys(samples):
            previous = reusable.get((number, args))
            if previous and number != 87:
                expected = (rows[number]['english'].replace('{LB}', '\n') % args).encode('cp932')
                assert previous['expanded_hex'] == expected.hex()
                assert digest(previous['preview']) == previous['preview_sha256']
                results.append(previous)
                continue
            case = run_case(ctx, rows[number], args)
            ctx.calls.clear()
            raw = bytes.fromhex(case['native_wrapper_output_hex'])
            if number in MESSAGE_IDS:
                assert [line.strip() for line in case['native_wrapper_lines']] == eligible_model(
                    bytes.fromhex(case['expanded_hex']).decode('cp932'), True), case
            if number == 86:
                assert raw.hex() == case['expanded_hex'], case
            assert b'..' not in raw or number in (90, 91)
            pixels, glyphs = render(raster, ctx.arm, kanji, raw)
            preview = ROOT / f"page_{len(results) + 1:03d}_ID{number}.png"
            Image.frombytes('L', (WIDTH, HEIGHT), bytes(0 if p else 255 for p in pixels)).save(preview)
            results.append(dict(**case, glyphs=glyphs, preview=str(preview), preview_sha256=digest(preview)))
    assert len({row['message_ID'] for row in results}) == 11
    stress = run_case(ctx, rows[95], ('Santo Domingo', 'ABCDEFGHIJKLMNOPQRSTUVW', 'Black Glacier Sword'))
    assert stress['over_three_rows']
    pages = pagination(raster, ctx.arm, kanji, bytes.fromhex(stress['native_wrapper_output_hex']))
    assert len(pages) == 2 and pages[-1]['remaining_bytes'] == 0
    pagination_previews = []
    for index, page in enumerate(pages, 1):
        preview = ROOT / f'ID95_synthetic_long_page_{index}.png'
        pixels = page.pop('pixels')
        Image.frombytes('L', (WIDTH, HEIGHT), bytes(0 if p else 255 for p in pixels)).save(preview)
        pagination_previews.append(dict(message_ID=95, preview=str(preview), preview_sha256=digest(preview)))
    sheets = contact_sheets([*results, *pagination_previews])
    (ROOT / 'ARM9_RESEARCH_ONLY.bin').write_bytes(ctx.arm)
    save(ROOT / 'native_preflight.json', dict(registered_input=binding, research_transform=ownership,
        dispatch=dispatch, catalog=catalog, catalog_combinations_modeled=model,
        native_wrapper_raster_pages=len(results), independent_complete_planes=True, records=results,
        rationale_and_exact_references=findings, contact_sheets=sheets,
        synthetic_23_character_company_name=dict(case=stress, pages=pages, previews=pagination_previews,
            exact_native_next_pointer_pagination=True, actual_name_entry_limit_and_transition_pending=True),
        evidence={str(p): digest(p) for p in (OUTPUT, dispatch_proof, PRIOR_LAYOUT, Path(__file__))},
        display_fixture_scope='Native offline. Original loader and varargs run with a scratch template at format entry.',
        direct_visual_review_pending=True, stored_layout_and_original_gameplay_pending=True, new_editorial_credit=0))
    print(f'{len(results)} complete native pages, {sum(model.values())} catalog combinations, '
          f'{dispatch["exact_legacy_results"]} exact unchanged dispatch results.')


if __name__ == '__main__':
    main()
