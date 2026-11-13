"""Current cold boots;whole framebuffer equality and postload identity controls."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/surrender_advice_startup_v2677')
RUN=Path('work/analysis/surrender_advice_runs_v2676')
ROM=Path('out/all_routes_combined_v2674_candidate.nds')

if __name__=='__main__':
    assert not ROOT.exists()
    digest=sha(ROM.read_bytes());arm=NdsImage.open(ROM).read_file('/__arm9__.bin')
    runs=[];selected=[]
    for case,oldcase,oldcap in [('newgame','newgame','refit_spritsail_v2287_newgame_V2284'),('town','refit','refit_spritsail_v2287_refit_V2284')]:
        planpath=RUN/(case+'_plan.json');terminalpath=RUN/(case+'_terminal.json');plan,terminal=read(planpath),read(terminalpath)
        assert terminal['terminal'] and terminal['candidate_sha256']==plan['candidate_sha256']==digest
        rp=Path(terminal['report']);report=read(rp);assert sha(rp.read_bytes())==terminal['report_sha256']
        oldrp=Path('E:/Rota Nova translations/Generated/work/emulation_v193')/oldcap/'capture_report.json';old=read(oldrp)
        assert report['ROM_sha256']==digest and report['frames']==old['frames']==plan['frames']
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and not report['hardware_device_verification'] and not report['goal_complete']
        assert report['core_DLL_sha256']==old['core_DLL_sha256'] and report['core_options']==old['core_options']
        assert read(plan['inputs'])==report['scripted_input_schedule']==old['scripted_input_schedule']
        assert sha(Path(plan['inputs']).read_bytes())==plan['inputs_sha256'] and terminal['no_new_RAM_code_gameplay_fixture_or_observer']
        images={r['frame']:r for r in report['frames_captured']};previous={r['frame']:r for r in old['frames_captured']}
        assert images.keys()==previous.keys();paired=[]
        for frame,current in images.items():
            photo=Path(current['path']);other=Path(previous[frame]['path'])
            assert sha(photo.read_bytes())==current['PNG_sha256'] and sha(other.read_bytes())==previous[frame]['PNG_sha256']
            im=Image.open(photo).convert('RGB');prior=Image.open(other).convert('RGB')
            assert im.size==prior.size==(256,384) and im.tobytes()==prior.tobytes(),(case,frame)
            paired.append(dict(frame=frame,capture=str(photo),capture_sha256=current['PNG_sha256'],
                whole_current_framebuffer_equal_verified_V2284=True))
        snapshots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']}
        oldsnaps={r['frame']:r for r in old['read_only_capture_RAM_snapshots']}
        last=plan['frames'];snapshots[last]=report['read_only_RAM_snapshot'];oldsnaps[last]=old['read_only_RAM_snapshot']
        modelchecks=[];oldarm=NdsImage.open(old['ROM']).read_file('/__arm9__.bin')
        for frame in ([4000,4001] if case=='newgame' else [11900,13700,last]):
            s,t=snapshots[frame],oldsnaps[frame];raw,prior=Path(s['path']).read_bytes(),Path(t['path']).read_bytes()
            assert sha(raw)==s['sha256'] and sha(prior)==t['sha256'] and len(raw)==len(prior)==0x400000
            cpu,get=get_machine(arm,raw);oldcpu,og=get_machine(oldarm,prior)
            root,other=get(0xCB184),og(0xCB184)
            assert get(0x7F244)==og(0x7F244) and bytes(cpu.mem_read(root,0x1A04))==bytes(oldcpu.mem_read(other,0x1A04))
            modelchecks.append(dict(frame=frame,captain_ID=get(0x7F244),all_actor_models_equal_V2284=True,
                current_RAM_sha256=sha(raw),prior_RAM_sha256=sha(prior)))
        if case=='town':
            assert sha(Path(plan['source_donor']).read_bytes())==sha(Path(plan['disposable_donor']).read_bytes())==plan['source_donor_sha256']
            frames=[11900,13700,last]
        else:frames=[1600,2000,4000]
        selected.extend(dict(case=case,**next(p for p in paired if p['frame']==f)) for f in frames)
        runs.append(dict(case=case,frames=report['frames'],report=str(rp),report_sha256=sha(rp.read_bytes()),
            old_report=str(oldrp),old_report_sha256=sha(oldrp.read_bytes()),plan=str(planpath),plan_sha256=sha(planpath.read_bytes()),
            terminal=str(terminalpath),terminal_sha256=sha(terminalpath.read_bytes()),paired_whole_frames=paired,
            postload_actor_identity_controls=modelchecks,no_new_RAM_code_gameplay_fixture_or_observer=True,
            inherited_five_ship_test_battery_not_earned_progress=case=='town'))
    ROOT.mkdir(parents=True);sheet=Image.new('RGB',(768,820),'#263238');draw=ImageDraw.Draw(sheet)
    for i,s in enumerate(selected):
        x,y=i%3*256,i//3*410;draw.text((x+3,y+3),f'Current2674 {s["case"]} frame{s["frame"]}',fill='white');sheet.paste(Image.open(s['capture']).convert('RGB'),(x,y+24))
    sp=ROOT/'current_startup_and_town_review.png';sheet.save(sp)
    save(ROOT/'cold_boot_startup_town_verification.json',dict(candidate=str(ROM),candidate_sha256=digest,
        runs=runs,all_current_requested_and_final_framebuffers_equal_V2284=True,
        all_five_postload_actor_model_and_captain_checks_equal=True,source_and_disposable_town_donor_unchanged=True,
        original_NewGame_story_and_town_Refit_cold_boots=True,no_current2029_or_other_aftermath_event_activation_claim=True,
        no_new_RAM_code_gameplay_fixture_observer_or_savestate=True,targeted_headless_not_full_route_or_hardware_verification=True,
        review_sheet=str(sp),review_sheet_sha256=sha(sp.read_bytes()),visual_review_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Current2674 NewGame andtown cold boots pass:all requested/final frames equal2284;five actor/captain controls anddonor hashes match. Visual review pending.')
