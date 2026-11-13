"""Bind actual source route and complete Japanese/body/name masks without forced conditional lines."""
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_name_catalog_glyphs_v278 import raster as old_raster
from scripts.Al_Ferid_font_oracles_v6520 import expected_pixels
from scripts.Al_Ferid_name_style_v6520 import native_name_raster
from scripts.prove_lil_B208_name_planes_v6405 import codes,original_name_events
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B214_source_actual_v6709');FIXTURE=Path('work/analysis/lil_B214_source_fixture_v6702/complete_B214_source_B22_fixture.json');RUN=Path('work/analysis/lil_B214_source_run_v6703')
BRANCH=Path('work/analysis/lil_B214_branches_v6701/original_relative_skip_operand_proof.json');CONTROL=Path('work/analysis/lil_B214_controls_v6708/four_unforced_predicates_ten_structural_cases50_seeded_ends_four_route_models.json')
CONSUMER=Path('work/analysis/lil_B214_consumers_v6698/all17_effective_bodies34_dispatches_two_whole_commands414_style_pointers.json');NAMES=Path('work/analysis/lil_B214_names_v6699/four_names_eight_getters_signature_mismatch_and_other_raw_occurrence_leads.json')
if __name__=='__main__':
    assert not ROOT.exists();fd=read(FIXTURE);fixture=fd['fixtures'][0];terminal,plan=read(RUN/'terminal.json'),read(RUN/'run_plan.json');cap=Path(plan['capture_folder']);rp,tp=cap/'capture_report.json',cap/'observer/commands.json';report,trace=read(rp),read(tp);source=read(fd['source_context']);consumer,names,branch,control=map(read,[CONSUMER,NAMES,BRANCH,CONTROL])
    assert terminal['terminal'] and terminal['observer_host_slots_restored'] and terminal['observer_instances']==1 and report['frames']==16001 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and not report.get('battery_save_preloaded') and not report['hardware_device_verification'] and not report['goal_complete']
    assert report['ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes()) and not trace['errors'] and trace['mismatches']==0 and not trace['unreturned_at_capture_end'] and trace['all_host_slots_restored_and_core_file_exact'] and plan['explicit_B22_entry_ROM_fixture'] and plan['all27_source_commands_retained'] and plan['source_event214_not_naturally_selected']
    schedule=read(plan['original_inputs']);assert sha(Path(plan['original_inputs']).read_bytes())==plan['inputs_sha256'] and report['scripted_input_schedule']==schedule and [r for r in schedule if r['start']<2300]==read('work/analysis/movie_viewport_v303/lil_start_inputs.json') and all(r['buttons']==['A'] for r in schedule if r['start']>=2300) and not any(v for k,v in report.items() if k.startswith('synthetic_'))
    image=NdsImage.open(fixture['research_ROM']);arm=image.read_file('/__arm9__.bin');bank=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;commands={r['fixture_offset']:r for r in fixture['selected_original_objects']};records={r['fixture_command_offset']:r for r in fixture['original_text_records']};photos={}
    for photo in report['frames_captured']:
        assert sha(Path(photo['path']).read_bytes())==photo['PNG_sha256'];im=Image.open(photo['path']).convert('RGB');assert im.size==(256,384);photos[photo['frame']]=(photo,im)
    pairs=[];observations=[];following=[];last=0;seen=set()
    for row in trace['rows']:
        assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'];s=row['source'];assert s['classification']=='original_SC_cache' and s['route']==2 and s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==sha(bank[s['block']])
        if row['kind']!='after_command':continue
        if s['block']!=22:following.append(dict(frame=row['frame'],block=s['block'],offset=s['instruction_offset'],word=s['first_word'],native_result=row['result_words']));continue
        entry=trace['rows'][row['entry_row']];at=entry['source']['instruction_offset'];seen.add(at);command=commands.get(at);word=entry['source']['first_word']
        if command:
            assert word==command['source_word']
            if word in [0x100,0x200,0x300,0x400]:assert row['decoded_length']==next(r for r in branch['cases'] if r['version']=='current' and r['offset']==command['source_offset'] and r['last_choice_or_result']==last)['native_decoded_extent']
            else:assert row['decoded_length']==command['native_extent']
        pair=dict(fixture_offset=at,source_offset=None if command is None else command['source_offset'],word=word,start=entry['frame'],returned=row['frame'],native_result=row['result_words'],decoded_length=row['decoded_length'],before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed'],UI_after=row['native_UI_request_words']);pairs.append(pair)
        if word==0x8000:assert row['result_words']==[2,0];last=0
        if at in records or word==0x4100:
            record=records.get(at);holds=[photo for frame,(photo,_) in photos.items() if entry['frame']+20<frame<row['frame']-4];assert holds
            if record:ident=record['id'];selector=record['source_selector'];kind='progressive';index=record['source_record_index']
            else:
                candidates=[r for r in source['typed_actor_style_records'] if r['command_offset']==command['source_offset'] and 4 in r['style_indices']];assert len(candidates)==1;record=candidates[0];ident=record['id'];selector=208;kind=record['kind'];index=None
            observations.append(dict(id=ident,kind=kind,source_record_index=index,source_selector=selector,interval=pair,selected_capture=holds[-1],held_capture_candidates=holds))
    expected=next(r['offsets'] for r in control['four_structural_route_models'] if r['predicate_Boolean_values']==[0,0]);assert len(pairs)==30 and [p['source_offset'] for p in pairs if p['source_offset'] is not None]==expected and len(observations)==9 and pairs[-1]['native_result']==[0,0] and pairs[-1]['returned']==5015
    offline=[r['id'] for r in source['records']+source['typed_actor_style_records'] if r['id'] not in {p['id'] for p in observations}];assert len(offline)==8 and [r['source_record_index'] for r in observations if r['kind']=='progressive']==[34,38,41,44,48,51,68,75]
    ROOT.mkdir(parents=True)
    class FontROM:
        @staticmethod
        def open(path):assert str(path)=='work/clean.nds';return image
    raster=FunctionType(old_raster.__code__,{**old_raster.__globals__,'NdsImage':FontROM},argdefs=old_raster.__defaults__);raster.__kwdefaults__=old_raster.__kwdefaults__
    dispatch={r['id']:r for r in consumer['speech_and_alternative_dispatch_cases'] if r['version']=='clean-Japanese'};getters={r['actor_ID']:r['progressive'] for r in names['source_name_fields']};bodycases=[];nameholds=[]
    for panel in observations:
        row=next(r for r in source['records']+source['typed_actor_style_records'] if r['id']==panel['id']);d=dispatch[row['id']];body=bytes.fromhex(next(b['text_hex'] for b in d['boundaries'] if b['kind']=='unexecuted-progressive-body'));assert body==bytes.fromhex(row['source_hex'])[1 if row['kind']=='progressive' else 0:]
        pixels,events,font=raster(arm,body);assert pixels==expected_pixels(arm,font,events) and [e['code'] for e in events if e['code']!=32]==[c for c in codes(body) if c not in [32,10]]
        assert all(e['y'] in [0,16,32,48] and 0<=e['x'] and e['x']+(6 if e['kind']=='ascii' else 12)<=216 for e in events);ink={(i%216,i//216) for i,b in enumerate(pixels) if b==1};complete=[];partial=[]
        actor=d['resolved_actor_ID'];label=getters[actor];np,ne,nf=native_name_raster(arm,label.encode('ascii'));assert np==expected_pixels(arm,nf,ne);emitted,flush=original_name_events(ne,label.encode('ascii'));assert emitted==list(label.encode('ascii'));nameink={(i%216,i//216) for i,b in enumerate(np) if b};width=max(e['x']+6 for e in ne)
        for photo in panel['held_capture_candidates']:
            im=photos[photo['frame']][1];found={(x-16,y-296) for y in range(296,360) for x in range(16,232) if im.getpixel((x,y))==(0,8,0)}
            if found!=ink:partial.append(dict(frame=photo['frame'],missing=len(ink-found),extra=len(found-ink),incomplete_progressive_hold=True));continue
            complete.append(dict(frame=photo['frame'],capture=photo['path'],sha256=photo['PNG_sha256'],complete_independent_source_black_mask_equal=True));actualname={(x-16,y-276) for y in range(276,289) for x in range(14,18+width) if im.getpixel((x,y))==(98,97,98)};assert actualname==nameink,(row['id'],photo['frame'],len(nameink-actualname),len(actualname-nameink))
            nameholds.append(dict(id=row['id'],actor_ID=actor,text=label,frame=photo['frame'],capture=photo['path'],sha256=photo['PNG_sha256'],complete_name_and_blank_guards_equal=True))
        assert complete and panel['selected_capture']['frame'] in [h['frame'] for h in complete];bp=ROOT/(row['id']+'_Japanese_complete_native.bin');bp.write_bytes(pixels);bodycases.append(dict(id=row['id'],source_selector=row['source_selector'],expanded_source_body_hex=body.hex(),native_events=events,native_plane=str(bp),native_plane_sha256=sha(pixels),complete_body_holds=complete,incomplete_progressive_holds=partial,source_gray_pixel_masks_not_compared=True))
    sheets=[]
    for start in range(0,len(observations),6):
        sheet=Image.new('RGB',(1560,832),'#263238');draw=ImageDraw.Draw(sheet)
        for index,panel in enumerate(observations[start:start+6]):
            photo=panel['selected_capture'];x,y=index%3*520,index//3*416;draw.text((x+4,y+3),panel['id']+' frame'+str(photo['frame']),fill='white');sheet.paste(photos[photo['frame']][1].crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST),(x+4,y+24))
        p=ROOT/f'Japanese_letter_and_response_sheet{start//6+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    after=min(f for f in photos if f>5015+60);fullframes=[3070,3550,after,16001];sheet=Image.new('RGB',(1024,410),'#263238');draw=ImageDraw.Draw(sheet)
    for index,frame in enumerate(fullframes):draw.text((index*256+3,3),'Source frame'+str(frame),fill='white');sheet.paste(photos[frame][1],(index*256,24))
    sp=ROOT/'source_crew_letter_return_and_final.png';sheet.save(sp);snap=report['read_only_RAM_snapshot'];raw=Path(snap['path']).read_bytes();assert snap['read_only_export'] and len(raw)==4194304 and sha(raw)==snap['sha256']
    save(ROOT/'eight_speeches_one_selected_style_complete_source_masks30_commands_and_return.json',dict(fixture=str(FIXTURE),fixture_sha256=sha(FIXTURE.read_bytes()),research_ROM=fixture['research_ROM'],research_ROM_sha256=fixture['research_ROM_sha256'],speech_observations=observations,actual_panel_observations=observations,source_body_masks=bodycases,actual_source_unique_speeches=8,actual_automatic_style_bodies=1,actual_selected_style_index=4,actual_complete_source_body_holds=sum(len(r['complete_body_holds']) for r in bodycases),actual_complete_name_holds=nameholds,incomplete_sampled_body_holds=sum(len(r['incomplete_progressive_holds']) for r in bodycases),unvisited_source_speech_IDs=['DK4_MES_B214_R0062','DK4_MES_B214_R0087'],offline_only_object_IDs=offline,unvisited_original_command_offsets=sorted(set(commands)-seen),command_pairs=pairs,stored_commands=36,visited_commands=30,both_original_predicates_actual_type2_Boolean0=True,source_Manuel_aside_and_reply_not_observed=True,six_other_automatic_voice_bodies_not_observed=True,all17_stored_objects_not_claimed_as_actual=True,three_current_name_headers_bound_not_full_catalogue_UI=True,source4500_4621_letter_transitions_observed_full_effects_not_decoded=True,exit_frame=5015,native_terminal_result=[0,0],normal_end_retains_existing_result_value=True,normal_port_sample_frame=after,following_native_commands=following,following_blocks=sorted({r['block'] for r in following}),capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes()),observer_report=str(tp),observer_report_sha256=sha(tp.read_bytes()),input_schedule_sha256=plan['inputs_sha256'],final_snapshot=snap,queried_final_native_state=state(arm,raw),review_sheets=sheets,transition_sheet=dict(path=str(sp),sha256=sha(sp.read_bytes()),frames=fullframes),visual_review_pending=True,Japanese_black_masks_only_English_bodies_unvisited=True,current_English_names_in_Japanese_fixture_not_original_Japanese_name_UI=True,actual_new_cold_boot_runs=1,total_frames=16001,ordinary_inputs_roster_roles_funds_conditions_RNG_and_effect_results_unforced=True,initialized_B22_not_natural_event214_original_location_earned_progress_full_effects_route_or_hardware=True,all_jobs_terminal_and_reaped=True,new_editorial_credit=0,evidence={str(p):sha(Path(p).read_bytes()) for p in [FIXTURE,RUN/'terminal.json',RUN/'run_plan.json',Path(plan['original_inputs']),rp,tp,Path(snap['path']),BRANCH,CONTROL,CONSUMER,NAMES,Path(__file__)]},full_goal_complete=False))
    print(dict(actual_speeches=8,selected_style_bodies=1,complete_body_holds=sum(len(r['complete_body_holds']) for r in bodycases),name_holds=len(nameholds),partial=sum(len(r['incomplete_progressive_holds']) for r in bodycases),selected_commands=30,exit=5015,terminal=[0,0],port=after,offline=8,credit=0))
