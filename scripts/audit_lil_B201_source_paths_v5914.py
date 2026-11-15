"""Both ordinary Japanese choice paths,all complete source speeches and scene returns."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B201_source_paths_v5914')
FIXTURE=Path('work/analysis/lil_B201_source_fixture_v5910/complete_B201_source_B22_fixture.json')

if __name__=='__main__':
    assert not ROOT.exists();f=read(FIXTURE);fixture=f['fixtures'][0]
    commands={r['fixture_offset']:r for r in fixture['selected_original_objects']}
    records={r['fixture_command_offset']:r for r in fixture['original_text_records']}
    versions=[];photosets={};unique={};all_seen=set();evidence={str(p):sha(p.read_bytes()) for p in [FIXTURE,Path(__file__)]}
    common=[5,8,11,14,18,21,24,27,30,34,37,41,45]
    for case,option,version in [('buy',0,5911),('decline',1,5913)]:
        run=Path(f'work/analysis/lil_B201_source_run_v{version}_{case}')
        terminal,plan=read(run/'terminal.json'),read(run/'run_plan.json');cap=Path(plan['capture_folder'])
        report,trace=read(cap/'capture_report.json'),read(cap/'observer/commands.json')
        assert terminal['terminal'] and terminal['observer_host_slots_restored'] and terminal['observer_instances']==1
        assert report['frames']==13001 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes())
        assert not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact']
        assert all(not v for k,v in report.items() if k.startswith('synthetic_')) and not report.get('battery_save_preloaded')
        assert plan['explicit_B22_entry_ROM_fixture'] and plan['all44_source_commands_retained'] and plan['source_event201_not_naturally_selected']
        schedule=read(plan['original_inputs']);assert sha(Path(plan['original_inputs']).read_bytes())==plan['inputs_sha256'] and report['scripted_input_schedule']==schedule
        assert sum(r['buttons']==['DOWN'] for r in schedule)==option
        photos={}
        for photo in report['frames_captured']:
            p=Path(photo['path']);assert sha(p.read_bytes())==photo['PNG_sha256'];im=Image.open(p).convert('RGB');assert im.size==(256,384)
            photos[photo['frame']]=(photo,im)
        photosets[case]=photos;pairs=[];observations=[]
        for row in trace['rows']:
            assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
            if row['kind']!='after_command' or row['source']['block']!=22:continue
            entry=trace['rows'][row['entry_row']];s=entry['source']
            assert s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==fixture['fixture_block_sha256']
            at=s['instruction_offset'];c=commands.get(at);all_seen.add(at)
            if c:assert row['decoded_length']==c['native_extent'] or c['source_word'] in [0x100,0x200,0x300,0x400]
            pair=dict(fixture_offset=at,source_offset=None if c is None else c['source_offset'],word=s['first_word'],
                start=entry['frame'],returned=row['frame'],native_result=row['result_words'],decoded_length=row['decoded_length'],
                before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed'],UI_after=row['native_UI_request_words']);pairs.append(pair)
            if at in records:
                r=records[at];holds=[photo for frame,(photo,im) in photos.items() if entry['frame']+20<frame<row['frame']-4]
                assert holds,(case,r['id']);chosen=holds[-1]
                observation=dict(id=r['id'],source_record_index=r['source_record_index'],source_selector=r['source_selector'],interval=pair,selected_capture=chosen)
                observations.append(observation);unique.setdefault(r['id'],dict(case=case,observation=observation))
        menus=[p for p in pairs if p['word']==0x2100];assert len(menus)==1 and menus[0]['native_result']==[2,option]
        expected=common+({'buy':[59,62,69,73,77,80],'decline':[86,90,94,97,100]}[case])
        assert [r['source_record_index'] for r in observations]==expected
        assert pairs[-1]['source_offset']==1448 and pairs[-1]['native_result']==[0,option]
        assert pairs[-1]['returned']=={'buy':7895,'decline':7416}[case]
        versions.append(dict(path=case,requested_option=option,actual_choice_result=menus[0]['native_result'],menu_interval=menus[0],
            speech_observations=observations,selected_source_speech_indices=expected,command_pairs=pairs,exit_frame=pairs[-1]['returned'],
            source_effect_offsets_executed=[p['source_offset'] for p in pairs if p['word']==0xA000 and p['source_offset'] is not None],
            source47xx_offsets_executed=[p['source_offset'] for p in pairs if p['word'] in [0x4720,0x4721]],
            capture_report=str(cap/'capture_report.json'),observer_report=str(cap/'observer/commands.json'),input_schedule_sha256=plan['inputs_sha256']))
        for p in [run/'terminal.json',run/'run_plan.json',Path(plan['original_inputs']),cap/'capture_report.json',cap/'observer/commands.json']:
            evidence[str(p)]=sha(p.read_bytes())
    expected_all={r['offset'] for r in fixture['all53_stored_fixture_commands']}
    assert all_seen==expected_all and len(unique)==24
    ROOT.mkdir(parents=True);panels=[]
    for r in fixture['original_text_records']:
        selected=unique[r['id']];o=selected['observation'];im=Image.open(o['selected_capture']['path']).convert('RGB')
        panels.append((selected['case']+' '+r['id'],im.crop((0,192,256,384))))
    sheets=[]
    for start in range(0,len(panels),6):
        sheet=Image.new('RGB',(1560,832),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(label,im) in enumerate(panels[start:start+6]):
            x,y=i%3*520,i//3*416;draw.text((x+4,y+3),label,fill='white');sheet.paste(im.resize((512,384),Image.Resampling.NEAREST),(x+4,y+24))
        p=ROOT/f'complete_Japanese_source_sheet{start//6+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    transitions=[]
    for case in ['buy','decline']:
        v=next(r for r in versions if r['path']==case);last=v['exit_frame'];frames=[6070,6130,6190,next(frame for frame in photosets[case] if frame>last+60),10030,12970]
        sheet=Image.new('RGB',(768,820),'#263238');draw=ImageDraw.Draw(sheet)
        for i,frame in enumerate(frames):
            x,y=i%3*256,i//3*410;photo,im=photosets[case][frame];draw.text((x+3,y+3),case+' frame'+str(frame),fill='white');sheet.paste(im,(x,y+24))
        p=ROOT/f'{case}_menu_selected_highlight_and_return_sailing.png';sheet.save(p);transitions.append(dict(path=str(p),sha256=sha(p.read_bytes()),frames=frames))
    save(ROOT/'two_actual_source_choice_paths_all24_speeches_all53_commands_and_returns.json',dict(
        versions=versions,source_unique_speech_indices=sorted(r['source_record_index'] for r in records.values()),
        source_distinct_speech_observations=24,total_speech_observations=37,unvisited_source_indices=[],
        all44_source_commands_and9_original_initializers_observed_over_two_paths=True,
        all53_stored_fixture_commands=sorted(all_seen),representative_original_speech_panels=list(unique.values()),
        review_sheets=sheets,transition_sheets=transitions,visual_review_pending=True,
        actual_new_cold_boot_runs=2,frames_per_run=13001,total_frames=26002,
        ordinary_inputs_original_roster_funds_conditions_RNG_effect_results_unforced=True,
        initialized_Amsterdam_B22_not_natural_event201_activation_original_location_earned_purchase_or_hardware=True,
        original_CForce_funds35000_below100000_offline_saturating_debit_not_affordability_claim=True,
        existing_item_card_Tireless_Hawser_Equipment_Sail_Handle_not_new_item_title_or_effect_fidelity_credit=True,
        English_localization_native_font_layout_and_registered_release_not_approved=True,
        evidence=evidence,producer_sha256=sha(Path(__file__).read_bytes()),new_editorial_credit=0,full_goal_complete=False))
    print([(v['path'],v['selected_source_speech_indices'],v['exit_frame']) for v in versions]);print('All24 speeches/all53 commands observed in two disclosed source fixtures;four prose/two full-screen sheets await visual review.')
