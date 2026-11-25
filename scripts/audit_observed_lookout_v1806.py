"""Terminal independent replay of declared fixtures and read-only original rolls."""
import json
import struct
from collections import Counter
from pathlib import Path
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_lookout_contact_v1798b import apply_fixture,ROM
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lookout_terminal_v1806')
RUN=Path('work/analysis/observed_lookout_v1799')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/observed_lookout_v1799_1775')

if __name__=='__main__':
    assert not ROOT.exists();ROOT.mkdir(parents=True)
    plan=read(RUN/'run_plan.json');report=read(CAP/'capture_report.json');terminal=read(RUN/'terminal.json')
    assert terminal['terminal']and terminal['frame']==report['frames']==6471
    assert terminal['source_and_disposable_donors_unchanged']and terminal['all_observer_slots_restored']
    assert report['cold_boot']and not report['savestate_loaded']and not report['callback_errors']
    assert not report['hardware_device_verification']and not report['goal_complete']
    assert sha(ROM.read_bytes())==plan['candidate_sha256']==report['ROM_sha256']
    for key in('source_donor','disposable_donor'):assert sha(Path(plan[key]).read_bytes())==plan['source_donor_sha256']
    journal=read(CAP/'navigation_command_journal.json');commands=[json.loads(s)for s in(RUN/'navigation.jsonl').read_text().splitlines()if s]
    assert commands==[r['command']for r in journal['commands_received']]
    assert all(r['validation_passed']for r in journal['commands_received'])and commands[-1]=={'stop':True}
    schedule=list(read(plan['inputs']))
    for r in journal['commands_received']:
        c=r['command']
        if c.get('buttons')or c.get('touch'):
            event={'start':r['frame']+1,'duration':c['duration'],'buttons':c.get('buttons',[])}
            if c.get('touch'):event['touch']=c['touch']
            schedule.append(event)
    assert schedule==report['scripted_input_schedule']
    snapshots={}
    for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']+[report['read_only_RAM_snapshot']]:
        data=Path(r['path']).read_bytes();assert len(data)==r['bytes']==0x400000 and sha(data)==r['sha256']and r['read_only_export']
        snapshots[r.get('frame',6471)]=r
    for r in report['frames_captured']:assert sha(Path(r['path']).read_bytes())==r['PNG_sha256']and Image.open(r['path']).size==(256,384)
    arm=NdsImage.open(ROM).read_file('/__arm9__.bin');fixtures=report['synthetic_battle_recovery_proximity_fixtures']
    assert len(fixtures)==206;replays=[]
    for r in journal['commands_received']:
        command=r['command']
        if not command.get('battle_fixture'):continue
        frame=r['frame'];fixture=next(f for f in fixtures if f['frame']==frame)
        raw=Path(snapshots[frame]['path']).read_bytes();after,receipt=apply_fixture(arm,raw,command['battle_fixture'])
        assert fixture=={**receipt,'frame':frame}and sha(after)==fixture['after_RAM_sha256']
        replays.append({'frame':frame,'context':receipt['context'],'owned_bytes':len(receipt['owned_bytes']),
            'independent_entire4MiB_replay_exact':True,'after_RAM_sha256':sha(after)})
        if len(replays)%40==0:print({'independent_fixture_replays':len(replays)},flush=True)
    trace_path=CAP/'observer/original_shot_trace.json';trace=read(trace_path)
    assert trace['all_host_slots_restored_and_core_file_exact']and not trace['errors']and not trace['mismatches']
    assert trace['callbacks']==len(trace['rows'])and all(r['CPU_WRAM_DTCM_ITCM_and_configuration_unchanged_by_callback']for r in trace['rows'])
    counts=dict(Counter(r['kind']for r in trace['rows']));rolls=[r for r in trace['rows']if r['kind']=='native_roll_compare']
    assert len(rolls)==12 and not any(r['native_shot_condition_met']for r in rolls)
    assert all(0<=r['original_RNG_roll']<2000 and r['original_Aim_div10_threshold']==16 for r in rolls)
    assert not counts.get('shot_announcement',0)and not counts.get('shot_message_return',0)
    levels=[]
    for frame in(5503,6465,6471):
        raw=Path(snapshots[frame]['path']).read_bytes();cpu,get=get_machine(arm,raw);actor=get(0xCB184)+4+16*32;root=get(0xCB1A8)
        levels.append({'frame':frame,'level':get(0x7E728,actor),'native_Lookout_Aim':get(0x8235C,root+0x2090,7,6,0),
            'actor32_hex':bytes(cpu.mem_read(actor,32)).hex()})
    assert levels[0]['level']==37 and levels[-1]['level']==38 and levels[-1]['native_Lookout_Aim']==168
    actor=get(0xCB184)+4+16*32
    assert all(not(set(f['owned_bytes'])&set(range(actor,actor+32))-{actor+13})for f in fixtures)
    proof={'candidate':str(ROM),'candidate_sha256':sha(ROM.read_bytes()),'terminal_frame':6471,
        'cold_boot_report':str(CAP/'capture_report.json'),'cold_boot_report_sha256':sha((CAP/'capture_report.json').read_bytes()),
        'all206_declared_fixtures_independently_replayed_entire4MiB':replays,'all_input_PNG_RAM_and_save_hashes_verified':True,
        'source_and_disposable_battery_saves_unchanged':True,'observer_trace':str(trace_path),'observer_trace_sha256':sha(trace_path.read_bytes()),
        'observer_counts':counts,'original_qualifying_shot_rolls':[{'frame':r['frame'],'roll':r['original_RNG_roll'],
            'threshold':r['original_Aim_div10_threshold']}for r in rolls],
        'all_original_rolls_failed_threshold_no_successful_shot_claim':True,'read_only_callback_and_terminal_host_restoration_checks_pass':True,
        'boundary_checks_do_not_exclude_temporary_write_restore':True,'native_level_and_Aim_observations':levels,
        'Lookout_level_and_experience_never_owned_by_any_fixture':True,
        'final_precondition_stop_was_fixture_assumption_level37_not_a_ROM_defect':True,
        'capture_notice_at5805_full_holds6105_6135_and_normal_A_return6195_visually_observed':True,
        'that_navigation_notice_is_not_the_successful_shot_or_full_battle_verification':True,
        'next_fixture_must_preserve_current_native_level_and_Aim_instead_of_requiring_frozen37_166':True,
        'no_native_RNG_message_result_or_live_cursor_override':True,'no_editorial_completion_credit':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'terminal_contact_roll_and_fixture_audit.json',proof)
    print('206 whole4MiB fixture replays and12 original failed shot rolls verified;native level38/Aim168 explains safe stop. No shot credit.',flush=True)
