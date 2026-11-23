"""Capture the processor and DMA state during the current Monster Fish transition."""

from types import FunctionType
from pathlib import Path

from scripts import play_special_target_battle_20261123 as previous
from scripts.stage_cartridge_title_20261123 import digest, read, write

RELEASE = Path("releases/all_routes_editorial_20261123_assigned_fleet_info_candidate/verification/registered_release_verification.json")
ROOT = previous.ROOT.with_name("monster_fish_transition_current_20261123")


def main():
    source_report = previous.ROOT / "fish_approach/capture/capture_report.json"
    old = read(source_report)
    release = read(RELEASE)
    assert digest(release["candidate"]) == release["candidate_sha256"]
    assert old["cold_boot"] and not old["callback_errors"]
    expected = old["battery_save_preloaded"]
    assert digest(expected["source"]) == expected["source_sha256"]
    root = ROOT / "current"
    assert not root.exists()
    ROOT.mkdir(exist_ok=True)
    journal = ROOT / "debug_commands.jsonl"
    # Same gameplay inputs up to the suspected stall. Export only the CPU/TCM
    # view at the two holds. The emulator never loads a serialized state.
    import json
    commands = [json.loads(line) for line in (previous.ROOT / "fish_approach/controller.jsonl").read_text(encoding="utf8").splitlines()]
    at_frame = 4800
    for item in commands:
        if at_frame in (7400, 10100):
            item.update(export_native_state=True)
        at_frame = item.get("until")
    journal.write_text("".join(json.dumps(item) + "\n" for item in commands), encoding="utf8")
    scope = vars(previous) | dict(ROOT=ROOT, RELEASE=RELEASE, __file__=__file__)
    FunctionType(previous.play.__code__, scope)("fish", "current", journal, None)
    report = read(root / "capture/capture_report.json")
    assert report["frames"] == 10100 and report["ROM_sha256"] == release["candidate_sha256"]
    assert report["battery_save_preloaded"]["source_sha256"] == expected["source_sha256"]
    assert not report["savestate_loaded"] and not report["callback_errors"]
    write(ROOT / "terminal.json", dict(capture=str(root / "capture/capture_report.json"),
          capture_sha256=digest(root / "capture/capture_report.json"), original_input_order_exact=True,
          latest_registered_release=release["candidate_sha256"], historical_capture_sha256=digest(source_report)))


if __name__ == "__main__":
    main()
