"""Replay the original fleet events with exact, disclosed selector inputs."""

from argparse import ArgumentParser
from inspect import getsource
import json
from pathlib import Path
import sys
from types import SimpleNamespace

from scripts import headless_desmume_v193 as emulator
from scripts import native_condition_fixture_v520 as fixture_adapter
from scripts import replay_sailing_hazards_and_dolphins_v1 as dolphin
from scripts import replay_sailing_reactions_v1 as reactions
from scripts import run_sea_event_bubbles_focused_v2 as earlier
from scripts import stage_fleet_encounter_dialogue_20261119 as build
from scripts.run_battle_cooking_livestock_live_v911 import GrowingCommands
from scripts.source_locked_derivation_v5118 import checked_text

base = build.base
ROOT = build.ROOT / "replays"
PAUSE = 8327
EVENTS = {"sirens": 9, "mermaid": 10}
TAIL = 11627


def set_condition(arm, raw, request):
    if request == {"event": "dolphins"}:
        source = checked_text(getsource(reactions.set_condition), {
            "event in ('wind', 'whale')": "event == 'dolphins'",
            "{'wind': 24, 'whale': 11}[event]": "12",
        })
        target = SimpleNamespace(ROM=build.ROM, CLEAN=build.CLEAN, ARM=build.ARM, NdsImage=base.NdsImage,
                                 BASE=earlier.BASE)
        env = vars(reactions) | {"stage": target, "__file__": __file__}
        exec(compile(source, __file__ + "::original-dolphin-condition", "exec"), env)
        return env["set_condition"](arm, raw, request)
    event, mode = request["event"], request["mode"]
    assert event in EVENTS and mode in ("choose", "restore")
    assert arm == base.NdsImage.open(build.ROM).read_file(build.ARM) and len(raw) == 0x400000
    original = base.NdsImage.open(build.CLEAN).read_file(build.ARM)
    at = earlier.FIELD-earlier.BASE
    assert arm[0x30F04:0x30F20] == original[0x30F04:0x30F20]
    assert arm[0x31EC0:0x325CC] == original[0x31EC0:0x325CC]
    assert arm[at:at+4] == earlier.ORIGINAL
    selected = EVENTS[event]
    override = (0xE3A00000 | selected).to_bytes(4, "little")
    before, after = (earlier.ORIGINAL, override) if mode == "choose" else (override, earlier.ORIGINAL)
    assert raw[at:at+4] == before
    changes = [dict(address=earlier.FIELD+i, before=x, after=y)
               for i, (x, y) in enumerate(zip(before, after, strict=True)) if x != y]
    return raw[:at]+after+raw[at+4:], dict(event=event, mode=mode, scoped_input=selected,
        instruction=earlier.FIELD, before=before.hex(), after=after.hex(), changes=changes,
        only_original_event_argument_forced=True, natural_random_selection_verified=False)


def schedule(event):
    if event == "dolphins":
        return dolphin.END, dolphin.COMMANDS
    commands = [dict(until=9627, condition_fixture={"event": event, "mode": "choose"}, buttons=["UP"], duration=400),
        dict(until=9827, condition_fixture={"event": event, "mode": "restore"}, buttons=["A"], duration=8)]
    commands.extend(dict(until=n, buttons=["A"], duration=8) for n in range(10027, 10828, 200))
    commands.extend([dict(until=TAIL), dict(stop=True)])
    return TAIL, commands


def run(event):
    staged = base.load(build.PROOF)
    assert base.digest(build.ROM) == staged["candidate_sha256"]
    terminal = base.load(earlier.OUT/"terminal.json")
    prior = base.load(terminal["report"])
    assert base.digest(terminal["report"]) == terminal["report_sha256"]
    inputs = earlier.OUT/"original_input_prefix.json"
    assert base.digest(inputs) == terminal["original_input_prefix_sha256"]
    donor = prior["battery_save_preloaded"]
    assert base.digest(donor["source"]) == donor["source_sha256"]
    folder = ROOT/event
    folder.mkdir(parents=True)
    end, commands = schedule(event)
    journal = folder/"commands.jsonl"
    journal.write_text("".join(json.dumps(c)+"\n" for c in commands), encoding="utf-8")
    argv = [sys.argv[0], "--rom", str(build.ROM), "--out", str(folder/"capture"), "--frames", str(end+1),
        "--inputs-json", str(inputs), "--battery-save", donor["source"], "--touchscreen",
        "--capture-every", "999999", "--pause-at", str(PAUSE), "--allow-condition-fixtures",
        "--dump-pause-ram", "--dump-ram"]
    stream = GrowingCommands(journal)
    setter, old_in, old_args = fixture_adapter.set_condition, sys.stdin, sys.argv
    try:
        fixture_adapter.set_condition, sys.stdin, sys.argv = set_condition, stream, argv
        emulator.main()
    finally:
        fixture_adapter.set_condition, sys.stdin, sys.argv = setter, old_in, old_args
        stream.close()
    path = folder/"capture/capture_report.json"
    report = base.load(path)
    assert report["frames"] == end and report["ROM_sha256"] == staged["candidate_sha256"]
    assert report["cold_boot"] and not report["savestate_loaded"] and not report["callback_errors"]
    assert base.digest(donor["source"]) == donor["source_sha256"]
    base.save(folder/"terminal.json", dict(candidate_sha256=report["ROM_sha256"], report=str(path),
        report_sha256=base.digest(path), commands=str(journal), commands_sha256=base.digest(journal)))


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("event", choices=("sirens", "mermaid", "dolphins"))
    run(parser.parse_args().event)
