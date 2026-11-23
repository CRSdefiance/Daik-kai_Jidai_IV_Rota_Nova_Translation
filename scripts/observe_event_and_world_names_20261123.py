"""Trace the Event and World class names through ordinary Forces Chart navigation."""

from inspect import getsource
from pathlib import Path
from types import SimpleNamespace

from scripts import observe_class_names_20261123 as labels
from scripts.reconcile_queued_sailing_hints_20261123 import RELEASE
from scripts.replay_forces_relationships_20261115 import REFERENCE
from scripts.source_locked_derivation_v5118 import checked_text


ROOT = labels.ROOT.parent / "event_and_world_names"
FRAMES = (13000, 13280, 13580, 13980, 14300)
EVENT, WORLD, HOME = 0x02276F88, 0x022CFD54, 0x0203CD24
OBJECT_CALLS = {0x02022ED4: EVENT, 0x02022EF8: EVENT,
                0x020CB10C: WORLD, 0x020CB3CC: WORLD}
REQUESTS = labels.playback.REQUESTS
FOCUS = {284, 318, 750, 751, 752}


def observer(rom, folder):
    source = checked_text(getsource(labels.observer), {
        "ORDER=ORDER, TARGETS=(*GETTERS, PAINTER, ORDER), __file__=__file__)":
            "ORDER=ORDER, OBJECT_CALLS=OBJECT_CALLS, REQUESTS=REQUESTS, HOME=HOME, "
            "TARGETS=(*GETTERS, PAINTER, *OBJECT_CALLS, *REQUESTS, HOME), __file__=__file__)",
        "    owner=None;text=None": """    if pc in REQUESTS:
     self.requests.append(dict(frame=frame,PC=pc,message_ID=v[REQUESTS[pc]],caller_LR=v[18]))
     return
    owner=None;text=None""",
        "assert pc==ORDER\n     vtable=None": """assert pc in OBJECT_CALLS or pc==HOME
     owner=v[4]
     if pc in OBJECT_CALLS and owner!=OBJECT_CALLS[pc]:return
     assert 0x02000000<=owner<0x023fff80
     vtable,=struct.unpack('<I',ct.string_at(self.wram+owner-0x02000000,4))
     key=pc,owner,v[18]
     if key in self.seen:return
     self.seen.add(key)""",
    })
    scope = vars(labels) | dict(HOME=HOME, OBJECT_CALLS=OBJECT_CALLS, REQUESTS=REQUESTS, __file__=__file__)
    exec(compile(source, __file__ + "::object-observer", "exec"), scope)
    return scope["observer"](rom, folder)


def schedule(case):
    assert case == "forces_chart"
    previous = labels.read(REFERENCE)
    assert tuple(previous["exact_requested_capture_frames"]) == FRAMES
    return previous["scripted_input_schedule"], FRAMES, previous["frames"], REFERENCE, previous["battery_save_preloaded"]


def main():
    release = labels.read(RELEASE)
    assert labels.digest("translations/release_stack.json") == release["registry_sha256"]
    parent = SimpleNamespace(ROM=Path(release["candidate"]), RELEASE=RELEASE)
    playback = labels.playback
    scope = vars(playback) | dict(ROOT=ROOT, parent=parent, observer=observer, FOCUS=FOCUS,
                                 get_schedule=schedule, __file__=__file__)
    exec(compile(getsource(playback.main), __file__ + "::ordinary-forces-chart", "exec"), scope)
    scope["main"]("forces_chart")


if __name__ == "__main__":
    main()
