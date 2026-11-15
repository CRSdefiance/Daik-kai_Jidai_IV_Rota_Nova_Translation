"""Terminal source-branch/FE evidence;current wording only,not revised gameplay."""
from pathlib import Path
from PIL import Image
import json
import struct

from ndspy.code import MainCodeFile
from dk4tool.dialogue.font_audit import GameAsciiFont
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts import execute_scene_caption_raster as modal
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_lesson_context_audit_v1726')
RUN=Path('work/analysis/lil_lesson_context_v1723')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/lil_lesson_context_v1723_1711')
FONTS=Path('work/analysis/lil_lesson_fonts_v1724c/native_consumer_and_font_research.json')


if __name__=='__main__':
    assert not ROOT.exists()
    plan,terminal,report,trace=[read(p) for p in [RUN/'run_plan.json',RUN/'terminal.json',CAP/'capture_report.json',CAP/'observer/commands.json']]
    digest=sha(Path(plan['candidate']).read_bytes())
    assert digest==plan['candidate_sha256']==terminal['candidate_sha256']==report['ROM_sha256']
    assert report['frames']==29930 and terminal['terminal'] and terminal['observer_host_slots_restored']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert 'battery_save_preloaded' not in report and not any(v for k,v in report.items() if k.startswith('synthetic_'))
    assert not trace['errors'] and not trace['mismatches'] and trace['all_host_slots_restored_and_core_file_exact']
    assert trace['unreturned_at_capture_end']==[]
    assert all(r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'] for r in trace['rows'])
    replay=read(plan['reference_complete_opening_capture_report'])
    assert sha(Path(plan['reference_complete_opening_capture_report']).read_bytes())==plan['reference_report_sha256']
    for frame in (22900,22930):
        a=next(CAP.glob(f'frame_{frame:06d}_*.png'))
        b=next(Path(replay['ROM']).parent.glob('NO_MATCH')) if False else Path(replay['frames_captured'][next(i for i,r in enumerate(replay['frames_captured']) if r['frame']==frame)]['path'])
        assert Image.open(a).convert('RGB').tobytes()==Image.open(b).convert('RGB').tobytes()
    journal=read(CAP/'navigation_command_journal.json')
    requested=[json.loads(s) for s in (RUN/'navigation.jsonl').read_text().splitlines() if s.strip()]
    assert requested==[r['command'] for r in journal['commands_received']]
    assert requested[-1]=={'stop':True} and journal['last_command_frame']==29930
    schedule=list(read(plan['input']))
    for r in journal['commands_received']:
        assert r['validation_passed']
        if r['command'].get('buttons'):schedule.append({'start':r['frame']+1,'duration':r['command']['duration'],'buttons':r['command']['buttons']})
    assert schedule==report['scripted_input_schedule']
    photos=[]
    for r in report['frames_captured']:
        assert sha(Path(r['path']).read_bytes())==r['PNG_sha256']
        assert list(Image.open(r['path']).size)==r['dimensions']==[256,384]
        photos.append({'frame':r['frame'],'path':r['path'],'sha256':r['PNG_sha256']})
    snapshots={}
    for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']+[report['read_only_RAM_snapshot']]:
        raw=Path(r['path']).read_bytes();assert len(raw)==r['bytes']==4194304 and sha(raw)==r['sha256'] and r['read_only_export']
        snapshots[r['path']]=r['sha256']
    rows=[r for r in trace['rows'] if r['source'].get('route')==2 and r['source'].get('block')==120]
    assert rows[0]['source']['instruction_offset']==8 and rows[-1]['source']['instruction_offset']==2072
    assert rows[-1]['kind']=='after_command' and rows[-1]['result_words']==[0,0]
    chosen=next(r for r in rows if r['kind']=='after_command' and r['source']['instruction_offset']==0x41A)
    assert chosen['result_words']==[2,1]
    first=next(r for r in rows if r['kind']=='after_command' and r['source']['instruction_offset']==0x450)
    second=next(r for r in rows if r['kind']=='after_command' and r['source']['instruction_offset']==0x454)
    assert (first['decoded_length'],second['decoded_length'])==(4,140)
    assert any(r['kind']=='before_command' and r['source']['instruction_offset']==0x4E0 for r in rows)
    image=NdsImage.open(plan['candidate']);arm=image.read_file('/__arm9__.bin');font=GameAsciiFont.from_arm9(arm)
    research=read(FONTS);stage=bytes(MainCodeFile(arm,0x02000000).sections[3].data[:-48]);itcm=MainCodeFile(arm,0x02000000).sections[4]
    env={**modal.__dict__,'MODAL_STAGED':stage,'MODAL_CURSOR':research['native_staged_cursor_helper'],
        'MODAL_CURSOR_BYTES':bytes.fromhex(research['native_staged_cursor_helper_hex']),
        'MODAL_ITCM_START':itcm.ramAddress,'MODAL_ITCM':bytes(itcm.data),
        'MODAL_ALIGN_START':research['source_alignment_helper'],
        'MODAL_ALIGN_BYTES':bytes.fromhex(research['source_alignment_helper_hex'])}
    adapter=Path('work/analysis/lil_lesson_fonts_v1724c/scoped_modal_adapter_source.txt')
    exec(compile(adapter.read_text(encoding='utf-8'),str(adapter),'exec'),env)
    packet=read('work/analysis/lil_lessons_source_v1717/complete_lesson_source_context.json')
    source={r['record_index']:r for b in packet['blocks'] if b['block']==120 for r in b['records']}
    checks=[];findings=[]
    for index,frame in [(36,25330),(39,25630),(155,27530),(159,27830),(163,28130),(177,29330)]:
        row=source[index];value=bytes.fromhex(row['current_native_macro_output_hex'])
        native=env['execute'](arm,value.decode('ascii'),modal=True,modal_guarded=True,audit_modal_legacy_guards=True,mode=16)
        expected=set()
        for e in native['glyph_events']:
            if e['code']==32:continue
            glyph=font.decode(chr(e['code']))
            expected.update((16+e['x']+x,296+e['y']+y) for y in range(11) for x in range(6) if glyph.getpixel((x,y)))
        photo=CAP/f'frame_{frame:06d}_navigation.png';actual=Image.open(photo).convert('RGB')
        ink={(x,y) for y in range(296,360) for x in range(16,244) if actual.getpixel((x,y))==(0,8,0)}
        good=expected==ink
        checks.append({'id':row['id'],'frame':frame,'capture':str(photo),'capture_sha256':sha(photo.read_bytes()),
            'complete_current_FE_native_glyph_ink_equal_actual_at16_296':good,
            'missing_pixels':len(expected-ink),'extra_pixels':len(ink-expected),
            'native_source_and_current_body_not_revised_manuscript':True})
        if not good:findings.append(checks[-1])
    ROOT.mkdir(parents=True)
    save(ROOT/'terminal_original_wind_branch_and_FE_context.json',{'candidate':plan['candidate'],'candidate_sha256':digest,
        'terminal_frame':29930,'all_source_observer_callbacks':len(trace['rows']),
        'source_observer_errors_mismatches_zero_host_slots_restored':True,
        'all_inputs_capture_hashes_and_unique4MiB_snapshots_verified':True,'captured_PNGs':photos,'RAM_snapshots':snapshots,
        'ordinary_wind_option1_selected_and_original_relative_skips4_140_observed':True,
        'original_B120_completed_and_returned_to_Sea_View_with_departure_log':True,
        'no_B23_revised_scene_full_route_hardware_or_completion_credit':True,
        'six_current_FE_actual_font_checks':checks,'current_FE_font_model_findings':findings,
        'no_preloaded_save_savestate_gameplay_fixtures_or_ROM_runtime_edit':True,
        'generated_isolated_saves':[{'path':str(p),'sha256':sha(p.read_bytes())} for p in (CAP/'saves').rglob('*') if p.is_file()],
        'proofs':{str(p):sha(p.read_bytes()) for p in [RUN/'run_plan.json',RUN/'terminal.json',RUN/'navigation.jsonl',
            CAP/'capture_report.json',CAP/'observer/commands.json',adapter,FONTS]},
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print({'terminal_frame':29930,'callbacks':len(trace['rows']),'current_FE_actual_checks':len(checks),'font_model_findings':findings},flush=True)
