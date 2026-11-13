"""Audit three paired bargaining paths without claiming visits to all conditionals."""
from collections import Counter
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import verify_ship_advice_choice_centering_20261022 as painter_base
from scripts.lil_current_font_oracles_v4792 import CURRENT_ARM9
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B196_actual_v5628')
PLAN=Path('work/analysis/lil_B196_display_fixture_v5625/complete_B196_B22_fixtures.json')
FONT=Path('work/analysis/lil_B196_fonts_v5609b/all24_progressive_FE_native_planes_and192_alignment_cases.json')
MENU=Path('work/analysis/lil_B196_choices_v5610b/B196_C218/original_choice_decoder_VM_geometry_and_native_pixels.json')
CAPBASE=Path('E:/Rota Nova translations/Generated/work/emulation_v193')
PATHS=['first_buy','all_pass','deepest_buy']

if __name__=='__main__':
    assert not ROOT.exists();plan,font,menu=map(read,[PLAN,FONT,MENU]);versions=[];photosets={};evidence={str(p):sha(p.read_bytes()) for p in [PLAN,FONT,MENU,Path(__file__)]}
    for path in PATHS:
        for fixture in plan['fixtures']:
            case=fixture['case'];fid=path+'_'+case
            run=Path('work/analysis/lil_B196_display_run_v5627_'+fid);cap=CAPBASE/('lil_B196_display_v5627_'+fid)
            files=[run/'terminal.json',run/'run_plan.json',cap/'capture_report.json',cap/'observer/commands.json',run/'ordinary_menu_inputs.json']
            terminal,rp,report,trace,inputs=map(read,files)
            assert terminal['terminal'] and terminal['observer_host_slots_restored'] and terminal['observer_instances']==1
            assert report['frames']==13001 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
            assert sha(Path(fixture['research_ROM']).read_bytes())==fixture['research_ROM_sha256']==report['ROM_sha256']==rp['research_ROM_sha256']
            assert rp['explicit_B22_entry_ROM_fixture'] and rp['source_event196_not_selected'] and rp['requested_bargaining_path']==path and rp['all_source119_commands_retained']
            assert sha(Path(rp['fixture_manifest']).read_bytes())==rp['fixture_manifest_sha256']==sha(PLAN.read_bytes())
            assert not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact']
            assert all(not v for k,v in report.items() if k.startswith('synthetic_'))
            assert inputs['ordinary_gamepad_only'] and inputs['no_game_RAM_or_predicate_or_seed_write']
            assert sha(Path(rp['original_inputs']).read_bytes())==rp['inputs_sha256']
            blocks=IlnkContainer.parse(NdsImage.open(fixture['research_ROM']).read_file('/data/SC2.DK4')).blocks
            block=blocks[22];assert sha(block)==fixture['fixture_block_sha256'];photos={}
            for photo in report['frames_captured']:
                p=Path(photo['path']);assert sha(p.read_bytes())==photo['PNG_sha256'];pic=Image.open(p).convert('RGB');assert pic.size==(256,384);photos[photo['frame']]=(photo,pic)
            snap=report['read_only_RAM_snapshot'];assert snap['read_only_export'] and snap['bytes']==4194304 and sha(Path(snap['path']).read_bytes())==snap['sha256']
            rows=trace['rows'];pairs=[];intervals=[];byat={r['fixture_command_offset']:r for r in fixture['original_text_records']};commands={r['fixture_offset']:r for r in fixture['selected_original_objects']}
            for r in rows:
                assert r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'];s=r['source']
                assert s['classification']=='original_SC_cache' and s['route']==2 and s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==sha(blocks[s['block']]) and s['block']!=196
                if r['kind']!='after_command':continue
                entry=rows[r['entry_row']];s=entry['source'];at=s['instruction_offset'];word=int.from_bytes(blocks[s['block']][at:at+2],'little')
                pair=dict(block=s['block'],offset=at,word=word,start=entry['frame'],returned=r['frame'],extent=r['decoded_length'],result_words=r['result_words'],before_seed=entry['original_RNG_seed'],after_seed=r['original_RNG_seed'],UI_request_after=r['native_UI_request_words'],UI_pending_after=r['native_UI_pending_flag']);pairs.append(pair)
                if s['block']!=22:continue
                if at in commands:
                    assert word==commands[at]['source_word'];pair.update(original_source_block=196,original_source_offset=commands[at]['source_offset'])
                if word==0x4000:
                    rec=byat[at];assert block[at:at+rec['native_extent']].hex()==rec['whole_command_hex']
                    intervals.append(dict(id=rec['id'],start=entry['frame'],returned=r['frame'],offset=at,prefix=rec['source_selector']))
            selected=[r for r in pairs if r['block']==22];choices=[r for r in selected if r['word']==0x2100]
            expected_choices=[218] if path=='first_buy' else [218,582,832,1156,1370,1588]
            assert [r['original_source_offset'] for r in choices]==expected_choices
            expected_options=[0] if path=='first_buy' else [1]*6 if path=='all_pass' else [1]*5+[0]
            assert [r['result_words'] for r in choices]==[[2,n] for n in expected_options]
            assert selected[-1]['word']==0 and selected[-1]['original_source_offset']==(364 if path=='first_buy' else 1810 if path=='all_pass' else 1708)
            assert selected[-1]['result_words']==[0,expected_options[-1]]
            assert len({r['id'] for r in intervals})==len(intervals)
            assert not trace['unreturned_at_capture_end']
            versions.append(dict(path=path,case=case,research_ROM=fixture['research_ROM'],research_ROM_sha256=fixture['research_ROM_sha256'],capture_report=str(files[2]),observer_report=str(files[3]),selected_B22_command_pairs=selected,selected_intervals=intervals,actual_choice_pairs=choices,fixture_exit_frame=selected[-1]['returned'],final_readonly_RAM_snapshot=snap,whole_final_frame=photos[12970][0]))
            photosets[path,case]=photos;evidence.update({str(p):sha(p.read_bytes()) for p in files})
    byversion={(v['path'],v['case']):v for v in versions};timings=[];rgb_differences=[]
    shape=lambda v:[(r.get('original_source_offset'),r['word'],r['result_words']) for r in v['selected_B22_command_pairs']]
    for path in PATHS:
        jp,en=[byversion[path,c] for c in ['clean_Japanese','reviewed_English']];assert shape(jp)==shape(en)
        for a,b in zip(jp['selected_B22_command_pairs'],en['selected_B22_command_pairs'],strict=True):
            if (a['start'],a['returned'])!=(b['start'],b['returned']):timings.append(dict(path=path,source_offset=a.get('original_source_offset'),word=a['word'],Japanese=[a['start'],a['returned']],English=[b['start'],b['returned']]))
        for frame,(photo,pic) in photosets[path,'reviewed_English'].items():
            if frame<=max(jp['fixture_exit_frame'],en['fixture_exit_frame']):continue
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
                if not max(interval['start'],source_interval['start'])<frame<min(interval['returned'],source_interval['returned']):continue
                actual=[{(x,y) for y in range(64) for x in range(preview.width) if pic.getpixel((16+x,296+y))==color} for color in [(0,8,0),(98,97,98)]]
                if actual!=masks:continue
                sourcephoto,sourcepic=photosets[path,'clean_Japanese'][frame]
                equal=all(pic.crop(box).tobytes()==sourcepic.crop(box).tobytes() for box in [(0,192,256,294),(0,0,256,192)])
                if not equal:nontext.append(dict(path=path,id=interval['id'],frame=frame));continue
                holds.append(dict(frame=frame,capture=photo['path'],capture_sha256=photo['PNG_sha256'],clean_capture=sourcephoto['path'],clean_capture_sha256=sourcephoto['PNG_sha256'],complete_ink_gray_masks_equal_native_plane=True,portrait_name_picture_and_upper_regions_equal_Japanese=True))
                evidence[photo['path']]=photo['PNG_sha256'];evidence[sourcephoto['path']]=sourcephoto['PNG_sha256']
            if not holds:failures.append(dict(path=path,id=interval['id'],finding='No complete native plane with paired nontext regions inside shared hold.'))
            record=dict(id=interval['id'],path=path,prefix=interval['prefix'],native_plane_sha256=c['whole_native_plane_sha256'],interval=interval,holds=holds,actually_displayed_in_disclosed_B22_fixture=True);observations.append(record)
            if holds and interval['id'] not in unique:unique[interval['id']]=record
    arm=NdsImage.open(plan['parent']).read_file('/__arm9__.bin');assert sha(arm)==CURRENT_ARM9
    env={**painter_base.__dict__,'LABEL_WIDTH':48,'sha':sha,'CURRENT_ARM9':CURRENT_ARM9};exec(compile(menu['source_derived_painter_adapter'],__file__+'::native-menu-painter','exec'),env)
    masks=[]
    for text in [b'Buy',b'Pass']:
        pixels,proof=env['paint'](arm,text,1);masks.append({(x,y) for y in range(20) for x in range(48) if pixels[y*48+x]})
    actualmenus=[]
    for path in PATHS:
        for interval in byversion[path,'reviewed_English']['actual_choice_pairs']:
            option=interval['result_words'][1];holds=[]
            for frame,(photo,pic) in photosets[path,'reviewed_English'].items():
                if not interval['start']+35<frame<interval['returned']:continue
                actual=[{(x,y) for y in range(20) for x in range(48) if pic.getpixel((104+x,268+20*i+y))==(8,8,8)} for i in range(2)]
                if actual!=masks:continue
                visible=pic.getpixel((104,268+20*option))==(0,165,172)
                holds.append(dict(frame=frame,path=photo['path'],sha256=photo['PNG_sha256'],complete_Buy_Pass_native_foreground_masks_equal=True,selected_highlight_matches_return_when_visible=visible))
                evidence[photo['path']]=photo['PNG_sha256']
            if not holds or not any(h['selected_highlight_matches_return_when_visible'] for h in holds):failures.append(dict(path=path,menu=interval['original_source_offset'],finding='No complete native labels and visibly correct selected option.'))
            actualmenus.append(dict(path=path,source_menu_offset=interval['original_source_offset'],native_result_words=interval['result_words'],text_canvas_origins=[[104,268],[104,288]],holds=holds))
    ROOT.mkdir(parents=True);panels=[(ident,Image.open(r['holds'][0]['capture']).convert('RGB')) for ident,r in unique.items()]
    panels +=[(f"{r['path']} C{r['source_menu_offset']} option{r['native_result_words'][1]}",Image.open(next(h for h in r['holds'] if h['selected_highlight_matches_return_when_visible'])['path']).convert('RGB')) for r in actualmenus if any(h['selected_highlight_matches_return_when_visible'] for h in r['holds'])]
    sheets=[]
    for start in range(0,len(panels),6):
        sheet=Image.new('RGB',(1040,1248),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(label,pic) in enumerate(panels[start:start+6]):
            x,y=i%2*520,i//2*416;draw.text((x+4,y+3),label,fill='white');sheet.paste(pic.crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST),(x+4,y+24))
        p=ROOT/f'actual_consumer_menu_sheet{start//6+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    offline=sorted(set(byid)-set(unique))
    save(ROOT/'three_paired_paths_native_panels_menus_and_separate_endings.json',dict(versions=versions,actual_panels=list(unique.values()),all_actual_speech_observations=observations,actual_menu_cases=actualmenus,
        fresh_actual_unique_speech_panels=len(unique),actual_English_speech_observations=len(observations),complete_native_holds=sum(len(r['holds']) for r in observations),offline_only_display_IDs=offline,
        actual_new_cold_boot_runs=6,frames_per_boot=13001,actual_frames=78006,failures=failures,paired_nontext_region_differences=nontext,command_timing_differences=timings,later_whole_RGB_differences=rgb_differences,
        review_sheets=sheets,visual_review_pending=True,all_six_original_menu_indices0_Buy1_Pass_observed=True,
        original_first_buy_end364_deepest_buy_end1708_all_pass_end1810_reached=True,
        all119_source_commands_stored_but_only_observed_paths_claimed=True,source_event196_not_naturally_selected=True,
        original_predicates_RNG_and_funds_unforced_and_only_ordinary_gamepad_inputs_added=True,
        item_picture_and_acquisition_notice_observed_not_an_offline_inference=True,
        Charm_model_and_item_inventory_and_full_state_equivalence_not_claimed_by_text_capture=True,
        no_natural_eligibility_earned_purchase_full_route_hardware_or_unvisited_conditional_claim=True,
        evidence=evidence,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(unique_panels=len(unique),speech_observations=len(observations),menus=len(actualmenus),offline_only=offline,failures=failures,timing_differences=len(timings),later_RGB_differences=len(rgb_differences),sheets=len(sheets)))
    if failures:raise SystemExit(1)
