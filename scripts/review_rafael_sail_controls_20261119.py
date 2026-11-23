"""Review Julio's full sail-control lesson and the crew's decision to sail for Athens."""

from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
from types import FunctionType, SimpleNamespace

from scripts import register_rafael_ceuta_contract_routes_20261119 as parent
from scripts import stage_story_short_phrase_wraps_20261119 as workflow
from scripts.review_rafael_early_phrase_wraps_20261118 import GATES, TOKEN, logical

base,native = workflow.base,workflow.native
ROOT = Path('work/rafael_early_navigation_source_20261119')
INTAKE = ROOT/'paired_source.json'
SOURCE,OUTPUT = ROOT/'sail_controls_paired_source_v3.json',ROOT/'sail_controls_contextual_v3.json'
STAGED = ROOT/'sail_controls_staged_v3'
ROM,PROOF = STAGED/'Rafael_Sail_Controls_STAGED.nds',STAGED/'stored_proof.json'
BLOCKS = ((128,),(),(),())
NAMES = {0:'Rafael Castor',4:'Janus Pasar',5:'Claudio Manaus',6:'Julio Erneco',254:'System'}
CONTEXT = ('Julio explains speed, anchoring and sail angles, and Rafael grows more confident. '
           'Julio remembers his request to sail to Athens. Clau teases him before the group realizes the trip concerns '
           'their future and their promise to Hayreddin.')
