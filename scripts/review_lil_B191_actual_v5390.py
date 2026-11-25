"""Measure every B191 sample/timing/state comparison before deciding its actual scope."""
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

ROOT=Path('work/analysis/lil_B191_actual_review_v5390')
ACTUAL=Path('work/analysis/lil_B191_actual_v5389/actual_all13_progressive_FE_RNG_effect_or_no_effect_C200_and_single_end.json')
FIXTURE=Path('work/analysis/lil_B191_display_fixture_v5386/complete_B191_B22_fixtures.json')
BASE=Path('E:/Rota Nova translations/Generated/work/emulation_v193')


def native_json(value):
    assert isinstance(value,bytes)
    return {'native_byte_span_hex':value.hex()}


if __name__=='__main__':
    assert not ROOT.exists()
    actual,fixture=read(ACTUAL),read(FIXTURE)
    assert actual['complete_matching_observations']==13 and not actual['failures'] and not actual['paired_region_differences']
    assert len(actual['review_sheets'])==3
    reports=[];photos=[];snapshots=[];arms=[];paths=[ACTUAL,FIXTURE,Path(__file__)]
    for f in fixture['fixtures']:
        folder=BASE/('lil_B191_display_v5388_'+f['case']);rp=folder/'capture_report.json';report=read(rp)
        assert report['frames']==9001 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['ROM_sha256']==f['research_ROM_sha256']==sha(Path(f['research_ROM']).read_bytes())
        snap=report['read_only_RAM_snapshot'];raw=Path(snap['path']).read_bytes()
        assert snap['read_only_export'] and len(raw)==4194304 and sha(raw)==snap['sha256']
        reports.append(report);photos.append({p['frame']:p for p in report['frames_captured']});snapshots.append((snap,raw))
        arms.append(NdsImage.open(f['research_ROM']).read_file('/__arm9__.bin'))
        paths.extend([rp,Path(snap['path']),folder/'observer/commands.json'])
    assert arms[0]==arms[1] and photos[0].keys()==photos[1].keys()
    assert reports[0]['scripted_input_schedule']==reports[1]['scripted_input_schedule']
    comparisons=[]
    for frame,source in sorted(photos[0].items()):
        english=photos[1][frame]
        for p in [source,english]:assert sha(Path(p['path']).read_bytes())==p['PNG_sha256']
        a,b=[Image.open(p['path']).convert('RGB') for p in [source,english]]
        bbox=ImageChops.difference(a.crop((0,0,256,294)),b.crop((0,0,256,294))).getbbox()
        comparisons.append(dict(frame=frame,source=source,English=english,upper_portrait_name_regions_equal=bbox is None,
            nontext_difference_bbox=bbox,whole_frame_difference_bbox=ImageChops.difference(a,b).getbbox(),whole_RGB_equal=a.tobytes()==b.tobytes()))
    assert len(comparisons)==115
    exit_frames=[v['fixture_exit_frame'] for v in actual['versions']]
    after=[r for r in comparisons if r['frame']>max(exit_frames)]
    differences=[r for r in after if not r['whole_RGB_equal']]
    native=[]
    for (snap,raw),arm in zip(snapshots,arms,strict=True):
        components={fn.__name__:fn(arm,raw) for fn in [state,models,persistent_objects,tasks,calendar]}
        cpu,get=get_machine(arm,raw);root,captain=get(0xCB184),get(0x7F244)
        assert captain==2 and 0x02000000<=root<=0x02400000-0x1A04
        native.append(dict(snapshot=snap,components=components,actor=bytes(cpu.mem_read(root,0x1A04)),actor_root=root,
            captain_ID=captain,seed=struct.unpack_from('<I',raw,0x168EB8)[0]))
    equality={k:native[0]['components'][k]==native[1]['components'][k] for k in native[0]['components']}
    shared=lambda v:{r['original_source_offset']:r for r in v['selected_B22_command_pairs'] if 'original_source_offset' in r}
    before,after_commands=map(shared,actual['versions'])
    timings=[dict(source=before[at],English=after_commands[at]) for at in sorted(before.keys()&after_commands.keys())
        if (before[at]['start'],before[at]['returned'])!=(after_commands[at]['start'],after_commands[at]['returned'])]
    conditional_only=dict(clean=sorted(before.keys()-after_commands.keys()),English=sorted(after_commands.keys()-before.keys()))
    for v in actual['versions']:
        assert len(v['selected_intervals'])==13 and v['single_source_end730_actually_reached']
        assert len(v['source_A000']) in [0,1] and len(v['source_C200'])==1
        assert v['selected_B22_command_pairs'][-1]['result_words']==[0,v['actual_predicate_transitions'][-1]['result']]
    holds={r['id']:r['holds'] for r in actual['actual_panels']}
    focus=[holds[key][0]['frame'] for key in ['DK4_MES_B191_R0056','DK4_MES_B191_R0064','DK4_MES_B191_R0088','DK4_MES_B191_R0100']]
    selections=[focus[:2],focus[2:],[after[0]['frame'],9001]]
    selections.extend([[r['frame'] for r in differences[start:start+2]] for start in range(0,len(differences),2)])
    ROOT.mkdir(parents=True);screens=[]
    for index,frames in enumerate(selections,1):
        sheet=Image.new('RGB',(1048,800*len(frames)),'#263238');draw=ImageDraw.Draw(sheet)
        for row,frame in enumerate(frames):
            for col,(label,photo) in enumerate(zip(['clean_Japanese','reviewed_English'],photos,strict=True)):
                p=photo[frame];picture=Image.open(p['path']).convert('RGB');x,y=col*524,row*800
                draw.text((x+4,y+4),label+' / frame '+str(frame),fill='white')
                sheet.paste(picture.resize((512,768),Image.Resampling.NEAREST),(x+4,y+24));paths.append(Path(p['path']))
        p=ROOT/f'paired_screen_review{index}.png';sheet.save(p)
        screens.append(dict(path=str(p),sha256=sha(p.read_bytes()),frames=frames,visual_review_pending=True))
    result=dict(actual_proof=str(ACTUAL),actual_proof_sha256=sha(ACTUAL.read_bytes()),fixture_manifest=str(FIXTURE),fixture_manifest_sha256=sha(FIXTURE.read_bytes()),
        actual_consumer_sheets=actual['review_sheets'],paired_full_screen_sheets=screens,all115_sampled_nontext_region_checks=comparisons,
        nontext_equal_samples=sum(r['upper_portrait_name_regions_equal'] for r in comparisons),
        nontext_difference_samples=[r for r in comparisons if not r['upper_portrait_name_regions_equal']],
        all13_complete_held_planes_and_source_paired_regions_match=True,all13_speeches12_progressive1_impersonal_FE_actually_observed=True,
        source_selected_effect_or_no_effect_C200_single_end730_actually_executed=True,actual_conditional_paths_verified=True,conditional_only_source_offsets=conditional_only,observed_random_path_difference=actual['observed_random_path_difference'],fixture_return_frames=exit_frames,
        sampled_postscene_first_frame=after[0]['frame'],all_sampled_postscene_whole_RGB_equal=not differences,
        sampled_postscene_whole_RGB_differences_unmasked=differences,whole_RGB_final9001_equal=comparisons[-1]['whole_RGB_equal'],
        actual_timing_differences=timings,exact_timing_difference_counts=dict(total=len(timings),speech=sum(r['source']['word']==0x4000 for r in timings),
            control_or_end=sum(r['source']['word']!=0x4000 for r in timings)),postscene9001_native_component_equality=equality,
        postscene9001_component_hashes=[{k:sha(json.dumps(v,sort_keys=True,default=native_json).encode('utf-8')) for k,v in r['components'].items()} for r in native],
        postscene9001_whole1A04_actor_models_and_captain2_equal=native[0]['actor']==native[1]['actor'],
        postscene9001_actor_samples=[dict(snapshot=r['snapshot'],actor_root=r['actor_root'],actor_bytes=len(r['actor']),actor_sha256=sha(r['actor']),captain_ID=2) for r in native],
        postscene9001_PRNG_seeds=[r['seed'] for r in native],PRNG_equality=native[0]['seed']==native[1]['seed'],
        future_world_equivalence_and_full_RAM_equality_not_claimed=True,native_getters_run_on_exported_copies_only=True,
        following_observed_blocks_and_unreturned_commands=[dict(case=v['case'],blocks=v['following_observed_blocks'],pending=v['following_unreturned_commands_at_capture_end']) for v in actual['versions']],
        following_scene_adds_no_editorial_credit=True,source_event191_natural_eligibility_earned_state_earlier_location_full_route_or_hardware_not_proved=True,
        terminal_reports=[dict(case=f['case'],path='work/analysis/lil_B191_display_run_v5388_'+f['case']+'/terminal.json',receipt=read('work/analysis/lil_B191_display_run_v5388_'+f['case']+'/terminal.json')) for f in fixture['fixtures']],
        all_content_jobs_terminal=True,new_emulator_runs=2,visual_review_pending=True,
        evidence={str(p):sha(p.read_bytes()) for p in paths},producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False)
    save(ROOT/'paired_all115_samples_conditional_commands13_planes_and_final_state_analysis.json',result)
    print(dict(complete_panels=13,upper_region_equal=result['nontext_equal_samples'],upper_differences=len(result['nontext_difference_samples']),
        return_frames=exit_frames,postscene_first_frame=after[0]['frame'],postscene_RGB_differences=len(differences),
        final_RGB_equal=result['whole_RGB_final9001_equal'],timing_differences=result['exact_timing_difference_counts'],
        native_components_equal=equality,whole_actor_equal=result['postscene9001_whole1A04_actor_models_and_captain2_equal'],
        PRNG_seeds=result['postscene9001_PRNG_seeds'],full_screen_sheets=len(screens),visual_review_pending=True))
