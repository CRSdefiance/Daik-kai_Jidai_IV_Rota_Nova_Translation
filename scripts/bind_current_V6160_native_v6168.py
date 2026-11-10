"""Bind future source research to V6160's own cold-boot snapshot without a new run."""
from pathlib import Path
from scripts.current_build_native_context_v6097 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/current_V6160_native_v6168')
if __name__=='__main__':
    assert not ROOT.exists();v=read('work/analysis/editorial_handoff_verification_v6166/verified_handoff.json');r=read('work/analysis/lil_B204_release_v6161/registered_release_verification.json');terminal=read('work/analysis/lil_B204_runs_v6162/newgame_terminal.json')
    assert terminal['terminal'] and terminal['candidate_sha256']==v['candidate_sha256']==r['candidate_sha256']==sha(Path(v['candidate']).read_bytes())
    report=read(terminal['report']);assert sha(Path(terminal['report']).read_bytes())==terminal['report_sha256'];snap=next(s for s in report['read_only_capture_RAM_snapshots'] if s['frame']==4000)
    assert snap['read_only_export'] and sha(Path(snap['path']).read_bytes())==snap['sha256']
    directory=read('work/analysis/shachihoko_native_v6098/target_capture_context.json')['directory_sha256'];ROOT.mkdir(parents=True);cp=ROOT/'current_capture_context.json'
    save(cp,dict(capture_report=terminal['report'],capture_report_sha256=terminal['report_sha256'],frame=4000,snapshot_sha256=snap['sha256'],directory_sha256=directory))
    inp=ROOT/'current_native_input.json';save(inp,dict(current_ROM=v['candidate'],current_ROM_sha256=v['candidate_sha256'],current_ARM9_sha256=r['ARM9_sha256'],current_COMMON_sha256=r['COMMON_sha256'],native_context_proof=str(cp)))
    ctx=CurrentContext(inp,'unused-no-historical-ROM',ROOT/'current_context');assert not ctx.machines
    save(ROOT/'verified_current_context_binding.json',dict(candidate=v['candidate'],candidate_sha256=v['candidate_sha256'],native_input=str(inp),native_input_sha256=sha(inp.read_bytes()),context_plan=str(ctx.proof_path),context_plan_sha256=sha(ctx.proof_path.read_bytes()),current_actual_opening4000_snapshot_and_all123264_staged_bytes_bound=True,current_ARM9_COMMON_directory_and_executed_instruction_guards_preserved=True,no_historical_initialized_RAM_overlay_or_battery_save=True,not_B205_or_any_later_event_activation=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('V6160 own4000-frame snapshot and exact123264-byte current native context bound for next source review;no new run or credit.')
