"""Verify this candidate's own Maria coldboot and both protected native name getters."""
from pathlib import Path
from types import SimpleNamespace
import sys
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from dk4tool.patch.main_pool_cache_visibility import BASE,POOL
from dk4tool.patch.reviewed_name_catalog import ROUTE
from dk4tool.rom.nds import NdsImage
from scripts.audit_story_glyph_consistency import load,save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.probe_escape_direct_source_v1186 import machine
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from scripts.build_registered_maria301_v1 import STAGED,STARTUP,GETTERS,PARENT,OUT,ARCHIVE
from scripts import verify_hodram_residual_startup_v1 as prior
from scripts.source_locked_derivation_v5118 import checked_text

CAPTURE = OUT/'own_startup_capture_v2/capture_report.json'


def main():
    assert not STARTUP.exists()
    staged,report,parent = map(load,[STAGED,CAPTURE,PARENT])
    plan_path = OUT/'own_startup_run_v1/run_plan.json'; plan = load(plan_path)
    assert digest(STAGED) == plan['staged_sha256'] and staged['own_registered_startup_pending']
    assert report['ROM_sha256'] == staged['candidate_sha256'] == digest(staged['candidate'])
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['frames'] == plan['frames'] == 31000 and staged['clean_input_patch_byte_exact']
    assert report['scripted_input_schedule'] == load(plan['inputs']) and digest(plan['inputs']) == plan['inputs_sha256']
    assert digest(plan['donor']) == plan['donor_sha256'] == report['battery_save_preloaded']['source_sha256']
    assert report['battery_save_preloaded']['copied_byte_exact_before_cold_boot']
    unlock = load(plan['fixture_manifest'])
    assert digest(plan['fixture_manifest']) == plan['fixture_manifest_sha256']
    assert unlock['only_system_low_four_bits_and_original_checksum_changed'] and unlock['all_six_route_save_slots_and_footer_unchanged']
    assert not unlock['earned_unlock_verified'] and unlock['production_ROM_sha256'] == staged['candidate_sha256']
    assert digest(PARENT) == staged['predecessor_release_sha256'] and digest(parent['candidate']) == staged['parent_sha256']
    image,parent_image = NdsImage.open(staged['candidate']),NdsImage.open(parent['candidate'])
    assert [p for _,p,v in parent_image.iter_files() if image.read_file(p) != v] == [ARCHIVE]
    assert all(image.read_file(p) == v for p,v in parent_image.iter_components())
    captures = {r['frame']:r for r in report['frames_captured']}
    assert {1600,2200,3340,4000,16000,31000} <= set(captures)
    selected = []
    for frame in [1600,2200,3340,4000,16000,31000]:
        cap = captures[frame];assert digest(cap['path']) == cap['PNG_sha256'] and cap['dimensions'] == [256,384]
        selected.append(cap)
    old_report_path = Path('work/Maria_current_context_20261109_v1/capture/capture_report.json')
    old = load(old_report_path); old_frames = {r['frame']:r for r in old['frames_captured']}
    assert old['scripted_input_schedule'] == report['scripted_input_schedule']
    reused = []
    for frame in [4000,16000,31000]:
        a,b = old_frames[frame],captures[frame]
        assert digest(a['path']) == a['PNG_sha256']
        assert Path(a['path']).read_bytes() == Path(b['path']).read_bytes(),('Changed startup frame requires investigation',frame)
        reused.append(dict(frame=frame,old_capture=a,new_capture=b,exact_previously_viewed_RGB=True))
    snapshot = report['read_only_RAM_snapshot'];raw = Path(snapshot['path']).read_bytes()
    assert snapshot['read_only_export'] and len(raw) == snapshot['bytes'] == 0x400000 and digest(snapshot['path']) == snapshot['sha256']
    arm,common = image.read_file('/__arm9__.bin'),image.read_file('/COMMON/MESFILE.DK4')
    sections = MainCodeFile(arm,BASE).sections;payload = bytes(sections[3].data[:-48])
    assert len(payload) == 123264 and raw[POOL-BASE:POOL-BASE+len(payload)] == payload
    assert raw[1435252:1435264] == b'Adernkatz\0\0\0' and raw[1435264:1435272] == b'Blades\0\0'
    owners = [*sections,SimpleNamespace(ramAddress=POOL,data=payload)]
    cpu,get,_ = machine(arm,common,raw,dict(patches=[]));executed = set()
    def exact(u,pc,size,_):
        matches = [s for s in owners if s.ramAddress <= pc and pc+size <= s.ramAddress+len(s.data)]
        assert len(matches) == 1,hex(pc)
        s = matches[0]
        assert bytes(u.mem_read(pc,size)) == bytes(s.data[pc-s.ramAddress:pc-s.ramAddress+size])
        executed.add(pc)
    hook = cpu.hook_add(UC_HOOK_CODE,exact);before = bytes(cpu.mem_read(BASE,0x400000))
    captain,actor_root = get(0x7F244),get(0xCB184)
    cpu.hook_del(hook)
    route = int.from_bytes(cpu.mem_read(ROUTE,4),'little')
    assert captain == route == 3 and bytes(cpu.mem_read(BASE,0x400000)) == before
    assert BASE <= actor_root < BASE+0x400000-0x1A04
    save(STARTUP,dict(candidate=staged['candidate'],candidate_sha256=staged['candidate_sha256'],profile=staged['profile'],
        cold_boot=True,savestate=False,frames=31000,callback_errors=0,
        actual_captain_getter=captain,actual_route_word=route,actual_actor_root=actor_root,read_only_snapshot=snapshot,
        native_getter_did_not_change_main_RAM=True,original_getter_instruction_addresses=len(executed),
        complete123264_staged_payload_andGerhard_next_Blades_exact=True,
        ARM9_COMMON_HELP_font_equal_registered_runtime_parent=True,
        ordinary_title_NewGame_Maria_opening_andHangzhou_observed=True,
        six_key_frames_directly_viewed=True,reviewed_captures=selected,
        three_opening_andtown_frames_exact_prior_RGB=reused,
        capture_report=str(CAPTURE),capture_report_sha256=digest(CAPTURE),
        existing_isolated_system_unlock_not_earned=True,no_savestate_story_RAM_orconditional_override=True,
        no_new_optional_scene_activation_orhardware_claim=True,
        evidence={str(p):digest(p) for p in [CAPTURE,plan_path,PARENT,old_report_path,Path(__file__)]},new_credit=0))
    staged.update(own_registered_startup_pending=False,own_registered_startup=str(STARTUP),own_registered_startup_sha256=digest(STARTUP))
    save(STAGED,staged)
    print('Own31,000-frame Maria coldboot passes: title/NewGame/opening/Hangzhou, captain3/route3, current payload andprotected data.')


getters_source = checked_text(prior.getters_source, {
    'captain=0': 'captain=3',
    'all12 protected names from the cumulative residual candidate own startup':
        'all12 protected names from the Maria301 cumulative candidate own startup',
})

if __name__ == '__main__':
    if sys.argv[1:] == ['--getters']:
        env = {**prior.env,**globals(),'__file__':__file__}
        exec(compile(getters_source,__file__+'::same-both-protected-getters-own-Maria-snapshot','exec'),env)
        env['verify_getters']()
    else:assert not sys.argv[1:];main()
