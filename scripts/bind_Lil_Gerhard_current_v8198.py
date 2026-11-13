"""Bind exact own-current Lil captain2 snapshot without a historical RAM overlay."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.Lil_current_route_context_v8198 import RouteCurrentContext
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Lil_Gerhard_current_binding_v8198')
RUN=Path('work/analysis/Lil_Gerhard_context_runs_v8197/route2')
NATIVE=Path('work/analysis/current_V8172_Lil_native_v8198')
if __name__=='__main__':
    assert not ROOT.exists() and not NATIVE.exists()
    plan,terminal=map(read,[RUN/'run_plan.json',RUN/'terminal.json']);assert terminal['terminal'] and plan['route']==plan['expected_original_captain_ID']==2
    rp=Path(terminal['report']);report=read(rp)
    assert sha(rp.read_bytes())==terminal['report_sha256'] and report['ROM_sha256']==plan['candidate_sha256']==terminal['candidate_sha256']
    assert report['frames']==4001 and report['cold_boot'] and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors']
    assert not any(v for k,v in report.items() if k.startswith('synthetic_'))
    assert report['scripted_input_schedule']==read(plan['inputs']) and sha(Path(plan['inputs']).read_bytes())==plan['inputs_sha256']
    image=NdsImage.open(plan['candidate']);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
    release=read('work/analysis/Rafael_B50_release_v8173/registered_release_verification.json')
    assert sha(Path(plan['candidate']).read_bytes())==release['candidate_sha256']==plan['candidate_sha256'] and plan['profile']=='all-routes-unified-v8172'
    assert sha(arm)==release['ARM9_sha256'] and sha(common)==release['COMMON_sha256']
    snap=next(s for s in report['read_only_capture_RAM_snapshots'] if s['frame']==4000);raw=Path(snap['path']).read_bytes()
    assert snap['read_only_export'] and len(raw)==4194304 and sha(raw)==snap['sha256']
    cpu,get=get_machine(arm,raw);actor=get(0xCB184);assert get(0x7F244)==2
    photos={p['frame']:p for p in report['frames_captured']};assert len(photos)==6
    for p in photos.values():assert sha(Path(p['path']).read_bytes())==p['PNG_sha256']
    ROOT.mkdir(parents=True);NATIVE.mkdir(parents=True)
    proof=NATIVE/'own_registered_capture_context.json'
    save(proof,dict(capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes()),frame=4000,snapshot_sha256=snap['sha256'],
        directory_sha256='80d007e6b0f0a7eb60ec8d51d25211302371b763a3f49eea666044d49064cc3e',route=2,actual_original_captain_ID=2))
    inp=NATIVE/'current_native_input.json'
    save(inp,dict(current_ROM=plan['candidate'],current_ROM_sha256=plan['candidate_sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),
        native_context_proof=str(proof),registered_profile=plan['profile'],expected_original_captain_ID=2,route_identity='Lil',own_current_cold_boot_RAM_no_historical_ROM_oroverlay=True))
    ctx=RouteCurrentContext(inp,'unused-no-historical-ROM',NATIVE/'current_context');assert not ctx.machines
    sheet=Image.new('RGB',(512,410),'#263238');draw=ImageDraw.Draw(sheet)
    for i,frame in enumerate([2000,4000]):
        draw.text((i*256+3,3),f'V8172 Lil frame{frame}',fill='white');sheet.paste(Image.open(photos[frame]['path']).convert('RGB'),(i*256,24))
    path=ROOT/'own_Lil_current_context.png';sheet.save(path)
    save(ROOT/'own_Lil_startup_andstrict_captain2_context.json',dict(candidate=plan['candidate'],candidate_sha256=plan['candidate_sha256'],capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes()),
        actual_frames=4001,whole_actor_sha256=sha(bytes(cpu.mem_read(actor,0x1A04))),actual_original_captain_ID=2,current_native_input=str(inp),current_native_input_sha256=sha(inp.read_bytes()),
        native_plan=str(ctx.proof_path),native_plan_sha256=sha(ctx.proof_path.read_bytes()),all_strict2b6_COMMON_directory_and123264_payload_guards_pass=True,
        ordinary_NewGame_only_not_optional_Gerhard_Stockholm_Hamburg_activation=True,no_historical_snapshot_orinitialized_RAM_overlay=True,
        review_sheet=dict(path=str(path),sha256=sha(path.read_bytes())),visual_review_pending=True,
        no_scene_orfullroute_hardware_ornew_prose_credit=True,new_credit=0,new_emulator_runs=1,
        evidence={str(p):sha(p.read_bytes()) for p in [RUN/'run_plan.json',RUN/'terminal.json',Path(__file__)]},full_goal_complete=False))
    print('Own V8172 Lil captain2 andstrict current123264-byte context pass;startup sheet view pending.No optional scene activated.')
