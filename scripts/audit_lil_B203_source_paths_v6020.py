"""Record observed source dialogue and transitions without claiming natural event activation."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B203_source_paths_v6020')
FIXTURE=Path('work/analysis/lil_B203_source_fixture_v6018/complete_B203_source_B22_fixture.json')
RUN=Path('work/analysis/lil_B203_source_run_v6019_clean_Japanese')
if __name__=='__main__':
    assert not ROOT.exists()
    fixture=read(FIXTURE)['fixtures'][0]
    terminal,plan=map(read,[RUN/'terminal.json',RUN/'run_plan.json'])
    cap=Path(plan['capture_folder']);report=read(cap/'capture_report.json');trace=read(cap/'observer/commands.json')
    assert terminal['terminal'] and terminal['observer_host_slots_restored']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and report['frames']==13001
    assert report['ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes())
    assert not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact']
    assert all(not v for k,v in report.items() if k.startswith('synthetic_'))
    by_at={r['fixture_offset']:r for r in fixture['selected_original_objects']}
    records={r['fixture_command_offset']:r for r in fixture['original_text_records']}
    photos={r['frame']:r for r in report['frames_captured']}
    pairs=[];speeches=[];panels=[];full=[]
    for row in trace['rows']:
        assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
        if row['kind']!='after_command' or row['source'].get('block')!=22:continue
        entry=trace['rows'][row['entry_row']];s=entry['source']
        assert s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==fixture['fixture_block_sha256']
        at=s['instruction_offset'];c=by_at.get(at)
        pair=dict(fixture_offset=at,source_offset=None if c is None else c['source_offset'],word=s['first_word'],
            start=entry['frame'],returned=row['frame'],native_result=row['result_words'],decoded_length=row['decoded_length'],
            before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed'],UI_after=row['native_UI_request_words'])
        pairs.append(pair)
        if at in records:
            r=records[at];holds=[p for f,p in photos.items() if entry['frame']+20<f<row['frame']-4]
            chosen=holds[-1] if holds else None
            speeches.append(dict(id=r['id'],source_record_index=r['source_record_index'],source_selector=r['source_selector'],
                interval=pair,selected_capture=chosen))
            if chosen:
                path=Path(chosen['path']);assert sha(path.read_bytes())==chosen['PNG_sha256']
                im=Image.open(path).convert('RGB')
                label=r['id']+' frame'+str(chosen['frame'])
                panels.append((label,im.crop((0,192,256,384))))
                if r['source_record_index'] in [5,17,21,28,35,38,46,50,54,57,60,67,70,74,77,80]:full.append((label,im))
    assert pairs[-1]['source_offset']==810 and pairs[-1]['word']==0
    selected=[r['source_record_index'] for r in speeches]
    assert set(selected)=={r['source_record_index'] for r in records.values()} and len(selected)==22
    assert len(pairs)==40 and {p['source_offset'] for p in pairs if p['source_offset'] is not None}=={r['source_offset'] for r in fixture['selected_original_objects']}
    ROOT.mkdir(parents=True)
    sheets=[]
    for start in range(0,len(panels),6):
        sheet=Image.new('RGB',(1040,1248),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(label,im) in enumerate(panels[start:start+6]):
            x,y=i%2*520,i//2*416;draw.text((x+4,y+3),label,fill='white')
            sheet.paste(im.resize((512,384),Image.Resampling.NEAREST),(x+4,y+24))
        path=ROOT/f'Japanese_dialogue_sheet{start//6+1}.png';sheet.save(path)
        sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    transitions=[]
    for start in range(0,len(full),4):
        sheet=Image.new('RGB',(1040,1600),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(label,im) in enumerate(full[start:start+4]):
            x,y=i%2*520,i//2*800;draw.text((x+4,y+3),label,fill='white')
            sheet.paste(im.resize((512,768),Image.Resampling.NEAREST),(x+4,y+24))
        path=ROOT/f'Japanese_scene_transition_sheet{start//4+1}.png';sheet.save(path)
        transitions.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    files=[FIXTURE,RUN/'terminal.json',RUN/'run_plan.json',RUN/'inputs.json',cap/'capture_report.json',cap/'observer/commands.json',Path(__file__)]
    save(ROOT/'one_actual_source_path_and_complete_command_intervals.json',dict(
        selected_source_speech_indices=selected,speech_observations=speeches,command_pairs=pairs,
        source_predicate_observations=[p for p in pairs if p['word']==0x8000],
        source_effect_offsets_executed=[p['source_offset'] for p in pairs if p['word']==0xA000 and p['source_offset'] is not None],
        source_end810_return_frame=pairs[-1]['returned'],review_sheets=sheets,transition_sheets=transitions,visual_review_pending=True,
        stored_source_objects=22,unvisited_source_indices=sorted({r['source_record_index'] for r in records.values()}-set(selected)),
        actual_new_cold_boot_runs=1,total_frames=13001,all31_source_plus9_original_initializer_commands_stored=True,
        ordinary_inputs_and_original_conditions_roster_funds_RNG_and_effect_results_unforced=True,
        initialized_Amsterdam_fixture_not_natural_event203_activation_or_original_location=True,
        no_full_route_hardware_or_complete_effect_semantics_claim=True,English_prose_native_layout_and_release_not_approved=True,
        evidence={str(p):sha(p.read_bytes()) for p in files},new_review_credit=0,full_goal_complete=False))
    print(dict(selected_source_indices=selected,unvisited=sorted({r['source_record_index'] for r in records.values()}-set(selected)),
        end_frame=pairs[-1]['returned'],dialogue_sheets=len(sheets),transition_sheets=len(transitions)))
