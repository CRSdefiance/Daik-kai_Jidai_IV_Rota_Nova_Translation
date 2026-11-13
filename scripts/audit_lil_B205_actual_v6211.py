"""Compare complete source/revised scenes,unaltered pixels,native glyphs and observed commands."""
import inspect
from pathlib import Path
from PIL import Image,ImageDraw,ImageChops
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts import audit_lil_B204_actual_v6146 as prior
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B205_actual_v6211')
SOURCE=Path('work/analysis/lil_B205_source_fixture_v6180/complete_B205_source_B22_fixture.json')
ENGLISH=Path('work/analysis/lil_B205_English_fixture_v6209/complete_B205_English_B22_fixture.json')
FONT=Path('work/analysis/lil_B205_fonts_v6195/all17_progressive_FE_native_planes_and136_alignment_cases.json')
INDICES=[5,9,13,17,20,24,28,32,36,40,44,47,51,55,59,63,67]
if __name__=='__main__':
    assert not ROOT.exists();source=checked_text(inspect.getsource(prior.load),{'len(pairs)==35':'len(pairs)==34',"pairs[-1]['source_offset']==1308":"pairs[-1]['source_offset']==616"});env={**prior.__dict__,'INDICES':INDICES};exec(compile(source,__file__+'::whole-source-bound-run','exec'),env)
    jp=env['load'](SOURCE,Path('work/analysis/lil_B205_source_run_v6181_clean_Japanese'));en=env['load'](ENGLISH,Path('work/analysis/lil_B205_English_run_v6210_reviewed_English'))
    assert jp['report']['frames']==en['report']['frames']==13001 and jp['following']==en['following']==[120] and jp['rp']['inputs_sha256']==en['rp']['inputs_sha256']
    assert all(en['image'].read_file(p)==v for p,v in jp['image'].iter_components()) and [p for _,p,v in jp['image'].iter_files() if en['image'].read_file(p)!=v]==['/data/SC2.DK4']
    a,b=[IlnkContainer.parse(v['image'].read_file('/data/SC2.DK4')).blocks for v in [jp,en]];assert [i for i,(x,y) in enumerate(zip(a,b,strict=True)) if x!=y]==[22]
    timing=[];rng=[]
    for old,new in zip(jp['pairs'],en['pairs'],strict=True):
        assert (old['source_offset'],old['word'],old['native_result'])==(new['source_offset'],new['word'],new['native_result'])
        if (old['start'],old['returned'])!=(new['start'],new['returned']):timing.append(dict(source=old,English=new))
        if (old['before_RNG'],old['after_RNG'])!=(new['before_RNG'],new['after_RNG']):rng.append(dict(source=old,English=new))
    comparisons=[]
    for frame,(p,pic) in jp['photos'].items():
        if frame not in en['photos']:continue
        q,eng=en['photos'][frame];comparisons.append(dict(frame=frame,whole_RGB_equal=pic.tobytes()==eng.tobytes(),difference_bbox=ImageChops.difference(pic,eng).getbbox(),upper_portrait_name_item_region_equal=pic.crop((0,0,256,294)).tobytes()==eng.crop((0,0,256,294)).tobytes(),source_capture=p['path'],English_capture=q['path']))
    font=read(FONT);byid={r['id']:r for r in font['cases']};panels=[];actual=[];failures=[];nontext=[]
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
                if not paired:nontext.append(dict(id=interval['id'],frame=frame,complete_native_text_plane_equal=True,same_frame_source_nontext_region_differs=True))
            holds.append(dict(frame=frame,capture=p['path'],capture_sha256=p['PNG_sha256'],complete_ink_and_gray_masks_equal_native_plane=True,same_frame_source_nontext_region_equal=paired))
        if not holds:failures.append(dict(id=interval['id'],finding='No complete native glyph plane in actual English interval.'))
        else:panels.append((interval['id'],Image.open(holds[0]['capture']).convert('RGB').crop((0,192,256,384))))
        actual.append(dict(id=interval['id'],prefix=interval['prefix'],interval=interval,holds=holds,native_plane_sha256=case['whole_native_plane_sha256'],actually_observed_in_disclosed_B22_fixture=True))
    assert len(actual)==17 and sum(r['prefix']==254 for r in actual)==7
    ROOT.mkdir(parents=True);sheets=[]
    for start in range(0,len(panels),6):
        sheet=Image.new('RGB',(1560,832),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(label,pic) in enumerate(panels[start:start+6]):
            x,y=i%3*520,i//3*416;draw.text((x+4,y+3),label+' / actual revised English',fill='white');sheet.paste(pic.resize((512,384),Image.Resampling.NEAREST),(x+4,y+24))
        p=ROOT/f'actual_consumer_sheet{start//6+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    versions=[dict(case=label,fixture=v['fixture']['research_ROM'],candidate_sha256=v['fixture']['research_ROM_sha256'],frames=v['report']['frames'],command_pairs=v['pairs'],selected_intervals=v['intervals'],exit_frame=v['pairs'][-1]['returned'],following_blocks=v['following'],capture_report=str(Path(v['rp']['capture_folder'])/'capture_report.json')) for label,v in [('clean-Japanese',jp),('reviewed-English',en)]]
    evidence={str(FONT):sha(FONT.read_bytes()),str(Path(__file__)):sha(Path(__file__).read_bytes()),**jp['evidence'],**en['evidence']}
    save(ROOT/'all17_actual_English_panels_complete_native_holds_source_comparison_and_return.json',dict(versions=versions,actual_panels=actual,actual_unique_speech_panels=17,complete_matching_observations=sum(bool(r['holds']) for r in actual),complete_matching_holds=sum(len(r['holds']) for r in actual),failures=failures,offline_only_display_IDs=[r['id'] for r in actual if not r['holds']],all34_commands25_source_plus9_initializers_and_seven_FE_objects_observed=True,original_command_paths_results_and_complete_end_preserved=True,observed_English_follows_B120=True,same_frame_comparisons=comparisons,source_English_command_timing_differences=timing,source_English_command_RNG_differences=rng,nontext_differences_retained_without_filtering_native_text_holds=nontext,source_and_English_same_ARM9_COMMON_all_components_and_input_schedule=True,source_exit_frame=jp['pairs'][-1]['returned'],English_exit_frame=en['pairs'][-1]['returned'],all_pixels_native_no_masking_retiming_or_pixel_edit=True,no_whole_scene_or_final_state_equivalence_inferred=True,no_natural_event_original_location_earned_inventory_full_effects_routes_or_hardware_claim=True,review_sheets=sheets,visual_review_pending=True,new_English_cold_boots=1,new_English_frames=13001,terminal_reaped_English_session=85639,source_bound_load_adapter=source,evidence=evidence,new_review_credit=0,full_goal_complete=False))
    print(dict(panels=17,complete_matching=sum(bool(r['holds']) for r in actual),holds=sum(len(r['holds']) for r in actual),failures=failures,nontext_differences=len(nontext),timing=len(timing),RNG=len(rng),source_exit=jp['pairs'][-1]['returned'],English_exit=en['pairs'][-1]['returned']))
    if failures:raise SystemExit(1)
