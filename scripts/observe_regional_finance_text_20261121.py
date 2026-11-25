"""Trace the regional finance format on the latest registered candidate."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from struct import unpack_from
import sys

from scripts import headless_desmume_v193 as harness
from scripts import observe_market_context_v2112 as native
from scripts import register_company_name_companion_scenes_20261121 as current
from scripts import reconcile_shared_display_20261121 as shared
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = Path("work/regional_finance_text_20261121_v2")
ORIGINAL = Path("work/emulation_v193/regional_missions_v617_actual/capture_report.json")
INPUTS = Path("work/analysis/regional_missions_v617/complete_V616_control_inputs.json")
FORMAT, RELEASE_PLANE = 0x02038DA8, 0x02038DB0
GETTER, COPIER = 0x0205528C, 0x020534F4
TRACED = (FORMAT, RELEASE_PLANE, GETTER, COPIER)
FOCUS = {100, 101, 102, 103, 108, 109, 110, 111, 113, 114, 115, 116, 117, 119, 124,
         284, 287, 300, 304, 318, 330, 331, 332, 333, 750, 751, 752}
FRAMES = (3400, 4400, 5000, 6000, 7000, 7800, 9800, 10200, 10600, 11800)
CHECKPOINT = shared.OUTPUT.with_name("shared_priority_and_regional_finance_20261121_v1.json")


def trace_class(folder):
    namespace = vars(native) | dict(ROOT=folder, ROM=current.ROM, TRACED=TRACED,
        FORMAT=FORMAT, RELEASE_PLANE=RELEASE_PLANE, GETTER=GETTER, COPIER=COPIER, FOCUS=FOCUS)
    setup = checked_text(getsource(native.prepare_contract), {'for pc in(REQUEST,FONT):': 'for pc in TRACED:'})
    exec(compile(setup, __file__ + "::trace_contract", "exec"), namespace)
    namespace["prepare_contract"]()
    original = getsource(native.Observer)
    start = original.index('    if frame<31000:return')
    end = original.index('   except BaseException as exc:', start)
    data = '''    if pc in (GETTER,COPIER):
     number=v[4] if pc==GETTER else v[5]
     self.slots_seen[pc]=self.slots_seen.get(pc,0)+1
     if number in FOCUS:self.requests.append(dict(frame=frame,PC=pc,ID=number,caller=v[18]))
     return
    row=dict(frame=frame,PC=pc,LR=v[18],destination=v[4])
    if pc==FORMAT:
     addr=v[5];assert 0x02000000<=addr<0x023fff80
     raw=ct.string_at(self.wram+addr-0x02000000,128).split(b'\\0')[0]
     third,=struct.unpack('<I',ct.string_at(self.wram+v[17]-0x02000000,4))
     row.update(pointer=addr,format_hex=raw.hex(),unsigned_arguments=[v[6],v[7],third])
    self.rows.append(row)
'''
    source = (original[:start] + data + original[end:]).replace('  def callback(frame):',
        '  self.slots_seen={}\n  def callback(frame):')
    exec(compile(source, __file__ + "::observer", "exec"), namespace)
    return namespace["Observer"]


def main():
    base = current.base
    release = base.load(current.RELEASE)
    assert base.digest(current.ROM) == release["candidate_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert not ROOT.exists()
    prior = base.load(ORIGINAL)
    save = prior["battery_save_preloaded"]
    assert base.digest(save["source"]) == save["source_sha256"]
    assert [event for event in prior["scripted_input_schedule"] if event["start"] <= FRAMES[-1]] == base.load(INPUTS)
    observe = trace_class(ROOT / "observer")
    hooks = []
    original = harness.ct

    class Loader:
        def __getattr__(self, name):
            return getattr(original, name)

        def CDLL(self, path, *args, **kwargs):
            core = original.CDLL(path, *args, **kwargs)
            if str(path).lower().endswith("desmume_libretro.dll"):
                hook = observe(core, ROOT / "observer")
                hook.install()
                hooks.append(hook)
                tick = core.retro_run

                def advance():
                    hook.header[0] += 1
                    return tick()

                core.retro_run = advance
            return core

    argv = [harness.__file__, "--rom", str(current.ROM), "--out", str(ROOT / "capture"),
        "--battery-save", save["source"], "--touchscreen", "--inputs-json", str(INPUTS),
        "--frames", "11801", "--capture-every", "999999", "--capture-at", *map(str, FRAMES)]
    previous = sys.argv
    try:
        sys.argv = argv
        harness.ct = Loader()
        harness.main()
    finally:
        sys.argv = previous
        harness.ct = original
        for hook in hooks:
            hook.close()
            hook.save()
    report_path = ROOT / "capture/capture_report.json"
    report = base.load(report_path)
    assert report["ROM_sha256"] == release["candidate_sha256"] and report["cold_boot"]
    assert not report["savestate_loaded"] and not report["callback_errors"] and report["frames"] == 11801
    hook, = hooks
    original_digest = base.digest(save["source"])
    assert original_digest == save["source_sha256"]
    arm = base.NdsImage.open(current.ROM).read_file(current.native.ARM)
    assert unpack_from("<I", arm, 0x38E00) == (0x02137118,)
    base.save(ROOT / "playback.json", dict(candidate_sha256=release["candidate_sha256"],
        format_calls=[row for row in hook.rows if row["PC"] == FORMAT],
        compositor_release_calls=[row for row in hook.rows if row["PC"] == RELEASE_PLANE],
        shared_requests_by_entry=hook.slots_seen, pending_shared_requests=hook.requests,
        traceable_calls=[hex(pc) for pc in TRACED], original_fixture_sha256=original_digest,
        report=str(report_path), report_sha256=base.digest(report_path)))


def checkpoint():
    base, native = current.base, current.native
    release, ledger, worklist = map(base.load, (current.RELEASE, base.LEDGER, shared.OUTPUT))
    candidate = release["candidate_sha256"]
    assert candidate == base.digest(current.ROM) == ledger["current_integrated_candidate"]["sha256"]
    assert base.digest(native.CLEAN) == release["clean_input_sha256"] == worklist["clean_sha256"]
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    clean, active = map(base.NdsImage.open, (native.CLEAN, current.ROM))
    arm_before, arm_after = (image.read_file(native.ARM) for image in (clean, active))
    assert native.digest(arm_after) == release["target_ARM9_sha256"]
    assert native.digest(active.read_file(shared.COMMON)) == release["target_COMMON_sha256"]
    originals = shared.workflow.common_message_entries(clean.read_file(shared.COMMON), arm_before)
    installed = shared.entries(active)
    clean_files = {path: raw for path, raw in native.files(clean).items() if path != shared.COMMON}
    priority_ids = set(worklist["first_investigation_list"])
    priority = []
    for row in worklist["records"]:
        key = row["message_ID"]
        assert originals[key].text.hex() == row["source_hex"] and installed[key].text.hex() == row["current_hex"]
        assert shared.workflow.reference(originals[key]) == row["source_reference"]
        assert shared.workflow.reference(installed[key]) == row["current_reference"]
        if key not in priority_ids:
            continue
        source_bytes = originals[key].text
        assert all(source_bytes not in raw and source_bytes.replace(b"\n", b"") not in raw
                   for raw in clean_files.values())
        priority.append({k: row[k] for k in ("message_ID", "source_reference", "current_reference", "source_hex", "current_hex")})
    assert len(priority) == len(priority_ids) == 35

    playback_path = ROOT / "playback.json"
    trace = base.load(playback_path)
    assert trace["candidate_sha256"] == candidate and base.digest(trace["report"]) == trace["report_sha256"]
    assert not any(trace[k] for k in ("format_calls", "compositor_release_calls", "pending_shared_requests"))
    assert all(trace["shared_requests_by_entry"][str(pc)] > 0 for pc in (GETTER, COPIER))
    evidence = base.load(trace["report"])
    at = next(p for p in evidence["frames_captured"] if p["frame"] == 11800)["path"]
    finance = '収入額%8lu支出額%8lu投資額%8lu'.encode('cp932') + b'\0'
    cluster_source, cluster_current = 'など'.encode('cp932'), b' etc.'
    assert all(arm[0x137118:0x137118+len(finance)] == finance for arm in (arm_before, arm_after))
    assert all(unpack_from("<I", arm, 0x38E00) == (0x02137118,) for arm in (arm_before, arm_after))
    assert arm_before[0x14C0E4:0x14C0EC] == cluster_source.ljust(8, b"\0")
    assert arm_after[0x14C0E4:0x14C0EC] == cluster_current.ljust(8, b"\0")
    assert all(unpack_from("<4I", arm, 0x8BEA8) == (0x0214C0E4, 0x0214C0EC, 0x022A44EC, 0x0214C0F0)
               for arm in (arm_before, arm_after))
    assert not CHECKPOINT.exists()
    base.save(CHECKPOINT, dict(candidate_sha256=candidate, clean_sha256=release["clean_input_sha256"],
        worklist=str(shared.OUTPUT), worklist_sha256=base.digest(shared.OUTPUT), rebound_shared_records=len(worklist["records"]),
        exact_string_variant_search=dict(clean_components_outside_COMMON=len(clean_files),
            variants=["verbatim CP932 bytes", "literal newlines removed"], records=priority,
            scope="Exact on-disk string matches. The scan does not exclude paraphrases, compressed resources, or runtime callers."),
        ordinary_regional_replay=dict(region="Stockholm", displayed_fleet="Manuel Fleet", controls="World Map and existing regional fleet",
            copied_existing_save=True, hardware=False, finance_format_calls=0, observed=["Income", "Expenses", "Invested", "Mission", "Manuel Fleet etc."],
            view_frame=dict(path=at, sha256=base.digest(at)), source_trace=str(playback_path), source_trace_sha256=base.digest(playback_path)),
        separate_finance_format=dict(ARM9_offset=0x137118, clean_and_installed_hex=finance.hex(), pointer_literal=0x02038E00,
            original_format_call=FORMAT, note="The sampled World Map panel displays its plaques and numbers through an independent path."),
        clustered_marker=dict(ARM9_offset=0x14C0E4, pointer_literal=0x0208BEA8, source_hex=cluster_source.hex(),
            installed_hex=cluster_current.hex(), maximum_bytes_including_NUL=8, next_owned_empty_string=0x0214C0EC,
            proposed_english=" + more", meaning="The named marker represents additional entities at the same point.",
            finding="The existing suffix reads as throwaway prose in a map label. A short plus label signals that more entries share the marker."),
        actual_new_visual_pages=1, new_editorial_credit=0, open_display_references=276, full_goal_complete=False))
    print("Bound 35 priority references and the observed World Map tooltip to the current release.")


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("--checkpoint", action="store_true")
    checkpoint() if parser.parse_args().checkpoint else main()
