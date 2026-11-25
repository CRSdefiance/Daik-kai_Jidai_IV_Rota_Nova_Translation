"""Audit terminal fixture traces and every actually selected English text plane."""
from collections import Counter
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B152_B154_actual_v3647')
PLAN=Path('work/analysis/lil_B152_B154_display_fixture_v3644b/explicit_source_consumer_B22_fixtures.json')
FONT=Path('work/analysis/lil_B152_B154_native_approval_v3635/all59_native_macro_font_and_source_reconciliation.json')
CAPBASE=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
if __name__=='__main__':
    assert not ROOT.exists();plan,font=map(read,[PLAN,FONT]);versions=[];photosets={};evidence={str(p):sha(p.read_bytes()) for p in [PLAN,FONT,Path(__file__)]}
    for case in ['clean_Japanese','reviewed_English']:assert read(Path('work/analysis/lil_B152_B154_display_run_v3645b_'+case)/'terminal.json')['terminal']
    for fixture in plan['fixtures']:
        case=fixture['case'];run=Path('work/analysis/lil_B152_B154_display_run_v3645b_'+case);cap=CAPBASE/('lil_B152_B154_display_v3645b_'+case);paths=[run/'terminal.json',run/'run_plan.json',cap/'capture_report.json',cap/'observer/commands.json'];terminal,rp,report,trace=map(read,paths);assert terminal['terminal'] and terminal['observer_host_slots_restored'] and terminal['observer_instances']==1 and report['frames']==24401 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'];assert sha(Path(fixture['research_ROM']).read_bytes())==fixture['research_ROM_sha256']==report['ROM_sha256']==rp['research_ROM_sha256'];assert rp['explicit_B22_entry_ROM_fixture'] and rp['source_events152_to154_not_selected'] and sha(Path(rp['fixture_manifest']).read_bytes())==rp['fixture_manifest_sha256']==sha(PLAN.read_bytes());assert not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact'];assert all(not v for k,v in report.items() if k.startswith('synthetic_'));assert sha(Path(rp['original_inputs']).read_bytes())==rp['inputs_sha256'];blocks=IlnkContainer.parse(NdsImage.open(fixture['research_ROM']).read_file('/data/SC2.DK4')).blocks;assert sha(blocks[22])==fixture['fixture_block_sha256'];photos={}
        for photo in report['frames_captured']:
            p=Path(photo['path']);assert sha(p.read_bytes())==photo['PNG_sha256'];pic=Image.open(p).convert('RGB');assert pic.size==(256,384);photos[photo['frame']]=(photo,pic)
        snap=report['read_only_RAM_snapshot'];assert snap['read_only_export'] and snap['bytes']==4194304 and sha(Path(snap['path']).read_bytes())==snap['sha256'];rows=trace['rows'];pairs=[];intervals=[];byat={r['fixture_command_offset']:r for r in fixture['original_text_records']};commands={r['fixture_offset']:r for r in fixture['selected_original_objects']}
        for r in rows:
            assert r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'];s=r['source'];assert s['classification']=='original_SC_cache' and s['route']==2 and s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==sha(blocks[s['block']]);assert s['block'] not in [152,153,154]
            if r['kind']!='after_command':continue
            entry=rows[r['entry_row']];s=entry['source'];at=s['instruction_offset'];word=int.from_bytes(blocks[s['block']][at:at+2],'little');pair=dict(block=s['block'],offset=at,word=word,start=entry['frame'],returned=r['frame'],extent=r['decoded_length'],result_words=r['result_words']);pairs.append(pair)
            if s['block']!=22:continue
            if at in commands:assert word==commands[at]['source_word'];pair.update(original_source_block=commands[at]['source_block'],original_source_offset=commands[at]['source_offset'])
            if word==0x4000:rec=byat[at];assert blocks[22][at:at+rec['native_extent']].hex()==rec['whole_command_hex'];intervals.append(dict(id=rec['id'],start=entry['frame'],returned=r['frame'],offset=at,prefix=rec['source_selector']))
        selected=[r for r in pairs if r['block']==22];assert selected and selected[-1]['word']==0 and selected[-1]['result_words']==[0,0] and len(intervals)==len({r['id'] for r in intervals});assert sum(r['word']==0x2000 for r in selected)==1 and sum(r['word']==0xA000 for r in selected)==0
        for pending in trace['unreturned_at_capture_end']:assert rows[pending['entry_row']]['source']['block']!=22
        versions.append(dict(case=case,ROM_sha256=report['ROM_sha256'],frames=24401,input_schedule=rp['original_inputs'],input_schedule_sha256=rp['inputs_sha256'],capture_report=str(cap/'capture_report.json'),observer_report=str(cap/'observer/commands.json'),selected_B22_command_pairs=selected,selected_intervals=intervals,all_selected_fixture_commands_and_speeches_return_normally=True,fixture_exit_frame=selected[-1]['returned'],following_observed_blocks=sorted({p['block'] for p in pairs if p['block']!=22}),following_pending_objects=trace['unreturned_at_capture_end'],later_pending_objects_are_outside_completed_fixture=True));photosets[case]=photos
        for p in paths:evidence[str(p)]=sha(p.read_bytes())
    assert versions[0]['input_schedule_sha256']==versions[1]['input_schedule_sha256'];shape=lambda v:[(r.get('original_source_block'),r.get('original_source_offset'),r['word'],r['result_words']) for r in v['selected_B22_command_pairs']];assert shape(versions[0])==shape(versions[1]);byid={r['id']:r for r in font['cases']};srcintervals={r['id']:r for r in versions[0]['selected_intervals']};actual=[];panels=[];failures=[]
    for interval in versions[1]['selected_intervals']:
        c=byid[interval['id']];preview=Image.open(c['preview']).convert('RGB');assert sha(Path(c['preview']).read_bytes())==c['preview_sha256'] and preview.size==(216,64);ink0={(x,y) for y in range(64) for x in range(216) if preview.getpixel((x,y))==(0,8,0)};gray0={(x,y) for y in range(64) for x in range(216) if preview.getpixel((x,y))==(98,97,98)};holds=[];src=srcintervals[interval['id']]
        for frame,(photo,pic) in photosets['reviewed_English'].items():
            if not max(interval['start'],src['start'])<frame<min(interval['returned'],src['returned']):continue
            ink={(x,y) for y in range(64) for x in range(216) if pic.getpixel((16+x,296+y))==(0,8,0)};gray={(x,y) for y in range(64) for x in range(216) if pic.getpixel((16+x,296+y))==(98,97,98)}
            if ink!=ink0 or gray!=gray0:continue
            sourcephoto,sourcepic=photosets['clean_Japanese'][frame];assert pic.crop((0,192,256,294)).tobytes()==sourcepic.crop((0,192,256,294)).tobytes() and pic.crop((0,0,256,192)).tobytes()==sourcepic.crop((0,0,256,192)).tobytes();holds.append(dict(frame=frame,capture=photo['path'],capture_sha256=photo['PNG_sha256'],clean_capture=sourcephoto['path'],clean_capture_sha256=sourcephoto['PNG_sha256'],complete_ink_and_gray_glyph_masks_equal_native_plane=True,complete_portrait_name_picture_and_upper_scene_regions_equal_source_fixture=True));evidence[photo['path']]=photo['PNG_sha256'];evidence[sourcephoto['path']]=sourcephoto['PNG_sha256']
        if not holds:failures.append(dict(id=interval['id'],prefix=interval['prefix'],finding='No complete native ink-gray mask match inside shared source-English holding interval.'))
        else:panels.append((interval['id'],interval['prefix'],Image.open(holds[0]['capture']).convert('RGB').crop((0,192,256,384))))
        actual.append(dict(id=interval['id'],prefix=interval['prefix'],consumer='progressive',native_plane_sha256=c['whole_native_plane_sha256'],interval=interval,holds=holds))
    ROOT.mkdir(parents=True);sheets=[]
    for start in range(0,len(panels),6):
        sheet=Image.new('RGB',(1560,832),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(ident,prefix,pic) in enumerate(panels[start:start+6]):
            x,y=i%3*520,i//3*416;draw.text((x+4,y+4),ident+' / '+format(prefix,'02X')+' / actual B22 fixture',fill='white');sheet.paste(pic.resize((512,384),Image.Resampling.NEAREST),(x+4,y+24))
        p=ROOT/f'actual_consumer_sheet{start//6+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    counts=Counter(r['word'] for r in versions[1]['selected_B22_command_pairs']);save(ROOT/'actual_source_English_selected_panels_pictures_resources_pause_and_return.json',dict(versions=versions,fixture_manifest=str(PLAN),fixture_manifest_sha256=sha(PLAN.read_bytes()),native_font_proof=str(FONT),native_font_proof_sha256=sha(FONT.read_bytes()),actual_panels=actual,complete_matching_panels=sum(bool(r['holds']) for r in actual),complete_matching_holds=sum(len(r['holds']) for r in actual),selected_command_counts={format(k,'04X'):v for k,v in counts.items()},failures=failures,review_sheets=sheets,visual_review_pending=True,all_selected_fixture_commands_and_speeches_normal_return=True,source_current_command_results_and_selection_match=True,actual_pause2000_resource_controls_picture_hide_C200_and_normal_exit_observed=True,actual_selected_source_B152_B154_events=False,actual_new_cold_boot_runs=2,fixture_entry_block22_not_source_event_eligibility=True,original_B22_initialization_preserved=True,inventory_recruitment_progression_effects_excluded=True,not_earned_items_recruitment_Proof_full_route_or_hardware_proof=True,source_two_endwords_preserved_but_second_not_reachability_claim=True,evidence=evidence,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));assert not failures,failures;print(dict(actual_panels=len(actual),matching_panels=sum(bool(r['holds']) for r in actual),commands=len(versions[1]['selected_B22_command_pairs']),exit_frames=[v['fixture_exit_frame'] for v in versions],sheets=len(sheets),visual_review_pending=True))
