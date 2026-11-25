"""Bind the complete12-panel source run to all23 fixture commands and observed returns."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B211_source_actual_v6561')
FIXTURE=Path('work/analysis/lil_B211_source_fixture_v6555/complete_B211_source_B22_fixture.json')
RUN=Path('work/analysis/lil_B211_source_run_v6556')
if __name__=='__main__':
    assert not ROOT.exists();fixture=read(FIXTURE)['fixtures'][0];terminal,plan=read(RUN/'terminal.json'),read(RUN/'run_plan.json');cap=Path(plan['capture_folder']);rp,tp=cap/'capture_report.json',cap/'observer/commands.json';report,trace=read(rp),read(tp)
    assert terminal['terminal'] and terminal['observer_host_slots_restored'] and terminal['observer_instances']==1 and report['frames']==16001 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and not report.get('battery_save_preloaded')
    assert report['ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes()) and not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact']
    assert not any(v for k,v in report.items() if k.startswith('synthetic_')) and plan['explicit_B22_entry_ROM_fixture'] and plan['all14_source_commands_retained'] and plan['source_event211_not_naturally_selected']
    schedule=read(plan['original_inputs']);assert sha(Path(plan['original_inputs']).read_bytes())==plan['inputs_sha256'] and report['scripted_input_schedule']==schedule and not any(r['buttons']==['DOWN'] for r in schedule)
    image=NdsImage.open(fixture['research_ROM']);bank=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;commands={r['fixture_offset']:r for r in fixture['selected_original_objects']};records={r['fixture_command_offset']:r for r in fixture['original_text_records']};photos={};evidence={str(p):sha(p.read_bytes()) for p in [FIXTURE,RUN/'terminal.json',RUN/'run_plan.json',Path(plan['original_inputs']),rp,tp,Path(__file__)]}
    for r in report['frames_captured']:
        p=Path(r['path']);assert sha(p.read_bytes())==r['PNG_sha256'];im=Image.open(p).convert('RGB');assert im.size==(256,384);photos[r['frame']]=(r,im)
    pairs=[];observations=[];following=[];seen=set()
    for row in trace['rows']:
        assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'];s=row['source'];assert s['classification']=='original_SC_cache' and s['route']==2 and s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==sha(bank[s['block']])
        if row['kind']!='after_command':continue
        if s['block']!=22:following.append(dict(frame=row['frame'],block=s['block'],offset=s['instruction_offset'],word=s['first_word'],native_result=row['result_words']));continue
        entry=trace['rows'][row['entry_row']];at=entry['source']['instruction_offset'];seen.add(at);c=commands.get(at)
        if c:assert row['decoded_length']==c['native_extent'] and entry['source']['first_word']==c['source_word']
        pair=dict(fixture_offset=at,source_offset=None if c is None else c['source_offset'],word=entry['source']['first_word'],start=entry['frame'],returned=row['frame'],native_result=row['result_words'],decoded_length=row['decoded_length'],before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed'],UI_after=row['native_UI_request_words']);pairs.append(pair)
        if at in records:
            r=records[at];holds=[photo for frame,(photo,im) in photos.items() if entry['frame']+20<frame<row['frame']-4];assert holds,r['id'];chosen=holds[-1]
            observations.append(dict(id=r['id'],source_record_index=r['source_record_index'],source_selector=r['source_selector'],interval=pair,selected_capture=chosen,held_captures=holds))
    assert len(observations)==12 and [r['source_record_index'] for r in observations]==[5,9,13,17,21,24,28,32,36,39,42,45]
    assert len(pairs)==23 and seen=={r['offset'] for r in fixture['all23_stored_fixture_commands']} and pairs[-1]['source_offset']==636 and pairs[-1]['word']==0 and pairs[-1]['native_result'][0]==0
    assert [r['source_offset'] for r in pairs if r['word']==0xA000 and r['source_offset'] is not None]==[628]
    snap=report['read_only_RAM_snapshot'];raw=Path(snap['path']).read_bytes();assert snap['read_only_export'] and sha(raw)==snap['sha256'] and len(raw)==4194304;evidence[snap['path']]=snap['sha256']
    ROOT.mkdir(parents=True);sheets=[]
    for start in range(0,12,6):
        sheet=Image.new('RGB',(1560,832),'#263238');draw=ImageDraw.Draw(sheet)
        for i,o in enumerate(observations[start:start+6]):
            x,y=i%3*520,i//3*416;draw.text((x+4,y+3),o['id']+' frame'+str(o['selected_capture']['frame']),fill='white');sheet.paste(Image.open(o['selected_capture']['path']).convert('RGB').crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST),(x+4,y+24));evidence[o['selected_capture']['path']]=o['selected_capture']['PNG_sha256']
        p=ROOT/f'all12_complete_Japanese_source_sheet{start//6+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    exitframe=pairs[-1]['returned'];after=next(f for f in photos if f>exitframe+60);frames=[3010,after,16001];sheet=Image.new('RGB',(768,410),'#263238');draw=ImageDraw.Draw(sheet)
    for i,f in enumerate(frames):
        r,im=photos[f];draw.text((i*256+3,3),'Source frame'+str(f),fill='white');sheet.paste(im,(i*256,24));evidence[r['path']]=r['PNG_sha256']
    p=ROOT/'source_nameplate_port_and_complete_return.png';sheet.save(p);transitions=[dict(path=str(p),sha256=sha(p.read_bytes()),frames=frames)]
    save(ROOT/'all12_source_panels_all23_commands_and_observed_return.json',dict(fixture=str(FIXTURE),fixture_sha256=sha(FIXTURE.read_bytes()),research_ROM=fixture['research_ROM'],research_ROM_sha256=fixture['research_ROM_sha256'],speech_observations=observations,source_distinct_speech_observations=12,total_speech_observations=12,unvisited_source_indices=[],command_pairs=pairs,all14_source_commands_and9_original_initializers_observed=True,all23_stored_fixture_commands=sorted(seen),exit_frame=exitframe,native_end_result=pairs[-1]['native_result'],source_effect_offsets_executed=[628],following_native_commands=following,following_blocks=sorted({r['block'] for r in following}),capture_report=str(rp),observer_report=str(tp),input_schedule_sha256=plan['inputs_sha256'],final_snapshot=snap,queried_final_native_state=state(image.read_file('/__arm9__.bin'),raw),review_sheets=sheets,transition_sheets=transitions,visual_review_pending=True,actual_new_cold_boot_runs=1,total_frames=16001,ordinary_inputs_original_roster_funds_conditions_RNG_effect_results_unforced=True,initialized_Amsterdam_B22_not_natural_event211_activation_original_location_earned_progress_or_hardware=True,no_full_quest_inventory_stat_or_A000_effect_claim=True,Lil_Cristina_names_three_FE_animal_panels_one_FI_and_unknown_object_identity_review_separate=True,English_localization_native_font_layout_and_registered_release_not_approved=True,all_jobs_terminal_and_reaped=True,evidence=evidence,producer_sha256=sha(Path(__file__).read_bytes()),new_editorial_credit=0,full_goal_complete=False))
    print(dict(source_speeches=12,all_fixture_commands=len(pairs),exit=exitframe,following_blocks=sorted({r['block'] for r in following}),complete_source_sheets=len(sheets),transition_sheets=1,frames=16001,no_new_credit=True))
