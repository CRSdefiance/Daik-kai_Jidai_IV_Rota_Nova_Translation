"""Audit all ten English objects and preserve measured timing, RGB and final-state limits."""
import inspect
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.lil_B207_name_style_v6354d import native_name_raster
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_shipyard_gameplay_v760 import models
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_followup_gameplay_v778 import tasks
from scripts.verify_ceremony_prayer_gameplay_v814 import calendar
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B210_actual_v6522');RUN=Path('work/analysis/lil_B210_English_run_v6517');FIXTURE=Path('work/analysis/lil_B210_English_fixture_v6516/complete_B210_English_B22_fixture.json');SOURCE=Path('work/analysis/lil_B210_source_actual_v6510/all10_source_panels_all21_commands_and_observed_return.json');STORED=Path('work/analysis/lil_B210_stored_v6514/all10_final_stored_targets40_alignment_cases_and10_complete_pages.json');NAMES=Path('work/analysis/lil_B210_name_source_planes_v6511/four_name_planes32_literal_alignments_all_source_headers_and_ten_Japanese_body_masks.json')
if __name__=='__main__':
    assert not ROOT.exists();fixture=read(FIXTURE)['fixtures'][0];terminal,plan,source,stored,names=map(read,[RUN/'terminal.json',RUN/'run_plan.json',SOURCE,STORED,NAMES]);cap=Path(plan['capture_folder']);rp,tp=cap/'capture_report.json',cap/'observer/commands.json';report,trace=read(rp),read(tp)
    assert terminal['terminal'] and terminal['observer_host_slots_restored'] and terminal['observer_instances']==1 and not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact'];assert report['frames']==16001 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and not report.get('battery_save_preloaded') and not any(v for k,v in report.items() if k.startswith('synthetic_'))
    assert report['ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes()) and plan['all12_source_commands_retained'] and plan['source_event210_not_naturally_selected'];schedule=read(plan['original_inputs']);assert sha(Path(plan['original_inputs']).read_bytes())==plan['inputs_sha256']==source['input_schedule_sha256'] and report['scripted_input_schedule']==schedule
    image=NdsImage.open(fixture['research_ROM']);sourceim=NdsImage.open(source['research_ROM']);arm=image.read_file('/__arm9__.bin');assert arm==sourceim.read_file('/__arm9__.bin');before,after=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [sourceim,image]];assert [i for i,(a,b) in enumerate(zip(before,after,strict=True)) if a!=b]==[22];assert all(image.read_file(p)==v for _,p,v in sourceim.iter_files() if p!='/data/SC2.DK4') and all(image.read_file(p)==v for p,v in sourceim.iter_components())
    refs={r['fixture_command_offset']:r for r in fixture['original_text_records']};commands={r['fixture_offset']:r for r in fixture['selected_original_objects']};st={r['id']:r for r in stored['records']};photos={};evidence={str(p):sha(p.read_bytes()) for p in [FIXTURE,RUN/'terminal.json',RUN/'run_plan.json',SOURCE,STORED,NAMES,rp,tp,Path(__file__)]}
    for p in report['frames_captured']:
        path=Path(p['path']);assert sha(path.read_bytes())==p['PNG_sha256'];im=Image.open(path).convert('RGB');assert im.size==(256,384);photos[p['frame']]=(p,im)
    labels={2:'Lil Argot',17:'Al Shin'};nameplanes={}
    for ident,text in labels.items():
        pixels,events,font=native_name_raster(arm,text.encode('ascii'));expected=next(p for p in names['name_planes'] if p['text']==text);assert sha(pixels)==expected['native_plane_sha256'];nameplanes[ident]=(pixels,max(e['x']+6 for e in events))
    pairs=[];panels=[];following=[];seen=set();failures=[]
    for row in trace['rows']:
        assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'];resident=row['source'];assert resident['classification']=='original_SC_cache' and resident['route']==2 and resident['whole_resident_payload_exact_ROM'] and resident['actual_sha256']==sha(after[resident['block']])
        if row['kind']!='after_command':continue
        if resident['block']!=22:following.append(dict(frame=row['frame'],block=resident['block'],offset=resident['instruction_offset'],word=resident['first_word'],native_result=row['result_words']));continue
        entry=trace['rows'][row['entry_row']];at=entry['source']['instruction_offset'];seen.add(at);c=commands.get(at)
        if c:assert entry['source']['first_word']==c['source_word'] and row['decoded_length']==c['native_extent']
        pair=dict(fixture_offset=at,source_offset=None if c is None else c['source_offset'],word=entry['source']['first_word'],start=entry['frame'],returned=row['frame'],native_result=row['result_words'],decoded_length=row['decoded_length'],before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed'],UI_after=row['native_UI_request_words']);pairs.append(pair)
        if at not in refs:continue
        ref=refs[at];record=st[ref['id']];pages=record['complete_pages']['pages'];assert len(pages)==1;page=pages[0];pixels=Path(page['native_plane']).read_bytes();assert sha(pixels)==page['native_plane_sha256'];ink={(i%216,i//216) for i,b in enumerate(pixels) if b==1};namepixels,width=nameplanes[ref['source_selector']];nameink={(i%216,i//216) for i,b in enumerate(namepixels) if b};complete=[];partial=[];nameholds=[]
        for frame,(photo,im) in photos.items():
            if not entry['frame']+20<frame<row['frame']-4:continue
            body={(x-16,y-296) for y in range(296,360) for x in range(16,232) if im.getpixel((x,y))==(0,8,0)};header={(x-4,y) for y in range(13) for x in range(width+8) if im.getpixel((12+x,276+y))==(98,97,98)}
            if header!=nameink:failures.append(dict(id=ref['id'],frame=frame,kind='nameplate',missing=len(nameink-header),extra=len(header-nameink)))
            else:nameholds.append(dict(frame=frame,capture=photo['path'],sha256=photo['PNG_sha256'],complete_native_name_and_blank_guards_equal=True))
            if body==ink:complete.append(dict(frame=frame,capture=photo['path'],sha256=photo['PNG_sha256'],complete_independent_native_body_and_all_glyphs_equal=True))
            else:partial.append(dict(frame=frame,missing=len(ink-body),extra=len(body-ink),incomplete_progressive_or_transition_frame=True))
        assert complete and nameholds,ref['id'];panels.append(dict(id=ref['id'],source_record_index=ref['source_record_index'],source_selector=ref['source_selector'],interval=pair,native_pages=1,complete_body_holds=complete,complete_name_holds=nameholds,incomplete_progressive_holds=partial,selected_complete_capture=complete[-1]))
    assert len(panels)==10 and len(pairs)==21 and seen=={r['offset'] for r in fixture['all21_stored_fixture_commands']} and not failures;assert pairs[-1]['source_offset']==682 and pairs[-1]['native_result'][0]==0
    sourcepairs=source['command_pairs'];assert len(sourcepairs)==len(pairs);resultdiff=[];uidiff=[];timing=[];rng=[];durations=[]
    for a,b in zip(sourcepairs,pairs,strict=True):
        assert a['source_offset']==b['source_offset'] and a['word']==b['word'];base=dict(source_offset=a['source_offset'],word=a['word'])
        for key,out in [('native_result',resultdiff),('UI_after',uidiff)]:
            if a[key]!=b[key]:out.append(dict(**base,source=a[key],English=b[key]))
        if [a['start'],a['returned']]!=[b['start'],b['returned']]:timing.append(dict(**base,source=[a['start'],a['returned']],English=[b['start'],b['returned']]))
        if [a['before_RNG'],a['after_RNG']]!=[b['before_RNG'],b['after_RNG']]:rng.append(dict(**base,source=[a['before_RNG'],a['after_RNG']],English=[b['before_RNG'],b['after_RNG']]))
        if a['returned']-a['start']!=b['returned']-b['start']:durations.append(dict(**base,source=a['returned']-a['start'],English=b['returned']-b['start']))
    assert not resultdiff and not uidiff;source_report_path=Path(source['capture_report']);assert sha(source_report_path.read_bytes())==source['evidence'][str(source_report_path)];source_report=read(source_report_path);assert source_report['ROM_sha256']==source['research_ROM_sha256']==sha(Path(source['research_ROM']).read_bytes());evidence[str(source_report_path)]=sha(source_report_path.read_bytes());evidence['scripts/measure_lil_B209_later_v6475.py']=sha(Path('scripts/measure_lil_B209_later_v6475.py').read_bytes());sourcephotos={p['frame']:p for p in source_report['frames_captured']};later=[];scene=[];upper=[];exitframe=pairs[-1]['returned'];threshold=max(exitframe,source['exit_frame'])+60
    for frame,(photo,im) in photos.items():
        oldphoto=sourcephotos[frame];path=Path(oldphoto['path']);assert sha(path.read_bytes())==oldphoto['PNG_sha256'];oldim=Image.open(path).convert('RGB');diff=ImageChops.difference(oldim,im);bounds=diff.getbbox()
        if frame<=max(exitframe,source['exit_frame']) and oldim.crop((0,0,256,272)).tobytes()!=im.crop((0,0,256,272)).tobytes():upper.append(dict(frame=frame,region=[0,0,256,272],separate_from_body_and_name_pixel_checks=True))
        if bounds:
            value=dict(frame=frame,pixels=sum(v!=(0,0,0) for v in diff.getdata()),bounds=list(bounds),source_capture=str(path),source_sha256=oldphoto['PNG_sha256'],English_capture=photo['path'],English_sha256=photo['PNG_sha256']);(later if frame>threshold else scene).append(value)
    semantic=[];semanticdiff=[]
    for panel in panels:
        original=next(p for p in source['speech_observations'] if p['id']==panel['id']);oldphoto=original['selected_capture'];newphoto=panel['selected_complete_capture'];a,b=[Image.open(p).convert('RGB') for p in [oldphoto['path'],newphoto['capture']]];equal=a.crop((0,0,256,272)).tobytes()==b.crop((0,0,256,272)).tobytes();case=dict(id=panel['id'],source_frame=oldphoto['frame'],English_frame=newphoto['frame'],region=[0,0,256,272],equal=equal,separate_timestamps_not_retimed_or_whole_RGB_equivalence=True);semantic.append(case)
        if not equal:semanticdiff.append(case)
    assert not semanticdiff;final=[]
    for language,snap,im in [('source',source_report['read_only_RAM_snapshot'],sourceim),('English',report['read_only_RAM_snapshot'],image)]:
        raw=Path(snap['path']).read_bytes();assert snap['read_only_export'] and len(raw)==4194304 and sha(raw)==snap['sha256'];code=im.read_file('/__arm9__.bin');cpu,get=get_machine(code,raw);actor=get(0xCB184);captain=get(0x7F244);assert captain==2;groups={fn.__name__:fn(code,raw) for fn in [state,models,persistent_objects,tasks,calendar]};groups['tasks']=dict(bytes=len(groups['tasks']),sha256=sha(groups['tasks']));final.append(dict(language=language,snapshot=snap,components=groups,captain_ID=captain,whole_actor_hex=bytes(cpu.mem_read(actor,0x1A04)).hex(),seed=int.from_bytes(raw[0x168EB8:0x168EBC],'little')));evidence[snap['path']]=snap['sha256']
    equality={k:final[0]['components'][k]==final[1]['components'][k] for k in final[0]['components']};ROOT.mkdir(parents=True);sheets=[]
    for start in range(0,10,6):
        sheet=Image.new('RGB',(1560,832),'#263238');draw=ImageDraw.Draw(sheet)
        for i,panel in enumerate(panels[start:start+6]):
            sample=panel['selected_complete_capture'];x,y=i%3*520,i//3*416;draw.text((x+4,y+3),panel['id']+' frame'+str(sample['frame']),fill='white');sheet.paste(Image.open(sample['capture']).convert('RGB').crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST),(x+4,y+24));evidence[sample['capture']]=sample['sha256']
        path=ROOT/f'all10_complete_English_panels_sheet{start//6+1}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    afterframe=next(f for f in photos if f>threshold);sheet=Image.new('RGB',(512,410),'#263238');draw=ImageDraw.Draw(sheet)
    for i,frame in enumerate([afterframe,16001]):draw.text((i*256+3,3),'English frame'+str(frame),fill='white');sheet.paste(photos[frame][1],(i*256,24))
    path=ROOT/'English_normal_return_and_final_full_frame.png';sheet.save(path);transition=dict(path=str(path),sha256=sha(path.read_bytes()),frames=[afterframe,16001]);later_sheet=None
    if later:
        selected=[later[i] for i in sorted({0,len(later)//2,len(later)-1})];sheet=Image.new('RGB',(512*len(selected),410),'#263238');draw=ImageDraw.Draw(sheet)
        for i,row in enumerate(selected):
            for j,language in enumerate(['source','English']):draw.text((i*512+j*256+3,3),language+' frame'+str(row['frame']),fill='white');sheet.paste(Image.open(row[language+'_capture']).convert('RGB'),(i*512+j*256,24))
        path=ROOT/'first_middle_final_unmasked_later_pairs.png';sheet.save(path);later_sheet=dict(path=str(path),sha256=sha(path.read_bytes()))
    save(ROOT/'all10_English_objects_native_body_name_holds21_commands_and_honest_later_scope.json',dict(candidate=fixture['research_ROM'],candidate_sha256=fixture['research_ROM_sha256'],source_actual_proof=str(SOURCE),source_actual_proof_sha256=sha(SOURCE.read_bytes()),English_fixture=str(FIXTURE),English_fixture_sha256=sha(FIXTURE.read_bytes()),actual_panels=panels,actual_unique_objects=10,actual_complete_native_pages=10,complete_native_body_holds=sum(len(p['complete_body_holds']) for p in panels),complete_native_name_holds=sum(len(p['complete_name_holds']) for p in panels),offline_only_objects=[],failures=failures,command_pairs=pairs,all21_stored_commands_observed=True,all12_original_commands_nine_original_initializers_preambles_A000_and_end_preserved=True,command_result_differences=resultdiff,command_UI_word_differences=uidiff,command_timing_differences=timing,command_RNG_differences=rng,command_duration_changes=durations,source_exit_frame=source['exit_frame'],English_exit_frame=exitframe,normal_English_port_sample_frame=afterframe,following_commands=following,upper_same_frame_region_differences=upper,semantic_upper_scene_portrait_pairs=semantic,semantic_upper_region_differences=semanticdiff,scene_same_frame_RGB_differences=scene,later_same_frame_RGB_differences=later,final_native_values=final,five_native_component_equality=equality,whole_actor_and_captain_equal=final[0]['whole_actor_hex']==final[1]['whole_actor_hex'],final_PRNG_equal=final[0]['seed']==final[1]['seed'],final_PRNG_seeds=[v['seed'] for v in final],final_source_snapshot=source_report['read_only_RAM_snapshot'],final_English_snapshot=report['read_only_RAM_snapshot'],capture_report=str(rp),observer_report=str(tp),review_sheets=sheets,transition_sheet=transition,later_pair_sheet=later_sheet,visual_review_pending=True,ordinary_inputs_identical_to_source_no_RNG_role_roster_condition_result_RAM_battery_or_savestate_force=True,all335_other_blocks_every_other_file_component_font_name_and_runtime_equal_source_fixture=True,name_field_typography_fix_is_separate_unapplied_in_these_content_fixtures=True,natural_event210_original_location_earned_progress_full_effects_routes_and_hardware_unclaimed=True,no_whole_RAM_future_sequence_broad_simulation_equivalence_or_complete_causation_claim=True,all_measured_differences_retained_for_later_older_record_technical_reaudit=True,source_and_English_runs_terminal_reaped=True,source_run16001_reused_without_replay=True,new_English_runs=1,new_English_frames=16001,new_review_credit=0,evidence=evidence,original_final_getter_sources={fn.__name__:inspect.getsource(fn) for fn in [state,models,persistent_objects,tasks,calendar]},RNG_static_data_contract_source='scripts/measure_lil_B209_later_v6475.py',producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(actual_objects=10,pages=10,body_holds=sum(len(p['complete_body_holds']) for p in panels),name_holds=sum(len(p['complete_name_holds']) for p in panels),commands=21,source_exit=source['exit_frame'],English_exit=exitframe,timing=len(timing),RNG=len(rng),durations=len(durations),later_RGB=len(later),final_components_equal=equality,final_actor_equal=final[0]['whole_actor_hex']==final[1]['whole_actor_hex'],seeds=[v['seed'] for v in final],visual_review_pending=True),flush=True)
