"""Record three ordinary Japanese choice paths,all24 speeches,four labels and complete returns."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B206_source_paths_v6247');FIXTURE=Path('work/analysis/lil_B206_source_fixture_v6242/complete_B206_source_B22_fixture.json')
if __name__=='__main__':
    assert not ROOT.exists();fixture=read(FIXTURE)['fixtures'][0];commands={r['fixture_offset']:r for r in fixture['selected_original_objects']};records={r['fixture_command_offset']:r for r in fixture['original_text_records']};versions=[];photosets={};unique={};all_seen=set();menu_panels=[];evidence={str(p):sha(p.read_bytes()) for p in [FIXTURE,Path(__file__)]}
    common=[5,9,13,17,20,24,28,32,36,39,42,46,49,53];specs=[('buy',6243,[0,0],common+[68,71,75,90]),('high_price',6245,[0,1],common+[68,71,75,97,100,103,106]),('pitch_refusal',6246,[1],common+[117,120])]
    for case,version,options,expected in specs:
        run=Path(f'work/analysis/lil_B206_source_run_v{version}_{case}');terminal,plan=read(run/'terminal.json'),read(run/'run_plan.json');cap=Path(plan['capture_folder']);report,trace=read(cap/'capture_report.json'),read(cap/'observer/commands.json')
        assert terminal['terminal'] and terminal['observer_host_slots_restored'] and terminal['observer_instances']==1 and report['frames']==16001 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and not report.get('battery_save_preloaded')
        assert report['ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes()) and not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact']
        assert all(not v for k,v in report.items() if k.startswith('synthetic_')) and plan['explicit_B22_entry_ROM_fixture'] and plan['all42_source_commands_retained'] and plan['source_event206_not_naturally_selected']
        schedule=read(plan['original_inputs']);assert sha(Path(plan['original_inputs']).read_bytes())==plan['inputs_sha256'] and report['scripted_input_schedule']==schedule
        down=[r['start'] for r in schedule if r['buttons']==['DOWN']];assert down==({'buy':[],'high_price':[7300],'pitch_refusal':[6300]}[case])
        photos={}
        for photo in report['frames_captured']:
            p=Path(photo['path']);assert sha(p.read_bytes())==photo['PNG_sha256'];im=Image.open(p).convert('RGB');assert im.size==(256,384);photos[photo['frame']]=(photo,im)
        photosets[case]=photos;pairs=[];observations=[];following=[]
        for row in trace['rows']:
            assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
            if row['kind']!='after_command':continue
            if row['source']['block']!=22:following.append(dict(frame=row['frame'],block=row['source']['block'],offset=row['source']['instruction_offset'],word=row['source']['first_word'],native_result=row['result_words']));continue
            entry=trace['rows'][row['entry_row']];s=entry['source'];assert s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==fixture['fixture_block_sha256'];at=s['instruction_offset'];c=commands.get(at);all_seen.add(at)
            if c:assert row['decoded_length']==c['native_extent'] or c['source_word'] in [0x100,0x200,0x300,0x400]
            pair=dict(fixture_offset=at,source_offset=None if c is None else c['source_offset'],word=s['first_word'],start=entry['frame'],returned=row['frame'],native_result=row['result_words'],decoded_length=row['decoded_length'],before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed'],UI_after=row['native_UI_request_words']);pairs.append(pair)
            if at in records:
                r=records[at];holds=[photo for frame,(photo,im) in photos.items() if entry['frame']+20<frame<row['frame']-4];assert holds,(case,r['id']);chosen=holds[-1];o=dict(id=r['id'],source_record_index=r['source_record_index'],source_selector=r['source_selector'],interval=pair,selected_capture=chosen);observations.append(o);unique.setdefault(r['id'],dict(case=case,observation=o))
        menus=[p for p in pairs if p['word']==0x2100];assert [m['native_result'] for m in menus]==[[2,n] for n in options] and [r['source_record_index'] for r in observations]==expected and pairs[-1]['source_offset']==1518 and pairs[-1]['native_result'][0]==0
        menu_holds=[]
        for m in menus:
            holds=[photo for frame,(photo,im) in photos.items() if m['start']+20<frame<m['returned']-4];assert holds;chosen=holds[-1];menu_holds.append(dict(interval=m,selected_capture=chosen));menu_panels.append((case+' choice at source'+str(m['source_offset'])+' result'+str(m['native_result'][1]),Image.open(chosen['path']).convert('RGB').crop((0,192,256,384))))
        snap=report['read_only_RAM_snapshot'];raw=Path(snap['path']).read_bytes();assert snap['read_only_export'] and sha(raw)==snap['sha256'] and len(raw)==4194304;arm=NdsImage.open(fixture['research_ROM']).read_file('/__arm9__.bin');money=state(arm,raw)
        versions.append(dict(path=case,requested_options=options,actual_choice_results=[m['native_result'] for m in menus],menu_intervals=menus,menu_holds=menu_holds,speech_observations=observations,selected_source_speech_indices=expected,command_pairs=pairs,exit_frame=pairs[-1]['returned'],native_end_result=pairs[-1]['native_result'],source_effect_offsets_executed=[p['source_offset'] for p in pairs if p['word']==0xA000 and p['source_offset'] is not None],source47xx_offsets_executed=[p['source_offset'] for p in pairs if p['word'] in [0x4735,0x4720]],following_native_commands=following,following_blocks=sorted({r['block'] for r in following}),capture_report=str(cap/'capture_report.json'),observer_report=str(cap/'observer/commands.json'),input_schedule_sha256=plan['inputs_sha256'],final_snapshot=snap,queried_final_native_state=money,no_causal_or_whole_state_equivalence_claim_from_final_money=True))
        for p in [run/'terminal.json',run/'run_plan.json',Path(plan['original_inputs']),cap/'capture_report.json',cap/'observer/commands.json']:evidence[str(p)]=sha(p.read_bytes())
    expected_all={r['offset'] for r in fixture['all51_stored_fixture_commands']};assert all_seen==expected_all and len(unique)==24 and sum(len(v['speech_observations']) for v in versions)==55 and len(menu_panels)==5
    ROOT.mkdir(parents=True);panels=[]
    for r in fixture['original_text_records']:
        u=unique[r['id']];o=u['observation'];im=Image.open(o['selected_capture']['path']).convert('RGB');panels.append((u['case']+' '+r['id'],im.crop((0,192,256,384))))
    def sheets_for(panels,prefix):
        sheets=[]
        for start in range(0,len(panels),6):
            sheet=Image.new('RGB',(1560,832),'#263238');draw=ImageDraw.Draw(sheet)
            for i,(label,im) in enumerate(panels[start:start+6]):
                x,y=i%3*520,i//3*416;draw.text((x+4,y+3),label,fill='white');sheet.paste(im.resize((512,384),Image.Resampling.NEAREST),(x+4,y+24))
            p=ROOT/f'{prefix}{start//6+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
        return sheets
    sheets=sheets_for(panels,'complete_Japanese_source_sheet');choice_sheets=sheets_for(menu_panels,'original_typed_choice_sheet');transitions=[]
    for case,version,options,expected in specs:
        v=next(r for r in versions if r['path']==case);after=next(frame for frame in photosets[case] if frame>v['exit_frame']+60);frames=[6250,6430]+([7210,7390] if len(options)==2 else [])+[after,16001];sheet=Image.new('RGB',(768,820),'#263238');draw=ImageDraw.Draw(sheet)
        for i,frame in enumerate(frames):
            x,y=i%3*256,i//3*410;photo,im=photosets[case][frame];draw.text((x+3,y+3),case+' frame'+str(frame),fill='white');sheet.paste(im,(x,y+24))
        p=ROOT/f'{case}_original_menus_and_complete_return.png';sheet.save(p);transitions.append(dict(path=str(p),sha256=sha(p.read_bytes()),frames=frames))
    save(ROOT/'three_actual_source_paths_all24_speeches_four_labels_all51_commands_and_returns.json',dict(versions=versions,source_unique_speech_indices=sorted(r['source_record_index'] for r in records.values()),source_distinct_speech_observations=24,total_speech_observations=55,unvisited_source_indices=[],actual_typed_menu_visits=5,actual_distinct_choice_labels=4,all42_source_commands_and9_original_initializers_observed_over_three_paths=True,all51_stored_fixture_commands=sorted(all_seen),representative_original_speech_panels=list(unique.values()),review_sheets=sheets,typed_choice_sheets=choice_sheets,transition_sheets=transitions,visual_review_pending=True,actual_new_cold_boot_runs=3,frames_per_run=16001,total_frames=48003,ordinary_inputs_original_roster_funds_conditions_RNG_effect_results_unforced=True,initialized_Amsterdam_B22_not_natural_event206_activation_original_location_earned_progress_or_hardware=True,source9000_asking_price_does_not_automatically_prove_payment_or_item_effect_semantics=True,cancellation_not_individually_observed_here=True,source_actors_current_nameplates_and_material_term_pending_contextual_editorial_decisions=True,English_localization_native_font_layout_and_registered_release_not_approved=True,evidence=evidence,producer_sha256=sha(Path(__file__).read_bytes()),new_editorial_credit=0,full_goal_complete=False))
    print([(v['path'],v['actual_choice_results'],v['exit_frame'],v['queried_final_native_state']['cash'],v['following_blocks']) for v in versions]);print('All24 source speeches/four labels/all51 commands observed over three unforced paths;four dialogue,one choice and three full-screen sheets await review.')
