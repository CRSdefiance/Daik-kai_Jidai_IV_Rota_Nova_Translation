"""Record complete viewed source exchange,distinct FE/thought presentation and limited return."""
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B208_source_view_v6400')
ACTUAL=Path('work/analysis/lil_B208_source_actual_v6399/all24_source_panels_all38_commands_and_observed_return.json')
NAMES=Path('work/analysis/lil_B208_source_names_v6393/two_exact_source_name_fields_voices_and_distinct_name_consumers.json')
if __name__=='__main__':
    assert not ROOT.exists();a,n=read(ACTUAL),read(NAMES);assert a['source_distinct_speech_observations']==a['total_speech_observations']==24 and len(a['command_pairs'])==38 and not a['unvisited_source_indices'] and a['all_jobs_terminal_and_reaped'] and a['total_frames']==16001
    assert a['all29_source_commands_and9_original_initializers_observed'] and a['exit_frame']==8616 and a['source_effect_offsets_executed']==[1166,1174]
    assert [(r['source_record_index'],r['source_selector']) for r in a['speech_observations'][-2:]]==[(86,7),(90,254)]
    sheets=[*a['review_sheets'],*a['transition_sheets']];assert len(sheets)==5
    for s in sheets:assert sha(Path(s['path']).read_bytes())==s['sha256'];s.update(viewed=True,viewed_after_image_return=True)
    assert [r['catalogue'] for r in n['source_name_fields']]==['Cristina Erneco','Mysterious Old Man']
    ends=[r for r in a['following_native_commands'] if r['block']==120 and r['word']==0 and r['native_result'][0]==0];assert ends
    ROOT.mkdir(parents=True);save(ROOT/'all24_source_panels_names_thought_FE_notice_and_return_viewed.json',dict(actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),source_names=str(NAMES),source_names_sha256=sha(NAMES.read_bytes()),actual_source_speeches=24,actual_progressive_panels=23,actual_FE_panels=1,source_private_thought_index=86,source_named_FE_notice_index=90,viewed_sheets=sheets,visual_review_pending=False,all24_Japanese_panels_read_in_whole_exchange_context=True,source_face_vs_demeanor_correction_reported_pirate_history_uncertain_value_personal_intuition_and_limited_commitment_preserved=True,
        source_initializers_and_all29_original_commands_observed=True,source_exit_frame=8616,normal_town_return_viewed_at8710=True,following_B120_complete_end_observed=ends,final16001_sailing_screen_viewed=True,
        separate_source_private_thought_and_portraitless_FE_attribute_notice_viewed=True,
        current_screenshot_pair_names=[dict(actor_ID=7,current_catalog_name='Cristina Erneco',clean_fields=['クリスティナ','エルネコ'],contextual_retention_reason='Established source-faithful working proper name matches the two clean fields and four distinct getters. No familiar replacement surname or unsupported Latin-artwork/user-approval claim. The literal character-named notice must be reviewed individually for spelling consistency.'),dict(actor_ID=170,current_catalog_name='Mysterious Old Man',clean_fields=['謎の老人','国籍不明'],contextual_retention_reason='Natural generic role label preserves the source mystery and older male identity. The complete exchange gives no personal name,rank,nationality,kinship or profession. Unused Unknown nationality metadata is not expanded into his name. No change is justified merely because this is a descriptive label.')],
        two_name_contextual_retention_reasons_recorded_native_glyph_bounds_still_pending=True,current_names_are_English_in_Japanese_dialogue_fixture=True,
        all207_names_role_labels_aliases_and_other_consumers_review_remains_open=True,source_170_nationality_metadata_not_dialogue_name_or_biography=True,
        no_natural_event208_original_location_earned_progress_full_stat_inventory_quest_effects_routes_or_hardware_claim=True,
        no_actual_revised_English_scene_or_native_English_display_approval=True,new_source_cold_boot_runs=1,new_source_frames=16001,all_jobs_terminal_and_reaped=True,
        evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,NAMES,Path(__file__)]},new_name_dialogue_or_item_credit=0,full_goal_complete=False))
    print('Viewed24 complete source panels/five sheets:23 progressive incl thought,one FE notice;return8710,B120 end and final sailing16001. Contextual name retentions documented;English/native approval pending.')
