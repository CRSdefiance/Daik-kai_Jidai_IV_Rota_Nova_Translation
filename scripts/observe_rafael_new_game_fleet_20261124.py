"""Trace fleet docking and destination fields through Rafael's ordinary New Game."""

from inspect import getsource
from pathlib import Path

from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_postload_fleet_fields_20261124 as postload
from scripts import register_deck_skill_guidance_20261124 as current
from scripts.source_locked_derivation_v5118 import checked_text
from scripts.stage_cartridge_title_20261123 import REGISTRY, digest, read


ROOT = current.ROM.parent.with_name("editorial_20261124_rafael_new_game_fleet_exact")
HISTORY = Path("out/rafael_preparation_gameplay_20261121/capture/capture_report.json")
PRIOR = HISTORY.parent.parent / "verified_preparation.json"
CASE = "rafael"
FRAMES = (100, 2190, 2790, 3280, 4001, 6500, 9600, 12000)
FIELDS = {base + index * stride: (field, index)
          for field, base, stride, count in (
              ("docking", 0x022CFDAC, 132, 64), ("destination", 0x022CFDAF, 132, 64),
              ("headquarters", 0x022D8E73, 76, 20))
          for index in range(count)}
ARCHIVED = {284, 318, 750, 751, 752}


def schedule(case):
    assert case == CASE
    history, prior = read(HISTORY), read(PRIOR)
    assert digest(HISTORY) == prior["report_sha256"] and prior["ordinary_new_game"]
    assert history["ROM_sha256"] == prior["candidate_sha256"]
    assert history["cold_boot"] and not history.get("battery_save_preloaded")
    assert not history["savestate_loaded"] and not history["callback_errors"]
    assert not any(value for key, value in history.items() if key.startswith("synthetic_"))
    events = [event for event in history["scripted_input_schedule"] if event["start"] < FRAMES[-1]]
    return events, FRAMES, FRAMES[-1] + 1, HISTORY, None


def observe(rom, folder):
    source = getsource(postload.observe)
    start = source.index("    release, saved = ")
    end = source.index("    source = checked_text", start)
    source = source[:start] + "    fields = FIELDS\n    first_frame = 0\n" + source[end:]
    source = checked_text(source, {"TARGETS=tuple(stores)": "TARGETS=(*playback.REQUESTS, *stores)"})
    region = vars(postload) | dict(FIELDS=FIELDS, playback=playback, __file__=__file__)
    exec(compile(source, __file__ + "::new-game-field-trace", "exec"), region)
    return region["observe"](rom, folder)


def main():
    release = read(current.RELEASE)
    assert digest(REGISTRY) == release["registry_sha256"] and digest(current.ROM) == release["candidate_sha256"]
    source = checked_text(getsource(playback.main), {
        "'--capture-at', *map(str, frames)]": "'--dump-capture-ram', '--capture-at', *map(str, frames)]",
    })
    scope = vars(playback) | dict(ROOT=ROOT, parent=current, get_schedule=schedule, observer=observe,
                                 FOCUS=ARCHIVED, __file__=__file__)
    exec(compile(source, __file__ + "::ordinary-rafael-new-game", "exec"), scope)
    scope["main"](CASE)


if __name__ == "__main__":
    main()
