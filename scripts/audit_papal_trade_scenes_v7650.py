"""Compare full actual source/English body and name masks, commands and normal returns."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
from scripts.draft_papal_trade_prose_v7631 import CURRENT,CONSUMERS
ROOT=Path('work/analysis/papal_trade_actual_v7650')
FIXTURES=Path('work/analysis/papal_trade_scene_fixtures_v7648/four_complete_source_English_original_route_prelude_fixtures.json')
RUNS=Path('work/analysis/papal_trade_scene_runs_v7649')
JP_FONT=Path('work/analysis/lil_B234_source_pages_v7582/all18_clean_objects_complete_native_CP932_pages_and_exact_consumption.json')
STORED=Path('work/analysis/papal_trade_stored_v7641/all36_stored_targets144_alignments16_zero_ink_tails36_complete_pages.json')
NAMES=Path('work/analysis/papal_trade_name_inputs_v7629/two_routes40_fresh_literal_alignments_five_exact_reused_font_planes.json')
if __name__=='__main__':
    assert not ROOT.exists();fixtures,jpfont,stored,names,current,consumers=map(read,[FIXTURES,JP_FONT,STORED,NAMES,CURRENT,CONSUMERS])
    # Check every job is terminal before producing any audit directory.
    terminals=[]
    for fixture in fixtures['fixtures']:
        folder=RUNS/f"route{fixture['route']}_{fixture['version']}";terminal=read(folder/'terminal.json')
        assert terminal['terminal'] and terminal['frames']==16001 and terminal['all_callbacks_readonly_andhost_slots_restored'];terminals.append((fixture,folder,terminal))
    ROOT.mkdir(parents=True);groups=[]
    for fixture,folder,terminal in terminals:
        route,version=fixture['route'],fixture['version'];rp=Path(terminal['report']);tp=Path(terminal['observer']);report,trace,plan=map(read,[rp,tp,folder/'run_plan.json'])
        assert sha(rp.read_bytes())==terminal['report_sha256'] and sha(tp.read_bytes())==terminal['observer_sha256']
        assert report['frames']==16001 and report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors']
        assert not report['hardware_device_verification'] and not report['goal_complete'] and not any(v for k,v in report.items() if k.startswith('synthetic_'))
        assert sha(Path(fixture['research_ROM']).read_bytes())==fixture['research_ROM_sha256']==report['ROM_sha256']
        assert sha(Path(plan['inputs']).read_bytes())==plan['inputs_sha256'] and report['scripted_input_schedule']==read(plan['inputs'])
        assert not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact']
        image=NdsImage.open(fixture['research_ROM']);banks={r:IlnkContainer.parse(image.read_file(f'/data/SC{r}.DK4')).blocks for r in range(4)}
        cg=current['groups'][route];np={r['text']:r for r in names['groups'][route]['name_planes']}
        getters={r['actor_ID']:r['text'] for r in consumers['groups'][route]['native_four_distinct_name_consumers']['rows'] if r['consumer']=='progressive-nameplate'}
        eng={r['id']:r for r in stored['groups'][route]['records']};sourcefont={r['source_reference']['record_index']:r for r in jpfont['records']}
        objects={r['fixture_command_offset']:(i,r) for i,r in enumerate(fixture['all_original_exchange_commands'])}
        records={r['fixture_command_offset']:r for r in fixture['original_text_records']};expected={c['offset']:c for c in fixture['all_fixture_commands']}
        photos={}
        for p in report['frames_captured']:
            assert sha(Path(p['path']).read_bytes())==p['PNG_sha256'];im=Image.open(p['path']).convert('RGB');assert im.size==(256,384);photos[p['frame']]=(p,im)
        pairs=[];speeches=[];following=[];unidentified=[]
        for ri,row in enumerate(trace['rows']):
            assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'];s=row['source']
            if s['classification']!='original_SC_cache':
                unidentified.append(dict(row=ri,frame=row['frame'],source=s));continue
            assert s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==s['registered_sha256']==sha(banks[s['route']][s['block']])
            if row['kind']!='after_command':continue
            if (s['route'],s['block'])!=(route,fixture['fixture_block']):
                following.append(dict(frame=row['frame'],route=s['route'],block=s['block'],offset=s['instruction_offset'],word=s['first_word'],native_result=row['result_words']));continue
            entry=trace['rows'][row['entry_row']];at=entry['source']['instruction_offset'];command=expected[at]
            assert s['instruction_offset']==at and row['decoded_length']==command['native_extent'] and s['first_word']==command['word']
            ordinal,original=objects.get(at,(None,None))
            pair=dict(fixture_offset=at,exchange_command_ordinal=ordinal,canonical_clean_offset=None if ordinal is None else cg['all_clean_native_commands'][ordinal]['offset'],word=command['word'],start=entry['frame'],returned=row['frame'],decoded_length=row['decoded_length'],native_result=row['result_words'],before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed'],UI_after=row['native_UI_request_words'])
            pairs.append(pair)
            if at not in records:continue
            r=records[at];index=r['source_record_index'];actor=r['source_selector'];name=np[getters[actor]];nameplane=Path(name['native_plane']).read_bytes()
            assert sha(nameplane)==name['native_plane_sha256'];nink={(i%216,i//216) for i,b in enumerate(nameplane) if b}
            if version=='clean_Japanese':
                native=sourcefont[index];src=next(x for x in cg['records'] if x['id']==r['id'])
                assert native['source_body_hex']==bytes.fromhex(src['source_hex'])[1:].hex();pages=native['pages']
            else:pages=eng[r['id']]['complete_pages']['pages']
            assert len(pages)==1;page=pages[0];pixels=Path(page['native_plane']).read_bytes();assert sha(pixels)==page['native_plane_sha256']
            black={(i%216,i//216) for i,b in enumerate(pixels) if b==1};gray={(i%216,i//216) for i,b in enumerate(pixels) if b==15}
            shadow=(197,198,197) if index==5 else (98,97,98);holds=[];partial=[];nameholds=[]
            for frame,(photo,im) in photos.items():
                if not entry['frame']+20<frame<row['frame']-4:continue
                found={(x-16,y-296) for y in range(296,360) for x in range(16,232) if im.getpixel((x,y))==(0,8,0)}
                foundgray={(x-16,y-296) for y in range(296,360) for x in range(16,232) if im.getpixel((x,y))==shadow}
                compare_gray=version=='English' or index==5
                if found!=black or compare_gray and foundgray!=gray:
                    partial.append(dict(frame=frame,missing_black=len(black-found),extra_black=len(found-black),missing_gray=len(gray-foundgray) if compare_gray else None,extra_gray=len(foundgray-gray) if compare_gray else None,sampled_during_progression_not_complete_hold=True));continue
                if index==5:
                    assert len(black)==len(gray)==18 and not any(im.getpixel((x,y))==(98,97,98) for y in range(296,360) for x in range(16,232))
                actualname={(x-16,y-276) for y in range(276,289) for x in range(14,18+name['original_pair_flush_width']) if im.getpixel((x,y))==(98,97,98)}
                assert actualname==nink,(route,version,index,frame,len(nink-actualname),len(actualname-nink))
                h=dict(frame=frame,capture=photo['path'],sha256=photo['PNG_sha256'],native_page=1,complete_independent_native_body_mask_equal=True,gray_compared=compare_gray,body_shadow_RGB=list(shadow) if compare_gray else None)
                holds.append(h);nameholds.append(dict(frame=frame,actor_ID=actor,text=getters[actor],complete_name_first_internal_final_glyphs_andblank_guards_equal=True,capture=photo['path'],sha256=photo['PNG_sha256']))
            assert holds and nameholds,(route,version,index,partial)
            speeches.append(dict(id=r['id'],file_path=fixture['source_file'],source_record_index=index,source_selector=actor,interval=pair,native_page_count=1,native_plane=page['native_plane'],native_plane_sha256=page['native_plane_sha256'],complete_body_holds=holds,complete_name_holds=nameholds,incomplete_sampled_holds=partial,selected_capture=holds[-1],actual_name=getters[actor]))
        assert len(pairs)==len(expected)=={0:30,1:28}[route] and len(speeches)==18 and len({r['id'] for r in speeches})==18
        assert [r['fixture_offset'] for r in pairs]==list(expected) and pairs[-1]['word']==0 and pairs[-1]['native_result']==[0,0]
        assert all((trace['rows'][x['entry_row']]['source'].get('route'),trace['rows'][x['entry_row']]['source'].get('block'))!=(route,fixture['fixture_block']) for x in trace['unreturned_at_capture_end'])
        exitframe=pairs[-1]['returned'];after=min(frame for frame in photos if frame>exitframe+60);sheets=[]
        for start in range(0,18,6):
            sheet=Image.new('RGB',(1560,832),'#263238');draw=ImageDraw.Draw(sheet)
            for i,panel in enumerate(speeches[start:start+6]):
                h=panel['selected_capture'];x,y=i%3*520,i//3*416;draw.text((x+4,y+3),f"{fixture['route_identity']} {version} R{panel['source_record_index']} frame{h['frame']}",fill='white')
                sheet.paste(photos[h['frame']][1].crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST),(x+4,y+24))
            path=ROOT/f'route{route}_{version}_six_complete_speeches_sheet{start//6+1}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
        frames=[speeches[0]['selected_capture']['frame'],speeches[-1]['selected_capture']['frame'],after,16000]
        sheet=Image.new('RGB',(1024,410),'#263238');draw=ImageDraw.Draw(sheet)
        for i,frame in enumerate(frames):draw.text((i*256+3,3),f'{version} frame{frame}',fill='white');sheet.paste(photos[frame][1],(i*256,24))
        path=ROOT/f'route{route}_{version}_first_last_return_final.png';sheet.save(path)
        groups.append(dict(route=route,route_identity=fixture['route_identity'],version=version,fixture=fixture,research_ROM_sha256=fixture['research_ROM_sha256'],capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes()),observer_report=str(tp),observer_report_sha256=sha(tp.read_bytes()),input_schedule_sha256=plan['inputs_sha256'],command_pairs=pairs,speech_observations=speeches,actual_unique_speeches=18,complete_body_holds=sum(len(s['complete_body_holds']) for s in speeches),complete_name_holds=sum(len(s['complete_name_holds']) for s in speeches),incomplete_sampled_holds=sum(len(s['incomplete_sampled_holds']) for s in speeches),exit_frame=exitframe,native_terminal_result=pairs[-1]['native_result'],normal_return_sample_frame=after,following_commands=following,unidentified_trace_rows=unidentified,unreturned_following_dialogues=trace['unreturned_at_capture_end'],review_sheets=sheets,transition_sheet=dict(path=str(path),sha256=sha(path.read_bytes()),frames=frames),visual_review_pending=True,full_catalogue_UI_unvisited=True))
        print(dict(route=route,version=version,speeches=18,complete_body=groups[-1]['complete_body_holds'],complete_headers=groups[-1]['complete_name_holds'],partial=groups[-1]['incomplete_sampled_holds'],commands=len(pairs),exit=exitframe,normal_return=after,unidentified=len(unidentified)))
    for route in [0,1]:
        a,b=[next(g for g in groups if g['route']==route and g['version']==v) for v in ['clean_Japanese','English']]
        assert a['input_schedule_sha256']==b['input_schedule_sha256']
    save(ROOT/'four_complete_scene_captures72_speech_occurrences_exact_body_headers_andnormal_returns.json',dict(groups=groups,total_actual_speech_occurrences=72,distinct_file_qualified_speeches=36,all_four_source_English_runs_original_command_order_andnormal_returns=True,all72_complete_leading_internal_final_body_andname_glyphs_bounds_andone_page_verified=True,all_four_R5_three_ellipsis_black18_lightgray18_masks_exact=True,no_ASCII_shadow_substitution_for_retained_CP932_R5=True,all_jobs_terminal_andreaped=True,all_callbacks_readonly_andhost_slots_restored=True,disclosed_original_route_opening_ROM_fixtures_not_natural_optional_activation_location_earned_progress_full_effects_routes_orhardware=True,source_Japanese_black_masks_except_R5_gray_only_English_full_black_gray_masks=True,visual_review_scene_portrait_comparison_measured_late_state_andrelease_pending=True,evidence={str(p):sha(p.read_bytes()) for p in [FIXTURES,JP_FONT,STORED,NAMES,CURRENT,CONSUMERS,Path(__file__)]},new_credit=0,full_goal_complete=False))
