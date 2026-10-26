"""Audit terminal source/English cold boots and all13 focused consumer panels."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B142_B145_actual_v3603')
PLAN=Path('work/analysis/lil_B142_B145_display_fixture_v3601/explicit_source_consumer_B22_fixtures.json')
FONT=Path('work/analysis/lil_B142_B145_native_approval_v3590/all38_native_macro_font_and_source_reconciliation.json')
CAPBASE=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
if __name__=='__main__':
    assert not ROOT.exists();plan,font=map(read,[PLAN,FONT]);versions=[];allphotos={};evidence={str(p):sha(p.read_bytes()) for p in [PLAN,FONT,Path(__file__)]}
    for case in ['clean_Japanese','reviewed_English']:assert read(Path('work/analysis/lil_B142_B145_display_run_v3602_'+case)/'terminal.json')['terminal']
    for fixture in plan['fixtures']:
        case=fixture['case'];run=Path('work/analysis/lil_B142_B145_display_run_v3602_'+case);cap=CAPBASE/('lil_B142_B145_display_v3602_'+case);paths=[run/'terminal.json',run/'run_plan.json',cap/'capture_report.json',cap/'observer/commands.json'];terminal,rp,report,trace=map(read,paths);assert terminal['terminal'] and terminal['observer_host_slots_restored'] and terminal['observer_instances']==1 and report['frames']==8601 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'];assert sha(Path(fixture['research_ROM']).read_bytes())==fixture['research_ROM_sha256']==report['ROM_sha256']==rp['research_ROM_sha256'];assert rp['explicit_B22_entry_ROM_fixture'] and rp['source_events142_to145_not_selected'] and sha(Path(rp['fixture_manifest']).read_bytes())==rp['fixture_manifest_sha256']==sha(PLAN.read_bytes());assert not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact'];assert all(not v for k,v in report.items() if k.startswith('synthetic_'));assert sha(Path(rp['original_inputs']).read_bytes())==rp['inputs_sha256']
        image=NdsImage.open(fixture['research_ROM']);blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;assert sha(blocks[22])==fixture['fixture_block_sha256'];photos={}
        for photo in report['frames_captured']:
            p=Path(photo['path']);assert sha(p.read_bytes())==photo['PNG_sha256'];pic=Image.open(p).convert('RGB');assert pic.size==(256,384);photos[photo['frame']]=(photo,pic)
        for snap in report.get('read_only_capture_RAM_snapshots',[])+report.get('read_only_pause_RAM_snapshots',[])+[report['read_only_RAM_snapshot']]:assert snap['read_only_export'] and snap['bytes']==4194304 and sha(Path(snap['path']).read_bytes())==snap['sha256']
        rows=trace['rows'];pairs=[];intervals=[];byat={r['fixture_command_offset']:r for r in fixture['original_text_records']}
        for r in rows:
            assert r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'];s=r['source'];assert s['classification']=='original_SC_cache' and s['route']==2 and s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==sha(blocks[s['block']]);assert s['block'] not in [142,143,144,145]
            if r['kind']!='after_command':continue
            entry=rows[r['entry_row']];s=entry['source'];at=s['instruction_offset'];word=int.from_bytes(blocks[s['block']][at:at+2],'little');pair=dict(block=s['block'],offset=at,word=word,start=entry['frame'],returned=r['frame'],extent=r['decoded_length'],result_words=r['result_words']);pairs.append(pair)
            if s['block']==22 and word==0x4000:rec=byat[at];assert blocks[22][at:at+rec['native_extent']].hex()==rec['whole_command_hex'];intervals.append(dict(id=rec['id'],start=entry['frame'],returned=r['frame'],offset=at,prefix=rec['source_selector']))
        selected=[r for r in pairs if r['block']==22];assert len(selected)==28 and [r['word'] for r in selected]==fixture['expected_command_words'] and selected[-1]['word']==0 and selected[-1]['result_words']==[0,0] and len(intervals)==13 and len({r['id'] for r in intervals})==13
        for pending in trace['unreturned_at_capture_end']:assert rows[pending['entry_row']]['source']['block']!=22
        versions.append(dict(case=case,ROM_sha256=report['ROM_sha256'],frames=8601,input_schedule=rp['original_inputs'],input_schedule_sha256=rp['inputs_sha256'],capture_report=str(cap/'capture_report.json'),observer_report=str(cap/'observer/commands.json'),selected_B22_command_pairs=selected,selected_intervals=intervals,all28_fixture_commands_and13_speeches_return_normally=True,fixture_exit_frame=selected[-1]['returned'],following_observed_blocks=sorted({p['block'] for p in pairs if p['block']!=22}),following_pending_objects=trace['unreturned_at_capture_end'],later_pending_objects_are_outside_completed_fixture=True));allphotos[case]=photos
        for p in paths:evidence[str(p)]=sha(p.read_bytes())
    assert versions[0]['input_schedule_sha256']==versions[1]['input_schedule_sha256'];byid={r['id']:r for r in font['cases']};source_intervals={r['id']:r for r in versions[0]['selected_intervals']};actual=[];pictures=[];failures=[]
    for interval in versions[1]['selected_intervals']:
        c=byid[interval['id']];preview=Image.open(c['preview']).convert('RGB');assert sha(Path(c['preview']).read_bytes())==c['preview_sha256'];width=preview.width;assert preview.height==64 and width in [216,228];expected_ink={(x,y) for y in range(64) for x in range(width) if preview.getpixel((x,y))==(0,8,0)};expected_gray={(x,y) for y in range(64) for x in range(width) if preview.getpixel((x,y))==(98,97,98)};holds=[];src=source_intervals[interval['id']]
        for frame,(photo,pic) in allphotos['reviewed_English'].items():
            if not max(interval['start'],src['start'])<frame<min(interval['returned'],src['returned']):continue
            ink={(x,y) for y in range(64) for x in range(width) if pic.getpixel((16+x,296+y))==(0,8,0)};gray={(x,y) for y in range(64) for x in range(width) if pic.getpixel((16+x,296+y))==(98,97,98)}
            if ink!=expected_ink or gray!=expected_gray:continue
            sourcephoto,sourcepic=allphotos['clean_Japanese'][frame];assert pic.crop((0,192,256,294)).tobytes()==sourcepic.crop((0,192,256,294)).tobytes();assert pic.crop((0,0,256,192)).tobytes()==sourcepic.crop((0,0,256,192)).tobytes();holds.append(dict(frame=frame,capture=photo['path'],capture_sha256=photo['PNG_sha256'],clean_capture=sourcephoto['path'],clean_capture_sha256=sourcephoto['PNG_sha256'],complete_ink_and_gray_glyph_masks_equal_native_plane=True,complete_portrait_name_and_picture_region_equal_source_fixture=True,complete_upper_scene_region_equal_source_fixture=True));evidence[photo['path']]=photo['PNG_sha256'];evidence[sourcephoto['path']]=sourcephoto['PNG_sha256']
        if not holds:failures.append(dict(id=interval['id'],prefix=interval['prefix'],finding='No complete ink-and-gray/native plane match in captured holding interval.'))
        else:pictures.append((interval['id'],interval['prefix'],Image.open(holds[0]['capture']).convert('RGB').crop((0,192,256,384))))
        actual.append(dict(id=interval['id'],prefix=interval['prefix'],consumer='FE-paper' if interval['prefix']==254 else 'progressive',native_plane_sha256=c['whole_native_plane_sha256'],interval=interval,holds=holds))
    ROOT.mkdir(parents=True);sheets=[]
    for start in range(0,len(pictures),4):
        sheet=Image.new('RGB',(1040,832),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(ident,prefix,pic) in enumerate(pictures[start:start+4]):
            x,y=i%2*520,i//2*416;draw.text((x+4,y+4),ident+' / '+format(prefix,'02X')+' / actual B22 fixture',fill='white');sheet.paste(pic.resize((512,384),Image.Resampling.NEAREST),(x+4,y+24))
        p=ROOT/f'actual_consumer_sheet{start//4+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    save(ROOT/'actual_source_English_13panels_portraits_pictures_FE_and_return.json',dict(versions=versions,fixture_manifest=str(PLAN),fixture_manifest_sha256=sha(PLAN.read_bytes()),native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),actual_panels=actual,complete_matching_panels=sum(bool(r['holds']) for r in actual),complete_matching_holds=sum(len(r['holds']) for r in actual),failures=failures,review_sheets=sheets,visual_review_pending=True,all28_fixture_commands_and13_speeches_normal_return=True,actual_selected_source_B142_B145_events=False,actual_new_cold_boot_runs=2,fixture_entry_block22_not_source_event_eligibility=True,original_B22_initialization_preserved=True,later_upgrade_inventory_progression_effects_excluded=True,portrait_name_picture_comparisons_are_complete_region_pairs_in_same_initialized_fixture=True,patterned_paper_background_not_claimed_equal_to_flat_native_preview=True,actual_Cesare13_Shipwright109_and_FE_nullactor_behavior_targeted=True,actual_cloth_lamp_map_picture_hide_C200_and_normal_exit_targeted=True,not_natural_complete_B144_exchange_or_earned_outcome_or_full_route_or_hardware_proof=True,evidence=evidence,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    assert not failures,failures;print('Two actual8601frame cold boots:all28fixture commands/13speeches return;all13native ink-gray planes/portraits/names/pictures match. Four sheets need visual review;not natural source eligibility.')
