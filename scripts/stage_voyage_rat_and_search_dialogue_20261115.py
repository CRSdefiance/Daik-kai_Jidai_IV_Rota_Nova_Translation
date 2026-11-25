"""Review all original rat warnings and empty-search replies in context."""

from pathlib import Path
from struct import unpack_from
from types import FunctionType

from scripts import observe_lisbon_voyage_and_osaka_20261115 as observed
from scripts import register_embedded_story_roles_20261115 as parent
from scripts.stage_market_conversation_20261115 import (
    ARM, CLEAN, COMMON, DIRECTORY_OFFSET, TABLE_OFFSET, GATES, RegisteredRuntime,
    common_message_entries, digest, files, font_tools, owned_deployment, owned_entries,
    portrait_sheets, reference, render_portrait, with_components,
)
from scripts.stage_mutiny_review_v1 import compile_layouts, portrait_case


base = parent.base
ROOT = Path('work/voyage_rat_and_search_dialogue_20261115_v1')
ROM, STORED = ROOT / 'Rat_and_Search_Dialogue_RESEARCH_ONLY.nds', ROOT / 'staged.json'
DIR = Path('translations/editorial_checkpoints/SharedText_20261110_v1')
MANUSCRIPT = DIR / 'voyage_rat_and_search_dialogue_20261115_v1.json'
SEA = DIR / 'sea_event_contextual_review.json'
RATS, SEARCH = range(401, 409), range(2217, 2222)
ACTORS = (4, 1, 0, 2, 5, 6, 14, 19, 4, 0, 6, 14, 19)
REVISIONS = {
    406: ("Admiral! Rats all over the ship!", "Our food's in trouble!"),
    408: ("Admiral, the ship is full of rats!", "Our food is in danger!"),
    2217: ('The search party has returned!', "Looks like there's nothing here!"),
    2218: ('The search party has come back.', 'Seems they found nothing good.'),
    2219: ('The expedition has returned.', 'Nothing here, by the looks of it.'),
    2221: ('The expedition has returned.', "Apparently, there's nothing nearby."),
}
NOTES = {
    401: ('The rats have proliferated and will ruin the food if nothing changes.',
          'Keep the scale of the infestation, the future condition and both complete phrases about the food.'),
    402: ('Rats have appeared. The speaker worries about the food.',
          'Keep the direct report and the speaker’s personal worry. Both clauses and the object of the worry remain intelligible across two rows.'),
    403: ('The ship is crawling with rats. The speaker fears they may get into the food.',
          'Keep the familiar clipped alert and the tentative warning. The two thoughts occupy full lines.'),
    404: ('The speaker cries out, says the ship is full of rats and shouts for help.',
          'The separate cry for help preserves the startle and distress. This voice says nothing about the food.'),
    405: ('The speaker reports a huge infestation to the admiral and urgently asks if the food is safe.',
          'Keep the blunt warning and the whole urgent question on the following row.'),
    406: ('The older voice says rats are all over the ship and the food is at risk.',
          'Use the older speaker’s clipped alarm. Keep the infestation on one row and the danger to the food on the next.'),
    407: ('Alarmed by all the rats, the young speaker pleads that they leave his own food alone.',
          'Keep the personal plea on its own row. Its comic focus is the speaker’s meal, as in the source.'),
    408: ('The speaker urgently tells the admiral that rats are all over the ship and the food is at risk.',
          'Avoid splitting “all over the ship.” The complete warning keeps the explicit address and Manuel’s measured phrasing.'),
    2217: ('The expedition returns. There appears to be nothing around here.',
           'Preserve the emphatic report and uncertainty. The new line keeps “Looks like” with the conclusion.'),
    2218: ('The expedition returns. It looks like nothing noteworthy turned up.',
           'Keep the casual return and the narrower judgment about finds worth noting. The complete second sentence carries the qualification.'),
    2219: ('The expedition returns, but there seems to be nothing in the area.',
           '“By the looks of it” preserves the older speaker’s qualified, disappointed assessment. A separate sentence gives the turn its own beat.'),
    2220: ('The speaker relays the returning expedition’s report that there is nothing nearby.',
           'Keep the young speaker’s hearsay wording. The existing line break comes after the attribution and the complete reported clause follows.'),
    2221: ('The expedition has returned and it appears there is nothing nearby.',
           'Keep the formal opening and the qualified conclusion. “Apparently” marks the uncertainty and the complete second sentence stays together.'),
}


def encoded_changes():
    compile_protected = FunctionType(compile_layouts.__code__, compile_layouts.__globals__ | {'PHRASES': REVISIONS})
    guarded = compile_protected({n: {'english': ' '.join(lines)} for n, lines in REVISIONS.items() if n in RATS})
    # The unmodified shore-search wrapper formats logical paragraphs directly.
    return guarded | {n: ' '.join(lines).encode('ascii') for n, lines in REVISIONS.items() if n in SEARCH}


def original_groups(clean, current):
    receipt = base.load(SEA)
    rats = next(row for row in receipt['exact_native_event_groups'] if row['first_ID'] == 401)
    caller = rats['source_native_caller']
    first, stop = caller['load_PC'] - 0x02000000, caller['call_PC'] - 0x02000000 + 4
    assert current[first:stop] == clean[first:stop] == bytes.fromhex(caller['clean_and_current_hex'])
    assert caller['consumer'] == 0x02053D44 and rats['original_role_argument'] == 1
    specs = ((rats['selector'], caller['literal_address'], tuple(rats['table_slots'])),
             (0x02116EC0, 0x02079FFC, (2217, -1, 2218, -1, -1, 2219, 2220, 2221)))
    assert clean[0x79F90:0x79FA8] == current[0x79F90:0x79FA8]
    search_call, = unpack_from('<I', clean, 0x79F98)
    assert search_call >> 24 == 0xEB and (
        (0x02079FA0 + ((search_call & 0xFFFFFF) << 2)) & 0x03FFFFFF) == 0x02053D44
    groups = []
    for table, pointer, slots in specs:
        for arm in (clean, current):
            assert unpack_from('<I', arm, pointer - 0x02000000) == (table,)
            assert unpack_from('<8i', arm, table - 0x02000000) == slots
        groups.append(dict(table=table, consumer=0x02053D44, original_role_argument=1, slots=slots))
    return groups


