"""Stage original discovery and reward text with complete mixed-font checks."""

import inspect
from hashlib import sha256
from pathlib import Path
import struct
from types import FunctionType

from PIL import Image, ImageDraw

from dk4tool.patch.discovery_reward_wrap_v1 import transform
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END, TABLE_OFFSET
from scripts import preflight_setup_save_equipment_v1 as equipment
from scripts import preflight_shipyard_fleet_setup_v1 as fleet
from scripts import preflight_shared_dynamic_notice_wrap_v1 as mixed
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.preflight_literal_notice_formatting_v1 import run_case
from scripts.register_shipyard_fleet_setup_v1 import RELEASE
from scripts.review_discovery_rewards_v1 import OUTPUT as MANUSCRIPT
from scripts.seal_shared_text_source_v1 import ARM, COMMON, reference
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_shared_notices_storage_v1 import relocate


BASE = 0x02000000
ROOT = Path('out/discovery_rewards_staged_20261111_v1')
ROM = ROOT / 'discovery_rewards_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_verification.json'
RETAIN_STORED = {297, 341}
RAW_NOTICE = 0x0205473C
LOOKUP = 0x5528C
AMENDMENTS = {
    303: {
        'english': 'Recovered from captured ships: %s barrels of food and %s barrels of water.',
        'localization_note': 'Keep the original food-then-water amounts and the barrel unit on each resource. The summary leads into the two distinct quantities.',
    },
}


def active_rows(manuscript):
    return {row['message_ID']: row | AMENDMENTS.get(row['message_ID'], {}) for row in manuscript['records']}


def storage_text(rows):
    planned = {n: row['english'] for n, row in rows.items()}
    groups = {
        302: ("Any trade goods you don't load", 'will be discarded. Continue?'),
        303: ('Recovered from captured ships:', '%s barrels of food', 'and %s barrels of water.'),
    }
    for n, lines in groups.items():
        assert ' '.join(lines) == planned[n]
        planned[n] = '\n '.join(lines)
    planned.update({n: rows[n]['current_English'] for n in RETAIN_STORED})
    return {n: text.encode('ascii') for n, text in planned.items()}


def dynamic_samples(ctx):
    towns, _ = fleet.name_samples(ctx)
    items, _ = equipment.stock_names(ctx)
    assert items[4]['name'] == 'Baby Shark'
    cpu, get, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)

    def word(at):
        return struct.unpack('<I', cpu.mem_read(at, 4))[0]

    def text(ptr):
        return bytes(cpu.mem_read(ptr, 96)).split(b'\0', 1)[0].decode('cp932')

    villages = []
    village_root = get(0xCB118)
    for index in range(24):
        obj = get(0xCACAC, village_root, index)
        getter = word(word(obj) + 8)
        villages.append(text(get(getter - BASE, obj)))
    assert 'Inuvik' in villages
    names = []
    for index in range(4, 114):
        names.append(text(get(0x7EA8C, ctx.actor_root + 4 + index * 32)))
    values = {n: text(get(0xABF50, n)) for n in (1, 9, 20, 21, 29, 100, 190, 250, 399, 400, 409, 2147483647)}
    assert all(value == str(n).translate(str.maketrans('0123456789', '０１２３４５６７８９'))
               for n, value in values.items())
    ctx.calls.clear()
    cities = [row['text'] for row in towns]
    longest_city = max(cities, key=lambda label: len(label.encode('cp932')))
    longest_place = max(cities + villages, key=lambda label: len(label.encode('cp932')))
    longest_item = max((row['name'] for row in items), key=lambda label: len(label.encode('cp932')))
    named = sorted({name for name in names if name and name.isascii()}, key=lambda label: (len(label), label))
    number_cases = lambda *keys: [(values[k],) for k in keys]
    samples = {
        288: number_cases(1, 250, 2147483647),
        292: list(dict.fromkeys((name,) for name in ('Lisbon', 'Santo Domingo', longest_city))),
        297: list(dict.fromkeys((name,) for name in ('Inuvik', 'Istanbul', longest_place))),
        301: number_cases(20, 399, 2147483647),
        303: [(values[20], values[29]), (values[409], values[400]), (values[100], values[21])],
        305: number_cases(9, 400, 2147483647),
        311: number_cases(100, 190, 2147483647),
        340: [(name,) for name in dict.fromkeys(('Baby Shark', 'Sextant', longest_item))],
        341: [(name,) for name in dict.fromkeys((named[0], 'Janus Pasar', named[-1]))],
    }
    return samples, dict(towns=cities, villages=villages, item_names=[row['name'] for row in items],
                         original_composed_actor_names=names, native_number_cases=values)


def native_reader():
    code = checked_text(inspect.getsource(run_case), {
        '        u.reg_write(UC_ARM_REG_R1, test)':
            '        assert bytes(u.mem_read(ptr, len(template) + 1)) == template + b"\\0"',
        "    for register, value in zip([UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3],":
            "    first = get(LOOKUP, row['message_ID']) if wrapper == RAW_NOTICE else row['message_ID']\n"
            "    for register, value in zip([UC_ARM_REG_R0, UC_ARM_REG_R1, UC_ARM_REG_R2, UC_ARM_REG_R3],",
        "            [row['message_ID'], *padded[:3]], strict=True):": "            [first, *padded[:3]], strict=True):",
        'original_storage_unmodified=True': 'actual_stored_template_pointer_used=True',
        'scratch_template_test_before_widget_creation=True': 'stopped_before_widget_creation=True',
    })
    env = {**run_case.__globals__, 'LOOKUP': LOOKUP, 'RAW_NOTICE': RAW_NOTICE,
           'WRAPPERS': run_case.__globals__['WRAPPERS'] | {RAW_NOTICE: 'raw-template-notice'}}
    exec(compile(code, __file__ + '::original-stored-pointer-and-raw-template', 'exec'), env)
    return env['run_case']


