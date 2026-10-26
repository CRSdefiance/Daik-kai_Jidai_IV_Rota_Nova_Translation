"""Independent terminal/input/fixture audit of the actual close-range notice."""
import json
import struct
from pathlib import Path
from PIL import Image
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.native_two_stage_sighting_v1786b import apply_fixture
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/close_sighting_terminal_v1791')
RUN=Path('work/analysis/two_stage_sighting_v1787_twoStageReady8')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193/two_stage_sighting_v1787_1775_twoStageReady8')
LIVE=Path('work/analysis/close_sighting_live_v1790/two_complete_close_range_holds_before_dismissal.json')
NAV=Path('work/analysis/two_stage_navigation_v1788/selected_original_event_hold_ready.json')

if __name__=='__main__':
    assert not ROOT.exists()
    plan,report,journal,preservation,live,nav=map(read,(RUN/'run_plan.json',CAP/'capture_report.json',
        CAP/'navigation_command_journal.json',RUN/'terminal_preservation.json',LIVE,NAV))
    rom=Path(plan['candidate']);arm=NdsImage.open(rom).read_file('/__arm9__.bin');digest=sha(rom.read_bytes())
    assert digest==plan['candidate_sha256']==report['ROM_sha256']==live['candidate_sha256']
    assert report['frames']==5503 and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report['hardware_device_verification'] and not report['goal_complete']
    for key in ('source_donor','disposable_donor'):assert sha(Path(plan[key]).read_bytes())==plan['source_donor_sha256']
    assert preservation['source_and_disposable_donors_unchanged']
    commands=[json.loads(s)for s in (RUN/'navigation.jsonl').read_text(encoding='utf-8').splitlines()if s.strip()]
    assert commands==[r['command']for r in journal['commands_received']]
    assert all(r['validation_passed']for r in journal['commands_received'])
    assert commands[-2:]==[{'until':5503,'buttons':['A'],'duration':8},{'stop':True}]
    schedule=list(read(plan['inputs']));assert sha(Path(plan['inputs']).read_bytes())==plan['inputs_sha256']
    for r in journal['commands_received']:
        c=r['command']
        if c.get('buttons')or c.get('touch'):
            event={'start':r['frame']+1,'duration':c['duration'],'buttons':c.get('buttons',[])}
            if c.get('touch'):event['touch']=c['touch']
            schedule.append(event)
    assert schedule==report['scripted_input_schedule']
    snapshots={}
    for r in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']+[report['read_only_RAM_snapshot']]:
        data=Path(r['path']).read_bytes();assert len(data)==r['bytes']==0x400000 and sha(data)==r['sha256'] and r['read_only_export']
        snapshots[r.get('frame',5503)]=r
    for r in report['frames_captured']:
        assert sha(Path(r['path']).read_bytes())==r['PNG_sha256'] and Image.open(r['path']).size==(256,384)
    fixtures=report['synthetic_battle_recovery_proximity_fixtures'];assert len(fixtures)==13
    assert [r['frame']for r in fixtures]==list(range(5100,5113))
    replay=[]
    for row in journal['commands_received']:
        command=row['command']
        if not command.get('battle_fixture'):continue
        frame=row['frame'];fixture=next(r for r in fixtures if r['frame']==frame)
        data=Path(snapshots[frame]['path']).read_bytes();after,receipt=apply_fixture(arm,data,command['battle_fixture'])
        assert fixture=={**receipt,'frame':frame} and sha(after)==fixture['after_RAM_sha256']
        assert len(receipt['owned_bytes'])==(17 if frame==5100 else 16)
        replay.append({'frame':frame,'context':receipt['context'],'owned_bytes':len(receipt['owned_bytes']),
            'all4MiB_independent_replay_exact':True,'after_RAM_sha256':sha(after)})
    rows=nav['observations'];assert rows[0]['frame']==5100 and rows[-1]['frame']==5113
    loaded_unseen=[r for r in rows if 8 in bytes.fromhex(r['groups_hex'])[::4]and not r['enemy8_seen']]
    assert len(loaded_unseen)>=2 and rows[-1]['enemy8_seen'] and not any(r['enemy8_seen']for r in rows[:-1])
    assert next(r['frame']for r in rows if r['fixture_preflight']['context']=='closeLoaded8')>loaded_unseen[0]['frame']
    assert all(r['fixture_preflight']['native_known_town_scan']==115 for r in rows[:-1])
    final=Path(snapshots[5503]['path']).read_bytes();cpu,get=get_machine(arm,final)
    assert list(struct.unpack('<3I',cpu.mem_read(get(0x3F0F8)+8,12)))==[0,1,8]
    root=get(0xCB1A8);groups=bytes(cpu.mem_read(root+0x2080,16))
    assert 8 in groups[::4] and cpu.mem_read(root+4+8*132+0x50,1)[0]&4
    ROOT.mkdir(parents=True)
    save(ROOT/'complete_close_range_scene_and_fixture_audit.json',{'candidate':str(rom),'candidate_sha256':digest,
        'terminal_frame':5503,'full_holds_proof':str(LIVE),'full_holds_sha256':sha(LIVE.read_bytes()),
        'two_complete_current_native_independent_actual_holds':live['holds'],
        'all13_fixtures_independently_replayed_entire4MiB':replay,
        'original_fleet8_loaded_unseen_before_close_approach':loaded_unseen,
        'seen_flag_changes_only_after_original_gameplay_step_not_fixture':True,
        'normal_single_A_dismissal_to_viewed_Sea_View':True,'original_pending_battle_context':[0,1,8],
        'no_complete_battle_playthrough_claim':True,'no_savestate_input_source_and_disposable_saves_unchanged':True,
        'all_input_schedules_PNG_hashes_RAM_snapshots_and_fixture_receipts_verified':True,
        'location_and_initial_source_relation_prerequisite_only_no_message_or_outcome_injection':True,
        'terminal_capture':str(CAP/'frame_005503_navigation.png'),
        'terminal_capture_sha256':sha((CAP/'frame_005503_navigation.png').read_bytes()),
        'proofs':{str(p):sha(p.read_bytes())for p in [RUN/'run_plan.json',CAP/'capture_report.json',CAP/'navigation_command_journal.json',RUN/'terminal_preservation.json',LIVE,NAV]},
        'producer_sha256':sha(Path(__file__).read_bytes()),'no_editorial_completion_credit_yet':True,'full_goal_complete':False})
    print('Close-range614 terminal5503:13 exact4MiB fixture replays,original unseen loading/seen selection,two complete font holds,normal A return andunchanged saves verified.',flush=True)
