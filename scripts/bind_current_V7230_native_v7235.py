"""Bind current native research to its own unmodified registered-ROM NewGame snapshot."""
from pathlib import Path
from scripts.square_shopkeeper_exact_native_context_v7020 import CurrentContext
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/current_V7230_native_v7235')
if __name__=='__main__':
    assert not ROOT.exists();release=read('work/analysis/lil_B225_release_v7231/registered_release_verification.json');tp=Path('work/analysis/lil_B225_runs_v7233/newgame_terminal.json');terminal=read(tp);reportpath=Path(terminal['report']);report=read(reportpath)
    assert terminal['terminal'] and report['ROM_sha256']==release['candidate_sha256']==sha(Path(release['candidate']).read_bytes()) and release['whole_ROM_reconstruction_byte_exact'] and sha(reportpath.read_bytes())==terminal['report_sha256']
    assert report['frames']==4001 and report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors'] and not any(v for k,v in report.items() if k.startswith('synthetic_'))
    snap=next(s for s in report['read_only_capture_RAM_snapshots'] if s['frame']==4000);assert snap['read_only_export'] and sha(Path(snap['path']).read_bytes())==snap['sha256']
    ROOT.mkdir(parents=True);context=ROOT/'own_registered_capture_context.json';save(context,dict(capture_report=str(reportpath),capture_report_sha256=sha(reportpath.read_bytes()),frame=4000,snapshot_sha256=snap['sha256'],directory_sha256='80d007e6b0f0a7eb60ec8d51d25211302371b763a3f49eea666044d49064cc3e'))
    inp=ROOT/'current_native_input.json';save(inp,dict(current_ROM=release['candidate'],current_ROM_sha256=release['candidate_sha256'],current_ARM9_sha256=release['ARM9_sha256'],current_COMMON_sha256=release['COMMON_sha256'],native_context_proof=str(context),registered_profile=release['profile'],own_current_cold_boot_RAM_no_historical_ROM_or_overlay=True))
    ctx=CurrentContext(inp,'unused-no-historical-ROM',ROOT/'current_context');assert not ctx.machines
    save(ROOT/'registered_current_native_input_binding.json',dict(input=str(inp),input_sha256=sha(inp.read_bytes()),candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],context=str(context),context_sha256=sha(context.read_bytes()),context_plan=str(ctx.proof_path),context_plan_sha256=sha(ctx.proof_path.read_bytes()),all123264_payload_bytes_COMMON_directory_actual_captain_and_exact2b6_guards_pass=True,source_is_own_registered_NewGame4000_not_initialized_scene_or_old_ROM_overlay=True,new_emulator_runs=0,new_credit=0,full_goal_complete=False));print('Current V7230 input bound to own registered NewGame4000 snapshot;strict2b6,payload,directory,captain checks pass.')
