"""Review and stage Julio's recruitment lesson using the registered Rafael candidate."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import prepare_london_guild_assignments_20261118 as intake
from scripts import register_rafael_deck_after_trade_20261119 as parent
from scripts import stage_story_tag_wraps_20261118 as template
from scripts.review_rafael_early_phrase_wraps_20261118 import GATES, TOKEN, logical
from scripts.source_locked_derivation_v5118 import checked_text

base, native, stage = template.base, template.native, template.stage
ROOT = Path('work/rafael_tutorial_natural_followthrough_20261119/paired_tavern')
SOURCE, OUTPUT = ROOT / 'paired_source.json', ROOT / 'contextual_review_v3.json'
STAGED = ROOT.parent / 'staged_tavern_v3'
ROM, PROOF = STAGED / 'Rafael_Tavern_Lesson_STAGED.nds', STAGED / 'stored_proof.json'
BLOCKS = ((138,), (), (), ())
CONTEXT = ('Julio takes Rafael through the Tavern recruitment sequence. He explains why the ship needs sailors, '
           'offers a way to attract them, and points out two decisions the player will make shortly. '
           'He ends with a warning about taking on too many sailors and invites Rafael to try.',)
LESSON = {
    6: ('Before they can get anywhere, the ship must be able to move. The people already aboard cannot handle her '
        'well by themselves and need sailors to help.',
        'Let Julio explain the practical problem before he says what they need.',
        "First we've got to get underway. We can't handle her on our own. We'll need some sailors.",
        ("First we've got to get underway.", "We can't handle her on our own.", "We'll need some sailors.")),
    10: ('Serving drinks is a good way to draw sailors in and show the admiral’s generosity.',
         'Keep the advice optional and use the same buying-a-round idiom as the next turn.',
         'Buy a round for the room. A generous admiral draws a crowd.',
         ('Buy a round for the room.', 'A generous admiral draws a crowd.')),
    14: ('A drink is welcome. Early on, they can probably find enough sailors without treating the room.',
         'Keep Julio’s dry first sentence. Let his reassurance follow as one thought without the inherited four short rows.',
         'Nobody minds a free drink. For now, you should find enough sailors without buying a round.',
         ('Nobody minds a free drink.', 'without buying a round.')),
    18: ('Julio wonders how many sailors will turn up when Rafael chooses the recruitment command.',
         'Retain the curious invitation and the verified Recruit Crew label. Both existing lines are complete.',
         None, ()),
    21: ('Assign the sailors after recruiting. The Flagship option is enough when the fleet has only one ship.',
         'Connect the instruction to recruitment and keep the exact menu choice and its one-ship condition.',
         "Once they join, assign your crew. If you've only got one ship, just choose Flagship.",
         ('Once they join, assign your crew.', "If you've only got one ship,", 'just choose Flagship.')),
    25: ('More sailors reduce the number of days the fleet can sail. Take care when hiring more than necessary.',
         'Explain the time at sea and preserve Julio’s specific warning about hiring beyond what they need.',
         'More hands mean fewer days at sea. Think twice before you hire more than you need.',
         ('More hands mean fewer days at sea.', 'more than you need.')),
    29: ('Julio tells Rafael to give it a try.',
         'The short invitation closes the lesson and hands control back before the barkeep greets Rafael.',
         None, ()),
}


def review():
    assert not OUTPUT.exists()
    if not SOURCE.exists():
        FunctionType(intake.main.__code__, vars(intake) | globals())()
    packet, release = map(base.load, (SOURCE, parent.RELEASE))
    assert packet['candidate_sha256'] == release['candidate_sha256'] == base.digest(parent.ROM)
    group, = packet['groups']
    assert {r['source_record_index'] for r in group['records']} == LESSON.keys()
    records = []
    for row in group['records']:
        idx = row['source_record_index']
        meaning, note, proposed, phrases = LESSON[idx]
        old = logical(row['current_English'])
        english = proposed or old
        revise = proposed is not None
        assert row['native_command_word'] == 0x4000 and row['selector'] == 6 and not row['slots']
        assert english.isascii() and not any(TOKEN.findall(s) for s in (english, old, row['Japanese']))
        source, current = (dict(file_path=group['file_path'], block=138, offset=row[f'{side}_offset'],
            command_offset=row[f'{side}_command_offset'], archive_sha256=group[f'{side}_archive_sha256'],
            exact_stored_hex='06' + row[f'{side}_body_hex']) for side in ('source', 'current'))
        source['record_index'] = idx
        records.append(dict(id=f'DK4_MES_B138_R{idx:04}', file_path=group['file_path'], route=0, block=138,
            kind='progressive', native_command_word=0x4000, source_selector=6, native_slots=[],
            source_reference=source, current_reference=current, source_hex=source['exact_stored_hex'],
            current_hex=current['exact_stored_hex'], Japanese=row['Japanese'], previous_English=old,
            english=english, speaker='Julio Erneco', source_meaning=meaning, context=CONTEXT[0],
            localization_note=note, protected_phrases=list(phrases),
            finding='prose' if revise else 'retention',
            decision='revision' if revise else 'retention', review=dict.fromkeys(GATES, True) | {'formatting': False}))
    base.save(OUTPUT, dict(source_packet_sha256=base.digest(SOURCE), previous_sha256=release['candidate_sha256'],
        previous_registry_sha256=release['registry_sha256'], translation_policy='natural-dialogue-v2',
        target_locale='en-US', encoder='dialogue-relocatable-v1', review_gates=GATES, records=records,
        new_coverage_credit=0, formatting_and_registration_pending=True))


def compile_lesson():
    scope = template.env | globals() | dict(paired=SimpleNamespace(BLOCKS=BLOCKS),
        review=SimpleNamespace(SOURCE=SOURCE, OUTPUT=OUTPUT), ROOT=STAGED, logical_end=template.logical_end)
    scope['catalogue_membership'] = FunctionType(template.catalogue_membership.__code__, scope)
    script = checked_text(getsource(template.precedent.main), {
        '    final = native.files(target)': '    final = native.files(target)\n    catalogue_membership(ctx.arm, initial, final)',
        'Assembled all revised guild exchanges with exact relative branches and whole-ROM inverse.':
            'Staged the revised recruitment lesson with exact catalogue ownership and whole-ROM inverse.',
    })
    exec(compile(script, __file__ + '::stage', 'exec'), scope)
    scope['main']()
    proof = base.load(PROOF)
    assert proof['whole_parent_inverse'] and proof['changed_blocks'] == {'/data/SC0.DK4': [138]}


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('review', 'stage'))
    {'review': review, 'stage': compile_lesson}[parser.parse_args().action]()
