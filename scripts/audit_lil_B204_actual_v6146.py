"""Audit complete English display and paths against two explicitly scoped source runs."""
from collections import Counter
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B204_actual_v6146')
FULL_SOURCE=Path('work/analysis/lil_B204_source_fixture_v6070/complete_B204_source_B22_fixture.json')
CURRENT_SOURCE=Path('work/analysis/shachihoko_item_menu_fixture_v6103/complete_B204_source_B22_fixture_with_coordinated_item_data.json')
ENGLISH=Path('work/analysis/lil_B204_English_fixture_v6144/complete_B204_English_B22_fixture.json')
FONT=Path('work/analysis/lil_B204_fonts_v6131/all20_progressive_FE_native_planes_and160_alignment_cases.json')
INDICES=[5,9,13,16,19,22,25,29,33,36,40,45,48,52,55,58,62,66,69,72]
def load(manifest,run):
    fixture=read(manifest)['fixtures'][0];rp=read(run/'run_plan.json');terminal=read(run/'terminal.json');cap=Path(rp['capture_folder']);report=read(cap/'capture_report.json');trace=read(cap/'observer/commands.json')
    assert terminal['terminal'] and terminal['observer_host_slots_restored'] and terminal['observer_instances']==1
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and not report.get('battery_save_preloaded')
    assert all(not v for k,v in report.items() if k.startswith('synthetic_'))
    assert report['ROM_sha256']==rp['research_ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes())
    assert not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact']
    assert sha(Path(rp['original_inputs']).read_bytes())==rp['inputs_sha256']
    image=NdsImage.open(fixture['research_ROM']);blocks=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks;assert sha(blocks[22])==fixture['fixture_block_sha256']
    photos={}
    for p in report['frames_captured']:
        assert sha(Path(p['path']).read_bytes())==p['PNG_sha256'];im=Image.open(p['path']).convert('RGB');assert im.size==(256,384);photos[p['frame']]=(p,im)
    commands={r['fixture_offset']:r for r in fixture['selected_original_objects']};text={r['fixture_command_offset']:r for r in fixture['original_text_records']};pairs=[];intervals=[];following=set()
    for row in trace['rows']:
        assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback'];s=row['source'];assert s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==sha(blocks[s['block']])
        if s['block']!=22:following.add(s['block'])
        if row['kind']!='after_command' or s['block']!=22:continue
        entry=trace['rows'][row['entry_row']];at=entry['source']['instruction_offset'];c=commands.get(at)
        pairs.append(dict(fixture_offset=at,source_offset=None if c is None else c['source_offset'],word=s['first_word'],start=entry['frame'],returned=row['frame'],native_result=row['result_words'],decoded_length=row['decoded_length'],before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed'],UI_after=row['native_UI_request_words']))
        if at in text:
            r=text[at];assert blocks[22][at:at+r['native_extent']].hex()==r['whole_command_hex'];intervals.append(dict(id=r['id'],source_record_index=r['source_record_index'],prefix=r['source_selector'],start=entry['frame'],returned=row['frame'],fixture_offset=at))
    assert len(pairs)==35 and pairs[-1]['source_offset']==1308 and pairs[-1]['word']==0 and pairs[-1]['native_result']==[0,0]
    assert [r['source_record_index'] for r in intervals]==INDICES and not any(r['word']==0x8000 for r in pairs)
    evidence={str(p):sha(p.read_bytes()) for p in [manifest,run/'terminal.json',run/'run_plan.json',Path(rp['original_inputs']),cap/'capture_report.json',cap/'observer/commands.json']}
    return dict(fixture=fixture,rp=rp,report=report,image=image,photos=photos,pairs=pairs,intervals=intervals,evidence=evidence,following=sorted(following))
if __name__=='__main__':
    assert not ROOT.exists();jp=load(FULL_SOURCE,Path('work/analysis/lil_B204_source_run_v6071_clean_Japanese'));current=load(CURRENT_SOURCE,Path('work/analysis/shachihoko_item_menu_run_v6104'));en=load(ENGLISH,Path('work/analysis/lil_B204_English_run_v6145_reviewed_English'))
    assert jp['report']['frames']==en['report']['frames']==13001 and current['report']['frames']==8420 and jp['following']==en['following']==[120]
    assert jp['rp']['inputs_sha256']==en['rp']['inputs_sha256']
    inputs=read(en['rp']['original_inputs']);assert [v for v in inputs if v['start']<8000]==read(current['rp']['original_inputs'])
    assert current['image'].read_file('/__arm9__.bin')==en['image'].read_file('/__arm9__.bin') and current['image'].read_file('/COMMON/MESFILE.DK4')==en['image'].read_file('/COMMON/MESFILE.DK4')
    assert all(en['image'].read_file(p)==v for p,v in current['image'].iter_components())
    assert [p for _,p,v in jp['image'].iter_files() if current['image'].read_file(p)!=v]==['/COMMON/MESFILE.DK4']
    assert [p for p,v in jp['image'].iter_components() if current['image'].read_file(p)!=v]==['/__arm9__.bin']
    assert [p for _,p,v in current['image'].iter_files() if en['image'].read_file(p)!=v]==['/data/SC2.DK4']
    a,b=[IlnkContainer.parse(v['image'].read_file('/data/SC2.DK4')).blocks for v in [current,en]];assert [i for i,(x,y) in enumerate(zip(a,b,strict=True)) if x!=y]==[22]
    comparisons={};timing={};rng={}
    for label,v in [('earlier-full-Japanese-V6050',jp),('current-Japanese-V6110-prefix-before-menu',current)]:
        assert len(v['pairs'])==len(en['pairs'])==35
        timing[label]=[];rng[label]=[]
        for old,new in zip(v['pairs'],en['pairs'],strict=True):
            assert (old['source_offset'],old['word'],old['native_result'])==(new['source_offset'],new['word'],new['native_result'])
            if (old['start'],old['returned'])!=(new['start'],new['returned']):timing[label].append(dict(source=old,English=new))
            if (old['before_RNG'],old['after_RNG'])!=(new['before_RNG'],new['after_RNG']):rng[label].append(dict(source=old,English=new))
        rows=[]
        for frame,(p,pic) in v['photos'].items():
            if frame not in en['photos'] or (v is current and frame>=8000):continue
            q,eng=en['photos'][frame];rows.append(dict(frame=frame,whole_RGB_equal=pic.tobytes()==eng.tobytes(),difference_bbox=ImageChops.difference(pic,eng).getbbox(),upper_portrait_name_item_region_equal=pic.crop((0,0,256,294)).tobytes()==eng.crop((0,0,256,294)).tobytes(),source_capture=p['path'],English_capture=q['path']))
        comparisons[label]=rows
    font=read(FONT);byid={r['id']:r for r in font['cases']};panels=[];actual=[];failures=[];all_nontext=[]
    for interval in en['intervals']:
        case=byid[interval['id']];assert sha(Path(case['preview']).read_bytes())==case['preview_sha256'];preview=Image.open(case['preview']).convert('RGB');w=228 if interval['prefix']==254 else 216;assert preview.size==(w,64)
        ink0={(x,y) for y in range(64) for x in range(w) if preview.getpixel((x,y))==(0,8,0)};gray0={(x,y) for y in range(64) for x in range(w) if preview.getpixel((x,y))==(98,97,98)};holds=[]
        for frame,(p,pic) in en['photos'].items():
            if not interval['start']<frame<interval['returned']:continue
            ink={(x,y) for y in range(64) for x in range(w) if pic.getpixel((16+x,296+y))==(0,8,0)};gray={(x,y) for y in range(64) for x in range(w) if pic.getpixel((16+x,296+y))==(98,97,98)}
            if ink!=ink0 or gray!=gray0:continue
            paired=None
            if frame in jp['photos']:
                paired=pic.crop((0,0,256,294)).tobytes()==jp['photos'][frame][1].crop((0,0,256,294)).tobytes()
                if not paired:all_nontext.append(dict(id=interval['id'],frame=frame,complete_native_text_plane_equal=True,older_source_nontext_region_differs=True,source_ARM9_COMMON_and_item_title_differ_explicitly=True))
            holds.append(dict(frame=frame,capture=p['path'],capture_sha256=p['PNG_sha256'],complete_ink_and_gray_masks_equal_native_plane=True,same_frame_earlier_source_nontext_region_equal=paired))
        if not holds:failures.append(dict(id=interval['id'],finding='No complete current-native glyph plane in observed English interval.'))
        else:panels.append((interval['id'],Image.open(holds[0]['capture']).convert('RGB').crop((0,192,256,384))))
        actual.append(dict(id=interval['id'],prefix=interval['prefix'],interval=interval,holds=holds,native_plane_sha256=case['whole_native_plane_sha256'],actually_observed_in_disclosed_B22_fixture=True))
    assert len(actual)==20 and sum(r['prefix']==254 for r in actual)==4
    ROOT.mkdir(parents=True);sheets=[]
    for start in range(0,len(panels),6):
        sheet=Image.new('RGB',(1560,832),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(label,pic) in enumerate(panels[start:start+6]):
            x,y=i%3*520,i//3*416;draw.text((x+4,y+3),label+' / actual reviewed English',fill='white');sheet.paste(pic.resize((512,384),Image.Resampling.NEAREST),(x+4,y+24))
        p=ROOT/f'actual_consumer_sheet{start//6+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    versions=[dict(case=label,fixture=v['fixture']['research_ROM'],candidate_sha256=v['fixture']['research_ROM_sha256'],frames=v['report']['frames'],command_pairs=v['pairs'],selected_intervals=v['intervals'],exit_frame=v['pairs'][-1]['returned'],following_blocks=v['following'],capture_report=str(Path(v['rp']['capture_folder'])/'capture_report.json')) for label,v in [('earlier-full-Japanese',jp),('current-Japanese-menu-prefix',current),('reviewed-English',en)]]
    evidence={str(FONT):sha(FONT.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes()),**jp['evidence'],**current['evidence'],**en['evidence']}
    save(ROOT/'all20_actual_English_panels_complete_native_holds_two_source_scopes_and_return.json',dict(versions=versions,actual_panels=actual,actual_unique_speech_panels=20,complete_matching_observations=sum(bool(r['holds']) for r in actual),complete_matching_holds=sum(len(r['holds']) for r in actual),failures=failures,offline_only_display_IDs=[r['id'] for r in actual if not r['holds']],all35_commands26_source_plus9_initializers_and_four_FE_parts_observed=True,original_command_paths_results_and_complete_end_preserved=True,observed_English_follows_B120=True,same_frame_comparisons=comparisons,source_English_command_timing_differences=timing,source_English_command_RNG_differences=rng,older_source_nontext_differences_retained_without_filtering_native_text_holds=all_nontext,source_current_item_name_Orca_to_Shachihoko_and_ARM9_COMMON_differences_not_hidden=True,current_Japanese_same_ARM9_COMMON_prefix_reused_before_manual_menu_inputs_at8000=True,older_full_Japanese_same_input_schedule_B120_return_retained_as_distinct_baseline=True,source_exit_frames=[7894,7895],English_exit_frame=en['pairs'][-1]['returned'],all_pixels_native_no_masking_retiming_or_pixel_edit=True,no_whole_scene_or_final_state_equivalence_inferred=True,no_natural_event_original_location_earned_inventory_full_effects_routes_or_hardware_claim=True,review_sheets=sheets,visual_review_pending=True,new_English_cold_boots=1,new_English_frames=13001,terminal_reaped_English_session=51172,evidence=evidence,new_review_credit=0,full_goal_complete=False))
    print(dict(panels=20,complete_matching=sum(bool(r['holds']) for r in actual),holds=sum(len(r['holds']) for r in actual),failures=failures,earlier_source_nontext_differences=len(all_nontext),timing={k:len(v) for k,v in timing.items()},English_exit=en['pairs'][-1]['returned']))
    if failures:raise SystemExit(1)
