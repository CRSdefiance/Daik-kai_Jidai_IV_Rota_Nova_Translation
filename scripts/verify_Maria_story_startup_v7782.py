"""Bind own registered Maria cold boot,whole-frame/actor controls andstrict current snapshot."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.maria_existing_unlock_contract_v7680 import validate_capture
from scripts.maria_unlocked_current_context_v7680 import MariaUnlockedCurrentContext
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/maria_story_startup_verification_v7782')
RUN=Path('work/analysis/maria_story_startup_runs_v7781/route3')
NATIVE=Path('work/analysis/current_V7779_native_v7782/route3')
RELEASE=Path('work/analysis/maria_story_release_v7780/registered_release_verification.json')
if __name__=='__main__':
    assert not ROOT.exists() and not NATIVE.exists()
    plan,terminal,release=map(read,[RUN/'run_plan.json',RUN/'terminal.json',RELEASE]);assert terminal['terminal']
    oldterminal=read(plan['prior_terminal']);rp,op=Path(terminal['report']),Path(oldterminal['report']);report,old=map(read,[rp,op])
    assert sha(rp.read_bytes())==terminal['report_sha256'] and sha(op.read_bytes())==oldterminal['report_sha256']
    assert report['ROM_sha256']==release['candidate_sha256']==terminal['candidate_sha256']
    assert report['frames']==old['frames']==plan['frames'] and report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['scripted_input_schedule']==old['scripted_input_schedule'] and report['core_options']==old['core_options']
    validate_capture(report);validate_capture(old)
    rom=Path(release['candidate']);image=NdsImage.open(rom);previous=NdsImage.open('out/all_routes_combined_v7717_candidate.nds')
    arm,common=image.read_file('/__arm9__.bin'),image.read_file('/COMMON/MESFILE.DK4')
    assert arm==previous.read_file('/__arm9__.bin') and common==previous.read_file('/COMMON/MESFILE.DK4')
    priorphotos={p['frame']:p for p in old['frames_captured']};pairs=[]
    for photo in report['frames_captured']:
        prior=priorphotos[photo['frame']]
        assert sha(Path(photo['path']).read_bytes())==photo['PNG_sha256'] and sha(Path(prior['path']).read_bytes())==prior['PNG_sha256']
        assert Image.open(photo['path']).convert('RGB').tobytes()==Image.open(prior['path']).convert('RGB').tobytes()
        pairs.append(dict(frame=photo['frame'],current=photo,prior=prior,whole_RGB_equal=True))
    values=[]
    for value in [old,report]:
        snap=next(s for s in value['read_only_capture_RAM_snapshots'] if s['frame']==4000);raw=Path(snap['path']).read_bytes()
        assert snap['read_only_export'] and len(raw)==4194304 and sha(raw)==snap['sha256']
        cpu,get=get_machine(arm,raw);actor=get(0xCB184);captain=get(0x7F244);assert captain==3
        values.append(dict(captain=captain,actor_root=actor,whole_actor_sha256=sha(bytes(cpu.mem_read(actor,0x1A04)))))
    assert values[0]==values[1]
    ROOT.mkdir(parents=True);NATIVE.mkdir(parents=True)
    snap=next(s for s in report['read_only_capture_RAM_snapshots'] if s['frame']==4000)
    proof=NATIVE/'own_registered_capture_context.json'
    save(proof,dict(capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes()),frame=4000,snapshot_sha256=snap['sha256'],
        directory_sha256='80d007e6b0f0a7eb60ec8d51d25211302371b763a3f49eea666044d49064cc3e',route=3,actual_original_captain_ID=3))
    inp=NATIVE/'current_native_input.json'
    save(inp,dict(current_ROM=str(rom),current_ROM_sha256=release['candidate_sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),
        native_context_proof=str(proof),registered_profile='all-routes-unified-v7779',expected_original_captain_ID=3,route_identity='Maria',
        own_current_cold_boot_RAM_no_historical_ROM_oroverlay=True,existing_system_only_unlock_fixture=True,earned_unlock_verified=False))
    ctx=MariaUnlockedCurrentContext(inp,'unused-no-historical-ROM',NATIVE/'current_context');assert not ctx.machines
    chosen=[3200,3400,4000];sheet=Image.new('RGB',(768,410),'#263238');draw=ImageDraw.Draw(sheet)
    for i,frame in enumerate(chosen):
        p=next(p for p in report['frames_captured'] if p['frame']==frame)
        draw.text((i*256+3,3),f'V7779 Maria frame{frame}',fill='white');sheet.paste(Image.open(p['path']).convert('RGB'),(i*256,24))
    path=ROOT/'own_Maria_registered_startup.png';sheet.save(path)
    save(ROOT/'own_Maria_startup_exact_V7717_andstrict_current_input.json',dict(candidate=str(rom),candidate_sha256=release['candidate_sha256'],
        run_plan=str(RUN/'run_plan.json'),run_plan_sha256=sha((RUN/'run_plan.json').read_bytes()),
        terminal=str(RUN/'terminal.json'),terminal_sha256=sha((RUN/'terminal.json').read_bytes()),capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes()),
        prior_report=str(op),prior_report_sha256=sha(op.read_bytes()),whole_frame_pairs=pairs,whole_RGB_frame_pairs=len(pairs),actual_frames=report['frames'],
        all_current_requested_andfinal_frames_equal_V7717=True,actual_original_captain_ID=3,actor_captain_controls=values,
        strict_current_native_input=str(inp),strict_current_native_input_sha256=sha(inp.read_bytes()),
        native_plan=str(ctx.proof_path),native_plan_sha256=sha(ctx.proof_path.read_bytes()),
        strict2b6_COMMON_directory_andall123264_payload_bytes_verified=True,existing_system_only_unlock_earned_false=True,
        unaffected_other_routes_andcompleted_prior_startups_reused_byunchanged_files_components_not_new_captures=True,
        no_optional_activation_original_location_earned_progress_fullroute_orhardware_claim=True,
        review_sheet=dict(path=str(path),sha256=sha(path.read_bytes())),visual_review_pending=True,new_credit=0,full_goal_complete=False))
    print('Own V7779 Maria startup:',len(pairs),'whole-frame pairs/',report['frames'],'frames;captain3/wholeactors matchV7717.Strict own-ROM input bound;visual review pending.')
