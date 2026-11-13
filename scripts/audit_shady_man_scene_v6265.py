"""Representative complete source purchase path:original commands and exact full nameplate masks."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/shady_man_scene_v6265');FIX=Path('work/analysis/shady_man_source_fixture_v6260/complete_B206_source_B22_fixture.json')
BASE=Path('work/analysis/lil_B206_source_paths_v6247/three_actual_source_paths_all24_speeches_four_labels_all51_commands_and_returns.json')
if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True);fixture=read(FIX)['fixtures'][0];old=read(BASE)['versions'][0];run=Path('work/analysis/shady_man_source_run_v6262_buy');terminal,plan=read(run/'terminal.json'),read(run/'run_plan.json');cap=Path(plan['capture_folder']);rp=cap/'capture_report.json';tp=cap/'observer/commands.json';report,trace=read(rp),read(tp)
    assert terminal['terminal'] and terminal['observer_instances']==1 and terminal['observer_host_slots_restored'] and report['frames']==16001 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and not report.get('battery_save_preloaded')
    assert report['ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes()) and not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact']
    assert all(not v for k,v in report.items() if k.startswith('synthetic_')) and plan['explicit_B22_entry_ROM_fixture'] and plan['all42_source_commands_retained']
    assert read(plan['original_inputs'])==read(old['capture_report'])['scripted_input_schedule']
    assert report['scripted_input_schedule']==read(plan['original_inputs']) and sha(Path(plan['original_inputs']).read_bytes())==plan['inputs_sha256']
    image=NdsImage.open(fixture['research_ROM']);font=GameAsciiFont.from_arm9(image.read_file('/__arm9__.bin'));photos={}
    for p in report['frames_captured']:
        assert sha(Path(p['path']).read_bytes())==p['PNG_sha256'];photo=Image.open(p['path']).convert('RGB');assert photo.size==(256,384);photos[p['frame']]=(p,photo)
    commands={r['fixture_offset']:r for r in fixture['selected_original_objects']};records={r['fixture_command_offset']:r for r in fixture['original_text_records']};pairs=[];observations=[];following=[];panels=[];changed=0
    values={2:'Lil Argot',7:'Cristina Erneco',173:'Shady Man'}
    for row in trace['rows']:
        assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
        if row['kind']!='after_command':continue
        if row['source']['block']!=22:following.append(dict(frame=row['frame'],block=row['source']['block'],offset=row['source']['instruction_offset'],word=row['source']['first_word'],native_result=row['result_words']));continue
        entry=trace['rows'][row['entry_row']];s=entry['source'];assert s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==fixture['fixture_block_sha256'];at=s['instruction_offset'];c=commands.get(at)
        if c:assert row['decoded_length']==c['native_extent'] or c['source_word'] in [0x100,0x200,0x300,0x400]
        pair=dict(fixture_offset=at,source_offset=None if c is None else c['source_offset'],word=s['first_word'],start=entry['frame'],returned=row['frame'],native_result=row['result_words'],decoded_length=row['decoded_length'],before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed'],UI_after=row['native_UI_request_words']);pairs.append(pair)
        if at not in records:continue
        r=records[at];name=values[r['source_selector']];glyphs={c:font.decode(c) for c in name};ink={(i*6+x,y) for i,c in enumerate(name) for y in range(11) for x in range(6) if glyphs[c].getpixel((x,y))};assert all(any(x//6==i for x,y in ink) for i in [0,len(name)-1])
        width=max(len(name),len('Suspicious Person') if r['source_selector']==173 else len(name))*6;holds=[]
        for frame,(p,photo) in photos.items():
            if not entry['frame']<frame<row['frame']:continue
            actual={(x-4,y-1) for y in range(13) for x in range(width+8) if photo.getpixel((12+x,276+y))==(98,97,98)}
            if actual==ink:holds.append(dict(frame=frame,capture=p['path'],capture_sha256=p['PNG_sha256'],complete_first_final_and_all_internal_glyphs_and_blank_old_tail_guard_exact=True))
        assert holds,(r['id'],name);changed+=r['source_selector']==173
        observation=dict(id=r['id'],source_record_index=r['source_record_index'],source_selector=r['source_selector'],name=name,interval=pair,holds=holds);observations.append(observation)
        if r['source_selector']==173:panels.append((r['id']+' / '+name,Image.open(holds[-1]['capture']).convert('RGB').crop((0,192,256,384))))
    assert pairs==old['command_pairs'] and following==old['following_native_commands']
    assert len(observations)==18 and changed==10 and [r['source_record_index'] for r in observations]==old['selected_source_speech_indices']
    assert pairs[-1]['source_offset']==1518 and pairs[-1]['returned']==7893
    sheets=[]
    for start in range(0,len(panels),6):
        sheet=Image.new('RGB',(1560,832),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(label,photo) in enumerate(panels[start:start+6]):
            x,y=i%3*520,i//3*416;draw.text((x+4,y+3),label,fill='white');sheet.paste(photo.resize((512,384),Image.Resampling.NEAREST),(x+4,y+24))
        p=ROOT/f'complete_Shady_Man_context_sheet{start//6+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    save(ROOT/'complete_source_path_and_all_ten_changed_headers.json',dict(complete_speech_intervals=observations,complete_speech_observations=18,complete_nameplate_observations=18,actual_target_nameplate_cases=10,complete_native_ASCII_glyph_masks_first_final_characters_and_blank_guards_exact=True,complete_command_pairs=pairs,following_native_commands=following,source_and_target_all_command_start_return_RNG_and_UI_words_exact=True,all_remaining_path_dialogue_and_control_bytes_exact=True,exit_frame=7893,following_B120_end_frame=12694,review_sheets=sheets,visual_review_pending=True,new_cold_boots=1,new_frames=16001,all_jobs_terminal_and_reaped=True,actual_catalogue_UI_not_visited_native_getters_checked_separately=True,initialized_Amsterdam_B22_not_natural_event206_original_location_earned_progress_full_effects_routes_or_hardware=True,source9000_asking_price_payment_semantics_remain_unproved=True,no_whole_state_or_broad_simulation_equivalence_claim=True,no_dialogue_or_name_completion_credit=True,full_goal_complete=False,evidence={str(p):sha(p.read_bytes()) for p in [FIX,BASE,rp,tp,run/'terminal.json',run/'run_plan.json',Path(plan['original_inputs']),Path(__file__)]}))
    print('18 complete source panels/names;10 Shady Man headers match every glyph and blank old-label tail. Same command timings,RNG/UI and complete B120 return. Two sheets await viewing.')
