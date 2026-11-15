"""Record whole-exchange source reasoning for the paired role-label revision draft."""
import struct
from pathlib import Path
from collections import defaultdict
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read, save

ROOT=Path('work/analysis/couple_context_review_v5775')
CENSUS=Path('work/analysis/couple_speaker_uses_v5773b/all_four_routes_direct_role_speech_census_and_complete_native_exchanges.json')
NAMES=Path('work/analysis/couple_name_consumers_v5774/four_current_native_role_getters_and_exact_staged_owners.json')
TEA=Path('work/analysis/couple_label_clean_context_v5766/four_complete_clean_route_exchanges_and_exact_couple_name_fields.json')
CONTEXTS={
 (0,169): ('Ian tavern observers',
   'Read all68 source speeches. The woman admires Ian and is delighted when he serves them; '
   'the man doubts Ian is male and later reacts jealously. They are unnamed observers. '
   'The wider exchange includes another patron touching Ian, his response, dismissal, ambush and recruitment. '
   'Do not present another speaker\'s gender assumptions or harassment as narrator fact.',
   ['She admires that person\'s beauty.', 'He questions whether that person is really male.',
    'She hushes him because Ian may hear.', 'She is excited that Ian brought their order.',
    'He objects to her delight and grumbles.']),
 (0,178): ('Fernando reads the distant breakup',
   'Read all63 source speeches. The captain guesses romantic conversation, but Fernando reads a breakup. '
   'The four distant lines confirm it. Surrounding dialogue explicitly calls them a couple. '
   'The woman rejects his way of thinking, he counters, she proposes not meeting again and he agrees they are through. '
   'The same role labels span a changing relationship; neither marriage nor unmarried status is certified.',
   ['She can no longer accept his thinking and calls him selfish.',
    'He says she can think that, but considers her selfish too.',
    'She concludes they should stop seeing each other.',
    'He agrees that if they both feel that way, they are through.']),
 (0,196): ('Tea and the purchase request shown in the screenshot',
   'Read all9 source speeches. They enjoy tea, wonder why it did not become popular earlier, '
   'agree to buy more for their shared supply and describe its comforting taste. '
   'The final unattributed notice forecasts a possible tea fashion in Sofala. '
   'Tea is explicit; retain it. A shared household supply does not establish marriage. '
   'The notice is tentative, not a shortage or guaranteed profit.',
   ['She praises how delicious the tea is.', 'He agrees tea is wonderful.',
    'She wonders why something so good did not catch on sooner.',
    'He agrees and says people have poor judgment.',
    'She says their tea is running low and asks him to buy some tomorrow.',
    'He promises to buy it.', 'She finds the taste comforting.',
    'He says they cannot live without tea.']),
 (0,197): ('Cold weather and fur demand',
   'Read all8 source speeches. They discuss unusual cold, a desired fur coat, '
   'reported fur sales and rising prices, and a wish for warmer weather. '
   'The final notice forecasts a possible fur fashion in Stockholm. '
   'Reported price changes and tentative trend wording must remain distinct. '
   'Nothing here establishes age, marriage or profession.',
   ['She complains about the cold.', 'He says it has not been this cold in a long time.',
    'She wants a fur coat and feels she might freeze.',
    'He reports that the cold is increasing fur sales and prices.',
    'She has heard the same and remains cold.', 'He hopes it warms up soon.',
    'She agrees but still wants fur while it stays cold.']),
 (1,172): ('Mikhail conversation without this woman\'s partner present',
   'Read all64 source speeches. The woman admires the old man\'s knowledge; another woman asks about '
   'supposed pepper which he identifies as rabbit droppings. He later makes a sexual comment and '
   'this woman calls him lecherous. Her colloquial address to the old man does not make him her grandfather. '
   'Julio\'s expressly mentioned granddaughter relationship elsewhere cannot be assigned to actor165. '
   'Actor164 is absent from this local exchange, making a compulsory couple description especially awkward.',
   ['She exclaims that the old man is amazing.',
    'She praises his broad knowledge and asks why he knows so much.',
    'She protests that he is being lecherous.'])
}

