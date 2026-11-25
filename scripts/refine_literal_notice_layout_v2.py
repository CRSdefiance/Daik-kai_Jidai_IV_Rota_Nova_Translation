"""Refine exact shared notice breaks and rerender only the changed static pages."""

from itertools import product
from pathlib import Path

from PIL import Image, ImageDraw

from dk4tool.dialogue.font_audit import GameAsciiFont
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.plan_literal_static_layout_v1 import ROOT as PRIOR, render, WIDTH, HEIGHT
from scripts.preflight_literal_notice_formatting_v1 import ARCHIVE, OUTPUT, RELEASE, STARTUP, VARIANTS, run_case
from scripts.primary_town_native_font_v2102 import font_tools
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime


ROOT = PRIOR.with_name('static_notice_layout_v2')
AMENDMENT = ARCHIVE / 'literal_notice_amendments_v1.json'
REPLACEMENTS = {
    93: ('The city of %s is firing on a fleet from %s.',
         "Use a fleet from to preserve the affiliation without repeating fleet when it appears in the company's name."),
    130: ('To dock the fleet, choose a city where you have a contract.',
          'Put the docking action first and attach the contract to the city. The wording avoids a second sentence that repeats the selected city.'),
}
PREFERENCES = {
    92: (["The fleets under our command have", "sent income and expense reports.", "Would you like to hear them?"],
         'Keep income and expense reports intact and give the confirmation question its own row.'),
    122: (["Couldn't load the system data.", "The game will start with", "default system data."],
          'Keep default system data intact and separate the failure from what happens next.'),
    135: (["The people here are furious.", "There's no way in or out right now."],
          'Use the sentence boundary and keep the full access warning together.'),
}


def aligned_render(ctx, raster, font, row, lines):
    seams = [('', ' '), (' ', ' '), ('', '  '), (' ', '  ')]
    trials = sorted(product(seams, repeat=len(lines)-1), key=lambda v: sum(len(a)+len(b) for a,b in v))
    for guards in trials:
        markup = lines[0] + ''.join(a+'{LB}'+b+line for (a,b),line in zip(guards, lines[1:], strict=True))
        case = run_case(ctx, {**row, 'english': markup}, ())
        text = bytes.fromhex(case['native_wrapper_output_hex'])
        try:
            plane, rendered, origins, glyphs = render(raster, font, ctx.arm, text)
        except AssertionError:
            continue
        if rendered == lines and len(set(origins)) == 1:
            return markup, text, plane, rendered, origins, glyphs, guards
    raise AssertionError(f"No even native continuation alignment for {row['message_ID']}")


def main():
    assert not ROOT.exists() and not AMENDMENT.exists()
    old_path = PRIOR / 'layout.json'
    previous, doc = load(old_path), load(OUTPUT)
    ctx = RegisteredRuntime(RELEASE, STARTUP, captain=3)
    assert ctx.receipt() == doc['runtime'] == previous['runtime']
    raster, _, _ = font_tools(ctx.image)
    font = GameAsciiFont.from_arm9(ctx.arm)
    manuscript = {r['message_ID']: r for r in doc['records']}
    changes = []
    for n, (english, reason) in REPLACEMENTS.items():
        original = manuscript[n]
        manuscript[n] = {**original, 'english': english,
            'context': original['context']+' '+reason, 'localization_note': reason}
        cases = [run_case(ctx, manuscript[n], args) for args in VARIANTS.get(n, [()])]
        changes.append(dict(message_ID=n, before=original['english'], after=english, rationale=reason,
            source_reference=original['source_reference'], current_reference=original['current_reference'],
            source_hex=original['source_hex'], current_hex=original['current_hex'],
            verified_fresh_native_expansion_cases=cases, current_prose_review=manuscript[n]['review']))
    save(AMENDMENT, dict(original=str(OUTPUT), original_sha256=digest(OUTPUT), amended_records=changes,
        fresh_native_expansion_cases=sum(len(r['verified_fresh_native_expansion_cases']) for r in changes),
        all_untouched_prose_remains_exact=True, no_new_credit=True,
        target_allocation_and_registered_release_pending=True, full_goal_complete=False))

    ROOT.mkdir()
    result, changed = [], []
    for original in previous['records']:
        n = original['message_ID']
        if n not in PREFERENCES and n != 130:
            assert digest(original['preview']) == original['preview_sha256']
            result.append({**original, 'unchanged_native_page_reused': True})
            continue
        row = manuscript[n]
        if n == 130:
            case = run_case(ctx, row, ())
            text = bytes.fromhex(case['native_wrapper_output_hex'])
            plane, lines, origins, glyphs = render(raster, font, ctx.arm, text)
            assert len(lines) == 2 and len(set(origins)) == 1
            markup, guards = row['english'], ()
            reason = REPLACEMENTS[n][1]
        else:
            lines, reason = PREFERENCES[n]
            assert ' '.join(lines) == row['english']
            markup, text, plane, lines, origins, glyphs, guards = aligned_render(ctx, raster, font, row, lines)
        preview = ROOT/f'ID{n:04d}_native.png'
        Image.frombytes('L', (WIDTH, HEIGHT), bytes(0 if p else 255 for p in plane)).save(preview)
        record = dict(message_ID=n, logical_English=row['english'], provisional_storage_markup=markup,
            native_display_hex=text.hex(), display_lines=lines, line_origins=origins, layout_reason=reason,
            optional_zero_ink_guards=guards, native_ordered_visible_glyphs=glyphs,
            complete_words_glyphs_raster_and_guards_verified=True,
            preview=str(preview), preview_sha256=digest(preview), registered_storage_andactual_pending=True,
            unchanged_native_page_reused=False)
        changed.append(record)
        result.append(record)
    assert len(changed) == 4 and len(result) == 19
    sheet = Image.new('RGB', (936, 244), '#263238')
    draw = ImageDraw.Draw(sheet)
    for j, row in enumerate(changed):
        x,y=j%2*468,j//2*122
        draw.text((x+4, y+3), str(row['message_ID']), fill='white')
        with Image.open(row['preview']) as page:
            sheet.paste(page.resize((456,96), Image.Resampling.NEAREST), (x+4,y+19))
    path = ROOT/'four_changed_pages.png'
    sheet.save(path)
    save(ROOT/'layout.json', dict(records=result, runtime=ctx.receipt(), final_static_native_pages=19,
        fresh_changed_pages=4, exact_native_page_reuses=15, original_228x48_panel_and_36_or35_cell_bounds=True,
        direct_visual_review_pending=True, dynamic_substitution_layout_andallocation_pending=True,
        changed_sheet=str(path), changed_sheet_sha256=digest(path), source_layout=str(old_path),
        evidence={str(p):digest(p) for p in [OUTPUT, AMENDMENT, old_path, Path(__file__)]}, full_goal_complete=False))
    print('Aligned and rerendered four changed static pages. The other 15 exact native pages are reused.')


if __name__ == '__main__':
    main()
