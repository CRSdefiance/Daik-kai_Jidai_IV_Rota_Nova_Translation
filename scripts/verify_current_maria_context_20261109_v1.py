"""Bind a fresh current-ROM Maria snapshot; do not infer changed-batch gameplay coverage."""
from pathlib import Path
from scripts.audit_story_glyph_consistency import load, save
from scripts.finish_rafael_B261_B280_native_pages_v1 import digest
from scripts.probe_escape_direct_source_v1186 import machine
from scripts.registered_editorial_runtime_v2 import RegisteredRuntime
from dk4tool.rom.nds import NdsImage
from dk4tool.patch.main_pool_cache_visibility import BASE, POOL
from ndspy.code import MainCodeFile

ROOT = Path('work/Maria_current_context_20261109_v1')


def main():
    out = ROOT / 'own_maria_startup_verification.json'
    assert not out.exists()
    plan_path = ROOT / 'run_plan.json'
    plan = load(plan_path)
    report_path = ROOT / 'capture/capture_report.json'
    report = load(report_path)
    assert report['ROM_sha256'] == plan['candidate_sha256'] == digest(plan['candidate'])
    assert report['cold_boot'] and not report['savestate_loaded'] and not report['callback_errors']
    assert report['frames'] == plan['frames'] == 31000
    assert digest(plan['donor']) == plan['donor_sha256']
    snapshot = report['read_only_RAM_snapshot']
    raw = Path(snapshot['path']).read_bytes()
    assert snapshot['read_only_export'] and len(raw) == 0x400000 and digest(snapshot['path']) == snapshot['sha256']
    image = NdsImage.open(plan['candidate'])
    arm, common = [image.read_file(p) for p in ['/__arm9__.bin', '/COMMON/MESFILE.DK4']]
    sections = MainCodeFile(arm, BASE).sections
    payload = bytes(sections[3].data[:-48])
    assert len(payload) == 123264 and raw[POOL-BASE:POOL-BASE+len(payload)] == payload
    cpu, get, _ = machine(arm, common, raw, dict(patches=[]))
    captain = get(0x7F244)
    assert captain == 3
    save(out, dict(candidate=plan['candidate'], candidate_sha256=plan['candidate_sha256'],
        cold_boot=True, savestate=False, frames=31000, actual_captain_getter=captain,
        read_only_snapshot=snapshot, complete_current_staged_payload_exact=True,
        initialized_Maria_context_not_Rafael_overlay=True,
        existing_isolated_system_unlock_only_not_earned=True,
        original_donor_unchanged=True, no_changed_Maria_batch_gameplay_approval=True,
        no_new_formatted_page_visual_approval=True, hardware_verified=False,
        evidence={str(p): digest(p) for p in [plan_path, report_path, Path(__file__)]}, new_credit=0))
    ctx = RegisteredRuntime('work/hodram_residual_release_v1/registered_release_verification.json', out, captain=3)
    own, own_get, _ = ctx.machine(ctx.arm, ctx.common, ctx.raw, ctx.plan)
    assert own_get(0x7F244) == 3
    assert bytes(own.mem_read(ctx.actor_root, 0x1A04)) == ctx.actor_bytes
    ctx.calls.clear()
    save(ROOT / 'runtime_context_qualification.json', dict(runtime=ctx.receipt(),
        current_ROM_andown_snapshot_exact=True, actual_captain_getter=3,
        all301_clean_first_drafts_precede_current_English_intake=True,
        original_machine_andregistered_runtime_guards_pass=True,
        no_changed_batch_editorial_formatting_gameplay_orcompletion_credit=True,
        evidence={str(out): digest(out), str(Path(__file__)): digest(__file__)}, new_credit=0))
    print('Current-ROM Maria context passes:31,000 frames, captain3, exact staged payload, own actor state;zero batch gameplay/credit.')


if __name__ == '__main__':
    main()
