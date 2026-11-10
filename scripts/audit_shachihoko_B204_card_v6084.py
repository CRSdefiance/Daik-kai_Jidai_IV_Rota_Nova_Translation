"""Measure complete source-fixture path and every paired frame;do not mask title differences."""
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shachihoko_B204_card_actual_v6084')
PARENT=Path('work/analysis/lil_B204_source_run_v6071_clean_Japanese')
TARGET=Path('work/analysis/shachihoko_B204_card_run_v6083_clean_Japanese')
FIXTURE=Path('work/analysis/shachihoko_B204_card_fixture_v6082/complete_B204_source_B22_fixture_with_provisional_item_name.json')
if __name__=='__main__':
    assert not ROOT.exists();fix=read(FIXTURE);runs=[]
    for label,root in [('parent',PARENT),('target',TARGET)]:
        plan,terminal=map(read,[root/'run_plan.json',root/'terminal.json']);cap=Path(plan['capture_folder']);report,trace=map(read,[cap/'capture_report.json',cap/'observer/commands.json'])
        assert terminal['terminal'] and terminal['observer_host_slots_restored'] and report['cold_boot'] and report['frames']==13001 and not report['savestate_loaded'] and not report['callback_errors'] and not trace['errors'] and not trace['mismatches']
        assert trace['all_host_slots_restored_and_core_file_exact'] and not any(v for k,v in report.items() if k.startswith('synthetic_'))
        pairs=[]
        for row in trace['rows']:
            assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
            if row['kind']!='after_command':continue
            entry=trace['rows'][row['entry_row']];s=entry['source'];assert s['whole_resident_payload_exact_ROM']
            pairs.append(dict(route=s['route'],block=s['block'],offset=s['instruction_offset'],word=s['first_word'],start=entry['frame'],returned=row['frame'],native_result=row['result_words'],decoded_length=row['decoded_length'],before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed']))
        runs.append(dict(case=label,root=root,cap=cap,plan=plan,report=report,trace=trace,pairs=pairs))
    a,b=runs;assert a['pairs']==b['pairs'];scene=[p for p in b['pairs'] if p['block']==22]
    assert len(scene)==35 and len([p for p in scene if p['word']==0x4000])==20 and scene[-1]['returned']==7894
    assert b['report']['ROM_sha256']==fix['fixtures'][0]['research_ROM_sha256'] and sha(Path(fix['fixtures'][0]['research_ROM']).read_bytes())==b['report']['ROM_sha256']
    photos=[];exact=0;different=[]
    for old,new in zip(a['report']['frames_captured'],b['report']['frames_captured'],strict=True):
        assert old['frame']==new['frame'];paths=[Path(r['path']) for r in [old,new]]
        for p,r in zip(paths,[old,new],strict=True):assert sha(p.read_bytes())==r['PNG_sha256']
        images=[Image.open(p).convert('RGB') for p in paths];bounds=ImageChops.difference(*images).getbbox()
        if bounds:
            different.append(dict(frame=old['frame'],difference_bounds=list(bounds),parent=str(paths[0]),target=str(paths[1]),parent_sha256=old['PNG_sha256'],target_sha256=new['PNG_sha256']))
            assert 88<=bounds[0]<bounds[2]<=176 and 238<=bounds[1]<bounds[3]<=249,('unexpected full-frame difference',old['frame'],bounds)
        else:exact+=1
        if old['frame'] in [4510,4750]:photos.extend([(str(old['frame'])+' '+label,im) for label,im in zip(['Original item title','Provisional Shachihoko'],images,strict=True)])
    assert different and len(photos)==4;ROOT.mkdir(parents=True);sheet=Image.new('RGB',(1040,1600),'#263238');draw=ImageDraw.Draw(sheet)
    for i,(label,im) in enumerate(photos):
        x,y=i%2*520,i//2*800;draw.text((x+4,y+3),label,fill='white');sheet.paste(im.resize((512,768),Image.Resampling.NEAREST),(x+4,y+24))
    picture=ROOT/'paired_actual_Japanese_scenes_item_title_only.png';sheet.save(picture)
    save(ROOT/'complete_source_path_and_unmasked_title_only_frame_differences.json',dict(
        source_fixture=str(FIXTURE),source_fixture_sha256=sha(FIXTURE.read_bytes()),all20_source_objects_and35_fixture_commands_observed=True,
        all_parent_target_completed_command_pairs=pairs,parent_target_all_observed_SC_command_paths_timings_results_and_interval_RNG_exact=True,
        source_end_return_frame=7894,whole_frames_compared=exact+len(different),whole_frames_equal=exact,whole_frames_with_measured_title_difference=different,
        no_pixel_mask_no_retiming_no_region_difference_suppression=True,all_measured_RGB_differences_inside_original_item_title_bounds=True,
        source_names_portraits_Japanese_text_cultural_item_image_category_and_other_UI_exact_at_same_frames=True,
        selected_sheet=str(picture),selected_sheet_sha256=sha(picture.read_bytes()),visual_review_pending=True,
        actual_initialized_Amsterdam_B22_fixture_not_natural_event204_activation_or_original_location=True,
        no_item_list_acquisition_menu_earned_inventory_full_route_hardware_or_complete_effect_claim=True,
        no_registered_candidate_or_new_editorial_credit=True,actual_new_cold_boots=1,actual_new_frames=13001,new_review_credit=0,full_goal_complete=False,
        evidence={str(p):sha(p.read_bytes()) for root in [PARENT,TARGET] for p in [root/'run_plan.json',root/'terminal.json',Path(read(root/'run_plan.json')['capture_folder'])/'capture_report.json',Path(read(root/'run_plan.json')['capture_folder'])/'observer/commands.json']}))
    print(dict(paired_frames=exact+len(different),whole_equal=exact,title_only_differences=len(different),all_SC_completed_pairs=len(pairs),B204_end=7894,visual_review_pending=True))