if __name__=='__main__':
    assert not ROOT.exists()
    census,names,tea=map(read,[CENSUS,NAMES,TEA])
    groups=defaultdict(list)
    for block in census['selected_native_blocks']:
        signature=tuple(r['source_hex'] for r in block['direct_couple_speech_records'])
        groups[signature].append(block)
    assert len(groups)==5
    contexts=[]
    for key,(title,reason,glosses) in CONTEXTS.items():
        block=next(b for b in census['selected_native_blocks'] if (b['route'],b['block'])==key)
        direct=block['direct_couple_speech_records']
        assert len(direct)==len(glosses)
        copies=groups[tuple(r['source_hex'] for r in direct)]
        contexts.append(dict(title=title,representative=dict(route=key[0],block=key[1],file_path=block['file_path'],
            source_block_sha256=block['source_block_sha256']),
            complete_representative_exchange_speeches_read=len(block['all_speech_records']),
            whole_exchange_source_reasoning=reason,
            individually_glossed_role_utterances=[dict(**r,source_context_gloss=g) for r,g in zip(direct,glosses)],
            identical_role_sequence_copies=[dict(route=b['route'],block=b['block'],file_path=b['file_path'],
                source_block_sha256=b['source_block_sha256'],exact_role_source_references=[r['source_reference'] for r in b['direct_couple_speech_records']]) for b in copies],
            only_role_sequence_identical_not_all_surrounding_route_dialogue=True,
            all_other_route_full_exchange_manual_rereads_not_claimed=True))
    assert sum(c['complete_representative_exchange_speeches_read'] for c in contexts)==212
    assert sum(len(c['individually_glossed_role_utterances']) for c in contexts)==27
    decisions=[]
    for ident,english in [(164,'Man'),(165,'Woman')]:
        owner=next(r for r in names['current_exact_owners'] if r['actor_ID']==ident)
        field=next(r for r in tea['source_name_fields'] if r['actor_ID']==ident)
        decisions.append(dict(actor_ID=ident,source_reference=field,current_reference=owner,
            editorial_decision='propose-revision',proposed_English=english,
            finding='Current label reads like a literal description of an internal role identifier.',
            rationale='Use a natural unnamed gendered speaker label across all five source contexts. '
                'The dialogue and surrounding scene retain the source-explicit couple relationship where it matters. '
                'Do not insert a relationship label into scenes in which the partner is absent, or a breakup is underway.',
            preserves_source_identification_function=True,
            relationship_information_in_conversation_must_not_be_erased=True,
            rejected_alternatives={
                'Husband/Wife':'Adds an unestablished marriage.',
                'Young Man/Young Woman':'Adds an unestablished age.',
                'Boyfriend/Girlfriend':'Adds certainty about relationship form and sounds odd after the breakup.',
                'Tea-Loving Man/Tea-Loving Woman':'Defines all appearances by one incidental scene.',
                'Couple (Man)/Couple (Woman)':'Still reads like a catalog identifier.',
                'Partner':'Relationship-first label is awkward when the partner is absent or the relationship ends.'},
            earlier_literal_label_rationale_preserved_not_overwritten=True,
            target_native_display_and_runtime_substitution_consumer_review_pending=True,
            registered_integration_pending=True,new_editorial_completion_credit=0))
    arm=NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    story_names=[]
    for ident in [2,9,22]:
        parts=[]
        for delta in [0,4,8]:
            field=0x120B80+ident*32+delta;p=struct.unpack_from('<I',arm,field)[0]
            if not p:parts.append(dict(pointer_field=field,null=True));continue
            at=p-0x02000000;raw=arm[at:arm.index(0,at)+1]
            parts.append(dict(pointer_field=field,pointer=p,storage_offset=at,terminated_hex=raw.hex(),Japanese=raw[:-1].decode('cp932')))
        story_names.append(dict(actor_ID=ident,source_file='/__arm9__.bin',source_fields=parts,
            localization_status='binding only; no fresh global name retention or revision credit'))
    assert story_names[2]['source_fields'][2]['Japanese']=='ダ'
    ROOT.mkdir(parents=True)
    save(ROOT/'five_whole_source_contexts_paired_label_draft_and_B199_name_fields.json',dict(
        policy='natural-dialogue-v2',target_locale='en-US',contexts=contexts,paired_nameplate_decisions=decisions,
        clean_literal_direct_role_census=dict(stored_blocks=1307,selected_blocks=17,direct_role_speeches=96,
            stored_full_context_speeches=581,distinct_role_sequences=5),
        manual_review_scope=dict(complete_representative_exchanges=5,complete_representative_speeches=212,
            distinct_role_utterances=27,all581_manually_reread=False),
        current_English_dialogue_not_used_as_translation_source=True,
        original207_name_queue_and_other_discovered_alias_consumers_remain_open=True,
        native_current_getters_establish_behavior_not_proposed_label_display_approval=True,
        B199_clean_name_fields=story_names,
        Samwell_full_catalogue_untranslated_middle_field_remains_open_no_silent_Romanization=True,
        portrait_subject_Rocco_name_spelling_not_approved_from_katakana_alone=True,
        no_new_ROM_or_emulator_run_or_completed_dialogue_credit=True,
        no_duplicate_credit_for_previously_integrated_Lil_B184_or_other_shared_copies=True,
        evidence={str(p):sha(p.read_bytes()) for p in [CENSUS,NAMES,TEA,Path(__file__)]},
        full_goal_complete=False))
    print('Five whole source contexts/212 representative speeches;27 distinct role utterances. Man/Woman draft; no build or completion credit.')
