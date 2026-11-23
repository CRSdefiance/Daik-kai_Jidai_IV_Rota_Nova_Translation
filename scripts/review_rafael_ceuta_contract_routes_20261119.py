"""Review Ceuta's trading-rights and sea-route lessons with their original controls."""

from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
from types import FunctionType, SimpleNamespace

from dk4tool.dialogue.codec import parse_markup, tokens_to_bytes
from scripts import audit_rafael_ceuta_arrival_20261119 as observed
from scripts import register_rafael_voyage_ceuta_20261119 as parent
from scripts import ruin_puzzle_fe_20261118 as system
from scripts import stage_rafael_first_voyage_debrief_20261119 as workflow
from scripts import verify_shared_notice_faction_bound_v1 as company
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.review_rafael_early_phrase_wraps_20261118 import GATES, TOKEN, logical

base, native = workflow.base, workflow.native
ROOT = observed.PAIR.parent
SOURCE, OUTPUT = observed.PAIR, ROOT / 'contextual_review_v2.json'
STAGED = ROOT / 'staged_v2'
ROM, PROOF = STAGED / 'Rafael_Ceuta_Contract_Routes_STAGED.nds', STAGED / 'stored_proof.json'
BLOCKS = ((45,139), (), (), ())
CONTEXT = {
    45: 'Rafael reaches Ceuta. Julio explains local trade rights, the contract he already arranged, and what the company share means for purchases.',
    139: 'Julio offers to explain connected sea routes. Rafael accepts on the observed path. Julio needs a sextant to serve as Surveyor, and Clau teases him.',
}
NAMES = {0:'Rafael Castor', 5:'Claudio Manaus', 6:'Julio Erneco', 254:'System', None:'Rafael Castor'}
CONTRACT = {
    5: ('Rafael wonders where Julio went.', 'A direct question sets up Julio’s answer from the Market.', None, ()),
    9: ('Julio calls Rafael over.', 'The brief familiar call answers Rafael immediately.', None, ()),
    13: ('Rafael realizes Julio is at the Market.', 'Keep the recognition and the exact Market label.', None, ()),
    18: ('Julio suggests trying to sell goods and names any purchased in Lisbon as an option before qualifying the advice.',
         'Use a clear conditional and give the caveat its own beat.',
         'Try selling some trade goods here. If you bought any in Lisbon, you can sell those. But remember...',
         ('If you bought any in Lisbon,', 'you can sell those.', 'But remember...')),
    21: ('Selling needs a contract.', 'The turn answers the caveat and gives Rafael something specific to ask about.', None, ()),
    24: ('Rafael asks about the contract.', 'The short echoed question fits the moment.', None, ()),
    29: ('Pay the ruler a fee at the Palace or Governor’s Office for the right to trade.',
         'The facility names, payment recipient and purpose are all clear in the existing three lines.', None, ()),
    33: ('Get contracts in several towns, with the minimum fee enough early on.',
         'Keep the qualification about when the minimum is enough.', None, ()),
    37: ('Julio arranged Ceuta’s contract and leaves future ones to Rafael.',
         'Keep Julio’s first-person claim and the shift of responsibility.', None, ()),
    52: ('The company holds a 20 percent share in Ceuta. The share determines purchasable local stock.',
         'Keep the company substitution and exact percentage. Explain the buying limit in a full clause and keep local stock together.',
         "FO has 20 percent of Ceuta's market. Your share caps how much local stock you can buy.",
         ('FO has 20 percent', "of Ceuta's market.", 'how much local stock you can buy.')),
    58: ('Julio invites Rafael to sell anything he wants to sell.', 'The invitation keeps the sale optional.', None, ()),
    61: ('Rafael agrees to do as Julio suggested.', 'Let Rafael answer the invitation without echoing Julio’s opening phrase.',
         'Yes, I will.', ()),
}
ROUTES = {
    5: ('Julio asks how Rafael is getting on and offers to explain confusing sea routes.',
        'Keep the personal check-in, the live name and the offer together in Julio’s voice.',
        "How's it going, FI? Sea routes can be confusing. Want me to explain how they work?",
        ("How's it going, FI?", 'Sea routes can be confusing.', 'Want me to explain how they work?')),
    10: ('Rafael accepts politely.', 'The short direct answer is appropriate for a choice.', None, ()),
    12: ('Rafael politely declines because he understands.', 'Keep the refusal and assurance in the existing choice.', None, ()),
    19: ('Contracts with nearby neighboring towns or ports create a sea route.', 'The rule is clear in the current two lines.', None, ()),
    23: ('Julio gives Lisbon and Ceuta as examples of towns the company has contracts with.',
         'Use the same contract term as the Ceuta lesson and keep both towns together.',
         'For example, FO has contracts in Lisbon and Ceuta.', ('has contracts in Lisbon and Ceuta.',)),
    27: ('Since the towns are neighbors, the company has a sea route between them.',
         'Make the reason explicit and leave enough width for the company name.',
         'Lisbon and Ceuta are neighbors. That gives FO a sea route between them.',
         ('Lisbon and Ceuta are neighbors.', 'That gives FO', 'a sea route between them.')),
    30: ('With a Captain and Surveyor assigned, a sea route enables Auto Move.',
         'Use the exact Deck View and Auto Move labels alongside both required jobs.',
         'Assign a Captain and Surveyor in Deck View to use Auto Move along a sea route.',
         ('Captain and Surveyor', 'Deck View', 'Auto Move', 'along a sea route.')),
    34: ('Rafael echoes the Auto Move command as a question.', 'Retain the exact short question before Julio expands on it.', None, ()),
    39: ('Pick a destination on the connected route and the navigators will steer the ship without further commands.',
         'Have Julio explain what Rafael needs to do and what the navigators take over.',
         'Pick a destination along the route. We navigators will do the steering.',
         ('a destination along the route.', 'We navigators will do the steering.')),
    42: ('Choose Auto Move at the Port and select a destination on the Route Map.',
         'Give the two actions in order and keep the exact menu captions together.',
         'At the Port, choose Auto Move. Set a destination on the Route Map.',
         ('choose Auto Move.', 'Set a destination on the Route Map.')),
    55: ('Julio pauses before he points out a problem.', 'Keep the deliberate short pause before Rafael reacts.', None, ()),
    59: ('Rafael reacts with silent confusion.', 'The short reaction leaves the explanation to Julio.', None, ()),
    64: ('Julio says nobody in the fleet can serve as Surveyor.', 'Keep the stated fleet scope and capitalize the assigned role.',
         'None of us can serve as Surveyor...', ()),
    67: ('Clau ribs Julio for talking big and being unable to survey.', 'The teasing and familiar address fit Clau’s relationship to Julio.', None, ()),
    71: ('Julio accepts the setback and asks them to buy a sextant in Lisbon. With it, he can manage.',
         'Let the reluctant opening and the practical solution land separately.',
         'No help for it... Buy a sextant in Lisbon. With that, I can manage.',
         ('Buy a sextant in Lisbon.', 'With that, I can manage.')),
    74: ('Julio reminds Rafael to equip the item on him.', 'Use his usual contraction and preserve the Equip action.',
         "Don't forget to equip me with it.", ()),
    77: ('Rafael asks what equipping means.', 'The short echo sets up Julio’s answer and preserves the control term.', None, ()),
    82: ('Julio says to examine the item after buying it and tells Rafael to head to Lisbon.',
         'Keep the timing and the destination in Julio’s direct teaching voice.',
         "Look at the item once you buy it. You'll see what to do. For now, head to Lisbon.",
         ('Look at the item once you buy it.', 'head to Lisbon.')),
    85: ('Rafael answers with a hesitant yes.', 'The stammer shows Rafael following an instruction he is still learning.', None, ()),
    102: ('Julio wishes Rafael luck.', 'The short closing suits the alternate path.', None, ()),
}


