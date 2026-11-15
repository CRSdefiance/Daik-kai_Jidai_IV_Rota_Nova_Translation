"""Record all viewed B175 panels, scoped transition differences and paired native state."""
import json
import struct
from pathlib import Path
from PIL import Image,ImageChops
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_market_gameplay_v753 import state
from scripts.verify_shipyard_gameplay_v760 import models
from scripts.verify_tavern_gameplay_v767 import persistent_objects
from scripts.verify_followup_gameplay_v778 import tasks
from scripts.verify_ceremony_prayer_gameplay_v814 import calendar
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B175_actual_review_v4535')
ACTUAL=Path('work/analysis/lil_B175_actual_v4534/actual_all32_progressive_FE_controls_C200_and_first_end.json')
FIXTURE=Path('work/analysis/lil_B175_display_fixture_v4531/complete_B175_B22_fixtures.json')
BASE=Path('E:/Rota Nova translations/Generated/work/emulation_v193')

def native_json(value):
    assert isinstance(value,bytes)
    return {'native_byte_span_hex':value.hex()}

if __name__=='__main__':
    assert not ROOT.exists()
    actual,fixture=read(ACTUAL),read(FIXTURE)
    assert actual['complete_matching_observations']==32 and not actual['failures'] and not actual['paired_region_differences']
    sheets=[]
    for s in actual['review_sheets']:
        assert sha(Path(s['path']).read_bytes())==s['sha256']
        sheets.append({**s,'viewed':True,'review':'Viewed complete32 progressive/FE panels across six sheets: recognition,encirclement,pirate-pride rebuke,sea challenge,FI/FA introduction,admiral tease,sword threat,departure,relief and closing banter. Every leading/internal/trailing character and punctuation is complete. Five named voices retain their native portraits/nameplates;all nine FE panels remain anonymous without a bottom-screen portrait or invented name. The original woman illustration is an upper-screen presentation,not a guessed static speaker. Thirteen retained wordings remain natural in the full exchange.'})
    assert len(sheets)==6
    reports=[];photos=[];snapshots=[];arms=[];paths=[ACTUAL,FIXTURE,Path(__file__)]
    for f in fixture['fixtures']:
        folder=BASE/('lil_B175_display_v4533_'+f['case']);reportpath=folder/'capture_report.json';report=read(reportpath)
        assert report['frames']==16001 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['ROM_sha256']==f['research_ROM_sha256']==sha(Path(f['research_ROM']).read_bytes())
        snapshot=report['read_only_RAM_snapshot'];raw=Path(snapshot['path']).read_bytes()
        assert snapshot['read_only_export'] and len(raw)==4194304 and sha(raw)==snapshot['sha256']
        reports.append(report);photos.append({p['frame']:p for p in report['frames_captured']});snapshots.append((snapshot,raw))
        arms.append(NdsImage.open(f['research_ROM']).read_file('/__arm9__.bin'))
        paths.extend([reportpath,Path(snapshot['path']),folder/'observer/commands.json'])
    assert arms[0]==arms[1] and photos[0].keys()==photos[1].keys()
    comparisons=[];differences=[]
    for frame,source in sorted(photos[0].items()):
        english=photos[1][frame]
        for p in [source,english]:assert sha(Path(p['path']).read_bytes())==p['PNG_sha256']
        a,b=[Image.open(p['path']).convert('RGB') for p in [source,english]]
        bbox=ImageChops.difference(a.crop((0,0,256,294)),b.crop((0,0,256,294))).getbbox()
        row=dict(frame=frame,source=source,English=english,upper_portrait_name_regions_equal=bbox is None,
            nontext_difference_bbox=bbox,whole_RGB_equal=a.tobytes()==b.tobytes())
        comparisons.append(row)
        if bbox:
            if frame in [3370,8890]:
                site=72 if frame==3370 else 1264
                pair=[next(r for r in v['source_three_presentations'] if r['original_source_offset']==site) for v in actual['versions']]
                assert all(r['start']<frame<r['returned'] for r in pair)
                assert pair[0]['start']-pair[1]['start']==pair[0]['returned']-pair[1]['returned']==1
                assert pair[0]['returned']-pair[0]['start']==(72 if site==72 else 40)
                row.update(scope='Viewed original upper-screen presentation transition at the same frame;one-frame start/return difference and equal native duration. No screenshot retiming or masking.',source_presentation_offset=site,paired_command_intervals=pair)
            else:
                assert frame>=15370 and bbox==(60,193,132,284)
                assert ImageChops.difference(a,b).getbbox()==bbox
                assert a.crop((0,0,256,192)).tobytes()==b.crop((0,0,256,192)).tobytes()
                assert a.crop((0,294,256,384)).tobytes()==b.crop((0,294,256,384)).tobytes()
                row.update(scope='Viewed differing foreground cloud in the following sailing scene;map and complete text panel remain exact. PRNG differs;no new causal trace or future-world equality is claimed.')
            differences.append(row)
    assert len(comparisons)==232 and len(differences)==14
    assert {r['frame'] for r in differences if r['frame']<15370}=={3370,8890}
    assert len([r for r in differences if r['frame']>=15370])==12
    assert all(next(r for r in comparisons if r['frame']==f)['whole_RGB_equal'] for f in [10570,10630,10690,10750,10810,10870])
    notes={3370:'Viewed paired full screens during original4696 presentation:the same anonymous woman illustration is opening at different one-frame transition positions. Both native durations are72frames. No identity is inferred from the illustration or CA80 operand.',
        8890:'Viewed paired full screens during original4635 presentation:the same return-to-interior shutter transition differs by one animation frame. Both native durations are40frames. No text defect or forced actor is introduced.',
        10570:'Viewed whole-RGB-identical initialized Amsterdam town return after C200 and first end. Amsterdam is the disclosed B22 fixture location,not an inferred B175 source location. Town UI/funds are inherited test state.',
        16001:'Viewed following sailing/departure screen in both versions. The map and complete Ski Snow / Departed Amsterdam text panel match;the bounded foreground-cloud region differs. Following B120/sailing adds no editorial credit or full-world equality claim.'}
    views=[]
    for version,photo in zip(['clean_Japanese','reviewed_English'],photos,strict=True):
        for frame,note in notes.items():
            p=photo[frame];views.append(dict(case=version,frame=frame,path=p['path'],sha256=p['PNG_sha256'],viewed=True,review=note));paths.append(Path(p['path']))
    native=[]
    for (snapshot,raw),arm in zip(snapshots,arms,strict=True):
        components={fn.__name__:fn(arm,raw) for fn in [state,models,persistent_objects,tasks,calendar]}
        cpu,get=get_machine(arm,raw);root,captain=get(0xCB184),get(0x7F244)
        assert captain==2 and 0x02000000<=root<=0x02400000-0x1A04
        native.append(dict(snapshot=snapshot,components=components,actor=bytes(cpu.mem_read(root,0x1A04)),actor_root=root,captain_ID=captain,
            seed=struct.unpack_from('<I',raw,0x168EB8)[0]))
    equality={k:native[0]['components'][k]==native[1]['components'][k] for k in native[0]['components']}
    assert all(equality.values()) and native[0]['actor']==native[1]['actor']
    timings=[dict(source=a,English=b) for a,b in zip(actual['versions'][0]['selected_B22_command_pairs'],actual['versions'][1]['selected_B22_command_pairs'],strict=True)
        if (a['start'],a['returned'])!=(b['start'],b['returned'])]
    assert len(timings)==30
    for v in actual['versions']:
        assert len(v['selected_B22_command_pairs'])==47 and len(v['selected_intervals'])==32
        assert v['first_source_end1702_actually_reached'] and v['second_source_end1706_stored_but_unvisited_offline_decoder_only']
        assert v['source_C200']['result_words']==[3,0] and v['selected_B22_command_pairs'][-1]['result_words']==[0,0]
        assert v['following_observed_blocks']==[120]
    ROOT.mkdir(parents=True)
    save(ROOT/'all6_actual_sheets_32_planes_scoped_transitions_return_and_final_state.json',dict(
        all6_actual_sheets_viewed=sheets,paired_full_screen_views=views,all232_sampled_nontext_region_checks=comparisons,
        all32_complete_held_planes_and_source_paired_regions_match=True,nontext_equal_samples=218,nontext_difference_samples=differences,
        two_original_presentation_transition_differences_at_equal_duration_one_frame_offset=True,
        twelve_following_sailing_foreground_cloud_differences_bounded_and_unmasked=True,
        whole_RGB_town10570_through10870_equal=True,final16001_whole_RGB_equality_not_claimed=True,
        all32_speeches23_progressive9_FE_actually_observed=True,source_C2001700_and_first_end1702_actually_reached=True,
        second_declared_end1706_offline_native_only=True,no_source_command_omission_flattening_or_forced_actor=True,
        original_three_presentation_resource_and_FE_transitions_preserved=True,actual47_of48_stored_fixture_commands_selected=True,
        actual_timing_differences=timings,exact_timing_difference_counts=dict(total=30,speech=sum(r['source']['word']==0x4000 for r in timings),control_or_end=sum(r['source']['word']!=0x4000 for r in timings)),
        postscene16001_native_component_equality=equality,
        postscene16001_component_hashes=[{k:sha(json.dumps(v,sort_keys=True,default=native_json).encode('utf-8')) for k,v in r['components'].items()} for r in native],
        postscene16001_whole1A04_actor_models_and_captain2_equal=True,
        postscene16001_actor_samples=[dict(snapshot=r['snapshot'],actor_root=r['actor_root'],actor_bytes=len(r['actor']),actor_sha256=sha(r['actor']),captain_ID=2) for r in native],
        postscene16001_PRNG_seeds=[r['seed'] for r in native],PRNG_equality_causal_trace_and_future_world_equivalence_not_claimed=True,
        full_RAM_equality_not_claimed_native_getters_run_on_exported_copies_only=True,
        representative_actual_coverage_sufficient_for_this_distinct_display_scope=True,no_open_translation_specific_display_or_control_finding=True,
        no_natural_event175_eligibility_earned_flags_full_route_or_hardware_claim=True,new_emulator_runs=2,
        reaped_tool_sessions=[dict(case='clean_Japanese',session_id=16289,exit_code=0),dict(case='reviewed_English',session_id=16795,exit_code=0)],
        all_content_jobs_terminal=True,evidence={str(p):sha(p.read_bytes()) for p in paths},producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(dict(viewed_sheets=6,complete_panels=32,FE=9,nontext_equal=218,nontext_scoped_differences=14,town_return_equal=True,
        final_native_components_and_actor_equal=True,final_foreground_cloud_difference_retained=True,timing_differences=30,new_boots=2))
