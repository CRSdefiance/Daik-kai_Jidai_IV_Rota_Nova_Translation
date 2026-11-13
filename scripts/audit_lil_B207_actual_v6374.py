"""Pair terminal B207 source/English runs with complete native masks and unmasked comparisons."""
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B207_actual_v6374')
SOURCE=Path('work/analysis/lil_B207_source_fixture_v6345/complete_B207_source_B22_fixture.json')
ENGLISH=Path('work/analysis/lil_B207_English_fixture_v6372/complete_B207_English_B22_fixture.json')
FONT=Path('work/analysis/lil_B207_fonts_v6361/all13_progressive_complete_native_planes104_alignment_cases.json')
NAMEFONT=Path('work/analysis/lil_B207_name_planes_v6354d/two_complete_native_names32_literal_macro_alignments_and_actual_headers.json')
def load(language,manifest,run):
    fixture=read(manifest)['fixtures'][0];terminal,plan=read(run/'terminal.json'),read(run/'run_plan.json');assert terminal['terminal'] and terminal['observer_instances']==1 and terminal['observer_host_slots_restored'];cap=Path(plan['capture_folder']);rp,tp=cap/'capture_report.json',cap/'observer/commands.json';report,trace=read(rp),read(tp)
    assert report['frames']==11001 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and not report.get('battery_save_preloaded') and not any(v for k,v in report.items() if k.startswith('synthetic_'))
    assert report['ROM_sha256']==fixture['research_ROM_sha256']==plan['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes()) and not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact']
    assert plan['explicit_B22_entry_ROM_fixture'] and plan['source_event207_not_naturally_selected'] and plan['all15_source_commands_retained'] and sha(Path(plan['fixture_manifest']).read_bytes())==plan['fixture_manifest_sha256']==sha(manifest.read_bytes())
    schedule=read(plan['original_inputs']);assert report['scripted_input_schedule']==schedule and sha(Path(plan['original_inputs']).read_bytes())==plan['inputs_sha256'];image=NdsImage.open(fixture['research_ROM']);bank=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;block=bank[22];assert block.hex()==fixture['fixture_block_hex'];photos={}
    for r in report['frames_captured']:
        p=Path(r['path']);assert sha(p.read_bytes())==r['PNG_sha256'];pic=Image.open(p).convert('RGB');assert pic.size==(256,384);photos[r['frame']]=(r,pic)
    snap=report['read_only_RAM_snapshot'];assert snap['read_only_export'] and snap['bytes']==4194304 and sha(Path(snap['path']).read_bytes())==snap['sha256']
    records={r['fixture_command_offset']:r for r in fixture['original_text_records']};commands={r['fixture_offset']:r for r in fixture['selected_original_objects']};pairs=[];speeches=[];following=[];seen=set()
    for r in trace['rows']:
        assert r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'];s=r['source'];assert s['classification']=='original_SC_cache' and s['route']==2 and s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==sha(bank[s['block']])
        if r['kind']!='after_command':continue
        if s['block']!=22:following.append(dict(frame=r['frame'],block=s['block'],offset=s['instruction_offset'],word=s['first_word'],native_result=r['result_words']));continue
        entry=trace['rows'][r['entry_row']];at=entry['source']['instruction_offset'];word=int.from_bytes(block[at:at+2],'little');c=commands.get(at);seen.add(at)
        if c:assert word==c['source_word'] and r['decoded_length']==c['native_extent']
        pair=dict(fixture_offset=at,source_offset=None if c is None else c['source_offset'],word=word,start=entry['frame'],returned=r['frame'],decoded_length=r['decoded_length'],native_result=r['result_words'],before_RNG=entry['original_RNG_seed'],after_RNG=r['original_RNG_seed'],UI_after=r['native_UI_request_words']);pairs.append(pair)
        if at in records:speeches.append(dict(id=records[at]['id'],source_record_index=records[at]['source_record_index'],prefix=records[at]['source_selector'],interval=pair))
    assert len(pairs)==24 and seen=={r['offset'] for r in fixture['all24_stored_fixture_commands']} and len(speeches)==13 and pairs[-1]['source_offset']==650 and pairs[-1]['word']==0 and pairs[-1]['native_result'][0]==0
    assert [p['source_offset'] for p in pairs if p['word']==0xA000 and p['source_offset'] is not None]==[642]
    files=[manifest,run/'terminal.json',run/'run_plan.json',rp,tp,Path(plan['original_inputs'])];return dict(language=language,fixture=fixture,plan=plan,report=report,trace=trace,image=image,photos=photos,command_pairs=pairs,speech_intervals=speeches,following_commands=following,exit_frame=pairs[-1]['returned'],final_snapshot=snap,capture_report=str(rp),observer_report=str(tp),evidence={str(p):sha(p.read_bytes()) for p in files})
