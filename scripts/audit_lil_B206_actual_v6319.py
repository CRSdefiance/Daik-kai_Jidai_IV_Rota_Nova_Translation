"""Pair three same-code source/English paths,complete native holds,menus and unmasked timing/RNG/RGB evidence."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.lil_B206_actual_source_v6318 import load,SOURCE,ENGLISH
from scripts.lil_B206_actual_masks_v6318b import match_English
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B206_actual_v6319');FONT=Path('work/analysis/lil_B206_fonts_v6298/all24_final_progressive_planes24_fresh168_exact_reused_alignment_cases.json');PATHS=['buy','high_price','pitch_refusal']
if __name__=='__main__':
    assert not ROOT.exists();font=read(FONT);values={(language,path):load(language,path) for language in ['source','English'] for path in PATHS};versions=[];actual=[];menus=[];failures=[];unique={};evidence={str(p):sha(p.read_bytes()) for p in [SOURCE,ENGLISH,FONT,Path(__file__),Path('scripts/lil_B206_actual_source_v6318.py'),Path('scripts/lil_B206_actual_masks_v6318b.py'),Path('work/analysis/lil_B206_actual_menu_palette_v6318b/actual_highlight_palette_and_all_four_complete_buy_menu_labels.json')]};seen={language:set() for language in ['source','English']};timing=[];rng=[];results=[];UI=[];nontext=[];comparisons=[];state_pairs=[]
    for path in PATHS:
        source,english=[values[language,path] for language in ['source','English']]
        assert source['plan']['inputs_sha256']==english['plan']['inputs_sha256'] and source['report']['scripted_input_schedule']==english['report']['scripted_input_schedule'] and source['report']['core_DLL_sha256']==english['report']['core_DLL_sha256'] and source['report']['core_options']==english['report']['core_options']
        assert source['photos'].keys()==english['photos'].keys() and all(english['image'].read_file(p)==v for p,v in source['image'].iter_components()) and [p for _,p,v in source['image'].iter_files() if english['image'].read_file(p)!=v]==['/data/SC2.DK4']
        left,right=[IlnkContainer.parse(v['image'].read_file('/data/SC2.DK4')).blocks for v in [source,english]];assert [n for n,(a,b) in enumerate(zip(left,right,strict=True)) if a!=b]==[22]
        a,b=source['command_pairs'],english['command_pairs'];assert len(a)==len(b) and [(r['source_offset'],r['word']) for r in a]==[(r['source_offset'],r['word']) for r in b]
        for old,new in zip(a,b,strict=True):
            if [old['start'],old['returned']]!=[new['start'],new['returned']]:timing.append(dict(path=path,source_offset=old['source_offset'],word=old['word'],Japanese=[old['start'],old['returned']],English=[new['start'],new['returned']]))
            if [old['before_RNG'],old['after_RNG']]!=[new['before_RNG'],new['after_RNG']]:rng.append(dict(path=path,source_offset=old['source_offset'],word=old['word'],Japanese=[old['before_RNG'],old['after_RNG']],English=[new['before_RNG'],new['after_RNG']]))
            if old['native_result']!=new['native_result']:results.append(dict(path=path,source=old,English=new))
            if old['UI_after']!=new['UI_after']:UI.append(dict(path=path,source=old,English=new))
        for frame,(p,jp) in source['photos'].items():
            q,en=english['photos'][frame];comparisons.append(dict(path=path,frame=frame,whole_RGB_equal=jp.tobytes()==en.tobytes(),whole_RGB_difference_bbox=ImageChops.difference(jp,en).getbbox(),after_both_scene_exits=frame>max(source['exit_frame'],english['exit_frame']),source_capture=p['path'],source_capture_sha256=p['PNG_sha256'],English_capture=q['path'],English_capture_sha256=q['PNG_sha256'],no_pixel_masking_or_retiming=True))
        matched=match_English(english,font);actual.extend(matched['speech_observations']);menus.extend(matched['actual_menu_cases']);failures.extend(matched['failures']);source_intervals={r['id']:r['interval'] for r in source['speech_intervals']}
        for row in matched['speech_observations']:
            if row['holds']:unique.setdefault(row['id'],row)
            original=source_intervals[row['id']]
            for hold in row['holds']:
                f=hold['frame'];p,jp=source['photos'][f];q,en=english['photos'][f];same=original['start']<f<original['returned'];hold.update(source_capture=p['path'],source_capture_sha256=p['PNG_sha256'],both_versions_in_same_semantic_speech_at_this_frame=same)
                if same:
                    crop=(0,0,256,294);equal=jp.crop(crop).tobytes()==en.crop(crop).tobytes();hold['paired_upper_portrait_name_item_region_equal']=equal
                    if not equal:nontext.append(dict(path=path,id=row['id'],frame=f,region=[0,0,256,294],difference_bbox=ImageChops.difference(jp.crop(crop),en.crop(crop)).getbbox(),both_semantic_speech_holds=True,complete_English_text_and_nameplate_still_match_native=True))
        states=[]
        for language,v in [('source',source),('English',english)]:
            raw=Path(v['final_snapshot']['path']).read_bytes();native=state(v['image'].read_file('/__arm9__.bin'),raw);states.append(dict(language=language,queried_native_market_fields=native));seen[language].update(v['all_seen_offsets']);evidence.update(v['evidence']);versions.append(dict(language=language,path=path,research_ROM=v['fixture']['research_ROM'],research_ROM_sha256=v['fixture']['research_ROM_sha256'],frames=16001,command_pairs=v['command_pairs'],speech_intervals=v['speech_intervals'],actual_menu_intervals=v['menu_intervals'],exit_frame=v['exit_frame'],following_commands=v['following_commands'],final_snapshot=v['final_snapshot'],queried_final_native_market_fields=native,capture_report=v['capture_report'],observer_report=v['observer_report'],input_schedule_sha256=v['plan']['inputs_sha256']))
        state_pairs.append(dict(path=path,versions=states,queried_fields_equal=states[0]['queried_native_market_fields']==states[1]['queried_native_market_fields'],no_whole_state_or_future_world_equivalence_claim=True))
    for language in ['source','English']:
        fixture=values[language,'buy']['fixture'];assert seen[language]=={r['offset'] for r in fixture['all51_stored_fixture_commands']}
    assert len(actual)==55 and len(unique)==24 and len(menus)==5 and not results;ROOT.mkdir(parents=True)
    panels=[(row['id']+' / '+row['path'],Image.open(row['holds'][0]['capture']).convert('RGB').crop((0,192,256,384))) for row in unique.values()];menu_panels=[(r['path']+' / choice'+str(r['source_command_offset'])+' / option'+str(r['observed_selected_option']),Image.open(r['holds'][-1]['capture']).convert('RGB').crop((0,192,256,384))) for r in menus if r['holds']]
    def sheets(items,prefix):
        out=[]
        for start in range(0,len(items),6):
            sheet=Image.new('RGB',(1560,832),'#263238');draw=ImageDraw.Draw(sheet)
            for i,(label,pic) in enumerate(items[start:start+6]):
                x,y=i%3*520,i//3*416;draw.text((x+4,y+3),label,fill='white');sheet.paste(pic.resize((512,384),Image.Resampling.NEAREST),(x+4,y+24))
            p=ROOT/f'{prefix}{start//6+1}.png';sheet.save(p);out.append(dict(path=str(p),sha256=sha(p.read_bytes())))
        return out
    dialogue_sheets=sheets(panels,'actual_English_dialogue_sheet');menu_sheets=sheets(menu_panels,'actual_English_menu_sheet');transitions=[]
    for path in PATHS:
        source,english=[values[language,path] for language in ['source','English']];menu_frame=next(r for r in menus if r['path']==path)['holds'][-1]['frame'];after=next(f for f in source['photos'] if f>max(source['exit_frame'],english['exit_frame'])+45);wanted=[menu_frame,after,16001];sheet=Image.new('RGB',(768,820),'#263238');draw=ImageDraw.Draw(sheet)
        for j,(language,v) in enumerate([('source',source),('English',english)]):
            for i,frame in enumerate(wanted):
                x,y=i*256,j*410;draw.text((x+3,y+3),language+' '+path+' frame'+str(frame),fill='white');sheet.paste(v['photos'][frame][1],(x,y+24))
        p=ROOT/f'{path}_unmasked_source_English_menus_returns_and_final.png';sheet.save(p);transitions.append(dict(path=str(p),sha256=sha(p.read_bytes()),frames=wanted))
    for row in actual:
        for hold in row['holds']:evidence[hold['capture']]=hold['capture_sha256'];evidence[hold['source_capture']]=hold['source_capture_sha256']
    for row in menus:
        for hold in row['holds']:evidence[hold['capture']]=hold['capture_sha256']
    post=[r for r in comparisons if r['after_both_scene_exits']];different=[r for r in post if not r['whole_RGB_equal']]
    save(ROOT/'all24_English_panels55_observations217_native_holds_five_menus_three_same_code_paths.json',dict(versions=versions,actual_panels=actual,actual_unique_speech_panels=len(unique),actual_English_speech_observations=len(actual),complete_native_text_and_nameplate_holds=sum(len(r['holds']) for r in actual),actual_menu_cases=menus,failures=failures,offline_only_display_IDs=[r['id'] for r in actual if not r['holds']],source_and_English_all51_commands42_source_plus9_initializers_observed=True,all_command_paths_and_results_preserved=True,command_result_differences=results,command_UI_word_differences=UI,command_timing_differences=timing,command_RNG_differences=rng,paired_nontext_region_differences=nontext,same_frame_whole_RGB_comparisons=comparisons,postscene_whole_RGB_comparisons=post,later_whole_RGB_differences=different,queried_final_native_state_comparisons=state_pairs,source_and_English_same_ARM9_COMMON_components_all_other_files_all335_other_blocks_and_input_schedules=True,all24_source_selectors_original_character_names_portraits_item138_and_scene_returns_observed=True,source_9000_asking_price_not_complete_payment_or_outer_event_semantics_proof=True,no_natural_event206_original_location_earned_progress_full_effects_routes_or_hardware_claim=True,no_timing_RNG_whole_state_future_sequence_or_broad_simulation_equivalence_claim=True,no_capture_masking_pixel_edit_or_retiming=True,review_sheets=dialogue_sheets,menu_sheets=menu_sheets,transition_sheets=transitions,visual_review_pending=True,new_English_cold_boots=3,new_English_frames=48003,new_same_code_source_refusal_boots=2,new_same_code_source_refusal_frames=32002,old_same_code_source_buy_v6262_reused_frames=16001,new_total_frames_this_phase=80005,all_jobs_terminal_and_reaped=True,evidence=evidence,new_review_credit=0,full_goal_complete=False));print(dict(unique_English_panels=len(unique),observations=len(actual),complete_holds=sum(len(r['holds']) for r in actual),menu_visits=len(menus),menu_holds=sum(len(r['holds']) for r in menus),failures=failures,timing_differences=len(timing),RNG_differences=len(rng),UI_word_differences=len(UI),shared_nontext_differences=len(nontext),postscene_RGB_differences=len(different),English_exits=[values['English',p]['exit_frame'] for p in PATHS],source_exits=[values['source',p]['exit_frame'] for p in PATHS]))
    if failures:raise SystemExit(1)
