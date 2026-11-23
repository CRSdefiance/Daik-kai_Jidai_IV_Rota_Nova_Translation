"""Review the ten Ancient Map rumors and stage three source-bound wrap improvements."""

from pathlib import Path
from types import FunctionType

from dk4tool.script.common_message_table import DIRECTORY_OFFSET, TABLE_END, TABLE_OFFSET
from scripts import register_twisted_horn_rumor_20261119 as parent
from scripts import stage_golden_route_exchanges_v1 as golden
from scripts import stage_twisted_horn_rumor_20261119 as prior

base, native = parent.base, parent.native
COMMON, ARM = prior.COMMON, prior.ARM
ROOT = Path('work/artifact_rumor_wraps_20261119/staged_v1')
ROM, PROOF = ROOT / 'Artifact_Rumor_Wraps_STAGED.nds', ROOT / 'stored_proof.json'
ORIGINAL_LAYOUT = prior.ANCIENT.with_name('stored_verification.json')
DECISIONS = {
    3658: (None, 'The flame comparison stays vivid and the Guildmaster marks the jewel as hearsay.'),
    3659: (None, 'The ancient blade and engraving lead naturally to the speaker’s doubts about reading it.'),
    3660: (None, 'The former priests and unsettling serpent carving are clearly conveyed. The carving phrase remains together.'),
    3661: ("It's a crimson crystal. Hold it up to the light. The story goes you'll see a star pattern inside.",
           'Keep the color, action and reported effect. The star pattern becomes a complete closing phrase.'),
    3662: (None, 'The reported diamond comes before the playful jewel-eating nickname, with the entire nickname on its line.'),
    3663: (None, 'The extravagant claim about cutting without contact and the Guildmaster’s doubt remain distinct.'),
    3664: ("It's a statue of a Siren, I hear. They say it served as a figurehead. A shipwrecking witch on the bow? Hard to believe.",
           'The Guildmaster reports the former use and then expresses disbelief. Keep the startling image of a witch on the bow together.'),
    3665: (None, 'The registered Lisbon revision keeps the three reported claims separate and the remedy on one line.'),
    3666: ("They say it's a great king's shield with a goddess pictured on it. Sailors say there's no finer charm.",
           'Retain the reported ownership, image and the sailors’ praise. Keep the charm claim in one phrase.'),
    3667: (None, 'The spear’s extraordinary size and rumored power to drive away evil are complete and readable.'),
}


