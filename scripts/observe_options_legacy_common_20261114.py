"""Observe the current Sound Setup controls and the Sailing Help confirmation."""

from inspect import getsource
from pathlib import Path

from scripts import observe_online_gallery_common_v1 as playback
from scripts import observe_setup_save_common_v1 as trace
from scripts import register_alexandria_cooking_20261114 as current


ROOT = Path("work/options_legacy_common_20261114_v1")
FOCUS = {102, 330, 331, 332, 333}
KEYS = (
    (1601, "START"), (2001, "DOWN"), (2401, "A"), (2801, "A"),
    (3201, "L"), (3601, "RIGHT"), (4001, "L"), (4401, "A"),
    (4801, "R"), (5201, "LEFT"), (5601, "R"), (6001, "B"),
    (6401, "DOWN"), (6801, "DOWN"), (7201, "A"), (7601, "B"),
    (8001, "B"),
)


def schedule(case):
    assert case == "options"
    events = [dict(start=frame,duration=8,buttons=[key]) for frame,key in KEYS]
    return events, [frame + 199 for frame,_ in KEYS[2:]], 8250, None, None


def main():
    env = vars(playback) | dict(ROOT=ROOT, parent=current, FOCUS=FOCUS,
        observer=trace.scoped_observer, get_schedule=schedule, __file__=__file__)
    exec(compile(getsource(playback.main), __file__ + "::exact-ordinary-inputs-and-COMMON-observer", "exec"), env)
    env["main"]("options")


if __name__ == "__main__":
    main()

