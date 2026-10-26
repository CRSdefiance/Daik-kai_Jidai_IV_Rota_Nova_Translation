"""Audit four terminal cold boots with both real advice choices and all47 unique speech panels."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import verify_ship_advice_choice_centering_20261022 as painter_base
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B164_actual_v3996')
PLAN=Path('work/analysis/lil_B164_display_fixture_v3992/complete_choice_preserving_B22_fixtures.json')
FONT=Path('work/analysis/lil_B164_native_approval_v3984/all49_native_speech_choice_and_source_reconciliation.json')
MENU=Path('work/analysis/lil_B164_choices_v3975/B164_C1654/original_choice_decoder_VM_geometry_and_native_pixels.json')
CAPBASE=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
if __name__=='__main__':
    assert not ROOT.exists();plan,font,menu=map(read,[PLAN,FONT,MENU]);versions=[];photosets={};evidence={str(p):sha(p.read_bytes()) for p in [PLAN,FONT,MENU,Path(__file__)]}
    for option in [0,1]:
        for fixture in plan['fixtures']:assert read(Path(f"work/analysis/lil_B164_display_run_v3993_O{option}_"+fixture['case'])/'terminal.json')['terminal']
    for option in [0,1]:
        for fixture in plan['fixtures']:
            case=fixture['case'];fid=f'O{option}_{case}';run=Path('work/analysis/lil_B164_display_run_v3993_'+fid);cap=CAPBASE/('lil_B164_display_v3993_'+fid);paths=[run/'terminal.json',run/'run_plan.json',cap/'capture_report.json',cap/'observer/commands.json'];terminal,rp,report,trace=map(read,paths);assert terminal['terminal'] and terminal['observer_host_slots_restored'] and terminal['observer_instances']==1 and report['frames']==20001 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'];assert sha(Path(fixture['research_ROM']).read_bytes())==fixture['research_ROM_sha256']==report['ROM_sha256']==rp['research_ROM_sha256'];assert rp['explicit_B22_entry_ROM_fixture'] and rp['source_event164_not_selected'] and rp['requested_advice_option']==option and sha(Path(rp['fixture_manifest']).read_bytes())==rp['fixture_manifest_sha256']==sha(PLAN.read_bytes());assert not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact'];assert all(not v for k,v in report.items() if k.startswith('synthetic_'));assert sha(Path(rp['original_inputs']).read_bytes())==rp['inputs_sha256'];blocks=IlnkContainer.parse(NdsImage.open(fixture['research_ROM']).read_file('/data/SC2.DK4')).blocks;block=blocks[22];assert sha(block)==fixture['fixture_block_sha256'];photos={}
            for photo in report['frames_captured']:
                p=Path(photo['path']);assert sha(p.read_bytes())==photo['PNG_sha256'];pic=Image.open(p).convert('RGB');assert pic.size==(256,384);photos[photo['frame']]=(photo,pic)
            snap=report['read_only_RAM_snapshot'];assert snap['read_only_export'] and snap['bytes']==4194304 and sha(Path(snap['path']).read_bytes())==snap['sha256'];rows=trace['rows'];pairs=[];intervals=[];byat={r['fixture_command_offset']:r for r in fixture['original_text_records']};commands={r['fixture_offset']:r for r in fixture['selected_original_objects']}
            for r in rows:
                assert r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'];s=r['source'];assert s['classification']=='original_SC_cache' and s['route']==2 and s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==sha(blocks[s['block']]) and s['block']!=164
                if r['kind']!='after_command':continue
                entry=rows[r['entry_row']];s=entry['source'];at=s['instruction_offset'];word=int.from_bytes(blocks[s['block']][at:at+2],'little');pair=dict(block=s['block'],offset=at,word=word,start=entry['frame'],returned=r['frame'],extent=r['decoded_length'],result_words=r['result_words']);pairs.append(pair)
                if s['block']!=22:continue
                if at in commands:assert word==commands[at]['source_word'];pair.update(original_source_block=164,original_source_offset=commands[at]['source_offset'])
                if word==0x4000:rec=byat[at];assert block[at:at+rec['native_extent']].hex()==rec['whole_command_hex'];intervals.append(dict(id=rec['id'],start=entry['frame'],returned=r['frame'],offset=at,prefix=rec['source_selector']))
            selected=[r for r in pairs if r['block']==22];assert selected[-1]['word']==0 and selected[-1]['result_words']==[0,0];assert len(intervals)==len({r['id'] for r in intervals})==[45,31][option];assert len(selected)==[64,49][option];menus=[r for r in selected if r['word']==0x2100];assert len(menus)==1 and menus[0]['result_words']==[2,option];assert sum(r['word']==0xA000 for r in selected)==4 and not any(r['word']==0xA000 and r.get('original_source_block')==164 for r in selected);assert sum(r['word']==0x632B for r in selected)==(1 if option==0 else 0)
            native={r['offset']:r for r in fixture['all69_stored_fixture_commands']};cursor=8;expected=[]
            while True:
                command=native[cursor];word=command['word'];expected.append(cursor)
                if word==0:break
                if word in [0x100,0x200,0x300,0x400]:span=int.from_bytes(block[cursor+2:cursor+4],'little');take=word==0x100 or option==word//256-2;cursor+=4+(span if take else 0)
                else:cursor+=command['native_extent']
            assert [r['offset'] for r in selected]==expected
            for pending in trace['unreturned_at_capture_end']:assert rows[pending['entry_row']]['source']['block']!=22
            versions.append(dict(case=case,option_index=option,source_block=164,ROM_sha256=report['ROM_sha256'],frames=report['frames'],input_schedule=rp['original_inputs'],input_schedule_sha256=rp['inputs_sha256'],capture_report=str(cap/'capture_report.json'),observer_report=str(cap/'observer/commands.json'),selected_B22_command_pairs=selected,selected_intervals=intervals,actual_choice_command_pair=menus[0],fixture_exit_frame=selected[-1]['returned'],source_end_offset=selected[-1]['original_source_offset'],following_observed_blocks=sorted({p['block'] for p in pairs if p['block']!=22}),all_retained_branch_commands_follow_native_source_outcome=True,all_selected_speeches_and_commands_return_normally=True));photosets[option,case]=photos
            for p in paths:evidence[str(p)]=sha(p.read_bytes())
    byversion={(v['option_index'],v['case']):v for v in versions};shape=lambda v:[(r.get('original_source_offset'),r['word'],r['result_words']) for r in v['selected_B22_command_pairs']]
    for option in [0,1]:assert shape(byversion[option,'clean_Japanese'])==shape(byversion[option,'reviewed_English']);assert byversion[option,'reviewed_English']['source_end_offset']==[3454,1854][option]
    byid={r['id']:r for r in font['cases']};observations=[];unique={};failures=[]
    for option in [0,1]:
        source_intervals={r['id']:r for r in byversion[option,'clean_Japanese']['selected_intervals']}
        for interval in byversion[option,'reviewed_English']['selected_intervals']:
            c=byid[interval['id']];preview=Image.open(c['preview']).convert('RGB');assert sha(Path(c['preview']).read_bytes())==c['preview_sha256'];ink0={(x,y) for y in range(64) for x in range(216) if preview.getpixel((x,y))==(0,8,0)};gray0={(x,y) for y in range(64) for x in range(216) if preview.getpixel((x,y))==(98,97,98)};src=source_intervals[interval['id']];holds=[]
            for frame,(photo,pic) in photosets[option,'reviewed_English'].items():
                if not max(interval['start'],src['start'])<frame<min(interval['returned'],src['returned']):continue
                ink={(x,y) for y in range(64) for x in range(216) if pic.getpixel((16+x,296+y))==(0,8,0)};gray={(x,y) for y in range(64) for x in range(216) if pic.getpixel((16+x,296+y))==(98,97,98)}
                if ink!=ink0 or gray!=gray0:continue
                sourcephoto,sourcepic=photosets[option,'clean_Japanese'][frame];assert pic.crop((0,192,256,294)).tobytes()==sourcepic.crop((0,192,256,294)).tobytes() and pic.crop((0,0,256,192)).tobytes()==sourcepic.crop((0,0,256,192)).tobytes();holds.append(dict(frame=frame,capture=photo['path'],capture_sha256=photo['PNG_sha256'],clean_capture=sourcephoto['path'],clean_capture_sha256=sourcephoto['PNG_sha256'],complete_ink_gray_masks_equal_native_plane=True,portrait_name_picture_and_upper_regions_equal_Japanese=True));evidence[photo['path']]=photo['PNG_sha256'];evidence[sourcephoto['path']]=sourcephoto['PNG_sha256']
            if not holds:failures.append(dict(id=interval['id'],option_index=option,finding='No complete native plane inside shared holding interval.'))
            record=dict(id=interval['id'],option_index=option,prefix=interval['prefix'],native_plane_sha256=c['whole_native_plane_sha256'],interval=interval,holds=holds,actually_displayed_in_disclosed_B22_fixture=True);observations.append(record)
            if holds and interval['id'] not in unique:unique[interval['id']]=record
    arm=NdsImage.open(plan['parent']).read_file('/__arm9__.bin');env={**painter_base.__dict__,'LABEL_WIDTH':48,'sha':sha};exec(compile(menu['source_derived_painter_adapter'],__file__+'::exact-menu-painter','exec'),env);label_masks=[]
    for text in [b'Yes',b'No']:pixels,proof=env['paint'](arm,text,1);label_masks.append({(x,y) for y in range(20) for x in range(48) if pixels[y*48+x]})
    actualmenus=[]
    for option in [0,1]:
        interval=byversion[option,'reviewed_English']['actual_choice_command_pair'];holds=[]
        for frame,(photo,pic) in photosets[option,'reviewed_English'].items():
            if not interval['start']+30<frame<interval['returned']:continue
            for i,expected in enumerate(label_masks):
                actual={(x,y) for y in range(20) for x in range(48) if pic.getpixel((104+x,268+20*i+y))==(8,8,8)};assert actual==expected
                assert pic.getpixel((104,268+20*i))==((0,165,172) if i==option else (205,198,180))
            holds.append(dict(frame=frame,path=photo['path'],sha256=photo['PNG_sha256'],all72_Yes_No_foreground_pixels_equal_original_native_planes=True,selected_style_matches_returned_option=True));evidence[photo['path']]=photo['PNG_sha256']
        assert holds;actualmenus.append(dict(option_index=option,native_result_words=interval['result_words'],text_canvas_origins=[[104,268],[104,288]],holds=holds))
    assert len(observations)==76 and len(unique)==47 and {r['prefix'] for r in observations}=={2,9,13};ROOT.mkdir(parents=True);panels=[(ident,r['prefix'],Image.open(r['holds'][0]['capture']).convert('RGB').crop((0,192,256,384))) for ident,r in unique.items()];sheets=[]
    for start in range(0,len(panels),6):
        sheet=Image.new('RGB',(1560,832),'#263238');draw=ImageDraw.Draw(sheet)
        for j,(ident,prefix,pic) in enumerate(panels[start:start+6]):x,y=j%3*520,j//3*416;draw.text((x+4,y+3),f'{ident} / {prefix:02X} / actual retained-choice B22 fixture',fill='white');sheet.paste(pic.resize((512,384)),(x+4,y+24))
        p=ROOT/f'actual_consumer_sheet{start//6+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    assert len(sheets)==8;save(ROOT/'actual_both_choices47_unique_panels76_observations_and_separated_returns.json',dict(versions=versions,actual_panels=list(unique.values()),all76_actual_speech_observations=observations,actual_menu_cases=actualmenus,fresh_actual_unique_speech_panels=47,actual_English_speech_observations=76,complete_matching_observations=sum(bool(r['holds']) for r in observations),failures=failures,review_sheets=sheets,visual_review_pending=True,actual_new_cold_boot_runs=4,all4_original_relative_commands_retained_not_flattened=True,both_real_choice_values_and_two_separated_ends_observed=True,actual_source_event164_not_selected=True,no_earned_recruitment_or_natural_Alexandria_activation_or_full_playthrough_or_hardware_claim=True,original_nine_B22_init_commands_preserved_one_later_recruitment_effect_omitted=True,evidence=evidence,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));assert not failures,failures;print(dict(unique_panels=47,observations=76,complete_matches=sum(bool(r['holds']) for r in observations),actual_menu_values=[r['native_result_words'] for r in actualmenus],commands=[64,49],exits=[(v['option_index'],v['case'],v['fixture_exit_frame']) for v in versions],sheets=8,visual_review_pending=True))