def main():
    assert not ROOT.exists()
    release, earlier, layouts, horn = map(base.load, (parent.RELEASE, prior.ANCIENT, ORIGINAL_LAYOUT, prior.PROOF))
    assert base.digest(parent.ROM) == release['candidate_sha256'] == horn['candidate_sha256']
    assert base.digest(base.REGISTRY) == release['registry_sha256']
    ctx = native.RegisteredRuntime(parent.RELEASE, release['own_registered_startup'], captain=3)
    source_rom = base.NdsImage.open(native.CLEAN)
    directory = native.digest(ctx.arm[DIRECTORY_OFFSET:TABLE_OFFSET])
    source = prior.review.common_message_entries(source_rom.read_file(COMMON), source_rom.read_file(ARM))
    entries = prior.review.owned_entries(ctx.common, ctx.arm, directory)
    reports = {row['message_ID']: row for row in layouts['records']}
    earlier_rows = {row['message_ID']: row for row in earlier['records']}
    source_rows, replacements = {}, {}
    for number, (proposal, note) in DECISIONS.items():
        old = earlier_rows[number]
        source_ref = prior.review.reference(source[number])
        assert source[number].text.hex() == old['source_hex'] and source_ref == old['source_reference']
        current = entries[number].text
        saved = horn['record']['staged_hex'] if number == 3665 else reports[number]['staged_hex']
        assert current.hex() == saved
        if proposal:
            assert proposal.isascii() and '%' not in proposal
            replacements[number] = proposal.encode('ascii')
        source_rows[number] = dict(id=old['id'], message_ID=number, file_path=COMMON,
            source_Japanese=old['source_Japanese'], source_meaning=old['source_meaning'], context=old['context'],
            speaker='Guildmaster', source_hex=old['source_hex'], source_reference=source_ref,
            current_reference=prior.review.reference(entries[number]), current_hex=current.hex(),
            current_English=current.decode('ascii'), english=proposal or current.decode('ascii'), localization_note=note,
            decision='revision' if proposal else 'retention', review=old['review'] | {'formatting': not proposal})
    repack = FunctionType(prior.relocate.__code__, prior.relocate.__globals__ | {'DIRECTORY': directory})
    common, arm, rebound, allocation = repack(ctx.common, ctx.arm, source_rows, replacements)
    assert allocation['changed_visible_templates'] == [3661, 3664, 3666] and allocation['touched_blocks'] == [40]
    assert allocation['all_41_blocks_fit_8KiB'] and allocation['all_unselected_native_copy_spans_exact']
    assert arm[:DIRECTORY_OFFSET] == ctx.arm[:DIRECTORY_OFFSET] and arm[TABLE_END:] == ctx.arm[TABLE_END:]
    portrait = golden.fleet.portrait
    runtime = portrait.with_components(ctx, arm, common)
    render = golden.portrait_with_arguments()
    raster, _, font = portrait.font_tools(ctx.image)
    glyph_data = ctx.image.read_file('/GRP/KANJI.FNT')
    pages = []
    for n, row in source_rows.items():
        row['staged_reference'] = prior.review.reference(rebound[n])
        row['staged_hex'] = rebound[n].text.hex()
        former = horn['revised_lines'] if n == 3665 else reports[n]['visible_lines']
        row['previous_lines'] = former
        if n not in replacements:
            assert rebound[n].text == entries[n].text
            row['visible_lines'] = former
            row['prior_display_evidence'] = str(prior.PROOF if n == 3665 else ORIGINAL_LAYOUT)
            continue
        result = render(runtime, row, None, replacements[n], None, ())
        rendered = result.pop('display')
        lines = rendered.decode('ascii').split('\n')
        assert len(lines) <= 4 and b' '.join(rendered.split()) == replacements[n]
        physical, positions = portrait.render_portrait(raster, arm, glyph_data, rendered)
        assert [r['code'] for r in positions] == golden.glyph_codes(rendered)
        pages.append((n, physical))
        row.update(visible_lines=lines, original_consumer=result, complete_native_page=True)
    assert 'a star pattern inside.' in source_rows[3661]['visible_lines'][-1]
    assert any('A shipwrecking witch on the bow?' in line for line in source_rows[3664]['visible_lines'])
    assert source_rows[3664]['visible_lines'][-1].strip() == 'Hard to believe.'
    assert source_rows[3666]['visible_lines'][-1].strip() == "Sailors say there's no finer charm."

    image = base.NdsImage.open(parent.ROM)
    image.replace_file(ARM, arm)
    image.replace_file(COMMON, common)
    target = bytes(image.rom.save())
    image.replace_file(ARM, ctx.arm)
    image.replace_file(COMMON, ctx.common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    ROOT.mkdir(parents=True)
    ROM.write_bytes(target)
    sheets = portrait.portrait_sheets(ROOT, pages)
    base.save(PROOF, dict(candidate_sha256=base.digest(ROM), predecessor_sha256=release['candidate_sha256'],
        target_ARM9_sha256=native.digest(arm), target_COMMON_sha256=native.digest(common),
        clean_input_sha256=release['clean_input_sha256'], whole_parent_inverse=True,
        allocation=allocation, records=list(source_rows.values()), sheets=sheets, font_contract=font,
        actual_gameplay=False, new_coverage_credit=0, evidence={str(p): base.digest(p) for p in (
            parent.RELEASE, prior.ANCIENT, ORIGINAL_LAYOUT, prior.PROOF, Path(__file__))}))
    print('Staged three rumor revisions and seven exact retentions with native portrait checks.')


if __name__ == '__main__':
    main()
