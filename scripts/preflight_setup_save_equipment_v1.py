"""Check shared system and equipment prose with the current native formatter."""

import struct
from hashlib import sha256
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.layout import format_markup
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_literal_static_layout_v1 import HEIGHT, PROFILE, WIDTH, render
from scripts.preflight_literal_notice_formatting_v1 import run_case
from scripts.primary_town_native_font_v2102 import font_tools
from scripts.register_captain_biographies_v1 import RELEASE
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.review_literal_notice_callers_v1 import WRAPPERS, current_copy
from scripts.review_setup_save_equipment_v1 import OUTPUT as MANUSCRIPT


ROOT = Path('work/SharedText_20261110_v1/setup_save_equipment_preflight_v1')
ACTOR_MAX_SAMPLE = 5


def stock_names(ctx):
    cpu, get, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)

    def word(address):
        return struct.unpack('<I', cpu.mem_read(address, 4))[0]

    def label(address):
        return bytes(cpu.mem_read(address, 128)).split(b'\0', 1)[0].decode('cp932')

    item_root = get(0xCB190) + 4
    items = []
    for index in range(218):
        obj = item_root + index * 20
        getter = word(word(obj) + 8)
        name = label(get(getter - 0x02000000, obj))
        assert name
        items.append(dict(item_ID=index, name=name, getter=getter))
    actor_catalog = []
    for index in range(4, 114):
        obj = ctx.actor_root + 4 + index * 32
        getter = word(word(obj) + 8)
        name = label(get(getter - 0x02000000, obj))
        assert name
        actor_catalog.append(dict(actor_ID=index, name=name, getter=getter))
    ctx.calls.clear()
    return items, actor_catalog


def variants(items, actors):
    longest = sorted((row['name'] for row in items if row['name'].isascii()), key=lambda name: (len(name), name))[-3:]
    names = sorted((row['name'] for row in actors if row['name'].isascii()), key=lambda name: (len(name), name))[-ACTOR_MAX_SAMPLE:]
    special = items[121]['name']
    assert special == 'Demon Figurehead'
    return {
        321: [('Rafael Castor', 'Travels of Marco Polo'), (names[-1], longest[-1]), (names[-2], 'Sextant')],
        322: [(special,), ('Figurehead',), (longest[-1],)],
        327: [('Hangzhou', special), ('Santa Maria', longest[-1]), ('ABCDEFGHIJKLMNOPQR', longest[-2])],
        329: [('Rafael Castor', 'Travels of Marco Polo'), (names[-1], longest[-1]), (names[-2], 'Sextant')],
    }


def summarize(case, rows, contexts):
    return dict(message_ID=case['message_ID'], arguments=list(case['arguments']), native_lines=rows,
                exact_expansion_hex=case['expanded_hex'], native_display_hex=case['native_wrapper_output_hex'],
                width_units=case['native_width_units'], **contexts)


def check_modal(ctx, record, args, raster, font):
    number = record['message_ID']
    calls = record['native_callers']
    assert len({row['target'] for row in calls}) == 1
    row = record | dict(current_copies=[dict(wrapper=calls[0]['target'])])
    choices = [row['english']]
    if not args:
        markup = format_markup(row['english'], PROFILE).replace('{LB}', '{LB} ')
        if markup != choices[0]:
            choices.append(markup)
    rejected = []
    for markup in choices:
        case = run_case(ctx, row | dict(english=markup), args)
        ctx.calls.clear()
        text = bytes.fromhex(case['native_wrapper_output_hex'])
        try:
            plane, lines, origins, glyphs = render(raster, font, ctx.arm, text)
            assert ' '.join(' '.join(lines).split()) == row['english'] % args
        except AssertionError:
            rejected.append(summarize(case, case['native_wrapper_lines'], dict(tested_storage_markup=markup)))
            continue
        return summarize(case, lines, dict(storage_markup=markup, origins=origins, glyph_count=len(glyphs),
                         native_ink_sha256=sha256(plane).hexdigest(), complete_glyphs_bounds_and_words=True,
                         earlier_rejected_formats=rejected)), plane
    return dict(message_ID=number, arguments=list(args), native_layout_pending=True,
                rejected_native_display=rejected), None


def main():
    assert not ROOT.exists()
    release = load(RELEASE)
    ctx = RegisteredRuntime(RELEASE, release['own_registered_startup'], captain=3)
    doc = load(MANUSCRIPT)
    assert ctx.release['candidate_sha256'] == doc['registered_predecessor_sha256']
    items, actors = stock_names(ctx)
    args_by_id = variants(items, actors)
    raster, _, meta = font_tools(ctx.image)
    font = GameAsciiFont.from_arm9(ctx.arm)
    cases, sheets, pages = [], [], []
    direct = None
    for record in doc['records']:
        n = record['message_ID']
        if n == 318:
            continue
        if n == 320:
            direct = current_copy(ctx, record, record['native_callers'][0]['target'])
            ctx.calls.clear()
            continue
        assert record['native_callers'][0]['target'] in WRAPPERS
        for args in args_by_id.get(n, [()]):
            assert len(args) == record['native_substitution_count']
            case, pixels = check_modal(ctx, record, args, raster, font)
            cases.append(case)
            if pixels is not None:
                page = Image.frombytes('L', (WIDTH, HEIGHT), bytes(0 if p else 255 for p in pixels))
                pages.append((case, page))
    ROOT.mkdir()
    for start in range(0, len(pages), 8):
        batch = pages[start:start + 8]
        sheet = Image.new('RGB', (936, 118 * ((len(batch) + 1) // 2)), '#263238')
        draw = ImageDraw.Draw(sheet)
        for i, (case, page) in enumerate(batch):
            x, y = (i % 2) * 468, (i // 2) * 118
            title = f"{case['message_ID']}  {' / '.join(case['arguments'])}"
            draw.text((x + 4, y + 3), title, fill='white')
            sheet.paste(page.resize((456, 96), Image.Resampling.NEAREST), (x + 4, y + 18))
        path = ROOT / f'panels_{start // 8 + 1:02d}.png'
        sheet.save(path)
        sheets.append(dict(path=str(path), sha256=digest(path), pages=len(batch)))
    pending = sorted({case['message_ID'] for case in cases if case.get('native_layout_pending')})
    save(ROOT / 'preflight.json', dict(registered_input=ctx.receipt(), modal_cases=cases, native_case_count=len(cases),
        complete_native_planes=len(pages), modal_layout_holds=pending, direct_original_320_copy=direct,
        direct_320_chooser_and_318_caller_pending=True, sheets=sheets, font_contract=meta,
        current_item_name_catalogue=items, current_actor_name_catalogue=actors,
        full_name_and_item_variants_are_focused_checks=True, custom_ship_name_sample_is_offline_only=True,
        staged_storage_and_actual_gameplay_pending=True, new_credit=0, full_goal_complete=False,
        evidence={str(path): digest(path) for path in (MANUSCRIPT, RELEASE, Path(__file__))}))
    print(f'{len(pages)}/{len(cases)} proposed modal variants pass. Layout holds: {pending}.')


if __name__ == '__main__':
    main()
