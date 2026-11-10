"""Verify the corrected candidate’s own boot, loaded literal and protected original name getters."""
from pathlib import Path
from types import SimpleNamespace
import struct
from PIL import Image
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from dk4tool.patch.main_pool_cache_visibility import BASE,POOL
from dk4tool.patch.reviewed_name_catalog import ROUTE
from dk4tool.patch.market_goods_info_terminator_v1 import NEW_FORMAT,PAYLOAD,FIELDS
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.grand_race_menu_release import sha
from scripts.audit_story_glyph_consistency import load,save
from scripts.probe_escape_direct_source_v1186 import machine
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.write_rafael_B169_contextual_v1 import getter

OUT=Path('work/market_goods_info_terminator_release_v1')

def digest(p):return sha(Path(p).read_bytes())

def main():
    output=OUT/'own_registered_startup_verification.json';names_out=OUT/'own_registered_name_getters_v1.json'
    assert not output.exists() and not names_out.exists()
    staged_path=OUT/'staged_successor.json';staged=load(staged_path)
    report_path=OUT/'startup_run_v2/capture/capture_report.json';report=load(report_path)
    plan_path=OUT/'startup_run_v2/run_plan.json';plan=load(plan_path)
    assert digest(staged_path)==plan['staged_sha256']
    assert digest(staged['candidate'])==report['ROM_sha256']==staged['candidate_sha256']
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors'] and not report.get('battery_save_preloaded')
    assert report['frames']==4001 and report['scripted_input_schedule']==load(plan['unchanged_inputs'])
    old=load(plan['predecessor_report']);assert digest(plan['predecessor_report'])==plan['predecessor_report_sha256']
    old_frames={r['frame']:r for r in old['frames_captured']};captures={r['frame']:r for r in report['frames_captured']}
    matches=[]
    for frame in [1000,1800,2200,3000,4000,4001]:
        cap=captures[frame];assert digest(cap['path'])==cap['PNG_sha256']
        assert Image.open(cap['path']).tobytes()==Image.open(old_frames[frame]['path']).tobytes()
        matches.append(dict(frame=frame,path=cap['path'],sha256=cap['PNG_sha256'],exact_prior_approved_RGB=True))
    state=report['read_only_capture_native_states'][0]
    assert state['frame']==4001 and state['read_only_export'] and not state['state_loaded']
    assert state['main_RAM_unchanged_by_export'] and state['serialized_RAM_matches_same_frame_direct_export']
    itcm=state['regions']['ITCM'];data=Path(itcm['path']).read_bytes();assert len(data)==32768 and digest(itcm['path'])==itcm['sha256']
    assert data[NEW_FORMAT%32768:NEW_FORMAT%32768+len(PAYLOAD)]==PAYLOAD
    image=NdsImage.open(staged['candidate']);arm=image.read_file('/__arm9__.bin');common=image.read_file('/COMMON/MESFILE.DK4')
    sections=MainCodeFile(arm,BASE).sections;assert len(sections)==6
    assert bytes(sections[4].data)[0x6AC:0x6B0]==data[0x46AC:0x46B0]==bytes.fromhex('0c209fe5')
    snapshot=report['read_only_RAM_snapshot'];raw=Path(snapshot['path']).read_bytes()
    assert len(raw)==0x400000 and snapshot['read_only_export'] and digest(snapshot['path'])==snapshot['sha256']
    for field in FIELDS:assert struct.unpack_from('<I',raw,field)[0]==NEW_FORMAT
    payload=bytes(sections[3].data[:-48]);assert len(payload)==123264 and raw[POOL-BASE:POOL-BASE+len(payload)]==payload
    owners=[*sections,SimpleNamespace(ramAddress=POOL,data=payload)];cpu,get,_=machine(arm,common,raw,dict(patches=[]));executed=set()
    def exact(u,pc,size,_):
        matches=[s for s in owners if s.ramAddress<=pc and pc+size<=s.ramAddress+len(s.data)];assert len(matches)==1
        owner=matches[0];at=pc-owner.ramAddress;assert bytes(u.mem_read(pc,size))==bytes(owner.data[at:at+size]);executed.add(pc)
    hook=cpu.hook_add(UC_HOOK_CODE,exact);before=bytes(cpu.mem_read(BASE,0x400000))
    captain,actors=get(0x7F244),get(0xCB184);route=int.from_bytes(cpu.mem_read(ROUTE,4),'little')
    cpu.hook_del(hook);assert captain==route==0 and bytes(cpu.mem_read(BASE,0x400000))==before
    save(output,dict(candidate=staged['candidate'],candidate_sha256=staged['candidate_sha256'],profile=staged['profile'],
        cold_boot=True,savestate=False,frames=4001,callback_errors=0,actual_captain_getter=captain,actual_route_word=route,
        actual_actor_root=actors,read_only_snapshot=snapshot,ordinary_Rafael_title_NewGame_andopening_observed=True,
        six_opening_frames_exact_prior_RGB=matches,three_selection_andopening_frames_directly_viewed=True,
        complete123264_staged_payload_exact=True,new_declared_format_bytes_andpointer_fields_loaded_exact=True,
        original_town_capture_instruction_loaded_exact=True,native_getter_did_not_change_main_RAM=True,
        original_getter_instruction_addresses=len(executed),capture_report=str(report_path),capture_report_sha256=digest(report_path),
        no_historical_RAM_overlay_orstory_save_override=True,no_hardware_claim=True,new_credit=0))
    context_path=OUT/'own_startup_native_context_input.json'
    save(context_path,{**staged,'own_registered_startup_pending':False,'own_registered_startup':str(output),
        'own_registered_startup_sha256':digest(output),'experimental_pre_registration_native_context':True})
    expected_path=Path('work/maria301_release_v1/own_registered_name_getters_v1.json');reference=load(expected_path)
    actors=sorted(map(int,reference['expected']))
    ctx=RegisteredRuntime(context_path,output,captain=0)
    env={**getter.__globals__,'ACTORS':actors}
    exec(compile(reference['original_adapter'],__file__+'::same-original-both-name-getters-own-fixed-candidate-RAM','exec'),env)
    native=ctx.execute(env['names']);assert len(native['rows'])==24
    for row in native['rows']:assert row['text']==reference['expected'][str(row['actor_ID'])][row['consumer']]
    save(names_out,dict(runtime=ctx.receipt(),own_name_consumers=native,
        both_name_getters_exact_for_all12_protected_actors=True,expected=reference['expected'],
        original_adapter=reference['original_adapter'],full_catalogue_UI_unvisited=True,no_historical_RAM_overlay=True,new_credit=0,
        evidence={str(p):digest(p) for p in [output,context_path,expected_path,Path(__file__)]}))
    print('PASS own4001-frame Rafael boot;new literal andboth pointers loaded,town code exact;24 protected name getters pass.')

if __name__=='__main__':main()
