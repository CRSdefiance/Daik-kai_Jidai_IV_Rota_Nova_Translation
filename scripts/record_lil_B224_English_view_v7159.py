"""Record all viewed English pages, two names and exact observed equality limits."""
from copy import deepcopy
from pathlib import Path
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B224_English_view_v7159');ACTUAL=Path('work/analysis/lil_B224_English_actual_v7157/all15_English_speeches_complete_native_masks27_commands_C200_source_comparison.json');LATER=Path('work/analysis/lil_B224_later_v7158/following_final_components_and_measured_timing_RNG_RGB_limits.json')
OLD_NAMES=Path('translations/lil_B224_speaker_name_review_v1.json');NEW_NAMES=Path('translations/lil_B224_speaker_name_review_v2.json')
if __name__=='__main__':
    assert not ROOT.exists() and not NEW_NAMES.exists();a,l=map(read,[ACTUAL,LATER]);assert l['actual_proof_sha256']==sha(ACTUAL.read_bytes())
    assert a['actual_unique_speeches']==15 and a['actual_complete_body_holds']==a['actual_complete_name_holds']==59 and a['incomplete_sampled_body_holds']==0 and len(a['actual_panels'])==15
    assert len(a['command_pairs'])==27 and not a['command_comparison_differences'] and a['source_English_all_measured_command_results_UI_timing_RNG_equal'] and a['source_English_command_results_and_UI_equal']
    assert a['source_exit_frame']==a['exit_frame']==6455 and a['normal_port_sample_frame']==6550 and a['normal_terminal_result']==[0,0] and a['original_C200_source_offset952_target1034_observed']
    assert len(a['semantic_upper_portrait_pairs'])==15 and all(r['upper_scene_RGB_equal'] and r['portrait_RGB_equal'] for r in a['semantic_upper_portrait_pairs'])
    assert len(a['later_sampled_whole_frame_comparisons'])==159 and a['all_sampled_later_whole_frame_RGB_equal'] and all(l['five_native_component_equality'].values()) and l['whole_actor_and_captain_equal'] and l['captain_IDs']==[2,2] and l['final_PRNG_seeds']==[3169181745,3169181745]
    assert [r['B120_end_frames'] for r in l['following_B120']]==[[11256],[11256]] and not a['unreturned_following_dialogues_at_capture_end'] and a['retained_R11_complete_original_CP932_ink_lighter_gray_and_whole_body_RGB_verified']
    sheets=a['review_sheets']+[a['transition_sheet']];assert len(sheets)==4
    for s in sheets:assert sha(Path(s['path']).read_bytes())==s['sha256']
    for i,panel in enumerate(a['actual_panels']):
        photo=panel['selected_capture'];sheet=Image.open(a['review_sheets'][i//6]['path']).convert('RGB');x,y=i%3*520+4,(i%6)//3*416+24;expected=Image.open(photo['capture']).convert('RGB').crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST);assert sheet.crop((x,y,x+512,y+384)).tobytes()==expected.tobytes()
    ellipsis=next(p for p in a['actual_panels'] if p['id']=='DK4_MES_B224_R0011');assert ellipsis['body_shadow_RGB']==[197,198,197] and len(ellipsis['complete_body_holds'])==4 and all(h['retained_R11_full_body_RGB_equals_original'] for h in ellipsis['complete_body_holds'])
    assert all(p['body_shadow_RGB']==[98,97,98] for p in a['actual_panels'] if p['id']!=ellipsis['id'])
    names=deepcopy(read(OLD_NAMES))
    for r in names['records']:
        panels=[p for p in a['actual_panels'] if p['source_selector']==r['actor_ID']];assert panels
        r.update(actual_English_header_to_recheck=False,actual_English_header_observed=True,actual_English_complete_header_holds=sum(len(p['complete_name_holds']) for p in panels));r['formatting_reason']+=' Complete actual English headers andblank guards also match on every observed held page.'
    names.update(previous_review=str(OLD_NAMES),previous_review_sha256=sha(OLD_NAMES.read_bytes()),actual_English_proof=str(ACTUAL),actual_English_proof_sha256=sha(ACTUAL.read_bytes()),both_actual_English_names_complete=True,new_name_or_dialogue_credit=0,full_goal_complete=False)
    ROOT.mkdir(parents=True);save(NEW_NAMES,names)
    save(ROOT/'all15_English_pages59_body59_headers_original_ellipsis_and_scope_viewed.json',dict(actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),later_scope=str(LATER),later_scope_sha256=sha(LATER.read_bytes()),viewed_sheets=sheets,all_four_English_sheets_individually_returned_and_viewed=True,all15_English_sheet_panes_pixel_equal_saved_whole_frame_crops=True,all15_pages59_body59_name_holds_complete=True,fuller_openings27_and29_cells_viewed=True,original_ellipsis_all4_actual_black_lighter_gray_and_full_RGB_holds_match_source=True,other14_English_paragraphs_keep_original_dark_gray_masks=True,all27_observed_commands_results_UI_timing_RNG_and_durations_equal=True,all15_semantic_scene_portrait_pairs_equal=True,both_normal_returns0_0_at6455_andAmsterdam6550=True,both_following_SC2_B120_ends11256_and_final_Sea_View_viewed=True,all159_later_sampled_whole_frame_RGBs_and_five_queried_components_equal=True,final_captain_IDs=[2,2],final_PRNG_seeds=[3169181745,3169181745],no_full_RAM_every_frame_future_sequence_broad_simulation_or_complete_causal_claim=True,source_event224_no_explicit_dependency_not_natural_activation_or_original_location=True,initialized_fixture_and_inherited_scope_not_earned_progress_or_hardware=True,speaker_name_review=str(NEW_NAMES),speaker_name_review_sha256=sha(NEW_NAMES.read_bytes()),full_catalogue_UI_and_full207_name_review_open=True,all_failed_probes_and_measured_limits_retained_for_later_technical_reaudit=True,visual_review_pending=False,registered_integration_and_current_startup_pending=True,new_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Viewed15 English pages/59 body59 headers;original ellipsis palette+RGB andall fifteen matched scenes pass. Observed27 commands/159 later samples/five components agree within scope;no broad equivalence orcredit.')
