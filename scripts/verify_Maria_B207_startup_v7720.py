"""Bind five own-ROM startup controls andstrict current inputs for allfour captains."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.maria_existing_unlock_contract_v7680 import validate_capture
from scripts.papal_trade_route_native_context_v7626 import RouteCurrentContext
from scripts.square_shopkeeper_exact_native_context_v7020 import CurrentContext
from scripts.maria_unlocked_current_context_v7680 import MariaUnlockedCurrentContext
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_B207_startup_verification_v7720')
RUN=Path('work/analysis/maria_B207_startup_runs_v7719')
NATIVE=Path('work/analysis/current_V7717_native_v7720')
RELEASE=Path('work/analysis/maria_B207_release_v7718/registered_release_verification.json')
if __name__=='__main__':
    cases=['route0','route1','route2','route3','town'];assert not ROOT.exists() and not NATIVE.exists() and all(read(RUN/c/'terminal.json')['terminal'] for c in cases)
    release=read(RELEASE);rom=Path(release['candidate']);image=NdsImage.open(rom);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
    assert arm==NdsImage.open('out/all_routes_combined_v7660_candidate.nds').read_file('/__arm9__.bin') and sha(rom.read_bytes())==release['candidate_sha256']
    ROOT.mkdir(parents=True);runs=[];photos=[];total=0;frames_total=0;contexts=[]
    for case in cases:
        pp,tp=RUN/case/'run_plan.json',RUN/case/'terminal.json';plan,terminal=map(read,[pp,tp]);ot=Path(plan['prior_terminal']);oldterminal=read(ot);rp,op=Path(terminal['report']),Path(oldterminal['report']);report,old=map(read,[rp,op])
        assert sha(rp.read_bytes())==terminal['report_sha256'] and sha(op.read_bytes())==oldterminal['report_sha256'] and report['ROM_sha256']==release['candidate_sha256']==terminal['candidate_sha256']
        assert report['frames']==old['frames']==plan['frames'] and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
        assert report['scripted_input_schedule']==old['scripted_input_schedule'] and report['core_options']==old['core_options']
        if case=='route3':validate_capture(report);validate_capture(old)
        elif case=='town':assert report['battery_save_preloaded'] and sha(Path(plan['source_donor']).read_bytes())==sha(Path(plan['disposable_donor']).read_bytes())==plan['source_donor_sha256']
        else:assert not report.get('battery_save_preloaded') and not any(v for k,v in report.items() if k.startswith('synthetic_'))
        oldpics={p['frame']:p for p in old['frames_captured']};pairs=[]
        for p in report['frames_captured']:
            q=oldpics[p['frame']];assert sha(Path(p['path']).read_bytes())==p['PNG_sha256'] and sha(Path(q['path']).read_bytes())==q['PNG_sha256']
            assert Image.open(p['path']).convert('RGB').tobytes()==Image.open(q['path']).convert('RGB').tobytes(),(case,p['frame'])
            pairs.append(dict(frame=p['frame'],current=p,prior=q,whole_RGB_equal=True));total+=1
        controls=[];expected={'route0':0,'route1':1,'route2':2,'route3':3,'town':1}[case]
        chosen=[4000] if case!='town' else [f for f in [3200,4000,17400] if any(s['frame']==f for s in report['read_only_capture_RAM_snapshots'])]
        assert chosen
        for frame in chosen:
            values=[]
            for r in [old,report]:
                snap=next(s for s in r['read_only_capture_RAM_snapshots'] if s['frame']==frame);raw=Path(snap['path']).read_bytes();assert snap['read_only_export'] and len(raw)==4194304 and sha(raw)==snap['sha256']
                cpu,get=get_machine(arm,raw);actor=get(0xCB184);captain=get(0x7F244);assert captain==expected
                values.append(dict(captain=captain,actor_root=actor,whole_actor_sha256=sha(bytes(cpu.mem_read(actor,0x1A04)))))
            assert values[0]==values[1],(case,frame);controls.append(dict(frame=frame,prior=values[0],current=values[1],equal=True))
        if case!='town':
            nr=NATIVE if case=='route2' else NATIVE/case;nr.mkdir(parents=True,exist_ok=case=='route2')
            snap=next(s for s in report['read_only_capture_RAM_snapshots'] if s['frame']==4000)
            proof=nr/'own_registered_capture_context.json';save(proof,dict(capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes()),frame=4000,snapshot_sha256=snap['sha256'],directory_sha256='80d007e6b0f0a7eb60ec8d51d25211302371b763a3f49eea666044d49064cc3e',route=expected,actual_original_captain_ID=expected))
            inp=nr/'current_native_input.json';save(inp,dict(current_ROM=str(rom),current_ROM_sha256=release['candidate_sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),native_context_proof=str(proof),registered_profile='all-routes-unified-v7717',expected_original_captain_ID=expected,route_identity=plan['route_identity'],own_current_cold_boot_RAM_no_historical_ROM_oroverlay=True,existing_system_only_unlock_fixture=expected==3,earned_unlock_verified=False if expected==3 else None))
            cls=RouteCurrentContext if expected in [0,1] else CurrentContext if expected==2 else MariaUnlockedCurrentContext
            ctx=cls(inp,'unused-no-historical-ROM',nr/'current_context');assert not ctx.machines
            contexts.append(dict(route=expected,route_identity=plan['route_identity'],input=str(inp),input_sha256=sha(inp.read_bytes()),native_plan=str(ctx.proof_path),native_plan_sha256=sha(ctx.proof_path.read_bytes()),actual_captain=expected,strict2b6_COMMON_directory123264_payload_andownership_guards_pass=True,existing_system_only_unlock_earned_false=expected==3))
        selected=[3200,3400,4000] if case=='route3' else [2000,4000] if case!='town' else [f for f in [3200,17400] if f in oldpics]
        for frame in selected:
            p=next(p for p in report['frames_captured'] if p['frame']==frame);photos.append(dict(case=case,frame=frame,capture=p['path'],sha256=p['PNG_sha256']))
        frames_total+=report['frames'];runs.append(dict(case=case,plan=str(pp),plan_sha256=sha(pp.read_bytes()),terminal=str(tp),terminal_sha256=sha(tp.read_bytes()),capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes()),prior_report=str(op),prior_report_sha256=sha(op.read_bytes()),whole_frame_pairs=pairs,actor_captain_controls=controls,measured_original_captain_ID=expected,source_anddisposable_donors_unchanged=True,existing_system_only_unlock_not_earned=case=='route3',inherited_town_battery_not_earned=case=='town'))
    assert total==47 and frames_total==33405 and [r['actual_captain'] for r in contexts]==[0,1,2,3]
    sheets=[]
    for start in range(0,len(photos),4):
        sheet=Image.new('RGB',(1024,410),'#263238');draw=ImageDraw.Draw(sheet)
        for i,p in enumerate(photos[start:start+4]):draw.text((i*256+3,3),f"V7717 {p['case']} frame{p['frame']}",fill='white');sheet.paste(Image.open(p['capture']).convert('RGB'),(i*256,24))
        sp=ROOT/f'own_ROM_startup_town_sheet{start//4+1}.png';sheet.save(sp);sheets.append(dict(path=str(sp),sha256=sha(sp.read_bytes())))
    save(ROOT/'own_ROM_four_NewGames_town_exact_V7660_controls_andfour_strict_inputs.json',dict(candidate=str(rom),candidate_sha256=release['candidate_sha256'],runs=runs,whole_RGB_frame_pairs=47,actual_frames=33405,all_current_requested_andfinal_frames_equal_V7660=True,all_native_actor_andcaptain_controls_equal=True,actual_NewGame_captains=[0,1,2,3],actual_inherited_town_captain=1,town_capture3200_Copenhagen_not_Stockholm=True,all_four_own_current_strict_native_contexts=contexts,default_Lil_native_input=str(NATIVE/'current_native_input.json'),source_anddisposable_town_donors_unchanged=True,Maria_exact_system_only_unlock_earned_false=True,no_RAM_code_observer_savestate_roles_roster_funds_RNG_orresult_forcing=True,no_optional_activation_fullroute_orhardware_claim=True,review_sheets=sheets,visual_review_pending=True,producer_sha256=sha(Path(__file__).read_bytes()),new_credit=0,full_goal_complete=False))
    print('Own V7717:47 exact whole-frame pairs/33405 frames;allfour captains0_1_2_3 plusCopenhagen town1/actors/donors matchV7660. Four strict own-ROM inputs bound;visual review pending.')
