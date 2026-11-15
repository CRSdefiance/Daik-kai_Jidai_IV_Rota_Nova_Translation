"""Bind both ordinary source choices, all source bodies and complete current headers."""
from pathlib import Path
from types import FunctionType
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_name_catalog_glyphs_v278 import raster as old_raster
from scripts.Al_Ferid_font_oracles_v6520 import expected_pixels
from scripts.prove_lil_B208_name_planes_v6405 import codes
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B221_source_actual_v6988')
FIXTURE=Path('work/analysis/lil_B221_source_fixture_v6978/complete_B221_source_B22_fixture.json')
CONSUMER=Path('work/analysis/lil_B221_consumers_v6968/fourteen_effective_bodies28_dispatches_three_actors_six_name_consumers.json')
NAMES=Path('work/analysis/lil_B221_name_planes_v6981/three_actors_six_getters_nine_name_component_planes36_alignments.json')
BRANCHES=Path('work/analysis/lil_B221_branches_v6970/original_relative_skip_operand_proof.json')
RUNS=[(0,Path('work/analysis/lil_B221_source_run_v6979')),
      (1,Path('work/analysis/lil_B221_source_run_v6979c'))]

if __name__=='__main__':
    assert not ROOT.exists()
    fd,consumer,naming,branches=map(read,[FIXTURE,CONSUMER,NAMES,BRANCHES])
    fixture=fd['fixtures'][0];source=read(fd['source_context'])
    image=NdsImage.open(fixture['research_ROM']);arm=image.read_file('/__arm9__.bin')
    bank=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
    assert sha(Path(fixture['research_ROM']).read_bytes())==fixture['research_ROM_sha256']
    commands={r['fixture_offset']:r for r in fixture['selected_original_objects']}
    records={r['fixture_command_offset']:r for r in fixture['original_text_records']}
    dispatch={r['id']:r for r in consumer['all28_source_current_dispatches'] if r['version']=='clean-Japanese'}
    getters={r['actor_ID']:r['text'] for r in consumer['native_six_distinct_name_consumers']['rows'] if r['consumer']=='progressive-nameplate'}
    nameplanes={r['text']:r for r in naming['name_planes']}
    assert getters=={2:'Lil Argot',17:'Al Shin',85:'Square Shopkeeper'}
    class FontROM:
        @staticmethod
        def open(path):
            assert str(path)=='work/clean.nds'
            return image
    raster=FunctionType(old_raster.__code__,{**old_raster.__globals__,'NdsImage':FontROM},argdefs=old_raster.__defaults__)
    raster.__kwdefaults__=old_raster.__kwdefaults__
    ROOT.mkdir(parents=True);versions=[];evidence=[FIXTURE,CONSUMER,NAMES,BRANCHES,Path(__file__)]
    all_ids=set();all_source_offsets=set();total_body_holds=total_name_holds=total_partial=0
    for selected,RUN in RUNS:
        terminal,plan=read(RUN/'terminal.json'),read(RUN/'run_plan.json')
        cap=Path(plan['capture_folder']);rp,tp=cap/'capture_report.json',cap/'observer/commands.json'
        report,trace=read(rp),read(tp)
        assert terminal['terminal'] and terminal['observer_host_slots_restored'] and terminal['observer_instances']==1
        assert report['frames']==16001 and report['cold_boot'] and not report['savestate_loaded']
        assert not report['callback_errors'] and not report.get('battery_save_preloaded')
        assert not report['hardware_device_verification'] and not report['goal_complete']
        assert report['ROM_sha256']==fixture['research_ROM_sha256']
        assert not trace['errors'] and trace['mismatches']==0 and not trace['unreturned_at_capture_end']
        assert trace['all_host_slots_restored_and_core_file_exact']
        assert plan['explicit_B22_entry_ROM_fixture'] and plan['all21_source_commands_retained'] and plan['source_event221_not_naturally_selected']
        schedule=read(plan['original_inputs'])
        assert sha(Path(plan['original_inputs']).read_bytes())==plan['inputs_sha256'] and report['scripted_input_schedule']==schedule
        assert [r for r in schedule if r['start']<2300]==read('work/analysis/movie_viewport_v303/lil_start_inputs.json')
        later=[r for r in schedule if r['start']>=2300]
        assert [r for r in later if r['buttons']!=['A']]==([] if selected==0 else [dict(start=3700,duration=5,buttons=['DOWN'])])
        assert not any(v for k,v in report.items() if k.startswith('synthetic_'))
        photos={}
        for photo in report['frames_captured']:
            assert sha(Path(photo['path']).read_bytes())==photo['PNG_sha256']
            im=Image.open(photo['path']).convert('RGB');assert im.size==(256,384)
            photos[photo['frame']]=(photo,im)
        pairs=[];observations=[];following=[]
        for row in trace['rows']:
            assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
            s=row['source'];assert s['classification']=='original_SC_cache' and s['route']==2 and s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==sha(bank[s['block']])
            if row['kind']!='after_command':continue
            if s['block']!=22:
                following.append(dict(frame=row['frame'],block=s['block'],offset=s['instruction_offset'],word=s['first_word'],native_result=row['result_words']))
                continue
            entry=trace['rows'][row['entry_row']];at=entry['source']['instruction_offset']
            command=commands.get(at);word=entry['source']['first_word']
            if command:
                assert word==command['source_word'];expected=command['native_extent']
                if word in [0x100,0x200,0x300]:
                    b=next(b for b in branches['cases'] if b['version']=='clean' and b['offset']==command['source_offset'] and b['last_choice_or_result']==selected)
                    expected=b['native_decoded_extent']
                assert row['decoded_length']==expected,(selected,at,word,row['decoded_length'],expected)
                all_source_offsets.add(command['source_offset'])
            pair=dict(fixture_offset=at,source_offset=None if command is None else command['source_offset'],word=word,
                start=entry['frame'],returned=row['frame'],native_result=row['result_words'],decoded_length=row['decoded_length'],
                before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed'],UI_after=row['native_UI_request_words'])
            pairs.append(pair)
            if at in records:
                record=records[at];holds=[photo for frame,(photo,_) in photos.items() if entry['frame']+20<frame<row['frame']-4]
                assert holds
                observations.append(dict(id=record['id'],source_record_index=record['source_record_index'],source_selector=record['source_selector'],
                    interval=pair,selected_capture=holds[-1],held_capture_candidates=holds))
        assert len(pairs)==[27,28][selected] and len(observations)==13
        expected_ids={r['id'] for r in source['records']}-{f'DK4_MES_B221_R{33 if selected==0 else 27:04d}'}
        assert {r['id'] for r in observations}==expected_ids
        all_ids.update(expected_ids)
        choice=next(p for p in pairs if p['word']==0x2100)
        assert choice['source_offset']==150 and choice['native_result']==[2,selected]
        assert pairs[-1]['word']==0 and pairs[-1]['native_result']==[0,selected]
        menu_holds=[photos[f][0] for f in [3610,3670,3730,3790] if choice['start']+20<f<choice['returned']-4]
        assert len(menu_holds)==4
        version_root=ROOT/f'choice{selected}';version_root.mkdir()
        bodycases=[];nameholds=[]
        for panel in observations:
            row=next(r for r in source['records'] if r['id']==panel['id'])
            body=bytes.fromhex(next(b['text_hex'] for b in dispatch[row['id']]['boundaries'] if b['kind']=='unexecuted-progressive-body'))
            assert body==bytes.fromhex(row['source_hex'])[1:]
            pixels,events,font=raster(arm,body)
            assert pixels==expected_pixels(arm,font,events)
            assert [e['code'] for e in events if e['code']!=32]==[c for c in codes(body) if c not in [32,10]]
            assert all(e['y'] in [0,16,32,48] and 0<=e['x'] and e['x']+(6 if e['kind']=='ascii' else 12)<=216 for e in events)
            ink={(i%216,i//216) for i,b in enumerate(pixels) if b==1}
            complete=[];partial=[];name=nameplanes[getters[row['source_selector']]]
            plane=Path(name['native_plane']).read_bytes();assert sha(plane)==name['native_plane_sha256']
            nameink={(i%216,i//216) for i,b in enumerate(plane) if b};width=name['original_pair_flush_width']
            for photo in panel['held_capture_candidates']:
                im=photos[photo['frame']][1]
                found={(x-16,y-296) for y in range(296,360) for x in range(16,232) if im.getpixel((x,y))==(0,8,0)}
                if found!=ink:
                    partial.append(dict(frame=photo['frame'],missing=len(ink-found),extra=len(found-ink),incomplete_progressive_hold=True));continue
                complete.append(dict(frame=photo['frame'],capture=photo['path'],sha256=photo['PNG_sha256'],complete_independent_source_black_mask_equal=True))
                actualname={(x-16,y-276) for y in range(276,289) for x in range(14,18+width) if im.getpixel((x,y))==(98,97,98)}
                assert actualname==nameink,(selected,row['id'],photo['frame'],len(nameink-actualname),len(actualname-nameink))
                nameholds.append(dict(id=row['id'],actor_ID=row['source_selector'],text=getters[row['source_selector']],frame=photo['frame'],capture=photo['path'],sha256=photo['PNG_sha256'],complete_name_and_blank_guards_equal=True))
            assert complete and panel['selected_capture']['frame'] in [h['frame'] for h in complete]
            bp=version_root/(row['id']+'_Japanese_complete_native.bin');bp.write_bytes(pixels)
            bodycases.append(dict(id=row['id'],source_selector=row['source_selector'],expanded_source_body_hex=body.hex(),native_events=events,
                native_plane=str(bp),native_plane_sha256=sha(pixels),complete_body_holds=complete,incomplete_progressive_holds=partial,source_gray_pixel_masks_not_compared=True))
        sheets=[]
        for start in range(0,len(observations),6):
            sheet=Image.new('RGB',(1560,832),'#263238');draw=ImageDraw.Draw(sheet)
            for index,panel in enumerate(observations[start:start+6]):
                photo=panel['selected_capture'];x,y=index%3*520,index//3*416
                draw.text((x+4,y+3),panel['id']+' choice'+str(selected)+' frame'+str(photo['frame']),fill='white')
                sheet.paste(photos[photo['frame']][1].crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST),(x+4,y+24))
            path=version_root/f'six_Japanese_speeches_sheet{start//6+1}.png';sheet.save(path)
            sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
        exit_frame=pairs[-1]['returned'];after=min(f for f in photos if f>exit_frame+60)
        fullframes=[3730,next(p['selected_capture']['frame'] for p in observations if p['source_record_index']==[27,33][selected]),after,16001]
        sheet=Image.new('RGB',(1024,410),'#263238');draw=ImageDraw.Draw(sheet)
        for index,frame in enumerate(fullframes):
            draw.text((index*256+3,3),'Source choice'+str(selected)+' frame'+str(frame),fill='white');sheet.paste(photos[frame][1],(index*256,24))
        sp=version_root/'menu_branch_normal_return_and_final.png';sheet.save(sp)
        snap=report['read_only_RAM_snapshot'];raw=Path(snap['path']).read_bytes()
        assert snap['read_only_export'] and len(raw)==4194304 and sha(raw)==snap['sha256']
        body_holds=sum(len(r['complete_body_holds']) for r in bodycases)
        partial=sum(len(r['incomplete_progressive_holds']) for r in bodycases)
        total_body_holds+=body_holds;total_name_holds+=len(nameholds);total_partial+=partial
        versions.append(dict(selected_original_option=selected,run=str(RUN),source_speech_observations=observations,
            source_body_masks=bodycases,actual_complete_source_body_holds=body_holds,actual_complete_name_holds=nameholds,
            incomplete_sampled_body_holds=partial,command_pairs=pairs,choice_interval=choice,menu_held_captures=menu_holds,
            branch_source_record_index=[27,33][selected],native_terminal_result=pairs[-1]['native_result'],exit_frame=exit_frame,
            normal_port_sample_frame=after,following_native_commands=following,
            capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes()),observer_report=str(tp),observer_report_sha256=sha(tp.read_bytes()),
            input_schedule_sha256=plan['inputs_sha256'],final_snapshot=snap,queried_final_native_state=state(arm,raw),
            review_sheets=sheets,transition_sheet=dict(path=str(sp),sha256=sha(sp.read_bytes()),frames=fullframes),
            current_English_names_in_Japanese_content_fixture_not_original_Japanese_name_UI=True))
        evidence.extend([RUN/'terminal.json',RUN/'run_plan.json',Path(plan['original_inputs']),rp,tp,Path(snap['path'])])
    assert len(all_ids)==14 and all_source_offsets=={r['source_offset'] for r in fixture['selected_original_objects']}
    save(ROOT/'two_source_choices_all14_speeches_all30_commands_complete_bodies_names_and_returns.json',dict(
        fixture=str(FIXTURE),fixture_sha256=sha(FIXTURE.read_bytes()),versions=versions,
        actual_source_unique_speeches=14,actual_speech_observations=26,
        actual_complete_source_body_holds=total_body_holds,actual_complete_name_holds=total_name_holds,
        incomplete_sampled_body_holds=total_partial,all21_source_and9_initializer_commands_observed_in_union=True,
        all30_stored_commands_executed_in_union=True,unvisited_source_speech_IDs=[],unvisited_original_command_offsets=[],
        Yes_native0_leads_R27_No_native1_leads_R33=True,
        all4_source_relative_sites_observed_with_original_choice_values=True,
        two_normal_ends_preserve_existing_value_words0_1=True,
        source_Japanese_black_masks_and_current_English_names_complete=True,
        Japanese_gray_masks_and_menu_glyph_pixel_masks_not_claimed=True,
        both_visible_menu_associations_and_source_sheets_need_visual_review=True,
        English_body_and_two_page_button_progression_unvisited=True,
        actual_new_cold_boot_runs=2,total_frames=32002,all_jobs_terminal_and_reaped=True,
        failed_input_case='work/analysis/lil_B221_source_run_v6979b',failed_input_case_excluded_from_complete_coverage=True,
        ordinary_controller_choices_not_forced_results_predicates_roster_funds_RNG_or_RAM=True,
        initialized_B22_not_natural_event221_original_location_earned_progress_full_effects_full_route_or_hardware=True,
        all207_names_and_separate_wider_Shopkeeper_asset_layer_remain_pending=True,
        no_new_editorial_credit=True,visual_review_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in evidence},full_goal_complete=False))
    print(dict(unique_source_speeches=14,speech_observations=26,commands_union=30,
        complete_source_body_holds=total_body_holds,complete_current_name_holds=total_name_holds,
        partial_body_holds=total_partial,choices=[v['choice_interval']['native_result'] for v in versions],
        normal_ends=[v['native_terminal_result'] for v in versions],credit=0))
