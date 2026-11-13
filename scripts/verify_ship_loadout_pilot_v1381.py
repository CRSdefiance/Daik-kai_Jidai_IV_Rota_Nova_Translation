"""Audit45-byte prebattle equipment pilots;do not infer a sinking outcome."""
import json
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_ship_cannon_fixture_v1378 import apply_fixture
from scripts.verify_village_wrap_v608 import read,save

ROM = Path('out/all_routes_combined_v1364_candidate.nds')


def audit(run,cap,terminal_frame):
    report_path = cap/'capture_report.json'
    report,plan,terminal = [read(p) for p in [report_path,run/'run_plan.json',run/'terminal_preservation.json']]
    assert report['frames']==terminal_frame and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not report['hardware_device_verification'] and not report['goal_complete']
    digest = sha(ROM.read_bytes())
    assert report['ROM_sha256']==plan['candidate_sha256']==digest=='dbf86d020cb868f443f9c6a9f68706e8cda28e9268ce0318a63ef765f4f3281c'
    assert sha(Path(plan['source_donor']).read_bytes())==sha(Path(plan['disposable_donor']).read_bytes())==terminal['source_donor_sha256']
    assert terminal['source_and_disposable_donors_unchanged']
    assert sha((run/'navigation.jsonl').read_bytes())==terminal['navigation_sha256']
    assert sha(Path('scripts/headless_desmume_v193.py').read_bytes())==plan['harness_sha256']
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = [(0x1856C,0x18574),(0x48144,0x481B4),(0x74538,0x74750),(0x751E0,0x756FC),
        (0x72734,0x72BD8),(0xAAF38,0xAB008),(0xAB71C,0xAB7AC)]
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
    after,fixture = apply_fixture(arm,raw,{'ship_sinking_context':'five_ship_approach'})
    assert report['synthetic_battle_recovery_proximity_fixtures']==[{**fixture,'frame':4800}]
    assert len(fixture['owned_bytes'])==45
    assert {0x02000000+i for i,(a,b) in enumerate(zip(raw,after,strict=True)) if a!=b}<=set(fixture['owned_bytes'])
    assert [r['after'] for r in fixture['cannon_equipment']]==[4,7,7,7,7]
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
        'entire4MiB_sole_prebattle45_owned_byte_fixture_and_all_input_schedule_audited':True,
        'sole_fixture':fixture,'source_and_disposable_donor_unchanged':True,
        'source_donor_sha256':terminal['source_donor_sha256'],'original_clean_code_spans':spans,
        'no_further_battle_or_duel_fixture_health_equipment_position_ability_actor_ID_RNG_or_result_edit':True,
        'source_census_and_fixture_equipment_are_not_earned_acquisition':True,
        'no_ROM_build_or_change':True,'targeted_headless_not_complete_route_or_hardware':True,
        'shared_auditor_sha256':sha(Path(__file__).read_bytes())}
    return receipt,snapshots,arm


if __name__=='__main__':
    root = Path('work/analysis/ship_loadout_pilot_verified_v1381')
    assert not root.exists()
    run = Path('work/analysis/ship_sinking_loadout_v1379')
    cap = Path('E:/Rota Nova translations/Generated/work/emulation_v193/ship_sinking_loadout_v1379_1364')
    assert sha(Path('scripts/run_ship_sinking_loadout_v1379.py').read_bytes())==read(run/'run_plan.json')['runner_sha256']
    proof,snapshots,arm = audit(run,cap,11830)
    last = read('work/analysis/ship_loadout_inspection_v1380/frame_011170.json')
    assert next(s for s in last['ships'] if (s['fleet'],s['slot'])==(5,2))['Hull_Crew']==[10,12]
    assert not any('touch' in r['command'] for r in read(cap/'navigation_command_journal.json')['commands_received'])
    proof.update(target_Hull_Crew_before_duel=[10,12],
        actual_duel_intro_at11830_visually_observed=True,
        original_proximity_duel_can_start_without_any_touchscreen_input=True,
        stopped_at_duel_intro_without_changing_duel_or_claiming_sinking=True,
        next_action='Replay through10090 and close sails before coast collision turns the flagship toward the enemy.',
        no_translation_completion_credit=True,full_goal_complete=False)
    root.mkdir(parents=True)
    save(root/'actual_loadout_pilot_verification.json',proof)
    print('45-byte equipment pilot/all4MiB/input/donors audited;target10Hull12Crew;proximity duel without touch;no sinking credit.',flush=True)
