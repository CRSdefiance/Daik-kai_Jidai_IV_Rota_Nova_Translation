"""Audit paired previous/proposed English scenes; retain every measured late-state limit."""
import inspect
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_shipyard_gameplay_v760 import models
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_followup_gameplay_v778 import tasks
from scripts.verify_ceremony_prayer_gameplay_v814 import calendar
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/retrospective_B218_actual_v7846')
FIXTURES=Path('work/analysis/retrospective_B218_scene_fixtures_v7844/paired_previous_proposed_fixtures_andrunners.json')
STORED=Path('work/analysis/retrospective_B218_stored_controls_v7840/one_changed_stored_plane13_dispatches_A00025_ends_andtwo_sheets_viewed.json')
OLD=Path('work/analysis/lil_B218_stored_v6895/all13_final_stored_targets52_alignments13_complete_pages.json')
NAMES=Path('work/analysis/lil_B218_name_planes_v6883/two_actors_four_getters_six_name_component_planes24_alignments.json')
CONSUMER=Path('work/analysis/lil_B218_consumers_v6876/thirteen_effective_bodies26_dispatches_two_actors_four_name_consumers.json')
TARGET='DK4_MES_B218_R0027'
if __name__=='__main__':
    assert not ROOT.exists()
    fixture_packet,stored,old,names,consumer=map(read,[FIXTURES,STORED,OLD,NAMES,CONSUMER])
    getters={r['actor_ID']:r['text'] for r in consumer['native_four_distinct_name_consumers']['rows'] if r['consumer']=='progressive-nameplate'}
    assert getters=={2:'Lil Argot',21:'Ian Dukov'}
    nameplanes={r['text']:r for r in names['name_planes']}
    oldrows={r['id']:r for r in old['records']}
    ROOT.mkdir(parents=True);groups=[];photo_groups={};final_values=[]
    for fixture in fixture_packet['fixtures']:
        case=fixture['case'];run=Path('work/analysis/retrospective_B218_scene_runs_v7845')/case
        terminal,plan=map(read,[run/'terminal.json',run/'run_plan.json']);cap=Path(plan['capture_folder'])
        rp,tp=cap/'capture_report.json',cap/'observer/commands.json';report,trace=map(read,[rp,tp])
        assert terminal['terminal'] and terminal['observer_host_slots_restored'] and terminal['observer_instances']==1
        assert report['frames']==16001 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not report.get('battery_save_preloaded') and not report['hardware_device_verification'] and not report['goal_complete']
        assert report['ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes())
        assert not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact']
        assert not any(v for k,v in report.items() if k.startswith('synthetic_'))
        assert report['scripted_input_schedule']==read(plan['original_inputs']) and sha(Path(plan['original_inputs']).read_bytes())==plan['inputs_sha256']
        assert plan['explicit_B22_entry_ROM_fixture'] and plan['all15_source_commands_retained'] and plan['source_event218_not_naturally_selected']
        image=NdsImage.open(fixture['research_ROM']);arm=image.read_file('/__arm9__.bin')
        assert sha(arm)=='2b6aaaa499d634be9afc255d1c39b64ef0f578283c9768c525b31e34499abd0a'
        bank=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks
        commands={r['offset']:r for r in fixture['all24_stored_fixture_commands']}
        records={r['fixture_command_offset']:r for r in fixture['original_text_records']}
        photos={}
        for p in report['frames_captured']:
            assert sha(Path(p['path']).read_bytes())==p['PNG_sha256']
            im=Image.open(p['path']).convert('RGB');assert im.size==(256,384);photos[p['frame']]=(p,im)
        photo_groups[case]=photos;pairs=[];panels=[];following=[]
        for row in trace['rows']:
            assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
            s=row['source'];assert s['classification']=='original_SC_cache' and s['route']==2 and s['whole_resident_payload_exact_ROM']
            assert s['actual_sha256']==sha(bank[s['block']])
            if row['kind']!='after_command':continue
            if s['block']!=22:
                following.append(dict(frame=row['frame'],block=s['block'],offset=s['instruction_offset'],word=s['first_word'],native_result=row['result_words']))
                continue
            entry=trace['rows'][row['entry_row']];at=entry['source']['instruction_offset'];command=commands[at]
            assert entry['source']['first_word']==command['word'] and row['decoded_length']==command['native_extent']
            pair=dict(fixture_offset=at,word=command['word'],start=entry['frame'],returned=row['frame'],
                duration=row['frame']-entry['frame'],native_result=row['result_words'],decoded_length=row['decoded_length'],
                before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed'],UI_after=row['native_UI_request_words'])
            pairs.append(pair)
            if at not in records:continue
            r=records[at];ident=r['id']
            page=(stored['changed_stored_pages']['pages'][0] if case=='proposed_English' and ident==TARGET else oldrows[ident]['complete_pages']['pages'][0])
            plane=Path(page['native_plane']).read_bytes();assert len(plane)==216*64 and sha(plane)==page['native_plane_sha256']
            black={(i%216,i//216) for i,b in enumerate(plane) if b==1};gray={(i%216,i//216) for i,b in enumerate(plane) if b==15}
            name=nameplanes[getters[r['source_selector']]];np=Path(name['native_plane']).read_bytes();assert sha(np)==name['native_plane_sha256']
            nink={(i%216,i//216) for i,b in enumerate(np) if b};width=name['original_pair_flush_width']
            holds=[];partial=[]
            for frame,(photo,im) in photos.items():
                if not entry['frame']+20<frame<row['frame']-4:continue
                rgb=list(im.crop((16,296,232,360)).getdata())
                actualblack={(i%216,i//216) for i,b in enumerate(rgb) if b==(0,8,0)}
                actualgray={(i%216,i//216) for i,b in enumerate(rgb) if b==(98,97,98)}
                jpgray={(i%216,i//216) for i,b in enumerate(rgb) if b==(197,198,197)}
                if actualblack!=black or actualgray!=gray or jpgray:
                    partial.append(dict(frame=frame,missing_black=len(black-actualblack),extra_black=len(actualblack-black),
                        missing_gray=len(gray-actualgray),extra_gray=len(actualgray-gray),unexpected_CP932_gray=len(jpgray)))
                    continue
                n=list(im.crop((14,276,18+width,289)).getdata())
                actualname={(i%(width+4)-2,i//(width+4)) for i,p in enumerate(n) if p==(98,97,98)}
                assert actualname==nink,(case,ident,frame)
                holds.append(dict(frame=frame,capture=photo['path'],sha256=photo['PNG_sha256'],
                    complete_native_body_black_gray_andnameplate_masks_equal=True))
            assert holds,(case,ident,'no complete hold',partial)
            panels.append(dict(id=ident,source_selector=r['source_selector'],speaker_name=getters[r['source_selector']],interval=pair,
                complete_body_andheader_holds=holds,incomplete_sampled_body_holds=partial,native_pages=1,
                selected_capture=holds[-1],native_stored_plane=page['native_plane'],native_stored_plane_sha256=page['native_plane_sha256']))
        assert len(pairs)==24 and len(panels)==13 and pairs[-1]['word']==0 and pairs[-1]['native_result'][0]==0
        assert {p['id'] for p in panels}==set(oldrows)
        exit_frame=pairs[-1]['returned'];after=min(f for f in photos if f>exit_frame+60)
        folder=ROOT/case;folder.mkdir();sheets=[]
        for start in range(0,13,6):
            sheet=Image.new('RGB',(1560,832),'#263238');draw=ImageDraw.Draw(sheet)
            for i,panel in enumerate(panels[start:start+6]):
                capture=photos[panel['selected_capture']['frame']][1]
                tile=capture.crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST)
                x,y=i%3*520+4,i//3*416+24;draw.text((x,y-20),panel['id'],fill='white');sheet.paste(tile,(x,y))
            sp=folder/f'complete_panels_sheet{start//6+1}.png';sheet.save(sp);sheets.append(dict(path=str(sp),sha256=sha(sp.read_bytes())))
        frames=[panels[0]['selected_capture']['frame'],panels[-1]['selected_capture']['frame'],after,16001]
        sheet=Image.new('RGB',(1024,410),'#263238');draw=ImageDraw.Draw(sheet)
        for i,frame in enumerate(frames):draw.text((i*256+3,3),case+' frame'+str(frame),fill='white');sheet.paste(photos[frame][1],(i*256,24))
        sp=folder/'first_last_return_final.png';sheet.save(sp)
        snapshot=report['read_only_RAM_snapshot'];raw=Path(snapshot['path']).read_bytes()
        assert snapshot['read_only_export'] and len(raw)==4194304 and sha(raw)==snapshot['sha256']
        cpu,get=get_machine(arm,raw);root=get(0xCB184);assert get(0x7F244)==2
        components={fn.__name__:fn(arm,raw) for fn in [state,models,persistent_objects,tasks,calendar]}
        components['tasks']=dict(bytes=len(components['tasks']),sha256=sha(components['tasks']))
        final_values.append(dict(case=case,snapshot=snapshot,components=components,captain_ID=2,
            whole_actor_sha256=sha(bytes(cpu.mem_read(root,0x1A04))),seed=int.from_bytes(raw[0x168EB8:0x168EBC],'little')))
        groups.append(dict(case=case,research_ROM=fixture['research_ROM'],research_ROM_sha256=fixture['research_ROM_sha256'],
            capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes()),observer_report=str(tp),observer_report_sha256=sha(tp.read_bytes()),
            input_schedule_sha256=plan['inputs_sha256'],actual_unique_speeches=13,actual_complete_pages=13,
            actual_complete_body_andheader_holds=sum(len(p['complete_body_andheader_holds']) for p in panels),
            incomplete_sampled_holds=sum(len(p['incomplete_sampled_body_holds']) for p in panels),
            panels=panels,command_pairs=pairs,exit_frame=exit_frame,normal_port_sample_frame=after,
            normal_terminal_result=pairs[-1]['native_result'],following_native_commands=following,
            unreturned_at_capture_end=trace['unreturned_at_capture_end'],review_sheets=sheets,
            transition_sheet=dict(path=str(sp),sha256=sha(sp.read_bytes())),full_catalogue_UI_unvisited=True))
    a,b=groups;assert a['input_schedule_sha256']==b['input_schedule_sha256']
    semantic=[]
    for pa,pb in zip(a['panels'],b['panels'],strict=True):
        assert pa['id']==pb['id'];ia=photo_groups[a['case']][pa['selected_capture']['frame']][1];ib=photo_groups[b['case']][pb['selected_capture']['frame']][1]
        regions={name:ia.crop(box).tobytes()==ib.crop(box).tobytes() for name,box in [
            ('upper_scene',(0,0,256,192)),('portrait',(0,192,68,266)),('nameplate',(0,272,256,290))]}
        assert all(regions.values()),(pa['id'],regions)
        semantic.append(dict(id=pa['id'],previous_frame=pa['selected_capture']['frame'],proposed_frame=pb['selected_capture']['frame'],**regions))
    comparisons=[]
    for i,(pa,pb) in enumerate(zip(a['command_pairs'],b['command_pairs'],strict=True)):
        assert pa['word']==pb['word']
        comparisons.append(dict(index=i,word=pa['word'],previous=pa,proposed=pb,
            differing_fields=[k for k in pa if pa[k]!=pb[k]]))
    later=[]
    for frame in sorted(set(photo_groups[a['case']])&set(photo_groups[b['case']])):
        if frame<=max(a['exit_frame'],b['exit_frame'])+60:continue
        later.append(dict(frame=frame,whole_RGB_equal=photo_groups[a['case']][frame][1].tobytes()==photo_groups[b['case']][frame][1].tobytes()))
    equality={key:final_values[0]['components'][key]==final_values[1]['components'][key] for key in final_values[0]['components']}
    output=dict(groups=groups,total_actual_pages=26,total_actual_complete_body_andheader_holds=sum(g['actual_complete_body_andheader_holds'] for g in groups),
        total_incomplete_sampled_holds=sum(g['incomplete_sampled_holds'] for g in groups),semantic_upper_portrait_nameplate_pairs=semantic,
        all13_paired_upper_scene_portrait_andnameplate_RGB_equal=True,command_comparisons=comparisons,
        command_difference_rows=sum(bool(c['differing_fields']) for c in comparisons),
        duration_difference_rows=sum(c['previous']['duration']!=c['proposed']['duration'] for c in comparisons),
        all24_original_command_results_andUI_equal=all(c['previous']['native_result']==c['proposed']['native_result'] and c['previous']['UI_after']==c['proposed']['UI_after'] for c in comparisons),
        later_sampled_whole_frame_comparisons=later,later_RGB_differences=sum(not r['whole_RGB_equal'] for r in later),
        final_native_values=final_values,five_native_component_equality=equality,
        final_whole_actor_equal=final_values[0]['whole_actor_sha256']==final_values[1]['whole_actor_sha256'],
        final_PRNG_seeds=[r['seed'] for r in final_values],
        all_measured_timing_RNG_state_actor_calendar_andlater_RGB_differences_preserved=True,
        both_jobs_terminal_andreaped=True,actual_frames=32002,read_only_observer_slots_restored_andcore_files_exact=True,
        previous_andproposed_English_only_no_new_Japanese_capture=True,
        initialized_Amsterdam_original_B22_prelude_not_natural_B218_activation_original_location_fullmechanics_routes_orhardware=True,
        no_every_frame_fullRAM_future_broad_simulation_orcausal_equivalence_claim=True,
        incidental_following_dialogue_not_new_editorial_credit=True,visual_review_pending=True,
        original_final_getter_sources={fn.__name__:inspect.getsource(fn) for fn in [state,models,persistent_objects,tasks,calendar]},
        new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [FIXTURES,STORED,OLD,NAMES,CONSUMER,Path(__file__)]},full_goal_complete=False)
    save(ROOT/'two_English_scenes_complete_masks_commands_andall_measured_late_limits.json',output)
    print('Paired B218 English:',[(g['case'],g['actual_unique_speeches'],g['actual_complete_body_andheader_holds'],g['incomplete_sampled_holds'],g['exit_frame']) for g in groups])
    print('Commands/results/UI equal',output['all24_original_command_results_andUI_equal'],'differences',output['command_difference_rows'],'durations',output['duration_difference_rows'],
        'later RGB',output['later_RGB_differences'],'/',len(later),'components',equality,'actors',output['final_whole_actor_equal'],'seeds',output['final_PRNG_seeds'])
