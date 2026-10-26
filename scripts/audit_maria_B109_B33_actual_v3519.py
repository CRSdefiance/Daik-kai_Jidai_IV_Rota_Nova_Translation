"""Audit terminal cold boots and exact actual text planes for the explicit B33 fixture."""
import json
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/maria_B109_B33_actual_v3519')
PLAN=Path('work/analysis/maria_B109_B33_fixture_v3516/B109_source_owned_relocation_and_B33_entry_fixture.json')
FONT=Path('work/analysis/maria_B109_fonts_v3515/current_macro_QA_and_progressive_font_proof.json')
SOURCE=Path('work/analysis/maria_B109_source_v3498/all26_clean_current_complete_context.json')
CAPBASE=Path('E:/Rota Nova translations/Generated/work/emulation_v193')

if __name__=='__main__':
    assert not ROOT.exists();plan,font,source=map(read,[PLAN,FONT,SOURCE]);versions=[];allphotos={};dependencies={}
    # Require both terminal receipts before inspecting either run's result artifacts.
    for case in ['clean_Japanese','reviewed_English']:
        run=Path('work/analysis/maria_B109_B33_fixture_run_v3517_'+case)
        assert read(run/'terminal.json')['terminal']
    source_commands=read(plan['control_proof'])['source_native_walk']['commands']
    for selected in plan['fixtures']:
        case=selected['case'];run=Path('work/analysis/maria_B109_B33_fixture_run_v3517_'+case);cap=CAPBASE/('maria_B109_B33_fixture_v3517_'+case)
        paths=[run/'terminal.json',run/'run_plan.json',cap/'capture_report.json',cap/'observer/commands.json',cap/'navigation_command_journal.json']
        terminal,runplan,report,trace,journal=map(read,paths)
        im=NdsImage.open(selected['research_ROM']);blocks=IlnkContainer.parse(im.read_file('/data/SC3.DK4')).blocks
        assert terminal['terminal'] and terminal['observer_host_slots_restored'] and terminal['frame']==report['frames']>=31000
        assert sha(Path(selected['research_ROM']).read_bytes())==selected['research_ROM_sha256']==report['ROM_sha256']==runplan['candidate_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert runplan['B109_content_in_B33_entry_ROM_fixture'] and runplan['source_event109_not_selected']
        assert all(k=='synthetic_gallery_fixtures' or not v for k,v in report.items() if k.startswith('synthetic_'))
        fixture=read(runplan['fixture_manifest']);assert sha(Path(runplan['fixture_manifest']).read_bytes())==runplan['fixture_manifest_sha256']
        assert fixture['only_system_low_four_bits_and_original_checksum_changed'] and fixture['all_six_route_save_slots_and_footer_unchanged'] and fixture['earned_unlock_verified'] is False
        assert fixture['production_ROM_sha256']==report['ROM_sha256'] and len(report['synthetic_gallery_fixtures'])==1
        assert report['synthetic_gallery_fixtures'][0]['manifest_sha256']==runplan['fixture_manifest_sha256']
        assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot'] and not report['battery_save_preloaded']['savestate_loaded']
        assert sha(Path(runplan['existing_isolated_system_unlock_save']).read_bytes())==runplan['save_sha256']==fixture['fixture_save_sha256']
        assert not trace['errors'] and not trace['mismatches'] and not trace['unreturned_at_capture_end'] and trace['all_host_slots_restored_and_core_file_exact']
        nav=[json.loads(s) for s in (run/'navigation.jsonl').read_text().splitlines() if s.strip()]
        assert nav==[r['command'] for r in journal['commands_received']]==[{'stop':True}]
        assert all(r['validation_passed'] for r in journal['commands_received'])
        assert read(runplan['inputs'])==report['scripted_input_schedule'] and sha(Path(runplan['inputs']).read_bytes())==runplan['inputs_sha256']
        photos={}
        for photo in report['frames_captured']:
            p=Path(photo['path']);assert sha(p.read_bytes())==photo['PNG_sha256'];pic=Image.open(p).convert('RGB');assert pic.size==(256,384)
            if photo['frame'] in photos:assert photos[photo['frame']][1].tobytes()==pic.tobytes()
            photos[photo['frame']]=(photo,pic)
        for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']+[report['read_only_RAM_snapshot']]:
            raw=Path(r['path']).read_bytes();assert len(raw)==r['bytes']==4194304 and sha(raw)==r['sha256'] and r['read_only_export']
        rows=trace['rows'];pairs=[];intervals=[]
        textmap={r['current_reference']['header_offset']:r for r in source['records']} if case=='clean_Japanese' else {r['new_command_offset']:r for r in plan['text_records']}
        commandmap={r['offset']:dict(word=r['word'],extent=r['native_extent']) for r in source_commands} if case=='clean_Japanese' else {r['new_offset']:dict(word=r['word'],extent=r['new_extent']) for r in plan['mapped_native_commands']}
        for r in rows:
            assert r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'];s=r['source']
            assert s['classification']=='original_SC_cache' and s['route']==3 and s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==sha(blocks[s['block']])
            assert s['block']!=109,'Fixture must not masquerade as selected event109'
            if r['kind']!='after_command':continue
            b=rows[r['entry_row']];s=b['source'];at=s['instruction_offset'];word=int.from_bytes(blocks[s['block']][at:at+2],'little')
            pair=dict(block=s['block'],offset=at,word=word,start=b['frame'],returned=r['frame'],extent=r['decoded_length'],result_words=r['result_words']);pairs.append(pair)
            if s['block']==33:
                assert commandmap[at]['word']==word and commandmap[at]['extent']==r['decoded_length']
                if word==0x4000:intervals.append(dict(**pair,id=textmap[at]['id'],prefix=blocks[33][at+5]))
        selectedpairs=[r for r in pairs if r['block']==33]
        assert len(selectedpairs)==34 and [r['word'] for r in selectedpairs]==[r['word'] for r in source_commands]
        assert selectedpairs[-1]['word']==0 and selectedpairs[-1]['result_words']==[0,0]
        assert len(intervals)==len({r['id'] for r in intervals})==26 and {r['prefix'] for r in intervals}=={3,11,21,74}
        assert blocks[33][8:18].hex()==plan['source_owned_prefix_span']['after']
        versions.append(dict(case=case,ROM_sha256=report['ROM_sha256'],terminal_frame=report['frames'],capture_report=str(cap/'capture_report.json'),observer_report=str(cap/'observer/commands.json'),original_commands=pairs,B109_content_in_B33_speech_intervals=intervals,all34_source_command_shapes_and_normal_exit=True,all26_speeches_observed=True,source_event109_not_selected=True,source_UI_prefix_4500_4684_pause_and_C200_executed=True,existing_system_unlock_not_earned=True,other_observed_blocks_unreviewed=sorted(set(r['block'] for r in pairs)-{33})))
        allphotos[case]=photos
        for p in paths+[run/'navigation.jsonl',Path(runplan['fixture_manifest'])]:dependencies[str(p)]=sha(p.read_bytes())
    assert read('work/analysis/maria_B109_B33_fixture_run_v3517_clean_Japanese/run_plan.json')['inputs_sha256']==read('work/analysis/maria_B109_B33_fixture_run_v3517_reviewed_English/run_plan.json')['inputs_sha256']
    proofs={r['id']:r for r in font['cases']};actual=[];unmatched=[]
    for interval in versions[1]['B109_content_in_B33_speech_intervals']:
        proof=proofs[interval['id']];p=Path(proof['preview']);assert sha(p.read_bytes())==proof['preview_sha256'];preview=Image.open(p).convert('RGB')
        expected={(x,y) for y in range(64) for x in range(216) if preview.getpixel((x,y))==(0,8,0)};holds=[]
        for frame,(photo,pic) in allphotos['reviewed_English'].items():
            if not interval['start']<frame<interval['returned']:continue
            ink={(x,y) for y in range(64) for x in range(216) if pic.getpixel((16+x,296+y))==(0,8,0)}
            if ink!=expected:unmatched.append(dict(id=interval['id'],frame=frame,missing=len(expected-ink),extra=len(ink-expected)));continue
            holds.append(dict(frame=frame,capture=photo['path'],capture_sha256=photo['PNG_sha256'],complete_actual216x64_ink_equal_independent_native_plane=True));dependencies[photo['path']]=photo['PNG_sha256']
        actual.append(dict(id=interval['id'],prefix=interval['prefix'],holds=holds))
    matched=[r for r in actual if r['holds']]
    ROOT.mkdir(parents=True);sheets=[]
    for start in range(0,len(matched),6):
        sheet=Image.new('RGB',(780,690),'#263238');draw=ImageDraw.Draw(sheet)
        for i,r in enumerate(matched[start:start+6]):
            hold=r['holds'][0];x,y=390*(i%2),230*(i//2);pic=Image.open(hold['capture']).convert('RGB');draw.text((x+4,y+3),r['id']+' / '+str(hold['frame']),fill='white');sheet.paste(pic.crop((0,260,256,384)).resize((384,186)),(x+3,y+25))
        p=ROOT/f'actual_English_sheet_{start//6+1:02d}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    overview=Image.new('RGB',(1024,768),'#263238');draw=ImageDraw.Draw(overview)
    for x,case in enumerate(['clean_Japanese','reviewed_English']):
        for y,frame in enumerate([4000,31000]):
            p=allphotos[case][frame][1];overview.paste(p.resize((512,384)),(x*512,y*384));draw.text((x*512+3,y*384+3),case+' / '+str(frame),fill='red')
    p=ROOT/'source_English_setup_and_final_transition.png';overview.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    proof=dict(versions=versions,plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),font_proof=str(FONT),font_proof_sha256=sha(FONT.read_bytes()),observed_speech_panels=actual,complete_matching_panels=len(matched),complete_matching_holds=sum(len(r['holds']) for r in matched),unmatched_capture_planes=unmatched,all_inputs_captures_RAM_hashes_callbacks_host_restoration_and_fixture_scope_verified=True,representative_contact_sheets=sheets,visual_review_pending=True,source_event109_not_selected_or_earned=True,B109_content_in_B33_entry_fixture_only=True,not_full_route_or_hardware_proof=True,evidence=dependencies,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    save(ROOT/'terminal_B33_fixture_commands_and_actual_native_planes.json',proof)
    print(dict(selected_content_speeches=26,matching_panels=len(matched),holds=proof['complete_matching_holds'],unmatched=unmatched,credit=0))
    assert len(matched)==26 and {r['prefix'] for r in matched}=={3,11,21,74},'Retained diagnostic; full display approval requires successor proof.'
