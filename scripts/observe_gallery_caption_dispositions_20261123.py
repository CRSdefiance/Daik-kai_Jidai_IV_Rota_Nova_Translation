"""Trace all four original Gallery carousels on the registered testing build."""

from inspect import getsource
from pathlib import Path

from scripts import observe_online_gallery_common_v1 as replay
from scripts import register_ending_credit_spacing_20261123 as current
from scripts.source_locked_derivation_v5118 import checked_text


base = current.base
ROOT = Path(".codex-release-work/shared_display_20261123/gallery_dispositions")
CASE = "all_routes"
HISTORY = Path("out/online_and_gallery_common_consumers_20261111_v1/gallery/capture/capture_report.json")
CAPTIONS_PER_ROUTE = (46, 41, 39, 38)
ROUTE_BUTTONS = (None, [170, 50], [84, 130], [170, 130])
STEP = 180


def schedule(case):
    assert case == CASE
    previous = base.load(HISTORY)
    assert previous["cold_boot"] and not previous["savestate_loaded"] and not previous["callback_errors"]
    assert not any(value for key, value in previous.items() if key.startswith("synthetic_"))
    donor = previous["battery_save_preloaded"]
    assert donor["copied_byte_exact_before_cold_boot"] and base.digest(donor["source"]) == donor["source_sha256"]
    schedule = list(previous["scripted_input_schedule"][:7])
    assert schedule[-1]["start"] == 3001
    frame = 3200
    held, transitions = {}, []
    for route, (count, touch) in enumerate(zip(CAPTIONS_PER_ROUTE, ROUTE_BUTTONS, strict=True)):
        if touch is not None:
            schedule.extend((dict(start=frame + 1, duration=8, buttons=[], touch=touch),
                             dict(start=frame + STEP + 1, duration=8, buttons=["A"])))
            frame += STEP * 2
        holds = []
        for _ in range(count):
            holds.append(frame)
            schedule.append(dict(start=frame + 1, duration=8, buttons=["RIGHT"]))
            frame += STEP
        held[route] = holds
        held[f"wrapped_{route}"] = [frame]
        schedule.append(dict(start=frame + 1, duration=8, buttons=["B"]))
        frame += STEP * 2
        transitions.append(frame)
    for _ in range(2):
        schedule.append(dict(start=frame + 1, duration=8, buttons=["B"]))
        frame += STEP * 2
        transitions.append(frame)
    return schedule, sorted([*transitions, *(f for group in held.values() for f in group)]), frame, HISTORY, donor


def observe():
    release = base.load(current.RELEASE)
    assert base.digest(base.REGISTRY) == release["registry_sha256"]
    assert base.digest(current.ROM) == release["candidate_sha256"]
    trace_source = checked_text(getsource(replay.observer), {
        "key=pc,ptr,v[7]": "key=pc,ptr,v[7],v[11],v[12]",
    })
    bindings = vars(replay) | dict(ROOT=ROOT, parent=current, FOCUS=set(range(3668)), get_schedule=schedule)
    exec(compile(trace_source, __file__ + "::retain_every_caption_position", "exec"), bindings)
    exec(compile(getsource(replay.main), __file__ + "::registered_gallery_carousels", "exec"), bindings)
    bindings["main"](CASE)


if __name__ == "__main__":
    observe()