def review():
    packet, release, actual = map(base.load, (SOURCE, parent.RELEASE, observed.OUTPUT))
    assert packet['candidate_sha256'] == actual['candidate_sha256'] == release['candidate_sha256'] == base.digest(parent.ROM)
    assert not OUTPUT.exists() and base.digest(base.REGISTRY) == release['registry_sha256']
    records = []
    for group, decisions in zip(packet['groups'], (CONTRACT,ROUTES),strict=True):
        block = group['block']
        assert {r['source_record_index'] for r in group['records']} == decisions.keys()
        for raw in group['records']:
            idx, selector = raw['source_record_index'], raw['selector']
            meaning, note, proposed, phrases = decisions[idx]
            old = logical(raw['current_English'])
            english = proposed or old
            assert english.isascii() and TOKEN.findall(english) == TOKEN.findall(old) == TOKEN.findall(raw['Japanese'])
            source, current = (dict(file_path=group['file_path'],block=block,offset=raw[f'{side}_offset'],
                command_offset=raw[f'{side}_command_offset'],archive_sha256=group[f'{side}_archive_sha256'],
                exact_stored_hex=(bytes([selector]).hex() if selector is not None else '')+raw[f'{side}_body_hex'])
                for side in ('source','current'))
            source['record_index'] = idx
            if selector is None:
                source['source_index'] = current['source_index'] = raw['slots'][0]
            records.append(dict(id=f'DK4_MES_B{block}_R{idx:04}',file_path=group['file_path'],route=0,block=block,
                kind='system-FE' if selector == 254 else 'typed-choice-label' if selector is None else 'progressive',
                native_command_word=raw['native_command_word'],source_selector=selector,native_slots=raw['slots'],
                source_reference=source,current_reference=current,source_hex=source['exact_stored_hex'],
                current_hex=current['exact_stored_hex'],Japanese=raw['Japanese'],previous_English=old,english=english,
                source_meaning=meaning,localization_note=note,context=CONTEXT[block],speaker=NAMES[selector],
                protected_phrases=list(phrases),finding='prose' if proposed else 'retention',
                decision='revision' if proposed else 'retention',review=dict.fromkeys(GATES,True)|{'formatting':False}))
    assert len(records) == 32
    counts = dict(Counter(r['finding'] for r in records))
    base.save(OUTPUT,dict(source_packet_sha256=base.digest(SOURCE),previous_sha256=release['candidate_sha256'],
        previous_registry_sha256=release['registry_sha256'],translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=GATES,records=records,counts=counts,
        ordinary_gameplay_reference=str(observed.OUTPUT),ordinary_gameplay_sha256=base.digest(observed.OUTPUT),
        new_coverage_credit=0,formatting_and_registration_pending=True))
    print(counts)


