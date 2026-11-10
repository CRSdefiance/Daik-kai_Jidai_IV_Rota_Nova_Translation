"""Complete B50 first clean-source glosses; no localized manuscript, mechanic inference or credit."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B50_clean_gloss_v8131')
SOURCE=Path('work/analysis/Rafael_next_clean_v8129/complete_clean_SC0_B50_EV0_andcoverage_before_current_English.json')
NAMES=Path('work/analysis/Rafael_B50_clean_names_v8130/three_clean_static_identity_fields_before_current_English.json')
GLOSSES={
 6:'Lil calls for the other person to wait.',
 10:'Rafael recognizes the caller and hesitantly checks whether her name was Lil. The familiar source honorific does not establish a new rank or relationship.',
 14:'Lil sounds impressed that he remembered her, then dismisses that subject and admits that in the end he outmaneuvered her/them. Preserve her competitive attitude; betrayal is not stated.',
 18:'Rafael responds with an awkward or polite thanks/acknowledgment, without demonstrating that he understands her point.',
 23:'Lil rejects that bland response and offers him the key to deciphering the map that records the treasure location. This states a map-deciphering aid, not a new map or the treasure itself; bind the exact item/effect before choosing a proper item name.',
 27:'Rafael exclaims in surprise and asks whether she is really willing to give it to him.',
 31:'Lil sighs in disbelief that she lost to someone like this, then lets the matter go. Preserve the exasperated competitive humor.',
 37:'Camille finally finds Lil here and says that the preparations are still not all finished. The purpose of the preparations is not named in this line.',
 40:'Camille greets Rafael and politely checks the FA identity substitution. Preserve FA until its exact native getter and target are verified; do not assume it is FI or substitute a fixed name.',
 44:'Rafael hesitantly confirms and checks whether Camille is the correct name. Use approved Camille later without inventing family or gender facts.',
 49:'Camille confirms and jokes awkwardly that perhaps this counts as a long-time-no-see greeting. This acknowledges a prior meeting but does not date or identify it mechanically.',
 53:'Camille turns to Lil and worries that she may be acting rudely again. The question is apprehensive, not an accusation of a new witnessed offense.',
 57:'Lil answers with drawn-out, playfully innocent agreement and says that she only handed over that pigment because she will no longer use it. Preserve the pigment and her affected casual tone; the exact item name and reason remain context questions.',
 61:'Camille realizes that FA is now the North Sea hegemon/dominant leader, addresses the source head-of-force title, and accepts the handover on that basis. Bind title and FA consumers before natural English; do not add conquest of another region or claim that event eligibility has been proved.',
 65:'Rafael is puzzled and asks whether something has happened.',
 69:'Lil starts to remark that he is as slow on the uptake as ever, catches herself, and switches to an ostentatiously polite comment about how easygoing he is. Preserve the self-correction and comic evasiveness.',
 73:'Lil tentatively says that she too seems to have found a way of living other than making money. Do not specify marriage, romance, pregnancy, retirement or a new occupation without further source evidence.',
 77:'Rafael gives a mild acknowledgment that sounds as though he understands.',
 82:'Lil asks in surprise whether he has finally understood.',
 86:'Rafael privately admits that he does not understand at all but decides to play along, then outwardly says that this is good news. Keep the internal thought separate from his spoken response and preserve the dramatic irony.',
 91:'Lil thanks him warmly.',
 95:'Camille also thanks him politely. The source does not name the occasion being thanked for.',
 99:'Lil then asks whether there is no congratulatory gesture or present. The occasion remains unnamed; do not fill it in with a wedding or other invented life event.',
 103:'Rafael stammers in surprise and privately realizes he is in trouble because he does not know what they are talking about. Preserve the gap between his apparent agreement and lack of understanding.',
 108:'Camille politely tells him not to worry, calls Lil to leave, bids FI well under the source force-leader title, and takes leave. Preserve FI separately from the earlier FA tokens and do not invent a surname, rank or commitment.',
 111:'Lil agrees to go, then cheerfully asks him to work hard for their share as well. This passes encouragement/expectations onward without explicitly stating a permanent retirement or transfer of every possession.',
 114:'Rafael thanks Lil and Camille by name and promises to do his best to meet their expectations. This is a commitment to try, not a guaranteed future outcome.',
 119:'Rafael privately wonders what that requested celebration/congratulatory present had been for. Preserve the unresolved joke rather than explaining the occasion to the player.',
}
if __name__=='__main__':
    assert not ROOT.exists();source,names=map(read,[SOURCE,NAMES]);g=source['groups'][0]
    assert len(g['records'])==len(GLOSSES)==28 and {r['source_record_index'] for r in g['records']}==set(GLOSSES)
    assert len(names['records'])==3 and not g['completed_coverage_overlap'] and not source['inventory_failures']
    assert len(g['commands'])==37 and len(g['source_event_records'])==1 and g['source_event_records'][0]['event_ID']==50
    assert not g['source_event_records'][0]['must_be_completed'] and not g['source_event_records'][0]['must_not_be_completed']
    rows=[]
    for i,r in enumerate(g['records']):
        rows.append(dict(**r,first_clean_source_gloss=GLOSSES[r['source_record_index']],
            previous_physical_source_ID=None if i==0 else g['records'][i-1]['id'],next_physical_source_ID=None if i+1==len(g['records']) else g['records'][i+1]['id'],
            physical_neighbors_not_yet_claimed_actual_execution=True,current_B50_English_body_still_unread=True))
    macro_counts={m:sum(r['source_Japanese'].count(m) for r in g['records']) for m in ['FI','FA','FO']};assert macro_counts==dict(FI=1,FA=2,FO=0)
    ROOT.mkdir(parents=True);save(ROOT/'28_first_clean_glosses_three_source_identities_before_current_English.json',dict(
        source_packet=str(SOURCE),source_packet_sha256=sha(SOURCE.read_bytes()),clean_names=str(NAMES),clean_names_sha256=sha(NAMES.read_bytes()),records=rows,
        source_event_records=g['source_event_records'],source_event_anddependencies=g['source_event_anddependencies'],
        source_actors={str(r['source_actor_ID']):[v.get('text') for v in r['fields']] for r in names['records']},source_macro_counts=macro_counts,
        complete_exchange_progression='Lil concedes being outmaneuvered and offers a map-deciphering key; Camille arrives while preparations are unfinished; pigment handover and North Sea leadership acknowledged; unnamed change in life and congratulatory gesture lead to thanks and a farewell; Rafael plays along while privately never understanding the occasion.',
        no_marriage_romance_pregnancy_kinship_retirement_newrank_oroccasion_invented=True,
        final_private_question_must_remain_unresolved_without_additional_source_evidence=True,
        source_EV50_category5_action51_no_explicit_prerequisite_exclusion_not_proof_ofnatural_activation=True,
        numeric_B49_B50_adjacency_not_proof_ofchronology_orprerequisite=True,
        native_FA_FI_getters_fullpreambles_controls_item_effects_callers_mechanics_andactual_context_pending=True,
        B49_names_previously_reviewed_approved_Camille_retained_no_fresh_current_B50_name_orbody_comparison=True,
        source_only_no_current_B50_English_exposed_no_localized_manuscript=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,NAMES,Path(__file__)]}))
    print('B50:28 complete first clean glosses/three clean identities;FA2/FI1. Occasion remains deliberately unnamed. Controls/item effects/title/getters/context/current comparison pending;zero credit.')
