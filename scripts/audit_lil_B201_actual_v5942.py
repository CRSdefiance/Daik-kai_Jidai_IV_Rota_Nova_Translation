"""Pair complete Japanese and reviewed English B201 fixture paths without retiming."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import verify_ship_advice_choice_centering_20261022 as painter_base
from scripts.lil_current_font_oracles_v5918 import CURRENT_ARM9
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B201_actual_v5942')
JP=Path('work/analysis/lil_B201_source_fixture_v5910/complete_B201_source_B22_fixture.json')
EN=Path('work/analysis/lil_B201_English_fixture_v5939b/complete_B201_English_B22_fixture.json')
FONT=Path('work/analysis/lil_B201_fonts_v5923c/all24_progressive_FE_native_planes_and192_alignment_cases.json')
MENU=Path('work/analysis/lil_B201_choices_v5924/B201_C880/original_choice_decoder_VM_geometry_and_native_pixels.json')
PATHS=['buy','decline']
COMMON=[5,8,11,14,18,21,24,27,30,34,37,41,45]

if __name__=='__main__':
    assert not ROOT.exists()
    jp,en,font,menu=map(read,[JP,EN,FONT,MENU]);versions=[];photosets={};seen={};evidence={str(p):sha(p.read_bytes()) for p in [JP,EN,FONT,MENU,Path(__file__)]}
    for path in PATHS:
        for case,manifest,revision,stem in [('clean_Japanese',JP,5911 if path=='buy' else 5913,'source'),('reviewed_English',EN,'5940b' if path=='buy' else '5941b','English')]:
            fixture=read(manifest)['fixtures'][0]
            run=Path(f'work/analysis/lil_B201_{stem}_run_v{revision}_{path}')
            terminal,rp=read(run/'terminal.json'),read(run/'run_plan.json');cap=Path(rp['capture_folder'])
            files=[run/'terminal.json',run/'run_plan.json',cap/'capture_report.json',cap/'observer/commands.json',Path(rp['original_inputs'])]
            report,trace,inputs=map(read,files[2:])
            assert terminal['terminal'] and terminal['observer_host_slots_restored'] and terminal['observer_instances']==1
            assert report['frames']==13001 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
            assert sha(Path(fixture['research_ROM']).read_bytes())==fixture['research_ROM_sha256']==report['ROM_sha256']==rp['research_ROM_sha256']
            assert rp['explicit_B22_entry_ROM_fixture'] and rp['source_event201_not_naturally_selected'] and rp['all44_source_commands_retained']
            assert sha(Path(rp['fixture_manifest']).read_bytes())==rp['fixture_manifest_sha256']==sha(manifest.read_bytes())
            assert not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact']
            assert all(not v for k,v in report.items() if k.startswith('synthetic_')) and not report.get('battery_save_preloaded')
            assert sha(files[-1].read_bytes())==rp['inputs_sha256'] and report['scripted_input_schedule']==inputs
            assert sum(r['buttons']==['DOWN'] for r in inputs)==PATHS.index(path)
            blocks=IlnkContainer.parse(NdsImage.open(fixture['research_ROM']).read_file('/data/SC2.DK4')).blocks;block=blocks[22]
            assert sha(block)==fixture['fixture_block_sha256'];photos={}
            for photo in report['frames_captured']:
                p=Path(photo['path']);assert sha(p.read_bytes())==photo['PNG_sha256'];pic=Image.open(p).convert('RGB');assert pic.size==(256,384);photos[photo['frame']]=(photo,pic)
            snap=report['read_only_RAM_snapshot'];assert snap['read_only_export'] and snap['bytes']==4194304 and sha(Path(snap['path']).read_bytes())==snap['sha256']
            rows=trace['rows'];pairs=[];intervals=[];byat={r['fixture_command_offset']:r for r in fixture['original_text_records']};commands={r['fixture_offset']:r for r in fixture['selected_original_objects']};allseen=set();following=set()
            for r in rows:
                assert r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'];s=r['source']
                assert s['classification']=='original_SC_cache' and s['route']==2 and s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==sha(blocks[s['block']])
                if s['block']!=22:following.add(s['block'])
                if r['kind']!='after_command' or s['block']!=22:continue
                entry=rows[r['entry_row']];at=entry['source']['instruction_offset'];word=int.from_bytes(block[at:at+2],'little');allseen.add(at)
                pair=dict(block=22,offset=at,word=word,start=entry['frame'],returned=r['frame'],extent=r['decoded_length'],result_words=r['result_words'],before_seed=entry['original_RNG_seed'],after_seed=r['original_RNG_seed'],UI_request_after=r['native_UI_request_words'],UI_pending_after=r['native_UI_pending_flag'])
                if at in commands:
                    c=commands[at];assert word==c['source_word'];pair.update(original_source_block=201,original_source_offset=c['source_offset'])
                    assert r['decoded_length']==c['native_extent'] or word in [0x100,0x200,0x300,0x400]
                pairs.append(pair)
                if word==0x4000:
                    rec=byat[at];assert block[at:at+rec['native_extent']].hex()==rec['whole_command_hex']
                    intervals.append(dict(id=rec['id'],source_record_index=rec['source_record_index'],start=entry['frame'],returned=r['frame'],offset=at,prefix=rec['source_selector']))
            choices=[r for r in pairs if r['word']==0x2100];assert len(choices)==1 and choices[0]['original_source_offset']==880 and choices[0]['result_words']==[2,PATHS.index(path)]
            assert pairs[-1]['word']==0 and pairs[-1]['original_source_offset']==1448 and pairs[-1]['result_words']==[0,PATHS.index(path)]
            assert [r['source_record_index'] for r in intervals]==COMMON+({'buy':[59,62,69,73,77,80],'decline':[86,90,94,97,100]}[path])
            seen.setdefault(case,set()).update(allseen)
            versions.append(dict(path=path,case=case,research_ROM=fixture['research_ROM'],research_ROM_sha256=fixture['research_ROM_sha256'],run_folder=str(run),capture_report=str(files[2]),observer_report=str(files[3]),selected_B22_command_pairs=pairs,selected_intervals=intervals,actual_choice_pairs=choices,fixture_exit_frame=pairs[-1]['returned'],final_readonly_RAM_snapshot=snap,whole_final_frame=photos[12970][0],following_observed_blocks=sorted(following),input_schedule_sha256=rp['inputs_sha256']))
            photosets[path,case]=photos;evidence.update({str(p):sha(p.read_bytes()) for p in files})
    for case,fixture in [('clean_Japanese',jp['fixtures'][0]),('reviewed_English',en['fixtures'][0])]:assert seen[case]=={r['offset'] for r in fixture['all53_stored_fixture_commands']}
    byversion={(v['path'],v['case']):v for v in versions};timings=[];results=[];rgb_differences=[];rng=[]
    shape=lambda v:[(r.get('original_source_offset'),r['word']) for r in v['selected_B22_command_pairs']]
    for path in PATHS:
        left,right=[byversion[path,c] for c in ['clean_Japanese','reviewed_English']];assert shape(left)==shape(right) and left['input_schedule_sha256']==right['input_schedule_sha256']
        assert photosets[path,'clean_Japanese'].keys()==photosets[path,'reviewed_English'].keys()
        for a,b in zip(left['selected_B22_command_pairs'],right['selected_B22_command_pairs'],strict=True):
            if (a['start'],a['returned'])!=(b['start'],b['returned']):timings.append(dict(path=path,source_offset=a.get('original_source_offset'),word=a['word'],Japanese=[a['start'],a['returned']],English=[b['start'],b['returned']]))
            if a['result_words']!=b['result_words']:results.append(dict(path=path,source_offset=a.get('original_source_offset'),word=a['word'],Japanese=a['result_words'],English=b['result_words']))
            if (a['before_seed'],a['after_seed'])!=(b['before_seed'],b['after_seed']):rng.append(dict(path=path,source_offset=a.get('original_source_offset'),word=a['word'],Japanese=[a['before_seed'],a['after_seed']],English=[b['before_seed'],b['after_seed']]))
        for frame,(photo,pic) in photosets[path,'reviewed_English'].items():
            if frame<=max(left['fixture_exit_frame'],right['fixture_exit_frame']):continue
            other=photosets[path,'clean_Japanese'][frame][1]
            if pic.tobytes()!=other.tobytes():rgb_differences.append(dict(path=path,frame=frame,whole_RGB_bbox=ImageChops.difference(pic,other).getbbox(),not_masked_or_retimed=True))
    byid={r['id']:r for r in font['cases']};observations=[];unique={};failures=[];nontext=[]
    for path in PATHS:
        source_intervals={r['id']:r for r in byversion[path,'clean_Japanese']['selected_intervals']}
        for interval in byversion[path,'reviewed_English']['selected_intervals']:
            c=byid[interval['id']];preview=Image.open(c['preview']).convert('RGB');assert sha(Path(c['preview']).read_bytes())==c['preview_sha256']
            assert preview.size==((228 if interval['prefix']==254 else 216),64)
            masks=[{(x,y) for y in range(64) for x in range(preview.width) if preview.getpixel((x,y))==color} for color in [(0,8,0),(98,97,98)]]
            source_interval=source_intervals[interval['id']];holds=[]
            for frame,(photo,pic) in photosets[path,'reviewed_English'].items():
                if not interval['start']<frame<interval['returned']:continue
                actual=[{(x,y) for y in range(64) for x in range(preview.width) if pic.getpixel((16+x,296+y))==color} for color in [(0,8,0),(98,97,98)]]
                if actual!=masks:continue
                shared=source_interval['start']<frame<source_interval['returned'];regions=None
                sourcephoto,sourcepic=photosets[path,'clean_Japanese'][frame]
                if shared:
                    regions={name:pic.crop(box).tobytes()==sourcepic.crop(box).tobytes() for name,box in [('upper',(0,0,256,192)),('portrait_name_picture',(0,192,256,294))]}
                    if not all(regions.values()):nontext.append(dict(path=path,id=interval['id'],frame=frame,region_equality=regions,whole_nontext_bbox=ImageChops.difference(pic.crop((0,192,256,294)),sourcepic.crop((0,192,256,294))).getbbox()))
                holds.append(dict(frame=frame,capture=photo['path'],capture_sha256=photo['PNG_sha256'],clean_capture=sourcephoto['path'],clean_capture_sha256=sourcephoto['PNG_sha256'],complete_ink_gray_masks_equal_native_plane=True,shared_source_speech_hold=shared,paired_region_equality=regions))
                evidence[photo['path']]=photo['PNG_sha256'];evidence[sourcephoto['path']]=sourcephoto['PNG_sha256']
            if not holds:failures.append(dict(path=path,id=interval['id'],finding='No complete native target plane in captured English hold.'))
            record=dict(id=interval['id'],path=path,prefix=interval['prefix'],native_plane_sha256=c['whole_native_plane_sha256'],interval=interval,holds=holds,actually_displayed_in_disclosed_B22_fixture=True);observations.append(record)
            if holds and interval['id'] not in unique:unique[interval['id']]=record
    arm=NdsImage.open(en['parent']).read_file('/__arm9__.bin');assert sha(arm)==CURRENT_ARM9
    target=menu['current_and_reviewed_VM_and_font_cases'][1];vm=target['native_VM_getters_geometry_and_selection'];width=target['source_derived_text_canvas_width']
    rect=vm['native_menu_rectangle'];assert width==48 and rect==[88,64,168,128]
    x,y=rect[0]+16,192+rect[1]+12
    env={**painter_base.__dict__,'LABEL_WIDTH':width,'sha':sha,'CURRENT_ARM9':CURRENT_ARM9};exec(compile(menu['source_derived_painter_adapter'],__file__+'::native-menu-painter','exec'),env)
    masks=[]
    for label in vm['labels']:
        pixels,proof=env['paint'](arm,label.encode('ascii'),1);masks.append({(xx,yy) for yy in range(20) for xx in range(width) if pixels[yy*width+xx]})
    actualmenus=[]
    for path in PATHS:
        interval=byversion[path,'reviewed_English']['actual_choice_pairs'][0];option=interval['result_words'][1];holds=[]
        for frame,(photo,pic) in photosets[path,'reviewed_English'].items():
            if not interval['start']+30<frame<interval['returned']:continue
            actual=[{(xx,yy) for yy in range(20) for xx in range(width) if pic.getpixel((x+xx,y+20*i+yy))==(8,8,8)} for i in range(2)]
            if actual!=masks:continue
            colors=[pic.getpixel((x,y+20*i)) for i in range(2)]
            settled=all(color in ([(0,165,172),(205,198,180)] if i==option else [(205,198,180)]) for i,color in enumerate(colors))
            if not settled:continue
            visible=colors[option]==(0,165,172)
            holds.append(dict(frame=frame,path=photo['path'],sha256=photo['PNG_sha256'],complete_both_native_label_masks_equal=True,selected_highlight_matches_return_when_visible=visible,background_colors=colors));evidence[photo['path']]=photo['PNG_sha256']
        if not holds or not any(h['selected_highlight_matches_return_when_visible'] for h in holds):failures.append(dict(path=path,menu=880,finding='No complete two-label masks with visibly correct returned option.'))
        actualmenus.append(dict(path=path,source_menu_offset=880,native_result_words=interval['result_words'],text_canvas_origins=[[x,y+20*i] for i in range(2)],holds=holds))
    assert len(unique)==24 and len(observations)==37
    ROOT.mkdir(parents=True);panels=[(ident,Image.open(r['holds'][-1]['capture']).convert('RGB')) for ident,r in unique.items()];sheets=[]
    for start in range(0,len(panels),6):
        sheet=Image.new('RGB',(1560,832),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(label,pic) in enumerate(panels[start:start+6]):
            xx,yy=i%3*520,i//3*416;draw.text((xx+4,yy+3),label,fill='white');sheet.paste(pic.crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST),(xx+4,yy+24))
        p=ROOT/f'actual_English_speech_sheet{start//6+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    transitions=[]
    for path in PATHS:
        exitframe=byversion[path,'reviewed_English']['fixture_exit_frame'];frames=[6070,6130,6190,next(frame for frame in photosets[path,'reviewed_English'] if frame>exitframe+60),10030,12970]
        sheet=Image.new('RGB',(1536,820),'#263238');draw=ImageDraw.Draw(sheet)
        for i,frame in enumerate(frames):
            xx,yy=i%3*512,i//3*410
            for j,case in enumerate(['clean_Japanese','reviewed_English']):
                photo,pic=photosets[path,case][frame];draw.text((xx+256*j+3,yy+3),case+' '+str(frame),fill='white');sheet.paste(pic,(xx+256*j,yy+24))
        p=ROOT/f'{path}_paired_menus_return_and_later_frames.png';sheet.save(p);transitions.append(dict(path=str(p),sha256=sha(p.read_bytes()),frames=frames))
    save(ROOT/'two_paths_all24_complete_panels_two_options_and_source_comparisons.json',dict(versions=versions,actual_panels=list(unique.values()),all_actual_speech_observations=observations,actual_menu_cases=actualmenus,
        actual_unique_speech_panels=len(unique),actual_English_speech_observations=len(observations),complete_native_holds=sum(len(r['holds']) for r in observations),offline_only_display_IDs=sorted(set(byid)-set(unique)),
        new_successful_English_cold_boot_runs=2,new_successful_English_frames=26002,reused_prior_Japanese_runs=2,reused_prior_Japanese_frames=26002,total_successful_paired_frames=52004,
        failures=failures,paired_nontext_region_differences=nontext,command_timing_differences=timings,command_result_differences=results,command_RNG_differences=rng,later_whole_RGB_differences=rgb_differences,
        review_sheets=sheets,transition_sheets=transitions,visual_review_pending=True,all44_original_commands_and9_initializers_stored_and_observed_over_each_two_path_union=True,
        original_funds_RNG_roster_conditions_and_results_unforced=True,ordinary_gamepad_only=True,source_event201_relocated_to_B22_not_natural_eligibility_or_original_location=True,
        capture_not_complete_item_Charm_inventory_full_RAM_future_world_hardware_or_full_route_audit=True,evidence=evidence,producer_sha256=sha(Path(__file__).read_bytes()),new_editorial_credit=0,full_goal_complete=False))
    print(dict(unique_panels=len(unique),speech_observations=len(observations),menus=len(actualmenus),failures=failures,nontext_differences=len(nontext),timing_differences=len(timings),result_differences=len(results),RNG_differences=len(rng),later_RGB_differences=len(rgb_differences),exit_frames=[(v['path'],v['case'],v['fixture_exit_frame']) for v in versions]))
    if failures:raise SystemExit(1)
