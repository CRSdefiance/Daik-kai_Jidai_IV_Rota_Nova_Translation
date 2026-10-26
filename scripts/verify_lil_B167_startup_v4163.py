"""Compare actual current cold boots with V4110, with honest coverage scope."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/lil_B167_startup_v4163')
RUN=Path('work/analysis/lil_B167_runs_v4162')
ROM=Path('out/all_routes_combined_v4160_candidate.nds')
if __name__=='__main__':
    assert all((RUN/(case+'_terminal.json')).exists() and read(RUN/(case+'_terminal.json'))['terminal'] for case in ['newgame','town']),'Both actual capture jobs must be terminal before comparison'
    assert not ROOT.exists();digest=sha(ROM.read_bytes());image=NdsImage.open(ROM);arm=image.read_file('/__arm9__.bin')
    prior=NdsImage.open('out/all_routes_combined_v4110_candidate.nds');assert arm==prior.read_file('/__arm9__.bin')
    runs=[];selected=[];total=0
    for case in ['newgame','town']:
        pp,tp=RUN/(case+'_plan.json'),RUN/(case+'_terminal.json');plan,terminal=read(pp),read(tp)
        assert terminal['terminal'] and terminal['candidate_sha256']==plan['candidate_sha256']==digest
        rp=Path(terminal['report']);report=read(rp);assert sha(rp.read_bytes())==terminal['report_sha256']
        oldtp=Path('work/analysis/lil_B166_runs_v4112')/(case+'_terminal.json')
        oldterminal=read(oldtp);oldrp=Path(oldterminal['report']);old=read(oldrp)
        assert sha(oldrp.read_bytes())==oldterminal['report_sha256']
        assert report['ROM_sha256']==digest and report['frames']==old['frames']==plan['frames']
        assert report['cold_boot'] and old['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not report['hardware_device_verification'] and not report['goal_complete']
        assert report['core_DLL_sha256']==old['core_DLL_sha256'] and report['core_options']==old['core_options']
        assert read(plan['inputs'])==report['scripted_input_schedule']==old['scripted_input_schedule']
        assert sha(Path(plan['inputs']).read_bytes())==plan['inputs_sha256']
        assert terminal['no_new_RAM_code_gameplay_fixture_or_observer']
        now={r['frame']:r for r in report['frames_captured']};then={r['frame']:r for r in old['frames_captured']};assert now.keys()==then.keys()
        paired=[]
        for frame,current in now.items():
            a,b=Path(current['path']),Path(then[frame]['path'])
            assert sha(a.read_bytes())==current['PNG_sha256'] and sha(b.read_bytes())==then[frame]['PNG_sha256']
            x,y=Image.open(a).convert('RGB'),Image.open(b).convert('RGB');assert x.size==y.size==(256,384) and x.tobytes()==y.tobytes(),(case,frame)
            paired.append(dict(frame=frame,capture=str(a),capture_sha256=current['PNG_sha256'],whole_framebuffer_equal_V4110=True));total+=1
        snapshots={r['frame']:r for r in report['read_only_capture_RAM_snapshots']};oldsnaps={r['frame']:r for r in old['read_only_capture_RAM_snapshots']}
        last=plan['frames'];snapshots[last]=report['read_only_RAM_snapshot'];oldsnaps[last]=old['read_only_RAM_snapshot'];models=[]
        for frame in ([4000,4001] if case=='newgame' else [11900,13700,last]):
            a,b=snapshots[frame],oldsnaps[frame];raw,oldraw=Path(a['path']).read_bytes(),Path(b['path']).read_bytes()
            assert len(raw)==len(oldraw)==0x400000 and sha(raw)==a['sha256'] and sha(oldraw)==b['sha256']
            cpu,get=get_machine(arm,raw);oldcpu,og=get_machine(arm,oldraw);root,oldroot=get(0xCB184),og(0xCB184)
            assert get(0x7F244)==og(0x7F244) and bytes(cpu.mem_read(root,0x1A04))==bytes(oldcpu.mem_read(oldroot,0x1A04))
            check=dict(frame=frame,captain_ID=get(0x7F244),whole_actor_models_equal=True,current_RAM_sha256=sha(raw),control_RAM_sha256=sha(oldraw))
            if case=='newgame':
                assert check['captain_ID']==2
                block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[22]
                assert block==IlnkContainer.parse(prior.read_file('/data/SC2.DK4')).blocks[22]
                at=raw.find(block);assert at>=0 and oldraw.find(block)==at
                check.update(Lil_opening_B22_resident_payload_exact_current_ROM=True,payload_address=0x02000000+at)
            models.append(check)
        if case=='town':assert sha(Path(plan['source_donor']).read_bytes())==sha(Path(plan['disposable_donor']).read_bytes())==plan['source_donor_sha256']
        wanted=[2000,2400,4000] if case=='newgame' else [11900,13700,last]
        selected.extend(dict(case=case,**next(p for p in paired if p['frame']==f)) for f in wanted)
        runs.append(dict(case=case,frames=report['frames'],report=str(rp),report_sha256=sha(rp.read_bytes()),old_report=str(oldrp),old_report_sha256=sha(oldrp.read_bytes()),
            plan=str(pp),plan_sha256=sha(pp.read_bytes()),terminal=str(tp),terminal_sha256=sha(tp.read_bytes()),
            paired_whole_frames=paired,postload_actor_identity_controls=models,inherited_five_ship_test_battery_not_earned_progress=case=='town'))
    ROOT.mkdir(parents=True);sheet=Image.new('RGB',(768,820),'#263238');draw=ImageDraw.Draw(sheet)
    for i,s in enumerate(selected):
        x,y=i%3*256,i//3*410;draw.text((x+3,y+3),f'Current4160 {s["case"]} frame{s["frame"]}',fill='white');sheet.paste(Image.open(s['capture']).convert('RGB'),(x,y+24))
    sp=ROOT/'current_Lil_startup_and_town_review.png';sheet.save(sp)
    save(ROOT/'cold_boot_Lil_startup_town_verification.json',dict(candidate=str(ROM),candidate_sha256=digest,runs=runs,
        all_current_requested_and_final_framebuffers_equal_V4110=True,paired_frame_count=total,
        all_five_postload_actor_model_and_captain_checks_equal=True,current_Lil_captain2_and_B22_payload_verified=True,
        source_and_disposable_town_donor_unchanged=True,original_Lil_NewGame_and_town_Refit_cold_boots=True,
        no_new_RAM_code_gameplay_fixture_observer_or_savestate=True,actual_selected_B167_IDs=[],
        targeted_headless_not_full_route_or_hardware_verification=True,review_sheet=str(sp),review_sheet_sha256=sha(sp.read_bytes()),visual_review_pending=True,
        producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print(f'Current4160 Lil NewGame andtown cold boots pass:{total}whole-frame pairs matchV4110;five actor/captain controls anddonor hashes pass. Visual review pending.')