REVIEW = {
    12: ('Julio offers to teach Rafael the remaining things he can do while sailing.',
         'Phrase the offer as a question so Rafael’s assent answers it naturally.',
         "There's more you can do at sea. Want to see how, FI?",
         ("There's more you can do at sea.", 'Want to see how, FI?')),
    15: ('Rafael accepts the offer.', 'The polite assent is brief and follows Julio’s offer.', None, ()),
    20: ('Julio will explain when full sail and anchoring are useful.',
         'Keep the distinction between the two conditions that Julio explains next.', None, ()),
    23: ('Full sail gives the ship top speed. The captain must give direct orders to the Sail Handlers himself.',
         'Give the top-speed benefit its own sentence and keep the role and the captain’s responsibility together.',
         "Full sail gives you top speed. As captain, you'll have to direct the Sail Handlers yourself.",
         ('Full sail gives you top speed.', 'direct the Sail Handlers yourself.')),
    26: ('A learner can stay at half sail. One Sail Handler per mast can manage the sails automatically.',
         'Preserve the learning advice, one handler per mast and automatic trimming.',
         "Half sail is fine while you learn. Put a Sail Handler on each mast and they'll trim the sails for you.",
         ('Half sail is fine while you learn.', 'Put a Sail Handler on each mast', 'trim the sails for you.')),
    29: ('Full sail may be too fast to handle well. Half sail may be more convenient in battle.',
         'The existing two sentences preserve Julio’s qualifications and the separate battle advice.', None, ()),
    32: ('Anchoring can bring a dispersed fleet back together or let it ambush an enemy.',
         'Use direct nautical instructions and keep both tactical uses.',
         'Drop anchor to regroup if your ships spread out, or to lie in wait for an enemy.',
         ('Drop anchor to regroup', 'lie in wait for an enemy.')),
    36: ('Rafael indicates he understands.', 'The short reply makes room for the system instructions.', None, ()),
    42: ('The sail setting adjusts speed while at sea, and anchoring stops the ship in place.',
         'Explain the two effects in plain language before the button instructions.',
         'At sea, the sails set your speed. Drop anchor to stop in place.',
         ('At sea, the sails set your speed.', 'Drop anchor to stop in place.')),
    46: ('A and B change the sail setting. B reduces speed and A increases it.',
         'Keep both buttons and make their opposite effects easy to scan.',
         'Use A and B to adjust the sails. B slows you down. A speeds you up.',
         ('Use A and B to adjust the sails.', 'B slows you down.', 'A speeds you up.')),
    50: ('B at full sail changes to half sail and slows the ship.',
         'Keep the two sail states and the speed change in the same sentence.',
         'At full sail, press B to slow to half sail.', ('slow to half sail.',)),
    53: ('B at half sail drops anchor and stops the ship.',
         'Keep anchoring and stopping together without losing the starting state.',
         'Press B at half sail to anchor and stop in place.', ('anchor and stop in place.',)),
    56: ('A at anchor changes to half sail. A at half sail changes to full sail.',
         'Give each step a complete instruction with each sail setting intact.',
         'At anchor, press A for half sail. Press A again to go to full sail.',
         ('At anchor, press A for half sail.', 'Press A again to go to full sail.')),
    60: ('Even at half sail the captain has to direct the sails if there are too few Sail Handlers.',
         'Use the same Sail Handler role and preserve the staffing exception.',
         "Even at half sail, you have to direct the sails if you're short on Sail Handlers.",
         ('Even at half sail,', 'short on Sail Handlers.')),
    63: ('Rafael asks if Julio really means that.', 'The quick question fits Rafael’s surprise.', None, ()),
    68: ('The captain is bound to need top speed at some point and must learn to manage the sails.',
         'The existing wording follows Rafael’s surprise with the reason he needs to learn the controls.', None, ()),
    72: ('Rafael answers with a startled stammer.', 'Keep the stammer and exclamation.', None, ()),
    77: ('Speed chiefly depends on catching the wind at the back of the sails.',
         'Use a direct teaching sentence and keep the part of the sails clear.',
         'For speed, you want the wind to catch the back of the sails.', ('the back of the sails.',)),
    81: ('L and R set sail direction. Trimming the sails makes the ship go faster.',
         'Use plain control wording and the same trim term heard in Julio’s explanation.',
         'Turn the sails with L and R. Trim them well to pick up speed.',
         ('Turn the sails with L and R.', 'Trim them well to pick up speed.')),
    85: ('L turns the sails left and R turns them right.',
         'Keep each button and its direction in a complete instruction.',
         'Press L to turn the sails left. Press R to turn them right.',
         ('Press L to turn the sails left.', 'Press R to turn them right.')),
    89: ('The stylus sets the optimal sail angle. Touching the flagship stops it.',
         'Retain the automatic setting to the best angle and give stopping its own line.',
         'The stylus sets the best angle. Touch the flagship to stop.',
         ('The stylus sets the best angle.', 'Touch the flagship to stop.')),
    93: ('Watch the wind relative to the ship’s heading and turn the sails until it catches them from behind.',
         'The player adjusts the sails while using the wind and heading as references.',
         'Watch the wind and your heading. Trim the sails so the wind catches them from behind.',
         ('Watch the wind and your heading.', 'Trim the sails', 'from behind.')),
    97: ('A tailwind is fairly easy and a headwind takes some skill.',
         'The two short sentences keep the practical distinction and Julio’s qualification.', None, ()),
    101: ('The on-screen gauge shows speed, and the player should trim for the longest bar.',
          'Preserve the visual target and use the same sail-control verb.',
          'Watch the on-screen speed gauge. Trim for the longest possible bar.',
          ('Watch the on-screen speed gauge.', 'Trim for the longest possible bar.')),
    104: ('Julio has covered the basics and leaves Rafael to experiment.',
          'The existing close hands control back in Julio’s familiar tone.', None, ()),
    107: ('Rafael says he understands and will try.',
          'Keep both the acknowledgment and the leap into trying the controls.',
          "Got it. I'll give it a try!", ()),
    111: ('Julio wonders whether he has forgotten something.',
          'Keep the hesitant opening and trailing thought before Rafael’s reaction.', None, ()),
    114: ('Rafael reacts with confusion.', 'The single ASCII question mark leaves room for Julio to remember.', None, ()),
    128: ('Julio remembers and asks Rafael to take the fleet to Athens.',
          'Keep the recall, live name and courteous request together.',
          "Oh, that's right! FI, could you take us to Athens?", ('could you take us to Athens?',)),
    132: ('Rafael recalls that Athens is in Greece, toward the eastern Mediterranean.',
          'Keep the uncertain geography as Rafael’s own question.', None, ()),
    137: ('Julio confirms and says he has a little business there.',
          'Use his established contraction style in American English.',
          "Right. I've got a small errand.", ()),
    140: ('Clau asks whether the old man’s errand should determine their destination.',
          'Keep his familiar tease and let Julio answer the premise directly in the next turn.', None, ()),
    143: ('Julio says he is investigating something that will concern everyone, beyond his own errand.',
          'Give the objection and the group’s future their natural spoken progression.',
          "It's not just my business. I'm going to look into something. It matters to us all down the road.",
          ("It's not just my business.", "I'm going to look into something.", 'It matters to us all down the road.')),
    147: ('Rafael asks if Julio means a goal for the crew in the future.',
          'Keep the pause and the tentative “something like” as he thinks it through.', None, ()),
    152: ('Julio says it is roughly that.', 'The short qualification preserves his reserve.', None, ()),
    155: ('There is no immediate need to act, but the crew will need it eventually.',
          'Keep the distinction between present urgency and later need.',
          "No rush for now. We'll need it later, though.", ("We'll need it later, though.",)),
    164: ('Rafael confirms they will learn what it is in Athens.',
          'Keep his question about what arrival will reveal in one clear thought.',
          "So we'll find out in Athens?", ()),
    168: ('Julio confirms.', 'The one-word answer lets his next turn carry the reason.', None, ()),
    174: ('The trip also matters for keeping their promise to Hayreddin.',
          'The promise, name and added reason all remain clear.', None, ()),
    180: ('Clau tells Rafael the trip sounds interesting.',
          'Give his surprise room for a long player name and keep his enthusiasm in a complete sentence.',
          'Oh, FI! This sounds interesting!', ('Oh, FI!', 'This sounds interesting!')),
    184: ('Rafael agrees enthusiastically.', 'Keep the simple familiar agreement with Clau.', None, ()),
    189: ('Julio urges them to get on with it and says he is counting on Rafael.',
          'Use a familiar call to action with room for the live name and the separate assurance.',
          "FI, let's get moving. I'm counting on you!", ("let's get moving.", "I'm counting on you!")),
    200: ('Janus wonders what they will find.', 'The open question fits his restrained curiosity.', None, ()),
    207: ('Clau calls for setting off to find a goal.',
          'Keep Clau’s deliberately odd goal-hunting joke together so Rafael can react to it.',
          "All right! Let's go find a goal!", ("Let's go find a goal!",)),
    210: ('Rafael is puzzled by Clau’s way of putting it.',
          'Keep the amused reaction after Clau’s odd send-off.', None, ()),
}


