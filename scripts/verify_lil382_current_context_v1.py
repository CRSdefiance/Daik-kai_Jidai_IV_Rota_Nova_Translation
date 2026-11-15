"""Verify the exact-ROM snapshot and unmodified native captain/route getters for Lil."""
from types import SimpleNamespace
from pathlib import Path
from ndspy.code import MainCodeFile
from unicorn import UC_HOOK_CODE
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from dk4tool.patch.reviewed_name_catalog import ROUTE
from dk4tool.rom.nds import NdsImage
from scripts.probe_escape_direct_source_v1186 import machine
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.prepare_lil382_current_context_v1 import ROOT, RELEASE, PRIOR
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime


def main():
    out = ROOT/'own_Lil_startup_verification.json'
    assert not out.exists()
    planpath = ROOT/'run_plan.json'
    reportpath = ROOT/'capture/capture_report.json'
    plan, report, release = map(load, [planpath, reportpath, RELEASE])
    assert digest(RELEASE) == plan['registered_release_sha256']
    assert report['ROM_sha256'] == plan['candidate_sha256'] == release['candidate_sha256'] == digest(release['candidate'])
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['frames'] == plan['frames'] == 4001
    assert not report.get('battery_save_preloaded') and not any(v for k, v in report.items() if k.startswith('synthetic_'))
    assert report['scripted_input_schedule'] == load(plan['inputs'])
    assert digest(plan['inputs']) == plan['inputs_sha256']
    snapshot = report['read_only_RAM_snapshot']
    raw = Path(snapshot['path']).read_bytes()
    assert snapshot['read_only_export'] and len(raw) == 4194304 and digest(snapshot['path']) == snapshot['sha256']
    image = NdsImage.open(release['candidate'])
    arm, common = image.read_file('/__arm9__.bin'), image.read_file('/COMMON/MESFILE.DK4')
    sections = MainCodeFile(arm, BASE).sections
    payload = bytes(sections[3].data[:-48])
    assert len(sections) == 6 and len(payload) == 123264 and raw[POOL-BASE:POOL-BASE+len(payload)] == payload
    owners = [*sections, SimpleNamespace(ramAddress=POOL, data=payload)]
    cpu, get, _ = machine(arm, common, raw, dict(patches=[]))
    before = bytes(cpu.mem_read(BASE, 4194304))
    executed = set()
    def exact(u, pc, size, unused):
        matches = [s for s in owners if s.ramAddress <= pc and pc+size <= s.ramAddress+len(s.data)]
        assert len(matches) == 1
        section = matches[0]
        assert bytes(u.mem_read(pc, size)) == bytes(section.data[pc-section.ramAddress:pc-section.ramAddress+size])
        executed.add(pc)
    hook = cpu.hook_add(UC_HOOK_CODE, exact)
    captain, root = get(0x7F244), get(0xCB184)
    cpu.hook_del(hook)
    route = int.from_bytes(cpu.mem_read(ROUTE, 4), 'little')
    assert captain == route == 2 and BASE <= root < BASE+4194304-0x1A04
    assert bytes(cpu.mem_read(BASE, 4194304)) == before
    captures = {c['frame']: c for c in report['frames_captured']}
    assert {180, 2000, 4000, 4001} <= set(captures)
    for frame in [180, 2000, 4000, 4001]:
        assert digest(captures[frame]['path']) == captures[frame]['PNG_sha256']
    save(out, dict(candidate=release['candidate'], candidate_sha256=release['candidate_sha256'],
        cold_boot=True, savestate=False, frames=4001, actual_captain_getter=captain, actual_route_word=route,
        actual_actor_root=root, read_only_snapshot=snapshot, no_historical_initialized_RAM_oroverlay=True,
        complete123264_current_staged_payload_exact=True, current_getters_leave_complete_host_setup_RAM_exact=True,
        original_getter_instruction_addresses=len(executed), no_battery_savestate_observer_orconditional_override=True,
        current_context_not_new_optional_scene_orhardware_coverage=True, direct_visual_review_pending=True,
        report=str(reportpath), report_sha256=digest(reportpath),
        evidence={str(p): digest(p) for p in [RELEASE, planpath, reportpath, PRIOR, Path(__file__)]}, new_credit=0))
    ctx = RegisteredRuntime(RELEASE, out, captain=2)
    save(ROOT/'registered_native_context.json', ctx.receipt())
    print('PASS fresh own-ROM Lil captain2/route2,4001frames,complete current payload andnative runtime guards.')


if __name__ == '__main__':
    main()
