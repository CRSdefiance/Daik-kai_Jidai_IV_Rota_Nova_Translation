"""Replay the ordinary Tripoli-to-Tunis voyage and recovery on the registered ROM."""

from argparse import ArgumentParser
from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_online_gallery_common_v1 as playback
from scripts.observe_setup_save_common_v1 import scoped_observer
from scripts.register_recruitment_shortfall_20261123 import RELEASE
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import REGISTRY, digest, read


ROOT = Path(".codex-release-work/shared_display_20261123/tripoli_tunis")
HISTORY = Path("work/emulation_v193/environment_voyage_v511/capture_report.json")
ROUTE_FRAMES = (3200, 3800, 4300, 4500, 5220, 6250, 6280, 7340, 7740, 10540,
                12140, 12940, 13340, 15000, 17540, 18740, 19540)
BATTLE_FRAMES = (3600, 4000, 7740, 10090, 11025, 11220, 11340, 11440, 11640, 12140)


def schedule(case):
    assert case in ("battle", "recovery")
    history = read(HISTORY)
    assert history["cold_boot"] and not history["savestate_loaded"] and not history["callback_errors"]
    assert not any(value for key, value in history.items() if key.startswith("synthetic_"))
    donor = history["battery_save_preloaded"]
    assert digest(donor["source"]) == donor["source_sha256"]
    frames = BATTLE_FRAMES if case == "battle" else ROUTE_FRAMES
    inputs = [entry for entry in history["scripted_input_schedule"] if entry["start"] <= frames[-1]]
    port = dict(start=3201 if case == "battle" else 3401, duration=8, buttons=[], touch=[230, 40])
    if case == "recovery":
        inputs = [entry for entry in inputs if entry["start"] not in (3401, 4001)]
    return sorted([*inputs, port], key=lambda entry: entry["start"]), frames, frames[-1], HISTORY, donor


def main(case):
    release = read(RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"]
    scope = vars(playback) | dict(ROOT=ROOT, parent=SimpleNamespace(RELEASE=RELEASE, ROM=Path(release["candidate"])),
        observer=scoped_observer, get_schedule=schedule, FOCUS=set(range(3668)), __file__=__file__)
    source = checked_text(getsource(playback.main), {
        "    installed = []": "    argv += ['--dump-capture-ram']\n    installed = []",
    })
    exec(compile(source, __file__ + "::tripoli-tunis-ordinary", "exec"), scope)
    scope["main"](case)


if __name__ == "__main__":
    cli = ArgumentParser(description=__doc__)
    cli.add_argument("case", choices=("battle", "recovery"))
    main(cli.parse_args().case)
