"""Compare every sampled B176 scene and postscene state; prepare honest visual review sheets."""
import json
import struct
from pathlib import Path
from PIL import Image,ImageChops,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_shipyard_gameplay_v760 import models
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_followup_gameplay_v778 import tasks
from scripts.verify_ceremony_prayer_gameplay_v814 import calendar
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B176_actual_review_v4589')
ACTUAL=Path('work/analysis/lil_B176_actual_v4588/actual_all10_progressive_FE_A000_C200_and_single_end.json')
FIXTURE=Path('work/analysis/lil_B176_display_fixture_v4585/complete_B176_B22_fixtures.json')
BASE=Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def native_json(value):
    assert isinstance(value,bytes)
    return {'native_byte_span_hex':value.hex()}


if __name__=='__main__':
    assert not ROOT.exists()
    actual,fixture=read(ACTUAL),read(FIXTURE)
    assert actual['complete_matching_observations']==10 and not actual['failures'] and not actual['paired_region_differences']
    assert len(actual['review_sheets'])==2
    reports=[];photos=[];snapshots=[];arms=[];paths=[ACTUAL,FIXTURE,Path(__file__)]
    for f in fixture['fixtures']:
        folder=BASE/('lil_B176_display_v4587_'+f['case'])
        reportpath=folder/'capture_report.json';report=read(reportpath)
        assert report['frames']==9001 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['ROM_sha256']==f['research_ROM_sha256']==sha(Path(f['research_ROM']).read_bytes())
        snapshot=report['read_only_RAM_snapshot'];raw=Path(snapshot['path']).read_bytes()
        assert snapshot['read_only_export'] and len(raw)==4194304 and sha(raw)==snapshot['sha256']
        reports.append(report);photos.append({p['frame']:p for p in report['frames_captured']});snapshots.append((snapshot,raw))
        arms.append(NdsImage.open(f['research_ROM']).read_file('/__arm9__.bin'))
        paths.extend([reportpath,Path(snapshot['path']),folder/'observer/commands.json'])
    assert arms[0]==arms[1] and photos[0].keys()==photos[1].keys()
    comparisons=[]
    for frame,source in sorted(photos[0].items()):
        english=photos[1][frame]
        for p in [source,english]:
            assert sha(Path(p['path']).read_bytes())==p['PNG_sha256']
        a,b=[Image.open(p['path']).convert('RGB') for p in [source,english]]
        bbox=ImageChops.difference(a.crop((0,0,256,294)),b.crop((0,0,256,294))).getbbox()
        comparisons.append(dict(frame=frame,source=source,English=english,
            upper_portrait_name_regions_equal=bbox is None,nontext_difference_bbox=bbox,
            whole_RGB_equal=a.tobytes()==b.tobytes()))
    assert len(comparisons)==115 and all(r['upper_portrait_name_regions_equal'] for r in comparisons)
    assert all(r['whole_RGB_equal'] for r in comparisons if r['frame']>=5290)
    native=[]
    for (snapshot,raw),arm in zip(snapshots,arms,strict=True):
        components={fn.__name__:fn(arm,raw) for fn in [state,models,persistent_objects,tasks,calendar]}
        cpu,get=get_machine(arm,raw);root,captain=get(0xCB184),get(0x7F244)
        assert captain==2 and 0x02000000<=root<=0x02400000-0x1A04
        native.append(dict(snapshot=snapshot,components=components,actor=bytes(cpu.mem_read(root,0x1A04)),
            actor_root=root,captain_ID=captain,seed=struct.unpack_from('<I',raw,0x168EB8)[0]))
    equality={k:native[0]['components'][k]==native[1]['components'][k] for k in native[0]['components']}
    assert all(equality.values()) and native[0]['actor']==native[1]['actor']
    timings=[dict(source=a,English=b) for a,b in zip(actual['versions'][0]['selected_B22_command_pairs'],
        actual['versions'][1]['selected_B22_command_pairs'],strict=True) if (a['start'],a['returned'])!=(b['start'],b['returned'])]
    assert not timings
    for v in actual['versions']:
        assert len(v['selected_B22_command_pairs'])==22 and len(v['selected_intervals'])==10
        assert v['single_source_end386_actually_reached'] and v['fixture_exit_frame']==5256
        assert len(v['source_A000'])==1 and v['source_A000'][0]['original_source_offset']==8
        assert v['source_A000'][0]['result_words']==v['source_C200']['result_words']==[3,0]
        assert v['selected_B22_command_pairs'][-1]['result_words']==[0,0]
        assert v['following_observed_blocks']==[120]
        assert v['following_unreturned_commands_at_capture_end']==[dict(entry_row=68,player=35173504,block=120,offset=606,start=8373,original_payload_exact_ROM=True)]
    ROOT.mkdir(parents=True)
    screens=[]
    for index,frames in enumerate([[2950,5050],[5290,9001]],1):
        sheet=Image.new('RGB',(1048,1600),'#263238');draw=ImageDraw.Draw(sheet)
        for row,frame in enumerate(frames):
            for col,(label,photo) in enumerate(zip(['clean_Japanese','reviewed_English'],photos,strict=True)):
                p=photo[frame];image=Image.open(p['path']).convert('RGB')
                x,y=col*524,row*800
                draw.text((x+4,y+4),label+' / frame '+str(frame),fill='white')
                sheet.paste(image.resize((512,768),Image.Resampling.NEAREST),(x+4,y+24))
                paths.append(Path(p['path']))
        path=ROOT/f'paired_screen_review{index}.png';sheet.save(path)
        screens.append(dict(path=str(path),sha256=sha(path.read_bytes()),frames=frames,visual_review_pending=True))
    save(ROOT/'paired_all115_samples22_commands10_planes_and_final_state_analysis.json',dict(
        actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),
        fixture_manifest=str(FIXTURE),fixture_manifest_sha256=sha(FIXTURE.read_bytes()),
        actual_consumer_sheets=actual['review_sheets'],paired_full_screen_sheets=screens,
        all115_sampled_nontext_region_checks=comparisons,nontext_equal_samples=115,nontext_difference_samples=[],
        all10_complete_held_planes_and_source_paired_regions_match=True,
        all10_speeches9_progressive1_impersonal_FE_actually_observed=True,
        source_A0008_C200384_single_end386_actually_executed=True,actual22_of22_stored_fixture_commands_selected=True,
        fixture_return_frames=[v['fixture_exit_frame'] for v in actual['versions']],
        all_sampled_whole_RGB_from5290_through9001_equal=True,whole_RGB_final9001_equal=True,
        actual_timing_differences=timings,
        postscene9001_native_component_equality=equality,
        postscene9001_component_hashes=[{k:sha(json.dumps(v,sort_keys=True,default=native_json).encode('utf-8')) for k,v in r['components'].items()} for r in native],
        postscene9001_whole1A04_actor_models_and_captain2_equal=True,
        postscene9001_actor_samples=[dict(snapshot=r['snapshot'],actor_root=r['actor_root'],actor_bytes=len(r['actor']),actor_sha256=sha(r['actor']),captain_ID=2) for r in native],
        postscene9001_PRNG_seeds=[r['seed'] for r in native],PRNG_equality=native[0]['seed']==native[1]['seed'],
        future_world_equivalence_and_full_RAM_equality_not_claimed=True,native_getters_run_on_exported_copies_only=True,
        following_B120_offset606_in_progress_at_end_adds_no_editorial_credit=True,
        source_event176_natural_eligibility_earned_state_earlier_location_full_route_or_hardware_not_proved=True,
        reaped_tool_sessions=[dict(case='clean_Japanese',session_id=18439,exit_code=0),dict(case='reviewed_English',session_id=27916,exit_code=0)],
        all_content_jobs_terminal=True,new_emulator_runs=2,visual_review_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in paths},producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(complete_panels=10,nontext_equal=115,nontext_differences=0,return_frames=[v['fixture_exit_frame'] for v in actual['versions']],
        native_components_equal=equality,PRNG_seeds=[r['seed'] for r in native],timing_differences=0,visual_review_pending=True))
