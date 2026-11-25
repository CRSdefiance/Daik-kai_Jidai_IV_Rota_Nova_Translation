"""Compare every observed source page and header; disclose unvisited conditional/style bodies."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B223_source_actual_v7088');RUN=Path('work/analysis/lil_B223_source_run_v7086')
FIXTURE=Path('work/analysis/lil_B223_source_fixture_v7085/complete_B223_source_B22_fixture.json')
CONTROL=Path('work/analysis/lil_B223_controls_v7082/two_unforced_predicate_cases_ten_structural_cases50_seeded_ends_two_route_models.json')
BRANCH=Path('work/analysis/lil_B223_branches_v7081/original_relative_skip_operand_proof.json')
FONT=Path('work/analysis/lil_B223_source_pages_v7087/all17_clean_objects_complete_native_CP932_pages_and_R40_two_page_sequence.json')
NAMES=Path('work/analysis/lil_B223_name_planes_v7084/four_actors_eight_getters_eleven_name_planes44_alignments.json')
CONSUMER=Path('work/analysis/lil_B223_consumers_v7079/all17_effective_bodies34_dispatches_two_whole_commands414_style_pointers.json')
if __name__=='__main__':
    assert not ROOT.exists();fd=read(FIXTURE);fixture=fd['fixtures'][0];source=read(fd['source_context']);control,branch,font,names,consumer=map(read,[CONTROL,BRANCH,FONT,NAMES,CONSUMER]);terminal,plan=read(RUN/'terminal.json'),read(RUN/'run_plan.json');cap=Path(plan['capture_folder']);rp,tp=cap/'capture_report.json',cap/'observer/commands.json';report,trace=read(rp),read(tp)
    assert terminal['terminal'] and terminal['observer_host_slots_restored'] and terminal['observer_instances']==1 and report['frames']==16001 and report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors'] and not report['hardware_device_verification'] and not report['goal_complete']
    assert report['ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes()) and not trace['errors'] and trace['mismatches']==0 and not trace['unreturned_at_capture_end'] and trace['all_host_slots_restored_and_core_file_exact']
    assert plan['explicit_B22_entry_ROM_fixture'] and plan['all22_source_commands_retained'] and plan['source_event223_not_naturally_selected']
    schedule=read(plan['original_inputs']);assert sha(Path(plan['original_inputs']).read_bytes())==plan['inputs_sha256'] and report['scripted_input_schedule']==schedule and [r for r in schedule if r['start']<2300]==read('work/analysis/movie_viewport_v303/lil_start_inputs.json') and all(r['buttons']==['A'] for r in schedule if r['start']>=2300) and not any(v for k,v in report.items() if k.startswith('synthetic_'))
    image=NdsImage.open(fixture['research_ROM']);arm=image.read_file('/__arm9__.bin');bank=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;assert sha(arm)==source['current_ARM9_sha256']=='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'
    commands={r['fixture_offset']:r for r in fixture['selected_original_objects']};records={r['fixture_command_offset']:r for r in fixture['original_text_records']};photos={}
    for photo in report['frames_captured']:
        assert sha(Path(photo['path']).read_bytes())==photo['PNG_sha256'];im=Image.open(photo['path']).convert('RGB');assert im.size==(256,384);photos[photo['frame']]=(photo,im)
    pairs=[];observations=[];following=[];last=0;seen=set()
    for row in trace['rows']:
        assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'];s=row['source'];assert s['classification']=='original_SC_cache' and s['route']==2 and s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==sha(bank[s['block']])
        if row['kind']!='after_command':continue
        if s['block']!=22:following.append(dict(frame=row['frame'],block=s['block'],offset=s['instruction_offset'],word=s['first_word'],native_result=row['result_words']));continue
        entry=trace['rows'][row['entry_row']];at=entry['source']['instruction_offset'];seen.add(at);command=commands.get(at);word=entry['source']['first_word']
        if command:
            assert word==command['source_word'] and bank[22][at:at+command['native_extent']].hex()==command['whole_command_hex']
            if word in [0x100,0x200,0x300,0x400]:assert row['decoded_length']==next(r for r in branch['cases'] if r['version']=='current' and r['offset']==command['source_offset'] and r['last_choice_or_result']==last)['native_decoded_extent']
            else:assert row['decoded_length']==command['native_extent']
        pair=dict(fixture_offset=at,source_offset=None if command is None else command['source_offset'],word=word,start=entry['frame'],returned=row['frame'],native_result=row['result_words'],decoded_length=row['decoded_length'],before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed'],UI_after=row['native_UI_request_words']);pairs.append(pair)
        if word==0x8000:assert row['result_words']==[2,0];last=0
        if at in records or word==0x4100:
            r=records.get(at)
            if r is None:r=next(r for r in source['typed_actor_style_records'] if r['command_offset']==command['source_offset'] and 4 in r['style_indices'])
            holds=[p for f,(p,_) in photos.items() if entry['frame']+20<f<row['frame']-4];assert holds
            observations.append(dict(id=r['id'],kind='progressive' if at in records else r['kind'],source_record_index=r.get('source_record_index'),source_selector=r['source_selector'],interval=pair,held_capture_candidates=holds))
    expected=next(r['offsets'] for r in control['two_structural_route_models'] if r['predicate_Boolean_value']==0)
    assert len(pairs)==27 and [p['source_offset'] for p in pairs if p['source_offset'] is not None]==expected and len(observations)==9 and pairs[-1]['native_result']==[0,0]
    assert [r['source_record_index'] for r in observations if r['kind']=='progressive']==[28,31,34,37,40,44,48,56]
    offline=[r['id'] for r in source['records']+source['typed_actor_style_records'] if r['id'] not in {p['id'] for p in observations}];assert len(offline)==8
    dispatch={r['id']:r for r in consumer['speech_and_alternative_dispatch_cases'] if r['version']=='clean-Japanese'};getters={r['actor_ID']:r['current_catalog_name'] for r in consumer['catalog']['rows']};getters[151]='Sailor';native={r['id']:r for r in font['records']};nplanes={r['text']:r for r in names['name_planes']}
    ROOT.mkdir(parents=True);pageobservations=[];nameholds=[];partials=[];transitions=[]
    for panel in observations:
        r=next(r for r in source['records']+source['typed_actor_style_records'] if r['id']==panel['id']);d=dispatch[r['id']];body=bytes.fromhex(next(b['text_hex'] for b in d['boundaries'] if b['kind']=='unexecuted-progressive-body'));assert body.hex()==native[r['id']]['source_body_hex']
        actor=d['resolved_actor_ID'];label=getters[actor];np=nplanes[label];pixels=Path(np['native_plane']).read_bytes();assert sha(pixels)==np['native_plane_sha256'];nink={(i%216,i//216) for i,b in enumerate(pixels) if b};width=np['original_pair_flush_width'];pages=[]
        for page in native[r['id']]['pages']:
            pixels=Path(page['native_plane']).read_bytes();assert sha(pixels)==page['native_plane_sha256'];pages.append(dict(page=page['page'],native_plane=page['native_plane'],native_plane_sha256=page['native_plane_sha256'],ink={(i%216,i//216) for i,b in enumerate(pixels) if b==1},complete_body_holds=[]))
        for photo in panel['held_capture_candidates']:
            frame=photo['frame'];im=photos[frame][1];actual={(x-16,y-296) for y in range(296,360) for x in range(16,232) if im.getpixel((x,y))==(0,8,0)};matched=[p for p in pages if p['ink']==actual]
            if not matched:partials.append(dict(id=r['id'],frame=frame,partial_progressive_or_between_pages=True));continue
            assert len(matched)==1;actualname={(x-16,y-276) for y in range(276,289) for x in range(14,18+width) if im.getpixel((x,y))==(98,97,98)};assert actualname==nink,(r['id'],frame)
            matched[0]['complete_body_holds'].append(dict(frame=frame,capture=photo['path'],sha256=photo['PNG_sha256'],complete_independent_source_black_mask_equal=True))
            nameholds.append(dict(id=r['id'],actor_ID=actor,text=label,frame=frame,capture=photo['path'],sha256=photo['PNG_sha256'],complete_name_and_blank_guards_equal=True))
        for p in pages:
            assert p['complete_body_holds'],(r['id'],p['page']);p.pop('ink');p['selected_capture']=next(p0 for p0 in panel['held_capture_candidates'] if p0['frame']==p['complete_body_holds'][-1]['frame']);pageobservations.append(dict(id=r['id'],**p))
        for before,after in zip(pages,pages[1:]):
            a=before['complete_body_holds'][-1]['frame'];b=after['complete_body_holds'][0]['frame'];inputs=[v for v in schedule if a<v['start']<=b and v['buttons']==['A']];assert a<b and inputs
            transitions.append(dict(id=r['id'],from_page=before['page'],to_page=after['page'],last_complete_previous_frame=a,first_complete_next_frame=b,original_A_inputs_in_interval=inputs,capture_bracket_not_exact_transition_frame=True))
        panel.update(native_pages=len(pages),pages=pages,selected_capture=pages[-1]['selected_capture'],complete_body_holds=[h for p in pages for h in p['complete_body_holds']])
    assert len(pageobservations)==10 and len(transitions)==1 and transitions[0]['id']=='DK4_MES_B223_R0040'
    sheets=[]
    for start in range(0,len(pageobservations),6):
        sheet=Image.new('RGB',(1560,832),'#263238');draw=ImageDraw.Draw(sheet)
        for index,panel in enumerate(pageobservations[start:start+6]):
            photo=panel['selected_capture'];x,y=index%3*520,index//3*416;draw.text((x+4,y+3),panel['id']+' page'+str(panel['page'])+' f'+str(photo['frame']),fill='white');sheet.paste(photos[photo['frame']][1].crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST),(x+4,y+24))
        p=ROOT/f'all_source_pages_sheet{start//6+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    exitframe=pairs[-1]['returned'];after=min(f for f in photos if f>exitframe+60);selected=[observations[0]['selected_capture']['frame'],observations[1]['selected_capture']['frame'],*[p['selected_capture']['frame'] for p in pageobservations if p['id'] in ['DK4_MES_B223_R0040','DK4_MES_B223_R0048']],after,16001];assert len(selected)==7
    sheet=Image.new('RGB',(768,1230),'#263238');draw=ImageDraw.Draw(sheet)
    for index,frame in enumerate(selected):x,y=index%3*256,index//3*410;draw.text((x+3,y+3),'Source f'+str(frame),fill='white');sheet.paste(photos[frame][1],(x,y+24))
    sp=ROOT/'delivery_letter_pages_signature_return_and_final.png';sheet.save(sp);snap=report['read_only_RAM_snapshot'];raw=Path(snap['path']).read_bytes();assert snap['read_only_export'] and len(raw)==4194304 and sha(raw)==snap['sha256']
    save(ROOT/'eight_speeches_one_style_ten_complete_pages27_commands_and_source_return.json',dict(fixture=str(FIXTURE),fixture_sha256=sha(FIXTURE.read_bytes()),research_ROM=fixture['research_ROM'],research_ROM_sha256=fixture['research_ROM_sha256'],speech_observations=observations,actual_page_observations=pageobservations,actual_source_unique_speeches=8,actual_automatic_style_bodies=1,actual_selected_style_index=4,actual_complete_source_pages=10,actual_complete_source_body_holds=sum(len(p['complete_body_holds']) for p in pageobservations),actual_complete_name_holds=nameholds,incomplete_progressive_or_transition_samples=partials,page_transitions=transitions,source_R40_two_pages_advanced_by_original_A_input=True,source_complete_Ian_signature_page_observed=True,offline_only_object_IDs=offline,unvisited_source_speech_IDs=['DK4_MES_B223_R0067','DK4_MES_B223_R0070'],unvisited_original_command_offsets=sorted(commands[a]['source_offset'] for a in set(commands)-seen),command_pairs=pairs,stored_commands=31,visited_commands=27,original_predicate_actual_type2_Boolean0=True,conditional_Cesare_and_Lil_reply_unvisited=True,six_other_automatic_voice_bodies_unvisited=True,all17_stored_objects_not_claimed_as_actual=True,source4500_4621_letter_transitions_observed_not_complete_effect_semantics=True,exit_frame=exitframe,native_terminal_result=pairs[-1]['native_result'],normal_port_sample_frame=after,following_native_commands=following,capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes()),observer_report=str(tp),observer_report_sha256=sha(tp.read_bytes()),input_schedule_sha256=plan['inputs_sha256'],final_snapshot=snap,queried_final_native_state=state(arm,raw),review_sheets=sheets,transition_sheet=dict(path=str(sp),sha256=sha(sp.read_bytes()),frames=selected),Japanese_black_masks_only_no_gray_mask_claim=True,current_English_names_in_Japanese_fixture_not_original_Japanese_name_UI=True,actual_cold_boots=1,total_frames=16001,ordinary_inputs_roster_roles_funds_conditions_RNG_results_RAM_battery_and_savestates_unforced=True,initialized_B22_not_natural_event223_location_earned_progress_full_effects_route_or_hardware=True,all_jobs_terminal_and_reaped=True,visual_review_pending=True,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [FIXTURE,RUN/'terminal.json',RUN/'run_plan.json',FONT,NAMES,CONSUMER,BRANCH,CONTROL,rp,tp,Path(snap['path']),Path(__file__)]},full_goal_complete=False))
    print(dict(speeches=8,selected_notices=1,complete_pages=10,body_holds=sum(len(p['complete_body_holds']) for p in pageobservations),name_holds=len(nameholds),partial_samples=len(partials),page_transitions=len(transitions),commands=27,exit=exitframe,port=after,offline_objects=8,credit=0))
