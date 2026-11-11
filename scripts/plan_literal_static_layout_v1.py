"""Plan and render the complete static subset of the reviewed literal notices."""

from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.dialogue.layout import format_markup
from dk4tool.dialogue.profiles import DialogueProfile
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.preflight_literal_notice_formatting_v1 import OUTPUT, RELEASE, STARTUP, TARGET, run_case
from scripts.primary_town_native_font_v2102 import font_tools, glyph_codes
from scripts.probe_button_prompt_native import BASE
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime


ROOT = Path('work/SharedText_20261110_v1/static_notice_layout_v1')
PROFILE = DialogueProfile('common-literal-modal-228', window_width_px=216, max_lines=3,
    guard_linebreaks=False, balanced_wrapping=True)
WIDTH, HEIGHT = 228, 48
ENTRY = 0x01FFCE40-BASE


def render(raster, font, arm, text):
    events = []
    plane, consumed = raster(arm, text, ENTRY, size=(WIDTH, HEIGHT),
        complete=False, instruction_limit=2000000, glyph_events=events)
    assert consumed == len(text)
    visible = [e for e in events if e['code'] != 32]
    assert [e['code'] for e in visible] == glyph_codes(text)
    lines = [line.strip() for line in text.decode('ascii').split('\n')]
    assert 1 <= len(lines) <= 3 and all(lines)
    ink = bytearray(WIDTH*HEIGHT)
    origins = []
    cursor = 0
    for row, line in enumerate(lines):
        origin = visible[cursor]['x']
        assert origin in [0, 6]
        assert origin+len(line)*6 <= 216
        origins.append(origin)
        for offset, char in enumerate(line):
            if char == ' ':
                continue
            x = origin+offset*6
            assert visible[cursor]['x'] == x and visible[cursor]['y'] == row*16
            assert visible[cursor]['code'] == ord(char)
            cursor += 1
            glyph = font.decode(char)
            for yy in range(glyph.height):
                for xx in range(glyph.width):
                    if glyph.getpixel((xx, yy)):
                        ink[(row*16+yy+1)*WIDTH+x+xx] = 1
    assert cursor == len(visible) and plane == bytes(ink)
    return plane, lines, origins, visible


def main():
    assert not ROOT.exists()
    doc, preflight = load(OUTPUT), load(TARGET)
    ctx = RegisteredRuntime(RELEASE, STARTUP, captain=3)
    assert ctx.receipt() == doc['runtime'] == preflight['runtime']
    raster, _, meta = font_tools(ctx.image)
    font = GameAsciiFont.from_arm9(ctx.arm)
    boundaries = []
    for n in [35, 36, 37]:
        text = ('F'+'a'*(n-2)+'!').encode()
        for lead in [b'', b'I\n ', b'I\n  ']:
            events = []
            _, consumed = raster(ctx.arm, lead+text, ENTRY, size=(WIDTH, HEIGHT),
                complete=False, instruction_limit=2000000, glyph_events=events)
            assert consumed == len(lead+text)
            start = next(e for e in events if e['code'] == ord('F'))
            end = next(e for e in events if e['code'] == ord('!'))
            single_row = start['y'] == end['y']
            assert single_row == (n <= (35 if lead.endswith(b'  ') else 36))
            boundaries.append(dict(length=n, input_prefix=lead.decode(), first=start, last=end, single_row=single_row))

    ROOT.mkdir()
    results = []
    for row in doc['records']:
        if row['native_substitution_count']:
            continue
        number = row['message_ID']
        original = next(c for c in preflight['cases'] if c['message_ID'] == number)
        text = bytes.fromhex(original['native_wrapper_output_hex'])
        selected = 'existing native formatter output'
        try:
            plane, lines, origins, glyphs = render(raster, font, ctx.arm, text)
            authored = row['english']
        except AssertionError:
            markup = format_markup(row['english'], PROFILE)
            authored = markup.replace('{LB}', '{LB} ')
            selected = 'balanced static paragraph formatting with validated continuation guard'
            formatted = run_case(ctx, {**row, 'english': authored}, ())
            text = bytes.fromhex(formatted['native_wrapper_output_hex'])
            plane, lines, origins, glyphs = render(raster, font, ctx.arm, text)
        assert ' '.join(' '.join(lines).split()) == ' '.join(row['english'].split())
        preview = ROOT/f'ID{number:04d}_native.png'
        Image.frombytes('L', (WIDTH, HEIGHT), bytes(0 if p else 255 for p in plane)).save(preview)
        results.append(dict(message_ID=number, logical_English=row['english'], provisional_storage_markup=authored,
            native_display_hex=text.hex(), display_lines=lines, line_origins=origins, layout=selected,
            native_ordered_visible_glyphs=glyphs, complete_words_glyphs_raster_and_guards_verified=True,
            preview=str(preview), preview_sha256=digest(preview), registered_storage_andactual_pending=True))
    assert len(results) == 19
    sheets = []
    for offset in range(0, len(results), 10):
        batch = results[offset:offset+10]
        sheet = Image.new('RGB', (936, 122*((len(batch)+1)//2)), '#263238')
        draw = ImageDraw.Draw(sheet)
        for j, row in enumerate(batch):
            x,y=j%2*468,j//2*122
            draw.text((x+4, y+3), str(row['message_ID']), fill='white')
            with Image.open(row['preview']) as page:
                sheet.paste(page.resize((456,96), Image.Resampling.NEAREST), (x+4,y+19))
        path = ROOT / f'static_{offset//10+1:02d}.png'
        sheet.save(path)
        sheets.append(dict(path=str(path), sha256=digest(path), message_IDs=[r['message_ID'] for r in batch]))
    save(ROOT/'layout.json', dict(runtime=ctx.receipt(), records=results, original_literal_panel=[WIDTH,HEIGHT],
        native_first_continuation_and_width_boundary_cases=boundaries, font_model=meta,
        complete_native_andindependent_planes=19, font_bounds_andcomplete_words_pass=True, sheets=sheets,
        selected_input_only_not_registered_allocation_orphysical_gameplay=True,
        direct_visual_review_pending=True, variable_substitution_cases_pending=True, new_credit=0,
        evidence={str(p):digest(p) for p in [OUTPUT, TARGET, Path(__file__)]}, full_goal_complete=False))
    print('19 native static notice pages pass exact word, glyph and pixel checks. Two sheets await visual review.')


if __name__ == '__main__':
    main()
