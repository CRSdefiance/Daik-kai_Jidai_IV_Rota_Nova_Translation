"""Bind future B206 English checks to the registered ROM's own actual opening capture."""
from pathlib import Path
from scripts.source_locked_derivation_v5118 import derive
from scripts.verify_village_wrap_v608 import read,save
from dk4tool.patch.grand_race_menu_release import sha
ROOT=Path('work/analysis/current_V6270_native_v6279')
if __name__=='__main__':
    assert not ROOT.exists();r=read('work/analysis/shady_man_label_release_v6271/registered_release_verification.json');terminal=read('work/analysis/shady_man_runs_v6272/newgame_terminal.json')
    assert terminal['terminal'] and terminal['candidate_sha256']==r['candidate_sha256']==sha(Path(r['candidate']).read_bytes())
    report=read(terminal['report']);assert sha(Path(terminal['report']).read_bytes())==terminal['report_sha256'];snap=next(s for s in report['read_only_capture_RAM_snapshots'] if s['frame']==4000)
    assert snap['read_only_export'] and sha(Path(snap['path']).read_bytes())==snap['sha256']
    derivation=derive('scripts/current_build_native_context_v6261.py','scripts/current_build_native_context_v6261b.py',{
      'snapshot_is_complete_B206_content_fixture_not_natural_event_activation':'snapshot_is_exact_current_ROM_capture_not_natural_event_activation',
    })
    from scripts.current_build_native_context_v6261b import CurrentContext
    directory=read('work/analysis/current_V6220_native_v6228/current_capture_context.json')['directory_sha256'];ROOT.mkdir(parents=True);cp=ROOT/'current_capture_context.json';save(cp,dict(capture_report=terminal['report'],capture_report_sha256=terminal['report_sha256'],frame=4000,snapshot_sha256=snap['sha256'],directory_sha256=directory))
    inp=ROOT/'current_native_input.json';save(inp,dict(current_ROM=r['candidate'],current_ROM_sha256=r['candidate_sha256'],current_ARM9_sha256=r['ARM9_sha256'],current_COMMON_sha256=r['COMMON_sha256'],native_context_proof=str(cp)))
    ctx=CurrentContext(inp,'unused-no-historical-ROM',ROOT/'current_context');assert not ctx.machines
    save(ROOT/'verified_current_context_binding.json',dict(candidate=r['candidate'],candidate_sha256=r['candidate_sha256'],native_input=str(inp),native_input_sha256=sha(inp.read_bytes()),context_plan=str(ctx.proof_path),context_plan_sha256=sha(ctx.proof_path.read_bytes()),helper_derivation=derivation,metadata_only_scope_neutral_successor_from_strict6261=True,current_actual_opening4000_and_all123264_staged_bytes_bound=True,current_ARM9_COMMON_directory_and_executed_instruction_guards_preserved=True,no_historical_initialized_RAM_overlay_or_battery_save=True,not_natural_B206_or_any_later_event_activation=True,new_ROMs=0,new_emulator_runs=0,new_review_credit=0,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False));print('V6270 own opening4000 snapshot bound with exact new ARM9/COMMON/directory/payload guards.6261b changes only scope metadata;no new run or credit.')
