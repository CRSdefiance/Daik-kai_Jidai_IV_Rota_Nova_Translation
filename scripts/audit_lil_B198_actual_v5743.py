"""Compare the observed original B198 path and every held English native text plane."""
from collections import Counter
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/lil_B198_actual_v5743')
FIXTURES=[Path('work/analysis/lil_B198_source_fixture_v5712/complete_B198_source_B22_fixture.json'),
    Path('work/analysis/lil_B198_English_fixture_v5738/complete_B198_English_B22_fixture.json')]
RUNS=[Path('work/analysis/lil_B198_source_run_v5713_clean_Japanese'),Path('work/analysis/lil_B198_English_run_v5739_reviewed_English')]
FONT=Path('work/analysis/lil_B198_fonts_v5741/all17_progressive_FE_native_planes_and136_alignment_cases.json')
if __name__=='__main__':
    assert not ROOT.exists()
    versions=[];photosets={};evidence={str(p):sha(p.read_bytes()) for p in FIXTURES+[FONT,Path(__file__)]}
    for manifest,run in zip(FIXTURES,RUNS,strict=True):
        fixture=read(manifest)['fixtures'][0];case=fixture['case']
        terminal,rp=read(run/'terminal.json'),read(run/'run_plan.json');cap=Path(rp['capture_folder'])
        report,trace=read(cap/'capture_report.json'),read(cap/'observer/commands.json')
        assert terminal['terminal'] and terminal['observer_host_slots_restored'] and terminal['observer_instances']==1
        assert report['frames']==13001 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['ROM_sha256']==rp['research_ROM_sha256']==fixture['research_ROM_sha256']==sha(Path(fixture['research_ROM']).read_bytes())
        assert rp['explicit_B22_entry_ROM_fixture'] and rp['all37_source_commands_retained']
        assert sha(Path(rp['original_inputs']).read_bytes())==rp['inputs_sha256']
        assert not trace['errors'] and trace['mismatches']==0 and trace['all_host_slots_restored_and_core_file_exact']
        assert all(not v for k,v in report.items() if k.startswith('synthetic_'))
        blocks=IlnkContainer.parse(NdsImage.open(fixture['research_ROM']).read_file('/data/SC2.DK4')).blocks
        assert sha(blocks[22])==fixture['fixture_block_sha256']
        photos={}
        for photo in report['frames_captured']:
            path=Path(photo['path']);assert sha(path.read_bytes())==photo['PNG_sha256']
            picture=Image.open(path).convert('RGB');assert picture.size==(256,384);photos[photo['frame']]=(photo,picture)
        by_at={r['fixture_command_offset']:r for r in fixture['original_text_records']}
        commands={r['fixture_offset']:r for r in fixture['selected_original_objects']}
        pairs=[];intervals=[];following=set()
        for row in trace['rows']:
            assert row['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']
            s=row['source']
            assert s['whole_resident_payload_exact_ROM'] and s['actual_sha256']==sha(blocks[s['block']])
            if s['block']!=22:following.add(s['block'])
            if row['kind']!='after_command' or s['block']!=22:continue
            entry=trace['rows'][row['entry_row']];at=entry['source']['instruction_offset'];c=commands.get(at)
            pair=dict(fixture_offset=at,source_offset=None if c is None else c['source_offset'],word=s['first_word'],
                start=entry['frame'],returned=row['frame'],native_result=row['result_words'],decoded_length=row['decoded_length'],
                before_RNG=entry['original_RNG_seed'],after_RNG=row['original_RNG_seed'],UI_after=row['native_UI_request_words'])
            pairs.append(pair)
            if at in by_at:
                r=by_at[at]
                assert blocks[22][at:at+r['native_extent']].hex()==r['whole_command_hex']
                intervals.append(dict(id=r['id'],source_record_index=r['source_record_index'],prefix=r['source_selector'],
                    start=entry['frame'],returned=row['frame'],fixture_offset=at))
        indices=[r['source_record_index'] for r in intervals]
        assert indices==[10,14,18,22,26,30,34,38,42,49,53,72,76,80,84]
        assert pairs[-1]['source_offset']==540 and pairs[-1]['word']==0 and pairs[-1]['native_result']==[0,0]
        predicates=[r for r in pairs if r['word']==0x8000]
        assert [(r['source_offset'],r['native_result']) for r in predicates]==[(306,[2,0]),(480,[2,0])]
        versions.append(dict(case=case,command_pairs=pairs,selected_intervals=intervals,selected_source_indices=indices,
            fixture_exit_frame=pairs[-1]['returned'],input_schedule_sha256=rp['inputs_sha256'],capture_report=str(cap/'capture_report.json'),
            observer_report=str(cap/'observer/commands.json'),following_observed_blocks=sorted(following)))
        photosets[case]=photos
        for p in [manifest,run/'terminal.json',run/'run_plan.json',Path(rp['original_inputs']),cap/'capture_report.json',cap/'observer/commands.json']:
            evidence[str(p)]=sha(p.read_bytes())
    def shape(v):return [(r['source_offset'],r['word'],r['native_result']) for r in v['command_pairs']]
    assert shape(versions[0])==shape(versions[1]) and versions[0]['input_schedule_sha256']==versions[1]['input_schedule_sha256']
    assert photosets['clean_Japanese'].keys()==photosets['reviewed_English'].keys()
    font=read(FONT);byid={r['id']:r for r in font['cases']};source_intervals={r['id']:r for r in versions[0]['selected_intervals']}
    actual=[];panels=[];failures=[];region_differences=[]
    for interval in versions[1]['selected_intervals']:
        case=byid[interval['id']];preview=Image.open(case['preview']).convert('RGB')
        assert sha(Path(case['preview']).read_bytes())==case['preview_sha256']
        width=228 if interval['prefix']==254 else 216;assert preview.size==(width,64)
        ink0={(x,y) for y in range(64) for x in range(width) if preview.getpixel((x,y))==(0,8,0)}
        gray0={(x,y) for y in range(64) for x in range(width) if preview.getpixel((x,y))==(98,97,98)}
        source_interval=source_intervals[interval['id']];holds=[]
        for frame,(photo,picture) in photosets['reviewed_English'].items():
            if not max(interval['start'],source_interval['start'])<frame<min(interval['returned'],source_interval['returned']):continue
            ink={(x,y) for y in range(64) for x in range(width) if picture.getpixel((16+x,296+y))==(0,8,0)}
            gray={(x,y) for y in range(64) for x in range(width) if picture.getpixel((16+x,296+y))==(98,97,98)}
            if ink!=ink0 or gray!=gray0:continue
            source_photo,source_picture=photosets['clean_Japanese'][frame]
            region_equal=(picture.crop((0,192,256,294)).tobytes()==source_picture.crop((0,192,256,294)).tobytes()
                and picture.crop((0,0,256,192)).tobytes()==source_picture.crop((0,0,256,192)).tobytes())
            if not region_equal:
                region_differences.append(dict(id=interval['id'],frame=frame,native_plane_exact=True,paired_nontext_region_differs=True,not_retimed_or_masked=True));continue
            holds.append(dict(frame=frame,capture=photo['path'],capture_sha256=photo['PNG_sha256'],
                clean_capture=source_photo['path'],clean_capture_sha256=source_photo['PNG_sha256'],
                complete_ink_gray_masks_equal_native_plane=True,upper_portrait_name_and_item_regions_equal_source=True))
            evidence[photo['path']]=photo['PNG_sha256'];evidence[source_photo['path']]=source_photo['PNG_sha256']
        if not holds:failures.append(dict(id=interval['id'],finding='No complete native plane with paired source regions in shared interval.'))
        else:panels.append((interval['id'],Image.open(holds[0]['capture']).convert('RGB').crop((0,192,256,384))))
        actual.append(dict(id=interval['id'],prefix=interval['prefix'],interval=interval,holds=holds,
            native_plane_sha256=case['whole_native_plane_sha256'],actually_displayed_in_disclosed_B22_fixture=True))
    assert len(actual)==15 and sum(r['prefix']==254 for r in actual)==6
    comparisons=[]
    for frame,(jp,source) in photosets['clean_Japanese'].items():
        en,target=photosets['reviewed_English'][frame]
        comparisons.append(dict(frame=frame,whole_RGB_equal=source.tobytes()==target.tobytes(),
            difference_bbox=ImageChops.difference(source,target).getbbox(),
            nontext_region_difference_bbox=ImageChops.difference(source.crop((0,0,256,294)),target.crop((0,0,256,294))).getbbox()))
    timings=[dict(source=a,English=b) for a,b in zip(versions[0]['command_pairs'],versions[1]['command_pairs'],strict=True)
        if (a['start'],a['returned'])!=(b['start'],b['returned'])]
    ROOT.mkdir(parents=True);sheets=[]
    for start in range(0,len(panels),6):
        sheet=Image.new('RGB',(1560,832),'#263238');draw=ImageDraw.Draw(sheet)
        for i,(label,picture) in enumerate(panels[start:start+6]):
            x,y=i%3*520,i//3*416;draw.text((x+4,y+3),label+' / actual B198 content',fill='white')
            sheet.paste(picture.resize((512,384),Image.Resampling.NEAREST),(x+4,y+24))
        p=ROOT/f'actual_consumer_sheet{start//6+1}.png';sheet.save(p);sheets.append(dict(path=str(p),sha256=sha(p.read_bytes())))
    after=[r for r in comparisons if r['frame']>max(v['fixture_exit_frame'] for v in versions)]
    save(ROOT/'fifteen_actual_panels_source_matched_controls_and_complete_native_holds.json',dict(
        versions=versions,actual_panels=actual,actual_unique_speech_panels=15,complete_matching_observations=sum(bool(r['holds']) for r in actual),
        complete_matching_holds=sum(len(r['holds']) for r in actual),offline_only_source_indices=[65,95],
        failures=failures,paired_region_differences=region_differences,review_sheets=sheets,visual_review_pending=True,
        all_sampled_frame_comparisons=comparisons,actual_timing_differences=timings,
        later_whole_RGB_differences=[r for r in after if not r['whole_RGB_equal']],
        actual_source_and_English_cold_boots=2,new_English_cold_boots=1,frames_each=13001,total_successful_source_English_frames=26002,
        all37_source_commands_and9_initializers_stored=True,selected_command_counts={format(w,'04X'):n for w,n in Counter(r['word'] for r in versions[1]['command_pairs']).items()},
        same_observed_source_path_original_results_predicates_and_end540=True,
        source_item_and_portrait_name_visibility_not_normalized_or_masked=True,
        no_natural_event198_activation_original_location_roster_fixture_effect_semantics_full_route_or_hardware_claim=True,
        no_broad_postscene_simulation_equivalence_or_causal_claim=True,
        evidence=evidence,new_editorial_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(panels=15,matching=sum(bool(r['holds']) for r in actual),holds=sum(len(r['holds']) for r in actual),failures=failures,
        nontext_differences=len(region_differences),timing_differences=len(timings),later_RGB_differences=sum(not r['whole_RGB_equal'] for r in after)))
    if failures:raise SystemExit(1)
