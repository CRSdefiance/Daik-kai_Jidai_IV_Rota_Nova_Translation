"""Audit actually visited source commands without treating all stored alternatives as gameplay."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B209_source_actual_v6456')
FIXTURE=Path('work/analysis/lil_B209_source_fixture_v6453/complete_B209_source_B22_fixture.json')
RUN=Path('work/analysis/lil_B209_source_run_v6454')
if __name__=='__main__':
    assert not ROOT.exists();fixture=read(FIXTURE)['fixtures'][0];terminal,plan=read(RUN/'terminal.json'),read(RUN/'run_plan.json');cap=Path(plan['capture_folder']);rp,tp=cap/'capture_report.json',cap/'observer/commands.json';report,trace=read(rp),read(tp)
    assert terminal['terminal'] and terminal['observer_host_slots_restored'] and terminal['observer_instances']==1 and report['frames']==16001 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and not report.get('battery_save_preloaded')
    assert report['ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes()) and not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact']
    assert not any(v for k,v in report.items() if k.startswith('synthetic_')) and plan['explicit_B22_entry_ROM_fixture'] and plan['all18_source_commands_retained'] and plan['source_event209_not_naturally_selected']
    schedule=read(plan['original_inputs']);assert sha(Path(plan['original_inputs']).read_bytes())==plan['inputs_sha256'] and report['scripted_input_schedule']==schedule and not any(r['buttons']==['DOWN'] for r in schedule)
    image=NdsImage.open(fixture['research_ROM']);bank=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;commands={r['fixture_offset']:r for r in fixture['selected_original_objects']};records={r['fixture_command_offset']:r for r in fixture['original_text_records']};photos={};evidence={str(p):sha(p.read_bytes()) for p in [FIXTURE,RUN/'terminal.json',RUN/'run_plan.json',Path(plan['original_inputs']),rp,tp,Path(__file__)]}
    for r in report['frames_captured']:
        p=Path(r['path']);assert sha(p.read_bytes())==r['PNG_sha256'];im=Image.open(p).convert('RGB');assert im.size==(256,384);photos[r['frame']]=(r,im)
    pairs=[];observations=[];following=[];seen=set();extent_changes=[]
    for row in trace['rows']:
        assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'];s=row['source'];assert s['classification']=='original_SC_cache' and s['route']==2 and s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==sha(bank[s['block']])
        if row['kind']!='after_command':continue
        if s['block']!=22:following.append(dict(frame=row['frame'],block=s['block'],offset=s['instruction_offset'],word=s['first_word'],native_result=row['result_words']));continue
        entry=trace['rows'][row['entry_row']];at=entry['source']['instruction_offset'];seen.add(at);c=commands.get(at)
        if c:
            assert entry['source']['first_word']==c['source_word']
            if row['decoded_length']!=c['native_extent']:extent_changes.append(dict(source_offset=c['source_offset'],word=c['source_word'],inventory_unmatched_extent=c['native_extent'],actual_native_extent=row['decoded_length']))
        pair=dict(fixture_offset=at,source_offset=None if c is None else c['source_offset'],word=entry['source']['first_word'],start=entry['frame'],returned=row['frame'],native_result=row['result_words'],decoded_length=row['decoded_length'],before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed'],UI_after=row['native_UI_request_words']);pairs.append(pair)
        if at in records or entry['source']['first_word']==0x4100:
            holds=[photo for frame,(photo,im) in photos.items() if entry['frame']+20<frame<row['frame']-4];assert holds,at
            r=records.get(at);observations.append(dict(id=r['id'] if r else f'B209_automatic4100_command_{c["source_offset"]}',source_record_index=r['source_record_index'] if r else None,source_selector=r['source_selector'] if r else 208,kind='progressive' if r else 'automatic4100-selected-style-body-not-yet-pixel-bound',interval=pair,selected_capture=holds[-1],held_captures=holds))
    assert len(pairs)==24 and len(observations)==6 and [r['source_record_index'] for r in observations if r['kind']=='progressive']==[27,30,33,71]
    allstored={r['offset'] for r in fixture['all27_stored_fixture_commands']};unvisited=sorted(allstored-seen);assert unvisited==[746,1088,1138]
    assert extent_changes==[dict(source_offset=694,word=0x200,inventory_unmatched_extent=4,actual_native_extent=8)]
    assert pairs[-1]['source_offset']==1144 and pairs[-1]['word']==0 and pairs[-1]['native_result'][0]==0 and pairs[-1]['returned']==4294
    assert next(p for p in pairs if p['source_offset']==686)['native_result'][0]==2
    ROOT.mkdir(parents=True);sheets=[];sheet=Image.new('RGB',(768,820),'#263238');draw=ImageDraw.Draw(sheet)
    for i,o in enumerate(observations):
        x,y=i%3*256,i//3*410;draw.text((x+2,y+2),o['id']+' f'+str(o['selected_capture']['frame']),fill='white');sheet.paste(Image.open(o['selected_capture']['path']).convert('RGB'),(x,y+24));evidence[o['selected_capture']['path']]=o['selected_capture']['PNG_sha256']
    p=ROOT/'all_six_observed_Japanese_panels_including_three_letter_pages.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    exitframe=pairs[-1]['returned'];after=next(f for f in photos if f>exitframe+60);frames=[after,16001];sheet=Image.new('RGB',(512,410),'#263238');draw=ImageDraw.Draw(sheet)
    for i,f in enumerate(frames):r,im=photos[f];draw.text((i*256+3,3),'Source frame'+str(f),fill='white');sheet.paste(im,(i*256,24));evidence[r['path']]=r['PNG_sha256']
    p=ROOT/'source_return_and_final_full_frame.png';sheet.save(p);transitions=[dict(path=str(p),sha256=sha(p.read_bytes()),frames=frames)]
    save(ROOT/'six_actual_panels24_visited_of27_stored_commands_and_honest_conditional_scope.json',dict(fixture=str(FIXTURE),fixture_sha256=sha(FIXTURE.read_bytes()),research_ROM=fixture['research_ROM'],research_ROM_sha256=fixture['research_ROM_sha256'],actual_panel_observations=observations,actual_progressive_speech_objects=4,actual_automatic_style_commands=2,actual_style_body_IDs_not_yet_bound=True,all20_stored_objects_not_claimed_as_actual=True,unvisited_explicit_Jam_record_index=65,command_pairs=pairs,stored_commands=27,visited_commands=24,unvisited_fixture_offsets=unvisited,unvisited_source_offsets=[v-48 for v in unvisited],original_predicate_result=2,actual0200_consumes_following0300_header=True,actual_vs_unmatched_inventory_extent_changes=extent_changes,all_source_commands_stored_without_omission=True,exit_frame=exitframe,native_end_result=pairs[-1]['native_result'],following_native_commands=following,following_blocks=sorted({r['block'] for r in following}),capture_report=str(rp),observer_report=str(tp),input_schedule_sha256=plan['inputs_sha256'],review_sheets=sheets,transition_sheets=transitions,visual_review_pending=True,source_letter_picture_staging_complete_glyphs_names_and_native_pagination_not_yet_approved=True,actual_new_cold_boot_runs=1,total_frames=16001,source_session40304_terminal_and_reaped=True,ordinary_inputs_original_roster_conditions_RNG_and_results_unforced=True,initialized_Amsterdam_B22_not_natural209_original_location_earned_progress_full_effects_routes_or_hardware=True,English_layout_and_registered_integration_pending=True,no_name_or_dialogue_credit_added=True,evidence=evidence,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('6 actual panels:4 speeches+2 selected automatic variants.24/27 commands executed;Jam reaction/one branch unvisited. Source exit4294. Two sheets await viewing;not all20 gameplay coverage.')
