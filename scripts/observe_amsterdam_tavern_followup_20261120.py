"""Extend the Amsterdam Tavern replay on the registered build with original input."""

import sys
from argparse import ArgumentParser
from pathlib import Path

from scripts import headless_desmume_v193 as harness
from scripts import observe_setup_save_common_v1 as trace
from scripts import register_damaged_save_digits_20261120 as current
from scripts.check_amsterdam_tavern_editorial_20261120 import REPLAY
from scripts.run_activity_special_live_v988 import GrowingCommands


base = current.base
START = 24550


def verified_schedule(root, events, capture):
    journal = base.load(root / "capture/navigation_command_journal.json")
    commands = journal["commands_received"]
    assert journal["ROM_sha256"] == capture["ROM_sha256"]
    assert all(row["validation_passed"] for row in commands)
    assert commands[0]["frame"] == START and commands[-1] == {
        "frame": capture["frames"], "command": {"stop": True}, "validation_passed": True}
    assert journal["last_command_frame"] == capture["frames"]
    appended = []
    for previous, following in zip(commands, commands[1:]):
        command = previous["command"]
        assert command["until"] == following["frame"]
        if command.get("buttons") or "touch" in command:
            event = dict(start=previous["frame"] + 1, duration=command.get("duration", 12),
                         buttons=command.get("buttons", []))
            if "touch" in command:
                event["touch"] = command["touch"]
            appended.append(event)
    assert capture["scripted_input_schedule"] == events + appended
    return appended


def main(root, observe):
    release = base.load(current.RELEASE)
    previous = base.load(REPLAY / "capture_report.json")
    rom = current.stage.ROOT / "clean_rebuilt.nds"
    assert base.digest(rom) == base.digest(current.ROM) == release["candidate_sha256"]
    assert previous["cold_boot"] and not previous["savestate_loaded"] and not previous.get("battery_save_preloaded")
    assert not previous["callback_errors"] and not any(v for k, v in previous.items() if k.startswith("synthetic_"))
    events = previous["scripted_input_schedule"]
    assert previous["frames"] >= START > max(row["start"] + row.get("duration", 8) for row in events)
    journal = root / "navigation.jsonl"
    assert journal.is_file() and not (root / "capture").exists()
    source = root / "prefix_inputs.json"
    base.save(source, events)
    trace_dir = root / "observer"
    observer = trace.scoped_observer(rom, trace_dir) if observe else None
    old_ct, old_argv, old_stdin = harness.ct, sys.argv, sys.stdin
    stream = GrowingCommands(journal)
    attached = []

    class CoreLoader:
        def __getattr__(self, name):
            return getattr(old_ct, name)

        def CDLL(self, path, *args, **kwargs):
            core = old_ct.CDLL(path, *args, **kwargs)
            if str(path).lower().endswith("desmume_libretro.dll"):
                recorder = observer(core, trace_dir)
                recorder.install()
                attached.append(recorder)
                advance = core.retro_run
                advance.restype = None

                def tick():
                    recorder.header[0] += 1
                    advance()

                core.retro_run = tick
            return core

    try:
        harness.ct, sys.stdin = (CoreLoader() if observe else old_ct), stream
        sys.argv = [harness.__file__, "--rom", str(rom), "--out", str(root / "capture"),
                    "--frames", "55000", "--inputs-json", str(source), "--press-start", "-1", "--touchscreen",
                    "--capture-every", "999999", "--pause-at", str(START)]
        harness.main()
    finally:
        harness.ct, sys.argv, sys.stdin = old_ct, old_argv, old_stdin
        stream.close()
        for recorder in attached:
            recorder.close()
    if observe:
        recorder, = attached
        recorder.save()
        print(f"Observed {sum(row['frame'] > START for row in recorder.requests)} shared requests after the Tavern return.")
    capture = base.load(root / "capture/capture_report.json")
    assert capture["ROM_sha256"] == release["candidate_sha256"]
    verified_schedule(root, base.load(source), capture)
    assert capture["cold_boot"] and not capture["savestate_loaded"] and not capture.get("battery_save_preloaded")
    assert not capture["callback_errors"] and not any(v for k, v in capture.items() if k.startswith("synthetic_"))


if __name__ == "__main__":
    parser = ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--observe", action="store_true")
    args = parser.parse_args()
    main(args.root, args.observe)
