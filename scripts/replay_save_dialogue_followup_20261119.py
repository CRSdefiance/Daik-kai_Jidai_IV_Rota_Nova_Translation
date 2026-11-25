"""Exercise the installed save prompt and the native cartridge-error dialog in an isolated replay."""

from argparse import ArgumentParser
import json
from pathlib import Path
from struct import pack, unpack_from
import sys
from types import FunctionType

from dk4tool.rom.nds import NdsImage
from scripts import replay_mutiny_dialogue_followup_20261119 as prior
from scripts import replay_sea_event_dialogue_followup_20261118 as startup_workflow
from scripts import stage_save_dialogue_followup_20261119 as stage
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands

base = stage.base
OUT = stage.ROOT / "occupied_slot_v2"
STARTUP = stage.ROOT / "startup_fixture"
REFERENCE = Path("work/emulation_v193/save_load_plaques_v612_current/capture_report.json")
HARNESS = Path("scripts/headless_desmume_v193.py")
PAUSE = 6600
FIELD = 0x020EEB2C
RENDER_FRAME = 7000


def patch():
    FunctionType(prior.patch.__code__, vars(prior) | dict(stage=stage))()


def startup():
    run = FunctionType(startup_workflow.startup.__code__, vars(startup_workflow) | dict(stage=stage, STARTUP=STARTUP))
    run()


def set_condition(arm, raw, request):
    assert arm == NdsImage.open(stage.ROM).read_file(stage.ARM) and len(raw) == 0x400000
    offset = FIELD - stage.BASE
    clean = NdsImage.open(stage.CLEAN).read_file(stage.ARM)
    assert arm[offset-12:offset+40] == clean[offset-12:offset+40]
    old = clean[offset:offset+4]
    word, = unpack_from("<I", old)
    destination = FIELD + 8 + 4 * (((word & 0xFFFFFF) ^ 0x800000) - 0x800000)
    assert word >> 24 == 0xEB and destination == 0x020D63A4
    failed = pack("<I", 0xE3A00000)
    mode = request["mode"]
    assert request == {"mode": mode} and mode in ("write-return-zero", "restore-write")
    before, after = (old, failed) if mode == "write-return-zero" else (failed, old)
    assert raw[offset:offset+4] == before
    updated = raw[:offset] + after + raw[offset+4:]
    return updated, dict(mode=mode, instruction=FIELD, original_write=destination,
        before=before.hex(), after=after.hex(), return_zero_only=True,
        changes=[dict(address=FIELD+i, before=a, after=b)
            for i,(a,b) in enumerate(zip(before, after, strict=True)) if a != b])


def gameplay():
    assert not OUT.exists()
    reference = base.load(REFERENCE)
    donor = reference["battery_save_preloaded"]
    assert base.digest(donor["source"]) == donor["source_sha256"]
    assert reference["cold_boot"] and not reference["savestate_loaded"] and not reference["callback_errors"]
    assert not any(value for key,value in reference.items() if key.startswith("synthetic_"))
    prefix = [row for row in reference["scripted_input_schedule"] if row["start"] < PAUSE]
    assert prefix[-1] == dict(start=6201, duration=8, buttons=["B"])
    prefix[-1] = prefix[-1] | {"buttons": ["A"]}
    OUT.mkdir()
    inputs, commands = OUT / "inputs.json", OUT / "commands.jsonl"
    base.save(inputs, prefix)
    schedule = [
        dict(until=RENDER_FRAME, condition_fixture=dict(mode="write-return-zero"), buttons=["A"], duration=8),
        dict(until=7200, condition_fixture=dict(mode="restore-write")),
        dict(stop=True),
    ]
    commands.write_text("".join(json.dumps(row) + "\n" for row in schedule), encoding="utf-8")
    code = HARNESS.read_text(encoding="utf-8")
    token = "from scripts.native_condition_fixture_v520 import set_condition"
    assert code.count(token) == 1
    code = code.replace(token, "from scripts.replay_save_dialogue_followup_20261119 import set_condition")
    previous, stdin = sys.argv, sys.stdin
    args = ["--rom", str(stage.ROM), "--out", str(OUT / "capture"), "--frames", "7400",
        "--inputs-json", str(inputs), "--battery-save", donor["source"], "--touchscreen", "--capture-every", "999999",
        "--capture-at", "5800", "6200", "--pause-at", str(PAUSE), "--dump-pause-ram", "--dump-ram",
        "--allow-condition-fixtures"]
    stream = GrowingCommands(commands)
    try:
        sys.argv, sys.stdin = [str(HARNESS), *args], stream
        exec(compile(code, str(HARNESS), "exec"), {"__name__": "__main__", "__file__": str(HARNESS.resolve())})
    finally:
        sys.argv, sys.stdin = previous, stdin
        stream.close()
    assert base.digest(donor["source"]) == donor["source_sha256"]
    path = OUT / "capture" / "capture_report.json"
    base.save(OUT / "terminal.json", dict(report=str(path), report_sha256=base.digest(path),
        commands=str(commands), commands_sha256=base.digest(commands),
        candidate_sha256=base.digest(stage.ROM), donor_sha256=donor["source_sha256"], donor_unchanged=True))


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("action", choices=("patch", "startup", "gameplay"))
    globals()[cli.parse_args().action]()

