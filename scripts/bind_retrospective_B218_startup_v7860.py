"""Bind the fresh own-ROM Lil snapshot and exact prior startup controls."""
from pathlib import Path
from PIL import Image,ImageDraw
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.square_shopkeeper_exact_native_context_v7020 import CurrentContext
from scripts.verify_personal_gameplay_v841 import get_machine
from scripts.verify_village_wrap_v608 import read,save
ROOT=Path('work/analysis/retrospective_B218_startup_binding_v7860')
RUN=Path('work/analysis/retrospective_B218_startup_runs_v7859/route2')
NATIVE=Path('work/analysis/current_V7857_Lil_native_v7860')
if __name__=='__main__':
    assert not ROOT.exists() and not NATIVE.exists()
    terminal,plan=map(read,[RUN/'terminal.json',RUN/'run_plan.json'])
    assert terminal['terminal'] and plan['route']==plan['expected_original_captain_ID']==2
    rp=Path(terminal['report']);report=read(rp);previous_terminal=read(plan['prior_terminal']);op=Path(previous_terminal['report']);old=read(op)
    assert sha(rp.read_bytes())==terminal['report_sha256'] and sha(op.read_bytes())==previous_terminal['report_sha256']
    assert report['ROM_sha256']==terminal['candidate_sha256']==plan['candidate_sha256']
    for value in [report,old]:
        assert value['frames']==4001 and value['cold_boot'] and not value['savestate_loaded'] and not value['callback_errors']
        assert not value.get('battery_save_preloaded') and not any(v for k,v in value.items() if k.startswith('synthetic_'))
    assert report['scripted_input_schedule']==old['scripted_input_schedule'] and report['core_options']==old['core_options']
    image=NdsImage.open(plan['candidate']);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
    previous=NdsImage.open(old['ROM'])
    from dk4tool.formats.ilnk import IlnkContainer
    mapping=read('translations/lil_B218_retrospective_relocation_map_v1.json')
    old_blocks,new_blocks=[IlnkContainer.parse(im.read_file('/data/SC2.DK4')).blocks for im in [previous,image]]
    assert len(old_blocks)==len(new_blocks)==336 and [i for i,(a,b) in enumerate(zip(old_blocks,new_blocks,strict=True)) if a!=b]==[218]
    assert sha(old_blocks[218])==mapping['groups'][0]['source_block_sha256'] and sha(new_blocks[218])==mapping['groups'][0]['target_block_sha256']
    for path in ['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']:
        assert image.read_file(path)==previous.read_file(path)
    priorphotos={p['frame']:p for p in old['frames_captured']};pairs=[];actors=[]
    for p in report['frames_captured']:
        q=priorphotos[p['frame']]
        assert sha(Path(p['path']).read_bytes())==p['PNG_sha256'] and sha(Path(q['path']).read_bytes())==q['PNG_sha256']
        assert Image.open(p['path']).convert('RGB').tobytes()==Image.open(q['path']).convert('RGB').tobytes()
        pairs.append(dict(frame=p['frame'],current=p,prior=q,whole_RGB_equal=True))
    for value in [old,report]:
        snap=next(s for s in value['read_only_capture_RAM_snapshots'] if s['frame']==4000)
        raw=Path(snap['path']).read_bytes();assert snap['read_only_export'] and len(raw)==4194304 and sha(raw)==snap['sha256']
        cpu,get=get_machine(arm,raw);root=get(0xCB184);assert get(0x7F244)==2
        actors.append(dict(captain=2,actor_root=root,whole_actor_sha256=sha(bytes(cpu.mem_read(root,0x1A04)))))
    assert actors[0]==actors[1]
    ROOT.mkdir(parents=True);NATIVE.mkdir(parents=True)
    snap=next(s for s in report['read_only_capture_RAM_snapshots'] if s['frame']==4000)
    proof=NATIVE/'own_registered_capture_context.json'
    save(proof,dict(capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes()),frame=4000,snapshot_sha256=snap['sha256'],
        directory_sha256='80d007e6b0f0a7eb60ec8d51d25211302371b763a3f49eea666044d49064cc3e',route=2))
    inp=NATIVE/'current_native_input.json'
    save(inp,dict(current_ROM=plan['candidate'],current_ROM_sha256=plan['candidate_sha256'],current_ARM9_sha256=sha(arm),current_COMMON_sha256=sha(common),
        native_context_proof=str(proof),registered_profile=plan['profile'],expected_original_captain_ID=2,route_identity='Lil',
        own_current_cold_boot_RAM_no_historical_ROM_oroverlay=True))
    ctx=CurrentContext(inp,'unused-no-historical-ROM',NATIVE/'current_context');assert not ctx.machines
    sheet=Image.new('RGB',(512,410),'#263238');draw=ImageDraw.Draw(sheet)
    for i,frame in enumerate([2000,4000]):
        p=next(p for p in report['frames_captured'] if p['frame']==frame)
        draw.text((i*256+3,3),f'V7857 Lil frame{frame}',fill='white');sheet.paste(Image.open(p['path']).convert('RGB'),(i*256,24))
    path=ROOT/'own_Lil_current_context.png';sheet.save(path)
    save(ROOT/'own_Lil_startup_andstrict_current_context.json',dict(candidate=plan['candidate'],candidate_sha256=plan['candidate_sha256'],
        capture_report=str(rp),capture_report_sha256=sha(rp.read_bytes()),prior_report=str(op),prior_report_sha256=sha(op.read_bytes()),
        actual_frames=4001,whole_RGB_pairs=pairs,whole_RGB_pair_count=len(pairs),actor_captain_controls=actors,
        all_prior_whole_RGB_actor_andcaptain_controls_equal=True,actual_captain=2,
        strict_current_native_input=str(inp),strict_current_native_input_sha256=sha(inp.read_bytes()),
        native_plan=str(ctx.proof_path),native_plan_sha256=sha(ctx.proof_path.read_bytes()),
        all_strict2b6_COMMON_directory_and123264_payload_guards_pass=True,
        review_sheet=dict(path=str(path),sha256=sha(path.read_bytes())),visual_review_pending=True,
        no_story_event_activation_ornew_B218_gameplay_claim=True,new_credit=0,new_emulator_runs=1,
        evidence={str(p):sha(p.read_bytes()) for p in [RUN/'terminal.json',RUN/'run_plan.json',Path(__file__)]},full_goal_complete=False))
    print('Own V7857 Lil context bound:',len(pairs),'whole-frame pairs/4001frames,wholeactors andcaptain2 exact. Strict native input ready;sheet view pending.')
