"""Record actual Japanese-source response paths before choosing revised English prose."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B197_source_paths_v5661')
FIXTURE=Path('work/analysis/lil_B197_source_fixture_v5658/complete_B197_source_B22_fixture.json')
if __name__=='__main__':
    assert not ROOT.exists();fixture=read(FIXTURE)['fixtures'][0];by_at={r['fixture_offset']:r for r in fixture['selected_original_objects']}
    records={r['fixture_command_offset']:r for r in fixture['original_text_records']};versions=[];panels=[];evidence={str(FIXTURE):sha(FIXTURE.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes())}
    for path,option in [('buy',0),('no_buy',1),('delegate',2)]:
        run=Path('work/analysis/lil_B197_source_run_v5659_'+path+'_clean_Japanese');terminal,plan=map(read,[run/'terminal.json',run/'run_plan.json'])
        cap=Path(plan['capture_folder']);files=[run/'terminal.json',run/'run_plan.json',run/'ordinary_menu_inputs.json',cap/'capture_report.json',cap/'observer/commands.json']
        inputs,report,trace=map(read,files[2:]);assert terminal['terminal'] and terminal['observer_host_slots_restored']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and report['frames']==13001
        assert report['ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes())
        assert not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact']
        assert inputs['ordinary_gamepad_only'] and inputs['no_game_RAM_or_predicate_or_seed_write']
        assert all(not v for k,v in report.items() if k.startswith('synthetic_'))
        photos={r['frame']:r for r in report['frames_captured']};pairs=[];speeches=[]
        for row in trace['rows']:
            assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
            if row['kind']!='after_command' or row['source'].get('block')!=22:continue
            entry=trace['rows'][row['entry_row']];s=entry['source'];assert s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==fixture['fixture_block_sha256']
            at=s['instruction_offset'];c=by_at.get(at)
            pair=dict(fixture_offset=at,source_offset=None if c is None else c['source_offset'],word=s['first_word'],start=entry['frame'],returned=row['frame'],native_result=row['result_words'],decoded_length=row['decoded_length'],before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed'],UI_after=row['native_UI_request_words']);pairs.append(pair)
            if at in records:
                r=records[at];holds=[p for f,p in photos.items() if entry['frame']+20<f<row['frame']-4]
                chosen=holds[-1] if holds else None
                speeches.append(dict(id=r['id'],source_record_index=r['source_record_index'],source_selector=r['source_selector'],interval=pair,selected_capture=chosen))
                if chosen:
                    p=Path(chosen['path']);assert sha(p.read_bytes())==chosen['PNG_sha256'];panels.append((path+' '+r['id'],Image.open(p).convert('RGB').crop((0,192,256,384))))
        menus=[p for p in pairs if p['word']==0x2200];assert len(menus)==1 and menus[0]['native_result']==[2,option]
        assert pairs[-1]['source_offset']==874 and pairs[-1]['word']==0
        selected=set(r['source_record_index'] for r in speeches)
        versions.append(dict(path=path,requested_option=option,actual_choice_result=menus[0]['native_result'],selected_source_speech_indices=[r['source_record_index'] for r in speeches],speech_observations=speeches,command_pairs=pairs,
            source_effect_offsets_executed=[p['source_offset'] for p in pairs if p['word']==0xA000 and p['source_offset'] is not None],source47xx_offsets_executed=[p['source_offset'] for p in pairs if p['word'] in [0x4720,0x4735]],source_FE_Ian_Charm_notice_selected=109 in selected,exit_frame=pairs[-1]['returned'],capture_report=str(files[3]),observer_report=str(files[4])))
        evidence.update({str(p):sha(p.read_bytes()) for p in files})
    ROOT.mkdir(parents=True);sheets=[]
    for start in range(0,len(panels),6):
        sheet=Image.new('RGB',(1040,1248),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(label,picture) in enumerate(panels[start:start+6]):
            x,y=i%2*520,i//2*416;draw.text((x+4,y+3),label,fill='white');sheet.paste(picture.resize((512,384),Image.Resampling.NEAREST),(x+4,y+24))
        p=ROOT/f'original_source_response_sheet{start//6+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    save(ROOT/'three_actual_source_menu_paths_and_original_response_intervals.json',dict(versions=versions,source_unique_speech_indices=sorted({n for v in versions for n in v['selected_source_speech_indices']}),review_sheets=sheets,visual_review_pending=True,
        actual_new_cold_boot_runs=3,frames_per_run=13001,total_frames=39003,
        all39_original_commands_and9_init_commands_stored_no_omission=True,ordinary_inputs_original_conditions_RNG_funds_and_effect_results_unforced=True,
        source_event197_not_naturally_selected=True,no_original_eligibility_earned_affordability_full_route_or_hardware_claim=True,
        English_localization_native_font_layout_and_registered_release_not_approved=True,
        evidence=evidence,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print([(v['path'],v['selected_source_speech_indices'],v['source_effect_offsets_executed'],v['source47xx_offsets_executed'],v['exit_frame']) for v in versions])
