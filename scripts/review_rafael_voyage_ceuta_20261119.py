"""Review Rafael's connected first-voyage and Ceuta sailing lessons."""

from argparse import ArgumentParser
from collections import Counter
from inspect import getsource
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import prepare_london_guild_assignments_20261118 as intake
from scripts import register_rafael_first_voyage_20261119 as voyage
from scripts import register_rafael_tavern_lesson_20261119 as parent
from scripts import stage_story_short_phrase_wraps_20261119 as workflow
from scripts.review_rafael_early_phrase_wraps_20261118 import GATES, TOKEN, logical
from scripts.source_locked_derivation_v5118 import checked_text

base, native = workflow.base, workflow.native
ROOT = Path('work/rafael_voyage_ceuta_20261119')
SOURCE, OUTPUT = ROOT / 'paired_source.json', ROOT / 'contextual_review_v3.json'
STAGED = ROOT / 'staged_v3'
ROM, PROOF = STAGED / 'Rafael_Voyage_Ceuta_STAGED.nds', STAGED / 'stored_proof.json'
BLOCKS = ((42, 127), (), (), ())
CONTEXT = {
    42: 'Julio takes Rafael to resupply after recruitment. Clau talks big about pirates, and Julio steers them toward '
        'visiting ports, meeting people and trading. Rafael takes the loan reminder seriously until Julio laughs it off.',
    127: 'Julio sets Ceuta as the destination. The system explains heading and sail controls, then Rafael can ask '
         'about the wind. Julio reassures him and explains what to do if the fleet encounters trouble en route.',
}
VOYAGE = {
    5: (None, 'The wording already works. Keep the whole invitation to stock up together.',
        ("you'll need food and water.", "Let's stock up at the Port.")),
    59: ("That's right. Try visiting ports in the Mediterranean, the North Sea, and places like that.",
         'Keep both regions as examples and let the phrase introducing them lead directly into the names.',
         ("That's right.", 'the Mediterranean,', 'the North Sea,')),
    95: ("If you let trading slide, you'll just keep losing money. It was my money to start with. Be careful with it.",
         'Keep Julio’s warning and personal reminder distinct so Rafael can take the reminder seriously in the next turn.',
         ("you'll just keep losing money.", 'It was my money to start with.', 'Be careful with it.')),
}
CEUTA = {
    5: ('Julio suggests sailing to Ceuta first.', 'Use Julio’s usual contraction and keep the order of priorities.',
        "Let's head for Ceuta first.", ()),
    9: ('Now they will actually move the ship.', 'The lively invitation turns the destination decision into action.', None, ()),
    13: ('First check the direction in which the ship is facing.', 'Use the short spoken instruction before Julio explains steering.',
         "First, see which way we're facing.", ('which way',)),
    16: ('Tell everyone the fleet’s course by turning the ship in the direction they want to go.',
         'Explain the instruction in Julio’s voice before the system displays the controls.',
         "Tell the crew where you're headed. Point the ship in the direction you want to sail.",
         ("Tell the crew where you're headed.", 'you want to sail.')),
    20: ('The D-Pad or stylus determines which way the ship moves.', 'State both steering controls in a complete sentence.',
         'Use the D-Pad or stylus to steer.', ('the D-Pad or stylus',)),
    23: ('Press the D-Pad toward the desired heading or touch the screen in that direction.',
         'Give the direction for the D-Pad and the corresponding place to touch on the screen.',
         'Press the D-Pad to aim the ship, or tap where you want to sail.',
         ('Press the D-Pad to aim the ship,', 'or tap where you want to sail.')),
    26: ('Using the stylus automatically sets the best sail angle. Touch the flagship to stop.',
         'Both actions are clear, and the short final command stays separate.', None, ()),
    29: ('Julio checks whether his explanation made sense.', 'The direct question leaves room for either answer.', None, ()),
    34: ('Rafael tells Julio he understands completely.', 'The brief, confident answer matches Rafael’s enthusiasm.', None, ()),
    36: ('Rafael doubts the wind direction is favorable.', 'The hedge and trailing pause set up Rafael’s question.', None, ()),
    44: ('Julio tells the admiral to keep it up.', 'The warm encouragement and source-supported address answer the confident choice.', None, ()),
    49: ('Rafael can set a heading and wonders whether they can move if the wind cannot catch the sails properly.',
         'Use Rafael’s tentative question and the usual sailing phrasing, followed by Julio’s tailwind answer.',
         "I can set our course, but will we move if the wind doesn't fill the sails?", ('fill the sails?',)),
    54: ('A headwind makes sailing difficult, but they should have a tailwind on the route to Ceuta.',
         'The contrast and qualified reassurance answer Rafael’s concern and preserve the actual wind direction.', None, ()),
    58: ('Rafael is still unsure it will work.', 'The brief question keeps the hesitation that prompts Julio’s proverb.', None, ()),
    63: ('Julio says doing it will be easier than worrying about it. They can return to Lisbon if they cannot get moving.',
         'Preserve the familiar meaning of the proverb and give the Lisbon fallback a clean landing.',
         "It'll be easier than you think. If we can't make headway, we can always go back to Lisbon.",
         ("It'll be easier than you think.", "If we can't make headway,", 'go back to Lisbon.')),
    70: ('Long voyages can bring sickness, rats, leaks and other trouble.', 'Give the examples a full line and preserve the trailing list.',
         'Long voyages can bring trouble. Sickness, rats, leaks...', ('Sickness, rats, leaks...',)),
    73: ('Many of those problems cannot be handled at sea, so make port as soon as possible.',
         'The direct advice and the original qualification follow the whole list of examples.', None, ()),
    77: ('If the fleet is in an abnormal condition, calling at a town restores it.',
         'The reference to the problems above is clear in the system’s instruction.', None, ()),
    80: ('Ceuta is southeast of the current position. Julio suggests checking the Route Map.',
         'Keep the direction, its point of reference, and the exact map command in Julio’s voice.',
         "Ceuta's southeast of here. Take a look at the Route Map.", ('Take a look at the Route Map.',)),
}
NAMES = {0: 'Rafael Castor', 4: 'Janus Pasar', 5: 'Claudio Manaus', 6: 'Julio Erneco', 254: 'System', None: 'Rafael Castor'}


