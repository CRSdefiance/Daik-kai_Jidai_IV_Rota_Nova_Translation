"""Read the complete clean B51 warning/reaction exchange before any current English exposure."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/Hodram_B51_clean_gloss_v8549')
SOURCE=Path('work/analysis/Hodram_B51_clean_v8548/complete_clean_SC1_B51_EV1_andcoverage_before_current_English.json')
GLOSSES={
 'DK4_MES_B51_R0006':(
    "The gruff speaker does not know what the addressee intends to do in this southern Mediterranean area,but offers a warning:the addressee would be better off leaving.",
    "Keep the explicit South Mediterranean setting,the speaker's stated lack ofknowledge ofthe party's plans,andthe colloquial warning/advice. Do not turn it into an expulsion froma town orbuilding,an order froman authority,orproof ofa specific enemy,quest,trade restriction orreligious affiliation."),
 'DK4_MES_B51_R0010':(
    "A restrained,puzzled question:...What do you mean? / What isthat supposed to mean?",
    "The reply seeks an explanation ofthe preceding warning. Preserve the questioning beat without inventing hostility,recognition,an accusation ora known identity."),
 'DK4_MES_B51_R0014':(
    "There is someone truly alarming orformidable here. The speaker insists the advice isfor the addressee's own good:heading toanother sea area would be wiser forself-preservation.",
    "悪いことは言わねえ is an idiomatic assurance thatthe warning iswell meant,not a claim aboutnever lying ornot doing evil. 身のため gives the safety/self-interest motive. The unnamed ヤツ isnot identified here;do not add a name,rank,nationality,gender claim,kinship,political role,crime,battle outcome orguaranteed safety."),
 'DK4_MES_B51_R0032':(
    "An echoing,hesitant question aboutthe warning's description:...Someone that alarming/formidable?",
    "Keep it as a questioning repetition ratherthan confirmation ofthe unnamed person's identity orstrength. This speech isinside the original0100 scope at258;native condition/query outcomes must be mapped before assigning it toan actual path."),
 'DK4_MES_B51_R0039':(
    "A parenthesized,private flash ofstartled disbelief orpossibility:...Could it be!? / ...No way!? No person isexplicitly named orconfirmed.",
    "Preserve the inward,alarmed reaction andits unresolved implication. Do not state whomthe speaker suspects,assert a relationship orpast encounter,orreplace the thought witha spoken explanation. Native branch membership andspeaker/name consumers remain tobe bound."),
}
if __name__=='__main__':
    assert not ROOT.exists();packet=read(SOURCE);assert packet['source_only_no_current_English_exposed_orused'] and not packet['inventory_failures']
    assert len(packet['groups'])==1;group=deepcopy(packet['groups'][0]);rows=group['records']
    assert list(GLOSSES)==[r['id'] for r in rows] and [r['source_selector'] for r in rows]==[113,1,113,18,16]
    assert all(r['current_English_body_unread'] and not r['already_contextually_completed'] and r['source_decode_error'] is None for r in rows)
    assert len(group['commands'])==20 and group['clean_stored_bytes']==group['clean_logical_end']==340 and group['clean_tail_bytes']==0
    assert rows[3]['source_0100_ancestors']==[258] and all(not rows[i]['source_0100_ancestors'] for i in [0,1,2,4])
    for row in rows:
        raw=bytes.fromhex(row['source_hex']);assert raw[1:].decode('cp932')==row['source_Japanese']
        gloss,note=GLOSSES[row['id']]
        row.update(first_clean_source_gloss=gloss,source_context_note=note,whole_clean_warning_andconditional_reactions_read=True,current_English_dialogue_still_unconsulted=True,source_meaning_only_not_localized_orformatting_approval=True,native_speakers_queries_branch_paths_names_current_editorial_actual_andregistered_integration_pending=True)
    event=group['source_event_records'];assert len(event)==1 and event[0]['event_ID']==51 and event[0]['action_index']==52 and event[0]['script_block']==51 and event[0]['must_be_completed']==event[0]['must_not_be_completed']==[]
    context="Three initial speeches form a gruff local warning,an explanatory question,andmore explicit advice toleave the southern Mediterranean becauseofan unnamed alarming person. Two later reactions addan echoing question andan inward startled possibility,subjectto the original native conditional flow. The script includes8100/8000 queries,two0200/0300 pairs andnested0100 scopes;do not flatten allfive speeches intoone observed path orinterpret packed control operands as names. Resolve the full source presentation preambles andselectors71/01/12/10 through native consumers before assigning names/roles. Event51 hasno listed prerequisite/exclusion,but other native conditions/outer scheduling areunexecuted. Numeric adjacency toB50 doesnot establish chronology orconnect this warning tothe wristband/bow exchange."
    ROOT.mkdir(parents=True);save(ROOT/'five_first_clean_glosses_warning_andconditional_reactions.json',dict(source=str(SOURCE),source_sha256=sha(SOURCE.read_bytes()),source_ROM=packet['source_ROM'],source_ROM_sha256=packet['source_ROM_sha256'],source_verified_handoff=packet['verified_handoff'],source_verified_handoff_sha256=packet['verified_handoff_sha256'],groups=[group],whole_exchange_context=context,all5_clean_utterances_glossed_before_current_English=True,current_English_dialogue_bodies_still_unconsulted=True,explicit_source_region_andidiomatic_well_meant_warning_preserved=True,unnamed_person_identity_andreaction_not_invented_orconfirmed=True,all_source_references_full_preambles_commands_queries_branches_opaque_effects_terminal_andtail_preserved=True,source_speaker_names_query_semantics_branch_outcomes_andactual_activation_unproven=True,no_prose_orformatting_approval_no_ROM_orcounter_credit=True,B50_registered_build_patch_startup_andonceonly_credit_remain_separate=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,Path(__file__)]}))
    print('B51five clean-first glosses saved:SouthMediterranean warning/conditional echo/private alarm;20commands/queries/branches/end retained.CurrentEnglish stillunread;no names/paths invented,approval orcredit.')
