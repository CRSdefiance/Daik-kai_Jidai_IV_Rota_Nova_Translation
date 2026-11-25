"""Follow ordinary controller input on the registered ROM from a Ceuta save."""

import sys
from pathlib import Path

from scripts import headless_desmume_v193 as harness
from scripts import observe_setup_save_common_v1 as trace
from scripts import register_tavern_drink_reply_20261123 as current


base = current.base
ROOT = Path(".codex-release-work/shared_display_20261123/azores_voyage")
HISTORY = Path("work/emulation_v193/environment_voyage_v513/capture_report.json")
FIRST_PAUSE = 4400


def main():
    release = base.load(current.RELEASE)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(current.ROM) == release["candidate_sha256"]
    history = base.load(HISTORY)
    assert history["cold_boot"] and not history["savestate_loaded"] and not history["callback_errors"]
    assert not any(value for key, value in history.items() if key.startswith("synthetic_"))
    donor = history["battery_save_preloaded"]
    assert base.digest(donor["source"]) == donor["source_sha256"]
    ROOT.mkdir(parents=True, exist_ok=True)
    inputs = ROOT / "inputs.json"
    base.save(inputs, [row for row in history["scripted_input_schedule"] if row["start"] <= FIRST_PAUSE])
    trace_folder = ROOT / "trace"
    observer = trace.scoped_observer(current.ROM, trace_folder)
    native, original = harness.ct, sys.argv
    installed = []

    class CoreLoader:
        def __getattr__(self, name):
            return getattr(native, name)

        def CDLL(self, path, *args, **kwargs):
            library = native.CDLL(path, *args, **kwargs)
            if str(path).lower().endswith("desmume_libretro.dll"):
                watch = observer(library, trace_folder)
                watch.install()
                installed.append(watch)
                advance = library.retro_run
                advance.restype = None

                def tick():
                    watch.header[0] += 1
                    advance()

                library.retro_run = tick
            return library

    try:
        harness.ct = CoreLoader()
        sys.argv = [__file__, "--rom", str(current.ROM), "--out", str(ROOT / "capture"),
            "--frames", "90000", "--inputs-json", str(inputs), "--press-start", "-1",
            "--capture-every", "999999", "--battery-save", donor["source"], "--touchscreen",
            "--pause-at", str(FIRST_PAUSE), "--dump-pause-ram"]
        harness.main()
    finally:
        sys.argv, harness.ct = original, native
        for watch in installed:
            watch.close()
    watch, = installed
    watch.save()
    path = ROOT / "capture/capture_report.json"
    receipt = base.load(path)
    assert receipt["ROM_sha256"] == release["candidate_sha256"]
    assert receipt["cold_boot"] and not receipt["callback_errors"] and not receipt["savestate_loaded"]
    assert not any(value for key, value in receipt.items() if key.startswith("synthetic_"))
    assert base.digest(donor["source"]) == donor["source_sha256"]
    assert receipt["battery_save_preloaded"]["source_sha256"] == donor["source_sha256"]
    evidence = (path, trace_folder / "requests.json", ROOT / "capture/navigation_command_journal.json",
        trace_folder / "source_contract.json", inputs, HISTORY, Path(__file__))
    base.save(ROOT / "terminal.json", dict(candidate_sha256=release["candidate_sha256"],
        ordinary_controller_inputs=True, copied_save_sha256=donor["source_sha256"],
        total_frames=receipt["frames"], common_requests=watch.requests,
        evidence={str(p): base.digest(p) for p in evidence}))
    print(f"Verified ordinary voyage input through frame {receipt['frames']}.")


if __name__ == "__main__":
    main()
