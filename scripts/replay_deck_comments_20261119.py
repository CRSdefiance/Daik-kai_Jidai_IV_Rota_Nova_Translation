"""Run the candidate's own startup and a bounded Shipwright replay."""

from argparse import ArgumentParser
from inspect import getsource
import json
from pathlib import Path
from shutil import copy2
import subprocess
import sys
from types import FunctionType

from PIL import Image

from scripts import native_work_room_fixture_v846 as fixture
from scripts import replay_sea_hazard_dialogue_20261119 as boot_replay
from scripts import run_work_room_adapter_v846 as adapter
from scripts import stage_deck_comments_20261119 as stage
from scripts import verify_setup_save_equipment_v1 as boot_audit
from scripts.finish_refit_display_v712 import load as load_capture
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.verify_personal_gameplay_v841 import hold, model_state

base = stage.base
STARTUP = stage.ROOT / "own_startup"
STARTUP_PROOF = stage.ROOT / "own_startup_verification.json"
CAPTURE = stage.ROOT / "shipwright_capture"
PLAYBACK = stage.ROOT / "shipwright_verification.json"
HISTORY = Path("work/analysis/work_comments_v846/845_GerhardShipwright_scheduled_run_plan.json")
ORIGINAL_PLAYBACK = Path("work/analysis/work_comments_v846/actual_gameplay_verification.json")
CASE = "GerhardShipwright"


def startup():
    run = boot_replay.previous.startup
    FunctionType(run.__code__, run.__globals__ | {"stage": stage, "STARTUP": STARTUP})()
    previous = base.load(stage.parent.RELEASE)
    basis = base.load(STARTUP / "basis.json")
    assert base.digest(basis["previous_report"]) == basis["previous_report_sha256"]
    assert base.digest(basis["manifest"]) == basis["manifest_sha256"]
    proof = checked_text(getsource(boot_audit.verify_startup), {
        "ROOT / 'own_startup/capture/capture_report.json'": "REPORT",
        "BIOGRAPHIES / 'own_startup/capture/capture_report.json'": "PRIOR_REPORT",
        "    term = load(ROOT / 'own_startup/terminal.json')\n"
        "    assert term['candidate_sha256'] == digest(ROM) and term['report_sha256'] == digest(path)\n": "",
        "proof['registered_input']['candidate_sha256']": "proof['parent_sha256']",
        "BIOGRAPHIES / 'own_startup_verification.json'": "PRIOR_BOOT",
    })
    scope = vars(boot_audit) | dict(ROM=stage.ROM, PROOF=stage.PROOF, BOOT=STARTUP_PROOF,
        REPORT=STARTUP / "capture/capture_report.json", PRIOR_REPORT=Path(basis["previous_report"]),
        PRIOR_BOOT=Path(previous["own_registered_startup"]), __file__=__file__)
    exec(compile(proof, __file__ + "::startup", "exec"), scope)
    scope["verify_startup"]()


def assign(arm, raw, request):
    assert request == CASE
    current = base.load(stage.PROOF)
    assert stage.native.digest(arm) == current["target_ARM9_sha256"]
    # Keep the original selector and model assertions. Rebind the allocation
    # hash to the exact research ROM just staged from the registered parent.
    code = checked_text(getsource(fixture.assign), {
        "    config=read('translations/work_comments_editorial_release_v1.json')\n"
        "    assert sha(arm) in (config['source_arm9_sha256'],config['target_arm9_sha256'])\n": "",
    })
    scope = vars(fixture) | {"__file__": __file__}
    exec(compile(code, __file__ + "::room_fixture", "exec"), scope)
    return scope["assign"](arm, raw, request)


def worker():
    old = getsource(adapter.main)
    code = checked_text(old, {
        "from scripts.native_work_room_fixture_v846 import assign as assign_missionary":
            "from scripts.replay_deck_comments_20261119 import assign as assign_missionary",
    })
    scope = vars(adapter) | {"__file__": __file__}
    exec(compile(code, __file__ + "::replay_adapter", "exec"), scope)
    sys.argv = sys.argv[1:]
    scope["main"]()


