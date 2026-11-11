"""Refine four Golden Route line breaks and reuse byte-matched native pages."""

from hashlib import sha256
from json import dumps, loads
from pathlib import Path
from types import FunctionType

from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END
from scripts import stage_golden_route_exchanges_v1 as previous


ARM, COMMON, BASE, OUTPUT = previous.ARM, previous.COMMON, previous.BASE, previous.OUTPUT
review, base, fleet = previous.review, previous.base, previous.fleet
modal_case = previous.modal_case
ROOT = previous.ROOT.with_name('golden_route_exchanges_staged_20261111_v2')
ROM, PROOF = ROOT / previous.ROM.name, ROOT / previous.PROOF.name
ADJUSTED = {
    3345: ('trade routes', 'I hear', 'a handsome sum'),
    3353: ('with a guild,', "let's tell them right away."),
    3377: ('right away',),
    3380: ('Is that true?',),
}
PHRASES = previous.PHRASES | ADJUSTED
stage = FunctionType(previous.stage.__code__, vars(previous) | {'PHRASES': PHRASES},
                     argdefs=previous.stage.__defaults__)


def main():
    assert not ROOT.exists()
    draft, release, prior = map(base.load, (OUTPUT, review.parent.RELEASE, previous.PROOF))
    runtime = base.RegisteredRuntime(review.parent.RELEASE, release['own_registered_startup'], captain=3)
    assert draft['registered_input'] == prior['registered_input'] == runtime.receipt()
    assert base.digest(OUTPUT) == prior['manuscript_sha256'] and base.digest(previous.ROM) == prior['research_ROM_sha256']
    assert all(base.digest(sheet['path']) == sheet['sha256'] for sheet in prior['sheets'])
    rows = {row['message_ID']: row for row in draft['records']}
    groups = {group['first_ID']: group for group in draft['native_context']}
    arm, common, storage, rebound, allocation, ownership = stage(runtime, release, rows, groups.values(), verified=prior)
    assert loads(dumps(ownership)) == prior['ownership']
    old = review.parent.base.NdsImage.open(previous.ROM)
    old_arm = old.read_file(ARM)
    assert arm[:DIRECTORY_OFFSET] == old_arm[:DIRECTORY_OFFSET] and arm[TABLE_END:] == old_arm[TABLE_END:]
    portrait = fleet.portrait
    ctx = portrait.with_components(runtime, arm, common)
    render, _, font = portrait.font_tools(runtime.image)
    assert font == prior['font']
    kanji = runtime.image.read_file('/GRP/KANJI.FNT')
    original_portrait = previous.portrait_with_arguments()
    pages, records = [], []
    for prior_row in prior['records']:
        number = prior_row['message_ID']
        row, template = rows[number], storage[number]
        assert row['source_reference'] == prior_row['source_reference']
        assert row['current_reference'] == prior_row['previous_reference']
        lookup = portrait.current_copy(ctx, row | {'current_hex': template.hex()}, BASE + 0x5528C)
        ctx.calls.clear()
        displays = prior_row['displays']
        if number in ADJUSTED:
            assert not row['original_substitution_count'] and template.hex() != prior_row['staged_hex']
            group = groups[row['native_group_first_ID']]
            caller, = group['native_callers']
            table = group | {'consumer': caller['consumer']} if group['table'] else None
            actor = next((i for i, _, msg in group['original_voice_choices'] if msg == number), None)
            native = original_portrait(ctx, row, table, template, actor, ())
            display = native.pop('display')
            assert display == template and b' '.join(display.split()) == row['english'].encode('ascii')
            lines = display.decode('cp932').split('\n')
            assert all(any(phrase in line for line in lines) for phrase in ADJUSTED[number])
            pixels, glyphs = portrait.render_portrait(render, arm, kanji, display)
            assert [glyph['code'] for glyph in glyphs] == previous.glyph_codes(display)
            pages.append((number, pixels))
            displays = [dict(native=native, argument_hex=[], normalized_visible_hex=b' '.join(display.split()).hex(),
                display_hex=display.hex(), visible_lines=[line.strip() for line in lines],
                complete_glyphs=len(glyphs), native_ink_sha256=sha256(pixels).hexdigest())]
        else:
            assert template.hex() == prior_row['staged_hex']
        records.append(prior_row | dict(staged_reference=base.reference(rebound[number]),
            staged_hex=template.hex(), original_stored_lookup=lookup, displays=displays))
    assert len(records) == 73 and len(pages) == len(ADJUSTED)
    image = review.parent.base.NdsImage.open(runtime.rompath)
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
    base.save(PROOF, prior | dict(research_ROM=str(ROM), research_ROM_sha256=base.digest(ROM),
        research_ARM9_sha256=sha256(arm).hexdigest(), research_COMMON_sha256=sha256(common).hexdigest(),
        allocation=allocation, records=records, sheets=prior['sheets'] + sheets,
        superseded_page_IDs=sorted(ADJUSTED), fresh_native_pages=len(pages), reused_native_pages=117 - len(pages),
        reused_renderer_and_selector_byte_exact=True, prior_proof_sha256=base.digest(previous.PROOF)))
    print('Verified four revised native pages, 113 dependency-matched pages and 73 fresh stored lookups.')


if __name__ == '__main__':
    main()
