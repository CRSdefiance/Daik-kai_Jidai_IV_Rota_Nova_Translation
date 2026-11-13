"""Distinct guided choice: identical input prefix,four new holds,and outer skip."""
from pathlib import Path
import struct
from PIL import Image
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/rafael_guided_actual_v2009')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/rafael_opening_guided_v2008_RESEARCH_ONLY')
RUN=Path('work/analysis/rafael_opening_guided_v2008')
PRIOR_CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/rafael_opening_trace_v2003_RESEARCH_ONLY')
PRIOR=Path('work/analysis/rafael_independent_actual_v2007e/independent_preparation_and_normal_Lisbon_return.json')
PLAN=Path('work/analysis/rafael_opening_relocation_v2001b/current_B44_typed_relocation_research.json')
FONT=Path('work/analysis/rafael_opening_fonts_v1998/all114_progressive_native_macros_and_complete_font_planes.json')

if __name__=='__main__':
    assert not ROOT.exists()
    report,obs,terminal,plan,font,prior=map(read,(CAP/'capture_report.json',CAP/'observer/commands.json',RUN/'terminal.json',PLAN,FONT,PRIOR))
    assert terminal['terminal']and terminal['observer_host_slots_restored']
    assert report['frames']==46020 and report['ROM_sha256']==plan['research_ROM_sha256']==sha(Path(plan['research_ROM']).read_bytes())
    assert report['cold_boot']and not report['savestate_loaded']and not report['callback_errors']
    assert not any(value for key,value in report.items()if key.startswith('synthetic_'))and 'battery_save_preloaded'not in report
    assert not obs['errors']and not obs['mismatches']and not obs['unreturned_at_capture_end']and obs['all_host_slots_restored_and_core_file_exact']
    old_report=read(PRIOR_CAP/'capture_report.json');old_obs=read(PRIOR_CAP/'observer/commands.json')
    assert [r for r in report['scripted_input_schedule']if r['start']<44881]==[r for r in old_report['scripted_input_schedule']if r['start']<44881]
    assert len([r for r in report['scripted_input_schedule']if r['start']<44881])==129
    def signature(row):
        return(row['frame'],row['kind'],row['source']['instruction_offset'],row.get('decoded_length'),row.get('result_words'))
    assert [signature(r)for r in obs['rows']if r['frame']<=44543]==[signature(r)for r in old_obs['rows']if r['frame']<=44543]
    images={};captures={}
    for r in report['frames_captured']:
        p=Path(r['path']);assert sha(p.read_bytes())==r['PNG_sha256'];image=Image.open(p).convert('RGB');assert image.size==(256,384)
        if r['frame']in images:assert images[r['frame']].tobytes()==image.tobytes()
        images[r['frame']]=image;captures[r['frame']]=dict(path=str(p),sha256=r['PNG_sha256'])
    old_menu=next(r for r in old_report['frames_captured']if r['frame']==44880)
    assert images[44880].tobytes()==Image.open(old_menu['path']).convert('RGB').tobytes()
    for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']+[report['read_only_RAM_snapshot']]:
        assert len(Path(r['path']).read_bytes())==4194304 and sha(Path(r['path']).read_bytes())==r['sha256']
    command_map={r['new_offset']:r for r in plan['mapped_native_commands']};texts={r['new_command_offset']:r for r in plan['text_records']}
    rows=obs['rows'];pairs=[];speeches=[]
    for r in rows:
        assert r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
        s=r['source'];assert s['classification']=='original_SC_cache'and s['route']==0 and s['block']==44 and s['whole_resident_payload_exact_ROM']
        assert s['actual_sha256']==plan['target_block_sha256']
        if r['kind']!='after_command':continue
        before=rows[r['entry_row']];at=before['source']['instruction_offset'];command=command_map[at]
        if command['word']not in(0x200,0x300):assert r['decoded_length']==command['new_native_extent']
        pairs.append(dict(offset=at,word=command['word'],start_frame=before['frame'],return_frame=r['frame'],native_length=r['decoded_length'],result_words=r['result_words']))
        if command['word']==0x4000:speeches.append(texts[at]['id'])
    assert len(pairs)==178 and len(speeches)==len(set(speeches))==114
    assert set(text['id']for text in texts.values())-set(speeches)=={'DK4_MES_B44_R0479'}
    assert len(set(speeches)|set(prior['all113_executed_speeches']))==115
    menu=next(r for r in pairs if r['word']==0x2100);assert menu['result_words']==[2,0]
    conditional=next(r for r in pairs if r['offset']==6486);assert conditional['native_length']==8
    assert pairs[pairs.index(conditional)+1]['offset']==6494
    skip=next(r for r in pairs if r['offset']==6670);assert skip['native_length']==72 and skip['result_words']==[3,0]
    assert pairs[pairs.index(skip)+1]['offset']==6742
    assert pairs[-1]['offset']==6822 and pairs[-1]['result_words']==[0,0]
    cases=[];fonts={r['id']:r for r in font['cases']}
    for ident,frames in(('DK4_MES_B44_R0464',(45240,45270)),('DK4_MES_B44_R0469',(45630,45660))):
        proof=fonts[ident];preview=Path(proof['preview']);assert sha(preview.read_bytes())==proof['preview_sha256']
        im=Image.open(preview).convert('RGB');expected={(x,y)for y in range(64)for x in range(216)if im.getpixel((x,y))==(0,8,0)}
        holds=[]
        for frame in frames:
            actual={(x,y)for y in range(64)for x in range(216)if images[frame].getpixel((16+x,296+y))==(0,8,0)}
            assert expected==actual
            holds.append(dict(frame=frame,complete_native_independent_actual_ink_equal=True,capture=captures[frame]))
        cases.append(dict(id=ident,holds=holds))
    image=NdsImage.open(plan['research_ROM']);arm=image.read_file('/__arm9__.bin');final=Path(report['read_only_RAM_snapshot']['path']).read_bytes()
    ev=image.read_file('/data/EV0.DK4');at=final.find(ev[:96]);assert at>=0 and final.find(ev[:96],at+1)<0
    owner=0x02000000+at-0x34;cpu,get=get_machine(arm,final)
    assert list(struct.unpack('<2I',cpu.mem_read(owner+0x2454,8)))==[5,11]
    assert get(0x7F244)==get(0x2E58C)==0 and bytes(cpu.mem_read(0x02000000,0x400000))==final
    ROOT.mkdir(parents=True)
    save(ROOT/'guided_preparation_repaired_outer_skip_and_Lisbon_return.json',dict(research_ROM=plan['research_ROM'],research_ROM_sha256=plan['research_ROM_sha256'],
        plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),prior_actual=str(PRIOR),prior_actual_sha256=sha(PRIOR.read_bytes()),
        capture_report=str(CAP/'capture_report.json'),capture_report_sha256=sha((CAP/'capture_report.json').read_bytes()),
        observer_report=str(CAP/'observer/commands.json'),observer_report_sha256=sha((CAP/'observer/commands.json').read_bytes()),
        all129_controller_events_and_interpreter_prefix_before_choice_identical=True,whole_menu44880_RGB_exact=True,
        actual_choice0_result_2_0_and_0200_jump_to6494=True,actual_repaired_outer0100_length72_and_cleanup6742=True,
        both_guided_instructions_four_holds_complete_native_actual_ink=True,focused_guided_holds=cases,
        all178_actual_command_pairs=pairs,all114_executed_speeches=speeches,both_actual_branches_union115_source_speeches=True,
        union_complete_matching_panel_samples=prior['complete_matching_speech_panels']+2,
        union_complete_matching_panel_holds=prior['complete_matching_speech_holds']+4,
        other8_opening_speeches_executed_with_offline_native_planes_no_fresh_per_panel_actual_pixel_claim=True,
        normal_Lisbon_town_ID=11,native_category_and_town_pair=[5,11],
        no_save_savestate_location_RNG_funds_outcome_or_event_fixture=True,
        all_inputs_captures_RAM_hashes_callbacks_and_host_restoration_verified=True,
        visual_reviewed_four_guided_instruction_holds_and_normal_Lisbon_return=True,
        registration_compiler_and_clean_patch_still_pending=True,not_full_route_or_hardware_proof=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(actual_commands=178,choice=0,new_full_pixel_holds=4,both_branches_union_speeches=115,normal_Lisbon_ID=11,registered_release_pending=True))
