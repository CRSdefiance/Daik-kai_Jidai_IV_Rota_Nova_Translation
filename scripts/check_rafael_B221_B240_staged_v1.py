"""Verify the original progressive signatures and FE swan staging in the registered renderer."""
from collections import defaultdict
from itertools import product
from pathlib import Path

from PIL import Image, ImageDraw

from scripts import check_rafael_B166_B167_ordinary_v1 as native
from scripts.audit_story_glyph_consistency import load, save
from scripts.check_rafael_B166_staged_FE_v7 import wrap_options
from scripts.plan_rafael_B221_B240_v1 import ROOT, STAGED, digest
from scripts.probe_rafael_B166_FE_source_staging_v1 import build_painter
from scripts.source_locked_derivation_v5118 import checked_text

OUT = ROOT / 'staged_native_v1'
FE_ID = 'DK4_MES_B223_R0017'
SWAN = ('Aah! Coo...', 'Coo... Aah...', '...Aah!')
STAGE = {
    'DK4_MES_B221_R0033': 'Yukihisa’s full signature closes the letter on its own indented row.',
    FE_ID: 'The three separate rows preserve the sequence of calls and the pause before the last call.',
    'DK4_MES_B226_R0068': 'Janus’s full signature is separate from his promise to write again.',
    'DK4_MES_B235_R0048': 'Ian’s full signature is separate from his closing invitation to look into the story.',
}


def visible(events):
    grouped = defaultdict(list)
    for event in events:
        code = event['code']
        text = chr(code) if event['kind'] == 'ascii' else code.to_bytes(2, 'big').decode('cp932')
        grouped[event['y']].append((event['x'], text))
    return [(y, next(x for x, text in row if not text.isspace()), ''.join(text for _, text in row).strip())
            for y, row in sorted(grouped.items()) if any(not text.isspace() for _, text in row)]


