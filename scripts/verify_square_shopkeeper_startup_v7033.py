"""Reuse the byte-identical target NewGame; compare a fresh registered town cold boot."""
from pathlib import Path
from PIL import Image,ImageDraw
from ndspy.code import MainCodeFile
from dk4tool.rom.nds import NdsImage
from dk4tool.formats.ilnk import IlnkContainer
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save

ROOT=Path('work/analysis/square_shopkeeper_startup_v7033')
ROM=Path('out/all_routes_combined_v7029_candidate.nds')
RELEASE=Path('work/analysis/square_shopkeeper_release_v7030/registered_release_verification.json')
if __name__=='__main__':
    assert not ROOT.exists();release=read(RELEASE);digest=sha(ROM.read_bytes())
    assert digest==release['candidate_sha256'] and release['whole_ROM_reconstruction_byte_exact']
    image=NdsImage.open(ROM);prior=NdsImage.open('out/all_routes_combined_v7011_candidate.nds');arm=image.read_file('/__arm9__.bin')
    native=read('work/analysis/square_shopkeeper_names_v7021/all_name_field_voice_dynamic_macro_and_complete_native_label_consumers.json')
    assert sha(arm)==native['target_ARM9_sha256']==release['ARM9_sha256']
    assert ROM.read_bytes()==Path(native['research_ROM']).read_bytes()
    assert len(release['stage']['data_plan']['changed_byte_offsets'])==18 and release['stage']['data_plan']['complete_ARM9_inverse']
    payload=bytes(MainCodeFile(arm,0x02000000).sections[3].data[:-48]);assert len(payload)==123264
    results=[];selected=[];total=0
    for case,run in [('newgame',Path('work/analysis/square_shopkeeper_run_v7019')),('town',Path('work/analysis/square_shopkeeper_runs_v7032'))]:
        pp=run/('run_plan.json' if case=='newgame' else 'town_plan.json');tp=run/('terminal.json' if case=='newgame' else 'town_terminal.json')
        plan,terminal=read(pp),read(tp);assert terminal['terminal'];rp=Path(terminal['report']);report=read(rp)
        assert sha(rp.read_bytes())==terminal['report_sha256'] and report['ROM_sha256']==digest
        oldtp=Path('work/analysis/lil_B221_runs_v7014')/(case+'_terminal.json');oldterminal=read(oldtp);oldrp=Path(oldterminal['report']);old=read(oldrp)
        assert sha(oldrp.read_bytes())==oldterminal['report_sha256'] and old['ROM_sha256']==sha(Path('out/all_routes_combined_v7011_candidate.nds').read_bytes())
        assert report['frames']==old['frames']==plan['frames']==(4001 if case=='newgame' else 17401)
        assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert not report['hardware_device_verification'] and not report['goal_complete']
        assert report['core_DLL_sha256']==old['core_DLL_sha256'] and report['core_options']==old['core_options']
        assert read(plan['inputs'])==report['scripted_input_schedule']==old['scripted_input_schedule'] and sha(Path(plan['inputs']).read_bytes())==plan['inputs_sha256']
        if case=='newgame':assert plan['no_battery_savestate_RAM_overlay_observer_or_extra_gameplay_input'] and not report.get('battery_save_preloaded')
        else:assert terminal['no_new_RAM_code_gameplay_fixture_or_observer'] and sha(Path(plan['source_donor']).read_bytes())==sha(Path(plan['disposable_donor']).read_bytes())==plan['source_donor_sha256']
        now,then=[{p['frame']:p for p in r['frames_captured']} for r in [report,old]];assert now.keys()==then.keys();pairs=[]
        for frame,a in now.items():
            b=then[frame];ap,bp=Path(a['path']),Path(b['path']);assert sha(ap.read_bytes())==a['PNG_sha256'] and sha(bp.read_bytes())==b['PNG_sha256']
            x,y=Image.open(ap).convert('RGB'),Image.open(bp).convert('RGB');assert x.size==y.size==(256,384) and x.tobytes()==y.tobytes(),(case,frame)
            pairs.append(dict(frame=frame,capture=str(ap),capture_sha256=a['PNG_sha256'],whole_framebuffer_equal_V7011=True));total+=1
        snapshots,oldsnapshots=[{s['frame']:s for s in r['read_only_capture_RAM_snapshots']} for r in [report,old]]
        snapshots[report['frames']]=report['read_only_RAM_snapshot'];oldsnapshots[old['frames']]=old['read_only_RAM_snapshot'];models=[]
        for frame in ([4000,4001] if case=='newgame' else [11900,13700,17401]):
            a,b=snapshots[frame],oldsnapshots[frame];raw,oldraw=Path(a['path']).read_bytes(),Path(b['path']).read_bytes()
            assert len(raw)==len(oldraw)==0x400000 and sha(raw)==a['sha256'] and sha(oldraw)==b['sha256']
            assert raw[0x387A20:0x387A20+123264]==payload
            cpu,get=get_machine(arm,raw);oldcpu,og=get_machine(prior.read_file('/__arm9__.bin'),oldraw);root,oldroot=get(0xCB184),og(0xCB184)
            assert get(0x7F244)==og(0x7F244) and bytes(cpu.mem_read(root,0x1A04))==bytes(oldcpu.mem_read(oldroot,0x1A04))
            row=dict(frame=frame,captain_ID=get(0x7F244),all_actor_models_including_actual_captain_equal=True,target_deployed123264_payload_exact=True)
            if case=='newgame':
                assert row['captain_ID']==2;block=IlnkContainer.parse(image.read_file('/data/SC2.DK4')).blocks[22]
                assert block==IlnkContainer.parse(prior.read_file('/data/SC2.DK4')).blocks[22]
                at=raw.find(block);assert at>=0 and oldraw.find(block)==at;row.update(Lil_B22_resident_payload_exact=True,address=0x02000000+at)
            models.append(row)
        wanted=[2000,2400,4000] if case=='newgame' else [11900,13700,17401]
        selected.extend(dict(case=case,**next(p for p in pairs if p['frame']==frame)) for frame in wanted)
        results.append(dict(case=case,frames=report['frames'],report=str(rp),report_sha256=sha(rp.read_bytes()),old_report=str(oldrp),old_report_sha256=sha(oldrp.read_bytes()),
            plan=str(pp),plan_sha256=sha(pp.read_bytes()),terminal=str(tp),terminal_sha256=sha(tp.read_bytes()),paired_whole_frames=pairs,postload_controls=models,
            reused_existing_exact_whole_ROM_target_run=case=='newgame',new_registered_current_capture=case=='town',inherited_five_ship_town_battery_not_earned_progress=case=='town'))
    assert total==31;ROOT.mkdir(parents=True);sheet=Image.new('RGB',(768,820),'#263238');draw=ImageDraw.Draw(sheet)
    for i,p in enumerate(selected):
        x,y=i%3*256,i//3*410;draw.text((x+2,y+3),f'V7029 {p["case"]} f{p["frame"]}',fill='white');sheet.paste(Image.open(p['capture']).convert('RGB'),(x,y+24))
    sp=ROOT/'current_name_layer_startup_and_town_review.png';sheet.save(sp)
    save(ROOT/'registered_current_startup_and_town_verification.json',dict(candidate=str(ROM),candidate_sha256=digest,ARM9_sha256=sha(arm),runs=results,
        paired_frame_count=31,all_current_requested_and_final_framebuffers_equal_V7011=True,all_five_actor_captain_and_current_payload_controls_pass=True,
        actual_target_NewGame7019_reused_by_exact_whole_ROM_hash=True,fresh_registered_town7032_cold_boot=True,new_current_candidate_runs=1,new_current_candidate_frames=17401,
        unchanged_source_and_disposable_town_donor=True,no_RAM_code_gameplay_fixture_observer_or_savestate=True,
        startup_does_not_activate_B189_or_B221_representative_name_scenes=True,full_route_natural_activation_and_hardware_not_claimed=True,
        review_sheet=str(sp),review_sheet_sha256=sha(sp.read_bytes()),visual_review_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),full_goal_complete=False))
    print('Current V7029:31 whole frames match V7011;five actor/captain/payload controls and donors pass. Exact target NewGame reused;fresh town captured. Visual review pending.',flush=True)
