"""Bind both actual current New Games to strict original captain, payload and route contexts."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/papal_trade_route_native_v7626');RUN=Path('work/analysis/papal_trade_route_runs_v7625')
if __name__=='__main__':
    assert not ROOT.exists() and all(read(RUN/f'route{i}'/'terminal.json')['terminal'] for i in [0,1])
    ROOT.mkdir(parents=True);rows=[];photos=[]
    for route in [0,1]:
        terminal=read(RUN/f'route{route}'/'terminal.json');pp=Path(terminal['run_plan']);plan=read(pp);rp=Path(terminal['report']);report=read(rp);image=NdsImage.open(plan['candidate']);arm=image.read_file('/__arm9__.bin')
        assert sha(pp.read_bytes())==terminal['run_plan_sha256'] and sha(rp.read_bytes())==terminal['report_sha256'] and report['ROM_sha256']==terminal['candidate_sha256']==sha(Path(plan['candidate']).read_bytes())
        assert report['cold_boot'] and report['frames']==4001 and not report['savestate_loaded'] and not report.get('battery_save_preloaded') and not report['callback_errors'] and not report['hardware_device_verification'] and not report['goal_complete']
        assert report['scripted_input_schedule']==read(plan['inputs']) and sha(Path(plan['inputs']).read_bytes())==plan['inputs_sha256']
        snap=next(r for r in report['read_only_capture_RAM_snapshots'] if r['frame']==4000);raw=Path(snap['path']).read_bytes()
        assert snap['read_only_export'] and len(raw)==4194304 and sha(raw)==snap['sha256']
        cpu,get=get_machine(arm,raw);actual=get(0x7F244);assert actual==route==plan['expected_original_captain_ID'];actor_root=get(0xCB184)
        folder=ROOT/f'route{route}';folder.mkdir();context=folder/'own_registered_capture_context.json'
        save(context,dict(capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes()),frame=4000,snapshot_sha256=snap['sha256'],directory_sha256='80d007e6b0f0a7eb60ec8d51d25211302371b763a3f49eea666044d49064cc3e',route=route,actual_original_captain_ID=actual,actual_original_actor_root=actor_root))
        inp=folder/'current_native_input.json';save(inp,dict(current_ROM=plan['candidate'],current_ROM_sha256=plan['candidate_sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(image.read_file('/COMMON/MESFILE.DK4')),native_context_proof=str(context),registered_profile=plan['profile'],expected_original_captain_ID=route,route_identity=plan['route_identity'],own_current_cold_boot_RAM_no_historical_ROM_oroverlay=True))
        ctx=RouteCurrentContext(inp,'unused-no-historical-ROM',folder/'current_context');assert not ctx.machines
        rows.append(dict(route=route,route_identity=plan['route_identity'],actual_original_captain_ID=actual,input=str(inp),input_sha256=sha(inp.read_bytes()),context=str(context),context_sha256=sha(context.read_bytes()),native_context_plan=str(ctx.proof_path),native_context_plan_sha256=sha(ctx.proof_path.read_bytes()),all_strict2b6_COMMON_directory_deployed_payload_andactual_captain_guards_pass=True))
        for frame in [2000,4000]:
            photo=next(p for p in report['frames_captured'] if p['frame']==frame);assert sha(Path(photo['path']).read_bytes())==photo['PNG_sha256'];photos.append(dict(route=route,name=plan['route_identity'],frame=frame,capture=photo['path'],sha256=photo['PNG_sha256']))
    sheet=Image.new('RGB',(512,820),'#263238');draw=ImageDraw.Draw(sheet)
    for p in photos:
        x,y=p['route']*256,(0 if p['frame']==2000 else 410);draw.text((x+3,y+3),p['name']+' frame'+str(p['frame']),fill='white');sheet.paste(Image.open(p['capture']).convert('RGB'),(x,y+24))
    sp=ROOT/'actual_Rafael_Hodram_route_selection_andopening.png';sheet.save(sp)
    save(ROOT/'two_own_current_route_contexts_actual_captains0_1_strict2b6.json',dict(candidate=plan['candidate'],candidate_sha256=plan['candidate_sha256'],contexts=rows,actual_new_cold_boots=2,actual_frames_each=4001,actual_original_captain_IDs=[r['actual_original_captain_ID'] for r in rows],review_sheet=dict(path=str(sp),sha256=sha(sp.read_bytes())),photos=photos,visual_review_pending=True,existing_captain2_context_andall_native_guards_preserved=True,no_RAM_code_roster_role_funds_RNG_event_battery_or_savestate_forcing=True,actual_openings_not_optional_SC0B246_orSC1B237_activation=True,no_new_other_route_optional_dialogue_orfull_route_hardware_credit=True,source_is_own_registered_capture_not_historical_RAM_oroverlay=True,new_credit=0,evidence={str(p):sha(p.read_bytes()) for p in [Path('work/analysis/papal_trade_route_context_tools_v7626/source_locked_route_context_class.json'),Path('scripts/papal_trade_route_native_context_v7626.py'),Path(__file__)]},full_goal_complete=False))
    print('Own current Rafael/Hodram contexts bind actual captains0/1,strict2b6,COMMON,directory and123264 deployed bytes;two ordinary New Games,zero optional-scene credit.')
