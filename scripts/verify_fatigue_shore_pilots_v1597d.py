"""Audit both terminal shore pilots;no recovery or event-selection credit."""
import json,struct
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts import native_fatigue_shore_fixture_v1587d as old_fixture
from scripts import native_fatigue_shore_fixture_v1597b as new_fixture
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/fatigue_shore_pilots_verified_v1597d')
CAP=Path('E:/Rota Nova translations/Generated/work/emulation_v193')

def audit(label,version,module,terminal_frame,fixture_frames):
    run=Path('work/analysis')/label;cap=CAP/(label+'_'+str(version));report_path=cap/'capture_report.json'
    report,plan,terminal=[read(p) for p in [report_path,run/'run_plan.json',run/'terminal_preservation.json']]
    digest=sha(module.ROM.read_bytes());assert report['ROM_sha256']==plan['candidate_sha256']==digest
    assert report['frames']==terminal_frame and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert not report['goal_complete'] and not report['hardware_device_verification']
    assert terminal['source_and_disposable_donors_unchanged']
    assert sha(Path(plan['source_donor']).read_bytes())==sha(Path(plan['disposable_donor']).read_bytes())==terminal['source_donor_sha256']
    assert sha((run/'navigation.jsonl').read_bytes())==terminal['navigation_sha256']
    assert sha(Path('scripts/headless_desmume_v193.py').read_bytes())==plan['harness_sha256']
    assert not any(v for k,v in report.items() if k.startswith('synthetic_') and k!='synthetic_battle_recovery_proximity_fixtures')
    snapshots={}
    for row in report['read_only_capture_RAM_snapshots']+report['read_only_pause_RAM_snapshots']:
        body=Path(row['path']).read_bytes();assert len(body)==row['bytes']==0x400000 and sha(body)==row['sha256']
        if row['frame'] in snapshots:assert snapshots[row['frame']]['sha256']==row['sha256']
        snapshots[row['frame']]=row
    for row in report['frames_captured']:assert sha(Path(row['path']).read_bytes())==row['PNG_sha256']
    commands=[json.loads(line) for line in (run/'navigation.jsonl').read_text(encoding='utf-8').splitlines()]
    journal=read(cap/'navigation_command_journal.json')['commands_received'];assert commands==[r['command'] for r in journal]
    assert journal[-1]['frame']==terminal_frame and journal[-1]['command']=={'stop':True}
    schedule=read(run/'original_departure_inputs.json');expected=[];arm=NdsImage.open(module.ROM).read_file('/__arm9__.bin')
    for item in journal:
        assert item['validation_passed'];c=item['command']
        if c.get('stop'):continue
        assert c['until'] in snapshots and c['until']>item['frame']
        if 'battle_fixture' in c:
            raw=Path(snapshots[item['frame']]['path']).read_bytes();after,proof=module.apply_fixture(arm,raw,c['battle_fixture'])
            assert len(proof['owned_bytes'])==40 and all(p['address'] in proof['owned_bytes'] for p in proof['changes'])
            assert proof['all_other4MiB_bytes_including_fatigue_RNG_actors_roles_health_and_event_choices_exact']
            expected.append({**proof,'frame':item['frame']})
        if c.get('buttons') or c.get('touch') is not None:
            event={'start':item['frame']+1,'duration':c.get('duration',12),'buttons':c.get('buttons',[])}
            if c.get('touch') is not None:event['touch']=c['touch']
            schedule.append(event)
    assert schedule==report['scripted_input_schedule']
    assert [p['frame'] for p in expected]==fixture_frames
    assert json.loads(json.dumps(expected))==report['synthetic_battle_recovery_proximity_fixtures']
    return {'candidate':str(module.ROM),'candidate_sha256':digest,'terminal_report':str(report_path),'terminal_report_sha256':sha(report_path.read_bytes()),
        'terminal_frame':terminal_frame,'fixture_frames':fixture_frames,'all40_coordinate_byte_changes_and_other4MiB_bytes_audited':True,
        'all_inputs_snapshots_PNG_hashes_and_unchanged_source_disposable_saves_audited':True,'fixtures':expected,
        'only_location_fixtures_no_fatigue_actor_RNG_state_event_or_outcome_forcing':True,'no_309_recovery_or_editorial_completion_credit':True,
        'source_query_does_not_prove_actual_event_reachability':True,'full_goal_complete':False}

if __name__=='__main__':
    assert not ROOT.exists()
    records=[audit('fatigue_shore_live_v1587e',1578,old_fixture,5800,[4800]),
        audit('fatigue_recovery_live_v1597c',1594,new_fixture,7000,[5000,5650])]
    ROOT.mkdir(parents=True);save(ROOT/'both_terminal_shore_pilots_audited.json',{'pilots':records,
        'observations':['First pilot drifted30,22 before Search and showed another nothing-found/+3 sequence.',
            'The second pilot legally moved only positions twice before its first expedition;it selected original beast attacks and crew-loss results. Recovery309 is not observed in its sampled holds.',
            'Original fleet virtual point getter is2C1C4,out-pointer then fleet,and reads cached fields34/38.36A24 is a mobile-position getter;the exploratory call with a fleet was the wrong ABI and its output is not evidence.',
            'Offline native region/shore classification is source research only;reconcile it with the actual cached point and Search caller before predicting a hot-spring outcome. No game or formatter fix is inferred from this testing-context gap.'],
        'source_prose_reviews_added':0,'completed_entries_added':0,'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Both shore pilots audited through5800/7000:40-byte locations atdeclared frames only,all4MiB/inputs/RAM/PNG/donors pass;recovery309 remains open.')
