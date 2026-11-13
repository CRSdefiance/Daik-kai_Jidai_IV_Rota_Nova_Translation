"""First clean-source gloss of Lil's complete wristband trade exchange, before current English."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
SOURCE=Path('work/analysis/Hodram_B49_clean_v8357/complete_clean_SC1_B49_EV1_andcoverage_before_current_English.json')
ROOT=Path('work/analysis/Hodram_B49_clean_gloss_v8358')
GLOSSES={
6:("Ah, here you are!",'Lil greets the arriving addressee with casual, eager repetition. Do not add lateness, impatience or a prior appointment.'),
10:("Heh-heh. This is the proof of supremacy around here, so I cannot just hand it over that easily after all.",'Playful, self-satisfied bargaining over the object she displays; this region, not the whole world. Do not invent her rank, legal ownership, territorial conquest or an actual victory for the player.'),
15:("...",'Hodram has an explicit source silence. Preserve the quiet reaction and do not supply spoken agreement, irritation or a motive.'),
19:("But there is one thing I would be willing to trade it for.",'One particular desired object qualifies her reluctance to give up the bow. She offers an exchange, not a free gift or money price.'),
22:("It is called something like the ten-yu wristband, and it is just such a super-cute item!",'Lil gives the title phonetically in hiragana and enthusiastically stretches her slang. Formal clean notice later spells it 天佑のリストバンド, a wristband of heavenly protection/favor; approved English item label remains unconsulted and must be bound separately. Do not infer a combat stat, magical power, deity or rarity.'),
33:("I hear it is somewhere in the New World. If you find it and bring it back, I will give you this. See you, bye-bye!",'Hearsay and an indefinite location, with a conditional exchange promise. Do not invent a town, island, map location, certainty of finding it or unconditional award.'),
40:("Huh, you have it? Let me see, let me see!",'Surprised excitement on the source possession-related branch. Exact raw predicate and branch selection are not yet proven by this prose gloss.'),
43:("Wow! It really is cute! Hey, give it to me! I will give you this bow and arrows in return!",'Her excited bargaining is about the wristband. The clean source explicitly names the offered bow/arrows here; preserve trade direction without inventing a completed handover or additional reward.'),
58:("Yes! No changing your mind afterward! See you!",'Triumphant, playful insistence that the addressee stick with the trade; do not turn this into a threat, permanent oath or new gameplay restriction.'),
64:("What?! It is a proof of supremacy, you know! You do not want it?",'Disbelieving follow-up to refusal in the presented exchange. Preserve the question rather than asserting that Hodram has no interest. Native choice control flow remains a separate check.'),
67:("...It is not that I do not want it.",'Hodram quietly qualifies the apparent refusal. Keep his restrained voice and the negated denial; do not reverse this into I do not want it or an explicit enthusiastic acceptance.'),
71:("Right, right! Here, I will give you this, so give me that!",'Lil takes up his qualification and presses the reciprocal exchange. This/that follow the bow-for-wristband direction; do not invent grabbing, theft or affection.'),
74:("Wow! It really is cute! Yes! See you!",'Distinct later delighted exclamation: unlike the earlier matching opening, this line ends with a cheer and farewell, not another request or offer. Do not collapse the two source records.'),
81:("Handed over the wristband of heavenly protection/favor.",'Original FE system notice reports handing over 天佑のリストバンド. This is the outgoing wristband, not receipt of it or of the bow. Exact established item wording and original FE consumer remain to be reviewed.'),
}
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);assert packet['source_only_no_current_English_exposed_orused'] and not packet['inventory_failures'];group=deepcopy(packet['groups'][0]);assert group['block']==49 and len(group['records'])==14 and group['completed_coverage_overlap']==0
    for row in group['records']:
        gloss,note=GLOSSES[row['source_record_index']];assert row['source_Japanese'] is not None and row['current_English_body_unread']
        row.update(first_clean_source_gloss=gloss,source_context_note=note,whole_source_exchange_andboth_prose_outcome_sequences_read=True,current_English_dialogue_still_unconsulted=True,localization_native_controls_names_items_formatting_actual_andregistered_integration_pending=True)
    choice=next(c for c in group['commands'] if c['word']==0x2100);raw=bytes.fromhex(group['clean_block_hex']);assert raw[580:590].decode('cp932')=='いいだろう' and raw[592:598].decode('cp932')=='だめだ'
    choices=[dict(source_reference=dict(block=49,command_offset=574,offset=580,bytes=10),source_Japanese='いいだろう',first_clean_source_gloss='All right. / Fine.',source_hex=raw[580:590].hex()),dict(source_reference=dict(block=49,command_offset=574,offset=592,bytes=6),source_Japanese='だめだ',first_clean_source_gloss='No. / I refuse.',source_hex=raw[592:598].hex())]
    ROOT.mkdir(parents=True);save(ROOT/'fourteen_first_clean_glosses_two_choice_labels_wristband_trade_direction_andqualified_Hodram_reply.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),groups=[group],source_typed_choice=dict(command=choice,labels=choices,complete_native_choice_layout_andselection_control_flow_not_yet_verified=True),all14_clean_utterances_andtwo_choices_glossed_before_current_English=True,source_event49_explicitly_requires48_but_outer_eligibility_activation_location_orfull_chronology_not_proven=True,source_title_phonetic_Lil_speech_andformal_FE_notice_bound_separately=True,no_current_English_comparison_localized_revision_name_item_approval_orcompletion_credit=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,producer_sha256=sha(Path(__file__).read_bytes())))
    print('Clean-first B49:14utterances/two choice labels glossed;trade direction,hearsay,conditional offer,Hodram silence/qualified reply anddistinct repeated delight preserved.Current English still unread;no completion credit.')
