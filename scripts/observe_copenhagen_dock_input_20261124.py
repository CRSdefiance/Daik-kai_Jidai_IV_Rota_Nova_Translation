"""Observe the port value at the accepted dock prompt on the registered Lisbon ROM."""

from inspect import getsource

from PIL import ImageChops

from scripts import observe_copenhagen_docking_20261124 as original
from scripts import register_lisbon_roster_galley_20261124 as current
from scripts import verify_copenhagen_docking_20261124 as baseline
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import REGISTRY, digest, read, reference, write


ROOT = current.build.ROOT.with_name("editorial_20261124_copenhagen_dock_input")
RUN = ROOT / "landing"
OUT = baseline.OUT.with_name("copenhagen_dock_request_input_20261124.json")
playback = original.playback
RETURN, PENDING, ACCEPT, DOCK = 0x02021DE4, 0x02090B8C, 0x020908EC, original.NATIVE_DOCK_STORE
VALUES = {RETURN: 5, PENDING: 5, ACCEPT: 5, DOCK: 9}


def observer(rom, folder):
    cooked = checked_text(getsource(playback.observer), {
        "    ptr=v[6]\n": """    if pc in VALUES:
     self.rows.append(dict(frame=frame,PC=pc,LR=v[18],value=v[VALUES[pc]], R0=v[4],R4=v[8],R6=v[10]))
     return
    ptr=v[6]
""",
        "REQUESTS=REQUESTS, ONLINE=ONLINE, GALLERY=GALLERY)":
            "REQUESTS=REQUESTS, ONLINE=ONLINE, GALLERY=GALLERY, VALUES=VALUES, __file__=__file__)",
    })
    scope = vars(playback) | dict(TARGETS=(*playback.REQUESTS, *VALUES), VALUES=VALUES, __file__=__file__)
    exec(compile(cooked, __file__ + "::read-docking-arguments", "exec"), scope)
    return scope["observer"](rom, folder)


def run():
    assert digest(REGISTRY) == read(current.RELEASE)["registry_sha256"]
    cooked = checked_text(getsource(playback.main), {
        "'--capture-at', *map(str, frames)]": "'--dump-capture-ram', '--capture-at', *map(str, frames)]",
    })
    scope = vars(playback) | dict(ROOT=ROOT, parent=current, get_schedule=original.schedule,
                                 observer=observer, FOCUS={49, 65}, __file__=__file__)
    exec(compile(cooked, __file__ + "::ordinary-copenhagen-input", "exec"), scope)
    scope["main"]("landing")


def verify():
    old = read(baseline.OUT)
    old_report_path = original.ROOT / "landing/capture/capture_report.json"
    report_path = RUN / "capture/capture_report.json"
    requests_path = RUN / "requests.json"
    old_report, report, requests = map(read, (old_report_path, report_path, requests_path))
    release = read(current.RELEASE)
    assert old["candidate_sha256"] == old_report["ROM_sha256"]
    assert report["ROM_sha256"] == release["candidate_sha256"] == digest(current.ROM)
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert not any(value for key, value in report.items() if key.startswith("synthetic_"))
    assert not requests["errors"] and not requests["mismatches"] and requests["all_host_slots_restored_and_core_file_exact"]
    events, frames, end, _, donor = original.schedule("landing")
    assert report["frames"] == end and report["scripted_input_schedule"] == events == old_report["scripted_input_schedule"]
    assert report["battery_save_preloaded"]["source_sha256"] == donor["source_sha256"] == digest(donor["source"])
    images = [{row["frame"]: row for row in data["frames_captured"] if row["path"].endswith("_cold_boot.png")}
              for data in (old_report, report)]
    for frame in frames:
        a, b = (baseline.panels.picture(group[frame]) for group in images)
        assert ImageChops.difference(a, b).getbbox() is None, frame
    fleet = old["player_accepted_approach_store"]["fleet"]
    dock, = [row for row in requests["rows"] if row["PC"] == DOCK and row["R6"] == fleet]
    assert dock["value"] == 9
    accept, = [row for row in requests["rows"] if row["PC"] == ACCEPT and row["R0"] == fleet]
    assert accept["value"] == dock["value"] and accept["frame"] <= dock["frame"]
    pending = [row for row in requests["rows"] if row["PC"] in (RETURN, PENDING) and
               3200 <= row["frame"] <= accept["frame"]]
    received = [row for row in pending if row["PC"] == RETURN and row["value"] == accept["value"]]
    staged = [row for row in pending if row["PC"] == PENDING and row["value"] == accept["value"]]
    assert received and staged and received[-1]["frame"] <= staged[-1]["frame"]
    write(OUT, dict(
        candidate_sha256=release["candidate_sha256"], ordinary_controllers=True, original_battery_save=reference(donor["source"]),
        original_playback=reference(baseline.OUT), current_capture=reference(report_path), native_trace=reference(requests_path),
        matching_gameplay_holds=list(frames), native_return=received[-1], internal_pending_store=staged[-1],
        accepted_port=accept, written_dock=dock, ordinary_port_slot=9,
        observed_Missionary=False, new_editorial_credit=0,
    ))
    print(f"Copenhagen slot 9 carried through all four native boundaries. {len(frames)} gameplay holds matched.")


if __name__ == "__main__":
    import sys

    actions = {"run": run, "verify": verify}
    actions[sys.argv[1]]()