def render_cases(ctx, clone, rows, storage, samples):
    raster, _, font_contract = mixed.font_tools(ctx.image)
    kanji = ctx.image.read_file('/GRP/KANJI.FNT')
    run = native_reader()
    results, planes = [], []
    for n, row in rows.items():
        target = row['native_callers'][0]['target']
        wrapper = RAW_NOTICE if n == 341 else target
        logical = row['english']
        markup = storage[n].decode('ascii').replace('\n', '{LB}')
        source = row | dict(english=markup, current_copies=[dict(wrapper=wrapper)])
        for args in samples.get(n, [()]):
            assert len(args) == row['native_substitution_count']
            result = run(clone, source | dict(current_hex=storage[n].hex()), args)
            clone.calls.clear()
            display = bytes.fromhex(result['native_wrapper_output_hex'])
            try:
                plane, glyphs = mixed.render(raster, clone.arm, kanji, display)
            except AssertionError as error:
                raise ValueError((n, args, result['native_wrapper_lines'])) from error
            lines = [line.strip() for line in display.decode('cp932').split('\n')]
            assert ' '.join(' '.join(lines).split()) == logical % args
            if n in RETAIN_STORED:
                before = run(ctx, source, args)
                ctx.calls.clear()
                assert before['native_wrapper_output_hex'] == result['native_wrapper_output_hex']
            results.append(result | dict(lines=lines, native_glyphs=len(glyphs),
                native_ink_sha256=sha256(bytes(pixel != 0 for pixel in plane)).hexdigest()))
            planes.append(plane)
    return results, planes, font_contract


def save_sheets(cases, planes):
    sheets = []
    for start in range(0, len(cases), 8):
        batch = cases[start:start + 8]
        sheet = Image.new('RGB', (936, 118 * ((len(batch) + 1) // 2)), '#263238')
        draw = ImageDraw.Draw(sheet)
        for i, (case, plane) in enumerate(zip(batch, planes[start:start + len(batch)], strict=True)):
            x, y = (i % 2) * 468, (i // 2) * 118
            draw.text((x + 4, y + 3), f"{case['message_ID']}  {' / '.join(case['arguments'])}", fill='white')
            page = Image.frombytes('L', (mixed.WIDTH, mixed.HEIGHT), bytes(0 if value else 255 for value in plane))
            sheet.paste(page.resize((456, 96), Image.Resampling.NEAREST), (x + 4, y + 18))
        path = ROOT / f'stored_panels_{start // 8 + 1:02d}.png'
        sheet.save(path)
        sheets.append(dict(path=str(path), sha256=digest(path), pages=len(batch)))
    return sheets


def stage():
    assert not ROOT.exists()
    release = load(RELEASE)
    ctx = equipment.RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    manuscript = load(MANUSCRIPT)
    assert manuscript['registered_predecessor_sha256'] == ctx.release['candidate_sha256']
    rows = active_rows(manuscript)
    storage = storage_text(rows)
    directory = sha256(ctx.arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    wrapped, ownership = transform(ctx.arm)
    repack = FunctionType(relocate.__code__, {**relocate.__globals__, 'DIRECTORY': directory})
    common, arm, rebound, packing = repack(ctx.common, wrapped, rows, storage)
    assert packing['all_41_blocks_fit_8KiB']
    assert arm[:DIRECTORY_OFFSET] == wrapped[:DIRECTORY_OFFSET] and arm[TABLE_END:] == wrapped[TABLE_END:]
    clone = with_components(ctx, arm, common)
    variants, catalogue = dynamic_samples(ctx)
    results, planes, font_contract = render_cases(ctx, clone, rows, storage, variants)
    image = NdsImage.open(ctx.rompath)
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    target = bytes(image.rom.save())
    image.replace_file(ARM, ctx.arm)
    image.replace_file(COMMON, ctx.common)
    assert bytes(image.rom.save()) == ctx.rompath.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(target)
    stored = NdsImage.open(ROM)
    assert stored.read_file(ARM) == arm and stored.read_file(COMMON) == common
    sheets = save_sheets(results, planes)
    save(PROOF, dict(registered_input=ctx.receipt(), research_ROM=str(ROM), research_ROM_sha256=digest(ROM),
        research_ARM9_sha256=sha256(arm).hexdigest(), research_COMMON_sha256=sha256(common).hexdigest(),
        records=[dict(message_ID=n, source=rows[n]['source_reference'], previous=rows[n]['current_reference'],
                      stored=reference(rebound[n]), stored_hex=storage[n].hex()) for n in sorted(rows)],
        parent_inverse_exact=True, rendered_variants=results, catalogue=catalogue,
        ownership=ownership, storage=packing, sheets=sheets, font_contract=font_contract,
        editorial_amendments=AMENDMENTS, gameplay_and_release_pending=True, new_credit=0, full_goal_complete=False,
        evidence={str(path): digest(path) for path in (MANUSCRIPT, RELEASE, Path(__file__))}))
    print(f'Staged {len(rows)} records with {len(results)} mixed-font and native ASCII variants.')


if __name__ == '__main__':
    stage()
