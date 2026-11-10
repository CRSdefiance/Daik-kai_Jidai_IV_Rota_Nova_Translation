"""Capture a registered build's own route context using a verified ordinary input schedule."""
import argparse
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from dk4tool.patch.main_pool_cache_visibility import BASE,POOL
from dk4tool.patch.reviewed_name_catalog import ROUTE
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.probe_escape_direct_source_v1186 import machine

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    for key in ['release','parent-startup','out']:ap.add_argument('--'+key,type=Path,required=True)
    ap.add_argument('--captain',type=int,choices=range(4),required=True)
    args=ap.parse_args();assert not args.out.exists()
    release,parent=map(load,(args.release,args.parent_startup))
    assert not release['own_registered_startup_pending'] and release['clean_input_patch_byte_exact']
    assert parent['cold_boot'] and not parent['savestate'] and parent['frames']==4001
    assert parent['actual_captain_getter']==args.captain and parent['six_key_frames_directly_viewed']
    assert digest(parent['capture_report'])==parent['capture_report_sha256']
    prior=load(parent['capture_report']);candidate=Path(release['candidate'])
    assert digest(candidate)==release['candidate_sha256']
    assert digest(release['manifest'])==release['manifest_sha256']
    assert digest('translations/release_stack.json')==release['registry_sha256']
    assert all(load(release['manifest'])['checks'].values())
    args.out.mkdir(parents=True);inputs=args.out/'ordinary_inputs.json'
    save(inputs,prior['scripted_input_schedule'])
    frames=prior['exact_requested_capture_frames'];assert len(frames)==6
    assert len(prior['frames_captured'])==len(parent['exact_own_RGB_reuse_of_prior_direct_visual_review'])==10
    assert all(r['byte_identical_to_prior_reviewed_RGB'] for r in parent['exact_own_RGB_reuse_of_prior_direct_visual_review'])
    command=[sys.executable,'-m','scripts.headless_desmume_v193','--rom',str(candidate),'--out',str(args.out),
        '--frames','4001','--inputs-json',str(inputs),'--capture-every','999999',
        '--capture-at',*map(str,frames),'--dump-ram']
    # Keep the emulator DLL in a clean process, separate from Unicorn's DLLs.
    subprocess.run(command,check=True)
    report_path=args.out/'capture_report.json';report=load(report_path)
    assert report['frames']==4001 and report['cold_boot'] and not report['savestate_loaded']
    assert report['ROM_sha256']==release['candidate_sha256'] and not report['callback_errors']
    assert report['scripted_input_schedule']==prior['scripted_input_schedule']
    old,new=[{r['frame']:r for r in p['frames_captured']} for p in (prior,report)]
    assert set(old)==set(new) and len(new)==10 and set(frames)<=set(new)
    pairs=[]
    for frame in sorted(new):
        a,b=old[frame],new[frame]
        assert digest(a['path'])==a['PNG_sha256'] and digest(b['path'])==b['PNG_sha256']
        assert Path(a['path']).read_bytes()==Path(b['path']).read_bytes(),('Fresh opening needs direct review',frame)
        pairs.append(dict(frame=frame,parent_capture=a['path'],own_capture=b['path'],
            PNG_sha256=b['PNG_sha256'],byte_identical_to_prior_reviewed_RGB=True))
    image=NdsImage.open(candidate);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
    snapshot={**report['read_only_RAM_snapshot'],'frame':4001,
        'recorded_after_final_frame_no_historical_overlay':True}
    raw=Path(snapshot['path']).read_bytes()
    assert snapshot['read_only_export'] and len(raw)==snapshot['bytes']==0x400000 and digest(snapshot['path'])==snapshot['sha256']
    sections=MainCodeFile(arm,BASE).sections;payload=bytes(sections[3].data[:-48])
    assert len(payload)==123264 and raw[POOL-BASE:POOL-BASE+len(payload)]==payload
    owners=[*sections,SimpleNamespace(ramAddress=POOL,data=payload)]
    cpu,get,_=machine(arm,common,raw,dict(patches=[]));executed=set()
    def exact(u,pc,size,_):
        matches=[s for s in owners if s.ramAddress<=pc and pc+size<=s.ramAddress+len(s.data)]
        assert len(matches)==1
        owner=matches[0]
        assert bytes(u.mem_read(pc,size))==bytes(owner.data[pc-owner.ramAddress:pc-owner.ramAddress+size])
        executed.add(pc)
    hook=cpu.hook_add(UC_HOOK_CODE,exact);before=bytes(cpu.mem_read(BASE,0x400000))
    captain=get(0x7F244);root=get(0xCB184);cpu.hook_del(hook)
    route=int.from_bytes(cpu.mem_read(ROUTE,4),'little')
    assert captain==route==args.captain and bytes(cpu.mem_read(BASE,0x400000))==before
    assert BASE<=root<BASE+0x400000-0x1A04
    assert digest(parent['review_sheet'])==parent['review_sheet_sha256']
    proof=args.out/'own_route_context.json'
    save(proof,dict(candidate=str(candidate),candidate_sha256=release['candidate_sha256'],profile=release['profile'],
        capture_report=str(report_path),capture_report_sha256=digest(report_path),cold_boot=True,savestate=False,
        frames=4001,callback_errors=0,actual_captain_getter=captain,actual_route_word=route,actual_actor_root=root,
        read_only_snapshot=snapshot,native_getter_did_not_change_main_RAM=True,
        complete123264_staged_payload_exact=True,original_getter_instruction_addresses=len(executed),
        six_key_frames_directly_viewed=True,exact_own_RGB_reuse_of_prior_direct_visual_review=pairs,
        review_sheet=parent['review_sheet'],review_sheet_sha256=parent['review_sheet_sha256'],
        review_sheet_is_prior_exact_RGB_reuse_not_a_new_capture=True,
        parent_startup=str(args.parent_startup),parent_startup_sha256=digest(args.parent_startup),
        registered_release=str(args.release),registered_release_sha256=digest(args.release),
        no_historical_RAM_overlay=True,no_new_optional_scene_activation_orhardware_claim=True,
        no_registered_release_or_ledger_mutation=True,new_credit=0,producer_sha256=digest(__file__)))
    print('Verified own route',captain,'on registered build: 4001 frames, ten exact reviewed RGB captures and fresh RAM.')

if __name__=='__main__':main()
