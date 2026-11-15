"""Audit terminal B97 content fixtures and original A continuation with its observed one-cell indent."""
from collections import Counter
from pathlib import Path
from types import FunctionType
import json,struct
from PIL import Image,ImageDraw
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_name_catalog_glyphs_v278 import raster as original_raster
from scripts.lil_current_font_oracles_v4792 import expected_pixels
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B97_actual_v5017')
PLAN=Path('work/analysis/maria_B97_fixture_v5014/B97_reversible_relocation_and_B33_content_fixture.json')
FONT=Path('work/analysis/maria_B97_fonts_v5013b/all32_font_matrices_256_alignments_and_source72_page_projection.json')
CAPBASE=Path('E:/Rota Nova translations/Generated/work/emulation_v193')

def masks(image):
    values=list(image.convert('RGB').get_flattened_data())
    return bytes(v==(0,8,0) for v in values),bytes(v==(98,97,98) for v in values)

if __name__=='__main__':
    assert not ROOT.exists();plan,font=read(PLAN),read(FONT);packet=read(plan['source_context']);versions=[];photosets={};reports={};raws={};evidence={}
    for case in ['clean_Japanese','reviewed_English']:assert read(Path('work/analysis/maria_B97_B33_fixture_run_v5015b_'+case)/'terminal.json')['terminal']
    for fixture in plan['fixtures']:
        case=fixture['case'];run=Path('work/analysis/maria_B97_B33_fixture_run_v5015b_'+case);cap=CAPBASE/('maria_B97_B33_fixture_v5015b_'+case)
        paths=[run/'terminal.json',run/'run_plan.json',cap/'capture_report.json',cap/'observer/commands.json',cap/'navigation_command_journal.json']
        terminal,rp,report,trace,journal=map(read,paths)
        assert terminal['terminal'] and terminal['observer_host_slots_restored'] and terminal['frame']==report['frames']==31000
        assert sha(Path(fixture['research_ROM']).read_bytes())==fixture['research_ROM_sha256']==report['ROM_sha256']==rp['candidate_sha256']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert rp['B97_content_in_B33_entry_ROM_fixture'] and rp['source_event97_not_selected'] and rp['no_savestate_or_location_RNG_funds_outcome_RAM_fixture']
        assert sha(Path(rp['fixture_scope_manifest']).read_bytes())==rp['fixture_scope_manifest_sha256']==sha(PLAN.read_bytes())
        manifest=read(rp['fixture_manifest']);assert sha(Path(rp['fixture_manifest']).read_bytes())==rp['fixture_manifest_sha256']
        assert manifest['only_system_low_four_bits_and_original_checksum_changed'] and manifest['all_six_route_save_slots_and_footer_unchanged'] and not manifest['earned_unlock_verified']
        assert manifest['production_ROM_sha256']==report['ROM_sha256'] and report['synthetic_gallery_fixtures']==[dict(preloaded_save_manifest=rp['fixture_manifest'],manifest_sha256=rp['fixture_manifest_sha256'],synthetic_gallery_fixture=True,earned_unlock_verified=False,validated_selected_supported_site_ids=None)]
        assert not any(v for k,v in report.items() if k.startswith('synthetic_') and k!='synthetic_gallery_fixtures')
        assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot'] and not report['battery_save_preloaded']['savestate_loaded']
        assert sha(Path(rp['existing_isolated_system_unlock_save']).read_bytes())==rp['save_sha256']==manifest['fixture_save_sha256']=='295631dc76ae7b8c10b99a62dcbdbba815400a9463fc24df55e61abbf220d949'
        assert not trace['errors'] and trace['mismatches']==0 and not trace['unreturned_at_capture_end'] and trace['all_host_slots_restored_and_core_file_exact']
        nav=[json.loads(s) for s in (run/'navigation.jsonl').read_text().splitlines() if s.strip()]
        assert nav==[r['command'] for r in journal['commands_received']]==[{'stop':True}] and all(r['validation_passed'] for r in journal['commands_received'])
        assert read(rp['inputs'])==report['scripted_input_schedule'] and sha(Path(rp['inputs']).read_bytes())==rp['inputs_sha256']
        blocks=IlnkContainer.parse(NdsImage.open(fixture['research_ROM']).read_file('/data/SC3.DK4')).blocks;body=blocks[33]
        assert sha(body)==fixture['body_sha256']
        commands=packet['blocks'][0]['all_clean_native_commands'] if case=='clean_Japanese' else [dict(offset=c['new_offset'],word=c['word'],native_extent=c['new_extent']) for c in plan['mapped_native_commands']]
        commandmap={c['offset']:c for c in commands}
        textmap={r['header_offset']:r for r in packet['records']} if case=='clean_Japanese' else {r['new_command_offset']:r for r in plan['text_records']}
        pairs=[];intervals=[];rows=trace['rows']
        for row in rows:
            assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'];s=row['source']
            assert s['classification']=='original_SC_cache' and s['route']==3 and s['block']==33 and s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==sha(body)
            if row['kind']!='after_command':continue
            entry=rows[row['entry_row']];at=entry['source']['instruction_offset'];word=struct.unpack_from('<H',body,at)[0];c=commandmap[at]
            assert c['word']==word and c['native_extent']==row['decoded_length']
            pair=dict(offset=at,word=word,start=entry['frame'],returned=row['frame'],extent=row['decoded_length'],result_words=row['result_words']);pairs.append(pair)
            if word==0x4000:intervals.append(dict(pair,id=textmap[at]['id'],prefix=body[at+5]))
        assert len(pairs)==40 and [r['offset'] for r in pairs]==[c['offset'] for c in commands] and len(intervals)==32
        assert pairs[-1]['word']==0 and pairs[-1]['result_words']==[0,0] and {r['prefix'] for r in intervals}=={3,10,180,254}
        assert Counter(r['word'] for r in pairs)==Counter(c['word'] for c in commands)
        photos={}
        for photo in report['frames_captured']:
            path=Path(photo['path']);assert sha(path.read_bytes())==photo['PNG_sha256'];picture=Image.open(path).convert('RGB');assert picture.size==(256,384)
            if photo['frame'] in photos:assert photos[photo['frame']][1].tobytes()==picture.tobytes()
            photos[photo['frame']]=(photo,picture)
        for snap in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']+[report['read_only_RAM_snapshot']]:
            raw=Path(snap['path']).read_bytes();assert snap['read_only_export'] and len(raw)==snap['bytes']==4194304 and sha(raw)==snap['sha256']
        raws[case]=Path(report['read_only_RAM_snapshot']['path']).read_bytes()
        versions.append(dict(case=case,ROM=fixture['research_ROM'],ROM_sha256=fixture['research_ROM_sha256'],frames=report['frames'],command_pairs=pairs,speech_intervals=intervals,normal_end_frame=pairs[-1]['returned'],input_schedule_sha256=rp['inputs_sha256'],capture_report=str(paths[2]),observer_report=str(paths[3]),source97_not_naturally_selected=True,original_setup_resources_two_effects_item_presentation_hide_and_end_actually_executed=True))
        photosets[case]=photos;reports[case]=report;evidence.update({str(p):sha(p.read_bytes()) for p in paths+[Path(rp['fixture_manifest']),run/'navigation.jsonl',Path(rp['inputs'])]})
    assert versions[0]['input_schedule_sha256']==versions[1]['input_schedule_sha256']
    assert [(r['word'],r['result_words']) for r in versions[0]['command_pairs']]==[(r['word'],r['result_words']) for r in versions[1]['command_pairs']]
    ROOT.mkdir(parents=True);image=NdsImage.open(plan['parent']);arm=image.read_file('/__arm9__.bin')
    class FontROM:
        @staticmethod
        def open(path):assert str(path)=='work/clean.nds';return image
    raster=FunctionType(original_raster.__code__,{**original_raster.__globals__,'NdsImage':FontROM},argdefs=original_raster.__defaults__);raster.__kwdefaults__=original_raster.__kwdefaults__
    r72=next(r for r in plan['text_records'] if r['id']=='DK4_MES_B97_R0072');expanded=bytes.fromhex(r72['stored_text_hex'])[1:];parts=expanded.split(b'\n');assert len(parts)==5
    continuation=parts[4];assert continuation==b" We're gathering them to stop that. "
    pixels,events,fontdata=raster(arm,continuation);assert pixels==expected_pixels(arm,fontdata,events)
    visible=[e for e in events if e['code']!=32];assert [e['code'] for e in visible]==[v for v in continuation if v!=32]
    assert min(e['x'] for e in visible)==6 and max(e['x'] for e in visible)<=210 and all(e['y']==0 for e in visible)
    page2=Image.new('RGB',(216,64));colors={0:(239,232,201),1:(0,8,0),15:(98,97,98)};page2.putdata([colors[p] for p in pixels]);p2=ROOT/'R72_continuation_native_one_cell_indent.png';page2.save(p2)
    (ROOT/'R72_continuation_native_one_cell_indent.bin').write_bytes(pixels)
    byid={r['id']:r for r in font['cases']};source_intervals={r['id']:r for r in versions[0]['speech_intervals']};actual=[];panels=[];failures=[];nontext=[]
    for interval in versions[1]['speech_intervals']:
        c=byid[interval['id']];previews=[(v['page'],Image.open(v['path']).convert('RGB')) for v in c['previews']]
        if interval['id']==r72['id']:previews[1]=(2,page2)
        src=source_intervals[interval['id']];source_candidates=[(f,p) for f,p in photosets['clean_Japanese'].items() if src['start']+90<f<src['returned']-20];assert source_candidates,src
        sf,(sphoto,spicture)=source_candidates[-1]
        for page,preview in previews:
            expected=masks(preview);holds=[]
            for frame,(photo,picture) in photosets['reviewed_English'].items():
                if not interval['start']<frame<interval['returned']:continue
                if masks(picture.crop((16,296,16+preview.width,360)))!=expected:continue
                regions=dict(upper=picture.crop((0,0,256,192)).tobytes()==spicture.crop((0,0,256,192)).tobytes(),portrait_name=picture.crop((0,192,256,294)).tobytes()==spicture.crop((0,192,256,294)).tobytes())
                nontext.append(dict(id=interval['id'],page=page,English_frame=frame,source_frame=sf,source_held_frame_by_corresponding_record_not_identical_wallclock=True,**regions))
                holds.append(dict(frame=frame,capture=photo['path'],capture_sha256=photo['PNG_sha256'],complete_native_ink_and_gray_masks_equal=True));evidence[photo['path']]=photo['PNG_sha256']
            if not holds:failures.append(dict(id=interval['id'],page=page,reason='No complete native-plane match within this original command interval'))
            else:panels.append((interval['id']+f' page{page}',holds[0]['frame'],Image.open(holds[0]['capture']).convert('RGB')))
            actual.append(dict(id=interval['id'],prefix=interval['prefix'],page=page,holds=holds,original_speech_command_interval=interval))
    pageholds=[r for r in actual if r['id']==r72['id']];assert len(pageholds)==2
    a_events=[r for r in reports['reviewed_English']['scripted_input_schedule'] if 'A' in r.get('buttons',[]) and pageholds[0]['holds'][0]['frame']<r['start']<pageholds[1]['holds'][0]['frame']]
    assert len(a_events)==1 and a_events[0]=={'start':15401,'duration':8,'buttons':['A']}
    sheets=[]
    for start in range(0,len(panels),6):
        sheet=Image.new('RGB',(780,960),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(ident,frame,picture) in enumerate(panels[start:start+6]):
            x,y=390*(i%2),320*(i//2);draw.text((x+4,y+3),ident+' / '+str(frame),fill='white');sheet.paste(picture.crop((0,192,256,384)).resize((384,288)),(x+3,y+25))
        path=ROOT/f'actual_English_sheet_{start//6+1:02d}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    states={}
    for case,raw in raws.items():states[case]=dict(final_RAM_sha256=sha(raw),actor_root022D4340_1A04_sha256=sha(raw[0x2D4340:0x2D5D44]),original_PRNG_word02168EB8=struct.unpack_from('<I',raw,0x168EB8)[0])
    final_equal=photosets['clean_Japanese'][31000][1].tobytes()==photosets['reviewed_English'][31000][1].tobytes()
    save(ROOT/'terminal40_commands32_speeches_and_actual_two_page_continuation.json',dict(versions=versions,plan=str(PLAN),plan_sha256=sha(PLAN.read_bytes()),font_proof=str(FONT),font_proof_sha256=sha(FONT.read_bytes()),actual_panels=actual,complete_actual_panel_pages=sum(bool(r['holds']) for r in actual),failures=failures,paired_nontext_samples=nontext,nontext_differences=[r for r in nontext if not r['upper'] or not r['portrait_name']],source72_page_boundary=dict(original_single_command_preserved=True,first_four_rows_match_font_matrix=True,continuation_input_hex=continuation.hex(),original_A_event=a_events[0],continuation_native_preview=str(p2),continuation_native_preview_sha256=sha(p2.read_bytes()),continuation_native_plane_sha256=sha(pixels),all_continuation_glyph_events=events,original_continuation_first_row_indent_px=6,full_wording_macro_controls_and_encoded_target_unchanged=True,earlier_zero_indent_projection_retained_as_diagnostic=True,no_renderer_font_guard_or_RAM_fixture_change=True),final_state_observations=states,final31000_whole_RGB_equal=final_equal,all32_source_controls_and_original_setup_resource_effects_picture_hide_end_actually_observed=True,source_exit23222_English23822_are_measured_not_forced=True,no_causal_PRNG_future_world_or_full_RAM_equivalence_claim=True,all_callbacks_read_only_at_entry_and_return_not_proof_against_original_temporary_game_writes=True,existing_system_unlock_is_unearned_and_only_declared_save_fixture=True,B97_content_in_B33_entry_not_natural_event97_earned_recruitment_or_earned_tablet=True,representative_contact_sheets=sheets,visual_review_pending=True,evidence={**evidence,str(PLAN):sha(PLAN.read_bytes()),str(FONT):sha(FONT.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes())},new_emulator_runs=2,new_emulator_frames=62000,new_review_credit=0,not_full_route_or_hardware_proof=True,full_goal_complete=False))
    print(dict(commands_each=40,speeches_each=32,actual_page_matches=sum(bool(r['holds']) for r in actual),failures=failures,nontext_differences=sum(not r['upper'] or not r['portrait_name'] for r in nontext),final_RGB_equal=final_equal,states=states,credit=0))
    assert not failures and len(actual)==33
