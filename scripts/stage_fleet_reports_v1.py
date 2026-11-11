"""Exercise fleet reports through the original portraits and number substitutions."""

from hashlib import sha256
from inspect import getsource
from pathlib import Path
from types import FunctionType

from dk4tool.rom.nds import NdsImage
from scripts import review_fleet_reports_v1 as review
from scripts import stage_crew_item_actions_v1 as prior
from scripts import stage_ship_emergency_review_v1 as portrait
from scripts.preflight_shared_dynamic_notice_wrap_v1 import glyph_codes
from scripts.source_locked_derivation_v5118 import checked_text


ARM, COMMON, BASE = review.ARM, review.COMMON, review.BASE
ROOT = Path('out/fleet_reports_staged_20261111_v1')
ROM = ROOT / 'fleet_reports_RESEARCH_ONLY.nds'
PROOF = ROOT / 'stored_verification.json'
OUTPUT = review.OUTPUT
PHRASES = {
    2575: ('with the money on hand.', 'The balance will go', "into next month's expenses."),
    2576: ('enough cash to cover the loss.', "We'll carry the rest over", "to next month's expenses."),
    2577: ("We're short on gold.", 'as an expense for next month.'),
    2578: ("We haven't enough gold", 'to cover the loss.', 'Best carry the balance over', "to next month's expenses."),
    2579: ("We can't cover the loss.", "We'll add the rest", "to next month's expenses."),
}


def stage(runtime, release, rows, groups):
    source = checked_text(getsource(prior.stage), {
        "group['runtime_item_name_inputs']": "group['argument_kind']",
        "allocation['touched_blocks'] == [26, 27]": "allocation['touched_blocks'] == [27]",
    })
    env = vars(prior) | {'review': review, 'PHRASES': PHRASES}
    exec(compile(source, __file__ + '::fleet-report-storage', 'exec'), env)
    return env['stage'](runtime, release, rows, groups)


def samples(kind, groups, number):
    if kind is None:
        return [None]
    if kind == 'gold':
        return [groups[kind][i] for i in (1 if number < 2571 else 0, -1)]
    choices = groups[kind]
    primary = next(row for row in choices if row['fleet_index'] == (1 if kind == 'company' else 0))
    longest = max(choices, key=lambda row: sum(len(value) for value in row['arguments']))
    if primary['arguments'] == longest['arguments']:
        longest = next(row for row in choices if row['fleet_index'] == 4)
    return [primary, longest]


def main():
    base = review.prior
    assert not ROOT.exists()
    draft, release = map(base.load, (OUTPUT, review.parent.RELEASE))
    runtime = base.RegisteredRuntime(review.parent.RELEASE, release['own_registered_startup'], captain=3)
    assert runtime.receipt() == draft['registered_input']
    rows = {row['message_ID']: row for row in draft['records']}
    groups = {group['first_ID']: group for group in draft['native_context']}
    arm, common, storage, rebound, allocation, ownership = stage(runtime, release, rows, groups.values())
    ctx = portrait.with_components(runtime, arm, common)
    render, _, font = portrait.font_tools(runtime.image)
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    native = portrait.with_arguments()
    pages, records = [], []
    for number, row in rows.items():
        template = storage[number]
        lookup = portrait.current_copy(ctx, row | {'current_hex': template.hex()}, BASE + 0x5528C)
        ctx.calls.clear()
        group = groups[row['native_group_first_ID']]
        caller = group['native_callers'][0]
        native_group = group | {'consumer': caller['consumer']}
        actor = next(i for i, _, msg in group['original_voice_choices'] if msg == number)
        displays = []
        for index, sample in enumerate(samples(group['argument_kind'], draft['initialized_argument_samples'], number)):
            arguments = tuple(bytes.fromhex(value) for value in sample['arguments']) if sample else ()
            case = native(ctx, row, native_group, template, actor, arguments)
            display = case.pop('display')
            expected = row['english'].encode('ascii') % arguments if arguments else row['english'].encode('ascii')
            assert b' '.join(display.split()) == expected, (number, display, expected)
            if b'\n' in template:
                assert display == template, (number, display)
            lines = display.decode('cp932').split('\n')
            assert all(any(phrase in line for line in lines) for phrase in PHRASES.get(number, ())), (number, lines)
            try:
                pixels, glyphs = portrait.render_portrait(render, arm, kanji, display)
            except AssertionError as error:
                raise AssertionError((number, lines, sample)) from error
            assert [row['code'] for row in glyphs] == glyph_codes(expected)
            pages.append((f'{number}/{index + 1}' if sample else number, pixels))
            displays.append(dict(native=case, argument_sample=sample, expanded_hex=expected.hex(),
                display_hex=display.hex(), visible_lines=[line.strip() for line in lines], complete_glyphs=len(glyphs),
                native_ink_sha256=sha256(pixels).hexdigest()))
        records.append(dict(message_ID=number, source_reference=row['source_reference'],
            previous_reference=row['current_reference'], staged_reference=base.reference(rebound[number]),
            staged_hex=template.hex(), original_stored_lookup=lookup, displays=displays))
    assert len(records) == 47 and len(pages) == 89
    image = NdsImage.open(runtime.rompath)
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    target = bytes(image.rom.save())
    image.replace_file(ARM, runtime.arm)
    image.replace_file(COMMON, runtime.common)
    assert bytes(image.rom.save()) == Path(runtime.rompath).read_bytes()
    ROOT.mkdir()
    with ROM.open('xb') as stream:
        stream.write(target)
    sheets = portrait.portrait_sheets(ROOT, pages)
    base.save(PROOF, dict(registered_input=runtime.receipt(), research_ROM=str(ROM), research_ROM_sha256=base.digest(ROM),
        research_ARM9_sha256=sha256(arm).hexdigest(), research_COMMON_sha256=sha256(common).hexdigest(),
        allocation=allocation, ownership=ownership, parent_inverse_exact=True, records=records, font=font,
        sheets=sheets, native_pages=len(pages), native_cases=len(pages), manuscript_sha256=base.digest(OUTPUT),
        formatting_pending_visual_review=True, gameplay_pending=True, new_credit=0, full_goal_complete=False))
    print(f'{len(records)} stored lookups and {len(pages)} original portrait cases passed.')


if __name__ == '__main__':
    main()
