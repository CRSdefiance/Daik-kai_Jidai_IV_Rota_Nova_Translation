"""Read the entire clean follow-up before current English;preserve arrival,gift direction andoutgoing notice."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B50_clean_gloss_v8483')
SOURCE=Path('work/analysis/Hodram_B50_clean_v8482/complete_clean_SC1_B50_EV1_andcoverage_before_current_English.json')
PREVIOUS=Path('work/analysis/Hodram_B49_clean_v8357/complete_clean_SC1_B49_EV1_andcoverage_before_current_English.json')
HANDOFF=Path('work/analysis/editorial_handoff_verification_v8481/verified_handoff.json')
GLOSSES={
    7:("Ah, you brought it for me?! Let me see, let me see!","The source greets the addressee's bringing the item and immediately asks to see it, with excited repetition. 持ってきてくれた is brought it for me, not merely already have it or found it. Do not invent lateness, an appointment, where it was found, hardship, a family relationship or rank."),
    10:("Wow! It really is cute! Here, I'll give you this! Yay! See you!","Her delighted confirmation, stretched cute exclamation, explicit offer of this, cheer and casual farewell form one progression. Keep the offer: unlike B49's later delighted farewell, this source includes はい、これあげる. Preserve this as the source's deictic object until the original item consumer is bound. やりー is a delighted cheer, not an order, singing, a victory award, affection or a new restriction. Do not collapse the repeated excited language into a different earlier record."),
    13:("Handed over the wristband of heavenly protection/favor.","The original FE system notice says 天佑のリストバンドを渡しました: the wristband is outgoing. Existing approved item wording is Heavenly Wristband, bound in the preceding review. This is not receipt of the wristband or a bow award, and FE is not a personal actor254/name. Native FE geometry, exact current output and actual B50 transition remain separate checks."),
}

if __name__=='__main__':
    assert not ROOT.exists();packet,previous,handoff=map(read,[SOURCE,PREVIOUS,HANDOFF]);group=deepcopy(packet['groups'][0])
    assert handoff['Hodram_B49_completed_once'] and handoff['completed']==7221 and packet['source_only_no_current_English_exposed_orused'] and not packet['inventory_failures']
    assert group['block']==50 and len(group['records'])==3 and group['completed_coverage_overlap']==0 and group['uncredited_source_positions']==3
    assert len(group['commands'])==12 and group['clean_stored_bytes']==236 and group['clean_logical_end']==234 and group['clean_tail_bytes']==2
    assert [r['source_record_index'] for r in group['records']]==[7,10,13] and [r['source_selector'] for r in group['records']]==[2,2,254]
    assert [(e['event_ID'],e['script_block'],e['must_be_completed'],e['must_not_be_completed']) for e in group['source_event_records']]==[(50,50,[49],[])]
    for row in group['records']:
        assert row['source_Japanese'] is not None and row['current_English_body_unread'];gloss,note=GLOSSES[row['source_record_index']]
        row.update(first_clean_source_gloss=gloss,source_context_note=note,whole_source_exchange_andoutgoing_notice_read=True,current_English_dialogue_still_unconsulted=True,source_meaning_only_not_localized_orformatting_approval=True,native_speaker_item_controls_FE_current_editorial_actual_andregistered_integration_pending=True)
    prior_notice=next(r for r in previous['groups'][0]['records'] if r['source_record_index']==81);notice=group['records'][-1]
    assert notice['source_hex']==prior_notice['source_hex'] and notice['source_Japanese']==prior_notice['source_Japanese']
    pictures=[c for c in group['commands'] if c['word']==0x4800];assert len(pictures)==1 and pictures[0]['offset']==214 and pictures[0]['whole_command_hex']=='004894a8'
    assert not any(c['word'] in [0x100,0x200,0x300,0x400,0x8000,0x8100,0x2100] for c in group['commands']) and group['commands'][-1]['word']==0 and group['commands'][-1]['native_extent']==4
    macros={token:sum(bytes.fromhex(r['source_hex'])[1:].count(token.encode()) for r in group['records']) for token in ['FI','FA','FO']};assert macros==dict(FI=0,FA=0,FO=0)
    ROOT.mkdir(parents=True);save(ROOT/'three_first_clean_glosses_gift_andoutgoing_wristband.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),groups=[group],all3_clean_utterances_glossed_before_current_English=True,complete_clean12_commands_three_preambles_fullterminal_andseparate2byte_tail_preserved=True,source_macro_counts=macros,source_FE_panels=1,source_no_relative_predicate_orchoice_commands=True,source_event50_explicitly_requires49_not_outer_eligibility_original_location_orfull_chronology_proof=True,previous_clean_notice=str(PREVIOUS),previous_clean_notice_sha256=sha(PREVIOUS.read_bytes()),same_literal_source_outgoing_notice_as_B49=True,previous_notice_source_reference=prior_notice['source_reference'],current_English_dialogue_bodies_still_unconsulted=True,no_new_prose_revision_name_item_native_actual_orregistered_approval=True,no_source_prose_orcompletion_credit=True,new_source_positions_uncredited=3,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,PREVIOUS,HANDOFF,Path(__file__)]}))
    print('B50 clean-first:3utterances/12commands glossed beforecurrentEnglish. Keep brought-it arrival,explicit this-gift,delightedcheer/farewell andoutgoingHeavenlyWristband notice. Event50requires49;no native/eligibility/actual orcredit claim.')