def review():
    packet,release = map(base.load,(INTAKE,parent.RELEASE))
    assert packet['candidate_sha256']==release['candidate_sha256']==base.digest(parent.ROM)
    assert base.digest(base.REGISTRY)==release['registry_sha256'] and not OUTPUT.exists() and not SOURCE.exists()
    group, = (g for g in packet['groups'] if g['block']==128)
    assert {r['source_record_index'] for r in group['records']}==REVIEW.keys()
    rows=[]
    for r in group['records']:
        idx,selector=r['source_record_index'],r['selector']
        meaning,note,chosen,phrases=REVIEW[idx]
        old=logical(r['current_English'])
        english=chosen or old
        assert r['native_command_word']==0x4000 and not r['slots'] and english.isascii()
        assert TOKEN.findall(english)==TOKEN.findall(old)==TOKEN.findall(r['Japanese'])
        source,current=(dict(file_path=group['file_path'],block=128,offset=r[f'{side}_offset'],
            command_offset=r[f'{side}_command_offset'],archive_sha256=group[f'{side}_archive_sha256'],
            exact_stored_hex=bytes([selector]).hex()+r[f'{side}_body_hex']) for side in ('source','current'))
        source['record_index']=idx
        rows.append(dict(id=f'DK4_MES_B128_R{idx:04}',file_path=group['file_path'],route=0,block=128,
            kind='system-FE' if selector==254 else 'progressive',native_command_word=0x4000,source_selector=selector,native_slots=[],
            source_reference=source,current_reference=current,source_hex=source['exact_stored_hex'],current_hex=current['exact_stored_hex'],
            Japanese=r['Japanese'],previous_English=old,english=english,source_meaning=meaning,localization_note=note,speaker=NAMES[selector],
            context=CONTEXT,protected_phrases=list(phrases),decision='revision' if chosen else 'retention',finding='prose' if chosen else 'retention',
            review=dict.fromkeys(GATES,True)|{'formatting':False}))
    counts=dict(Counter(r['finding'] for r in rows))
    base.save(SOURCE,packet|dict(groups=[group],complete_intake_sha256=base.digest(INTAKE)))
    base.save(OUTPUT,dict(source_packet_sha256=base.digest(SOURCE),previous_sha256=release['candidate_sha256'],
        previous_registry_sha256=release['registry_sha256'],translation_policy='natural-dialogue-v2',target_locale='en-US',
        encoder='dialogue-relocatable-v1',review_gates=GATES,records=rows,counts=counts,new_coverage_credit=0,formatting_and_registration_pending=True))


def compile_lesson():
    main=workflow.env['main']
    scope=workflow.env|dict(parent=parent,paired=SimpleNamespace(BLOCKS=BLOCKS),
        review=SimpleNamespace(SOURCE=SOURCE,OUTPUT=OUTPUT),ROOT=STAGED,ROM=ROM,PROOF=PROOF)
    scope['catalogue_membership']=FunctionType(workflow.catalogue.catalogue_membership.__code__,scope)
    FunctionType(main.__code__,scope)()
    p=base.load(PROOF)
    assert p['whole_parent_inverse'] and p['changed_blocks']=={'/data/SC0.DK4':[128]}


if __name__=='__main__':
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('review','stage'))
    {'review':review,'stage':compile_lesson}[parser.parse_args().action]()
