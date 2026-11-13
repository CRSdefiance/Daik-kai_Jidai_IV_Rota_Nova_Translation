"""Audit complete paired B175 command execution and progressive/FE native text planes."""
from collections import Counter
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B175_actual_v4534')
PLAN=Path('work/analysis/lil_B175_display_fixture_v4531/complete_B175_B22_fixtures.json')
FONT=Path('work/analysis/lil_B175_native_approval_v4518/all32_native_progressive_FE_and_source_reconciliation.json')
CAPBASE=Path('E:/Rota Nova translations/Generated/work/emulation_v193')

if __name__=='__main__':
    assert not ROOT.exists()
    plan,font=read(PLAN),read(FONT);versions=[];photosets={}
    evidence={str(p):sha(p.read_bytes()) for p in [PLAN,FONT,Path(__file__)]}
    for fixture in plan['fixtures']:
        case=fixture['case'];run=Path('work/analysis/lil_B175_display_run_v4533_'+case);cap=CAPBASE/('lil_B175_display_v4533_'+case)
        paths=[run/'terminal.json',run/'run_plan.json',cap/'capture_report.json',cap/'observer/commands.json']
        terminal,rp,report,trace=map(read,paths)
        assert terminal['terminal'] and terminal['observer_host_slots_restored'] and terminal['observer_instances']==1
        assert report['frames']==16001 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert sha(Path(fixture['research_ROM']).read_bytes())==fixture['research_ROM_sha256']==report['ROM_sha256']==rp['research_ROM_sha256']
        assert rp['explicit_B22_entry_ROM_fixture'] and rp['source_event175_not_selected']
        assert rp['all_source39_commands_23_progressive9_FE_resource_three_presentations_C200_and_two_ends_retained']
        assert sha(Path(rp['fixture_manifest']).read_bytes())==rp['fixture_manifest_sha256']==sha(PLAN.read_bytes())
        assert not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact']
        assert all(not v for k,v in report.items() if k.startswith('synthetic_'))
        assert sha(Path(rp['original_inputs']).read_bytes())==rp['inputs_sha256']
        blocks=IlnkContainer.parse(NdsImage.open(fixture['research_ROM']).read_file('/data/SC2.DK4')).blocks
        block=blocks[22];assert sha(block)==fixture['fixture_block_sha256']
        photos={}
        for photo in report['frames_captured']:
            path=Path(photo['path']);assert sha(path.read_bytes())==photo['PNG_sha256']
            picture=Image.open(path).convert('RGB');assert picture.size==(256,384);photos[photo['frame']]=(photo,picture)
        snapshot=report['read_only_RAM_snapshot']
        assert snapshot['read_only_export'] and snapshot['bytes']==4194304
        assert sha(Path(snapshot['path']).read_bytes())==snapshot['sha256']
        by_at={r['fixture_command_offset']:r for r in fixture['original_text_records']}
        commands={r['fixture_offset']:r for r in fixture['selected_original_objects']}
        rows=trace['rows'];pairs=[];intervals=[]
        for row in rows:
            assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
            source=row['source'];assert source['classification']=='original_SC_cache' and source['route']==2
            assert source['whole_resident_payload_exact_ROM'] and source['actual_sha256']==sha(blocks[source['block']])
            assert source['block']!=175
            if row['kind']!='after_command':continue
            entry=rows[row['entry_row']];source=entry['source'];at=source['instruction_offset']
            word=int.from_bytes(blocks[source['block']][at:at+2],'little')
            pair=dict(block=source['block'],offset=at,word=word,start=entry['frame'],returned=row['frame'],
                extent=row['decoded_length'],result_words=row['result_words']);pairs.append(pair)
            if source['block']!=22:continue
            if at in commands:
                assert word==commands[at]['source_word']
                pair.update(original_source_block=175,original_source_offset=commands[at]['source_offset'])
            if word==0x4000:
                record=by_at[at];assert block[at:at+record['native_extent']].hex()==record['whole_command_hex']
                intervals.append(dict(id=record['id'],start=entry['frame'],returned=row['frame'],offset=at,prefix=record['source_selector']))
        selected=[r for r in pairs if r['block']==22]
        expected=[c['offset'] for c in fixture['original_B22_prelude_commands']]
        for command in fixture['selected_original_objects']:
            expected.append(command['fixture_offset'])
            if command['source_word']==0:break
        assert len(selected)==len(expected)==47 and [r['offset'] for r in selected]==expected
        assert len(intervals)==len({r['id'] for r in intervals})==32
        assert [r['id'] for r in intervals]==[r['id'] for r in fixture['original_text_records']]
        assert sum(r['prefix']==254 for r in intervals)==9
        assert selected[-1]['word']==0 and selected[-1]['original_source_offset']==1702 and selected[-1]['result_words']==[0,0]
        assert not any(r.get('original_source_offset')==1706 for r in selected)
        assert sum(r['word']==0xA000 for r in selected)==4
        assert not any(r['word'] in [0x8000,0x100,0x200,0x300,0x400,0x2100,0x4100,0x2000] for r in selected)
        presentations=[r for r in selected if r.get('original_source_block')==175 and r['word'] in [0x6000,0x4696,0x4635]]
        assert [r['word'] for r in presentations]==[0x6000,0x4696,0x4635]
        resources=[r for r in selected if r.get('original_source_block')==175 and r['word']&0xFF00==0x6300]
        assert [r['word'] for r in resources]==[0x6344]
        ui=[r for r in selected if r['word']==0xC200]
        assert len(ui)==1 and ui[0]['original_source_offset']==1700 and ui[0]['result_words']==[3,0]
        assert intervals[-1]['returned']<=ui[0]['start']<=ui[0]['returned']<=selected[-1]['start']
        for pending in trace['unreturned_at_capture_end']:assert pending['source']['block']!=22
        versions.append(dict(case=case,research_ROM=fixture['research_ROM'],research_ROM_sha256=fixture['research_ROM_sha256'],
            capture_report=str(paths[2]),observer_report=str(paths[3]),selected_B22_command_pairs=selected,selected_intervals=intervals,
            input_schedule=rp['original_inputs'],input_schedule_sha256=rp['inputs_sha256'],
            source_three_presentations=presentations,source_resource=resources,source_C200=ui[0],fixture_exit_frame=selected[-1]['returned'],
            first_source_end1702_actually_reached=True,second_source_end1706_stored_but_unvisited_offline_decoder_only=True,
            following_observed_blocks=sorted({r['block'] for r in pairs if r['block']!=22})))
        photosets[case]=photos;evidence.update({str(p):sha(p.read_bytes()) for p in paths})
    shape=lambda v:[(r.get('original_source_offset'),r['word'],r['result_words']) for r in v['selected_B22_command_pairs']]
    assert shape(versions[0])==shape(versions[1]) and versions[0]['input_schedule_sha256']==versions[1]['input_schedule_sha256']
    byid={r['id']:r for r in font['cases']};source_intervals={r['id']:r for r in versions[0]['selected_intervals']}
    actual=[];panels=[];failures=[];region_differences=[]
    for interval in versions[1]['selected_intervals']:
        case=byid[interval['id']];preview=Image.open(case['preview']).convert('RGB')
        assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
        assert preview.height==64 and preview.width==(228 if interval['prefix']==254 else 216)
        ink0={(x,y) for y in range(64) for x in range(preview.width) if preview.getpixel((x,y))==(0,8,0)}
        gray0={(x,y) for y in range(64) for x in range(preview.width) if preview.getpixel((x,y))==(98,97,98)}
        source_interval=source_intervals[interval['id']];holds=[]
        for frame,(photo,picture) in photosets['reviewed_English'].items():
            if not max(interval['start'],source_interval['start'])<frame<min(interval['returned'],source_interval['returned']):continue
            ink={(x,y) for y in range(64) for x in range(preview.width) if picture.getpixel((16+x,296+y))==(0,8,0)}
            gray={(x,y) for y in range(64) for x in range(preview.width) if picture.getpixel((16+x,296+y))==(98,97,98)}
            if ink!=ink0 or gray!=gray0:continue
            source_photo,source_picture=photosets['clean_Japanese'][frame]
            regions_equal=(picture.crop((0,192,256,294)).tobytes()==source_picture.crop((0,192,256,294)).tobytes()
                           and picture.crop((0,0,256,192)).tobytes()==source_picture.crop((0,0,256,192)).tobytes())
            if not regions_equal:
                region_differences.append(dict(id=interval['id'],frame=frame,native_text_plane_exact=True,paired_nontext_region_differs=True,not_masked_or_retimed=True));continue
            holds.append(dict(frame=frame,capture=photo['path'],capture_sha256=photo['PNG_sha256'],clean_capture=source_photo['path'],
                clean_capture_sha256=source_photo['PNG_sha256'],complete_ink_gray_masks_equal_native_plane=True,
                portrait_name_picture_and_upper_regions_equal_Japanese=True))
            evidence[photo['path']]=photo['PNG_sha256'];evidence[source_photo['path']]=source_photo['PNG_sha256']
        if not holds:failures.append(dict(id=interval['id'],prefix=interval['prefix'],finding='No complete native plane with paired nontext regions in the shared holding interval.'))
        else:panels.append((interval['id'],interval['prefix'],Image.open(holds[0]['capture']).convert('RGB').crop((0,192,256,384))))
        actual.append(dict(id=interval['id'],prefix=interval['prefix'],consumer='FE-paper' if interval['prefix']==254 else 'progressive',
            native_plane_sha256=case['whole_native_plane_sha256'],interval=interval,holds=holds,actually_displayed_in_disclosed_B22_fixture=True))
    assert len(actual)==32 and sum(r['prefix']==254 for r in actual)==9
    ROOT.mkdir(parents=True);sheets=[]
    for start in range(0,len(panels),6):
        sheet=Image.new('RGB',(1560,832),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(ident,prefix,picture) in enumerate(panels[start:start+6]):
            x,y=i%3*520,i//3*416;draw.text((x+4,y+3),f'{ident} / {prefix:02X} / actual B175 content',fill='white')
            sheet.paste(picture.resize((512,384),Image.Resampling.NEAREST),(x+4,y+24))
        path=ROOT/f'actual_consumer_sheet{start//6+1}.png';sheet.save(path);sheets.append(dict(path=str(path),sha256=sha(path.read_bytes())))
    counts=Counter(r['word'] for r in versions[1]['selected_B22_command_pairs'])
    save(ROOT/'actual_all32_progressive_FE_controls_C200_and_first_end.json',dict(versions=versions,actual_panels=actual,
        fresh_actual_unique_speech_panels=32,complete_matching_observations=sum(bool(r['holds']) for r in actual),
        offline_only_display_IDs=[],failures=failures,paired_region_differences=region_differences,review_sheets=sheets,visual_review_pending=True,
        actual_new_cold_boot_runs=2,frames_per_boot=16001,selected_command_counts={format(w,'04X'):n for w,n in counts.items()},
        all39_source_commands_stored_and47_of48_fixture_commands_actually_selected=True,
        all32_unconditional_speeches23_progressive9_FE_observed=True,second_declared_end1706_offline_native_only=True,
        three_presentations_resource_C200_and_first_end_actually_executed_without_source_omission=True,
        source_packed_presentation_semantics_and_anonymous_woman_identity_not_inferred=True,
        actual_source_event175_not_selected=True,no_earned_flags_natural_eligibility_full_playthrough_or_hardware_claim=True,
        evidence=evidence,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(actual_panels=32,FE=9,complete_matching_observations=sum(bool(r['holds']) for r in actual),failures=failures,nontext_differences=len(region_differences)),flush=True)
    if failures:raise SystemExit(1)
