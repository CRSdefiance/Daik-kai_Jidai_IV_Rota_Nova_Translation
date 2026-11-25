"""Verify a candidate's own cold boot and reuse byte-identical reviewed startup frames."""
import argparse
from pathlib import Path
from types import SimpleNamespace
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from dk4tool.patch.grand_race_menu_release import sha
from dk4tool.patch.main_pool_cache_visibility import BASE,POOL
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.probe_escape_direct_source_v1186 import machine

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    for arg in ('release','capture','parent-startup','out'):
        parser.add_argument('--'+arg,type=Path,required=True)
    args=parser.parse_args();assert not args.out.exists()
    release,capture,parent=map(load,[args.release,args.capture,args.parent_startup])
    candidate=Path(release['candidate'])
    assert sha(candidate.read_bytes())==release['candidate_sha256']==capture['ROM_sha256']
    assert capture['cold_boot'] and not capture['savestate_loaded'] and capture['frames']==4001
    assert not capture['callback_errors'] and release['clean_input_patch_byte_exact']
    assert release['parent_sha256']==parent['candidate_sha256']
    assert release['all_other_files_components_graphics_names_andruntime_exact_to_parent']
    previous_capture_path=Path(parent['capture_report'])
    assert sha(previous_capture_path.read_bytes())==parent['capture_report_sha256']
    previous=load(previous_capture_path)
    assert previous['scripted_input_schedule']==capture['scripted_input_schedule']
    assert previous['exact_requested_capture_frames']==capture['exact_requested_capture_frames']
    old,new=[{p['frame']:p for p in r['frames_captured']} for r in (previous,capture)]
    assert set(old)==set(new)
    pairs=[]
    for frame in sorted(new):
        a,b=old[frame],new[frame]
        assert sha(Path(a['path']).read_bytes())==a['PNG_sha256']
        assert sha(Path(b['path']).read_bytes())==b['PNG_sha256']
        assert Path(a['path']).read_bytes()==Path(b['path']).read_bytes(), ('New startup image needs direct review',frame)
        pairs.append(dict(frame=frame,parent_capture=a['path'],own_capture=b['path'],
            PNG_sha256=b['PNG_sha256'],byte_identical_to_prior_reviewed_RGB=True))
    image=NdsImage.open(candidate);parent_image=NdsImage.open(parent['candidate'])
    unchanged=['/__arm9__.bin','/COMMON/MESFILE.DK4','/GRP/KANJI.FNT']
    unchanged.extend(path for _,path,_ in image.iter_files() if 'HELP' in Path(path).name.upper())
    assert all(image.read_file(path)==parent_image.read_file(path) for path in unchanged)
    arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
    snapshot=next(p for p in capture['read_only_capture_RAM_snapshots'] if p['frame']==4000)
    raw=Path(snapshot['path']).read_bytes()
    assert snapshot['read_only_export'] and len(raw)==snapshot['bytes']==0x400000 and sha(raw)==snapshot['sha256']
    sections=MainCodeFile(arm,BASE).sections;payload=bytes(sections[3].data[:-48])
    assert len(payload)==123264 and raw[POOL-BASE:POOL-BASE+len(payload)]==payload
    assert raw[1435252:1435264]==b'Adernkatz\0\0\0' and raw[1435264:1435272]==b'Blades\0\0'
    owners=[*sections,SimpleNamespace(ramAddress=POOL,data=payload)]
    cpu,get,_=machine(arm,common,raw,dict(patches=[]));executed=set()
    def exact(u,pc,size,_):
        matches=[s for s in owners if s.ramAddress<=pc and pc+size<=s.ramAddress+len(s.data)]
        assert len(matches)==1,hex(pc)
        owner=matches[0]
        assert bytes(u.mem_read(pc,size))==bytes(owner.data[pc-owner.ramAddress:pc-owner.ramAddress+size]),hex(pc)
        executed.add(pc)
    hook=cpu.hook_add(UC_HOOK_CODE,exact)
    before=bytes(cpu.mem_read(BASE,0x400000))
    captain=get(0x7F244);root=get(0xCB184)
    cpu.hook_del(hook)
    assert captain==1 and bytes(cpu.mem_read(BASE,0x400000))==before
    assert BASE<=root<BASE+0x400000-0x1A04
    assert sha(Path(parent['review_sheet']).read_bytes())==parent['review_sheet_sha256']
    result=dict(candidate=str(candidate),candidate_sha256=release['candidate_sha256'],profile=release['profile'],
        capture_report=str(args.capture),capture_report_sha256=sha(args.capture.read_bytes()),
        cold_boot=True,savestate=False,frames=capture['frames'],callback_errors=0,
        six_key_frames_directly_viewed=parent['six_key_frames_directly_viewed'],
        exact_own_RGB_reuse_of_prior_direct_visual_review=pairs,
        review_sheet=parent['review_sheet'],review_sheet_sha256=parent['review_sheet_sha256'],
        review_sheet_is_prior_exact_RGB_reuse_not_a_new_capture=True,
        ordinary_title_NewGame_Hodram_Joakim_Bergstrom_andopening_observed=True,
        actual_captain_getter=captain,actual_actor_root=root,read_only_snapshot=snapshot,
        native_getter_did_not_change_main_RAM=True,original_getter_instruction_addresses=len(executed),
        complete123264_staged_payload_andGerhard_next_Blades_exact=True,
        unchanged_runtime_resources=unchanged,ARM9_COMMON_HELP_font_equal_registered_runtime_parent=True,
        original_COMMON_host_IO_cache_reset_disclosed_no_historical_RAM_overlay=True,
        no_new_optional_scene_activation_orhardware_claim=True,
        parent_startup=str(args.parent_startup),parent_startup_sha256=sha(args.parent_startup.read_bytes()),
        producer_sha256=sha(Path(__file__).read_bytes()))
    save(args.out,result)
    release['own_registered_startup_pending']=False
    release['own_registered_startup']=str(args.out)
    release['own_registered_startup_sha256']=sha(args.out.read_bytes())
    save(args.release,release)
    print('Own4001-frame registered cold boot,all10 exact RGB pairs,current captain1,payload andprotected names pass;no old RAM overlay.')

if __name__=='__main__':
    main()
