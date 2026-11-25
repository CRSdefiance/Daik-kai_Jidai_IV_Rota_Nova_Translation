"""Trace the current regional fleet orders and town attack eligibility panels."""

from inspect import getsource
from pathlib import Path

from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_setup_save_common_v1 as trace
from scripts import register_title_reports_label_20261123 as current


base = current.base
ROOT = Path(".codex-release-work/shared_display_20261123/regional_orders")
HISTORY = Path("work/emulation_v193/regional_missions_v617_actual/capture_report.json")
FRAMES = (7000, 9800, 10200, 15400, 15800, 20200, 20600, 24600, 26600,
          28600, 30600, 32200, 34600, 35400, 35800, 36200, 36600)


def schedule(case):
    assert case == "regional"
    prior = base.load(HISTORY)
    assert prior["cold_boot"] and not prior["savestate_loaded"] and not prior["callback_errors"]
    donor = prior["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"]
    assert base.digest(donor["source"]) == donor["source_sha256"] == "2bec91a13ba69361c5c79ff52dcc3c8a3d5cf2ccbe2fc4b614bac8d12ab4cee1"
    end = FRAMES[-1]
    inputs = [row for row in prior["scripted_input_schedule"] if row["start"] < end]
    return inputs, FRAMES, end, HISTORY, donor


def main():
    assert not (ROOT / "regional").exists()
    release = base.load(current.RELEASE)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    scope = vars(playback) | dict(ROOT=ROOT, parent=current, observer=trace.scoped_observer,
        get_schedule=schedule, FOCUS=set(range(3668)), __file__=__file__)
    exec(compile(getsource(playback.main), __file__ + "::registered-regional-order-controls", "exec"), scope)
    scope["main"]("regional")


if __name__ == "__main__":
    main()