def progressive_shapes(row, source_rows):
    source_y, source_x, name = source_rows[-1]
    assert name == row['source_signature_row'].strip() and source_y in (32, 48) and source_x > 0
    signature = row['localized_signature']
    assert source_x + len(signature) * 6 <= 216
    for lines in wrap_options(row['localized_letter_close'], source_y // 16):
        blanks = source_y // 16 - len(lines)
        if len(lines) < 2:
            continue
        yield tuple((0, line) for line in lines) + ((0, ''),) * blanks + ((source_x, signature),)


def candidates(shape):
    for tails in product((0, 1), repeat=len(shape) - 1):
        for lead_extra in (0, 1, 2):
            parts = []
            for index, (x, text) in enumerate(shape):
                lead = x // 6 + lead_extra if x else 0
                tail = tails[index] if text and index < len(tails) else 0
                parts.append(b' ' * lead + text.encode('ascii') + b' ' * tail)
            yield b'\n'.join(parts)


def main():
    assert not OUT.exists()
    stage = load(STAGED)
    runtime = stage['runtime']
    n = native.env
    ctx = n['RegisteredRuntime'](runtime['release_proof'], runtime['startup_proof'], captain=0)
    assert ctx.receipt() == runtime
    painter, calibration = build_painter(runtime)
    font = ctx.image.read_file('/GRP/KANJI.FNT')
    adapter = checked_text(load(n['SOURCE'])['source_owned_target_page_adapter'], {
        '12ebaf3f3ce558e731c4c972ae90696392a351426cf147fbf3bd830dd1d82d1b': n['sha'](ctx.arm)
    })
    env = {**n['inherited_pages'].__globals__, 'expected_pixels': n['independent_pixels'], 'codes': n['codes']}
    exec(compile(adapter, __file__ + '::registered-progressive-painter', 'exec'), env)
    macro = load(n['MACROS'])
    prog_env = {**n['progressive_expand'].__globals__, 'DYNAMIC_BINDINGS': {}}
    prog_adapter = checked_text(macro['source_owned_progressive_adapter'], {
        'assert identity==prefix and captain==0': 'assert identity==prefix and captain==0'
    })
    exec(compile(prog_adapter, __file__ + '::progressive-macro-ABI', 'exec'), prog_env)
    fe_env = dict(n['FE_expand'].__globals__)
    fe_adapter = checked_text(macro['source_owned_FE_adapter'], {
        "b'Hodram'": "b'Rafael'", "b'Bergstrom'": "b'Castor'", "b'Bergstrom Fleet'": "b'Castor Co.'"
    })
    exec(compile(fe_adapter, __file__ + '::FE-macro-ABI', 'exec'), fe_env)

    OUT.mkdir()
    pictures, records, plans = [], [], []
    for row in stage['records']:
        ident, prefix = row['id'], row['source_selector']
        source = bytes.fromhex(row['source_hex'])
        assert source[0] == prefix and row['source_complete_preamble_hex'] == f'0040ffff00{prefix:02x}'
        assert not row['native_literal_tokens']
        is_fe = ident == FE_ID
        if is_fe:
            assert prefix == 254
            paint = painter
            pitch, width = 12, 228
        else:
            def paint(raw):
                pages = env['pages'](ctx.arm, font, raw)
                page, = pages['pages']
                return page
            pitch, width = 16, 216
        source_display = paint(source[1:])
        source_rows = visible(source_display['events'])
        if is_fe:
            assert [(y, x) for y, x, _ in source_rows] == [(0, 0), (12, 0), (24, 0)]
            shapes = (tuple((0, text) for text in SWAN),)
        else:
            shapes = progressive_shapes(row, source_rows)
        chosen = None
        for shape in shapes:
            assert ' '.join(text for _, text in shape if text) == row['english']
            expected = [(i * pitch, x, text) for i, (x, text) in enumerate(shape) if text]
            if any(x + 6 * len(text) > width for _, x, text in expected):
                continue
            for trial in candidates(shape):
                try:
                    display = paint(trial)
                except (AssertionError, ValueError):
                    continue
                if visible(display['events']) == expected:
                    chosen = trial, display, expected, shape
                    break
            if chosen:
                break
        assert chosen, (ident, source_rows)
        body, display, expected, shape = chosen
        assert b'\0' not in body and not body.startswith((b' ', b'\n')) and not body.endswith((b' ', b'\n'))
        alignment = ctx.execute(fe_env['expand'] if is_fe else prog_env['expand'], body, *(() if is_fe else (prefix,)))
        assert len(alignment['cases']) == 4 and all(case['output_hex'] == body.hex() for case in alignment['cases'])
        if is_fe:
            plane = display.pop('physical')
            logical = display.pop('logical')
            assert display['complete_consumed_bytes'] == len(body)
            (OUT / (ident + '_logical.bin')).write_bytes(logical)
            display['planned_native_row_comparison'] = dict(complete_glyph_row_membership_exact=True,
                complete_visible_row_origins_exact=True, planned_visible_rows=expected)
        else:
            plane = bytes.fromhex(display.pop('native_plane_hex'))
            assert (display['start'], display['end'], display['first_visible_origin']) == (0, len(body), [0, 0])
            display['native_guard_at_zero_not_missing_first_glyph'] = False
        path = OUT / (ident + '.bin')
        path.write_bytes(plane)
        picture = Image.new('RGB', (width, 64))
        colors = {0: (239, 232, 201), 1: (0, 8, 0), 15: (98, 97, 98)}
        picture.putdata([colors[int(bool(v))] if is_fe else colors[v] for v in plane])
        png = path.with_suffix('.png')
        picture.save(png)
        display.update(native_plane=str(path), native_plane_sha256=digest(path), preview=str(png),
                       preview_sha256=digest(png))
        pictures.append((ident, picture))
        record = dict(id=ident, block=row['block'], kind=row['kind'], source_reference=row['source_reference'],
            current_reference=row['current_reference'], compiled_hex=(bytes([prefix]) + body).hex(),
            expanded_native_hex=body.hex(), logical_English=row['english'], native_alignment=alignment,
            complete_native_English_display=display if is_fe else dict(pages=[display],
                complete_consumed_bytes=len(body), all_visible_first_internal_final_characters_in_order=True),
            source_staging_reason=STAGE[ident], source_staged_FE=is_fe, source_staged_progressive=not is_fe,
            exact_source_rows=source_rows, exact_native_English_rows=expected)
        records.append(record)
        plans.append(dict(id=ident, block=row['block'], kind=row['kind'], source_hex=row['source_hex'],
            source_record_index=row['source_record_index'], source_selector=prefix, logical_English=row['english'],
            encoded_hex=record['compiled_hex'], expected_native_pages=1, lines=[text for _, text in shape],
            source_staging_reason=STAGE[ident], approved_native_structural_layout=expected,
            base_QA=dict(issues=[], native_staged_consumer_exact=True), original_usable_width_px=width))
    assert len(records) == 4
    sheet = Image.new('RGB', (912, 320), '#263238')
    draw = ImageDraw.Draw(sheet)
    for i, (ident, picture) in enumerate(pictures):
        x, y = i % 2 * 456, i // 2 * 160
        draw.text((x+3, y+3), ident + ' source-staged', fill='white')
        sheet.paste(picture.resize((picture.width*2, 128), Image.Resampling.NEAREST), (x, y+24))
    png = OUT / 'all_four_staged_pages.png'
    sheet.save(png)
    save(OUT / 'compiled_staged.json', dict(runtime=runtime, font_sha256=n['sha'](font), records=records, plans=plans,
        review_sheets=[dict(path=str(png), sha256=digest(png), pages=4)], source_staged_placements_exact=True,
        FE_calibration=calibration, complete_native_glyphs_pages_bounds_and_canaries_pass=True,
        direct_visual_review_pending=True, actual_gameplay=False, new_credit=0,
        evidence={str(path): digest(path) for path in (STAGED, n['SOURCE'], n['MACROS'], Path(__file__))}))
    print([(row['id'], row['exact_native_English_rows']) for row in records], flush=True)


if __name__ == '__main__':
    main()

