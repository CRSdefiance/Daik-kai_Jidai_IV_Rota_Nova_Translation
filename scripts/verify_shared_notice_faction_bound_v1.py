"""Apply the source-owned company-name limit to the three affected notice layouts."""

from itertools import product
from pathlib import Path
from types import SimpleNamespace

from ndspy.code import MainCodeFile
from PIL import Image, ImageDraw

from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_literal_static_layout_v1 import HEIGHT, WIDTH
from scripts.preflight_literal_notice_formatting_v1 import run_case
from scripts.preflight_shared_dynamic_notice_wrap_v1 import ROOT as DYNAMIC, eligible_model, font_tools, manuscript, render
from scripts.probe_map_player_faction_name import CAPACITY, LOCKS, STORAGE, edit_dispatch
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.stage_shared_notices_storage_v1 import ARM, COMMON, ROOT
from scripts.stage_ship_command_release_v1 import RELEASE, STARTUP


PROOF = Path('work/analysis/map_creature_complete_v139/native_player_faction_name_proof.json')
OUT = ROOT / 'faction_name_bound_v1'
NAMES = ('ABCDEFGHIJKLMNOPQR', 'ABCDEFGHI JKLMNOPQ', '長崎海洋商会遠洋船', 'ABC長崎海洋商会DEF')


def main():
    assert not OUT.exists()
    source = NdsImage.open('work/clean.nds').read_file(ARM)
    staged_path = ROOT / 'stored_verification.json'
    staged = load(staged_path)
    target = NdsImage.open(staged['target'])
    arm = target.read_file(ARM)
    assert digest(staged['target']) == staged['target_sha256']
    prior = load(PROOF)
    assert (CAPACITY, STORAGE) == (18, 19)
    assert prior['editor_capacity_bytes'] == CAPACITY and prior['serialized_storage_bytes'] == STORAGE
    assert prior['shared_name_offset'] == 0x1A39 and len(prior['cases']) == 27
    spans = []
    for low, high in (*LOCKS, (0x3CF9C, 0x3CFF0), (0xB41C4, 0xB4248), (0xB4274, 0xB42A4)):
        assert source[low:high] == arm[low:high], hex(low)
        spans.append(dict(start=BASE + low, end=BASE + high, length=high - low))
    assert all(len(name.encode('cp932')) == CAPACITY for name in NAMES)
    editor = [edit_dispatch(arm, name.encode('cp932')) for name in NAMES]

    rows, _ = manuscript()
    native_path = DYNAMIC / 'native_preflight.json'
    catalog = load(native_path)['catalog']
    towns = sorted(row['name'] for row in catalog['towns'])
    goods = sorted(row['name'] for row in catalog['goods'])
    assert len(towns) == 90 and len(goods) == 124
    assert max(len(f'In {town}, '.encode('cp932')) for town in towns) + CAPACITY == 36
    totals = {}
    for number, cases in (
        (93, product(towns, NAMES)), (95, product(towns, NAMES, goods)), (96, ((name,) for name in NAMES)),
    ):
        count = 0
        for args in cases:
            lines = eligible_model(rows[number]['english'] % args, True)
            assert len(lines) <= 3 and all(len(line.encode('cp932')) <= (36 if i == 0 else 35)
                for i, line in enumerate(lines)), (number, args, lines)
            count += 1
        totals[number] = count

    ctx = RegisteredRuntime(RELEASE, STARTUP, captain=3)
    ctx.arm, ctx.common = arm, target.read_file(COMMON)
    ctx.raw = ctx.raw[:DIRECTORY_OFFSET] + arm[DIRECTORY_OFFSET:TABLE_END] + ctx.raw[TABLE_END:]
    sections = MainCodeFile(arm, BASE).sections
    ctx.sections = [*sections, SimpleNamespace(ramAddress=POOL, data=bytes(sections[3].data[:-48]))]
    raster, _, _ = font_tools(target)
    kanji = target.read_file('/GRP/KANJI.FNT')
    refs = {row['message_ID']: row for row in staged['exact_record_references']}
    OUT.mkdir()
    results = []
    for name in NAMES:
        for number, args in (
            (93, ('Santo Domingo', name)), (95, ('Santo Domingo', name, 'Black Glacier Sword')), (96, (name,)),
        ):
            row = {**rows[number], 'current_hex': refs[number]['target_hex']}
            case = run_case(ctx, row, args)
            ctx.calls.clear()
            data = bytes.fromhex(case['native_wrapper_output_hex'])
            assert not case['over_three_rows']
            assert [line.strip() for line in data.decode('cp932').splitlines()] == eligible_model(row['english'] % args, True)
            pixels, glyphs = render(raster, arm, kanji, data)
            path = OUT / f'case_{len(results) + 1:02d}_ID{number}.png'
            Image.frombytes('L', (WIDTH, HEIGHT), bytes(0 if p else 255 for p in pixels)).save(path)
            results.append(dict(**case, path=str(path), sha256=digest(path), ordered_glyphs=glyphs))
    sheet = Image.new('RGB', (936, 732), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, row in enumerate(results):
        x, y = i % 2 * 468, i // 2 * 122
        draw.text((x + 4, y + 3), f"{i + 1}. ID {row['message_ID']}", fill='white')
        with Image.open(row['path']) as page:
            sheet.paste(page.resize((456, 96), Image.Resampling.NEAREST), (x + 4, y + 19))
    contact = OUT / 'name_bound_cases.png'
    sheet.save(contact)
    save(OUT / 'verification.json', dict(candidate_sha256=staged['target_sha256'],
        original_company_name_byte_capacity=CAPACITY, serialized_field_bytes_with_NUL=STORAGE,
        exact_clean_spans=spans, fresh_native_dispatch_tests=editor,
        modeled_cases=totals, native_complete_pages=results, contact_sheet=str(contact),
        contact_sheet_sha256=digest(contact), valid_18_byte_examples_fit_three_rows=True,
        synthetic_23_byte_name_exceeds_source_editor_limit=True,
        partial_or_malformed_save_fields_not_a_legal_editor_case=True,
        all_cases_offline=True, keyboard_and_full_save_IO_are_explicit_boundaries=True,
        evidence={str(p): digest(p) for p in (PROOF, staged_path, native_path, Path(__file__))}))
    print(f'Original 18-byte editor limit and {len(results)} exact native glyph pages pass.')


if __name__ == '__main__':
    main()
