"""Bind strict current native contexts to this registered ROM's own three NewGame snapshots."""
from pathlib import Path
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.square_shopkeeper_exact_native_context_v7020 import CurrentContext
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/current_V7660_native_v7665')
STARTUP=Path('work/analysis/papal_trade_startup_verification_v7664c/own_ROM_three_NewGames_town_exact_prior_comparisons.json')
if __name__=='__main__':
    assert not ROOT.exists();s=read(STARTUP);release=read('work/analysis/papal_trade_release_v7661/registered_release_verification.json')
    assert s['candidate_sha256']==release['candidate_sha256'] and s['all_three_captains0_1_2_actual_NewGames_verified'] and release['whole_clean_input_ROM_reconstruction_byte_exact']
    image=NdsImage.open(release['candidate']);arm=image.read_file('/__arm9__.bin');ROOT.mkdir(parents=True);contexts=[]
    for route in [0,1,2]:
        run=next(r for r in s['runs'] if r['case']==f'route{route}');rp=Path(run['capture_report']);report=read(rp)
        assert sha(rp.read_bytes())==run['capture_report_sha256'] and report['ROM_sha256']==release['candidate_sha256']==sha(Path(release['candidate']).read_bytes())
        assert report['frames']==4001 and report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors']
        snap=next(r for r in report['read_only_capture_RAM_snapshots'] if r['frame']==4000);assert snap['read_only_export'] and sha(Path(snap['path']).read_bytes())==snap['sha256']
        folder=ROOT if route==2 else ROOT/f'route{route}'
        folder.mkdir(parents=True,exist_ok=True);context=folder/'own_registered_capture_context.json'
        save(context,dict(capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes()),frame=4000,snapshot_sha256=snap['sha256'],directory_sha256='80d007e6b0f0a7eb60ec8d51d25211302371b763a3f49eea666044d49064cc3e',route=route))
        inp=folder/'current_native_input.json'
        save(inp,dict(current_ROM=release['candidate'],current_ROM_sha256=release['candidate_sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),native_context_proof=str(context),registered_profile=release['profile'],expected_original_captain_ID=route,route_identity={0:'Rafael',1:'Hodram',2:'Lil'}[route],own_current_cold_boot_RAM_no_historical_ROM_or_overlay=True))
        cls=CurrentContext if route==2 else RouteCurrentContext;ctx=cls(inp,'unused-no-historical-ROM',folder/'current_context');assert not ctx.machines
        contexts.append(dict(route=route,route_identity={0:'Rafael',1:'Hodram',2:'Lil'}[route],input=str(inp),input_sha256=sha(inp.read_bytes()),context=str(context),context_sha256=sha(context.read_bytes()),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),all_strict2b6_COMMON_directory123264_payload_andactual_captain_guards_pass=True))
    save(ROOT/'registered_current_three_native_input_bindings.json',dict(candidate=release['candidate'],candidate_sha256=release['candidate_sha256'],contexts=contexts,default_Lil_input=str(ROOT/'current_native_input.json'),actual_original_captain_IDs=[0,1,2],all_inputs_from_own_registered_ROM_NewGame4000_not_initialized_fixture_orold_RAM=True,no_native_guard_orhistorical_context_weakening=True,new_emulator_runs=0,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [STARTUP,Path('scripts/square_shopkeeper_exact_native_context_v7020.py'),Path('scripts/papal_trade_route_native_context_v7626.py'),Path(__file__)]},full_goal_complete=False))
    print('V7660 own-current native inputs:actualcaptains0/1/2,strict2b6/COMMON/directory123264 bytes pass. DefaultLil input andseparateRafael/Hodram inputs retained;no overlays.')
