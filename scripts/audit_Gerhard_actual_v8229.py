"""Measure actual selected paths, complete five-body/three-name masks and normal returns; no natural-route claim."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Gerhard_actual_v8229')
WHOLE=Path('work/analysis/Gerhard_scene_fixtures_v8224/four_complete_parent_revised_SC2_scripts_original_Lil_prelude_fixtures.json')
INTRO=Path('work/analysis/Gerhard_intro_display_fixtures_v8227/two_focused_parent_revised_eight_speech_intro_display_fixtures.json')
MODELS=Path('work/analysis/Gerhard_actual_models_v8226/five_previous_body_planes_revised_exact_reuses_three_header_consumers.json')
COLORS=[(0,8,0),(98,97,98),(197,198,197)]

def body_masks(picture):
    pixels=picture.crop((16,296,232,360)).get_flattened_data()
    return {c:{(i%216,i//216) for i,v in enumerate(pixels) if v==c} for c in COLORS}

def model_masks(page):
    plane=Path(page['native_plane']).read_bytes();assert sha(plane)==page['native_plane_sha256'] and len(plane)==216*64
    assert all(e['kind']=='ascii' for e in page['events'])
    return {COLORS[0]:{(i%216,i//216) for i,v in enumerate(plane) if v==1},
        COLORS[1]:{(i%216,i//216) for i,v in enumerate(plane) if v==15},COLORS[2]:set()}

if __name__=='__main__':
    assert not ROOT.exists();whole,intro,models=map(read,[WHOLE,INTRO,MODELS])
    for sheet in models['review_sheets']:assert sha(Path(sheet['path']).read_bytes())==sheet['sha256']
    ROOT.mkdir(parents=True);groups=[];unresolved=[];evidence={str(p):sha(p.read_bytes()) for p in [WHOLE,INTRO,MODELS,Path(__file__)]}
    jobs=[('whole',f,Path('work/analysis/Gerhard_scene_runs_v8225')/f'route2_B{f["source_block"]}_{f["version"]}') for f in whole['fixtures']]
    jobs += [('intro-display',f,Path('work/analysis/Gerhard_intro_display_runs_v8228')/f'route2_B27_{f["version"]}') for f in intro['fixtures']]
    selected_ids={r['id'] for r in models['native_models']['revised_English']}
    for scope,fixture,folder in jobs:
        version=fixture['version'];number=fixture['source_block'];terminal=read(folder/'terminal.json');rp,tp=Path(terminal['report']),Path(terminal['observer'])
        report,trace,plan=map(read,[rp,tp,folder/'run_plan.json']);expected_frames=32001 if scope=='whole' else 12001
        assert terminal['terminal'] and terminal['frames']==report['frames']==expected_frames and terminal['all_callbacks_readonly_andhost_slots_restored']
        assert sha(rp.read_bytes())==terminal['report_sha256'] and sha(tp.read_bytes())==terminal['observer_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors']
        assert not report['goal_complete'] and not report['hardware_device_verification'] and not any(v for k,v in report.items() if k.startswith('synthetic_'))
        assert report['ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes())
        assert not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact']
        schedule=read(plan['inputs']);assert report['scripted_input_schedule']==schedule and sha(Path(plan['inputs']).read_bytes())==plan['inputs_sha256']
        assert scope=='whole' or plan['focused_intro_display_only_original_outer_condition_andremaining_B27_NOT_executed']
        image=NdsImage.open(fixture['research_ROM']);banks={r:IlnkContainer.parse(image.read_file(f'/data/SC{r}.DK4')).blocks for r in range(4)}
        expected={c['offset']:c for c in fixture['all_fixture_commands']};records={r['fixture_command_offset']:r for r in fixture['original_text_records']}
        objects={r['fixture_command_offset']:r for r in fixture['all_original_exchange_commands']}
        native={r['id']:r for r in models['native_models'][version]};names={r['actor_ID']:r for r in models['name_planes'][version]}
        nameinks={}
        for actor,n in names.items():
            plane=Path(n['native_plane']).read_bytes();assert sha(plane)==n['native_plane_sha256'];nameinks[actor]={(i%216,i//216) for i,v in enumerate(plane) if v}
        photos={}
        for photo in report['frames_captured']:
            path=Path(photo['path']);assert sha(path.read_bytes())==photo['PNG_sha256'];pic=Image.open(path).convert('RGB');assert pic.size==(256,384)
            photos[photo['frame']]=dict(reference=photo,image=pic,masks=body_masks(pic))
        pairs=[];speeches=[];headers=[];following=[];unknown=[];lastnext=None;finished=False;normal=None
        for ri,row in enumerate(trace['rows']):
            assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'];source=row['source']
            if source['classification']!='original_SC_cache':unknown.append(dict(row=ri,frame=row['frame'],source=source,after_return=finished));continue
            assert source['whole_resident_payload_exact_ROM'] and source['actual_sha256']==source['registered_sha256']==sha(banks[source['route']][source['block']])
            if row['kind']!='after_command':continue
            if finished or (source['route'],source['block'])!=(2,22):
                following.append(dict(frame=row['frame'],route=source['route'],block=source['block'],offset=source['instruction_offset'],word=source['first_word'],native_result=row['result_words']));continue
            entry=trace['rows'][row['entry_row']];at=entry['source']['instruction_offset'];command=expected[at];word=command['word'];assert entry['kind']=='before_command'
            assert source['instruction_offset']==at and source['first_word']==word
            for observed in [entry,row]:
                resident=observed['source'];assert resident['route']==2 and resident['block']==22 and resident['actual_sha256']==fixture['fixture_block_sha256']
                assert resident['payload_bytes']==fixture['fixture_stored_bytes'] and resident['instruction_pointer']==resident['payload_address']+at
                assert sha(Path(resident['actual_payload_file']).read_bytes())==fixture['fixture_block_sha256']
            if lastnext is not None:assert at==lastnext
            if word in [0x100,0x200,0x300,0x400]:
                span=int.from_bytes(bytes.fromhex(command['whole_command_hex'])[2:4],'little');previous=entry['mode']
                taken=word==0x100 or word==0x200 and previous==0 or word==0x300 and previous==1 or word==0x400 and previous==2
                assert row['decoded_length']==4+(span if taken else 0)
            else:assert row['decoded_length']==command['native_extent']
            lastnext=at+row['decoded_length'];original=objects.get(at)
            pair=dict(fixture_offset=at,canonical_source_offset=None if original is None else original['canonical_clean_offset'],
                source_command_ordinal=None if original is None else original['source_command_ordinal'],word=word,start=entry['frame'],returned=row['frame'],duration=row['frame']-entry['frame'],
                entry_row=row['entry_row'],return_row=ri,decoded_length=row['decoded_length'],observed_previous_result=entry['mode'],native_result=row['result_words'],
                before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed'],UI_before=entry['native_UI_request_words'],UI_after=row['native_UI_request_words'])
            pairs.append(pair)
            if word==0:
                assert row['result_words']==[0,pairs[-2]['native_result'][1]];finished=True;normal=dict(frame=row['frame'],native_result=row['result_words'],complete_four_byte_end=True)
            if at not in records:continue
            record=records[at];actor=record['source_selector'];candidate_photos=[(frame,p) for frame,p in photos.items() if entry['frame']+20<frame<row['frame']-4]
            nameholds=[];namepartials=[]
            if actor in names and (actor==16 or record['id'] in selected_ids):
                n=names[actor];ink=nameinks[actor]
                for frame,photo in candidate_photos:
                    found={(x-16,y-276) for y in range(276,289) for x in range(14,18+n['original_pair_flush_width']) if photo['image'].getpixel((x,y))==COLORS[1]}
                    if found==ink:nameholds.append(dict(frame=frame,capture=photo['reference']['path'],sha256=photo['reference']['PNG_sha256'],complete_first_internal_final_name_glyphs=True))
                    else:namepartials.append(dict(frame=frame,missing=len(ink-found),extra=len(found-ink)))
                if not nameholds:unresolved.append(dict(scope=scope,version=version,block=number,id=record['id'],kind='no-complete-relevant-name-hold',partial=namepartials))
                headers.append(dict(id=record['id'],actor_ID=actor,name=n['text'],holds=nameholds,partial_ortransition_samples=namepartials,all_complete_holds_match_native=True))
            if record['id'] not in selected_ids:
                speeches.append(dict(id=record['id'],source_selector=actor,changed_body=False,start=entry['frame'],returned=row['frame'],complete_body_ink_not_reaudited=True));continue
            model=native[record['id']];assert len(model['pages'])==1;expected_masks=model_masks(model['pages'][0]);holds=[];partial=[]
            for frame,photo in candidate_photos:
                diffs={str(c):len(photo['masks'][c]^expected_masks[c]) for c in COLORS}
                if any(diffs.values()):partial.append(dict(frame=frame,differences=diffs,not_counted_as_complete=True));continue
                if frame not in {h['frame'] for h in nameholds}:unresolved.append(dict(scope=scope,version=version,block=number,id=record['id'],frame=frame,kind='complete-body-without-complete-name'));continue
                holds.append(dict(frame=frame,capture=photo['reference']['path'],sha256=photo['reference']['PNG_sha256'],native_page=1,
                    all_black_gray_first_internal_final_glyph_masks_andname_exact=True,actual_name=names[actor]['text']))
            if not holds:unresolved.append(dict(scope=scope,version=version,block=number,id=record['id'],kind='no-complete-corrected-body-hold',partial=partial))
            speeches.append(dict(id=record['id'],source_selector=actor,changed_body=True,start=entry['frame'],returned=row['frame'],pages=1,complete_holds=holds,
                partial_ortransition_samples=partial,selected_capture=holds[0] if holds else None,all_original_words_complete_not_shortened=True))
        assert finished and normal and not unknown
        ids=[r['id'] for r in speeches];assert len(ids)==len(set(ids))
        missing=[r['id'] for r in fixture['original_text_records'] if r['id'] not in ids]
        if scope=='whole' and number==27:assert len(speeches)==35 and all(i not in ids for i in ['DK4_MES_B27_R0091','DK4_MES_B27_R0094']) and len(missing)==16
        elif scope=='whole':assert number==74 and len(speeches)==75 and len(missing)==4 and {i for i in ids if i in selected_ids}=={'DK4_MES_B74_R0060','DK4_MES_B74_R0185','DK4_MES_B74_R0260'}
        else:assert len(speeches)==8 and not missing and {i for i in ids if i in selected_ids}=={'DK4_MES_B27_R0091','DK4_MES_B27_R0094'}
        for p in [folder/'terminal.json',folder/'run_plan.json',rp,tp]:evidence[str(p)]=sha(p.read_bytes())
        groups.append(dict(scope=scope,version=version,block=number,fixture=fixture,terminal=str(folder/'terminal.json'),actual_frames=expected_frames,
            command_pairs=pairs,speeches=speeches,relevant_header_observations=headers,normal_return=normal,unvisited_conditional_text_IDs=missing,
            following_original_cache_commands=following,unknown_sources=unknown,all_selected_command_boundaries_follow_native_relative_results=True,
            all_selected_payloads_exact_own_fixture_ROM_andall_callbacks_readonly=True,all_unselected_conditions_preserved_inwhole_script=True,
            conditional_membership_not_proved_by_intro_display_slice=scope=='intro-display',capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes())))
        print('ACTUAL',scope,number,version,'speeches',len(speeches),'changed',sum(r['changed_body'] for r in speeches),'headers',len(headers),'normal',normal,'unvisited',len(missing),flush=True)
    revised_ids={s['id'] for g in groups if g['version']=='revised_English' for s in g['speeches'] if s['changed_body']};assert revised_ids==selected_ids
    comparisons=[];sheets=[]
    for scope,number in [('whole',27),('whole',74),('intro-display',27)]:
        a=next(g for g in groups if g['scope']==scope and g['block']==number and g['version']=='parent_English');b=next(g for g in groups if g['scope']==scope and g['block']==number and g['version']=='revised_English')
        assert [(r['source_command_ordinal'],r['word']) for r in a['command_pairs']]==[(r['source_command_ordinal'],r['word']) for r in b['command_pairs']]
        assert [r['native_result'] for r in a['command_pairs']]==[r['native_result'] for r in b['command_pairs']]
        assert [r['id'] for r in a['speeches']]==[r['id'] for r in b['speeches']] and a['unvisited_conditional_text_IDs']==b['unvisited_conditional_text_IDs']
        rows=[]
        for x,y in zip(a['command_pairs'],b['command_pairs'],strict=True):
            rows.append(dict(canonical_source_offset=x['canonical_source_offset'],word=x['word'],parent_start=x['start'],revised_start=y['start'],
                parent_returned=x['returned'],revised_returned=y['returned'],parent_duration=x['duration'],revised_duration=y['duration'],
                results_equal=x['native_result']==y['native_result'],UI_before_equal=x['UI_before']==y['UI_before'],UI_after_equal=x['UI_after']==y['UI_after'],
                parent_before_RNG=x['before_RNG'],revised_before_RNG=y['before_RNG'],parent_after_RNG=x['after_RNG'],revised_after_RNG=y['after_RNG']))
        comparisons.append(dict(scope=scope,block=number,commands=rows,all_selected_results_andtext_membership_equal=True,
            duration_differences=sum(r['parent_duration']!=r['revised_duration'] for r in rows),UI_before_differences=sum(not r['UI_before_equal'] for r in rows),
            UI_after_differences=sum(not r['UI_after_equal'] for r in rows),parent_normal_return=a['normal_return'],revised_normal_return=b['normal_return']))
        for old in [s for s in a['speeches'] if s['changed_body']]:
            new=next(s for s in b['speeches'] if s['id']==old['id']);oldphoto,newphoto=old['selected_capture'],new['selected_capture']
            if oldphoto is None or newphoto is None:continue
            sheet=Image.new('RGB',(976,300),'#263238');draw=ImageDraw.Draw(sheet)
            for n,(version,photo) in enumerate([('previous',oldphoto),('revised',newphoto)]):
                path=Path(photo['capture']);assert sha(path.read_bytes())==photo['sha256'];pic=Image.open(path).convert('RGB')
                draw.text((n*488+4,4),old['id']+' '+version+f' actual frame{photo["frame"]}',fill='white')
                sheet.paste(pic.crop((8,256,248,384)).resize((480,256),Image.Resampling.NEAREST),(n*488+4,28))
            path=ROOT/(old['id']+'_actual_previous_revised.png');sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes()),id=old['id']))
    result=dict(groups=groups,comparisons=comparisons,unresolved=unresolved,complete_changed_body_IDs_revised=sorted(revised_ids),
        complete_changed_body_pages_revised=5,actual_changed_body_observations_both_versions=sum(s['changed_body'] for g in groups for s in g['speeches']),
        complete_body_holds=sum(len(s.get('complete_holds',[])) for g in groups for s in g['speeches']),
        relevant_name_holds=sum(len(h['holds']) for g in groups for h in g['relevant_header_observations']),
        directly_viewed_native_model_sheets=models['review_sheets'],native_model_sheets_viewed=True,actual_review_sheets=sheets,actual_visual_review_pending=True,
        actual_full_script_scopes=dict(B27_selected35_of51_original_conditions_preserved=True,B74_selected75_of79_original_conditions_preserved=True),
        additional_B27_intro_display8_of8_is_not_full_branch_controlflow_ornatural_activation=True,
        all5_changed_bodies_complete_native_masks_inactual_UI_across_full_andfocused_scopes=not unresolved,
        actual_same_controller_schedule_no_retiming_both_English_versions=True,
        no_battery_savestate_runtime_RAM_code_flags_roster_roles_funds_RNG_orresults_forced=True,
        original_source_full_context_andall_control_inverses_are_separate_offline_evidence=True,
        original_Hamburg_choice_selected_option0_only_option1_individual_actual_coverage_not_claimed=True,
        no_natural_event_location_earned_progress_fullroute_hardware_orbroad_simulation_equivalence_claim=True,
        all6_runs_terminal_andreaped=True,new_emulator_runs=6,new_actual_frames=152006,new_credit=0,full_goal_complete=False,evidence=evidence)
    save(ROOT/'six_paired_runs_actual_five_surname_bodies_headers_conditions_andnormal_returns.json',result)
    print('Actual changed-body holds',result['complete_body_holds'],'nameholds',result['relevant_name_holds'],'unresolved',len(unresolved),'visual review pending',flush=True)
    if unresolved:raise SystemExit(1)
