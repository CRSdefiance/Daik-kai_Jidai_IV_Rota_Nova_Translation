"""Measure both actual English choices and all complete pages against independent native planes."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts import native_B221_menu_backing_v6976 as backing
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B221_English_actual_v7004')
FIXTURE=Path('work/analysis/lil_B221_English_fixture_v7001/complete_B221_English_B22_fixture.json')
SOURCE=Path('work/analysis/lil_B221_source_actual_v6988/two_source_choices_all14_speeches_all30_commands_complete_bodies_names_and_returns.json')
STORED=Path('work/analysis/lil_B221_stored_v6995/all14_final_stored_targets56_alignments16_complete_pages.json')
NAMES=Path('work/analysis/lil_B221_name_planes_v6981/three_actors_six_getters_nine_name_component_planes36_alignments.json')
MENU=Path('work/analysis/lil_B221_choices_v6977/three_original_choice_decoders_nine_modal_cases_twelve_complete_label_planes.json')
RELOCATION=Path('work/analysis/lil_B221_relocation_v6994/all16_objects21_commands_four_relatives_full1208_inverse_RESEARCH.json')
CONSUMER=Path('work/analysis/lil_B221_consumers_v6968/fourteen_effective_bodies28_dispatches_three_actors_six_name_consumers.json')
RUNS=[(0,Path('work/analysis/lil_B221_English_run_v7002')),(1,Path('work/analysis/lil_B221_English_run_v7003'))]

def photos(report):
    result={}
    for photo in report['frames_captured']:
        assert sha(Path(photo['path']).read_bytes())==photo['PNG_sha256']
        im=Image.open(photo['path']).convert('RGB');assert im.size==(256,384)
        result[photo['frame']]=(photo,im)
    return result

def body_masks(im):
    return [{(x-16,y-296) for y in range(296,360) for x in range(16,232) if im.getpixel((x,y))==color}
        for color in [(0,8,0),(98,97,98)]]

if __name__=='__main__':
    assert not ROOT.exists()
    fixture=read(FIXTURE)['fixtures'][0]
    source,stored,names,menu,relocation,consumer=map(read,[SOURCE,STORED,NAMES,MENU,RELOCATION,CONSUMER])
    image=NdsImage.open(fixture['research_ROM']);arm=image.read_file('/__arm9__.bin')
    assert sha(Path(fixture['research_ROM']).read_bytes())==fixture['research_ROM_sha256']
    bank=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    commands={r['fixture_offset']:r for r in fixture['selected_original_objects']}
    records={r['fixture_command_offset']:r for r in fixture['original_text_records']}
    storedrows={r['id']:r for r in stored['records']}
    nameplanes={r['text']:r for r in names['name_planes']}
    getters={r['actor_ID']:r['text'] for r in consumer['native_six_distinct_name_consumers']['rows'] if r['consumer']=='progressive-nameplate'}
    target_menu=next(r for r in menu['native_cases'] if r['version']=='reviewed-research')
    width=target_menu['source_derived_text_canvas_width'];rect=target_menu['native_VM_getters_geometry_and_selection']['native_menu_rectangle']
    assert width==48 and rect==[88,64,168,128]
    caption=(rect[0]+16,192+rect[1]+16);menu_masks=[]
    ROOT.mkdir(parents=True)
    for index,label in enumerate(['Yes','No']):
        pixels,proof=backing.paint(arm,label.encode('ascii'),8,width,(0,index*12))
        original=next(r for r in target_menu['all_six_style_label_planes'] if r['index']==index and r['style']==8)
        assert sha(pixels)==original['whole_native_plane_sha256']
        path=ROOT/f'menu_option{index}_style8.bin';path.write_bytes(pixels)
        menu_masks.append({(i%width,i//width) for i,p in enumerate(pixels) if p})
    evidence=[FIXTURE,SOURCE,STORED,NAMES,MENU,RELOCATION,CONSUMER,Path(__file__)]
    versions=[];failures=[];unique=set();allcommands=set();total_body=total_names=total_pages=0
    for selected,RUN in RUNS:
        src=next(r for r in source['versions'] if r['selected_original_option']==selected)
        terminal,plan=read(RUN/'terminal.json'),read(RUN/'run_plan.json')
        cap=Path(plan['capture_folder']);rp,tp=cap/'capture_report.json',cap/'observer/commands.json'
        report,trace=read(rp),read(tp);source_report=read(src['capture_report'])
        assert terminal['terminal'] and terminal['observer_host_slots_restored'] and terminal['observer_instances']==1
        assert report['frames']==16001 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not report.get('battery_save_preloaded') and not report['hardware_device_verification'] and not report['goal_complete']
        assert report['ROM_sha256']==fixture['research_ROM_sha256']
        assert not trace['errors'] and trace['mismatches']==0 and not trace['unreturned_at_capture_end'] and trace['all_host_slots_restored_and_core_file_exact']
        assert plan['explicit_B22_entry_ROM_fixture'] and plan['all21_source_commands_retained'] and plan['source_event221_not_naturally_selected']
        assert src['input_schedule_sha256']==plan['inputs_sha256']==sha(Path(plan['original_inputs']).read_bytes())
        assert report['scripted_input_schedule']==source_report['scripted_input_schedule']==read(plan['original_inputs'])
        assert report['core_DLL_sha256']==source_report['core_DLL_sha256'] and report['core_options']==source_report['core_options']
        assert not any(v for k,v in report.items() if k.startswith('synthetic_'))
        captured=photos(report);source_photos=photos(source_report)
        assert captured.keys()==source_photos.keys()
        pairs=[];panels=[];following=[];page_photos=[]
        for row in trace['rows']:
            assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
            s=row['source'];assert s['classification']=='original_SC_cache' and s['route']==2 and s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==sha(bank[s['block']])
            if row['kind']!='after_command':continue
            if s['block']!=22:
                following.append(dict(frame=row['frame'],block=s['block'],offset=s['instruction_offset'],word=s['first_word'],native_result=row['result_words']))
                continue
            entry=trace['rows'][row['entry_row']];at=entry['source']['instruction_offset'];command=commands.get(at);word=entry['source']['first_word']
            if command:
                assert word==command['source_word'];expected=command['native_extent']
                if word in [0x100,0x200,0x300]:
                    edge=next(e for e in relocation['blocks'][0]['relative_skip_fixups'] if e['offset']==command['source_offset'])
                    case=next(c for c in relocation['blocks'][0]['target_native_skip_cases'] if c['new_offset']==edge['new_offset'] and c['last_result']==selected)
                    expected=case['native_extent']
                assert row['decoded_length']==expected
                allcommands.add(command['source_offset'])
            pair=dict(fixture_offset=at,source_offset=None if command is None else command['source_offset'],word=word,
                start=entry['frame'],returned=row['frame'],native_result=row['result_words'],decoded_length=row['decoded_length'],
                before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed'],UI_after=row['native_UI_request_words'])
            pairs.append(pair)
            if at not in records:continue
            record=records[at];ref=storedrows[record['id']];native_pages=ref['complete_pages']['pages'];page_masks=[]
            for page in native_pages:
                plane=Path(page['native_plane']).read_bytes();assert sha(plane)==page['native_plane_sha256']
                page_masks.append([{(i%216,i//216) for i,v in enumerate(plane) if v==color} for color in [1,15]])
            name=nameplanes[getters[record['source_selector']]];np=Path(name['native_plane']).read_bytes()
            assert sha(np)==name['native_plane_sha256'];nameink={(i%216,i//216) for i,v in enumerate(np) if v}
            namewidth=name['original_pair_flush_width'];holds=[[] for _ in native_pages];nameholds=[];partial=[];sequence=[]
            for frame,(photo,im) in captured.items():
                if not entry['frame']+20<frame<row['frame']-4:continue
                masks=body_masks(im);matches=[i for i,expected in enumerate(page_masks) if masks==expected]
                actualname={(x-16,y-276) for y in range(276,289) for x in range(14,18+namewidth) if im.getpixel((x,y))==(98,97,98)}
                if actualname!=nameink:
                    failures.append(dict(choice=selected,id=record['id'],frame=frame,kind='current-name-mask',missing=len(nameink-actualname),extra=len(actualname-nameink)))
                else:nameholds.append(dict(frame=frame,capture=photo['path'],sha256=photo['PNG_sha256'],complete_name_and_blank_guards_equal=True))
                if matches:
                    assert len(matches)==1;page=matches[0];sequence.append(page+1)
                    holds[page].append(dict(frame=frame,capture=photo['path'],sha256=photo['PNG_sha256'],complete_native_black_gray_all_glyphs_equal=True))
                else:
                    nearest=min(range(len(page_masks)),key=lambda i:sum(len(a^b) for a,b in zip(masks,page_masks[i],strict=True)))
                    partial.append(dict(frame=frame,nearest_page=nearest+1,missing_black=len(page_masks[nearest][0]-masks[0]),extra_black=len(masks[0]-page_masks[nearest][0]),
                        missing_gray=len(page_masks[nearest][1]-masks[1]),extra_gray=len(masks[1]-page_masks[nearest][1]),unclassified_progressive_or_transition_sample=True))
            for index,pageholds in enumerate(holds):
                if not pageholds:failures.append(dict(choice=selected,id=record['id'],page=index+1,kind='no-complete-actual-page'))
                else:page_photos.append((record['id'],index+1,pageholds[-1]))
            assert sequence==sorted(sequence)
            transitions=[]
            if len(holds)==2 and all(holds):
                first,last=holds[0][-1]['frame'],holds[1][0]['frame']
                buttons=[r for r in report['scripted_input_schedule'] if first<r['start']<=last and r['buttons']==['A']]
                assert buttons
                transitions.append(dict(last_complete_page1_frame=first,first_complete_page2_frame=last,ordinary_A_events_between=buttons,no_new_scene_command_for_page=True))
            src_panel=next(p for p in src['source_speech_observations'] if p['id']==record['id'])
            source_image=Image.open(src_panel['selected_capture']['path']).convert('RGB')
            semantic=[]
            for index,pageholds in enumerate(holds):
                if not pageholds:continue
                im=captured[pageholds[-1]['frame']][1]
                upper=im.crop((0,0,256,192)).tobytes()==source_image.crop((0,0,256,192)).tobytes()
                portrait=im.crop((0,192,68,266)).tobytes()==source_image.crop((0,192,68,266)).tobytes()
                if not portrait:failures.append(dict(choice=selected,id=record['id'],page=index+1,kind='source-portrait-RGB-difference'))
                semantic.append(dict(page=index+1,English_frame=pageholds[-1]['frame'],source_frame=src_panel['selected_capture']['frame'],upper_scene_RGB_equal=upper,portrait_RGB_equal=portrait))
            panels.append(dict(id=record['id'],source_record_index=record['source_record_index'],source_selector=record['source_selector'],interval=pair,
                native_pages=len(native_pages),actual_complete_page_holds=holds,complete_name_holds=nameholds,
                partial_or_transition_holds=partial,ordinary_page_transitions=transitions,semantic_source_scene_portrait_pairs=semantic))
        assert len(pairs)==[27,28][selected] and len(panels)==13
        assert [p['source_offset'] for p in pairs]==[p['source_offset'] for p in src['command_pairs']]
        assert [p['word'] for p in pairs]==[p['word'] for p in src['command_pairs']]
        expected=set(storedrows)-{f'DK4_MES_B221_R{33 if selected==0 else 27:04d}'}
        assert {p['id'] for p in panels}==expected;unique.update(expected)
        choice=next(p for p in pairs if p['word']==0x2100)
        assert choice['source_offset']==150 and choice['native_result']==[2,selected]
        assert pairs[-1]['word']==0 and pairs[-1]['native_result']==[0,selected]
        menu_holds=[]
        for frame,(photo,im) in captured.items():
            if not max(choice['start']+30,3705 if selected else 0)<frame<choice['returned']-3:continue
            actual=[{(x,y) for y in range(12) for x in range(width) if im.getpixel((caption[0]+x,caption[1]+index*20+y))==(8,8,8)} for index in range(2)]
            colors=[im.getpixel((caption[0],caption[1]+index*20)) for index in range(2)]
            expected_colors=[(0,165,172) if index==selected else (205,198,180) for index in range(2)]
            if actual==menu_masks and colors==expected_colors:
                menu_holds.append(dict(frame=frame,capture=photo['path'],sha256=photo['PNG_sha256'],both_full_native_labels_and_selected_highlight_equal=True))
        if not menu_holds:failures.append(dict(choice=selected,kind='no-complete-menu-with-correct-visible-selection'))
        comparisons=[]
        for index,(before,after) in enumerate(zip(src['command_pairs'],pairs,strict=True)):
            fields={k:dict(source=before[k],English=after[k]) for k in ['word','native_result','UI_after','start','returned','before_RNG','after_RNG'] if before[k]!=after[k]}
            if fields:comparisons.append(dict(index=index,source_offset=before['source_offset'],word=before['word'],different_fields=fields))
            if before['native_result']!=after['native_result']:
                failures.append(dict(choice=selected,source_offset=before['source_offset'],kind='source-English-command-result-difference',source=before['native_result'],English=after['native_result']))
        exit_frame=pairs[-1]['returned'];after=min(f for f in captured if f>exit_frame+60);later=[]
        for frame,(photo,im) in captured.items():
            if frame<=max(exit_frame,src['exit_frame'])+60:continue
            difference=ImageChops.difference(source_photos[frame][1],im);bounds=difference.getbbox()
            later.append(dict(frame=frame,whole_RGB_equal=bounds is None,whole_RGB_difference_bounds=bounds,
                source_capture=source_photos[frame][0]['path'],source_sha256=source_photos[frame][0]['PNG_sha256'],
                English_capture=photo['path'],English_sha256=photo['PNG_sha256'],no_mask_edit_or_retiming=True))
        version_root=ROOT/f'choice{selected}';version_root.mkdir();sheets=[]
        for start in range(0,len(page_photos),6):
            sheet=Image.new('RGB',(1560,832),'#263238');draw=ImageDraw.Draw(sheet)
            for index,(ident,page,photo) in enumerate(page_photos[start:start+6]):
                x,y=index%3*520,index//3*416
                draw.text((x+4,y+3),ident+' page'+str(page)+' frame'+str(photo['frame']),fill='white')
                sheet.paste(captured[photo['frame']][1].crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST),(x+4,y+24))
            path=version_root/f'six_English_pages_sheet{start//6+1}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
        frames=[3730,after,16001];sheet=Image.new('RGB',(1536,410),'#263238');draw=ImageDraw.Draw(sheet)
        for index,frame in enumerate(frames):
            for language,(photo,im) in enumerate([source_photos[frame],captured[frame]]):
                x=index*512+language*256;draw.text((x+3,3),('Source ' if language==0 else 'English ')+str(frame),fill='white');sheet.paste(im,(x,24))
        transition=version_root/'source_English_menu_return_and_final.png';sheet.save(transition)
        snap=report['read_only_RAM_snapshot'];raw=Path(snap['path']).read_bytes()
        assert snap['read_only_export'] and len(raw)==4194304 and sha(raw)==snap['sha256']
        body_count=sum(len(h) for p in panels for h in p['actual_complete_page_holds'])
        names_count=sum(len(p['complete_name_holds']) for p in panels)
        total_body+=body_count;total_names+=names_count;total_pages+=len(page_photos)
        versions.append(dict(selected_original_option=selected,run=str(RUN),actual_panels=panels,command_pairs=pairs,
            actual_complete_native_pages=len(page_photos),actual_complete_body_holds=body_count,actual_complete_name_holds=names_count,
            actual_menu=dict(interval=choice,labels=['Yes','No'],caption_origin=list(caption),native_rectangle=rect,holds=menu_holds),
            source_actual_version=selected,source_exit_frame=src['exit_frame'],exit_frame=exit_frame,normal_terminal_result=pairs[-1]['native_result'],normal_port_sample_frame=after,
            command_comparison_differences=comparisons,following_native_commands=following,later_sampled_whole_frame_comparisons=later,
            final_snapshot=snap,queried_final_native_state=state(arm,raw),
            review_sheets=sheets,transition_sheet=dict(path=str(transition),sha256=sha(transition.read_bytes()),frames=frames),
            capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes()),observer_report=str(tp),observer_report_sha256=sha(tp.read_bytes()),
            input_schedule_sha256=plan['inputs_sha256']))
        evidence.extend([RUN/'terminal.json',RUN/'run_plan.json',Path(plan['original_inputs']),rp,tp,Path(snap['path'])])
    assert len(unique)==14 and allcommands=={r['source_offset'] for r in fixture['selected_original_objects']}
    assert total_pages==30 and all(len(v['actual_menu']['holds'])>0 for v in versions)
    save(ROOT/'two_English_choices_all14_speeches30_native_pages_complete_masks_and_source_differences.json',dict(
        fixture=str(FIXTURE),fixture_sha256=sha(FIXTURE.read_bytes()),research_ROM=fixture['research_ROM'],research_ROM_sha256=fixture['research_ROM_sha256'],
        source_actual_proof=str(SOURCE),source_actual_proof_sha256=sha(SOURCE.read_bytes()),versions=versions,
        actual_unique_speeches=14,actual_speech_observations=26,actual_complete_native_page_observations=30,
        actual_complete_body_holds=total_body,actual_complete_name_holds=total_names,
        all30_stored_commands_executed_in_union=True,all14_stored_speeches_and_two_original_options_observed=True,
        all_four_actual_two_page_transitions_use_original_A_input=True,
        same_source_schedules_no_button_retiming_or_forced_conditions_results_RNG_roster_funds_RAM=True,
        failures=failures,original_source_runs_reused_without_replay=True,
        current_name_preservation_not_approval_of_Square_Shopkeeper_localization=True,full_catalogue_UI_unvisited=True,
        initialized_B22_not_natural_event221_original_location_earned_progress_full_effects_full_route_or_hardware=True,
        all_measured_timing_RNG_UI_and_later_RGB_differences_preserved=True,
        no_full_RAM_future_sequence_broad_simulation_or_complete_causal_claim=True,
        English_cold_boots=2,English_frames=32002,all_jobs_terminal_and_reaped=True,visual_review_pending=True,new_credit=0,
        evidence={str(p):sha(p.read_bytes()) for p in evidence},full_goal_complete=False))
    print(dict(unique_speeches=14,observations=26,complete_pages=total_pages,body_holds=total_body,name_holds=total_names,
        menu_holds=[len(v['actual_menu']['holds']) for v in versions],
        source_English_exits=[(v['source_exit_frame'],v['exit_frame']) for v in versions],failures=failures,credit=0))
    if failures:raise SystemExit(1)