def main():
    assert not ROOT.exists() and not MANUSCRIPT.exists()
    prior = base.load(parent.RELEASE)
    assert base.digest(base.REGISTRY) == prior['registry_sha256']
    assert base.digest(CLEAN) == prior['clean_input_sha256']
    ctx = RegisteredRuntime(parent.RELEASE, prior['own_registered_startup'], captain=3)
    clean = base.NdsImage.open(CLEAN)
    clean_arm = clean.read_file(ARM)
    arm, common = ctx.arm, ctx.common
    rat_group, search_group = original_groups(clean_arm, arm)
    source = common_message_entries(clean.read_file(COMMON), clean_arm)
    old = owned_entries(common, arm, digest(arm[DIRECTORY_OFFSET:TABLE_OFFSET]))
    edited = encoded_changes()
    target, installed, slots = owned_deployment(common, arm, old, edited)
    updated = with_components(ctx, arm, target)
    raster, _, font = font_tools(ctx.image)
    kanji = ctx.image.read_file('/GRP/KANJI.FNT')
    credited = {(r['file_path'], r['id']) for r in base.load(base.LEDGER)[base.CONTEXT]['integrated_record_keys']}
    rows, pages, results = [], [], []
    for n, actor in zip((*RATS, *SEARCH), ACTORS, strict=True):
        identifier = f'COMMON_MESSAGE_{n}'
        assert (COMMON, identifier) in credited
        s, a, b = source[n], old[n], installed[n]
        assert all(b'%' not in row.text for row in (s, a, b))
        group = rat_group if n in RATS else search_group
        before, after = [portrait_case(model, dict(message_ID=n), group, entry.text, actor)
                         for model, entry in ((ctx, a), (updated, b))]
        old_display, new_display = before.pop('display'), after.pop('display')
        planes = [render_portrait(raster, arm, kanji, display)[0] for display in (old_display, new_display)]
        lines = tuple(line.strip().decode('ascii') for line in new_display.split(b'\n'))
        assert 1 <= len(lines) <= 3
        if n in edited:
            assert lines == REVISIONS[n], (n, lines, new_display)
            assert planes[0] != planes[1]
            pages.extend(((f'{n} previous', planes[0]), (f'{n} revised', planes[1])))
        else:
            assert old_display == new_display and planes[0] == planes[1]
            pages.append((f'{n} retained', planes[1]))
        context = ('One of eight alternative warnings in the same rat infestation. The speaker reports the immediate threat. '
                   'The eight choices are different voices, and only one speaks in a given incident.') if n in RATS else (
                   'One of five alternative replies after a shore expedition returns from an apparently empty search. '
                   'The following fatigue notice reports the cost of the attempt, independently of the dialogue wording.')
        meaning, note = NOTES[n]
        rows.append(dict(id=identifier, message_ID=n, file_path=COMMON, speaker='Crew member selected by original voice',
            context=context, source_meaning=meaning, localization_note=note, Japanese=s.text.decode('cp932'),
            previous_English=' '.join(a.text.decode('ascii').split()), english=' '.join(lines),
            decision='revision' if n in edited else 'retention', source_reference=reference(s),
            current_reference=reference(a), staged_reference=reference(b), source_hex=s.text.hex(), current_hex=a.text.hex(),
            staged_hex=b.text.hex(), review=dict.fromkeys(GATES, True)))
        results.append(dict(message_ID=n, actor_example=actor, old_display_hex=old_display.hex(), display_hex=new_display.hex(),
                            lines=lines, old_plane_sha256=digest(planes[0]), plane_sha256=digest(planes[1]),
                            one_panel=True, original_wrapper_before=before, original_wrapper_after=after))
    ROOT.mkdir(parents=True)
    image = base.NdsImage.open(parent.ROM)
    before = files(image)
    image.replace_file(COMMON, target)
    assert {name for name, data in files(image).items() if data != before[name]} == {COMMON}
    image.save(ROM)
    image.replace_file(COMMON, common)
    assert bytes(image.rom.save()) == parent.ROM.read_bytes()
    candidate = base.digest(ROM)
    terminal = observed.ROOT / 'voyage/terminal.json'
    base.save(MANUSCRIPT, dict(translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=list(GATES), records=rows,
        candidate_sha256=candidate, previous_sha256=prior['candidate_sha256']))
    base.save(STORED, dict(candidate_sha256=candidate, previous_sha256=prior['candidate_sha256'],
        target_ARM9_sha256=digest(arm), target_COMMON_sha256=digest(target), allocations=slots,
        whole_parent_inverse=True, native_cases=results, font=font, sheets=portrait_sheets(ROOT, pages),
        original_voice_tables=[rat_group, search_group], original_rat_source_review=str(SEA),
        original_rat_source_review_sha256=base.digest(SEA), observation=str(terminal),
        observation_sha256=base.digest(terminal), manuscript_sha256=base.digest(MANUSCRIPT)))
    print('Staged six revisions, seven retentions and nineteen verified native previews.')


if __name__ == '__main__':
    main()
