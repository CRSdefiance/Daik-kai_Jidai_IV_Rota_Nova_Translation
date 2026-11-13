"""Audit the three terminal41-byte activation pilots;none loaded a target."""
import json
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_sea_inspection_fixture_v1552b import apply_fixture
from scripts.verify_village_wrap_v608 import read,save
ROM = Path('out/all_routes_combined_v1542_candidate.nds')
def audit(run,cap,terminal_frame):
    report_path = cap/'capture_report.json'
    report,plan,terminal = [read(p) for p in [report_path,run/'run_plan.json',run/'terminal_preservation.json']]
    assert report['frames']==terminal_frame and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not report['hardware_device_verification'] and not report['goal_complete']
    digest = sha(ROM.read_bytes())
    assert report['ROM_sha256']==plan['candidate_sha256']==digest=='b8b256650bb426e99012be06fd060114da0fbf32f763b5c3434204dda8f50437'
    assert sha(Path(plan['source_donor']).read_bytes())==sha(Path(plan['disposable_donor']).read_bytes())==terminal['source_donor_sha256']
    assert terminal['source_and_disposable_donors_unchanged']
    assert sha((run/'navigation.jsonl').read_bytes())==terminal['navigation_sha256']
    assert sha(Path('scripts/headless_desmume_v193.py').read_bytes())==plan['harness_sha256']
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = [(0x34674,0x34688),(0x36C70,0x36CB8),(0xAB128,0xAB18C),
        (0x55850,0x55874),(0x18398,0x183A8),(0x181BC,0x181C4),(0x6F610,0x6F680)]
    assert all(arm[a:b]==clean[a:b] for a,b in spans)
    snapshots = {}
    for row in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']:
        body = Path(row['path']).read_bytes()
        assert len(body)==row['bytes']==0x400000 and sha(body)==row['sha256']
        if row['frame'] in snapshots:
            assert snapshots[row['frame']]['sha256']==row['sha256']
        snapshots[row['frame']] = row
    for row in report['frames_captured']:
        assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
    raw = Path(snapshots[4800]['path']).read_bytes()
    after,fixture = apply_fixture(arm,raw,{'sea_inspection_context':'activate_existing_Monster_Fish'})
    assert report['synthetic_battle_recovery_proximity_fixtures']==[{**fixture,'frame':4800}]
    assert len(fixture['owned_bytes'])==41
    assert {0x02000000+i for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a!=b}<=set(fixture['owned_bytes'])
    assert not any(v for k,v in report.items() if k.startswith('synthetic_') and k!='synthetic_battle_recovery_proximity_fixtures')
    commands = [json.loads(line) for line in (run/'navigation.jsonl').read_text(encoding='utf-8').splitlines()]
    journal = read(cap/'navigation_command_journal.json')['commands_received']
    assert commands==[r['command'] for r in journal]
    assert journal[-1]['frame']==terminal_frame and journal[-1]['command']=={'stop':True}
    schedule = read(run/'original_departure_inputs.json')
    for item in journal:
        assert item['validation_passed']
        command = item['command']
        if command.get('stop'):
            continue
        assert set(command)<={'until','buttons','touch','duration','battle_fixture'}
        assert command['until'] in snapshots and command['until']>item['frame']
        if item['frame']>4800:
            assert 'battle_fixture' not in command
        if command.get('buttons') or command.get('touch') is not None:
            event = {'start':item['frame']+1,'duration':command.get('duration',12),'buttons':command.get('buttons',[])}
            if command.get('touch') is not None:
                event['touch'] = command['touch']
            schedule.append(event)
    assert schedule==report['scripted_input_schedule']
    receipt = {'candidate':str(ROM),'candidate_sha256':digest,'terminal_frame':terminal_frame,
        'terminal_report':str(report_path),'terminal_report_sha256':sha(report_path.read_bytes()),
        'run_plan':str(run/'run_plan.json'),'navigation_sha256':terminal['navigation_sha256'],
        'complete_primary_RAM_and_PNG_hash_audits':True,'snapshot_count':len(snapshots),'capture_count':len(report['frames_captured']),
        'entire4MiB_sole_prebattle41_owned_byte_fixture_and_all_input_schedule_audited':True,
        'sole_fixture':fixture,'source_and_disposable_donor_unchanged':True,
        'source_donor_sha256':terminal['source_donor_sha256'],'original_clean_code_spans':spans,
        'no_further_battle_or_duel_fixture_health_equipment_position_ability_actor_ID_RNG_or_result_edit':True,
        'artificial_existing_fleet_activation_not_natural_spawn':True,
        'no_ROM_build_or_change':True,'targeted_headless_not_complete_route_or_hardware':True,
        'shared_auditor_sha256':sha(Path(__file__).read_bytes())}
    return receipt,snapshots,arm

if __name__ == '__main__':
    root=Path('work/analysis/sea_activation_pilots_v1552f')
    assert not root.exists()
    receipts=[]
    for label,frame in [('sea_inspection_pilot_v1552c',4900),('sea_inspection_pilot_v1552d',5100),('sea_inspection_live_v1552e',5920)]:
        run=Path('work/analysis')/label
        cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/(label+'_1542')
        proof,snapshots,arm=audit(run,cap,frame)
        proof.update(original_special_target_not_loaded=True,no_sea_response_activation_or_editorial_completion_credit=True,full_goal_complete=False)
        receipts.append(proof)
    root.mkdir(parents=True)
    save(root/'three_terminal_pilots_audited.json',{'pilots':receipts,'next_action':'Trace original live-party registration;the at-sea flag alone does not load a mobile.','full_goal_complete':False})
    print('All3 terminal pilots audited:41 owned bytes,entire4MiB,input schedules,RAM/PNG and donors;no target/event credit.')
