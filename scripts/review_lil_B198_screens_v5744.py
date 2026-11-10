"""Prepare paired full-screen source/English review with explicit capture and simulation scope."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B198_screen_review_v5744')
ACTUAL=Path('work/analysis/lil_B198_actual_v5743/fifteen_actual_panels_source_matched_controls_and_complete_native_holds.json')
if __name__=='__main__':
    assert not ROOT.exists()
    actual=read(ACTUAL)
    assert not actual['failures'] and not actual['paired_region_differences']
    assert actual['complete_matching_observations']==15 and actual['complete_matching_holds']==56
    assert not actual['actual_timing_differences'] and not actual['later_whole_RGB_differences']
    assert all(r['nontext_region_difference_bbox'] is None for r in actual['all_sampled_frame_comparisons'])
    reports=[read(v['capture_report']) for v in actual['versions']]
    photos=[{p['frame']:p for p in r['frames_captured']} for r in reports]
    holds={r['id']:r['holds'] for r in actual['actual_panels']}
    frames=[holds[f'DK4_MES_B198_R{i:04d}'][-1]['frame'] for i in [10,49,53,72,84]]
    frames.append(max(photos[0]));assert len(set(frames))==6
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
    snapshots=[r['read_only_RAM_snapshot'] for r in reports]
    seeds=[]
    for r in snapshots:
        data=Path(r['path']).read_bytes();assert r['read_only_export'] and len(data)==4194304 and sha(data)==r['sha256']
        seeds.append(int.from_bytes(data[0x168EB8:0x168EBC],'little'))
    save(ROOT/'paired_scene_and_return_sheets_with_measured_limits.json',dict(actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),
        actual_consumer_sheets=actual['review_sheets'],paired_full_screen_sheets=sheets,visual_review_pending=True,
        all15_complete_native_planes56_holds_and_source_regions_match=True,
        sampled_nontext_frames=len(actual['all_sampled_frame_comparisons']),all_sampled_nontext_regions_equal=True,
        source_and_English_return_frames=[v['fixture_exit_frame'] for v in actual['versions']],
        command_timing_difference_count=0,later_sampled_whole_RGB_difference_count=0,
        final_13001_PRNG_seeds=seeds,final_13001_PRNG_equal=seeds[0]==seeds[1],
        exported_snapshots=snapshots,no_broad_world_effect_full_RAM_or_future_simulation_equivalence_claim=True,
        source_name_portrait_item_and_background_visibility_preserved_without_normalization=True,
        no_natural_event198_activation_original_location_exhaustive_condition_visits_or_hardware_claim=True,
        actual_source_English_cold_boots=2,total_successful_frames=26002,new_English_runs=1,
        original_source_run_reused_and_not_recounted_as_new=True,offline_only_source_indices=[65,95],
        evidence={str(p):sha(p.read_bytes()) for p in [ACTUAL,Path(__file__)]},new_review_credit=0,full_goal_complete=False))
    print(dict(paired_sheets=3,nontext_frames=len(actual['all_sampled_frame_comparisons']),returns=[v['fixture_exit_frame'] for v in actual['versions']],PRNG_seeds=seeds))
