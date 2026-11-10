"""Prepare exact-frame source/English scene and subsequent sailing comparisons."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B200_screen_review_v5864')
ACTUAL=Path('work/analysis/lil_B200_actual_v5861/nineteen_actual_panels_source_matched_controls_and_complete_native_holds.json')
STATE=Path('work/analysis/lil_B200_timing_state_v5862/measured_command_durations_screen_bounds_and_native_final_components.json')
PIXELS=Path('work/analysis/lil_B200_postscene_difference_v5863/unmodified_final_difference_pixel_inventory.json')
if __name__=='__main__':
    assert not ROOT.exists();actual,state,pixels=map(read,[ACTUAL,STATE,PIXELS])
    assert not actual['failures'] and not actual['paired_region_differences']
    assert actual['complete_matching_observations']==19 and actual['complete_matching_holds']==73
    assert state['actual_proof_sha256']==sha(ACTUAL.read_bytes()) and all(state['native_final_component_equality'].values())
    assert state['all_duration_changes_are_speeches'] and len(state['actual_command_duration_changes'])==8
    assert [r['duration_delta'] for r in state['actual_command_duration_changes']]==[-1,4,-1,-1,-4,5,-4,3]
    assert state['shifted_start_or_return_pairs']==19 and state['source_and_English_return_frames']==[7676,7677]
    prompt=[];sky=[]
    for row in actual['later_whole_RGB_differences']:
        if row['nontext_region_difference_bbox'] is None:
            assert row['difference_bbox'][0:3:2]==[224,240] and row['difference_bbox'][1]==360 and row['difference_bbox'][3]<=376;prompt.append(row)
        else:
            assert row['difference_bbox']==row['nontext_region_difference_bbox']==[137,192,191,243] and row['frame']>=12490;sky.append(row)
    assert len(prompt)==6 and len(sky)==10 and len(actual['all_sampled_frame_comparisons'])==182
    assert sum(r['nontext_region_difference_bbox'] is None for r in actual['all_sampled_frame_comparisons'])==172
    assert pixels['difference_bbox']==[137,192,191,243] and len(pixels['difference_pixels'])==1037
    reports=[read(v['capture_report']) for v in actual['versions']];photos=[{p['frame']:p for p in r['frames_captured']} for r in reports]
    holds={r['id']:r['holds'] for r in actual['actual_panels']};indices=[5,17,21,33,54,58,62,65,72]
    frames=[holds[f'DK4_MES_B200_R{i:04d}'][-1]['frame'] for i in indices]+[8410,12490,13001];assert len(set(frames))==12
    ROOT.mkdir(parents=True);sheets=[]
    for start in range(0,len(frames),2):
        selected=frames[start:start+2];sheet=Image.new('RGB',(1048,1600),'#263238');draw=ImageDraw.Draw(sheet)
        for row,frame in enumerate(selected):
            for col,(label,items) in enumerate(zip(['clean_Japanese','reviewed_English'],photos,strict=True)):
                p=items[frame];assert sha(Path(p['path']).read_bytes())==p['PNG_sha256'];im=Image.open(p['path']).convert('RGB');x,y=col*524,row*800
                draw.text((x+4,y+3),label+' / frame '+str(frame),fill='white');sheet.paste(im.resize((512,768),Image.Resampling.NEAREST),(x+4,y+24))
        path=ROOT/f'paired_full_screen_sheet{start//2+1}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),frames=selected))
    save(ROOT/'paired_scene_return_and_measured_sailing_difference_sheets.json',dict(actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),
        actual_consumer_sheets=actual['review_sheets'],paired_full_screen_sheets=sheets,visual_review_pending=True,
        all19_complete_native_planes_and73_source_region_holds_match=True,complete_matching_holds=73,
        sampled_nontext_frames=182,nontext_equal_samples=172,following_sailing_sky_difference_samples=10,
        all_changed_scene_held_portrait_name_picture_regions_exact=True,following_sailing_sky_differences_not_masked_or_removed=True,
        source_and_English_return_frames=[7676,7677],command_start_return_difference_count=19,actual_speech_duration_changes=state['actual_command_duration_changes'],
        all_nonspeech_command_durations_results_and_shapes_equal=True,later_whole_RGB_difference_count=16,
        advance_prompt_region_differences=prompt,following_sailing_sky_region_differences=sky,
        original_full_final_screens_and_unmodified_crop_viewed_before_classification=True,
        final_difference_pixels=1037,final_difference_bbox=[137,192,191,243],
        no_native_cloud_object_or_complete_timing_cause_claim=True,
        exact_timing_and_native_state_proof=str(STATE),exact_timing_and_native_state_proof_sha256=sha(STATE.read_bytes()),
        all_queried_native_final_components_equal=True,final_13001_PRNG_seeds=state['final_13001_PRNG_seeds'],final_13001_PRNG_equal=False,
        no_broad_world_effect_full_RAM_or_future_simulation_equivalence_claim=True,
        source_name_portrait_item_and_background_visibility_preserved_during_changed_scene=True,Stranger_target_not_applied=True,
        no_natural_event200_activation_original_location_exhaustive_condition_visits_or_hardware_claim=True,
        actual_source_English_cold_boots=2,total_successful_frames=26002,new_English_runs=1,
        original_source_run_reused_and_not_recounted_as_new=True,offline_only_source_indices=[],
        evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,STATE,PIXELS,Path(__file__)]},new_review_credit=0,full_goal_complete=False))
    print('Six paired sheets prepared:19 panels/73 complete holds,172/182 nontext samples exact;ten subsequent sky samples and six prompt samples differ. Native state groups equal;PRNG differs.')