def fe_layout(row, painter):
    assert row['id'] == 'DK4_MES_B45_R0052' and TOKEN.findall(row['english']) == ['FO']
    assert company.CAPACITY == 18 and workflow.MAX_COMPANY_CELLS == 20
    longest = 'W' * workflow.MAX_COMPANY_CELLS
    cases = ('Castor Co.', 'I', 'ABCDEFGHIJKLMNOPQRST', 'ABCDEFGHIJKLMNOPQRS', *company.NAMES)
    phrases = [phrase.replace('FO', longest) for phrase in row['protected_phrases']]
    for _, maximum_rows, _ in system.candidate_rows(row['english'].replace('FO',longest),phrases):
        lines = [line.replace(longest,'FO') for line in maximum_rows]
        options = '{SPEAKER:FE}' + '{LB}'.join(lines)
        raw = tokens_to_bytes(parse_markup(options),guard_linebreaks=True,pair_phase_safe_breaks=True)
        proof = []
        for name in cases:
            supplied = raw[1:].replace(b'FO',name.encode('cp932'))
            try:
                render = painter(supplied)
                events = render['events']
                assert render['complete_consumed_bytes'] == len(supplied)
                assert all(not any(render['physical'][y*228+216:(y+1)*228]) for y in range(64))
                for i, line in enumerate(lines):
                    expected = [c for c in codes(line.replace('FO',name).encode('cp932')) if c != 32]
                    assert [e['code'] for e in events if e['y']==12*i and e['code']!=32] == expected
                proof.append(dict(name=name,glyph_count=sum(e['code']!=32 for e in events),
                    complete_rows_and_right_bound=True,expanded_body_hex=supplied.hex()))
            except AssertionError:
                break
        else:
            return raw[1:],dict(lines=[line.replace('FO','{MACRO:FO}') for line in lines],expected_native_pages=1,
                encoded_hex=raw.hex(),company_render_cases=proof,original_company_editor_limit=company.CAPACITY)
    raise AssertionError('No company-safe Ceuta share layout')


def rebuild_function():
    original = workflow.rebuild_function()
    scope = original.__globals__ | dict(plan_fe=fe_layout)
    for handler in (workflow.stage.changed_speech, workflow.stage.changed_styles):
        scope[handler.__name__] = FunctionType(handler.__code__,scope)
    return FunctionType(original.__code__,scope)


def compile_lesson():
    template = workflow.workflow
    scope = template.env | dict(parent=parent,paired=SimpleNamespace(BLOCKS=BLOCKS),
        review=SimpleNamespace(SOURCE=SOURCE,OUTPUT=OUTPUT),ROOT=STAGED,ROM=ROM,PROOF=PROOF,rebuild_function=rebuild_function)
    scope['catalogue_membership'] = FunctionType(template.catalogue.catalogue_membership.__code__,scope)
    FunctionType(template.env['main'].__code__,scope)()
    proof = base.load(PROOF)
    assert proof['whole_parent_inverse'] and proof['changed_blocks'] == {'/data/SC0.DK4':[45,139]}


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('review','stage'))
    {'review':review,'stage':compile_lesson}[parser.parse_args().action]()
