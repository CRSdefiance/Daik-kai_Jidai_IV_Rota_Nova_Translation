"""First source-only glosses for both treasure-race outcomes;current English remains unconsulted."""
from copy import deepcopy
from pathlib import Path
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/Hodram_B47_B48_clean_gloss_v8312')
PACKETS=[Path('work/analysis/Hodram_B47_clean_v8310/complete_clean_SC1_B47_EV1_andcoverage_before_current_English.json'),
    Path('work/analysis/Hodram_B48_clean_v8311/complete_clean_SC1_B48_EV1_andcoverage_before_current_English.json')]
PREVIOUS=Path('work/analysis/Hodram_B137_B45_B46_clean_gloss_v8183/28_first_clean_glosses_six_identities_explicit_prerequisite_graph_before_current_English.json')
GLOSSES={
 (47,6):'Lil exclaims in surprise that the other person has already found it and expresses drawn-out frustration. In the preceding B46 challenge,the object of finding first is the treasure,not winning a duel. Preserve the competitive frustration without inventing cheating,unfairness ornew insults.',
 (47,10):'Lil admits that she has lost,then shrugs it off ordecides it is all right. Keep the rueful pause andher resilient change of mood;do not turn this into a completed alliance,romance,apology ornewgift.',
 (47,13):'Because the other person beat her,Lil insists that they must not lose to anyone else andmust become numberone in the world. Preserve her forceful,competitive encouragement;this is a demand oraspiration,not a report that the player is already worldnumberone,nor an explicit order to conquer the world.',
 (48,6):'The system reports that Lil Argot appears to have discovered the named artifact 狩猟神ウルの弓矢. Preserve the apparent/reporting qualification andthe complete source artifact identity. Its established English item label must be resolved separately before localization;do not invent player acquisition orownership.',
 (48,11):'Lil chuckles andteases the runtime FI addressee that it is too bad for them. The musical note conveys playful orlilting delivery;it doesnot establish singing,romance orfamily ties. Preserve FI as a real runtime substitution,andlocalize さん through natural address ratherthan inventing a rank.',
 (48,14):'Lil says that if the addressee wants this,they should wait in Amsterdam. The instruction is forthe addressee towait there;do not reverse it into a statement that Lil isalready waiting there. Preserve the conditional desire anddestination,without claiming the artifact hasbeen handed over.',
}
if __name__=='__main__':
    assert not ROOT.exists();packets=list(map(read,PACKETS));previous=read(PREVIOUS);groups=[]
    assert len(previous['groups']) if 'groups' in previous else previous
    for packet in packets:
        assert packet['source_only_no_current_English_exposed_orused'] and not packet['inventory_failures']
        group=deepcopy(packet['groups'][0]);assert group['block'] in [47,48] and len(group['records'])==3 and group['completed_coverage_overlap']==0
        assert not any(c['word'] in [0x100,0x200,0x300,0x400,0x2100,0x4100] for c in group['commands'])
        for i,row in enumerate(group['records']):
            assert row['source_Japanese'] is not None and row['source_decode_error'] is None
            row.update(first_clean_source_gloss=GLOSSES[group['block'],row['source_record_index']],
                previous_physical_source_ID=group['records'][i-1]['id'] if i else None,next_physical_source_ID=group['records'][i+1]['id'] if i+1<len(group['records']) else None,
                source_literal_read=True,whole_three_utterance_outcome_read=True,current_English_dialogue_body_not_yet_consulted=True,
                native_control_identity_FE_geometry_FI_expansion_andactual_event_selection_not_yet_approved=True,
                source_prose_orcompletion_credit_added=False)
        groups.append(group)
    assert len(GLOSSES)==sum(len(g['records']) for g in groups)==6
    assert [r['source_selector'] for r in groups[0]['records']]==[2,2,2] and [r['source_selector'] for r in groups[1]['records']]==[254,2,2]
    assert sum(bytes.fromhex(r['source_hex'])[1:].count(b'FI') for g in groups for r in g['records'])==1
    ROOT.mkdir(parents=True);save(ROOT/'six_first_clean_glosses_both_race_outcomes_FE_FI_andAmsterdam_wait_direction.json',dict(groups=groups,
        complete_prior_B46_treasure_race_challenge_clean_context=str(PREVIOUS),complete_prior_context_sha256=sha(PREVIOUS.read_bytes()),
        all_six_clean_utterances_glossed_before_current_English=True,
        B47_explicit_event_excludes48_B48_no_exclusion_not_proof_of_outer_eligibility_orchronology=True,
        physical_TEXT_order_without_relative_scopes_not_all_effects_orordinary_scene_activation=True,
        source_FE_notice_one_FI_macro_one_musical_note_preserved_inraw_source=True,
        artifact_approved_English_name_andtwo_complete_source_identity_contexts_still_pending=True,
        no_current_English_translation_comparison_rewrite_formatting_orname_approval=True,
        all_six_source_positions_uncredited_until_required_review_andintegration=True,new_credit=0,new_emulator_runs=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for p in [*PACKETS,PREVIOUS,Path(__file__)]}))
    print('Six clean-first glosses:both complete race outcomes,Lil competitive voice/system FE/FI/♪/Amsterdam wait-direction;artifact label andnative context pending.No currentEnglish orcredit.')