def review():
    packet, previous, earlier = map(base.load, (SOURCE, parent.RELEASE, voyage.REVIEW))
    assert packet['candidate_sha256'] == previous['candidate_sha256'] == base.digest(parent.ROM)
    assert base.digest(base.REGISTRY) == previous['registry_sha256'] and not OUTPUT.exists()
    prior = {r['id']: r for r in earlier['records']}
    records = []
    for group in packet['groups']:
        block = group['block']
        for row in group['records']:
            idx, speaker = row['source_record_index'], row['selector']
            ident = f'DK4_MES_B{block}_R{idx:04}'
            old = logical(row['current_English'])
            source, current = (dict(file_path=group['file_path'], block=block, offset=row[f'{side}_offset'],
                command_offset=row[f'{side}_command_offset'], archive_sha256=group[f'{side}_archive_sha256'],
                exact_stored_hex=(bytes([speaker]).hex() if speaker is not None else '')+row[f'{side}_body_hex'])
                for side in ('source', 'current'))
            source['record_index'] = idx
            if speaker is None:
                source['source_index'] = current['source_index'] = row['slots'][0]
            if block == 42:
                previous_row = prior[ident]
                assert previous_row['source_hex'] == source['exact_stored_hex']
                assert previous_row['registered_reference']['exact_stored_hex'] == current['exact_stored_hex']
                meaning = previous_row['source_meaning']
                chosen, note, phrases = VOYAGE.get(idx, (None, previous_row['localization_note'], ()))
                change = idx in VOYAGE
            else:
                meaning, note, chosen, phrases = CEUTA[idx]
                change = chosen is not None
            english = chosen or old
            assert english.isascii() and TOKEN.findall(english) == TOKEN.findall(old) == TOKEN.findall(row['Japanese'])
            records.append(dict(id=ident, file_path=group['file_path'], route=0, block=block,
                kind='system-FE' if speaker == 254 else 'typed-choice-label' if speaker is None else 'progressive',
                native_command_word=row['native_command_word'], source_selector=speaker, native_slots=row['slots'],
                source_reference=source, current_reference=current, source_hex=source['exact_stored_hex'],
                current_hex=current['exact_stored_hex'], Japanese=row['Japanese'], previous_English=old, english=english,
                speaker=NAMES[speaker], source_meaning=meaning, context=CONTEXT[block], localization_note=note,
                protected_phrases=list(phrases), decision='revision' if change else 'retention',
                finding=('wrap' if english == old else 'prose') if change else 'retention',
                review=dict.fromkeys(GATES, True) | {'formatting': False}))
    assert len(records) == 47 and len({r['id'] for r in records}) == 47
    counts = dict(Counter(r['finding'] for r in records))
    base.save(OUTPUT, dict(source_packet_sha256=base.digest(SOURCE), previous_sha256=previous['candidate_sha256'],
        previous_registry_sha256=previous['registry_sha256'], translation_policy='natural-dialogue-v2', target_locale='en-US',
        encoder='dialogue-relocatable-v1', review_gates=GATES, records=records, counts=counts,
        new_coverage_credit=0, formatting_and_registration_pending=True))
    print(counts)


def compile_lesson():
    scope = workflow.env | dict(parent=parent, paired=SimpleNamespace(BLOCKS=BLOCKS),
        review=SimpleNamespace(SOURCE=SOURCE, OUTPUT=OUTPUT), ROOT=STAGED, ROM=ROM, PROOF=PROOF)
    scope['catalogue_membership'] = FunctionType(workflow.catalogue.catalogue_membership.__code__, scope)
    source = checked_text(getsource(workflow.workflow.main), {
        '    final = native.files(target)': '    final = native.files(target)\n    catalogue_membership(ctx.arm, initial, final)',
        'Assembled all revised guild exchanges with exact relative branches and whole-ROM inverse.':
            'Staged the connected voyages with exact command and whole-ROM inverses.',
    })
    exec(compile(source, __file__ + '::stage', 'exec'), scope)
    scope['main']()
    proof = base.load(PROOF)
    assert proof['whole_parent_inverse'] and proof['changed_blocks'] == {'/data/SC0.DK4': [42, 127]}


def pair_source():
    scope = vars(intake) | dict(parent=parent, ROOT=ROOT, BLOCKS=BLOCKS, CONTEXT=(CONTEXT[42] + ' ' + CONTEXT[127],))
    FunctionType(intake.main.__code__, scope)()


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('action', choices=('source', 'review', 'stage'))
    {'source': pair_source, 'review': review, 'stage': compile_lesson}[parser.parse_args().action]()
