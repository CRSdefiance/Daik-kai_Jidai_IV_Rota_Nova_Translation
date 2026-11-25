"""Audit the terminal original-combat pilot without granting sinking credit."""
import json
from copy import deepcopy
from pathlib import Path
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.rom.nds import NdsImage
from scripts.native_flagship_capture_fixture_v1368 import apply_fixture
from scripts.inspect_ship_sinking_live_v1374 import inspect,CAP,ROM
from scripts.verify_village_wrap_v608 import read,save

ROOT = Path('work/analysis/ship_sinking_gunnery_verified_v1375')
RUN = Path('work/analysis/ship_sinking_gunnery_v1373')


def main():
    assert not ROOT.exists()
    report_path = CAP/'capture_report.json'
    report,plan,terminal = [read(p) for p in [report_path,RUN/'run_plan.json',RUN/'terminal_preservation.json']]
    digest = sha(ROM.read_bytes())
    assert digest==report['ROM_sha256']==plan['candidate_sha256']
    assert report['frames']==11360 and report['cold_boot'] and not report['savestate_loaded']
    assert not report['callback_errors'] and not report['hardware_device_verification'] and not report['goal_complete']
    assert terminal['source_and_disposable_donors_unchanged']
    assert sha(Path(plan['source_donor']).read_bytes())==sha(Path(plan['disposable_donor']).read_bytes())==terminal['source_donor_sha256']
    assert sha((RUN/'navigation.jsonl').read_bytes())==terminal['navigation_sha256']
    assert sha(Path('scripts/run_ship_sinking_gunnery_v1373.py').read_bytes())==plan['runner_sha256']
    assert sha(Path('scripts/headless_desmume_v193.py').read_bytes())==plan['harness_sha256']
    rom = NdsImage.open(ROM)
    arm = rom.read_file('/__arm9__.bin')
    clean = NdsImage.open('work/clean.nds').read_file('/__arm9__.bin')
    spans = [(0x751E0,0x756FC),(0x72734,0x72BD8),(0xAAF38,0xAB008)]
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
    before = Path(snapshots[4800]['path']).read_bytes()
    after,fixture = apply_fixture(arm,before,{'ship_sinking_context':'five_ship_approach'})
    assert report['synthetic_battle_recovery_proximity_fixtures']==[{**fixture,'frame':4800}]
    assert len(fixture['owned_bytes'])==40
    changed = {0x02000000+i for i,(a,b) in enumerate(zip(before,after,strict=True)) if a!=b}
    assert changed and changed<=set(fixture['owned_bytes'])
    assert not any(v for k,v in report.items() if k.startswith('synthetic_') and k!='synthetic_battle_recovery_proximity_fixtures')
    source_commands = [json.loads(line) for line in (RUN/'navigation.jsonl').read_text(encoding='utf-8').splitlines()]
    journal = read(CAP/'navigation_command_journal.json')['commands_received']
    assert source_commands==[item['command'] for item in journal]
    assert journal[-1]['frame']==11360 and journal[-1]['command']=={'stop':True}
    schedule = read(RUN/'original_departure_inputs.json')
    for item in journal:
        assert item['validation_passed']
        command = item['command']
        if command.get('stop'):
            continue
        assert command['until'] in snapshots and command['until']>item['frame']
        assert set(command)<={'until','buttons','touch','duration','battle_fixture'}
        if item['frame']>4800:
            assert 'battle_fixture' not in command
        if command.get('buttons') or command.get('touch') is not None:
            event = {'start':item['frame']+1,'duration':command.get('duration',12),'buttons':command.get('buttons',[])}
            if command.get('touch') is not None:
                event['touch'] = command['touch']
            schedule.append(event)
    assert schedule==report['scripted_input_schedule']
    prior = Path('E:/Rota Nova translations/Generated/work/emulation_v193/flagship_capture_v1369_1364')
    prefix = []
    for frame,row in sorted(snapshots.items()):
        if frame<=9100:
            assert sha((prior/f'frame_{frame:06d}_arm9_ram.bin').read_bytes())==row['sha256']
            prefix.append(frame)
    states = [inspect(frame,arm) for frame in [9100,9200,9250,9330,9390,9690,10090,10150,10210,10260,10360,10760,11060,11360]]
    assert all(row['mode']==[0,1,5] for row in states)
    def ship(frame,fleet,slot):
        return next(s for row in states if row['frame']==frame for s in row['ships'] if (s['fleet'],s['slot'])==(fleet,slot))
    assert ship(9100,5,2)['Hull_Crew']==[30,21]
    assert ship(10360,5,2)['Hull_Crew']==ship(11360,5,2)['Hull_Crew']==[26,0]
    assert all(s['Hull_Crew'][0]>0 for row in states for s in row['ships'])
    ROOT.mkdir(parents=True)
    proof = {'candidate':str(ROM),'candidate_sha256':digest,'terminal_frame':11360,
        'terminal_report':str(report_path),'terminal_report_sha256':sha(report_path.read_bytes()),
        'runner_sha256':plan['runner_sha256'],'navigation_sha256':terminal['navigation_sha256'],
        'all_primary_RAM_and_PNG_hashes_verified':True,'capture_count':len(report['frames_captured']),
        'snapshot_count':len(snapshots),'identical_current_ROM_replay_prefix_frames':prefix,
        'sole_prebattle_fixture':fixture,'entire4MiB_fixture_delta_and_every_input_audited':True,
        'source_and_disposable_donor_unchanged':True,'source_donor_sha256':terminal['source_donor_sha256'],
        'original_projectile_damage_hull_crew_and_cleanup_code_exact_clean':spans,
        'native_states':states,'natural_enemy_slot2_Hull_Crew_transition':[[30,21],[26,0]],
        'no_sinking_notice_seen_or_sinking_translation_completion_claimed':True,
        'stopped_by_test_harness_while_original_battle_active_not_a_gameplay_withdrawal':True,
        'next_action':'Choose a source-bound setup that can reduce Hull to zero before crew exhaustion;preserve healthy enemy state and original RNG/results.',
        'current16_sinking_entries_remain_native_integrated_and_actual_gameplay_pending':True,
        'no_ROM_build_change_or_canonical_promotion':True,
        'targeted_headless_test_not_full_route_or_hardware_verification':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False}
    save(ROOT/'terminal_gunnery_pilot_verification.json',proof)
    ledger_path = Path('translations/editorial_review_current_v1.json')
    ledger = read(ledger_path)
    before_ledger = deepcopy(ledger)
    assert ledger['records_editorially_completed']==1307 and ledger['records_with_source_and_prose_pass']==1395
    assert len(ledger['reviewed_but_incomplete_COMMON_IDs'])==88
    assert set(range(2058,2074))<=set(ledger['reviewed_but_incomplete_COMMON_IDs'])
    checkpoint = {'id':'V1375-original-gunnery-pilot-no-sinking-credit',
        'proof':str(ROOT/'terminal_gunnery_pilot_verification.json'),
        'proof_sha256':sha((ROOT/'terminal_gunnery_pilot_verification.json').read_bytes()),
        'completed_entries_added':0,'source_prose_entries_added':0,
        'finding':'Original gunnery exhausts enemy slot2 crew with26 Hull remaining;no sinking or gameplay withdrawal claimed.',
        'next_action':proof['next_action']}
    assert not any(c['id']==checkpoint['id'] for c in ledger['research_checkpoints'])
    ledger['research_checkpoints'].append(checkpoint)
    assert {k:v for k,v in ledger.items() if k!='research_checkpoints'}=={k:v for k,v in before_ledger.items() if k!='research_checkpoints'}
    save(ROOT/'ledger_before.json',before_ledger)
    save(ledger_path,ledger)
    save(ROOT/'ledger_update_receipt.json',{'only_research_checkpoint_added':True,
        'completed_entries_unchanged':1307,'source_prose_unchanged':1395,'reviewed_incomplete_unchanged':88,
        'all16_sinking_entries_still_pending':True,'ledger_after_sha256':sha(ledger_path.read_bytes())})
    print('Terminal gunnery pilot audited:all inputs/RAM/PNGs/donors exact;enemy crew0/Hull26;no sinking credit.',flush=True)


if __name__=='__main__':
    main()
