"""Reconcile the full clean exchange with the observed unforced source scene."""
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B198_context_v5715')
SOURCE=Path('work/analysis/lil_B198_source_v5702/all17_clean_current_complete_context.json')
ACTUAL=Path('work/analysis/lil_B198_source_paths_v5714/one_actual_source_path_and_complete_command_intervals.json')
NAMES=Path('work/analysis/lil_B198_source_names_v5711/two_actors_all_clean_fields_and_current_consumers.json')
CONTROLS=Path('work/analysis/lil_B198_controls_v5710c/twelve_exact_leaves_two_predicates_resource_picture_seven_structural_pairs_and_end.json')
PROGRESSION=("An unattributed rough voice repeats the Namahage bad-children refrain twice in each of two calls. "
    "It directly asks Yukihisa whether he is bad three times, ignoring his challenge and recognition of Namahage. "
    "Yukihisa calmly says he does not recall doing wrong; the voice acknowledges this. A pause and changed "
    "backdrop lead to his realization that it was a dream. Angelo's conditional startled question, if selected, "
    "precedes Yukihisa's shared reaction and silence. A displayed object accompanies his composed reflection "
    "that strange things happen and his intention to give this to the Admiral, perhaps tomorrow morning. "
    "Angelo's second conditional line resumes his unanswered question. No narrator confirms a supernatural cause.")
if __name__=='__main__':
    assert not ROOT.exists()
    packet,actual,names,controls=map(read,[SOURCE,ACTUAL,NAMES,CONTROLS])
    gp=Path(packet['whole_exchange_context_notes']);gloss=read(gp)
    assert gloss['read_no_predecessor_English'] and len(gloss['records'])==17
    assert actual['selected_source_speech_indices']==[10,14,18,22,26,30,34,38,42,49,53,72,76,80,84]
    assert actual['unvisited_source_indices']==[65,95] and actual['source_end540_return_frame']==6697
    assert [(r['source_offset'],r['native_result']) for r in actual['source_predicate_observations']]==[(306,[2,0]),(480,[2,0])]
    sheets=actual['review_sheets']+actual['transition_sheets'];assert len(sheets)==5
    for r in sheets:
        assert sha(Path(r['path']).read_bytes())==r['sha256']
        r.update(viewed_in_full_current_turn=True,original_detail=True)
    rows=deepcopy(gloss['records'])
    for r in rows:
        r['actual_source_fixture_observed']=r['source_record_index'] in actual['selected_source_speech_indices']
        r['actual_source_paths']=['unforced_initial_roster'] if r['actual_source_fixture_observed'] else []
        if r['source_record_index'] in [65,95]:
            r['whole_exchange_note']+=' Both original predicates returned zero in the unforced initial-roster source fixture, omitting these two Angelo reactions. Their complete Japanese clauses and nesting remain reviewed offline; do not claim actual captures or change the condition to make them appear.'
        if r['source_record_index']==53:
            r['whole_exchange_note']+=' The source scene changes from a black upper screen to a coastal/mountain backdrop before this explicit dream realization. No spoken scene name or narrator-confirmed supernatural explanation is added.'
        if r['source_record_index'] in [72,76,80,84]:
            r['whole_exchange_note']+=' The existing UI displays Namahage Cleaver / Weapon / dash. This supports the deictic object context but is not new title/widget fidelity credit and does not license naming it in otherwise unnamed speech.'
    ROOT.mkdir(parents=True)
    save(ROOT/'clean_first_context_Namahage_dream_and_original_unforced_path.json',dict(
        source_context=str(SOURCE),source_context_sha256=sha(SOURCE.read_bytes()),historical_clean_gloss=str(gp),
        historical_clean_gloss_sha256=sha(gp.read_bytes()),corrected_contextual_gloss_records=rows,
        complete_exchange_progression=PROGRESSION,approved_prose_names={'12':'Yukihisa Shiraki','15':'Angelo Puccini'},
        source_clean_names=names['source_name_records'],source_actual_paths=str(ACTUAL),source_actual_paths_sha256=sha(ACTUAL.read_bytes()),
        actual_original_source_cold_boots=1,actual_source_frames=13001,actual_source_distinct_speeches=15,
        offline_only_conditional_source_indices=[65,95],source_15_speeches_and_dream_transition_viewed=True,
        viewed_source_sheets=sheets,source_end540_returns_normally_at6697=True,
        source_FE_is_unattributed_speaking_voice_not_impersonal_notice=True,
        source_four_chant_occurrences_and_three_direct_questions_preserved=True,
        cultural_reference_checks=gloss['cultural_reference_checks'],external_references_not_game_facts=True,
        source_dream_explicit_but_no_confirmed_Namahage_identity_cause_or_item_powers=True,
        source_item_card_observed_text=['Namahage Cleaver','Weapon','—'],spoken_this_remains_unnamed=True,
        tomorrow_morning_Admiral_handover_remains_prospective_not_completed=True,
        source_predicate_results_zero_for_both_sites_not_full_roster_membership_semantics_proof=True,
        both_conditional_Angelo_questions_need_shared_context_valid_without_first_question=True,
        source_blank_FE_portrait_name_and_source_controlled_progressive_visibility_preserved=True,
        no_added_age_kinship_rank_marriage_room_sharing_ritual_date_or_scene_location=True,
        source_initialized_B22_fixture_not_natural_event198_activation_original_location_full_route_or_hardware=True,
        all_clean_first_glosses_and_original_actual_context_precede_predecessor_speech_comparison=True,
        source_effect_and_resource_bodies_not_fully_executed_offline=True,
        evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,gp,ACTUAL,NAMES,CONTROLS,Path(__file__)]},
        new_ROMs=0,new_emulator_runs=0,new_editorial_credit=0,full_goal_complete=False))
    print('B198 reconciled:15 observed/2 offline-only source speeches;Namahage refrain,dream and deictic object context preserved. Five source sheets viewed. No prior-English comparison or credit.')
