"""Prepare exact-frame whole-screen pairs for distinct B199 displays and normal return."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B199_screen_review_v5808')
ACTUAL=Path('work/analysis/lil_B199_actual_v5807/thirty_one_actual_panels_source_matched_controls_and_complete_native_holds.json')
STATE=Path('work/analysis/lil_B199_timing_state_v5808b/six_speech_duration_changes_34_shifted_pairs_prompt_bounds_and_native_state.json')
if __name__=='__main__':
    assert not ROOT.exists();actual=read(ACTUAL)
    assert not actual['failures'] and not actual['paired_region_differences']
    assert actual['complete_matching_observations']==31 and actual['complete_matching_holds']>=31
    state=read(STATE)
    assert state['actual_proof_sha256']==sha(ACTUAL.read_bytes())
    assert all(state['native_final_component_equality'].values())
    assert len(actual['actual_timing_differences'])==34 and len(actual['later_whole_RGB_differences'])==6
    assert all(r['nontext_region_difference_bbox'] is None for r in actual['all_sampled_frame_comparisons'])
    reports=[read(v['capture_report']) for v in actual['versions']]
    photos=[{p['frame']:p for p in r['frames_captured']} for r in reports]
    holds={r['id']:r['holds'] for r in actual['actual_panels']}
    indices=[5,9,34,37,54,70,88,95,115]
    frames=[holds[f'DK4_MES_B199_R{i:04d}'][-1]['frame'] for i in indices]
    frames.extend([max(photos[0]),11530,12130]);assert len(set(frames))==12
    ROOT.mkdir(parents=True);sheets=[]
    for start in range(0,len(frames),2):
        selected=frames[start:start+2];sheet=Image.new('RGB',(1048,1600),'#263238');draw=ImageDraw.Draw(sheet)
        for row,frame in enumerate(selected):
            for col,(label,items) in enumerate(zip(['clean_Japanese','reviewed_English'],photos,strict=True)):
                p=items[frame];assert sha(Path(p['path']).read_bytes())==p['PNG_sha256']
                im=Image.open(p['path']).convert('RGB');x,y=col*524,row*800
                draw.text((x+4,y+3),label+' / frame '+str(frame),fill='white')
                sheet.paste(im.resize((512,768),Image.Resampling.NEAREST),(x+4,y+24))
        path=ROOT/f'paired_full_screen_sheet{start//2+1}.png';sheet.save(path)
        sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),frames=selected))
    snapshots=[r['read_only_RAM_snapshot'] for r in reports];seeds=[]
    for r in snapshots:
        data=Path(r['path']).read_bytes();assert r['read_only_export'] and len(data)==4194304 and sha(data)==r['sha256']
        seeds.append(int.from_bytes(data[0x168EB8:0x168EBC],'little'))
    save(ROOT/'paired_scene_and_return_sheets_with_measured_limits.json',dict(actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),
        actual_consumer_sheets=actual['review_sheets'],paired_full_screen_sheets=sheets,visual_review_pending=True,
        all31_complete_native_planes_and_source_regions_match=True,complete_matching_holds=actual['complete_matching_holds'],
        sampled_nontext_frames=len(actual['all_sampled_frame_comparisons']),all_sampled_nontext_regions_equal=True,
        source_and_English_return_frames=[v['fixture_exit_frame'] for v in actual['versions']],
        command_timing_difference_count=34,later_sampled_whole_RGB_difference_count=6,
        six_speech_duration_changes_and_other_control_durations_equal=state['six_actual_speech_duration_changes'],
        exact_timing_and_native_state_proof=str(STATE),exact_timing_and_native_state_proof_sha256=sha(STATE.read_bytes()),
        all_queried_native_final_components_equal=True,
        final_13001_PRNG_seeds=seeds,final_13001_PRNG_equal=seeds[0]==seeds[1],exported_snapshots=snapshots,
        no_broad_world_effect_full_RAM_or_future_simulation_equivalence_claim=True,
        source_name_portrait_item_and_background_visibility_preserved_without_normalization=True,
        no_natural_event199_activation_original_location_exhaustive_condition_visits_or_hardware_claim=True,
        actual_source_English_cold_boots=2,total_successful_frames=26002,new_English_runs=1,
        original_source_run_reused_and_not_recounted_as_new=True,offline_only_source_indices=[],
        evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,STATE,Path(__file__)]},new_review_credit=0,full_goal_complete=False))
    print(dict(paired_sheets=6,nontext_frames=len(actual['all_sampled_frame_comparisons']),holds=actual['complete_matching_holds'],
        returns=[v['fixture_exit_frame'] for v in actual['versions']],PRNG_seeds=seeds))
