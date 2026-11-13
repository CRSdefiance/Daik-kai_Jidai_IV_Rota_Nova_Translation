"""Preserve partial evidence after the confirmed navigation-stream timeout."""
from pathlib import Path
from scripts.verify_stronger_fleet_survey_v1476 import observe
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/early_mode_timeout_v1477')

if __name__=='__main__':
    assert not ROOT.exists()
    run=Path('work/analysis/stronger_fleet_early_modes_v1475')
    cap=Path('E:/Rota Nova translations/Generated/work/emulation_v193/stronger_fleet_early_modes_v1475_1456')
    log=Path('work/analysis/ship_loss_surrender_release_v1455/stronger_fleet_early_modes.log')
    assert 'TimeoutError: No appended navigation command for20 minutes;run not restarted' in log.read_text(encoding='utf-8')
    assert not (cap/'capture_report.json').exists() and not (run/'terminal_preservation.json').exists()
    plan=read(run/'run_plan.json')
    assert sha(Path(plan['source_donor']).read_bytes())==sha(Path(plan['disposable_donor']).read_bytes())==plan['source_donor_sha256']
    arm=NdsImage.open(plan['candidate']).read_file('/__arm9__.bin')
    assert sha(Path(plan['candidate']).read_bytes())==plan['candidate_sha256']
    files=[{'path':str(p),'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())} for p in sorted(cap.iterdir()) if p.is_file()]
    observations=[]
    for frame in [4830,4900,4950,5000,5100,5120,5140,5160]:
        p=cap/f'frame_{frame:06}_arm9_ram.bin'
        observations.append(observe(arm,{'frame':frame,'path':str(p)}))
    assert all(r['mode']==[0,0,0] for r in observations)
    ROOT.mkdir(parents=True)
    save(ROOT/'partial_timeout_evidence.json',{'candidate':plan['candidate'],'candidate_sha256':plan['candidate_sha256'],
        'exit_code_observed':1,'live_tool_session_polled':73888,'process_missing_confirmed':True,
        'terminal_report_missing_no_complete_execution_or_input_audit_claim':True,
        'timeout_log':str(log),'timeout_log_sha256':sha(log.read_bytes()),'primary_partial_files':files,
        'native_pause_observations':observations,'source_and_disposable_donors_unchanged':True,
        'source_donor_sha256':plan['source_donor_sha256'],'no_restart_due_to_observation_timeout':True,
        'no_new_combat_event_or_editorial_completion_credit':True,
        'producer_sha256':sha(Path(__file__).read_bytes()),'full_goal_complete':False})
    print('Confirmed exit1 after20-minute navigation timeout;partial files preserved,donors unchanged,no terminal-run or event credit.')