def gameplay():
    plan = base.load(HISTORY)
    old = base.load(ORIGINAL_PLAYBACK)["terminal_capture_receipts"][CASE]
    assert base.digest(old["report"]) == old["sha256"]
    old_folder = Path(plan["folder"])
    assert old_folder / "capture_report.json" == Path(old["report"])
    journal = old_folder / "navigation_command_journal.json"
    script = base.load(journal)
    assert script["ROM_sha256"] == plan["ROM_sha256"]
    assert script["last_command_frame"] == 4800
    commands = script["commands_received"]
    assert len(commands) == 9 and all(c["validation_passed"] for c in commands)
    assert commands[0]["command"] == {"until": 3400, "work_room_fixture": CASE}
    source = Path(plan["source_donor"])
    inputs = Path(plan["inputs"])
    assert base.digest(source) == plan["source_donor_sha256"]
    assert base.digest(inputs) == plan["inputs_sha256"]
    donor = stage.ROOT / "disposable_shipwright.dsv"
    assert not CAPTURE.exists() and not donor.exists()
    copy2(source, donor)
    args = ["--rom", str(stage.ROM), "--out", str(CAPTURE), "--battery-save", str(donor), "--inputs-json", str(inputs),
        "--touchscreen", "--frames", "4801", "--capture-every", "999999", "--capture-at", "1", "60", "180", "3200",
        "--dump-capture-ram", "--dump-pause-ram", "--dump-ram", "--pause-at", "3200", "--allow-work-room-fixtures"]
    command_stream = "".join(json.dumps(c["command"]) + "\n" for c in commands)
    subprocess.run([sys.executable, "-m", "scripts.replay_deck_comments_20261119", "worker", *args],
        input=command_stream, text=True, check=True)
    assert base.digest(source) == base.digest(donor) == plan["source_donor_sha256"]
    verify_gameplay(old_folder, journal, commands, source, inputs)


def verify_gameplay(old_folder, journal, commands, source, inputs):
    digest = base.digest(stage.ROM)
    report, shots, receipt = load_capture(CAPTURE, digest, 4800)
    new_journal = CAPTURE / "navigation_command_journal.json"
    assert base.load(new_journal)["commands_received"] == commands
    ram = {}
    for item in report["read_only_pause_RAM_snapshots"] + report["read_only_capture_RAM_snapshots"]:
        raw = Path(item["path"]).read_bytes()
        assert item["read_only_export"] and len(raw) == 0x400000 and stage.native.digest(raw) == item["sha256"]
        assert ram.setdefault(item["frame"], raw) == raw
    fixture_proof, = report["synthetic_work_room_occupant_fixtures"]
    assert fixture_proof["frame"] == 3200 and fixture_proof["case"] == CASE
    assert len(fixture_proof["changes"]) in (2, 3)
    assert report["controlled_work_room_adapter"]["original_harness_file_unchanged"]
    assert not any(v for k, v in report.items() if k.startswith("synthetic_") and k != "synthetic_work_room_occupant_fixtures")
    rom = base.NdsImage.open(stage.ROM)
    arm = rom.read_file(stage.ARM)
    result, replay = assign(arm, ram[3200], CASE)
    assert replay == {k: v for k, v in fixture_proof.items() if k != "frame"}
    assert stage.native.digest(result) == fixture_proof["after_RAM_sha256"]
    row, = (r for r in base.load(stage.PROOF)["records"] if r["message_ID"] == 1387)
    r = dict(row, message_id=1387, actor_ID=16)
    check = FunctionType(hold.__code__, hold.__globals__ | {
        "layout": stage.native_lines, "expected_pixels": stage.current_pixels,
    })
    holds = [check(rom, ram[frame], shots[frame], r, 12) | {"capture_frame": frame} for frame in (4200, 4400)]
    assert all(item["source_role_type"] == 13 and item["original_parent_activity_state"] == 0 for item in holds)
    assert model_state(arm, ram[3400]) == model_state(arm, ram[4800])
    assert shots[3400].tobytes() == shots[4800].tobytes()

    previous, old_shots, _ = load_capture(old_folder, base.load(HISTORY)["ROM_sha256"], 4800)
    assert old_shots[4200].tobytes() != shots[4200].tobytes()
    assert previous["scripted_input_schedule"] == report["scripted_input_schedule"]
    sheet = stage.ROOT / "verified_shipwright_and_return.png"
    canvas = Image.new("RGB", (768, 384))
    for i, frame in enumerate((4200, 4400, 4800)):
        canvas.paste(shots[frame], (i * 256, 0))
    canvas.save(sheet)
    base.save(PLAYBACK, dict(candidate_sha256=digest, report=receipt, complete_holds=holds,
        normal_return_frame=4800, original_room_fixture=fixture_proof, original_and_current_schedule_exact=True,
        natural_activation=False, hardware=False, sheets=[dict(path=str(sheet), sha256=base.digest(sheet))],
        evidence={str(p): base.digest(p) for p in (CAPTURE / "capture_report.json", new_journal, journal, source, inputs, sheet)}))
    print("Verified two complete revised Shipwright holds and the original return to Copenhagen.", flush=True)


if __name__ == "__main__":
    if sys.argv[1:2] == ["worker"]:
        worker()
    else:
        parser = ArgumentParser(description=__doc__)
        parser.add_argument("action", choices=("startup", "gameplay"))
        globals()[parser.parse_args().action]()
