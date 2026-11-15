"""Use the registered V6584 opening snapshot and unchanged strict native guards."""
from pathlib import Path
from scripts.Al_Ferid_exact_native_context_v6520 import CurrentContext
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/current_V6584_native_v6593')
if __name__=='__main__':
    assert not ROOT.exists();v=read('work/analysis/editorial_handoff_verification_v6590/verified_handoff.json');r=read('work/analysis/lil_B211_release_v6585/registered_release_verification.json');terminal=read('work/analysis/lil_B211_runs_v6587/newgame_terminal.json')
    assert terminal['terminal'] and terminal['candidate_sha256']==v['candidate_sha256']==r['candidate_sha256']==sha(Path(v['candidate']).read_bytes())
    report=read(terminal['report']);assert sha(Path(terminal['report']).read_bytes())==terminal['report_sha256'];snap=next(s for s in report['read_only_capture_RAM_snapshots'] if s['frame']==4000)
    assert snap['read_only_export'] and sha(Path(snap['path']).read_bytes())==snap['sha256']
    previous=Path('work/analysis/current_V6541_native_v6549/current_capture_context.json');directory=read(previous)['directory_sha256'];ROOT.mkdir(parents=True);cp=ROOT/'current_capture_context.json'
    save(cp,dict(capture_report=terminal['report'],capture_report_sha256=terminal['report_sha256'],frame=4000,snapshot_sha256=snap['sha256'],directory_sha256=directory))
    inp=ROOT/'current_native_input.json';save(inp,dict(current_ROM=v['candidate'],current_ROM_sha256=v['candidate_sha256'],current_ARM9_sha256=r['ARM9_sha256'],current_COMMON_sha256=r['COMMON_sha256'],native_context_proof=str(cp)))
    ctx=CurrentContext(inp,'unused-no-historical-ROM',ROOT/'current_context');assert not ctx.machines
    save(ROOT/'verified_current_context_binding.json',dict(candidate=v['candidate'],candidate_sha256=v['candidate_sha256'],native_input=str(inp),native_input_sha256=sha(inp.read_bytes()),context_plan=str(ctx.proof_path),context_plan_sha256=sha(ctx.proof_path.read_bytes()),strict_helper='scripts/Al_Ferid_exact_native_context_v6520.py',strict_helper_sha256=sha(Path('scripts/Al_Ferid_exact_native_context_v6520.py').read_bytes()),current_actual_opening4000_and_all123264_staged_bytes_bound=True,current_ARM9_COMMON_directory_and_executed_instruction_guards_preserved=True,no_historical_initialized_RAM_overlay_or_battery_save=True,not_natural_B212_or_any_later_event_activation=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('V6584 own4000-frame capture bound to strict6520 ARM9/COMMON/directory/123264-byte/current-instruction guards;no new run or credit.')
