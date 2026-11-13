"""Measure complete actual native pages and controls while retaining every source/English difference."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B209_actual_v6474')
FIXTURE=Path('work/analysis/lil_B209_English_fixture_v6469/complete_B209_English_B22_fixture.json')
SOURCE=Path('work/analysis/lil_B209_source_actual_v6456/six_actual_panels24_visited_of27_stored_commands_and_honest_conditional_scope.json')
STORED=Path('work/analysis/lil_B209_stored_v6467/all20_final_stored_targets80_alignment_cases_and22_complete_pages.json')
NAMES=Path('work/analysis/lil_B209_name_planes_v6464/four_name_planes112_alignments_actual_headers_and_two_source_style4_masks.json')
RUN=Path('work/analysis/lil_B209_English_run_v6470')
def load_photos(report):
    result={}
    for row in report['frames_captured']:
        p=Path(row['path']);assert sha(p.read_bytes())==row['PNG_sha256'];im=Image.open(p).convert('RGB');assert im.size==(256,384);result[row['frame']]=(row,im)
    return result
def dark_body(im):return {(x-16,y-296) for y in range(296,360) for x in range(16,232) if im.getpixel((x,y))==(0,8,0)}
if __name__=='__main__':
    assert not ROOT.exists();fixture=read(FIXTURE)['fixtures'][0];source,stored,names=map(read,[SOURCE,STORED,NAMES]);terminal,plan=read(RUN/'terminal.json'),read(RUN/'run_plan.json');cap=Path(plan['capture_folder']);rp,tp=cap/'capture_report.json',cap/'observer/commands.json';report,trace=read(rp),read(tp)
    assert terminal['terminal'] and terminal['observer_host_slots_restored'] and terminal['observer_instances']==1 and report['cold_boot'] and report['frames']==16001 and not report['savestate_loaded'] and not report['callback_errors'] and not report.get('battery_save_preloaded')
    assert report['ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes()) and not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact']
    assert not any(v for k,v in report.items() if k.startswith('synthetic_')) and plan['all18_source_commands_retained'] and plan['source_event209_not_naturally_selected']
    sr=read(source['capture_report']);assert report['scripted_input_schedule']==sr['scripted_input_schedule']==read(plan['original_inputs']) and sha(Path(plan['original_inputs']).read_bytes())==plan['inputs_sha256']==source['input_schedule_sha256']
    assert report['core_DLL_sha256']==sr['core_DLL_sha256'] and report['core_options']==sr['core_options']
    photos=load_photos(report);sourcephotos=load_photos(sr);image=NdsImage.open(fixture['research_ROM']);bank=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;sourceimage=NdsImage.open(source['research_ROM'])
    assert all(sourceimage.read_file(p)==v for p,v in image.iter_components())
    assert [p for _,p,v in image.iter_files() if sourceimage.read_file(p)!=v]==['/data/SC2.DK4']
    sourcebank=IlnkContainer.parse(sourceimage.read_file('/data/SC2.DK4')).blocks;assert [i for i,(a,b) in enumerate(zip(sourcebank,bank,strict=True)) if a!=b]==[22]
    commands={r['fixture_offset']:r for r in fixture['selected_original_objects']};records={r['fixture_command_offset']:r for r in fixture['original_text_records']};fonts={r['id']:r for r in stored['records']};nameplanes={r['actor_ID']:r for r in names['planes']}
    pairs=[];following=[];panels=[];failures=[];partial=[];names_total=0;complete_body_holds=0
    for row in trace['rows']:
        assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'];s=row['source'];assert s['classification']=='original_SC_cache' and s['route']==2 and s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==sha(bank[s['block']])
        if row['kind']!='after_command':continue
        if s['block']!=22:following.append(dict(frame=row['frame'],block=s['block'],offset=s['instruction_offset'],word=s['first_word'],native_result=row['result_words']));continue
        entry=trace['rows'][row['entry_row']];at=entry['source']['instruction_offset'];c=commands.get(at)
        pair=dict(fixture_offset=at,source_offset=None if c is None else c['source_offset'],word=entry['source']['first_word'],start=entry['frame'],returned=row['frame'],native_result=row['result_words'],decoded_length=row['decoded_length'],before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed'],UI_after=row['native_UI_request_words']);pairs.append(pair)
        if at not in records and pair['word']!=0x4100:continue
        if at in records:ident=records[at]['id'];actor=records[at]['source_selector']
        else:ident='DK4_VOICE_B209_C8_T188' if c['source_offset']==8 else 'DK4_VOICE_B209_C702_T164';actor=151
        assert c is not None and ident in fonts
        f=fonts[ident];pageproofs=f['complete_pages']['pages'];pageinks=[]
        for pg in pageproofs:
            pixels=Path(pg['native_plane']).read_bytes();assert sha(pixels)==pg['native_plane_sha256'];pageinks.append({(i%216,i//216) for i,b in enumerate(pixels) if b==1})
        np=nameplanes[actor];preview=Path(np['preview']);assert sha(preview.read_bytes())==np['preview_sha256'];nameim=Image.open(preview).convert('RGB');nameink={(x,y) for y in range(64) for x in range(216) if nameim.getpixel((x,y))==(65,53,42)};namewidth=max(e['x']+6 for e in np['native_glyph_events']);held=[p for frame,(p,im) in photos.items() if pair['start']+20<frame<pair['returned']-4]
        complete=[[] for _ in pageproofs];nameholds=[];other=[]
        for photo in held:
            im=photos[photo['frame']][1];body=dark_body(im);matching=[i for i,ink in enumerate(pageinks) if body==ink]
            found={(x-4,y) for y in range(13) for x in range(namewidth+8) if im.getpixel((12+x,276+y))==(98,97,98)}
            if found!=nameink:failures.append(dict(id=ident,frame=photo['frame'],kind='name-mask',missing=len(nameink-found),extra=len(found-nameink)))
            else:nameholds.append(dict(frame=photo['frame'],capture=photo['path'],sha256=photo['PNG_sha256'],complete_native_header_and_guards_equal=True));names_total+=1
            if matching:
                assert len(matching)==1;index=matching[0];complete[index].append(dict(frame=photo['frame'],capture=photo['path'],sha256=photo['PNG_sha256'],complete_independent_native_body_and_all_glyphs_equal=True));complete_body_holds+=1
            else:
                nearest=min(range(len(pageinks)),key=lambda i:len(body^pageinks[i]));other.append(dict(frame=photo['frame'],nearest_page=nearest+1,missing=len(pageinks[nearest]-body),extra=len(body-pageinks[nearest]),empty_body=not body,unclassified_progressive_or_transition_hold=True))
        for i,holds in enumerate(complete):
            if not holds:failures.append(dict(id=ident,page=i+1,kind='no-complete-actual-page',held_frames=[h['frame'] for h in held]))
        changes=[]
        if len(complete)==2 and all(complete):
            first,last=complete[0][-1]['frame'],complete[1][0]['frame'];buttons=[b for b in report['scripted_input_schedule'] if first<b['start']<=last and b['buttons']==['A']];assert buttons
            changes.append(dict(last_complete_page1_frame=first,first_complete_page2_frame=last,ordinary_A_events_between=buttons,no_fixture_command_inserted_for_page=True))
        panels.append(dict(id=ident,source_offset=c['source_offset'],source_selector=208 if actor==151 else actor,actor_ID=actor,interval=pair,native_pages=len(pageproofs),actual_complete_page_holds=complete,actual_complete_name_holds=nameholds,partial_or_transition_holds=other,ordinary_page_transitions=changes))
    assert len(pairs)==24 and len(panels)==6 and len(following)>0 and sum(p['native_pages'] for p in panels)==8
    assert [p['source_offset'] for p in pairs]==[p['source_offset'] for p in source['command_pairs']] and [p['word'] for p in pairs]==[p['word'] for p in source['command_pairs']]
    results=[];ui=[];timing=[];rng=[];durations=[]
    for a,b in zip(source['command_pairs'],pairs,strict=True):
        key=dict(source_offset=a['source_offset'],word=a['word'])
        if a['native_result']!=b['native_result']:results.append(dict(**key,source=a['native_result'],English=b['native_result']))
        if a['UI_after']!=b['UI_after']:ui.append(dict(**key,source=a['UI_after'],English=b['UI_after']))
        if [a['start'],a['returned']]!=[b['start'],b['returned']]:timing.append(dict(**key,source=[a['start'],a['returned']],English=[b['start'],b['returned']]))
        if [a['before_RNG'],a['after_RNG']]!=[b['before_RNG'],b['after_RNG']]:rng.append(dict(**key,source=[a['before_RNG'],a['after_RNG']],English=[b['before_RNG'],b['after_RNG']]))
        if a['returned']-a['start']!=b['returned']-b['start']:durations.append(dict(**key,source=a['returned']-a['start'],English=b['returned']-b['start']))
    assert pairs[-1]['word']==0 and pairs[-1]['native_result']==[0,0] and next(p for p in pairs if p['source_offset']==686)['native_result']==[2,0]
    exitframe=pairs[-1]['returned'];later=[];same=[]
    for frame,(photo,im) in photos.items():
        assert frame in sourcephotos
        old=sourcephotos[frame][1]
        if im.tobytes()!=old.tobytes():
            pixels_a,pixels_b=im.load(),old.load();points=[(x,y) for y in range(384) for x in range(256) if pixels_a[x,y]!=pixels_b[x,y]];item=dict(frame=frame,pixels=len(points),bounds=[min(x for x,y in points),min(y for x,y in points),max(x for x,y in points)+1,max(y for x,y in points)+1],source_capture=sourcephotos[frame][0]['path'],source_sha256=sourcephotos[frame][0]['PNG_sha256'],English_capture=photo['path'],English_sha256=photo['PNG_sha256'])
            (later if frame>max(exitframe,source['exit_frame'])+60 else same).append(item)
    ROOT.mkdir(parents=True);sheets=[];allpages=[]
    for panel in panels:
        for index,holds in enumerate(panel['actual_complete_page_holds']):
            if holds:allpages.append((panel['id'],index+1,holds[-1]))
    for start in range(0,len(allpages),4):
        sheet=Image.new('RGB',(1024,430),'#263238');draw=ImageDraw.Draw(sheet)
        for n,(ident,page,photo) in enumerate(allpages[start:start+4]):
            x=n*256;draw.text((x+2,3),ident+' p'+str(page),fill='white');draw.text((x+2,18),'Actual frame'+str(photo['frame']),fill='white');sheet.paste(photos[photo['frame']][1],(x,40))
        p=ROOT/f'all_eight_actual_English_pages_sheet{start//4+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    after=next(f for f in photos if f>exitframe+60);frames=[after,16001];sheet=Image.new('RGB',(512,410),'#263238');draw=ImageDraw.Draw(sheet)
    for i,f in enumerate(frames):draw.text((i*256+2,2),'English frame'+str(f),fill='white');sheet.paste(photos[f][1],(i*256,24))
    p=ROOT/'English_normal_return_and_final_frame.png';sheet.save(p);transitions=[dict(path=str(p),sha256=sha(p.read_bytes()),frames=frames)]
    save(ROOT/'six_English_objects_eight_native_pages24_commands_and_source_differences.json',dict(fixture=str(FIXTURE),fixture_sha256=sha(FIXTURE.read_bytes()),source_actual_proof=str(SOURCE),source_actual_proof_sha256=sha(SOURCE.read_bytes()),stored_native_proof=str(STORED),stored_native_proof_sha256=sha(STORED.read_bytes()),candidate=fixture['research_ROM'],candidate_sha256=fixture['research_ROM_sha256'],actual_panels=panels,actual_unique_objects=6,actual_complete_native_pages=len(allpages),complete_native_body_holds=complete_body_holds,complete_native_name_holds=names_total,failures=failures,command_pairs=pairs,following_commands=following,all24_visited_commands_same_original_path_and_result_type=True,stored_commands=27,explicit_Jam_R65_and13_other_stored_style_bodies_unvisited=True,command_result_differences=results,command_UI_word_differences=ui,command_timing_differences=timing,command_RNG_differences=rng,command_duration_changes=durations,source_exit_frame=source['exit_frame'],English_exit_frame=exitframe,English_normal_port_sample_frame=after,ordinary_original_A_schedule_identical_to_source=True,original_predicate_type2_Boolean0_and_branches_preserved=True,all335_other_blocks_and_all_other_files_components_runtime_and_names_equal_source_fixture=True,same_frame_RGB_differences_during_scene=same,later_same_frame_RGB_differences=later,no_pixel_masking_edit_or_input_retiming=True,review_sheets=sheets,transition_sheets=transitions,visual_review_pending=True,both_runs16001_frames_total32002=True,source_run_reused_without_replay=True,English_session95798_terminal_and_reaped=True,all_current_jobs_terminal_and_reaped=True,actual_page_mask_scope_not_all20_conditional_objects_or_full_route=True,natural_event209_dependency85_original_location_earned_progress_full_effects_or_hardware_unclaimed=True,whole_RAM_final_PRNG_and_future_simulation_equivalence_unproven=True,capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes()),observer_report=str(tp),observer_report_sha256=sha(tp.read_bytes()),source_capture_report=source['capture_report'],final_source_snapshot=sr['read_only_RAM_snapshot'],final_English_snapshot=report['read_only_RAM_snapshot'],new_English_runs=1,new_English_frames=16001,new_review_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(objects=len(panels),complete_pages=len(allpages),body_holds=complete_body_holds,name_holds=names_total,failures=failures,result_differences=len(results),UI_differences=len(ui),timing=len(timing),RNG=len(rng),duration=len(durations),later_RGB=len(later),source_exit=source['exit_frame'],English_exit=exitframe,normal_port_sample=after,sheets=len(sheets)))
    if failures or results:raise SystemExit(1)
