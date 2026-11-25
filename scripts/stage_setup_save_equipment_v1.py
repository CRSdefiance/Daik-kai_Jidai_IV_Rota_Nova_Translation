"""Stage the source-bound equipment and system notices for emulator verification."""

import inspect
from hashlib import sha256
from pathlib import Path
from types import FunctionType

from PIL import Image, ImageDraw

from dk4tool.patch.equipment_removal_wrap_v1 import transform
from dk4tool.rom.nds import NdsImage
from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END, TABLE_OFFSET
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts import preflight_setup_save_equipment_v1 as preflight
from scripts.preflight_shared_crew_notices_v1 import with_components
from scripts.review_literal_notice_callers_v1 import current_copy
from scripts.seal_shared_text_source_v1 import ARM, COMMON, reference
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_shared_notices_storage_v1 import relocate


ROOT = Path('out/setup_save_equipment_staged_20261111_v1')
ROM = ROOT / 'setup_save_equipment_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_verification.json'
PREFLIGHT = preflight.ROOT / 'preflight.json'
RETAIN_STORED = {316, 321, 326, 327}


def check_stored():
    source = checked_text(inspect.getsource(preflight.run_case), {
        '        u.reg_write(UC_ARM_REG_R1, test)':
            '        assert bytes(u.mem_read(ptr, len(template) + 1)) == template + b"\\0"',
        'original_storage_unmodified=True': 'actual_stored_template_pointer_used=True',
        'scratch_template_test_before_widget_creation=True': 'stopped_before_widget_creation=True',
    })
    env = dict(preflight.run_case.__globals__)
    exec(compile(source, __file__ + '::actual-stored-template', 'exec'), env)
    return env['run_case']


def stage():
    assert not ROOT.exists()
    release = load(preflight.RELEASE)
    ctx = preflight.RegisteredRuntime(preflight.RELEASE, release['own_registered_startup'], captain=3)
    original_arm, original_common = ctx.arm, ctx.common
    manuscript, prepared = map(load, (preflight.MANUSCRIPT, PREFLIGHT))
    assert prepared['registered_input'] == ctx.receipt()
    assert prepared['modal_layout_holds'] == [329]
    rows = {row['message_ID']: row for row in manuscript['records'] if row['message_ID'] != 318}
    assert len(rows) == 14
    planned = {case['message_ID']: case['storage_markup'] for case in prepared['modal_cases']
               if case.get('complete_glyphs_bounds_and_words')}
    planned[329] = rows[329]['english']
    planned[320] = '  ' + rows[320]['english']
    assert set(planned) == set(rows)
    planned.update({n: rows[n]['current_English'] for n in RETAIN_STORED})
    storage = {n: markup.replace('{LB}', '\n').encode('ascii') for n, markup in planned.items()}
    directory = sha256(original_arm[DIRECTORY_OFFSET:TABLE_OFFSET]).hexdigest()
    wrapped, wrap = transform(original_arm)
    repack = FunctionType(relocate.__code__, {**relocate.__globals__, 'DIRECTORY': directory})
    common, arm, rebound, packing = repack(original_common, wrapped, rows, storage)
    assert packing['all_41_blocks_fit_8KiB']
    assert arm[:DIRECTORY_OFFSET] == wrapped[:DIRECTORY_OFFSET] and arm[TABLE_END:] == wrapped[TABLE_END:]
    clone = with_components(ctx, arm, common)
    raster, _, _ = preflight.font_tools(ctx.image)
    font = preflight.GameAsciiFont.from_arm9(arm)
    native = check_stored()
    confirmed, pages = [], []
    for case in prepared['modal_cases']:
        n, args = case['message_ID'], case['arguments']
        row = rows[n]
        wrapper = row['native_callers'][0]['target']
        markup = storage[n].decode('ascii').replace('\n', '{LB}')
        result = native(clone, row | dict(english=markup, current_hex=storage[n].hex(),
                        current_copies=[dict(wrapper=wrapper)]), tuple(args))
        clone.calls.clear()
        plane, lines, origins, glyphs = preflight.render(raster, font, arm, bytes.fromhex(result['native_wrapper_output_hex']))
        assert ' '.join(' '.join(lines).split()) == row['english'] % tuple(args)
        if n in RETAIN_STORED:
            before = native(ctx, row | dict(english=markup, current_copies=[dict(wrapper=wrapper)]), tuple(args))
            ctx.calls.clear()
            assert before['native_wrapper_output_hex'] == result['native_wrapper_output_hex']
        record = result | dict(lines=lines, origins=origins, native_glyphs=len(glyphs),
                               native_ink_sha256=sha256(plane).hexdigest())
        confirmed.append(record)
        pages.append((record, plane))
    direct = current_copy(clone, rows[320] | {'current_hex': storage[320].hex()}, 0x0205528C)
    clone.calls.clear()
    assert direct['copied_hex'] == storage[320].hex()

    image = NdsImage.open(ctx.rompath)
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    target = bytes(image.rom.save())
    image.replace_file(ARM, original_arm)
    image.replace_file(COMMON, original_common)
    assert bytes(image.rom.save()) == ctx.rompath.read_bytes()
    ROOT.mkdir()
    ROM.write_bytes(target)
    result = NdsImage.open(ROM)
    assert result.read_file(ARM) == arm and result.read_file(COMMON) == common
    sheets = []
    for start in range(0, len(pages), 8):
        batch = pages[start:start + 8]
        sheet = Image.new('RGB', (936, 118 * ((len(batch) + 1) // 2)), '#263238')
        draw = ImageDraw.Draw(sheet)
        for i, (case, plane) in enumerate(batch):
            x, y = (i % 2) * 468, (i // 2) * 118
            draw.text((x + 4, y + 3), f"{case['message_ID']}  {' / '.join(case['arguments'])}", fill='white')
            page = Image.frombytes('L', (preflight.WIDTH, preflight.HEIGHT), bytes(0 if p else 255 for p in plane))
            sheet.paste(page.resize((456, 96), Image.Resampling.NEAREST), (x + 4, y + 18))
        path = ROOT / f'stored_panels_{start // 8 + 1:02d}.png'
        sheet.save(path)
        sheets.append(dict(path=str(path), sha256=digest(path), pages=len(batch)))
    save(PROOF, dict(registered_input=ctx.receipt(), research_ROM=str(ROM), research_ROM_sha256=digest(ROM),
        research_ARM9_sha256=sha256(arm).hexdigest(), research_COMMON_sha256=sha256(common).hexdigest(),
        parent_inverse_exact=True, records=[dict(message_ID=n, source=rows[n]['source_reference'],
            previous=rows[n]['current_reference'], stored=reference(rebound[n]), stored_hex=storage[n].hex())
            for n in sorted(rows)], rendered_variants=confirmed, direct_320_stored_copy=direct,
        ownership=wrap, storage=packing, sheets=sheets, gameplay_and_release_pending=True,
        evidence={str(path): digest(path) for path in (preflight.MANUSCRIPT, PREFLIGHT, Path(__file__))},
        new_credit=0, full_goal_complete=False))
    print(f'Staged {len(rows)} records, {len(pages)} complete modal variants and direct chooser copy. Research only.')


if __name__ == '__main__':
    stage()