if __name__=='__main__':
    assert not ROOT.exists();jp=load('source',SOURCE,Path('work/analysis/lil_B207_source_run_v6346'));en=load('English',ENGLISH,Path('work/analysis/lil_B207_English_run_v6373'));assert jp['plan']['inputs_sha256']==en['plan']['inputs_sha256'] and jp['photos'].keys()==en['photos'].keys()
    assert all(en['image'].read_file(p)==value for _,p,value in jp['image'].iter_files() if p!='/data/SC2.DK4') and all(en['image'].read_file(p)==value for p,value in jp['image'].iter_components());old,new=[IlnkContainer.parse(v['image'].read_file('/data/SC2.DK4')).blocks for v in [jp,en]];assert [i for i,(a,b) in enumerate(zip(old,new,strict=True)) if a!=b]==[22]
    timing=[];rng=[];results=[];UI=[]
    for a,b in zip(jp['command_pairs'],en['command_pairs'],strict=True):
        assert (a['source_offset'],a['word'])==(b['source_offset'],b['word']);identity=dict(source_offset=a['source_offset'],word=a['word'])
        for field,bucket in [('native_result',results),('UI_after',UI)]:
            if a[field]!=b[field]:bucket.append(dict(**identity,Japanese=a[field],English=b[field]))
        if [a['start'],a['returned']]!=[b['start'],b['returned']]:timing.append(dict(**identity,Japanese=[a['start'],a['returned']],English=[b['start'],b['returned']]))
        if [a['before_RNG'],a['after_RNG']]!=[b['before_RNG'],b['after_RNG']]:rng.append(dict(**identity,Japanese=[a['before_RNG'],a['after_RNG']],English=[b['before_RNG'],b['after_RNG']]))
    font=read(FONT);fonts={r['id']:r for r in font['cases']};names={r['actor_ID']:r for r in read(NAMEFONT)['planes']};source_speeches={r['id']:r for r in jp['speech_intervals']};actual=[];failures=[];nontext=[];evidence={**jp['evidence'],**en['evidence'],str(FONT):sha(FONT.read_bytes()),str(NAMEFONT):sha(NAMEFONT.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes())}
    for speech in en['speech_intervals']:
        case=fonts[speech['id']];preview=Image.open(case['preview']).convert('RGB');assert sha(Path(case['preview']).read_bytes())==case['preview_sha256'];masks=[{(i%216,i//216) for i,c in enumerate(preview.getdata()) if c==color} for color in [(0,8,0),(98,97,98)]];name=names[speech['prefix']];np=Image.open(name['preview']).convert('RGB');assert sha(Path(name['preview']).read_bytes())==name['preview_sha256'];nameink={(i%216,i//216) for i,c in enumerate(np.getdata()) if c==(65,53,42)};width=name['native_width_including_flush_space'];holds=[];source=source_speeches[speech['id']]['interval']
        for frame,(photo,pic) in en['photos'].items():
            if not speech['interval']['start']<frame<speech['interval']['returned']:continue
            crop=pic.crop((16,296,232,360));found=[{(i%216,i//216) for i,c in enumerate(crop.getdata()) if c==color} for color in [(0,8,0),(98,97,98)]]
            if found!=masks:continue
            actualname={(x-4,y) for y in range(13) for x in range(width+8) if pic.getpixel((12+x,276+y))==(98,97,98)}
            if actualname!=nameink:continue
            shared=source['start']<frame<source['returned'];sourcephoto,sourcepic=jp['photos'][frame];equal=pic.crop((0,0,256,294)).tobytes()==sourcepic.crop((0,0,256,294)).tobytes()
            h=dict(frame=frame,capture=photo['path'],capture_sha256=photo['PNG_sha256'],all216x64_ink_gray_pixels_equal_complete_native_plane=True,complete_current_style11_nameplate_glyphs_and_blank_guards_equal=True,source_capture=sourcephoto['path'],source_capture_sha256=sourcephoto['PNG_sha256'],both_versions_in_same_semantic_speech_at_this_frame=shared,paired_upper_portrait_name_region_equal=equal);holds.append(h)
            if shared and not equal:nontext.append(dict(id=speech['id'],frame=frame,region=[0,0,256,294],difference_bbox=ImageChops.difference(pic.crop((0,0,256,294)),sourcepic.crop((0,0,256,294))).getbbox()))
        if not holds:failures.append(dict(id=speech['id'],finding='No complete English body/name hold matches the approved native planes.'))
        actual.append(dict(id=speech['id'],source_record_index=speech['source_record_index'],prefix=speech['prefix'],name=name['label'],interval=speech['interval'],holds=holds,native_plane_sha256=case['whole_native_plane_sha256'],actual_complete_dialogue_and_nameplate_observed=bool(holds)))
    comparisons=[]
    for frame,(p,pic) in en['photos'].items():
        sp,sim=jp['photos'][frame];bounds=ImageChops.difference(pic,sim).getbbox();comparisons.append(dict(frame=frame,whole_RGB_equal=bounds is None,whole_RGB_difference_bbox=bounds,after_both_scene_exits=frame>max(jp['exit_frame'],en['exit_frame']),source_capture=sp['path'],source_capture_sha256=sp['PNG_sha256'],English_capture=p['path'],English_capture_sha256=p['PNG_sha256'],no_pixel_masking_or_retiming=True))
    post=[r for r in comparisons if r['after_both_scene_exits']];later=[r for r in post if not r['whole_RGB_equal']];versions=[]
    for v in [jp,en]:
        raw=Path(v['final_snapshot']['path']).read_bytes();versions.append(dict(language=v['language'],research_ROM=v['fixture']['research_ROM'],research_ROM_sha256=v['fixture']['research_ROM_sha256'],frames=11001,command_pairs=v['command_pairs'],speech_intervals=v['speech_intervals'],exit_frame=v['exit_frame'],following_commands=v['following_commands'],final_snapshot=v['final_snapshot'],queried_final_native_market_fields=state(v['image'].read_file('/__arm9__.bin'),raw),capture_report=v['capture_report'],observer_report=v['observer_report'],input_schedule_sha256=v['plan']['inputs_sha256']))
    ROOT.mkdir(parents=True);sheets=[]
    for start in range(0,len(actual),6):
        sheet=Image.new('RGB',(1560,832),'#263238');draw=ImageDraw.Draw(sheet)
        for i,r in enumerate(actual[start:start+6]):
            if not r['holds']:continue
            h=r['holds'][-1];x,y=i%3*520,i//3*416;draw.text((x+4,y+3),r['id']+' frame'+str(h['frame']),fill='white');sheet.paste(Image.open(h['capture']).convert('RGB').crop((0,192,256,384)).resize((512,384),Image.Resampling.NEAREST),(x+4,y+24));evidence[h['capture']]=h['capture_sha256']
        p=ROOT/f'all13_actual_English_dialogue_sheet{start//6+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    sheet=Image.new('RGB',(1536,410),'#263238');draw=ImageDraw.Draw(sheet)
    for i,frame in enumerate([3010,6070,11001]):
        for j,v in enumerate([jp,en]):
            p,pic=v['photos'][frame];x=i*512+j*256;draw.text((x+3,3),v['language']+' frame'+str(frame),fill='white');sheet.paste(pic,(x,24));evidence[p['path']]=p['PNG_sha256']
    p=ROOT/'unmasked_source_English_scene_port_and_following_B120.png';sheet.save(p);transitions=[dict(path=str(p),sha256=sha(p.read_bytes()),frames=[3010,6070,11001])]
    save(ROOT/'all13_English_panels_complete_native_holds24_commands_and_source_comparison.json',dict(versions=versions,actual_panels=actual,actual_unique_speech_panels=len({r['id'] for r in actual if r['holds']}),actual_English_speech_observations=len(actual),complete_native_text_and_nameplate_holds=sum(len(r['holds']) for r in actual),failures=failures,offline_only_display_IDs=[r['id'] for r in actual if not r['holds']],source_and_English_all24_commands15_source_plus9_initializers_observed=True,all_command_paths_and_results_preserved=not results,command_result_differences=results,command_UI_word_differences=UI,command_timing_differences=timing,command_RNG_differences=rng,paired_nontext_region_differences=nontext,same_frame_whole_RGB_comparisons=comparisons,postscene_whole_RGB_comparisons=post,later_whole_RGB_differences=later,source_and_English_same_ARM9_COMMON_components_all_other_files_all335_other_blocks_and_input_schedules=True,source_original_A000_execution_not_full_quest_inventory_eligibility_or_effect_semantics_proof=True,no_natural_event207_original_location_earned_progress_full_routes_or_hardware_claim=True,no_timing_RNG_whole_state_future_sequence_or_broad_simulation_equivalence_claim=True,no_capture_masking_pixel_edit_or_retiming=True,review_sheets=sheets,transition_sheets=transitions,visual_review_pending=True,new_English_cold_boots=1,new_English_frames=11001,reused_source_frames=11001,total_paired_frames=22002,all_jobs_terminal_and_reaped=True,evidence=evidence,new_review_credit=0,full_goal_complete=False))
    print(dict(English_panels=len(actual),native_holds=sum(len(r['holds']) for r in actual),failures=failures,results_differences=len(results),UI_differences=len(UI),timing_differences=len(timing),RNG_differences=len(rng),nontext_differences=len(nontext),postscene_RGB_differences=len(later),source_exit=jp['exit_frame'],English_exit=en['exit_frame']))
