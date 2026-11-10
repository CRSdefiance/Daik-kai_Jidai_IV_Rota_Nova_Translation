"""Bind a strict Maria context to its own current4000 snapshot andactual captain3."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.maria_unlocked_current_context_v7680 import MariaUnlockedCurrentContext as MariaCurrentContext
from scripts.maria_existing_unlock_contract_v7680 import validate_capture
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_native_v7681')
RUN=Path('work/analysis/maria_B207_route_run_v7680')
if __name__=='__main__':
    assert not ROOT.exists();t=read(RUN/'terminal.json');pp=Path(t['run_plan']);rp=Path(t['report']);p,r=map(read,[pp,rp])
    assert t['terminal'] and sha(pp.read_bytes())==t['run_plan_sha256'] and sha(rp.read_bytes())==t['report_sha256']
    image=NdsImage.open(p['candidate']);arm=image.read_file('/__arm9__.bin');assert sha(Path(p['candidate']).read_bytes())==p['candidate_sha256']==r['ROM_sha256'] and r['scripted_input_schedule']==read(p['inputs'])
    assert r['frames']==4001;validate_capture(r)
    snap=next(s for s in r['read_only_capture_RAM_snapshots'] if s['frame']==4000);raw=Path(snap['path']).read_bytes();assert snap['read_only_export'] and len(raw)==4194304 and sha(raw)==snap['sha256']
    cpu,get=get_machine(arm,raw);captain=get(0x7F244);root=get(0xCB184);assert captain==3
    ROOT.mkdir(parents=True);context=ROOT/'own_registered_capture_context.json';save(context,dict(capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes()),frame=4000,snapshot_sha256=snap['sha256'],directory_sha256='80d007e6b0f0a7eb60ec8d51d25211302371b763a3f49eea666044d49064cc3e',route=3,actual_original_captain_ID=captain,actual_original_actor_root=root))
    inp=ROOT/'current_native_input.json';save(inp,dict(current_ROM=p['candidate'],current_ROM_sha256=p['candidate_sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),native_context_proof=str(context),registered_profile=p['profile'],expected_original_captain_ID=3,route_identity='Maria',own_current_cold_boot_RAM_no_historical_ROM_oroverlay=True))
    ctx=MariaCurrentContext(inp,'unused-no-historical-ROM',ROOT/'current_context');assert not ctx.machines
    sheet=Image.new('RGB',(768,410),'#263238');draw=ImageDraw.Draw(sheet)
    for i,frame in enumerate([3200,3400,4000]):
        photo=next(q for q in r['frames_captured'] if q['frame']==frame);assert sha(Path(photo['path']).read_bytes())==photo['PNG_sha256'];draw.text((i*256+3,3),'Maria ownV7660 frame'+str(frame),fill='white');sheet.paste(Image.open(photo['path']).convert('RGB'),(i*256,24))
    sp=ROOT/'actual_Maria_selection_confirmation_opening.png';sheet.save(sp)
    save(ROOT/'own_current_Maria_captain3_strict2b6_context_binding.json',dict(candidate=p['candidate'],candidate_sha256=p['candidate_sha256'],input=str(inp),input_sha256=sha(inp.read_bytes()),context=str(context),context_sha256=sha(context.read_bytes()),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),actual_original_captain_ID=3,all_strict2b6_COMMON_directory123264_deployed_bytes_actor_andownership_guards_pass=True,source_is_own_registered_NewGame4000_not_historical_RAM_orfixture=True,review_sheet=dict(path=str(sp),sha256=sha(sp.read_bytes())),visual_review_pending=True,ordinary_opening_not_optional_B207_activation_orfullroute_credit=True,new_credit=0,existing_system_only_unlock_fixture=True,earned_unlock_verified=False,evidence={str(q):sha(q.read_bytes()) for q in [RUN/'terminal.json',RUN/'run_plan.json',Path('scripts/maria_unlocked_current_context_v7680.py'),Path('scripts/maria_existing_unlock_contract_v7680.py'),Path(__file__)]},full_goal_complete=False))
    print('Own V7660 Maria snapshot binds actualcaptain3,strict2b6,COMMON,directory andall123264 deployed bytes. No older RAM orroute defaults;B207 notactivated.')
