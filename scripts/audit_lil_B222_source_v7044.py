"""Measure all sixteen original Japanese bodies,current headers and unforced normal return."""
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_name_catalog_glyphs_v278 import raster as old_raster
from scripts.square_shopkeeper_font_oracles_v7020 import expected_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B222_source_actual_v7044')
FIXTURE=Path('work/analysis/lil_B222_source_fixture_v7042/complete_B222_source_B22_fixture.json')
CONSUMER=Path('work/analysis/lil_B222_consumers_v7038/sixteen_effective_bodies32_dispatches_two_actors_four_name_consumers.json')
NAMES=Path('work/analysis/lil_B222_name_planes_v7041/two_actors_four_getters_six_name_component_planes48_alignments.json')
RUN=Path('work/analysis/lil_B222_source_run_v7043')
if __name__=='__main__':
    assert not ROOT.exists();fd,consumer,naming=map(read,[FIXTURE,CONSUMER,NAMES]);fixture=fd['fixtures'][0];source=read(fd['source_context'])
    terminal,plan=read(RUN/'terminal.json'),read(RUN/'run_plan.json');cap=Path(plan['capture_folder']);rp,tp=cap/'capture_report.json',cap/'observer/commands.json';report,trace=read(rp),read(tp)
    assert terminal['terminal'] and terminal['observer_host_slots_restored'] and terminal['observer_instances']==1
    assert report['ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes())
    assert report['frames']==16001 and report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors']
    assert not report['hardware_device_verification'] and not report['goal_complete'] and not any(v for k,v in report.items() if k.startswith('synthetic_'))
    assert plan['explicit_B22_entry_ROM_fixture'] and plan['source_event222_not_naturally_selected'] and plan['all18_source_commands_retained']
    schedule=read(plan['original_inputs']);assert sha(Path(plan['original_inputs']).read_bytes())==plan['inputs_sha256'] and report['scripted_input_schedule']==schedule
    assert [r for r in schedule if r['start']<2300]==read('work/analysis/movie_viewport_v303/lil_start_inputs.json')
    assert all(r['buttons']==['A'] for r in schedule if r['start']>=2300)
    assert not trace['errors'] and trace['mismatches']==0 and not trace['unreturned_at_capture_end'] and trace['all_host_slots_restored_and_core_file_exact']
    image=NdsImage.open(fixture['research_ROM']);arm=image.read_file('/__arm9__.bin');assert sha(arm)==source['current_ARM9_sha256']=='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'
    bank=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;assert bank[22].hex()==fixture['fixture_block_hex']
    commands={r['offset']:r for r in fixture['all27_stored_fixture_commands']};mapped={r['fixture_offset']:r for r in fixture['selected_original_objects']};records={r['fixture_command_offset']:r for r in fixture['original_text_records']}
    getters={r['actor_ID']:r['text'] for r in consumer['native_four_distinct_name_consumers']['rows'] if r['consumer']=='progressive-nameplate'}
    assert getters=={2:'Lil Argot',16:'Gerhard Ardelknatts'};dispatch={r['id']:r for r in consumer['all32_source_current_dispatches'] if r['version']=='clean-Japanese'}
    nameplanes={r['text']:r for r in naming['name_planes']}
    class FontROM:
        @staticmethod
        def open(path):
            assert str(path)=='work/clean.nds';return image
    raster=FunctionType(old_raster.__code__,{**old_raster.__globals__,'NdsImage':FontROM},argdefs=old_raster.__defaults__);raster.__kwdefaults__=old_raster.__kwdefaults__
    captured={}
    for photo in report['frames_captured']:
        assert sha(Path(photo['path']).read_bytes())==photo['PNG_sha256'];im=Image.open(photo['path']).convert('RGB');assert im.size==(256,384);captured[photo['frame']]=(photo,im)
    pairs=[];observations=[];following=[]
    for row in trace['rows']:
        assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'];s=row['source']
        assert s['classification']=='original_SC_cache' and s['route']==2 and s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==sha(bank[s['block']])
        if row['kind']!='after_command':continue
        entry=trace['rows'][row['entry_row']]
        if s['block']!=22:
            following.append(dict(block=s['block'],offset=entry['source']['instruction_offset'],word=s['first_word'],frame=row['frame'],native_result=row['result_words']));continue
        at=entry['source']['instruction_offset'];command=commands[at]
        assert command['word']==s['first_word'] and command['native_extent']==row['decoded_length']
        assert bank[22][at:at+command['native_extent']].hex()==command['whole_command_hex']
        pair=dict(fixture_offset=at,source_offset=mapped.get(at,{}).get('source_offset'),word=command['word'],start=entry['frame'],returned=row['frame'],
            native_result=row['result_words'],decoded_length=row['decoded_length'],before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed'],UI_after=row['native_UI_request_words']);pairs.append(pair)
        if at in records:
            r=records[at];holds=[photo for frame,(photo,_) in captured.items() if entry['frame']+20<frame<row['frame']-4];assert holds
            observations.append(dict(id=r['id'],source_record_index=r['source_record_index'],source_selector=r['source_selector'],interval=pair,selected_capture=holds[-1],held_capture_candidates=holds))
    assert len(pairs)==27 and [p['fixture_offset'] for p in pairs]==list(commands) and len(observations)==16
    assert {p['id'] for p in observations}=={r['id'] for r in source['records']}
    assert pairs[-1]['word']==0 and pairs[-1]['source_offset']==1108 and pairs[-1]['native_result']==[0,0]
    assert next(p for p in pairs if p['source_offset']==1100)['word']==0xA000
    ROOT.mkdir(parents=True);bodycases=[];nameholds=[];partial_total=0
    for panel in observations:
        row=next(r for r in source['records'] if r['id']==panel['id']);body=bytes.fromhex(next(b['text_hex'] for b in dispatch[row['id']]['boundaries'] if b['kind']=='unexecuted-progressive-body'))
        assert body==bytes.fromhex(row['source_hex'])[1:];pixels,events,font=raster(arm,body);assert pixels==expected_pixels(arm,font,events)
        assert [e['code'] for e in events if e['code']!=32]==[c for c in codes(body) if c not in [32,10]]
        assert all(e['y'] in [0,16,32,48] and 0<=e['x'] and e['x']+(6 if e['kind']=='ascii' else 12)<=216 for e in events)
        ink={(i%216,i//216) for i,v in enumerate(pixels) if v==1};name=nameplanes[getters[row['source_selector']]];np=Path(name['native_plane']).read_bytes()
        assert sha(np)==name['native_plane_sha256'];nameink={(i%216,i//216) for i,v in enumerate(np) if v};width=name['original_pair_flush_width'];complete=[];partial=[]
        for photo in panel['held_capture_candidates']:
            im=captured[photo['frame']][1];actual={(x-16,y-296) for y in range(296,360) for x in range(16,232) if im.getpixel((x,y))==(0,8,0)}
            if actual!=ink:partial.append(dict(frame=photo['frame'],missing=len(ink-actual),extra=len(actual-ink)));continue
            actualname={(x-16,y-276) for y in range(276,289) for x in range(14,18+width) if im.getpixel((x,y))==(98,97,98)}
            assert actualname==nameink,(row['id'],photo['frame'],len(nameink-actualname),len(actualname-nameink))
            h=dict(frame=photo['frame'],capture=photo['path'],sha256=photo['PNG_sha256']);complete.append(h);nameholds.append(dict(id=row['id'],actor_ID=row['source_selector'],text=getters[row['source_selector']],**h))
        assert complete and panel['selected_capture']['frame'] in [h['frame'] for h in complete]
        path=ROOT/(row['id']+'_complete_Japanese_native.bin');path.write_bytes(pixels);partial_total+=len(partial)
        bodycases.append(dict(id=row['id'],source_selector=row['source_selector'],source_body_hex=body.hex(),native_events=events,native_plane=str(path),native_plane_sha256=sha(pixels),
            complete_body_holds=complete,incomplete_sampled_holds=partial,Japanese_gray_masks_not_compared=True))
    sheets=[]
    for start in range(0,len(observations),6):
        selected=observations[start:start+6];sheet=Image.new('RGB',(768,820),'#263238');draw=ImageDraw.Draw(sheet)
        for i,panel in enumerate(selected):
            photo=panel['selected_capture'];x,y=i%3*256,i//3*410;draw.text((x+2,y+3),f'B222 R{panel["source_record_index"]} f{photo["frame"]}',fill='white');sheet.paste(captured[photo['frame']][1],(x,y+24))
        path=ROOT/f'six_source_speeches_sheet{start//6+1}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),panes=[p['selected_capture'] for p in selected]))
    exit_frame=pairs[-1]['returned'];after=min(f for f in captured if f>exit_frame+60);summary=Image.new('RGB',(768,410),'#263238');draw=ImageDraw.Draw(summary)
    for i,frame in enumerate([observations[0]['selected_capture']['frame'],after,16001]):
        draw.text((i*256+2,3),f'Source f{frame}',fill='white');summary.paste(captured[frame][1],(i*256,24))
    path=ROOT/'first_silence_normal_return_and_final.png';summary.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    total=sum(len(p['complete_body_holds']) for p in bodycases)
    save(ROOT/'all16_Japanese_speeches27_commands_complete_masks_headers_and_normal_return.json',dict(candidate=fixture['research_ROM'],candidate_sha256=fixture['research_ROM_sha256'],
        fixture=str(FIXTURE),fixture_sha256=sha(FIXTURE.read_bytes()),source_context=fd['source_context'],source_context_sha256=fd['source_context_sha256'],
        run=str(RUN),report=str(rp),report_sha256=sha(rp.read_bytes()),trace=str(tp),trace_sha256=sha(tp.read_bytes()),
        source_speech_observations=observations,command_pairs=pairs,source_complete_native_body_masks=bodycases,complete_name_holds=nameholds,
        actual_unique_source_speeches=16,actual_complete_source_body_holds=total,actual_complete_name_holds=len(nameholds),incomplete_sampled_body_holds=partial_total,
        all27_stored_commands_executed=True,all18_original_source_commands_and9_original_initializers_observed=True,
        normal_terminal_result=pairs[-1]['native_result'],exit_frame=exit_frame,normal_port_sample_frame=after,following_native_commands=following,
        final_RAM_snapshot=report['read_only_RAM_snapshot'],review_sheets=sheets,all_jobs_terminal_and_reaped=True,visual_review_pending=True,
        source_event222_requires89_unforced_and_not_naturally_selected=True,initialized_Amsterdam_not_original_Japan_location_earned_progress_or_full_effects=True,
        current_names_preserved_not_actual_full_catalogue_UI_or_global207_approval=True,no_full_route_hardware_RNG_timing_or_later_world_equivalence_claim=True,
        new_emulator_runs=0,new_review_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [FIXTURE,CONSUMER,NAMES,RUN/'terminal.json',RUN/'run_plan.json',rp,tp,Path(__file__)]},full_goal_complete=False))
    print(dict(unique_source_speeches=16,commands=27,complete_body_holds=total,complete_name_holds=len(nameholds),incomplete_holds=partial_total,normal=pairs[-1]['native_result'],exit_frame=exit_frame,normal_port=after,visual_review_pending=True),flush=True)
