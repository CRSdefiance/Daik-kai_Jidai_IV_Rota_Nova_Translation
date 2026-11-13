"""Add the explicitly new active-highlight capture without rewriting the first audit."""
from copy import deepcopy
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import verify_ship_advice_choice_centering_20261022 as prior
from scripts.lil_current_font_oracles_v4792 import CURRENT_ARM9
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B197_actual_v5684b')
ACTUAL=Path('work/analysis/lil_B197_actual_v5684/three_paths_complete_native_panels_three_options_and_source_comparisons.json')
RUN=Path('work/analysis/lil_B197_English_run_v5683c_no_buy_reviewed_English')
MENU=Path('work/analysis/lil_B197_choices_v5669/B197_C230/original_choice_decoder_VM_geometry_and_native_pixels.json')
if __name__=='__main__':
    assert not ROOT.exists();actual=deepcopy(read(ACTUAL));terminal,plan=map(read,[RUN/'terminal.json',RUN/'run_plan.json'])
    assert actual['failures']==[dict(path='no_buy',menu=230,finding='No complete three-label masks with visibly correct returned option.')]
    cap=Path(plan['capture_folder']);report,trace,inputs=map(read,[cap/'capture_report.json',cap/'observer/commands.json',RUN/'ordinary_menu_inputs.json'])
    assert terminal['terminal'] and terminal['observer_host_slots_restored'] and report['frames']==4601 and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact']
    assert all(not v for k,v in report.items() if k.startswith('synthetic_')) and inputs['ordinary_gamepad_only'] and inputs['no_game_RAM_or_predicate_or_seed_write']
    original=next(v for v in actual['versions'] if v['path']=='no_buy' and v['case']=='reviewed_English')
    assert report['ROM_sha256']==plan['research_ROM_sha256']==original['research_ROM_sha256']
    choices=[]
    for row in trace['rows']:
        assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
        if row['kind']=='after_command' and row['source'].get('block')==22 and row['source']['first_word']==0x2200:
            entry=trace['rows'][row['entry_row']];assert entry['source']['whole_resident_payload_exact_ROM']
            choices.append(dict(start=entry['frame'],returned=row['frame'],result=row['result_words']))
    assert len(choices)==1 and choices[0]['result']==[2,1]
    assert [choices[0]['start'],choices[0]['returned']]==[original['actual_choice_pairs'][0]['start'],original['actual_choice_pairs'][0]['returned']]
    menu=read(MENU);target=menu['current_and_reviewed_VM_and_font_cases'][1];width=target['source_derived_text_canvas_width'];assert width==72
    arm=NdsImage.open(original['research_ROM']).read_file('/__arm9__.bin');assert sha(arm)==CURRENT_ARM9
    env={**prior.__dict__,'LABEL_WIDTH':width,'sha':sha,'CURRENT_ARM9':CURRENT_ARM9};exec(compile(menu['source_derived_painter_adapter'],__file__,'exec'),env)
    masks=[]
    for label in ["Let's buy it",'Pass','You decide']:
        pixels,_=env['paint'](arm,label.encode('ascii'),1);masks.append({(x,y) for y in range(20) for x in range(width) if pixels[y*width+x]})
    holds=[]
    for photo in report['frames_captured']:
        frame=photo['frame'];p=Path(photo['path']);assert sha(p.read_bytes())==photo['PNG_sha256']
        if not choices[0]['start']+35<frame<choices[0]['returned']:continue
        pic=Image.open(p).convert('RGB')
        actual_masks=[{(x,y) for y in range(20) for x in range(width) if pic.getpixel((92+x,258+i*20+y))==(8,8,8)} for i in range(3)]
        colors=[pic.getpixel((92,258+20*i)) for i in range(3)]
        if actual_masks!=masks or colors!=[(205,198,180),(0,165,172),(205,198,180)]:continue
        holds.append(dict(frame=frame,path=str(p),sha256=photo['PNG_sha256'],complete_all_three_native_label_masks_equal=True,selected_highlight_matches_return_when_visible=True,
            background_colors=colors,supplemental_focused_cold_boot=True,capture_report=str(cap/'capture_report.json')))
    assert holds
    record=next(m for m in actual['actual_menu_cases'] if m['path']=='no_buy');record['holds'].extend(holds)
    ROOT.mkdir(parents=True);sheet=Image.new('RGB',(1040,832),'#263238');draw=ImageDraw.Draw(sheet)
    for i,record in enumerate(actual['actual_menu_cases']):
        h=next(h for h in record['holds'] if h['selected_highlight_matches_return_when_visible']);pic=Image.open(h['path']).convert('RGB')
        x,y=i%2*520,i//2*416;draw.text((x+4,y+3),record['path']+' / actual option'+str(record['native_result_words'][1]),fill='white');sheet.paste(pic.crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST),(x+4,y+24))
    image=ROOT/'all_three_visible_selected_options.png';sheet.save(image)
    actual.update(previous_incomplete_audit=str(ACTUAL),previous_incomplete_audit_sha256=sha(ACTUAL.read_bytes()),historical_initial_menu_sampling_failure=actual['failures'],failures=[],
        focused_refusal_run_folder=str(RUN),focused_refusal_capture_report=str(cap/'capture_report.json'),focused_refusal_menu_result=choices,
        focused_refusal_complete_active_highlight_holds=holds,supplemental_menu_sheet=dict(path=str(image),sha256=sha(image.read_bytes())),
        new_successful_English_cold_boot_runs=4,new_successful_English_frames=43604,total_successful_paired_frames=82607,
        successful_complete_source_and_English_runs=6,successful_short_English_menu_focus_runs=1,
        earlier_three_full_English_runs_and_Japanese_runs_not_replaced_or_retimed=True,
        selection_blink_is_observed_inactive_in_original4390_and_active_in_new_focused_frames=True,
        focused_run_not_claimed_as_complete_scene_or_new_source_scene_activation=True)
    files=[ACTUAL,MENU,RUN/'terminal.json',RUN/'run_plan.json',RUN/'ordinary_menu_inputs.json',cap/'capture_report.json',cap/'observer/commands.json',Path(__file__)]
    actual['evidence'].update({str(p):sha(p.read_bytes()) for p in files});actual['evidence'].update({h['path']:h['sha256'] for h in holds})
    save(ROOT/'three_paths_and_focused_refusal_highlight.json',actual)
    print(dict(source_English_complete_runs=6,English_menu_focus_frames=4601,complete_active_Pass_holds=len(holds),all21_speeches_35_observations_native_complete=True,all3_actual_options_visible=True))
