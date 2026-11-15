"""Bind own-current captain0,exact startup controls andthe complete strict native context."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/Rafael_B45_context_binding_v7868')
RUN=Path('work/analysis/Rafael_B45_context_runs_v7867/route0')
PRIOR=Path('work/analysis/papal_trade_startup_runs_v7663b/route0')
NATIVE=Path('work/analysis/current_V7857_Rafael_native_v7868')
if __name__=='__main__':
    assert not ROOT.exists() and not NATIVE.exists()
    plan,terminal,oldterminal=map(read,[RUN/'run_plan.json',RUN/'terminal.json',PRIOR/'terminal.json'])
    assert terminal['terminal'] and oldterminal['terminal'] and plan['route']==plan['expected_original_captain_ID']==0
    rp,op=Path(terminal['report']),Path(oldterminal['report']);report,old=map(read,[rp,op])
    assert sha(rp.read_bytes())==terminal['report_sha256'] and sha(op.read_bytes())==oldterminal['report_sha256']
    assert report['ROM_sha256']==plan['candidate_sha256']==terminal['candidate_sha256']
    for value in [report,old]:
        assert value['frames']==4001 and value['cold_boot'] and not value['savestate_loaded'] and not value['callback_errors']
        assert not value.get('battery_save_preloaded') and not any(v for k,v in value.items() if k.startswith('synthetic_'))
    assert report['scripted_input_schedule']==old['scripted_input_schedule'] and report['core_options']==old['core_options']
    image=NdsImage.open(plan['candidate']);previous=NdsImage.open(old['ROM'])
    for path in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/data/SC0.DK4','/data/EV0.DK4','/GRP/KANJI.FNT']:
        assert image.read_file(path)==previous.read_file(path)
    arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
    priorphotos={p['frame']:p for p in old['frames_captured']};pairs=[];actors=[]
    for p in report['frames_captured']:
        q=priorphotos[p['frame']]
        assert sha(Path(p['path']).read_bytes())==p['PNG_sha256'] and sha(Path(q['path']).read_bytes())==q['PNG_sha256']
        assert Image.open(p['path']).convert('RGB').tobytes()==Image.open(q['path']).convert('RGB').tobytes()
        pairs.append(dict(frame=p['frame'],current=p,prior=q,whole_RGB_equal=True))
    for value in [old,report]:
        snap=next(s for s in value['read_only_capture_RAM_snapshots'] if s['frame']==4000);raw=Path(snap['path']).read_bytes()
        assert snap['read_only_export'] and len(raw)==4194304 and sha(raw)==snap['sha256']
        cpu,get=get_machine(arm,raw);actor=get(0xCB184);assert get(0x7F244)==0
        actors.append(dict(captain=0,actor_root=actor,whole_actor_sha256=sha(bytes(cpu.mem_read(actor,0x1A04)))))
    assert actors[0]==actors[1]
    ROOT.mkdir(parents=True);NATIVE.mkdir(parents=True)
    snap=next(s for s in report['read_only_capture_RAM_snapshots'] if s['frame']==4000)
    proof=NATIVE/'own_registered_capture_context.json'
    save(proof,dict(capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes()),frame=4000,snapshot_sha256=snap['sha256'],
        directory_sha256='80d007e6b0f0a7eb60ec8d51d25211302371b763a3f49eea666044d49064cc3e',route=0,actual_original_captain_ID=0))
    inp=NATIVE/'current_native_input.json'
    save(inp,dict(current_ROM=plan['candidate'],current_ROM_sha256=plan['candidate_sha256'],
        current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),native_context_proof=str(proof),
        registered_profile=plan['profile'],expected_original_captain_ID=0,route_identity='Rafael',
        own_current_cold_boot_RAM_no_historical_ROM_oroverlay=True))
    ctx=RouteCurrentContext(inp,'unused-no-historical-ROM',NATIVE/'current_context');assert not ctx.machines
    sheet=Image.new('RGB',(512,410),'#263238');draw=ImageDraw.Draw(sheet)
    for i,frame in enumerate([2000,4000]):
        p=next(p for p in report['frames_captured'] if p['frame']==frame)
        draw.text((i*256+3,3),f'V7857 Rafael frame{frame}',fill='white');sheet.paste(Image.open(p['path']).convert('RGB'),(i*256,24))
    sp=ROOT/'own_Rafael_current_context.png';sheet.save(sp)
    save(ROOT/'own_Rafael_startup_andstrict_captain0_context.json',dict(candidate=plan['candidate'],candidate_sha256=plan['candidate_sha256'],
        capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes()),prior_report=str(op),prior_report_sha256=sha(op.read_bytes()),
        actual_frames=4001,whole_RGB_pairs=pairs,whole_RGB_pair_count=len(pairs),all_whole_RGB_actor_andcaptain_controls_equal=True,
        actor_captain_controls=actors,actual_original_captain_ID=0,current_native_input=str(inp),current_native_input_sha256=sha(inp.read_bytes()),
        native_plan=str(ctx.proof_path),native_plan_sha256=sha(ctx.proof_path.read_bytes()),
        all_strict2b6_COMMON_directory_and123264_payload_guards_pass=True,
        review_sheet=dict(path=str(sp),sha256=sha(sp.read_bytes())),visual_review_pending=True,
        initial_opening_not_optional_B45_activation_natural_location_orfullroute=True,new_credit=0,new_emulator_runs=1,
        evidence={str(p):sha(p.read_bytes()) for p in [RUN/'run_plan.json',RUN/'terminal.json',Path(__file__)]},full_goal_complete=False))
    print('Own V7857 Rafael context:',len(pairs),'whole-frame controls,wholeactors/captain0 andstrict123264 deployed bytes pass.B45 not activated;sheet view pending.')
