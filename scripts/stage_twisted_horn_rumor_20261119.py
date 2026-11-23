"""Keep the Guildmaster's complete remedy claim together in the portrait dialogue."""

from pathlib import Path
from types import FunctionType

from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END, TABLE_OFFSET
from scripts import review_lisbon_return_shared_20261119 as review
from scripts import stage_golden_route_exchanges_v1 as golden
from scripts.stage_shared_notices_storage_v1 import relocate

base, native, parent = review.base, review.native, review.latest
COMMON, ARM, ID = review.COMMON, native.ARM, 3665
ROOT = Path('work/twisted_horn_rumor_20261119/staged_v2')
ROM, PROOF = ROOT / 'Twisted_Horn_Rumor_STAGED.nds', ROOT / 'stored_proof.json'
ANCIENT = Path('releases/all_routes_editorial_20261111_ancient_map_text_candidate/verification/registered_review.json')


def main():
    assert not ROOT.exists()
    release, reviewed, earlier = map(base.load, (parent.RELEASE, review.OUTPUT, ANCIENT))
    assert release['candidate_sha256'] == reviewed['registered_candidate_sha256'] == base.digest(parent.ROM)
    assert release['registry_sha256'] == base.digest(base.REGISTRY)
    row, = (r for r in reviewed['records'] if r['message_ID'] == ID)
    original, = (r for r in earlier['records'] if r['message_ID'] == ID)
    assert row['source_hex'] == original['source_hex'] and original['decision'] == 'revision'
    ctx = native.RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    assert native.digest(ctx.common) == reviewed['common_sha256']
    directory = native.digest(ctx.arm[DIRECTORY_OFFSET:TABLE_OFFSET])
    repack = FunctionType(relocate.__code__, relocate.__globals__ | {'DIRECTORY': directory})
    raw = row['english'].encode('ascii')
    common, arm, records, allocation = repack(ctx.common, ctx.arm, {ID: row}, {ID: raw})
    assert allocation['changed_visible_templates'] == [ID] and allocation['touched_blocks'] == [40]
    assert allocation['all_41_blocks_fit_8KiB'] and allocation['all_unselected_native_copy_spans_exact']
    assert arm[:DIRECTORY_OFFSET] == ctx.arm[:DIRECTORY_OFFSET] and arm[TABLE_END:] == ctx.arm[TABLE_END:]
    portrait = golden.fleet.portrait
    result = portrait.with_components(ctx, arm, common)
    layout = golden.portrait_with_arguments()
    prior = layout(ctx, row, None, bytes.fromhex(row['current_hex']), None, ())
    revised = layout(result, row, None, raw, None, ())
    old_text, new_text = (entry.pop('display') for entry in (prior, revised))
    old_lines, new_lines = (screen.decode('ascii').split('\n') for screen in (old_text, new_text))
    assert old_lines[-1].strip() == 'illness.'
    assert len(new_lines) == 4 and new_lines[-1].strip() == 'medicine that cures any illness.'
    assert b' '.join(new_text.split()) == raw
    raster, _, font = portrait.font_tools(ctx.image)
    kanji = ctx.image.read_file('/GRP/KANJI.FNT')
    pages = []
    for value, label in ((old_text, '3665 previous'), (new_text, '3665 revised')):
        physical, events = portrait.render_portrait(raster, arm, kanji, value)
        assert [r['code'] for r in events] == golden.glyph_codes(value)
        pages.append((label, physical))
    image = base.NdsImage.open(parent.ROM)
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    compiled = bytes(image.rom.save())
    image.replace_file(ARM, ctx.arm)
    image.replace_file(COMMON, ctx.common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir(parents=True)
    ROM.write_bytes(compiled)
    shots = portrait.portrait_sheets(ROOT, pages)
    base.save(PROOF, dict(candidate_sha256=base.digest(ROM), predecessor_sha256=release['candidate_sha256'],
        clean_input_sha256=release['clean_input_sha256'], whole_parent_inverse=True, allocation=allocation,
        target_ARM9_sha256=native.digest(arm), target_COMMON_sha256=native.digest(common),
        record=row | dict(source_meaning=original['source_meaning'], context=original['context'],
            staged_reference=review.reference(records[ID]), staged_hex=raw.hex()),
        previous_lines=old_lines, revised_lines=new_lines, portrait_original_call=prior, revised_call=revised,
        offline_font=font, sheets=shots, actual_gameplay_on_stage=False,
        evidence={str(p):base.digest(p) for p in (review.OUTPUT, parent.RELEASE, ANCIENT, Path(__file__))}))
    print('Staged the revised Guild rumor with exact native portrait rendering and whole-ROM inverse.')


if __name__ == '__main__':
    main()
